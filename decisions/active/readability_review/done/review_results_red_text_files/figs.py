import json, glob, statistics, sys
from pathlib import Path
T = Path.home()/"Documents/thesis/thesis-progress/scripts"
sys.path[:0] = [str(T), str(T/"images")]
import appendix_results as ar
from appendix_data import C, plt, style, panel_title, ARM_COLOUR
from scipy.stats import t
TR = Path.home()/"thesis_runs/training/fleet_16"
RUNS = {"centralised": {"fixed": ["fixed_long", "fixed_long_part2"], "demand": ["demand_long", "demand_long_part2"], "congestion": ["congestion_long"]},
        "section": {r: [f"{r}_long", f"{r}_long_part2"] for r in ("fixed", "demand", "congestion")},
        "decentralised": {r: [f"{r}_long"] for r in ("fixed", "demand", "congestion")},
        "decentralised_comm": {"fixed": ["fixed_long"], "demand": ["demand_long", "demand_long_part2"], "congestion": ["congestion_long", "congestion_long_part2"]}}
NAMES = {"centralised": "centralised", "section": "section-based", "decentralised": "decentralised", "decentralised_comm": "with messages"}
COL = {**ARM_COLOUR, "decentralised_comm": C["comm"]}
tp = ar.token_passing_rows(16)
fig, axes = plt.subplots(1, 3, figsize=(10, 3.0), sharey=True)
for ax, rule in zip(axes, ("fixed", "demand", "congestion")):
    for arm, rules in RUNS.items():
        ys = []
        for d in rules[rule]:
            f = glob.glob(str(TR/arm/d/"*_training_progress.jsonl"))
            ys += [r["tasks_completed"]/r["episode_step"] for r in map(json.loads, open(f[0]))]
        xs = [48_000*(i+1)/1e6 for i in range(len(ys))]
        ax.plot(xs, ys, color=COL[arm], lw=1.4, label=NAMES[arm])
    ax.axhline(statistics.fmean(r["throughput"] for r in tp[rule]), color=C["text"], ls="--", lw=1, label="Token Passing (test)")
    panel_title(ax, ar.RULES[rule] if hasattr(ar,'RULES') else rule); style(ax); ax.set_xlabel("environment steps (millions)")
axes[0].set_ylabel("tasks finished per step")
h, l = axes[0].get_legend_handles_labels()
fig.legend(h, l, loc="upper center", ncol=5, frameon=False, bbox_to_anchor=(0.5, 1.08), fontsize=9)
fig.savefig(sys.argv[1]+"/learning.png", dpi=200, bbox_inches="tight")

# gain of demand storage vs fleet, Token Passing, with service time split
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.0))
fleets = (8, 16, 32, 64)
for k, (rule, mk) in enumerate((("demand", "o"), ("congestion", "s"))):
    g_mu, g_h = [], []
    for m in fleets:
        d = ar.token_passing_rows(m); fx = {r["seed"]: r for r in d["fixed"]}
        g = [100*(fx[r["seed"]]["mean_order_completion"]-r["mean_order_completion"])/fx[r["seed"]]["mean_order_completion"] for r in d[rule]]
        g_mu.append(statistics.fmean(g)); g_h.append(t.ppf(.975, len(g)-1)*statistics.stdev(g)/len(g)**.5)
    a1.errorbar([x+(k-.5)*.15 for x in range(4)], g_mu, yerr=g_h, marker=mk, ls="-", capsize=3, color=C["text"], mfc=C["text"] if rule=="demand" else "white", label=f"{rule} storage")
a1.set_xticks(range(4)); a1.set_xticklabels([f"{m}" for m in fleets]); a1.set_xlabel("agents"); a1.set_ylabel("order gain over fixed (%)"); a1.set_ylim(0, 25); a1.legend(frameon=False, fontsize=8); style(a1); panel_title(a1, "(a) gain")
parts = (("mean_wait_for_agent", "wait for an agent"), ("mean_travel_time", "travel"), ("mean_blocked_time", "blocked"))
w = .38
for k, rule in enumerate(("fixed", "demand")):
    bottom = [0]*4
    for j, (key, lab) in enumerate(parts):
        v = [statistics.fmean(r[key] for r in ar.token_passing_rows(m)[rule]) for m in fleets]
        a2.bar([x+(k-.5)*w for x in range(4)], v, w*.95, bottom=bottom, color=["#bbbbbb", "#777777", "#333333"][j], label=lab if k==0 else None, hatch=None if rule=="fixed" else "//", edgecolor="white")
        bottom = [b+x for b, x in zip(bottom, v)]
a2.set_xticks(range(4)); a2.set_xticklabels([f"{m}" for m in fleets]); a2.set_xlabel("agents (left fixed, right demand)"); a2.set_ylabel("pick service time (steps)"); a2.legend(frameon=False, fontsize=8); style(a2); panel_title(a2, "(b) where a pick's time goes")
fig.savefig(sys.argv[1]+"/tp_fleet.png", dpi=200, bbox_inches="tight")
for m in fleets:
    d = ar.token_passing_rows(m)
    print(m, {rule: [round(statistics.fmean(r[k] for r in d[rule]),1) for k,_ in parts] for rule in ("fixed","demand","congestion")}, "crowd/blocked", {rule: round(statistics.fmean(r["mean_blocked_time"] for r in d[rule]),2) for rule in d})
