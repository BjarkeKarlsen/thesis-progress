"""Colab lane of the performance test (author 2026-11-24): plays the episodes perf_colab.sh claimed
at home, with the same job.sh as the PC and the Lenovo, on a CPU high-mem machine.

perf_colab.sh uploads this file, /content/perf_job.json, /content/job.sh, /content/in/runs.tgz
(the run folders, relative to ~/thesis_runs) and /content/in/warehouses.tgz (the prepared stores).

    /root/code/main                          the repo at the commit in perf_job.json
    /root/thesis_runs/...                    runs and warehouses, laid out as at home
    /root/thesis_runs/scaling_2026-11/perf   rows/ and logs/ as job.sh writes them
    /content/state.txt                       installing, smoke, running k/n, finished or failed
"""

import json
import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

JOB = json.load(open("/content/perf_job.json"))
HOME = "/root"
TR = f"{HOME}/thesis_runs"
CODE = f"{HOME}/code/main"
P = f"{TR}/scaling_2026-11/perf"
STORE = f"{TR}/warehouses"
STATE = "/content/state.txt"


def state(word):
    with open(STATE, "w") as f:
        f.write(word + "\n")
    print("state:", word, flush=True)


def run(cmd, **kwargs):
    print("+", " ".join(cmd), flush=True)
    return subprocess.run(cmd, check=True, **kwargs)


def done_count():
    return sum(os.path.exists(f"{P}/logs/{m}_{a}_{s}.exit") for m, a, s, _, _ in JOB["jobs"])


try:
    state("installing")
    if not os.path.isdir(f"{CODE}/.git"):
        run(["git", "init", "-q", CODE])
        run(["git", "-C", CODE, "remote", "add", "origin",
             "https://github.com/BjarkeKarlsen/slap-mapd-coupling.git"])
        run(["git", "-C", CODE, "fetch", "-q", "--depth", "1", "origin", JOB["commit"]])
        run(["git", "-C", CODE, "checkout", "-q", "FETCH_HEAD"])
    run([sys.executable, "-m", "pip", "install", "-q", "-e", CODE, "ray[rllib]==2.57.0"])
    print(JOB["commit"], "on", os.cpu_count(), "cores", flush=True)

    os.makedirs(STORE, exist_ok=True)
    os.makedirs(f"{P}/rows", exist_ok=True)
    os.makedirs(f"{P}/logs", exist_ok=True)
    shutil.copy("/content/job.sh", f"{P}/job.sh")
    for name, dest in (("runs.tgz", TR), ("warehouses.tgz", STORE)):
        if os.path.exists(f"/content/in/{name}"):
            run(["tar", "-xzf", f"/content/in/{name}", "-C", dest])
            os.remove(f"/content/in/{name}")
    # Runs trained on Colab or Kaggle name their own table folder; every name points at the store.
    for alias in ("/content/warehouses", "/tmp/warehouses"):
        if not os.path.exists(alias):
            os.symlink(STORE, alias)

    # Smoke test: a few steps of the most expensive job, on a copy of the stores, so its shorter
    # horizon cannot touch the stores the real episodes read.
    state("smoke")
    m, arm, seed, run_rel, ck_rel = JOB["jobs"][-1]
    smoke_store = "/content/smoke_store"
    if not os.path.exists(smoke_store):
        shutil.copytree(STORE, smoke_store, symlinks=True)
    cfg = "decentralised" if arm == "decentralised_comm" else arm
    extra = ["--sections", str(2 if m == 8 else 3 * m // 16)] if arm == "section" else []
    run([sys.executable, "-m", "slap_mapd_coupling.training.scaling_probe", f"{TR}/{run_rel}",
         f"{TR}/{ck_rel}", "--target", f"configs/fleet_{m}/{cfg}.yaml", *extra,
         "--steps", "40", "--warmup", "20", "--seed", str(seed),
         "--pool-seeds", *[str(s) for s in range(200000, 200020)],
         "--output", "/content/smoke.jsonl"], cwd=CODE,
        env=dict(os.environ, PYTHONPATH="src", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1",
                 SLAP_WAREHOUSE_STORE=smoke_store, RAY_TMPDIR="/var/tmp/ray_smoke"))
    print("smoke row:", open("/content/smoke.jsonl").read()[:300], flush=True)
    if JOB.get("smoke_only"):
        state("finished smoke")
        sys.exit(0)

    def play(job):
        m, arm, seed, run_rel, ck_rel = job
        if os.path.exists(f"{P}/logs/{m}_{arm}_{seed}.exit"):
            return
        subprocess.run(["bash", f"{P}/job.sh", str(m), arm, str(seed), run_rel, ck_rel],
                       env=dict(os.environ, HOME=HOME, P=P, W=CODE, PY=sys.executable))
        state(f"running {done_count()}/{len(JOB['jobs'])}")

    state(f"running {done_count()}/{len(JOB['jobs'])}")
    with ThreadPoolExecutor(JOB["lanes"]) as pool:
        list(pool.map(play, JOB["jobs"]))
    state(f"finished {done_count()}/{len(JOB['jobs'])}")
except Exception as error:  # noqa: BLE001
    print("failed:", error, flush=True)
    state("failed")
