"""
The backward path of the loop [A93], fig:loop in 3.ProblemFormulation.tex
(Section sec:pf:coupling). It carries on the tea example of
fig:storageexample (arrival_storage.py), drawn in the style of
storage_update.py: white aisle vertices, shelves as slot boxes hanging off
the aisle as leaves, the workstation and the dock as leaves too, agents
only on vertices, and the put-away as the dashed blue arrow.

(a) Demand storage put the new tea on shelf A, the nearest, and the old tea
    is still on shelf C at the far end of the right aisle. Every tea pick
    takes A, so a_1 picks there while a_2 and a_3 wait their turn on the
    aisle. Picks from A stand still about 5 steps, picks from C about 1
    step (the numbers of the pickup example in Section sec:pf:tasks).
(b) Congestion-aware storage reads that. The next tea line takes C, 6
    edges from the workstation against 4 for A, because 6 + 1 < 4 + 5. At
    the next storage update the new tea goes to the empty shelf of the
    quiet aisle, which has no reading yet and so counts zero.
Replaces loop.tex / loop.py / loop.pdf.
"""
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

from base import OUT, C

PUTAWAY = "#2f6fae"
BOX = 0.62
# Aisle vertices: a cross-aisle at the bottom and two aisles going up.
CROSS = [(-1.0, -1.0), (0.0, -1.0), (1.0, -1.0)]
LEFT = [(-1.0, 0.0), (-1.0, 1.2), (-1.0, 2.4)]
RIGHT = [(1.0, 0.0), (1.0, 1.2), (1.0, 2.4)]
WORK = (0.0, -2.0)      # leaf under the middle of the cross-aisle
DOCK = (2.1, -1.0)      # leaf at the right end of the cross-aisle
# Shelves, each a leaf off one aisle vertex: (position, its aisle vertex).
SHELF = {"A": ((-2.1, 0.0), LEFT[0]), "C": ((2.1, 2.4), RIGHT[2]),
         "new": ((2.1, 0.0), RIGHT[0])}
FILL = {"A": 0.75, "C": 0.45, "new": 0.0}   # share of the room tea takes
WALK_C = [WORK, CROSS[1], CROSS[2], RIGHT[0], RIGHT[1], RIGHT[2], SHELF["C"][0]]
WALK_A = [WORK, CROSS[1], CROSS[0], LEFT[0], SHELF["A"][0]]


def _line(ax, a, b):
    ax.plot(*zip(a, b), color=C["edge"], lw=1.6, zorder=1)


def _shelf(ax, name, new_tea=False):
    (x, y), _ = SHELF[name]
    left, bottom = x - BOX / 2, y - BOX / 2
    ax.add_patch(Rectangle((left, bottom), BOX, BOX, fc="white", lw=0, zorder=3))
    ax.add_patch(Rectangle((left, bottom), BOX, BOX * FILL[name], fc=C["store_f"], lw=0,
                           zorder=4))
    if new_tea:
        ax.add_patch(Rectangle((left, bottom), BOX, BOX * 0.5, fc="white", ec=C["store_e"],
                               lw=0.6, hatch="////", zorder=4))
    ax.add_patch(Rectangle((left, bottom), BOX, BOX, fc="none",
                           ec=C["comm"] if new_tea else C["node"],
                           lw=1.6 if new_tea else 0.9, zorder=5))
    if name != "new":
        ax.text(x, bottom + BOX + 0.1, f"shelf {name}", ha="center", va="bottom",
                fontsize=10.5, color=C["text"])


def _agent(ax, p, label, dx=0, dy=13):
    ax.scatter(*p, s=150, c=C["agent"], edgecolors="white", linewidths=1.2, zorder=7)
    ax.annotate(label, p, textcoords="offset points", xytext=(dx, dy), ha="center",
                va="center", fontsize=11, color=C["agent"], zorder=8)


def _walk(ax, path, alpha, ls, lw):
    xs, ys = zip(*path)
    ax.plot(xs, ys, color=C["agent"], lw=lw, alpha=alpha, ls=ls, solid_capstyle="round",
            zorder=2)
    ax.annotate("", xy=path[-1], xytext=path[-2], zorder=2,
                arrowprops=dict(arrowstyle="-|>", lw=lw, color=C["agent"], alpha=alpha,
                                shrinkB=12, linestyle=ls))


