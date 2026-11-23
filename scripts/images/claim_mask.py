"""Figure for sec:method:controllers: the zones of the section-based controller and the claim mask.

(a) a small warehouse cut into three zones, blocks of neighbouring aisles, in the viewer's zone
tints. Zone Y_2 has its halo H_2 (eq:halo) hatched, the vertices outside it within travel cost
d_obs = 2, computed here by breadth-first search on unit edge costs. The agents a_1 to a_3 of Y_2
choose one after another in the priority order.
(b) and (c) the two cases of the claim mask (eq:claimmask) that can switch off a move, as in move_blocked of
slap-mapd-coupling (resolution/conflict_resolution.py) that claim_mask (environment/spaces.py)
calls: a_2 on v chooses after a_1 and may not move onto w when (b) a_1 has chosen w, (c) w holds
an agent that has not chosen yet. The third case, a swap, never arises inside one decision,
because a_1 could not have chosen v while a_2 stood there unchosen, so it is not drawn ([A119]).

Run from the workspace root:

    python3 thesis-progress/scripts/images/claim_mask.py
"""
import os
import sys
from collections import deque

sys.path.insert(0, os.path.dirname(__file__))
from base import OUT, PG, aisle_node, dock_mark, plt, shelf_slot, work_mark  # noqa: E402
from warehouses import GROUP_COLOURS, ZONE_EDGE, ZONE_TINT, _tint  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import FancyArrowPatch, Patch, Rectangle  # noqa: E402

D_OBS = 2
AISLES = (0, 3, 6, 9, 12, 15)          # x of the vertical aisles
ZONE_OF_AISLE = (0, 0, 1, 1, 2, 2)     # two neighbouring aisles per zone
ROWS = 4                               # aisle positions per aisle, between the two cross-aisles
Q = 1                                  # the zone shaded and haloed, Y_2
REFUSED = "#8a949e"


def graph():
    """Unit-cost aisle grid: cross-aisles at y = 0 and y = ROWS + 1, vertical aisles, a shelf on
    each side of an aisle position, workstations below the front lane, docks above the back."""
    pos, role, adj = {}, {}, {}

    def add(n, p, r):
        pos[n], role[n] = p, r
        adj.setdefault(n, set())

    def link(a, b):
        adj[a].add(b)
        adj[b].add(a)

    top, bottom = 0, ROWS + 1
    xs = range(AISLES[0], AISLES[-1] + 1)
    for y in (top, bottom):
        for x in xs:
            add((x, y), (x, y), "aisle")
        for x in xs[:-1]:
            link((x, y), (x + 1, y))
    for a in AISLES:
        for y in range(1, ROWS + 1):
            add((a, y), (a, y), "aisle")
            link((a, y), (a, y - 1))
            for s in (a - 1, a + 1):
                if AISLES[0] <= s <= AISLES[-1]:
                    add(("s", s, y), (s, y), "shelf")
                    link(("s", s, y), (a, y))
        link((a, ROWS), (a, bottom))
    for x in (1, 7, 13):
        add(("w", x), (x, bottom + 1), "workstation")
        link(("w", x), (x, bottom))
    for x in (4, 11):
        add(("d", x), (x, top - 1), "dock")
        link(("d", x), (x, top))
    return pos, role, adj


