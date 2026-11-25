"""The learned controllers' rows of Appendix L's 16-agent tables, from the long runs ([A144]).

Run:  python3 thesis-progress/results/L_results/long_runs_16/tables.py   (from the workspace root)
Out:  thesis-progress/results/L_results/long_runs_16/tables.tex, one block per table, the learned
      rows only (Token Passing's rows stay as they are in L.Results.tex).

Reads the test rows `slap-mapd evaluate` wrote for each long run (20 test seeds, 10000 steps,
5000 warm-up, chosen checkpoint), under ~/thesis_runs/evaluation/fleet_16. Keep-up and the
served share are recounted with served_counts.recount ([A96], f_up 0.9 [A111]). A run stalls
when no task finishes for longer than the stall length, 36 / arrival rate = 200 steps at 16
agents ([A118], Appendix H). The decision time is left out here: the test episodes played 8 at a
time on the CPU, so their times are not the controller's own (see app:results:scaling).
"""
import json
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "scripts"))
from served_counts import recount  # noqa: E402

EVAL = os.path.expanduser("~/thesis_runs/evaluation/fleet_16")
SERVED = "evaluation_served_horizon10000_warmup5000"
LONG = {"centralised": {"fixed": "fixed_long_part2", "demand": "demand_long_part2",
                        "congestion": "congestion_long"},
        "section": {"fixed": "fixed_long_part2", "demand": "demand_long_part2",
                    "congestion": "congestion_long_part2"},
        "decentralised": {"fixed": "fixed_long", "demand": "demand_long",
                          "congestion": "congestion_long"},
        "decentralised_comm": {"fixed": "fixed_long", "demand": "demand_long_part2",
                               "congestion": "congestion_long_part2"}}
NAMES = {"centralised": "centralised", "section": "section-based",
         "decentralised": "decentralised", "decentralised_comm": "with messages"}
STALL = 36 / 0.18


def rows(arm, rule):
    path = os.path.join(EVAL, arm, LONG[arm][rule], SERVED, "test.jsonl")
    found = [json.loads(line) for line in open(path)]
    found = [r for r in found if r.get("role", "chosen") == "chosen" and r["storage_mode"] == rule]
    assert len(found) == 20, (arm, rule, len(found))
    return [{**r, **recount(r)} for r in found]


def mean(rs, field, digits=1):
    values = [r[field] for r in rs if r.get(field) is not None]
    return f"{statistics.fmean(values):.{digits}f}" if values else "n/a"


def count(rs, field):
    return f"{sum(bool(r[field]) for r in rs)} of {len(rs)}"


TABLES = (
    ("tab:app:check:16", lambda rs: [
        count(rs, "keeps_up_picks"), count(rs, "keeps_up_putaways"), mean(rs, "served_share", 2),
        mean(rs, "backlog_slope", 2), str(sum(r["longest_completion_gap"] > STALL for r in rs))]),
    ("tab:app:result:16", lambda rs: [
        mean(rs, "mean_service_time"), mean(rs, "mean_wait_for_agent"), mean(rs, "mean_travel_time"),
        mean(rs, "mean_blocked_time"), mean(rs, "mean_stock_wait", 2), mean(rs, "mean_crowding", 2),
        mean(rs, "robot_busy_share", 2), "n/a"]),
    ("tab:app:cost:16", lambda rs: [
        mean(rs, "mean_putaway_service_time"), mean(rs, "mean_order_completion"),
        mean(rs, "orders_per_timestep", 3), mean(rs, "throughput", 3),
        f"{statistics.fmean(r['throughput'] for r in rs) / 16:.4f}"]),
    ("tab:app:backlog:16", lambda rs: [
        mean(rs, "num_waiting_tasks"), mean(rs, "num_active_tasks"), mean(rs, "num_waiting_orders"),
        mean(rs, "num_lines_waited"), mean(rs, "num_released_putaways"),
        mean(rs, "num_completed_putaways")]),
    ("tab:app:stock:16", lambda rs: [
        mean(rs, "mean_split_skus"), mean(rs, "mean_tasks_per_line", 2),
        mean(rs, "mean_cold_prime_share", 2), mean(rs, "mean_unit_age_at_pick", 0),
        mean(rs, "num_storage_updates", 0), mean(rs, "mean_arrived_units")]),
)

lines = ["% written by thesis-progress/results/L_results/long_runs_16/tables.py, learned rows only"]
for label, cells in TABLES:
    lines.append(f"% {label}")
    for rule in ("fixed", "demand", "congestion"):
        lines.append(f"% {rule}")
        for arm in LONG:
            lines.append(f"               & {NAMES[arm]:<14} & " + " & ".join(cells(rows(arm, rule))) + " \\\\")
out = os.path.join(HERE, "tables.tex")
open(out, "w").write("\n".join(lines) + "\n")
print(open(out).read())