def _base(ax, new_tea):
    ax.set_xlim(-3.3, 3.4); ax.set_ylim(-2.6, 3.2)
    ax.set_aspect("equal"); ax.axis("off")
    for aisle in (LEFT, RIGHT):
        _line(ax, aisle[0], (aisle[0][0], -1.0))
        for p0, p1 in zip(aisle, aisle[1:]):
            _line(ax, p0, p1)
    for p0, p1 in zip(CROSS, CROSS[1:]):
        _line(ax, p0, p1)
    _line(ax, CROSS[1], WORK); _line(ax, CROSS[2], DOCK)
    for (p, via) in SHELF.values():
        _line(ax, p, via)
    for p in CROSS + LEFT + RIGHT:
        ax.scatter(*p, s=200, c="white", edgecolors=C["node"], zorder=3)
    for name in SHELF:
        _shelf(ax, name, new_tea=(new_tea and name == "new"))
    ax.scatter(*WORK, s=380, marker="s", c=C["del_f"], edgecolors=C["del_e"], zorder=3)
    ax.annotate("workstation", WORK, textcoords="offset points", xytext=(0, -22),
                ha="center", fontsize=10.5, color=C["del_e"])
    ax.scatter(*DOCK, s=380, marker="^", c=C["rcv_f"], edgecolors=C["rcv_e"], zorder=3)
    ax.annotate("dock", DOCK, textcoords="offset points", xytext=(0, -22),
                ha="center", fontsize=10.5, color=C["rcv_e"])
    ax.text(-1.0, 2.95, "Left aisle", ha="center", fontsize=11, color=C["text"])
    ax.text(1.0, 2.95, "Right aisle", ha="center", fontsize=11, color=C["text"])


def _panel_a(ax):
    _base(ax, new_tea=False)
    _agent(ax, SHELF["A"][0], r"$a_1$", dx=-30, dy=0)
    _agent(ax, LEFT[0], r"$a_2$", dx=13, dy=10)
    _agent(ax, CROSS[0], r"$a_3$", dx=-13, dy=10)
    ax.text(-0.75, -0.5, "waiting", ha="left", va="center", fontsize=10, color=C["agent"])
    (xa, ya), _ = SHELF["A"]
    ax.text(xa, ya - BOX / 2 - 0.45, "picks stood\nstill 5 steps", ha="center", va="top",
            fontsize=10, color=C["agent"])
    (xc, yc), _ = SHELF["C"]
    ax.text(xc, yc - BOX / 2 - 0.12, "picks stood\nstill 1 step", ha="center", va="top",
            fontsize=10, color=C["text"])


def _panel_b(ax):
    _base(ax, new_tea=True)
    off = [(x + 0.07, y + 0.07) for x, y in WALK_A]
    _walk(ax, off, alpha=0.3, ls=(0, (3, 2)), lw=2.0)
    (xa, ya), _ = SHELF["A"]
    ax.text(xa, ya - BOX / 2 - 0.12, "demand storage:\nA, 4 edges", ha="center", va="top",
            fontsize=10, color=C["agent"], alpha=0.55)
    off = [(x + 0.07, y) if x > 0 else (x, y) for x, y in WALK_C]
    _walk(ax, off, alpha=0.85, ls="-", lw=2.8)
    (xc, yc), _ = SHELF["C"]
    ax.text(xc, yc - BOX / 2 - 0.12, "next tea line:\nC, 6 edges", ha="center", va="top",
            fontsize=10, color=C["agent"])
    (xn, yn), _ = SHELF["new"]
    ax.annotate("", xy=(xn, yn - BOX / 2), xytext=DOCK, zorder=6,
                arrowprops=dict(arrowstyle="-|>", lw=2.0, color=PUTAWAY, ls=(0, (3, 2)),
                                shrinkA=12, shrinkB=2, connectionstyle="arc3,rad=0.5"))
    ax.text(xn, yn + BOX / 2 + 0.1, "new tea at the\nnext update", ha="center", va="bottom",
            fontsize=10, color=C["store_e"])


def shelf_loop():
    fig, axes = plt.subplots(1, 2, figsize=(10.0, 5.4))
    _panel_a(axes[0])
    axes[0].set_title("(a) demand storage: every tea pick\ntakes shelf A, and agents wait their turn",
                      fontsize=11, pad=6)
    _panel_b(axes[1])
    axes[1].set_title("(b) congestion-aware storage: the next line\ntakes C, new tea goes to the quiet aisle",
                      fontsize=11, pad=6)
    handles = [
        Line2D([], [], marker="o", ls="", mfc=C["agent"], mec="white", ms=10, label="agent"),
        Line2D([], [], color=C["agent"], lw=3.0, alpha=0.85, label="walk to the chosen tea"),
        Rectangle((0, 0), 1, 1, fc=C["store_f"], ec=C["node"], label="shelf, room taken by tea"),
        Line2D([], [], color=PUTAWAY, lw=2.0, ls=(0, (3, 2)), label="put-away of new stock"),
        Rectangle((0, 0), 1, 1, fc="white", ec=C["store_e"], hatch="////",
                  label="new tea on its way"),
        Rectangle((0, 0), 1, 1, fc="none", ec=C["comm"], lw=1.6, label="shelf a put-away reached"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=3, frameon=False, fontsize=10,
               bbox_to_anchor=(0.5, -0.01))
    fig.tight_layout(rect=[0, 0.1, 1, 1])
    fig.savefig(f"{OUT}/shelf_loop.png"); plt.close(fig)


if __name__ == "__main__":
    shelf_loop()