def zone_of(x):
    cuts = [(AISLES[2 * k + 1] + AISLES[2 * k + 2]) / 2 for k in range(len(AISLES) // 2 - 1)]
    return sum(x > c for c in cuts), cuts


def halo(adj, zone, q, d_obs):
    """eq:halo: the vertices outside Y_q within travel cost d_obs of some vertex of Y_q."""
    dist = {v: 0 for v in adj if zone[v] == q}
    queue = deque(dist)
    while queue:
        v = queue.popleft()
        if dist[v] == d_obs:
            continue
        for w in adj[v]:
            if w not in dist:
                dist[w] = dist[v] + 1
                queue.append(w)
    return {v for v in dist if zone[v] != q}


def agent(ax, p, colour, label=None, offset=(0, 13), s=150, fs=12):
    ax.scatter(*p, s=s, c=colour, edgecolors="white", linewidths=1.2, zorder=6)
    if label:
        ax.annotate(label, p, textcoords="offset points", xytext=offset, ha="center",
                    color=PG["text"], fontsize=fs, zorder=7)


def arrow(ax, a, b, colour, refused=False, rad=0.0, lw=1.6):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=13, lw=lw,
                                 color=REFUSED if refused else colour,
                                 ls=(0, (3, 2)) if refused else "-", shrinkA=9, shrinkB=9,
                                 connectionstyle=f"arc3,rad={rad}", zorder=5))
    if refused:
        # the cross sits on the middle of the (possibly curved) arrow
        (x0, y0), (x1, y1) = a, b
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        # arc3 bends by rad times the chord, turned a quarter; the y axis is inverted
        mx, my = mx - rad * (y1 - y0) / 2, my + rad * (x1 - x0) / 2
        ax.scatter(mx, my, marker="x", s=70, c=PG["text"], linewidths=2.0, zorder=7)


def panel_a(ax):
    pos, role, adj = graph()
    zone = {}
    for v, (x, _) in pos.items():
        zone[v], cuts = zone_of(x)
    ring = halo(adj, zone, Q, D_OBS)
    low, high = -1.5, ROWS + 2.5
    edges = [AISLES[0] - 0.6] + cuts + [AISLES[-1] + 0.6]
    for z in range(len(edges) - 1):
        ax.add_patch(Rectangle((edges[z], low), edges[z + 1] - edges[z], high - low, lw=0,
                               fc=_tint(GROUP_COLOURS[z], ZONE_TINT), zorder=0))
        ax.text(edges[z] + 0.25, high - 0.3, f"$Y_{z + 1}$", ha="left",
                va="center", fontsize=13, color=GROUP_COLOURS[z])
    for x in cuts:
        ax.plot((x, x), (low, high), color=ZONE_EDGE, lw=1.2, ls=(0, (4, 2)), zorder=0.5)
    for v in ring:
        x, y = pos[v]
        ax.add_patch(Rectangle((x - 0.5, y - 0.5), 1, 1, fc="none", ec=GROUP_COLOURS[Q],
                               hatch="////", lw=0, zorder=0.8))
    for (x0, y0), (x1, y1) in {tuple(sorted((pos[v], pos[w]))) for v in adj for w in adj[v]}:
        ax.plot((x0, x1), (y0, y1), color=PG["edge"], lw=1.0, zorder=1)
    for v, r in role.items():
        p = pos[v]
        if r == "aisle":
            aisle_node(ax, p, s=26)
        elif r == "shelf":
            shelf_slot(ax, *p, half=0.26)
        elif r == "workstation":
            work_mark(ax, p, s=120)
        else:
            dock_mark(ax, p, s=140)
    # the agents of Y_2 in priority order, and one agent of Y_1 standing in the halo
    agent(ax, (6, 2), PG["to_pickup"], "$a_1$", offset=(-13, -4), s=110, fs=11)
    agent(ax, (9, 4), PG["putaway"], "$a_2$", offset=(-13, -4), s=110, fs=11)
    agent(ax, (8, 0), PG["to_pickup"], "$a_3$", offset=(0, 9), s=110, fs=11)
    agent(ax, (4, ROWS + 1), PG["putaway"], s=110)
    ax.set_xlim(edges[0] - 0.1, edges[-1] + 0.1)
    ax.set_ylim(low - 0.1, high + 0.1)
    ax.set_title(rf"(a) zone $Y_2$ and its halo $H_2$, $d_{{\mathrm{{obs}}}} = {D_OBS}$",
                 fontsize=12, color=PG["text"])


