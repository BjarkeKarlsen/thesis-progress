"""
Served share of every test seed at 16 agents, one dot per seed, for the long-trained learned
arms ([A110]), with keep-up at f_up = 0.9 ([A111]). Shows why the number of seeds that keep up does not follow the mean: the count
depends on how the seeds spread around f_up = 0.8, and a seed that locks drops far below it.

Run:  python thesis-progress/scripts/images/fleet16_seeds.py   (from the workspace root)
Out:  thesis-progress/scripts/Images/fleet16_seeds.png
      thesis-progress/scripts/Images/fleet16_seeds_short.png   the same for the short runs

Reads the rows `slap-mapd evaluate` wrote under ~/thesis_runs/evaluation/fleet_16, counted with
served_counts.recount ([A96]). A seed locks when two agents hold the same task for 500 steps or
more (`longest_two_agent_hold`, as in tab:exp:locks).
"""
import os
import random
import statistics
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from served_counts import rows, recount, SERVED  # noqa: E402

F_UP = 0.9  # proposed f_up ([A111]); the rows were flagged at 0.8, so keep-up is recounted from the shares
from base import OUT, C, plt  # noqa: E402


def style(ax):
    ax.grid(axis="y", color=C["edge"], alpha=0.3, lw=0.6)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)


def panel_title(ax, text):
    ax.set_title(text, loc="left", fontsize=11, color=C["text"])


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path)
    plt.close(fig)
    return path

SOURCE = os.path.expanduser("~/thesis_runs/evaluation/fleet_16")
LOCK = 500
ARMS = {"centralised": "centralised", "section": "section-\nbased",
        "decentralised": "decentralised", "decentralised_comm": "with\nmessages"}
ARM_COLOUR = {"centralised": C["accent"], "section": C["ep_e"],
              "decentralised": C["del_e"], "decentralised_comm": C["comm"]}
RULES = {"fixed": "fixed", "demand": "demand", "congestion": "congestion-aware"}
# The run folder of the long training, newest part first.
LONG = ("{rule}_long_part2", "{rule}_long")


def seeds(arm, rule, long=True):
    """(served share, keeps up, locked) per test seed, or None when the run is not home."""
    names = LONG if long else ("{rule}",)
    for name in names:
        path = os.path.join(SOURCE, arm, name.format(rule=rule), SERVED, "test.jsonl")
        if os.path.exists(path):
            found = rows(Path(path), rule)
            if found:
                out = []
                for r in found:
                    c = recount(r)
                    up = all(share is None or share >= F_UP
                             for share in (c["served_share_picks"], c["served_share_putaways"]))
                    out.append((c["served_share"], up, r["longest_two_agent_hold"] >= LOCK))
                return out
    return None


def draw(long, name):
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.6), sharey=True)
    rng = random.Random(0)
    for ax, (rule, title) in zip(axes, RULES.items()):
        style(ax)
        ax.axhline(F_UP, color=C["node"], ls="--", lw=1)
        for x, arm in enumerate(ARMS):
            found = seeds(arm, rule, long)
            if found is None:
                ax.text(x, 0.06, "not yet\nevaluated", ha="center", va="bottom", fontsize=8,
                        color=C["node"], style="italic")
                continue
            colour = ARM_COLOUR[arm]
            for share, up, locked in found:
                dx = rng.uniform(-0.2, 0.2)
                if locked:
                    ax.plot(x + dx, share, "x", color=colour, ms=6, mew=1.5)
                else:
                    ax.plot(x + dx, share, "o", ms=5, mec=colour, mew=1.2,
                            mfc=colour if up else "white")
            mean = statistics.fmean(s for s, _, _ in found)
            ax.plot([x - 0.3, x + 0.3], [mean, mean], color=C["text"], lw=2)
            ax.text(x, 1.17, f"{sum(u for _, u, _ in found)}", ha="center", fontsize=9,
                    color=C["text"])
        ax.set_xticks(range(len(ARMS)), ARMS.values(), fontsize=9)
        ax.set_xlim(-0.6, len(ARMS) - 0.4)
        ax.set_ylim(0, 1.25)
        panel_title(ax, title)
    axes[0].set_ylabel("served share per seed")
    handles = [plt.Line2D([], [], ls="", marker="o", mec=C["text"], mfc=C["text"], label="keeps up"),
               plt.Line2D([], [], ls="", marker="o", mec=C["text"], mfc="white", label="falls behind"),
               plt.Line2D([], [], ls="", marker="x", color=C["text"], mew=1.5, label="locks"),
               plt.Line2D([], [], color=C["text"], lw=2, label="mean"),
               plt.Line2D([], [], color=C["node"], ls="--", lw=1, label=r"$f_{\mathrm{up}}$"),
               plt.Line2D([], [], ls="", label="top: seeds that keep up")]
    fig.legend(handles=handles, loc="upper center", ncol=6, frameon=False,
               bbox_to_anchor=(0.5, 1.06), fontsize=9)
    fig.tight_layout()
    return save(fig, name)


if __name__ == "__main__":
    print(draw(True, "fleet16_seeds.png"))
    print(draw(False, "fleet16_seeds_short.png"))
