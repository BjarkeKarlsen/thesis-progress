"""Tasks finished per step in the long training of each learned controller at 16 agents, one panel
per storage rule, Token Passing's test throughput dashed (5.Experiments, fig:exp:learning, [A142]).
The training return is not drawn, because the shaping term dominates it.

Run:  ~/.venvs/rl/bin/python thesis-progress/scripts/images/fleet16_training.py   (workspace root)
Reads ~/thesis_runs/training/fleet_16/<arm>/<run>/*_training_progress.jsonl, long run then part 2.
"""
import json, glob, statistics, sys
from pathlib import Path
T = Path.home()/"Documents/thesis/thesis-progress/scripts"
sys.path[:0] = [str(T), str(T/"images")]
import appendix_results as ar
from appendix_data import C, plt, style, panel_title, ARM_COLOUR, save
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
print(save(fig, "fleet16_training.png"))

