"""Collects the lock-measure replays (PR #216) from the Lenovo and counts locks.

    python3 ~/thesis_runs/locks_replay/collect.py [--threshold 200]

1. rsync /root/thesis_runs/locks_replay/rows from thesis-eval to ~/thesis_runs/locks_replay/rows.
2. Checks each replay against its original row (served share, backlog, hold, stand-still). A
   mismatch means the replay did not repeat the episode: report it, do not use it.
3. Counts seeds that lock (longest_pair_stand_still >= threshold) per controller and fleet. An
   episode not in jobs_all.txt cannot reach 200 (hold or stand-still < 200), so it counts as not
   locked. Layout seeds from locks_layout.json, split as layout vs other seeds.
"""
import argparse, glob, json, subprocess
from pathlib import Path

H = Path.home()
L = H / "thesis_runs/locks_replay"
PERF = H / "Documents/thesis/thesis-progress/results/L_results/scaling/perf"
EVAL = H / "thesis_runs/evaluation/fleet_16"
LONG = {"centralised": ["congestion_long", "demand_long_part2", "fixed_long_part2"],
        "section": ["congestion_long_part2", "demand_long_part2", "fixed_long_part2"],
        "decentralised": ["congestion_long", "demand_long", "fixed_long"],
        "decentralised_comm": ["congestion_long_part2", "demand_long_part2", "fixed_long"]}
CHECK = ["served_share", "backlog", "longest_two_agent_hold", "longest_stand_still"]

ap = argparse.ArgumentParser()
ap.add_argument("--threshold", type=int, default=200)
ap.add_argument("--no-fetch", action="store_true")
a = ap.parse_args()
if not a.no_fetch:
    subprocess.run(["rsync", "-a", "thesis-eval:/root/thesis_runs/locks_replay/rows/", str(L / "rows") + "/"], check=True)

jobs = [l.split() for l in open(L / "jobs_all.txt") if l.strip()]
wanted = set()
originals, replays, missing, bad = {}, {}, [], []
for f in glob.glob(str(PERF / "rows/*.jsonl")):
    d = json.loads(open(f).readline())
    m, rest = Path(f).stem.split("_", 1); arm, s = rest.rsplit("_", 1)
    originals[("perf", int(m), arm, "congestion", int(s))] = d
for arm, runs in LONG.items():
    for run in runs:
        p = EVAL / arm / run / "evaluation_served_horizon10000_warmup5000/test.jsonl"
        if p.exists():
            for l in open(p):
                d = json.loads(l); originals[("16", 16, arm, run, d["seed"])] = d
for j in jobs:
    if j[0] == "perf":
        key, name = ("perf", int(j[1]), j[2], "congestion", int(j[3])), f"perf_{j[1]}_{j[2]}_{j[3]}"
    else:
        arm, run = j[1].split("/"); key, name = ("16", 16, arm, run, int(j[3])), f"16_{arm}_{run}_{j[3]}"
    wanted.add(key)
    f = L / "rows" / f"{name}.jsonl"
    if not f.exists() or not f.stat().st_size:
        missing.append(name); continue
    r = json.loads(open(f).readline()); o = originals[key]
    diff = [k for k in CHECK if r.get(k) != o.get(k)]
    if diff: bad.append((name, diff))
    replays[key] = r["longest_pair_stand_still"]
print(f"{len(replays)} of {len(jobs)} replays in, {len(missing)} missing, {len(bad)} not matching the original row")
for b in bad: print("  MISMATCH", b)
for m in missing: print("  missing", m)

layout = json.load(open(PERF / "locks_layout.json"))
print(f"\nseeds that lock (pair stand-still >= {a.threshold}), out of 20; layout seeds / other seeds")
for key0 in sorted({k[:4] for k in originals}, key=lambda k: (k[0], k[2], k[3], k[1])):
    seeds = sorted(k[4] for k in originals if k[:4] == key0)
    locked = [s for s in seeds if replays.get((*key0, s), 0) >= a.threshold]
    lay = [s for s in seeds if layout.get(f"{key0[1]}_{s}", {}).get("cats_all_lane")]
    pend = [s for s in seeds if (*key0, s) in wanted and (*key0, s) not in replays]
    print(f"  {key0[0]:4s} {key0[1]:2d} {key0[2]:19s} {key0[3]:22s} {len(locked):2d}/{len(seeds)}"
          f"   layout {sum(s in lay for s in locked)}/{len(lay)}, other {sum(s not in lay for s in locked)}/{len(seeds)-len(lay)}"
          + (f"   ({len(pend)} still to replay)" if pend else "") + f"   {locked}")
