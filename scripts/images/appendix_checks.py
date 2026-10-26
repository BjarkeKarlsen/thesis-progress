"""
The figure of the Simulator checks appendix (K.Checks.tex, app:repro).

Run:  python thesis-progress/scripts/images/appendix_checks.py   (from the workspace root)
Out:  thesis-progress/scripts/Images/app_timing.png   fig:app:timing

Reads results/timing/fleet_<m>/<arm>/timing.jsonl, the timing log of
measures_catalogue.md, one line per episode with {"parts": {part: {"seconds", "calls"}}}.
Written by M4 of decisions/active/measures_plan.md, not built yet, so the part names below
are proposals. A missing run is drawn as a placeholder.
"""
import os

from appendix_data import RESULTS, FLEETS, ARMS, C, plt, read_jsonl, style, placeholder, save

TIMING = os.path.join(RESULTS, "timing")
# The six stages of the step (4.Implementation.tex), routing split in two, then the parts
# outside the stages.
PARTS = (("release", "1 release"), ("assignment", "2 assignment"),
         ("observations", "3a observations"), ("forward", "3b forward pass"),
         ("resolution", "4 resolution"), ("moves", "5 moves and log"),
         ("storage", "6 storage"), ("crowding", "crowding"), ("reward", "reward"),
         ("measures", "end measures"))
SHADES = ("#2f6fae", "#5b8fc4", "#c9761a", "#e0a35f", "#3f8f45", "#7fbf83", "#7d3c98",
          "#9aa5b1", "#c0c8d0", "#e2e6ea")


def timing(arms=("token_passing", "decentralised")):
    """The share of an episode's wall-clock time spent in each part of the step, summed over
    episodes, one bar per fleet and arm. A part taking most of the step shows at once."""
    bars, labels = [], []
    for arm in arms:
        for fleet in FLEETS:
            rows = read_jsonl(os.path.join(TIMING, f"fleet_{fleet}", arm, "timing.jsonl"))
            if not rows:
                continue
            seconds = [sum(r["parts"].get(key, {}).get("seconds", 0.0) for r in rows)
                       for key, _ in PARTS]
            total = sum(seconds) or 1.0
            bars.append([s / total for s in seconds])
            labels.append(f"{ARMS[arm]}, {fleet}")
    fig, ax = plt.subplots(figsize=(6.8, 0.45 * max(len(bars), 4) + 1.4))
    for i, bar in enumerate(bars):
        left = 0.0
        for (_, name), value, colour in zip(PARTS, bar, SHADES):
            ax.barh(i, value, left=left, color=colour, label=name if i == 0 else None)
            left += value
    ax.set_yticks(range(len(labels)), labels)
    ax.invert_yaxis()
    ax.set_xlim(0, 1)
    ax.set_xlabel("share of the step time")
    style(ax)
    if bars:
        ax.legend(ncol=5, frameon=False, fontsize=8, loc="upper center",
                  bbox_to_anchor=(0.5, -0.25))
    else:
        placeholder(ax, "results/timing/fleet_<m>/<arm>/timing.jsonl")
    return save(fig, "app_timing.png")


def appendix_checks():
    return [timing()]


if __name__ == "__main__":
    for path in appendix_checks():
        print(path)
