import json
import os

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch

from base import OUT, C

# The four generated warehouses of app:instances, one per fleet size, as the
# configs use them (seed 42), drawn in van Knippenberg et al.'s style (their
# Figures 1 and 4): aisle vertices small and white, the role vertices coloured,
# two-way edges as plain lines and one-way edges as arrows. The layouts are
# exported from the generator (slap-mapd-coupling's scripts/instance_report.py,
# copied from results/tests/A_graph_v2/warehouses/instances/fleet_*/seed_42.json)
# to data/, so this script needs only the JSON, not the codebase.
# data/instances_used_v1.json holds the graph v1 warehouses, drawn the same way
# so the thesis can show why the design changed (model revision step 09).
DATA = os.path.join(os.path.dirname(__file__), "data")

# Receiving has no colour in base.py, since no other figure draws it apart.
RCV_F, RCV_E = "#e8d9f0", C["comm"]
ROLES = (  # drawn in this order, so a role vertex sits on top of the plain ones
    ("storage", C["store_f"], C["store_e"], "o", "slot"),
    ("delivery", C["del_f"], C["del_e"], "s", "workstation"),
    ("receiving", RCV_F, RCV_E, "^", "dock"),
    ("endpoint", C["ep_f"], C["ep_e"], "D", "parking"),
)
# Marker area of a plain vertex per fleet size. A role vertex is drawn larger.
SIZES = {"8": 34, "16": 14, "32": 6, "64": 2.5}


def _panel(ax, inst, title, size):
    pos = {int(v): p for v, p in inst["positions"].items()}
    roles = {int(v): r for v, r in inst["roles"].items()}
    edges = {(int(u), int(v)) for u, v in inst["edges"]}
    for u, v in edges:
        if (v, u) in edges:
            if u < v:
                ax.plot(*zip(pos[u], pos[v]), color=C["edge"], lw=0.7, zorder=1)
        else:
            ax.add_patch(FancyArrowPatch(
                pos[u], pos[v], arrowstyle="-|>", mutation_scale=4 + size ** 0.5,
                color=C["node"], lw=0.8, shrinkA=1, shrinkB=1, zorder=2))
    plain = [p for v, p in pos.items() if not roles[v]]
    ax.scatter(*zip(*plain), s=size, facecolor="white", edgecolor=C["node"],
               linewidths=0.5, zorder=3)
    for name, fc, ec, marker, _ in ROLES:
        pts = [pos[v] for v, r in roles.items() if name in r]
        if pts:
            ax.scatter(*zip(*pts), s=size * 1.8, marker=marker, facecolor=fc,
                       edgecolor=ec, linewidths=0.7, zorder=4)
    ax.set_title(title, fontsize=12)
    ax.set_aspect("equal")
    ax.axis("off")


def _legend(fig, y):
    handles = [Line2D([], [], ls="", marker=mk, markersize=8, markerfacecolor=fc,
                      markeredgecolor=ec, label=label)
               for _, fc, ec, mk, label in ROLES]
    handles.append(Line2D([], [], color=C["node"], marker=">", markersize=6,
                          lw=1, label="one-way edge"))
    fig.legend(handles=handles, loc="lower center", ncol=5, frameon=False,
               bbox_to_anchor=(0.5, y))


def _four(name, out):
    with open(os.path.join(DATA, name)) as handle:
        used = json.load(handle)
    fig, axes = plt.subplots(2, 2, figsize=(11, 10),
                             gridspec_kw=dict(hspace=0.15, wspace=0.05))
    for ax, (m, letter) in zip(axes.flat, zip(("8", "16", "32", "64"), "abcd")):
        n = len(used[m]["positions"])
        _panel(ax, used[m], f"({letter}) $m={m}$, $|V|={n}$", SIZES[m])
    _legend(fig, 0.03)
    fig.savefig(os.path.join(OUT, out))
    plt.close(fig)


def warehouses():
    """Graph v2, the four fleets (app:instances), and the 8-agent one alone for the chapter."""
    _four("instances_used.json", "warehouses.png")
    _four("instances_used_v1.json", "warehouses_v1.png")
    with open(os.path.join(DATA, "instances_used.json")) as handle:
        m8 = json.load(handle)["8"]
    fig, ax = plt.subplots(figsize=(9, 6.5))
    _panel(ax, m8, "", 60)
    _legend(fig, -0.02)
    fig.savefig(os.path.join(OUT, "warehouse_m8.png"))
    plt.close(fig)


if __name__ == "__main__":
    warehouses()
