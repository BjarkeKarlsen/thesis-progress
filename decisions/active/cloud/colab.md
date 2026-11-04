# Training on Colab

**Replaced 2026-11-04 by the command line, `colab_cli/`.** The notebook below is kept for history.
`colab_cli/colab.bash` starts, watches, fetches and stops a run from this PC with the Colab
command line (`uv tool install google-colab-cli`, log in once with `colab new` in a normal
terminal). Drive cannot be mounted from the command line (the browser mounts it on a machine of
its own), so the run lives on the Colab machine's disk and `watch` copies it home every 30 minutes
into `~/thesis_runs/training/fleet_<m>/<arm>/<regime>/`. A run that stopped continues with `start`
again, which sends the run from home. The header of `colab.bash` lists the commands and settings.

What the smoke tests of 2026-11-04 showed (fleet 8, decentralised, fixed storage, 60000 steps):

- A High-RAM CPU machine has 8 cores and 50 GB, costs 0.26 units an hour, and Pro gives 100 units.
- Sampling took 29 s an iteration and the learner's update 181 s on one core. With
  `--learner-cpus 5` (PR #204) the update took 126 s, the whole iteration about 140 s.
- Fleet 32 on CPU (2026-11-04): decentralised about 420 to 450 s an iteration (about 10 h a
  run). Section over an hour an iteration, nearly all of it the learner's update, so stopped.
- A T4 High-RAM machine costs 1.57 units an hour (CPU 0.26), with 50 GB and a 15 GB T4. Set
  `GPU=T4` on `start` and `watch`.
- Fetching works (run folder, spec, progress log, checkpoints, `done`). `resume` after a dropped
  session is not tested yet.


One notebook trains one arm (a fleet and a regime). Colab can drop the session at any time, and
it stops when the tab has been closed or idle for a while. So the run trains on the session's
own disk and is copied to Google Drive every 10 minutes. Running the notebook again picks the
run up from Drive and continues it.

Do the Kaggle smoke test first ([kaggle.md](kaggle.md)). This guide assumes the commands work.

## One-time setup

1. Buy the month (Colab Pro). Check under **Resources** what each runtime costs in compute
   units. A CPU runtime costs far less than a GPU one.
2. New notebook. **Runtime, Change runtime type**: CPU and High-RAM, or a GPU only if the Kaggle
   smoke test showed it helps.
3. Paste the cells below, one per cell.

## The cells

**1. Settings.** The only cell you edit. `NAME` is the run's folder on Drive and at home.

```python
BRANCH = "feat/workstation-sections"  # a pushed branch
CONFIG = "configs/step12/fleet_32.yaml"
REGIME = "fixed_only"                 # or "matched" (trained under demand storage)
LOAD = None                           # the fleet's main load, from results/E_load/
NAME = "fleet_32/fixed_only"
HOURS = 20                            # stop cleanly before the session would end
BUDGET = None                         # env steps, None keeps the config's budget
GPU = False                           # True only on a GPU runtime
```

**2. Drive and code.** If Colab asks to restart the runtime after the install, restart it and
run the cells again. The install is quick the second time.

```python
import os, shutil, subprocess, sys
from google.colab import drive
drive.mount("/content/drive")
DRIVE_RUN = f"/content/drive/MyDrive/slap-mapd/{NAME}"
os.makedirs(DRIVE_RUN, exist_ok=True)

os.chdir("/content")
if not os.path.isdir("code"):
    subprocess.run(["git", "clone", "--depth", "1", "--branch", BRANCH,
                    "https://github.com/BjarkeKarlsen/slap-mapd-coupling.git", "code"],
                   check=True)
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-e", "code",
                "ray[rllib]==2.57.0"], check=True)
subprocess.run("apt-get -qq install -y rsync > /dev/null", shell=True)
COMMIT = subprocess.run(["git", "-C", "code", "rev-parse", "HEAD"],
                        capture_output=True, text=True).stdout.strip()
print(COMMIT, "on", os.cpu_count(), "cores")
```

**3. Run folder.** When Drive already holds the run, it is copied back to the same path and
continued. Otherwise a new run starts.

```python
import glob
RUN = "/content/run"
RESUME = bool(glob.glob(f"{DRIVE_RUN}/*_spec.json"))
if RESUME:
    shutil.copytree(DRIVE_RUN, RUN, dirs_exist_ok=True)
os.makedirs(RUN, exist_ok=True)
with open(f"{RUN}/commit.txt", "a") as f:
    f.write(f"{COMMIT} {BRANCH}\n")

config = os.path.abspath(f"code/{CONFIG}")
if REGIME == "matched" and not RESUME:
    # As bedtime.bash does: trained under the rule it is evaluated in, demand storage.
    import yaml
    data = yaml.safe_load(open(config))
    data.update(regime="matched", evaluation_storage_mode="demand")
    config = f"{RUN}/config.yaml"
    yaml.safe_dump(data, open(config, "w"), sort_keys=False)
print("continuing" if RESUME else "new run", DRIVE_RUN)
```

**4. Train.** Copies the run to Drive every 10 minutes while it trains, and once more at the
end. `timeout` sends Ctrl-C after `HOURS` and Ray stops cleanly.

```python
sync = f'rsync -a "{RUN}/" "{DRIVE_RUN}/"'
syncer = subprocess.Popen(["bash", "-c", f"while true; do sleep 600; {sync}; done"])

os.makedirs("/tmp/ray_c", exist_ok=True)
env = dict(os.environ, RAY_TMPDIR="/tmp/ray_c", SLAP_WAREHOUSE_STORE="/content/warehouses")
if RESUME:
    cmd = [sys.executable, "-m", "slap_mapd_coupling.main", "resume", RUN]
else:
    cmd = [sys.executable, "-m", "slap_mapd_coupling.main", "train", "--config", config,
           "--controller", "decentralised", "--regime", REGIME, "--arrival-rate", str(LOAD),
           "--env-runners", str(os.cpu_count() - 1), "--checkpoint-every", "3",
           "--output", RUN]
    cmd += ["--budget-env-steps", str(BUDGET)] if BUDGET else []
    cmd += ["--gpu"] if GPU else []
with open(f"{RUN}/train.log", "a") as log:
    code = subprocess.run(["timeout", "--signal=INT", f"{HOURS}h", *cmd],
                          cwd="code", env=env, stdout=log, stderr=subprocess.STDOUT).returncode
syncer.kill()
print("exit code", code)
```

**5. Finish.**

```python
if code == 0:
    open(f"{RUN}/done", "w").write(f"colab, commit {COMMIT}\n")
subprocess.run(sync, shell=True, check=True)
print("Finished." if code == 0 else "Not finished. Run all cells again to continue.")
print(open(f"{RUN}/train.log").read()[-3000:])
```

## Running it

**Runtime, Run all**, and keep the tab open. Watch progress with
`!tail -n 5 /content/run/train.log` in a new cell.

If the session dies, open the notebook again and **Run all**. Cell 3 finds the run on Drive and
cell 4 resumes it. At most the last 10 minutes and the iterations since the last checkpoint are
trained again.

## Bringing it home

Download `MyDrive/slap-mapd/<NAME>` from drive.google.com (it comes as a zip), and unpack it into
`~/thesis_runs/training/<NAME>/`. Then evaluate it and copy the progress file as in
[kaggle.md](kaggle.md), "Bringing it home".
