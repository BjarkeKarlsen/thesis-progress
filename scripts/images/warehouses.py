import json
import os

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch

from base import OUT, C, PG, ROLE_MARK

# The generated warehouses of app:instances, one per fleet size at seed 42 and four
# seeds of the 8-agent warehouse, in the pygame viewer's style ([A104], base.py
# ROLE_MARK): aisle positions small and white, the role vertices coloured, two-way
# edges as plain lines and one-way edges as arrows. Workstations are ringed by the
# category they serve ([A77], four neighbouring rack faces per category), and the
# 16-agent panel also shows the three zones of the section-based controller
# (zones_by_aisle), both as the viewer's W and Z layers. The layouts are exported
# from the generator by warehouses_data.py to data/warehouses_fleet.json, so this
# script needs only the JSON, not the codebase.
# data/instances_used_v1.json holds the graph v1 warehouses, drawn the same way
# so the thesis can show why the design changed (model revision step 09).
DATA = os.path.join(os.path.dirname(__file__), "data")

# The viewer's marks ([A104], base.py ROLE_MARK): a shelf an empty square slot, a
# workstation an orange square, a dock a purple triangle, parking a green diamond.
ROLES = (  # drawn in this order, so a role vertex sits on top of the plain ones
    ("storage", "shelf"), ("delivery", "workstation"), ("receiving", "dock"),
    ("endpoint", "parking"),
)
ROLES = tuple((name, ROLE_MARK[name][0], ROLE_MARK[name][1], ROLE_MARK[name][2], label)
              for name, label in ROLES)
# Marker area of a plain vertex per fleet size. A role vertex is drawn larger.
SIZES = {"8": 34, "16": 14, "32": 6, "64": 2.5}


