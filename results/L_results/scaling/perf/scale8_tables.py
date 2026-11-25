"""Appendix L, 8 agents from the scale test: Token Passing on the test seeds (all rules) and the
16-agent congestion-aware policies played at 8 agents (perf test), served counts recounted."""
import sys, json, glob, re
from pathlib import Path
T = Path.home()/"Documents/thesis/thesis-progress/scripts"
sys.path[:0] = [str(T), str(T/"images")]
import appendix_results as ar
from served_counts import recount
TP = Path.home()/"thesis_runs/tp_testseeds8_2026-11-17/rows/load_sweep.jsonl"
PERF = Path.home()/"Documents/thesis/thesis-progress/results/L_results/scaling/perf/rows"
# decision time, 5-seed mean at 8 agents, step time test of 2026-11-24 (seconds)
KAPPA = {"token_passing": 0.00031, "centralised": 0.0198, "section": 0.0156,
         "decentralised": 0.0035, "decentralised_comm": 0.0046}
def fix(r):
    c = recount(r) or {}
    return {**r, **c, "completed_share": c.get("served_share", r.get("served_share")),
            "stalled": r["longest_completion_gap"] > 400,
            "mean_decision_runtime_seconds": KAPPA[r["_c"]]}
tp = [dict(json.loads(l), _c="token_passing") for l in open(TP)]
data = {("token_passing", m): [fix(r) for r in tp if r["storage_mode"] == m] for m in ("fixed", "demand", "congestion")}
for arm in ar.LEARNED:
    fs = [f for f in glob.glob(str(PERF/f"8_{arm}_*.jsonl")) if re.fullmatch(rf".*/8_{arm}_\d+\.jsonl", f)]
    data[(arm, "congestion")] = [fix(dict(json.loads(open(f).readline()), _c=arm)) for f in sorted(fs)]
for label, cells in ar.TABLES[:4]:
    print("%", label)
    for rule in ("fixed", "demand", "congestion"):
        ctrls = ("token_passing",) if rule != "congestion" else ar.CONTROLLERS
        for i, c in enumerate(ctrls):
            rows = data[(c, rule)]
            first = rule.ljust(10) if i == 0 else " " * 10
            print(f"    {first} & {ar.ARMS[c]:<14} & " + " & ".join(cells(rows, c)) + f" \\\\  % {len(rows)} seeds")