# The small panels: a_2 stands on v, w is the vertex to its right.
V, W = (0, 0), (1, 0)
NEIGHBOURS = ((-1, 0), (0, 1), (0, -1))


def mini(ax, title):
    pts = [V, W, (1, 1), (1, -1)] + list(NEIGHBOURS)
    edges = [(V, W), (W, (1, 1)), (W, (1, -1))] + [(V, n) for n in NEIGHBOURS]
    for (x0, y0), (x1, y1) in edges:
        ax.plot((x0, x1), (y0, y1), color=PG["edge"], lw=1.2, zorder=1)
    for p in pts:
        aisle_node(ax, p, s=40)
    ax.annotate("$v$", V, textcoords="offset points", xytext=(-11, -15), color=PG["text"],
                fontsize=12)
    ax.annotate("$w$", W, textcoords="offset points", xytext=(8, -15), color=PG["text"],
                fontsize=12)
    for n in NEIGHBOURS:
        arrow(ax, V, n, PG["putaway"])
    ax.set_xlim(-1.5, 1.8)
    ax.set_ylim(-1.3, 1.3)
    ax.set_title(title, fontsize=12, color=PG["text"])


def main():
    fig = plt.figure(figsize=(12, 6.9))
    grid = fig.add_gridspec(2, 2, height_ratios=(1.25, 1), hspace=0.12, wspace=0.08)
    ax = fig.add_subplot(grid[0, :])
    panel_a(ax)
    axes = [fig.add_subplot(grid[1, k]) for k in range(2)]

    ax = axes[0]  # (b) a_1 has chosen w
    mini(ax, "(b) $a_1$ has chosen $w$")
    agent(ax, (1, 1), PG["to_pickup"], "$a_1$", offset=(14, -4))
    arrow(ax, (1, 1), W, PG["to_pickup"])
    agent(ax, V, PG["putaway"], "$a_2$", offset=(-10, 10))
    arrow(ax, V, W, PG["putaway"], refused=True)

    ax = axes[1]  # (c) w holds an agent that has not chosen yet
    mini(ax, "(c) $a_3$ on $w$ has not chosen")
    agent(ax, W, PG["to_pickup"], "$a_3$", offset=(14, 5))
    agent(ax, V, PG["putaway"], "$a_2$", offset=(-10, 10))
    arrow(ax, V, W, PG["putaway"], refused=True)

    for ax in [fig.axes[0]] + axes:
        ax.set_aspect("equal")
        ax.invert_yaxis()  # as the viewer draws it, row 0 at the top
        ax.axis("off")

    handles = [
        Line2D([], [], marker="s", ls="", mfc="white", mec=PG["slot_rim"], ms=8, label="shelf"),
        Line2D([], [], marker="s", ls="", mfc=PG["work_f"], mec=PG["work_e"], ms=8,
               label="workstation"),
        Line2D([], [], marker="^", ls="", mfc=PG["dock_f"], mec=PG["dock_e"], ms=9, label="dock"),
        Patch(fc=_tint(GROUP_COLOURS[Q], ZONE_TINT), ec="none", label="zone"),
        Patch(fc="white", ec=GROUP_COLOURS[Q], hatch="////", lw=0, label="halo"),
        Line2D([], [], marker="o", ls="", mfc=PG["to_pickup"], mec="white", ms=9,
               label="agent to a pick"),
        Line2D([], [], marker="o", ls="", mfc=PG["putaway"], mec="white", ms=9,
               label="agent on a put-away"),
        Line2D([], [], color=REFUSED, ls=(0, (3, 2)), marker="x", mec=PG["text"], ms=7,
               lw=1.6, label="switched off"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=len(handles), frameon=False,
               fontsize=10.5, bbox_to_anchor=(0.5, 0.06), handletextpad=0.4, columnspacing=1.1)
    path = os.path.join(OUT, "claim_mask.png")
    fig.savefig(path)
    print("wrote", path)


if __name__ == "__main__":
    main()
