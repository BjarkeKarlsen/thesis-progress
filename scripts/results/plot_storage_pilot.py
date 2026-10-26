"""
The learned-storage pilot night, one row per stage. A working plot, not a thesis figure.

Run:  python thesis-progress/scripts/results/plot_storage_pilot.py [RUN_DIR]   (any directory)
Out:  RUN_DIR/plots/pilot.png, RUN_DIR defaults to ~/thesis_runs/storage_pilot_night_2026-10-22

Reads each stage's train/progress.jsonl and eval/rows.jsonl, which slap-mapd-coupling's
scripts/storage_pilot.py writes. Columns, left to right:
(a) the training return per iteration, what the policy maximises,
(b) the pick service time per iteration in training, the rules' test-seed means dashed,
(c) on the 20 test seeds, the put-away service time, the cost of the result,
(d) on the 20 test seeds, the pick service time, with the seeds keeping up beside each point.
Training lines are a 10-iteration rolling mean over the raw values, drawn faint. Test points are
the mean over seeds with the 95 % t interval.
"""
import json
import os
import statistics
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RUN = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser(
    "~/thesis_runs/storage_pilot_night_2026-10-22")
# Every stage folder of RUN with a training log and an evaluation, in name order. Each row of
# the figure is one stage: (directory, title, the cost measure of column (c), its label).
STAGES = tuple(
    (path.name, path.name.replace("fleet", "").replace("_", " agents, credit "),
     "mean_putaway_service_time", "put-away service time")
    for path in sorted(Path(RUN).iterdir())
    if (path / "train" / "progress.jsonl").exists() and (path / "eval" / "rows.jsonl").exists()
)
# Fixed order, shared with plot_parameter_sweep.py, so a rule keeps its colour across figures.
RULES = {"fixed": ("#2a78d6", "o"), "demand": ("#eb6834", "s"), "congestion": ("#1baf7a", "^"),
         "random": ("#eda100", "D"), "learned": ("#e87ba4", "v")}
INK, MUTED, GRID = "#2b2b2b", "#6b6b6b", "#e4e4e0"
T95 = 2.093  # t quantile for 19 degrees of freedom, 20 seeds
WINDOW = 10

plt.rcParams.update({"font.size": 10, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
                     "xtick.color": MUTED, "ytick.color": MUTED, "savefig.dpi": 150,
                     "savefig.bbox": "tight"})


def jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def rolling(values):
    return [statistics.mean(values[max(0, i - WINDOW + 1):i + 1]) for i in range(len(values))]


def mean_and_half_width(values):
    return statistics.mean(values), T95 * statistics.stdev(values) / len(values) ** 0.5


def style(ax):
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)


def training(ax, progress, key, colour):
    xs = [p["iteration"] for p in progress]
    ys = [p[key] for p in progress]
    ax.plot(xs, ys, color=colour, lw=1, alpha=0.25)
    ax.plot(xs, rolling(ys), color=colour, lw=2)
    ax.set_xlabel("iteration")


def test_points(ax, by_rule, key, keep_up=False):
    for i, (rule, (colour, marker)) in enumerate(RULES.items()):
        mean, half = mean_and_half_width([r[key] for r in by_rule[rule]])
        ax.errorbar([i], [mean], yerr=[half], color=colour, marker=marker, ms=8, capsize=4,
                    elinewidth=1.5)
        if keep_up:
            kept = sum(r["keeps_up"] for r in by_rule[rule])
            ax.annotate(f"{kept}/20", (i, mean), xytext=(8, -3), textcoords="offset points",
                        fontsize=9, color=INK if kept == 20 else "#c0392b")
    ax.set_xticks(range(len(RULES)), list(RULES), rotation=30)
    ax.set_xlim(-0.5, len(RULES) - 0.3)


def plot():
    fig, axes = plt.subplots(len(STAGES), 4, figsize=(18, 4.2 * len(STAGES)))
    for row, (name, title, loaded_key, loaded_label) in zip(axes, STAGES):
        progress = jsonl(os.path.join(RUN, name, "train", "progress.jsonl"))
        by_rule = {}
        for r in jsonl(os.path.join(RUN, name, "eval", "rows.jsonl")):
            by_rule.setdefault(r["rule"], []).append(r)
        learned = RULES["learned"][0]

        training(row[0], progress, "mean_return", learned)
        row[0].set_ylabel(f"{title}\n\ntraining return")

        training(row[1], progress, "mean_service_time", learned)
        # Rules whose means lie within 1 of each other share one label.
        labels = []
        for rule in ("fixed", "demand", "random"):
            mean = statistics.mean(r["mean_service_time"] for r in by_rule[rule])
            row[1].axhline(mean, color=RULES[rule][0], ls="--", lw=1.2)
            close = next((label for label in labels if abs(label[0] - mean) < 1.0), None)
            if close:
                close[1].append(rule)
            else:
                labels.append((mean, [rule]))
        for mean, rules in labels:
            row[1].annotate(", ".join(rules), (1, mean), xycoords=("axes fraction", "data"),
                            xytext=(3, 0), textcoords="offset points", va="center",
                            fontsize=9, color=INK)
        row[1].set_ylabel("pick service time, training")

        test_points(row[2], by_rule, loaded_key)
        row[2].set_ylabel(f"{loaded_label}, test")

        test_points(row[3], by_rule, "mean_service_time", keep_up=True)
        row[3].set_ylabel("pick service time, test")
        for ax in row:
            style(ax)
    for ax, letter in zip(axes[0], "abcd"):
        ax.set_title(f"({letter})", loc="left", color=INK)
    fig.suptitle("Learned-storage pilot, Token Passing. Test columns: 20 paired seeds, 95 % "
                 "interval, red counts mean some seeds do not keep up.", y=1.0, color=INK)
    fig.tight_layout()
    out = os.path.join(RUN, "plots")
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, "pilot.png")
    fig.savefig(path)
    plt.close(fig)
    return path


if __name__ == "__main__":
    print(plot())
