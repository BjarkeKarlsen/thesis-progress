"""Play policies for one very long episode each on Kaggle, no training, with a per-step trace, to
see after how many steps a policy breaks down (author, 2026-11-18). push_long_episode.sh uploads
the policies as a private dataset (run_<label>/: the run's spec and one checkpoint) and fills in
the settings. Each policy plays SEEDS test seeds of STEPS steps, no warm-up, its training rule.
Branch replay/served-counts (the code of the fleet 16 replays). Output in /kaggle/working/long.
"""
import glob, os, subprocess, sys, tarfile, time
from concurrent.futures import ProcessPoolExecutor, as_completed

START = time.time()
BRANCH = "@BRANCH@"
STEPS = @STEPS@
SEEDS = [@SEEDS@]
HOURS = 11.5

def run(cmd, **kw):
    print("+", " ".join(cmd), flush=True); return subprocess.run(cmd, check=True, **kw)

os.chdir("/kaggle/working")
run(["git", "clone", "--depth", "1", "--branch", BRANCH,
     "https://github.com/BjarkeKarlsen/slap-mapd-coupling.git", "code"])
run([sys.executable, "-m", "pip", "install", "-q", "-e", "code", "ray[rllib]==2.57.0"])
COMMIT = subprocess.run(["git", "-C", "code", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
print(COMMIT, "on", os.cpu_count(), "cores", flush=True)
tars = glob.glob("/kaggle/input/**/policies.tar", recursive=True)
if tars:
    with tarfile.open(tars[0]) as t: t.extractall("/kaggle/working/policies")
else:
    found = glob.glob("/kaggle/input/**/run_*", recursive=True)
    os.makedirs("/kaggle/working/policies", exist_ok=True)
    for f in found: subprocess.run(["cp", "-r", f, "/kaggle/working/policies/"], check=True)
POLICIES = sorted(glob.glob("/kaggle/working/policies/run_*"))
print("policies", POLICIES, flush=True)
STORE = "/kaggle/warehouses_store"; os.makedirs(STORE, exist_ok=True)
for alias in ("/tmp/warehouses", "/content/warehouses", os.path.expanduser("~/thesis_runs/warehouses")):
    if not os.path.exists(alias):
        os.makedirs(os.path.dirname(alias), exist_ok=True); os.symlink(STORE, alias)
os.environ.update(SLAP_WAREHOUSE_STORE=STORE, OMP_NUM_THREADS="1", MKL_NUM_THREADS="1", PYTHONUNBUFFERED="1")
sys.path.insert(0, "/kaggle/working/code/src")
OUT = "/kaggle/working/long"; os.makedirs(OUT, exist_ok=True)

def one(job):
    import json
    from pathlib import Path
    import torch
    torch.set_num_threads(1)
    from slap_mapd_coupling.training.evaluate_run import _studies, play
    run_dir, seed = job
    label = os.path.basename(run_dir).removeprefix("run_")
    _, _, spec, study = _studies(Path(run_dir), None, None, None, STEPS, 0)
    ck = Path(glob.glob(f"{run_dir}/*/PPO_*/checkpoint_*")[0])
    t = time.time()
    m = play(study, spec, ck, seed, None, Path(f"{OUT}/trace_{label}_seed{seed}.jsonl"))
    row = {"label": label, "checkpoint": ck.name, "seed": seed, "steps": STEPS,
           "play_seconds": time.time() - t, "commit": COMMIT, **m.model_dump(mode="json")}
    with open(f"{OUT}/rows.jsonl", "a") as f: f.write(json.dumps(row) + "\n")
    return label, seed, row["play_seconds"]

if __name__ == "__main__":
    # The warehouse tables of each seed, built once before the episodes start.
    for p in POLICIES:
        spec = glob.glob(f"{p}/*_spec.json")[0]
        run([sys.executable, "-m", "slap_mapd_coupling.main", "prepare-warehouses", "--config", spec,
             "--workers", str(os.cpu_count())], cwd="code")
    jobs = [(p, s) for s in SEEDS for p in POLICIES]
    with ProcessPoolExecutor(max_workers=os.cpu_count()) as ex:
        futs = [ex.submit(one, j) for j in jobs]
        for f in as_completed(futs, timeout=HOURS * 3600 - (time.time() - START)):
            try: print("done", f.result(), flush=True)
            except Exception as e: print("failed", repr(e), flush=True)
    open(f"{OUT}/done", "w").write(f"kaggle, commit {COMMIT}\n")
    subprocess.run(["rm", "-rf", "/kaggle/working/code", "/kaggle/working/policies"])
