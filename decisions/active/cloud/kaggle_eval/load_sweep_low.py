"""Token Passing load sweep below each fleet's capacity, with the served counts ([A96], [A111]),
as a Kaggle script kernel. Pushed by push_load_sweep_low.sh.

Why: Appendix E's capacities were read with f_up 0.8 on the sweep of 2026-10-31. The served_check
of 2026-11-17 replayed only the capacity and above. With f_up 0.9 the capacity also needs every
lower tested rate to pass, so the lower rates of Appendix E's updated sweep are played again here,
fixed storage, 20 seeds, 10000 steps with a 5000-step warm-up, on configs/step12/fleet_<m>.yaml.
Branch main (8ba3048): same simulation as the learned evaluations (131b6b1), served counts of the
first [A96] version, which served_counts.py recounts. No training, no window tables.
Rows land in /kaggle/working/E_load/fleet_<m>/served_check_low/.
"""

import os
import subprocess
import sys
import time

START = time.time()
BRANCH = "@BRANCH@"
HOURS = 11.5
# fleet: the lower tested rates of Appendix E's updated sweep (results/E_load/fleet_<m>/load_sweep.jsonl)
JOBS = [(8, ["0.1", "0.125"]), (16, ["0.2", "0.25"]), (32, ["0.4"]), (64, ["0.8"])]


def run(cmd, **kwargs):
    print("+", " ".join(cmd), flush=True)
    return subprocess.run(cmd, check=True, **kwargs)


os.chdir("/kaggle/working")
run(["git", "clone", "--depth", "1", "--branch", BRANCH,
     "https://github.com/BjarkeKarlsen/slap-mapd-coupling.git", "code"])
run([sys.executable, "-m", "pip", "install", "-q", "-e", "code"])
COMMIT = subprocess.run(["git", "-C", "code", "rev-parse", "HEAD"],
                        capture_output=True, text=True).stdout.strip()
cores = os.cpu_count() or 4
print(COMMIT, "on", cores, "cores", flush=True)

env = dict(os.environ, PYTHONPATH="src", PYTHONUNBUFFERED="1",
           OMP_NUM_THREADS="1", MKL_NUM_THREADS="1")
failed = []
for fleet, rates in JOBS:
    out = f"/kaggle/working/E_load/fleet_{fleet}/served_check_low"
    os.makedirs(out, exist_ok=True)
    left = int(HOURS * 3600 - (time.time() - START))
    if left < 600:
        failed.append(fleet)
        print("no time left for fleet", fleet, flush=True)
        continue
    cmd = [sys.executable, "scripts/sweep/load_sweep.py", "--config",
           f"configs/step12/fleet_{fleet}.yaml", "--seeds", "20", "--workers", str(cores),
           "--horizon", "10000", "--warmup", "5000", "--rates", *rates, "--out", out]
    print("+", " ".join(cmd), f"(time left {left} s)", flush=True)
    t0 = time.time()
    with open(f"{out}/sweep.log", "a") as log:
        code = subprocess.run(["timeout", "--signal=INT", f"{left}s", *cmd], cwd="code",
                              env=env, stdout=log, stderr=subprocess.STDOUT).returncode
    print(f"fleet {fleet} exit {code} after {(time.time() - t0) / 60:.0f} min", flush=True)
    if code != 0:
        failed.append(fleet)

with open("/kaggle/working/E_load/done" if not failed else "/kaggle/working/E_load/partial", "w") as f:
    f.write(f"kaggle, commit {COMMIT}, failed fleets {failed}\n")
import shutil  # noqa: E402
shutil.rmtree("/kaggle/working/code", ignore_errors=True)
print("finished, failed fleets:", failed)
