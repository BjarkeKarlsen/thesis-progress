"""Shelf-to-workstation distance of the pick tasks in a trace, the jump in the potential at pickup."""
import json, sys, statistics as st
from collections import deque
lines = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
edges = [(e["source"], e["target"]) if isinstance(e, dict) else (e[0], e[1]) for e in lines[0]["edges"]]
rev = {}
for a, b in edges:
    rev.setdefault(b, []).append(a)
def dist_to(goal):
    d = {goal: 0}; q = deque([goal])
    while q:
        v = q.popleft()
        for u in rev.get(v, []):
            if u not in d:
                d[u] = d[v] + 1; q.append(u)
    return d
tasks = [l for l in lines if l.get("type") == "tasks"][-1]["tasks"]
picks = [t for t in tasks if t.get("kind") == "pick"]
cache, trips = {}, []
for t in picks:
    g = t["to"]
    cache.setdefault(g, dist_to(g))
    d = cache[g].get(t["from"])
    if d is not None: trips.append(d)
trips.sort()
print(f"{len(trips)} picks: shelf to workstation median {trips[len(trips)//2]}, mean {st.mean(trips):.0f}, 90 % below {trips[int(.9*len(trips))]}")
