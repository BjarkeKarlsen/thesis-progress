import sys, json, statistics
from pathlib import Path
T = Path.home()/"Documents/thesis/thesis-progress/scripts"
sys.path[:0] = [str(T), str(T/"images")]
import appendix_results as ar
from served_counts import recount, SERVED
ev = Path.home()/"thesis_runs/evaluation/fleet_8"
data = {"token_passing": ar.token_passing_rows(8)}
for arm in ar.LEARNED:
    data[arm] = {}
    for rule in ar.RULE_ORDER:
        p = ev/arm/rule/SERVED/"test.jsonl"
        rows = [json.loads(l) for l in p.open()]
        rows = [r for r in rows if r.get("role","chosen")=="chosen" and r["storage_mode"]==rule]
        data[arm][rule] = [{**r, **(recount(r) or {}), "completed_share": (recount(r) or {}).get("served_share")} for r in rows]
# TP rows: completed_share as served_share where present
print("stalled present:", sum("stalled" in r for r in data["centralised"]["fixed"]), "runtime sample", data["centralised"]["fixed"][0].get("mean_decision_runtime_seconds"))
for label, cells in ar.TABLES:
    print("%", label)
    for rule in ar.RULE_ORDER:
        for i, c in enumerate(ar.CONTROLLERS):
            rows = data.get(c, {}).get(rule)
            vals = cells(rows, c) if rows else ["TBD"]*ar.WIDTH[label]
            first = rule.ljust(10) if i == 0 else " "*10
            print(f"    {first} & {ar.ARMS[c]:<14} & " + " & ".join(vals) + " \\\\")
