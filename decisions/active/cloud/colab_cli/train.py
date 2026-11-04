"""Train one arm of slap-mapd-coupling on a Colab machine, started by colab.bash.

colab.bash uploads this file and /content/job.json, and starts it in the background, so the
training keeps going when the terminal at home disconnects. Everything happens on the machine's
own disk. colab.bash copies the run home now and then, since Drive cannot be mounted from the
command line.

    /content/code         the repo at the commit in job.json
    /content/warehouses   the warehouse tables (SLAP_WAREHOUSE_STORE), uploaded from home or built
    /content/run          the run folder, uploaded from home when the run is continued
    /content/state.txt    one word that colab.bash reads: installing, warehouses, training,
                          finished or failed, with the exit code
"""

import json
import os
import subprocess
import sys

JOB = json.load(open("/content/job.json"))
CODE, STORE, RUN = "/content/code", "/content/warehouses", "/content/run"
STATE = "/content/state.txt"


def state(word):
    with open(STATE, "w") as f:
        f.write(word + "\n")
    print("state:", word, flush=True)


def run(cmd, **kwargs):
    print("+", " ".join(cmd), flush=True)
    return subprocess.run(cmd, check=True, **kwargs)


try:
    # ------------------------------------------------------------------ the code, the same Ray as at home
    state("installing")
    if not os.path.isdir(f"{CODE}/.git"):
        run(["git", "init", "-q", CODE])
        run(["git", "-C", CODE, "remote", "add", "origin",
             "https://github.com/BjarkeKarlsen/slap-mapd-coupling.git"])
        run(["git", "-C", CODE, "fetch", "-q", "--depth", "1", "origin", JOB["commit"]])
        run(["git", "-C", CODE, "checkout", "-q", "FETCH_HEAD"])
        # Uncommitted changes to try before they are on GitHub (PATCH in colab.bash).
        if os.path.exists("/content/code.patch"):
            run(["git", "-C", CODE, "apply", "/content/code.patch"])
    run([sys.executable, "-m", "pip", "install", "-q", "-e", CODE, "ray[rllib]==2.57.0"])
    print(JOB["commit"], "on", os.cpu_count(), "cores", flush=True)
    if JOB.get("learner_cpus") is None:
        JOB["learner_cpus"] = max(1, os.cpu_count() - JOB["runners"])

    # ------------------------------------------------------------------ the run folder and its config
    os.makedirs(RUN, exist_ok=True)
    resume = any(name.endswith("_spec.json") for name in os.listdir(RUN))
    with open(f"{RUN}/commit.txt", "a") as f:
        f.write(f"{JOB['commit']} colab {JOB['controller']} fleet {JOB['fleet']} "
                f"{JOB['regime']}\n")
    config = f"{CODE}/configs/fleet_{JOB['fleet']}/{JOB['controller']}.yaml"
    if JOB["regime"] == "matched" and not resume:
        # As bedtime.bash does: trained under the rule it is evaluated in, demand storage.
        import yaml
        data = yaml.safe_load(open(config))
        data.update(regime="matched", evaluation_storage_mode="demand")
        config = f"{RUN}/config.yaml"
        yaml.safe_dump(data, open(config, "w"), sort_keys=False)

    env = dict(os.environ, RAY_TMPDIR="/tmp/ray_c", SLAP_WAREHOUSE_STORE=STORE,
               PYTHONUNBUFFERED="1")
    os.makedirs("/tmp/ray_c", exist_ok=True)

    # ------------------------------------------------------------------ the warehouse tables
    # Seeds already stored (uploaded from home) are skipped, so this only builds what is missing.
    state("warehouses")
    run([sys.executable, "-m", "slap_mapd_coupling.main", "prepare-warehouses",
         "--config", config, "--workers", str(os.cpu_count())], cwd=CODE, env=env)

    # ------------------------------------------------------------------ train
    # timeout sends Ctrl-C after the hours, Ray stops cleanly, and `resume` can continue the run.
    state("training")
    if resume:
        cmd = [sys.executable, "-m", "slap_mapd_coupling.main", "resume", RUN]
    else:
        cmd = [sys.executable, "-m", "slap_mapd_coupling.main", "train", "--config", config,
               "--controller", JOB["controller"], "--regime", JOB["regime"],
               "--env-runners", str(JOB["runners"]), "--checkpoint-every", "3",
               "--output", RUN]
        # The cores the runners leave go to the learner's update (--learner-cpus), which
        # changes no result. A resumed run keeps what it started with.
        if JOB.get("learner_cpus", 1) > 1:
            cmd += ["--learner-cpus", str(JOB["learner_cpus"])]
        cmd += ["--budget-env-steps", str(JOB["budget"])] if JOB.get("budget") else []
    print("+", " ".join(cmd), flush=True)
    with open(f"{RUN}/train.log", "a") as log:
        code = subprocess.run(["timeout", "--signal=INT", f"{JOB['hours']}h", *cmd], cwd=CODE,
                              env=env, stdout=log, stderr=subprocess.STDOUT).returncode
    if code == 0:
        open(f"{RUN}/done", "w").write(f"colab, commit {JOB['commit']}\n")
    state(f"finished {code}")
except Exception as error:  # noqa: BLE001, the state file must say why it stopped
    print("failed:", repr(error), flush=True)
    state(f"failed {error!r}")
