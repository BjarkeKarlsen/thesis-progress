"""Train one arm of slap-mapd-coupling on Kaggle, as a script kernel.

Pushed and started from home with the Kaggle command line (see ../kaggle.md):

    kaggle kernels push -p thesis-progress/decisions/active/cloud/kaggle_kernel

Edit the settings below, push, and download the run folder when it is done. Everything the run
writes is in /kaggle/working/run, which Kaggle keeps as the kernel's output.
"""

import os
import shutil
import subprocess
import sys

# ------------------------------------------------------------------ settings, the only part to edit
BRANCH = "feat/warm-start-a93"                       # a pushed branch of slap-mapd-coupling
CONTROLLER = "decentralised"          # or "centralised", "section"
FLEET = 16                            # 8, 16, 32 or 64
REGIME = "demand"   # the storage rule it trains under: "fixed", "demand" or "congestion"
COMMUNICATION = False                 # True: decentralised with local communication (RQ5)
HOURS = 5.5                           # stop cleanly before Kaggle's 12 h limit (11 for a real run)
BUDGET = 2000000                        # env steps, None keeps the config's budget (smoke test: 60000)
GPU = True                          # True only with "enable_gpu": true in kernel-metadata.json
HORIZON = 16000                       # episode length, as decentralised_comm/fixed_long
# The checkpoint to warm start from: dataset bjarkekarlsen/slap-init-f16-decentralised holds one
# folder per regime with the checkpoint the old 2000-step run was tested with.
import glob
INIT = next(iter(sorted(glob.glob(f"/kaggle/input/**/{REGIME}/checkpoint_0000*", recursive=True))), None)
print("warm start from", INIT, flush=True)
# To continue a run that hit HOURS: add this kernel's output as an input in
# kernel-metadata.json ("kernel_sources") and set the path of its run folder here, for example
# "/kaggle/input/slap-mapd-train/run". The script prints the inputs it finds.
RESUME_FROM = next(iter(sorted(
    os.path.dirname(p) for p in glob.glob("/kaggle/input/**/run/*_spec.json", recursive=True)
)), None)
print("resume from", RESUME_FROM, flush=True)

# The config holds everything else, the fleet's main load included (arrival_rate, from the
# updated Token Passing run, results/E_load/fleet_<m>/capacity.json).
CONFIG = f"configs/fleet_{FLEET}/{CONTROLLER}.yaml"


def run(cmd, **kwargs):
    print("+", " ".join(cmd), flush=True)
    return subprocess.run(cmd, check=True, **kwargs)


# ------------------------------------------------------------------ the code, the same Ray as at home
os.chdir("/kaggle/working")
if os.path.isdir("/kaggle/input"):
    print("inputs:", [os.path.join("/kaggle/input", d) for d in os.listdir("/kaggle/input")])
run(["git", "clone", "--depth", "1", "--branch", BRANCH,
     "https://github.com/BjarkeKarlsen/slap-mapd-coupling.git", "code"])
run([sys.executable, "-m", "pip", "install", "-q", "-e", "code", "ray[rllib]==2.57.0"])
COMMIT = subprocess.run(["git", "-C", "code", "rev-parse", "HEAD"],
                        capture_output=True, text=True).stdout.strip()
print(COMMIT, "on", os.cpu_count(), "cores", flush=True)

# ------------------------------------------------------------------ the run folder
RUN = "/kaggle/working/run"
if RESUME_FROM:
    shutil.copytree(RESUME_FROM, RUN)
os.makedirs(RUN, exist_ok=True)
with open(f"{RUN}/commit.txt", "a") as f:
    f.write(f"{COMMIT} {BRANCH} {CONTROLLER} fleet {FLEET} {REGIME}"
            f"{' communication' if COMMUNICATION else ''}\n")

config = os.path.abspath(f"code/{CONFIG}")

# ------------------------------------------------------------------ the warehouse tables
# A dataset in "dataset_sources" of kernel-metadata.json that holds a pool_key.txt is a set of
# warehouse tables built at home (slap-mapd prepare-warehouses). Each is copied to
# /tmp/warehouses/<its key>, where the run looks first. A set whose key the run does not ask for
# is ignored, and a missing one is built on first use, which takes about 20 minutes at fleet 8.
STORE = "/tmp/warehouses"
for source in sorted(os.listdir("/kaggle/input")) if os.path.isdir("/kaggle/input") else []:
    found = [os.path.join(root, "pool_key.txt")
             for root, _, files in os.walk(os.path.join("/kaggle/input", source))
             if "pool_key.txt" in files]
    for marker in found:
        key = open(marker).read().strip()
        target = os.path.join(STORE, key)
        if not os.path.isdir(target):
            shutil.copytree(os.path.dirname(marker), target,
                            ignore=shutil.ignore_patterns("pool_key.txt", "dataset-metadata.json"))
        print("warehouse tables", key, len(os.listdir(target)), "files", flush=True)

# ------------------------------------------------------------------ train
# timeout sends Ctrl-C after HOURS, Ray stops cleanly, and the run can be continued with
# RESUME_FROM.
os.makedirs("/tmp/ray_k", exist_ok=True)
env = dict(os.environ, RAY_TMPDIR="/tmp/ray_k", SLAP_WAREHOUSE_STORE=STORE,
           PYTHONUNBUFFERED="1")
if RESUME_FROM:
    cmd = [sys.executable, "-m", "slap_mapd_coupling.main", "resume", RUN]
else:
    cmd = [sys.executable, "-m", "slap_mapd_coupling.main", "train", "--config", config,
           "--controller", CONTROLLER, "--regime", REGIME,
           "--env-runners", "3", "--checkpoint-every", "3",  # 3 runners, 3 episodes per update
           "--output", RUN]
    cmd += ["--budget-env-steps", str(BUDGET)] if BUDGET else []
    cmd += ["--gpu"] if GPU else []
    cmd += ["--communication"] if COMMUNICATION else []
    cmd += ["--horizon", str(HORIZON), "--no-validate"]
    if INIT is None:
        raise SystemExit("No warm-start checkpoint found under /kaggle/input.")
    cmd += ["--init-checkpoint", INIT]
print("+", " ".join(cmd), flush=True)
# Every line of the training goes to train.log and to Kaggle's log, so the run can be followed
# live on its page. The Output tab only fills once the run has ended.
with open(f"{RUN}/train.log", "a") as log:
    process = subprocess.Popen(["timeout", "--signal=INT", f"{HOURS}h", *cmd], cwd="code",
                               env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               text=True, bufsize=1)
    for line in process.stdout:
        log.write(line)
        log.flush()
        print(line, end="", flush=True)
    code = process.wait()

# ------------------------------------------------------------------ finish
print("exit code", code)
if code == 0:
    open(f"{RUN}/done", "w").write(f"kaggle, commit {COMMIT}\n")
    print("Finished. Download the run folder.")
else:
    print("Not finished. Continue it with RESUME_FROM, see kaggle.md.")
# The cloned code is not part of the result, so it stays out of the output.
shutil.rmtree("/kaggle/working/code", ignore_errors=True)
