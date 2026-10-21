import json
import os

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from base import OUT, C

# The four generated warehouses of app:instances, one per fleet size, as the
# configs use them (seed 42). The layouts are exported from the generator by
# slap-mapd-coupling's scripts/instance_report.py (OUT/instances_used.json)
# and copied to data/, so this script needs only the JSON, not the codebase.
DATA = os.path.join(os.path.dirname(__file__), "data", "instances_used.json")

# Receiving has no colour in base.py, since no other figure draws it apart.
RCV_F, RCV_E = "#e8d9f0", C["comm"]
ROLES = (  # drawn in this order, so a role vertex sits on top of the plain ones
    ("storage", C["store_f"], C["store_e"], "o"),
    ("delivery", C["del_f"], C["del_e"], "s"),
    ("receiving", RCV_F, RCV_E, "^"),
    ("endpoint", C["ep_f"], C["ep_e"], "D"),
)


def _panel(ax, inst, title, size):
    pos = {int(v): p for v, p in inst["positions"].items()}
    roles = {int(v): r for v, r in inst["roles"].items()}
    seen = set()
    for u, v in inst["edges"]:
        if (v, u) in seen:
            continue
        seen.add((u, v))
        ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]],
                color=C["edge"], lw=0.8, zorder=1)
    plain = [p for v, p in pos.items() if not roles[v]]
    ax.scatter(*zip(*plain), s=size, facecolor="white", edgecolor=C["node"],
               linewidths=0.6, zorder=2)
    for name, fc, ec, marker in ROLES:
        pts = [pos[v] for v, r in roles.items() if name in r]
        ax.scatter(*zip(*pts), s=size * 1.6, marker=marker, facecolor=fc,
                   edgecolor=ec, linewidths=0.8, zorder=3)
    ax.set_title(title, fontsize=12)
    ax.set_aspect("equal")
    ax.axis("off")


def warehouses():
    with open(DATA) as handle:
        used = json.load(handle)
    fig, axes = plt.subplots(2, 2, figsize=(11, 10.5),
                             gridspec_kw=dict(hspace=0.12, wspace=0.05))
    sizes = {"8": 40, "16": 22, "32": 11, "64": 5}
    for ax, (m, letter) in zip(axes.flat, zip(("8", "16", "32", "64"), "abcd")):
        n = len(used[m]["positions"])
        _panel(ax, used[m], f"({letter}) $m={m}$, $|V|={n}$", sizes[m])
    handles = [Line2D([], [], ls="", marker=mk, markersize=8, markerfacecolor=fc,
                      markeredgecolor=ec, label=lab)
               for (_, fc, ec, mk), lab in zip(
                   ROLES, ("storage", "delivery", "receiving", "parking"))]
    fig.legend(handles=handles, loc="lower center", ncol=4, frameon=False,
               bbox_to_anchor=(0.5, 0.02))
    fig.savefig(os.path.join(OUT, "warehouses.png"))
    plt.close(fig)


if __name__ == "__main__":
    warehouses()
