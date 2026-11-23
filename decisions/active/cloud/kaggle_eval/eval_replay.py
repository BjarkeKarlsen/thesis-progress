"""Replay the test of one trained run on Kaggle with the served counts ([A96]), as a script kernel.

push_replay.sh fills in the settings, uploads the run folder as a private dataset and pushes this
script. The same replay as the fleet 16 replays on the PC (replay_served_2026-11-16, replay_r1):
only the chosen checkpoint, read back from the run's validation rows (--chosen-only), plays 20
test seeds of 10000 steps with a 5000-step warm-up. A run trained under fixed storage plays under
fixed (Regime 2) and congestion-aware storage (Regime 1), the others under the rule they trained
with. Branch replay/served-counts. Everything lands in /kaggle/working/evaluation.
"""

import os
import shutil
import subprocess
import sys
import tarfile
import time

START = time.time()

# ------------------------------------------------------------------ settings, filled in by push_eval.sh
BRANCH = "@BRANCH@"   # main, or a branch with a needed option (feat/parallel-evaluation for WORKERS)
WORKERS = @WORKERS@        # evaluate --workers, episodes played at once (1 = the plain evaluate)
REGIME = "@REGIME@"     # the rule the run trained with
HOURS = 11.5            # stop cleanly before Kaggle's 12 h limit. Test rows already written stay


def run(cmd, **kwargs):
    print("+", " ".join(cmd), flush=True)
    return subprocess.run(cmd, check=True, **kwargs)


os.chdir("/kaggle/working")
run(["git", "clone", "--depth", "1", "--branch", BRANCH,
     "https://github.com/BjarkeKarlsen/slap-mapd-coupling.git", "code"])
run([sys.executable, "-m", "pip", "install", "-q", "-e", "code", "ray[rllib]==2.57.0"])
COMMIT = subprocess.run(["git", "-C", "code", "rev-parse", "HEAD"],
                        capture_output=True, text=True).stdout.strip()
print(COMMIT, "on", os.cpu_count(), "cores", flush=True)

# ------------------------------------------------------------------ the run folder, from the dataset
# The dataset holds run.tar (the run folder as it is at home). Kaggle may hand it over as the
# file or already unpacked, so both are looked for. The input is read-only, so it is copied.
RUN = "/kaggle/working/run"
found_tar = found_dir = None
for root, dirs, files in os.walk("/kaggle/input"):
    if "run.tar" in files:
        found_tar = os.path.join(root, "run.tar")
    if any(f.endswith("_spec.json") for f in files) and "commit.txt" in files:
        found_dir = root
if found_tar:
    with tarfile.open(found_tar) as tar:
        tar.extractall("/kaggle/working")   # the tar holds the folder "run"
elif found_dir:
    shutil.copytree(found_dir, RUN)
else:
    sys.exit("No run.tar or run folder in /kaggle/input")
print("run folder", os.listdir(RUN), flush=True)

# ------------------------------------------------------------------ the warehouse tables
# evaluate reads the window tables of the validation and test seeds, so they are prepared
# first from the run's own spec. A table dataset attached by push_eval.sh is copied in, as in
# train.py, and only the seeds it lacks are built.
STORE = "/kaggle/warehouses_store"
os.makedirs(STORE, exist_ok=True)
# The policy keeps the table folder of the machine it trained on (/tmp/warehouses on Kaggle,
# /content/warehouses on Colab, ~/thesis_runs/warehouses at home) and reads its tables there,
# so every one of those names points at the one store.
for alias in ("/tmp/warehouses", "/content/warehouses",
              os.path.expanduser("~/thesis_runs/warehouses")):
    if alias != STORE and not os.path.exists(alias):
        os.makedirs(os.path.dirname(alias), exist_ok=True)
        os.symlink(STORE, alias)
for root, _, files in os.walk("/kaggle/input"):
    if "pool_key.txt" in files:
        key = open(os.path.join(root, "pool_key.txt")).read().strip()
        target = os.path.join(STORE, key)
        if not os.path.isdir(target):
            shutil.copytree(root, target,
                            ignore=shutil.ignore_patterns("pool_key.txt", "dataset-metadata.json"))
        print("warehouse tables", key, len(os.listdir(target)), "files", flush=True)
SPEC = next(os.path.join(RUN, f) for f in os.listdir(RUN) if f.endswith("_spec.json"))
os.makedirs("/tmp/ray_e", exist_ok=True)
base_env = dict(os.environ, RAY_TMPDIR="/tmp/ray_e", PYTHONUNBUFFERED="1",
                SLAP_WAREHOUSE_STORE=STORE)
run([sys.executable, "-m", "slap_mapd_coupling.main", "prepare-warehouses", "--config", SPEC,
     "--workers", str(os.cpu_count())], cwd="code", env=base_env)

# ------------------------------------------------------------------ evaluate
EVAL = "/kaggle/working/evaluation"
os.makedirs(EVAL, exist_ok=True)
# A test that ran out of time before: push_eval.sh RESUME_ROWS=... sends its test.jsonl as
# resume_test.jsonl, and evaluate --resume (feat/evaluate-resume) plays only the missing episodes.
resume = []
for root, _, files in os.walk("/kaggle/input"):
    if "resume_test.jsonl" in files:
        shutil.copy(os.path.join(root, "resume_test.jsonl"), f"{EVAL}/test.jsonl")
        resume = ["--resume"]
        print("resuming from", sum(1 for _ in open(f"{EVAL}/test.jsonl")), "test rows", flush=True)
modes = ["--storage-modes", "fixed", "--storage-modes", "congestion"] if REGIME == "fixed" else []
cmd = [sys.executable, "-m", "slap_mapd_coupling.main", "evaluate", RUN, "--chosen-only",
       "--test-seeds", "20", "--horizon", "10000", "--warmup", "5000", "--output", EVAL, *modes,
       "--workers", str(WORKERS), *resume]
left = int(HOURS * 3600 - (time.time() - START))
print("+", " ".join(cmd), f"(time left {left} s)", flush=True)
env = dict(base_env, OMP_NUM_THREADS="1", MKL_NUM_THREADS="1")
with open(f"{EVAL}/evaluate.log", "a") as log:
    process = subprocess.Popen(["timeout", "--signal=INT", f"{left}s", *cmd], cwd="code",
                               env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               text=True, bufsize=1)
    for line in process.stdout:
        log.write(line)
        log.flush()
        print(line, end="", flush=True)
    code = process.wait()

print("evaluate exit code", code)
if code == 0:
    open(f"{EVAL}/done", "w").write(f"kaggle, commit {COMMIT}\n")
    print("Finished. Download the output.")
else:
    print("Not finished. The test rows written so far are in evaluation/test.jsonl.")
# Only the evaluation is new, so the run folder stays out of the output.
shutil.rmtree(RUN, ignore_errors=True)
shutil.rmtree("/kaggle/working/code", ignore_errors=True)
