"""
Token Passing at each fleet's main load on the 20 test seeds ([A142], fig:exp:rq4).
(a) the order gain of demand and congestion-aware storage over fixed storage, paired by seed, with
95 % intervals. (b) where a pick's time goes under fixed and demand storage.

Run:  python thesis-progress/scripts/images/tp_fleet.py   (from the workspace root)
Out:  thesis-progress/scripts/Images/tp_fleet.png, copy to thesis/Images/
Rows: thesis-progress/results/L_results/scaling/tp_test_seeds/fleet_<m>/load_sweep.jsonl
The gains are those of tab:exp:rq1 (printed for a check).
"""
import json
import os
import statistics
import sys

from scipy.stats import t

sys.path.insert(0, os.path.dirname(__file__))
from base import OUT, C, plt  # noqa: E402
from appendix_data import style, panel_title  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROWS = os.path.join(HERE, "..", "..", "results", "L_results", "scaling", "tp_test_seeds")
FLEETS = (8, 16, 32, 64)
PARTS = (("mean_wait_for_agent", "wait for an agent"), ("mean_travel_time", "travel"),
         ("mean_blocked_time", "blocked"))


def rows(m):
    out = {}
    for line in open(os.path.join(ROWS, f"fleet_{m}", "load_sweep.jsonl")):
        r = json.loads(line)
        out.setdefault(r["storage_mode"], {})[r["seed"]] = r
    return out


def gain(m, rule):
    d = rows(m)
    g = [100 * (d["fixed"][s]["mean_order_completion"] - r["mean_order_completion"])
         / d["fixed"][s]["mean_order_completion"] for s, r in d[rule].items()]
    mu = statistics.fmean(g)
    return mu, t.ppf(0.975, len(g) - 1) * statistics.stdev(g) / len(g) ** 0.5


fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.0))
for k, (rule, marker) in enumerate((("demand", "o"), ("congestion", "s"))):
    mu, half = zip(*(gain(m, rule) for m in FLEETS))
    print(rule, [f"{x:.1f} +- {h:.1f}" for x, h in zip(mu, half)])
    a1.errorbar([x + (k - 0.5) * 0.15 for x in range(len(FLEETS))], mu, yerr=half, marker=marker,
                ls="-", capsize=3, color=C["text"], mfc=C["text"] if rule == "demand" else "white",
                label="demand" if rule == "demand" else "congestion-aware")
a1.set_xticks(range(len(FLEETS)), [str(m) for m in FLEETS])
a1.set_xlabel("agents")
a1.set_ylabel("order gain over fixed (%)")
a1.set_ylim(0, 26)
a1.legend(frameon=False, fontsize=8)
style(a1)
panel_title(a1, "(a) gain")

width = 0.38
for k, rule in enumerate(("fixed", "demand")):
    bottom = [0.0] * len(FLEETS)
    for j, (key, label) in enumerate(PARTS):
        v = [statistics.fmean(r[key] for r in rows(m)[rule].values()) for m in FLEETS]
        a2.bar([x + (k - 0.5) * width for x in range(len(FLEETS))], v, width * 0.95, bottom=bottom,
               color=["#bbbbbb", "#777777", "#333333"][j], label=label if k == 0 else None,
               hatch=None if rule == "fixed" else "//", edgecolor="white")
        bottom = [b + x for b, x in zip(bottom, v)]
a2.set_xticks(range(len(FLEETS)), [str(m) for m in FLEETS])
a2.set_xlabel("agents (left fixed, right demand)")
a2.set_ylabel("pick service time (steps)")
a2.legend(frameon=False, fontsize=8)
style(a2)
panel_title(a2, "(b) where a pick's time goes")
path = os.path.join(OUT, "tp_fleet.png")
fig.savefig(path, dpi=200, bbox_inches="tight")
print(path)
