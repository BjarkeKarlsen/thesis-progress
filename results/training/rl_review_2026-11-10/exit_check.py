"""Is the robot on a workstation blocked from leaving? Steps 1000 to 2000 of a trace.
For every robot-step on a workstation: does it have a task, is the workstation its goal, does it
try to move out, and is the way out (the aisle vertex next to the leaf) taken by another robot."""
import json, sys
from collections import Counter
lines = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
h = lines[0]
stations = {v["id"] for v in h["vertices"] if v["delivery"]}
edges = [(e["source"], e["target"]) if isinstance(e, dict) else (e[0], e[1]) for e in h["edges"]]
out = {}
for a, b in edges:
    out.setdefault(a, set()).add(b)
steps = [l for l in lines[1:] if "agents" in l]
c = Counter()
stays = []          # how long a robot stays on a workstation in one visit
on = {}             # robot -> steps on its current workstation
prev = None
for s in steps[1000:2000]:
    at = {r["at"]: k for k, r in s["agents"].items()}
    for k, r in s["agents"].items():
        v = r["at"]
        if v in stations:
            on[k] = on.get(k, 0) + 1
            c["robot-steps on a workstation"] += 1
            c["  holding a task" if r["task"] is not None else "  free"] += 1
            if r["task"] is not None:
                c["    its goal is this workstation" if r["goal"] == v else "    its goal is elsewhere"] += 1
            exits = out.get(v, set())
            if exits and all(x in at for x in exits):
                c["  way out taken by another robot"] += 1
            if not r["moved"] and r["intent"] is not None:
                c["  tried to move, did not"] += 1
        elif k in on:
            stays.append(on.pop(k))
    prev = s
for k, v in c.items():
    print(f"{k:45s} {v}")
stays.sort()
if stays:
    print(f"visits that ended: {len(stays)}, steps on the workstation median {stays[len(stays)//2]}, longest {stays[-1]}")
print(f"robots still on a workstation at step 2000: {len(on)}, for {sorted(on.values())} steps")
