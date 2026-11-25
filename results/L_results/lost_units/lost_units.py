"""Share of arriving units lost (pallets that fit on no shelf) per arm, 16 agents, test seeds.

Run from the home folder: python3 lost_units.py. Arriving units = mean_arrived_units per update
times horizon / 100 (Delta = 100), over the whole run. Lost = unplaced_units, whole run.
"""
import json, glob, os
BASE = os.path.expanduser("~/thesis_runs/evaluation/fleet_16")
ARMS = {"centralised": "centralised", "section-based": "section",
        "decentralised": "decentralised", "with messages": "decentralised_comm"}
def share(path):
    lost = arr = n = nz = 0
    for line in open(path):
        r = json.loads(line); n += 1
        lost += r["unplaced_units"]; nz += r["unplaced_units"] > 0
        arr += r["mean_arrived_units"] * r["horizon"] / 100
    return lost / arr, nz, n
print("controller | rule | share lost | seeds with loss | folder")
for name, d in ARMS.items():
    for rule in ("fixed", "demand", "congestion"):
        hits = sorted(glob.glob(f"{BASE}/{d}/{rule}_long*/evaluation_served_horizon10000_warmup5000/test.jsonl"))
        if not hits:
            print(f"{name} | {rule} | not evaluated yet | | "); continue
        p = hits[-1]; s, nz, n = share(p)
        print(f"{name} | {rule} | {100*s:.1f}% | {nz}/{n} | {p.split('fleet_16/')[1].split('/evaluation')[0]}")
tp = [json.loads(l) for f in glob.glob(os.path.expanduser("~/Documents/thesis/thesis-progress/results/G_storage/fleet_16/**/*.jsonl"), recursive=True) for l in open(f)]
tp = [r for r in tp if "unplaced_units" in r]
print(f"Token Passing, Appendix G rows at 16 agents: {sum(r['unplaced_units']>0 for r in tp)} of {len(tp)} lose units")
