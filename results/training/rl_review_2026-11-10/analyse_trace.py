"""What do the robots of a trace do? For robots holding a task: steps towards the goal, away, sideways
(same distance) and still; back-and-forth (A, B, A); and the same for free robots. Usage:
    python analyse_trace.py trace.jsonl
"""

import json
import sys
from collections import Counter, deque

path = sys.argv[1]
lines = [json.loads(l) for l in open(path) if l.strip()]
header = lines[0]
steps = [l for l in lines[1:] if "agents" in l]
edges = [(e["source"], e["target"]) if isinstance(e, dict) else (e[0], e[1]) for e in header["edges"]]
out = {}
for a, b in edges:
    out.setdefault(a, []).append(b)


def dist_from_all(goal):
    # shortest path distance from every vertex to goal: BFS on reversed edges
    rev = {}
    for a, b in edges:
        rev.setdefault(b, []).append(a)
    d = {goal: 0}
    q = deque([goal])
    while q:
        v = q.popleft()
        for u in rev.get(v, []):
            if u not in d:
                d[u] = d[v] + 1
                q.append(u)
    return d


cache = {}


def dist(v, goal):
    if goal not in cache:
        cache[goal] = dist_from_all(goal)
    return cache[goal].get(v)


def summarise(first, last):
    busy = Counter()
    free = Counter()
    phase = Counter()
    kinds = Counter()
    bounce = 0
    busy_moves = 0
    hist = {}
    goal_dist = []
    prev = None
    for s in steps[first:last]:
        for k, r in s["agents"].items():
            h = hist.setdefault(k, deque(maxlen=3))
            h.append(r["at"])
            if prev is None or k not in prev:
                continue
            p = prev[k]
            if r["task"] is None:
                free["moved" if r["moved"] else "still"] += 1
                continue
            phase[r["phase"]] += 1
            kinds[r["kind"]] += 1
            if p["task"] != r["task"] or p["goal"] != r["goal"]:
                continue  # target changed this step
            d0, d1 = dist(p["at"], r["goal"]), dist(r["at"], r["goal"])
            if d1 is not None:
                goal_dist.append(d1)
            if not r["moved"]:
                busy["still (overridden)" if r["overridden"] else "still (chosen)"] += 1
            elif d0 is None or d1 is None:
                busy["moved, unknown"] += 1
            elif d1 < d0:
                busy["towards goal"] += 1
            elif d1 > d0:
                busy["away from goal"] += 1
            else:
                busy["same distance"] += 1
            if r["moved"]:
                busy_moves += 1
                if len(h) == 3 and h[0] == h[2] and h[0] != h[1]:
                    bounce += 1
        prev = s["agents"]
    n = sum(busy.values())
    print(f"steps {first} to {last}")
    print(f"  robots with a task: {n} robot-steps, without: {sum(free.values())}")
    for key, c in busy.most_common():
        print(f"    {key:20s} {c / n:6.1%}")
    print(f"    back and forth (A, B, A) among moves: {bounce / max(1, busy_moves):.1%}")
    print(f"  free robots: moved {free['moved'] / max(1, sum(free.values())):.1%}")
    print(f"  phase: {dict(phase)}  kinds: {dict(kinds)}")
    if goal_dist:
        goal_dist.sort()
        print(f"  distance to goal: median {goal_dist[len(goal_dist) // 2]}, 90 % below {goal_dist[int(0.9 * len(goal_dist))]}")


summarise(0, 200)
summarise(len(steps) // 2, len(steps))
tasks = [l for l in lines if l.get("type") == "tasks"]
if tasks:
    t = tasks[-1]["tasks"]
    done = [x for x in t if x.get("finish_time") is not None]
    assigned = [x for x in t if x.get("assign_time") is not None or x.get("assigned_agent") is not None]
    print(f"tasks: {len(t)} released, {len(assigned)} assigned, {len(done)} finished")
    held = [x for x in t if x.get("finish_time") is None and x.get("pickup_time") is not None]
    print(f"  picked up but not delivered at the end: {len(held)}")
