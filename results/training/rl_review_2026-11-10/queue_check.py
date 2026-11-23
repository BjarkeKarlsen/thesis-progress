"""Do loaded robots crowd around their workstation? For steps 1000 to 2000: per step, robots heading to
delivery, how many share a goal, the distance histogram, and whether the goal vertex is occupied."""
import json, sys, statistics as st
from collections import Counter, deque
lines = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
edges = [(e["source"], e["target"]) if isinstance(e, dict) else (e[0], e[1]) for e in lines[0]["edges"]]
rev = {}
for a, b in edges: rev.setdefault(b, []).append(a)
cache = {}
def dist(v, g):
    if g not in cache:
        d = {g: 0}; q = deque([g])
        while q:
            x = q.popleft()
            for u in rev.get(x, []):
                if u not in d: d[u] = d[x] + 1; q.append(u)
        cache[g] = d
    return cache[g].get(v)
steps = [l for l in lines[1:] if "agents" in l][1000:2000]
share, occupied, hist, goals = [], 0, Counter(), Counter()
for s in steps:
    at = {r["at"] for r in s["agents"].values()}
    c = Counter(r["goal"] for r in s["agents"].values() if r["phase"] == "to_delivery")
    goals.update(c.keys())
    share.extend(c.values())
    for r in s["agents"].values():
        if r["phase"] == "to_delivery":
            hist[min(dist(r["at"], r["goal"]) or 0, 30) // 3 * 3] += 1
    occupied += sum(1 for g in c if g in at)
print(f"distinct workstations robots carry to: {len(goals)}")
print(f"loaded robots sharing one workstation, per step: mean {st.mean(share):.1f}, max {max(share)}")
print(f"workstations with a loaded robot heading there that have a robot standing on them: {occupied / max(1, sum(1 for s in steps for _ in [0])):.1f} per step")
tot = sum(hist.values())
print("distance of loaded robots to their workstation:", {f"{k}-{k+2}": f"{v / tot:.0%}" for k, v in sorted(hist.items())})
