import json
import os

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

from base import OUT, C

# Figure 2 of model revision step 09: the stock on every slot of the 8-agent
# warehouse at three moments, under fixed, demand and random storage (Token
# Passing, one seed). A slot is a small box filled from the bottom, one band
# per SKU, as far as the units take up of its capacity. The band's shade is
# the SKU's popularity rank at that moment, dark the most popular. The red
# number is the picks waiting on the slot. A slot outlined in the dock colour
# has received a put-away by then, so the outlines are the storage rule's own
# decisions. Data from stock_moments_data.py.
DATA = os.path.join(os.path.dirname(__file__), "data", "stock_moments.json")
RANKS = cm.Blues_r  # rank 0, the most popular, darkest
PALE = 0.75  # the least popular rank's place on the scale, still visible on white
WAIT = "#c0392b"
BOX = 1.0  # side of a slot box, in position units


def _panel(ax, warehouse, moment):
    pos = {int(v): p for v, p in warehouse["positions"].items()}
    roles = {int(v): r for v, r in warehouse["roles"].items()}
    caps = {int(v): c for v, c in warehouse["capacities"].items()}
    edges = {(s, t) for s, t in warehouse["edges"]}
    for s, t in edges:
        if s < t or (t, s) not in edges:
            ax.plot(*zip(pos[s], pos[t]), color=C["edge"], lw=0.5, zorder=1)
    for role, colour, marker in (("delivery", C["del_e"], "s"), ("receiving", C["comm"], "^")):
        pts = [pos[v] for v, r in roles.items() if role in r]
        ax.scatter(*zip(*pts), s=14, marker=marker, color=colour, zorder=2)
    norm = Normalize(0, moment["skus"] - 1)
    slots = moment["slots"]
    stored = set(moment["stored"])
    for v, cap in caps.items():
        x, y = pos[v]
        left, bottom = x - BOX / 2, y - BOX / 2
        ax.add_patch(Rectangle((left, bottom), BOX, BOX, facecolor="white", lw=0, zorder=3))
        entry = slots.get(str(v))
        if entry:
            level = bottom
            for rank, used in entry["fill"]:
                h = BOX * used / cap
                ax.add_patch(Rectangle((left, level), BOX, h, facecolor=RANKS(norm(rank) * PALE),
                                       lw=0, zorder=4))
                level += h
            if entry["waiting"]:
                ax.text(x + BOX * 0.55, y + BOX * 0.55, str(entry["waiting"]), color=WAIT,
                        fontsize=6, fontweight="bold", ha="left", va="bottom", zorder=6)
        put = v in stored
        ax.add_patch(Rectangle((left, bottom), BOX, BOX, facecolor="none",
                               edgecolor=C["comm"] if put else C["node"],
                               lw=1.6 if put else 0.5, zorder=5))
    ax.set_aspect("equal")
    ax.axis("off")


def stock_moments():
    with open(DATA) as handle:
        data = json.load(handle)
    rules = ("fixed", "demand", "random")
    moments = [str(t) for t in data["moments"]]
    fig, axes = plt.subplots(3, 3, figsize=(13, 9.4),
                             gridspec_kw=dict(hspace=0.08, wspace=0.03))
    for row, rule in enumerate(rules):
        for col, t in enumerate(moments):
            ax = axes[row, col]
            _panel(ax, data["warehouse"], data["rules"][rule][t])
            if row == 0:
                ax.set_title(f"$t = {t}$", fontsize=12)
            if col == 0:
                ax.text(-0.02, 0.5, f"{rule}", transform=ax.transAxes, rotation=90,
                        ha="right", va="center", fontsize=12)
    bar = fig.add_axes([0.25, 0.055, 0.25, 0.012])
    scale = fig.colorbar(cm.ScalarMappable(Normalize(0, PALE), RANKS), cax=bar,
                         orientation="horizontal", ticks=[0, PALE])
    scale.ax.set_xticklabels(["most popular", "least popular"], fontsize=9)
    scale.ax.set_title("SKU popularity rank", fontsize=9)
    handles = [Line2D([], [], ls="", marker="$3$", color=WAIT, markersize=7,
                      label="picks waiting on the slot"),
               Line2D([], [], ls="", marker="s", markerfacecolor="none", markeredgecolor=C["comm"],
                      markeredgewidth=1.6, markersize=8, label="slot a put-away reached"),
               Line2D([], [], ls="", marker="s", color=C["del_e"], markersize=5,
                      label="workstation"),
               Line2D([], [], ls="", marker="^", color=C["comm"], markersize=5, label="dock")]
    fig.legend(handles=handles, loc="lower left", bbox_to_anchor=(0.57, 0.025), ncol=2,
               frameon=False, fontsize=9)
    fig.savefig(os.path.join(OUT, "stock_moments.png"))
    plt.close(fig)


if __name__ == "__main__":
    stock_moments()
