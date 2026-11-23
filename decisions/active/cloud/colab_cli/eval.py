"""Evaluate trained runs on a Colab machine, started by colab_eval.bash.

colab_eval.bash uploads this file, /content/eval_job.json and one /content/in/<name>.tgz per run,
and starts it in the background. Every run is evaluated at the same time, one process each with
one thread, as on the PC queue (queue_2026-11-13_fleet16_cng/run.sh): 5 validation seeds choose
the checkpoint ([A60]), then the chosen and the last checkpoint play 20 test seeds of 10000 steps
with a 5000-step warm-up, under the storage rules the job names for that run.

    /content/code              the repo at the commit in eval_job.json
    /content/runs/<name>       the run folder (its validation rows are written here)
    /content/evals/<name>      validation.jsonl, test.jsonl, summary.md, evaluate.log, done
    /content/state.txt         installing, warehouses, evaluating, finished or failed
"""

import json
import os
import subprocess
import sys

JOB = json.load(open("/content/eval_job.json"))
CODE = "/content/code"
STATE = "/content/state.txt"


def state(word):
    with open(STATE, "w") as f:
        f.write(word + "\n")
    print("state:", word, flush=True)


def run(cmd, **kwargs):
    print("+", " ".join(cmd), flush=True)
    return subprocess.run(cmd, check=True, **kwargs)


try:
    state("installing")
    if not os.path.isdir(f"{CODE}/.git"):
        run(["git", "init", "-q", CODE])
        run(["git", "-C", CODE, "remote", "add", "origin",
             "https://github.com/BjarkeKarlsen/slap-mapd-coupling.git"])
        run(["git", "-C", CODE, "fetch", "-q", "--depth", "1", "origin", JOB["commit"]])
        run(["git", "-C", CODE, "checkout", "-q", "FETCH_HEAD"])
        # Uncommitted changes on top of the commit (PATCH in colab_eval.bash).
        if os.path.exists("/content/code.patch"):
            run(["git", "-C", CODE, "apply", "/content/code.patch"])
    run([sys.executable, "-m", "pip", "install", "-q", "-e", CODE, "ray[rllib]==2.57.0"])
    print(JOB["commit"], "on", os.cpu_count(), "cores", flush=True)

    # evaluate reads the window tables of the validation and test seeds, so they are prepared
    # first from each run's own spec (one pool per key, the runs of an arm share it).
    STORE = "/content/warehouses_store"
    os.makedirs(STORE, exist_ok=True)
    # The policy keeps the table folder of the machine it trained on (/tmp/warehouses on Kaggle,
    # /content/warehouses on Colab, ~/thesis_runs/warehouses at home) and reads its tables there,
    # so every one of those names points at the one store.
    for alias in ("/tmp/warehouses", "/content/warehouses",
                  os.path.expanduser("~/thesis_runs/warehouses")):
        if alias != STORE and not os.path.exists(alias):
            os.makedirs(os.path.dirname(alias), exist_ok=True)
            os.symlink(STORE, alias)
    base_env = dict(os.environ, PYTHONUNBUFFERED="1", SLAP_WAREHOUSE_STORE=STORE)
    state("warehouses")
    # Tables sent from home (tables_<key>.tgz) go into the store first, so only missing seeds are built.
    for name in sorted(os.listdir("/content/in")) if os.path.isdir("/content/in") else []:
        if name.startswith("tables_") and name.endswith(".tgz"):
            run(["tar", "-xzf", f"/content/in/{name}", "-C", STORE])
            os.remove(f"/content/in/{name}")
    for item in JOB["runs"]:
        run_dir, archive = f"/content/runs/{item['name']}", f"/content/in/{item['name']}.tgz"
        os.makedirs(run_dir, exist_ok=True)
        if os.path.exists(archive):
            run(["tar", "-xzf", archive, "-C", run_dir])
            os.remove(archive)
        spec = next(f"{run_dir}/{f}" for f in os.listdir(run_dir) if f.endswith("_spec.json"))
        run([sys.executable, "-m", "slap_mapd_coupling.main", "prepare-warehouses",
             "--config", spec, "--workers", str(os.cpu_count())], cwd=CODE,
            env=dict(base_env, RAY_TMPDIR="/tmp/ray_w"))

    state("evaluating")
    processes = {}
    for item in JOB["runs"]:
        name = item["name"]
        run_dir, out = f"/content/runs/{name}", f"/content/evals/{name}"
        if os.path.exists(f"{out}/done"):
            continue
        os.makedirs(out, exist_ok=True)
        ray_tmp = f"/tmp/ray_{len(processes)}"
        os.makedirs(ray_tmp, exist_ok=True)
        modes = [arg for mode in item["modes"] for arg in ("--storage-modes", mode)]
        cmd = [sys.executable, "-m", "slap_mapd_coupling.main", "evaluate", run_dir,
               "--validation-seeds", "5", "--test-seeds", "20", "--horizon", "10000",
               "--warmup", "5000", "--output", out, *modes,
               *(["--workers", str(item["workers"])] if item.get("workers", 1) > 1 else []),
               *JOB.get("extra", [])]
        print("+", " ".join(cmd), flush=True)
        env = dict(base_env, RAY_TMPDIR=ray_tmp, OMP_NUM_THREADS="1", MKL_NUM_THREADS="1")
        log = open(f"{out}/evaluate.log", "a")
        processes[name] = (subprocess.Popen(cmd, cwd=CODE, env=env, stdout=log,
                                            stderr=subprocess.STDOUT), out)
    codes = {}
    for name, (process, out) in processes.items():
        codes[name] = process.wait()
        print(name, "exit", codes[name], flush=True)
        if codes[name] == 0:
            open(f"{out}/done", "w").write(f"colab, commit {JOB['commit']}\n")
    state("finished " + " ".join(f"{n}={c}" for n, c in codes.items()))
except Exception as error:  # noqa: BLE001, the state file must say why it stopped
    print("failed:", repr(error), flush=True)
    state(f"failed {error!r}")