def _panel(ax, inst, title, size):
    pos = {int(v): p for v, p in inst["positions"].items()}
    roles = {int(v): r for v, r in inst["roles"].items()}
    # Two edge formats: a list of directed pairs (instances_used.json), or one entry
    # per edge with its one-way flag (warehouses_step12.json).
    if inst["edges"] and len(inst["edges"][0]) == 3:
        edges = set()
        for u, v, one_way in inst["edges"]:
            edges.add((int(u), int(v)))
            if not one_way:
                edges.add((int(v), int(u)))
    else:
        edges = {(int(u), int(v)) for u, v in inst["edges"]}
    for u, v in edges:
        if (v, u) in edges:
            if u < v:
                ax.plot(*zip(pos[u], pos[v]), color=C["edge"], lw=0.7, zorder=1)
        else:
            ax.add_patch(FancyArrowPatch(
                pos[u], pos[v], arrowstyle="-|>", mutation_scale=4 + size ** 0.5,
                color=PG["one_way"], lw=0.8, shrinkA=1, shrinkB=1, zorder=2))
    plain = [p for v, p in pos.items() if not roles[v]]
    ax.scatter(*zip(*plain), s=size * 0.5, facecolor="white", edgecolor=PG["transit"],
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
    handles.append(Line2D([], [], color=PG["one_way"], marker=">", markersize=6,
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


# The viewer's Z and W layers (viz/pygame_renderer.py _GROUP_COLOURS, _ZONE_TINT,
# _SECTION_OFFSET): a zone is a pale tint of its colour with a dark line where two zones
# meet, and a workstation gets a ring in the colour of its category. The categories start
# further down the list, so a category never shares a colour with a zone.
GROUP_COLOURS = ("#1f77b4", "#2ca02c", "#ff7f0e", "#9467bd", "#17becf", "#d62728",
                 "#8c564b", "#e377c2", "#bcbd22", "#7f7f7f")
ZONE_TINT = 0.78
ZONE_EDGE = "#282828"
CATEGORY_OFFSET = 5
GRID = 1.5  # the generator's grid step, so a tinted square per vertex touches its neighbours


def _tint(colour, share):
    rgb = [int(colour[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(round(c + (255 - c) * share) for c in rgb)


def _category_colour(index):
    return GROUP_COLOURS[(index + CATEGORY_OFFSET) % len(GROUP_COLOURS)]


def _layers(ax, inst, size, zones):
    """The workstation categories as rings, and with `zones` the zone strips."""
    from matplotlib.patches import Rectangle
    pos = {int(v): p for v, p in inst["positions"].items()}
    if zones:
        # A zone is a block of consecutive aisles, so it is drawn as one strip from the
        # front lane to the back lane, its edge halfway to the next zone's first vertex.
        zone = {int(v): z for v, z in inst["zone"].items()}
        ys = [p[1] for p in pos.values()]
        low, high = min(ys) - GRID / 2, max(ys) + GRID / 2
        spans = [(min(pos[v][0] for v, k in zone.items() if k == z),
                  max(pos[v][0] for v, k in zone.items() if k == z))
                 for z in sorted(set(zone.values()))]
        cuts = [spans[0][0] - GRID / 2]
        cuts += [(spans[z][1] + spans[z + 1][0]) / 2 for z in range(len(spans) - 1)]
        cuts.append(spans[-1][1] + GRID / 2)
        for z in range(len(spans)):
            ax.add_patch(Rectangle((cuts[z], low), cuts[z + 1] - cuts[z], high - low, lw=0,
                                   fc=_tint(GROUP_COLOURS[z], ZONE_TINT), zorder=0))
            ax.text((cuts[z] + cuts[z + 1]) / 2, high + 0.3, f"zone {z + 1}", ha="center",
                    va="bottom", fontsize=9, color=GROUP_COLOURS[z])
        for x in cuts[1:-1]:
            ax.plot((x, x), (low, high), color=ZONE_EDGE, lw=1.4, ls=(0, (4, 2)), zorder=0.5)
    category = {int(v): int(c) for v, c in inst["category"].items()}
    order = sorted(set(category.values()))
    for v, c in category.items():
        ax.scatter(*pos[v], s=size * 5.5, marker="o", facecolor="none",
                   edgecolor=_category_colour(order.index(c)), linewidths=1.6, zorder=5)


def _fleet_legend(fig, y, zones):
    handles = [Line2D([], [], ls="", marker=mk, markersize=8, markerfacecolor=fc,
                      markeredgecolor=ec, label=label)
               for _, fc, ec, mk, label in ROLES]
    handles.append(Line2D([], [], color=PG["one_way"], marker=">", markersize=6,
                          lw=1, label="one-way edge"))
    handles.append(Line2D([], [], ls="", marker="o", markersize=11, markerfacecolor="none",
                          markeredgecolor=_category_colour(0), markeredgewidth=1.6,
                          label="workstation category"))
    if zones:
        from matplotlib.patches import Patch
        handles.append(Patch(fc=_tint(GROUP_COLOURS[0], ZONE_TINT), ec="none",
                             label="zone"))
    fig.legend(handles=handles, loc="lower center", ncol=len(handles), frameon=False,
               bbox_to_anchor=(0.5, y), fontsize=10, handletextpad=0.3, columnspacing=1.2)


def _fleet(key, out, title, height=10, zones_on=()):
    """Four panels of data/warehouses_fleet.json (warehouses_data.py), the warehouses
    of the training configs ([A73], [A74], [A77]). Every panel rings the workstations by
    category, and the panels in `zones_on` also show the zones of the section-based
    controller."""
    with open(os.path.join(DATA, "warehouses_fleet.json")) as handle:
        items = json.load(handle)[key]
    fig, axes = plt.subplots(2, 2, figsize=(11, height),
                             gridspec_kw=dict(hspace=0.12, wspace=0.05))
    for i, (ax, inst, letter) in enumerate(zip(axes.flat, items, "abcd")):
        size = SIZES[str(inst["fleet"])]
        _panel(ax, inst, "", size)
        _layers(ax, inst, size, i in zones_on)
        ax.set_title(f"({letter}) " + title(inst), fontsize=11, color=PG["text"],
                     pad=16 if i in zones_on else 6)
    _fleet_legend(fig, 0.02, bool(zones_on))
    fig.savefig(os.path.join(OUT, out))
    plt.close(fig)


def warehouses():
    """app:instances: the four fleet sizes at seed 42, and four seeds of the
    8-agent warehouse. Graph v1 and the 8-agent one alone are kept from before."""
    _fleet("sizes", "warehouses.png",
           lambda inst: f"{inst['fleet']} agents, $|V|={len(inst['roles'])}$", zones_on=(1,))
    _fleet("seeds", "warehouses_seeds.png", lambda inst: f"seed {inst['seed']}", height=7)
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
