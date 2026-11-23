"""
The tea example in one small warehouse, drawn in the style of storage_update.py: white aisle
vertices, shelves as the V_str circles of fig:instance, the workstation and the dock as leaves,
agents only on vertices, the put-away as the dashed blue arrow. Two figures use it:

- arrival_tea() -> arrival_storage.png, fig:storageexample. New tea under fixed storage goes to
  its home shelf C, under demand storage to shelf A, the shortest trip (dock to shelf to
  workstation, 3 + 4 = 7 steps against 7 + 6 = 13 for C).
- shelf_loop() -> shelf_loop.png, fig:loop ([A93]). One storage period later under demand
  storage every tea pick takes A, so agents wait their turn there. Picks from A stand still
  about 5 steps, from C about 1 (the pickup example of Section sec:pf:tasks). Under
  congestion-aware storage the next line takes C, 6 edges from the workstation against 4 for
  A, because 6 + 1 < 4 + 5, and the new tea goes to the empty shelf N of the quiet aisle,
  trip 5 + 4 = 9 with no reading, against 7 + 5 = 12 for A.

The dock is on the left, as the docks of the thesis warehouses are on the left wall, so that A
and not N is the best trip for demand storage.
"""
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

from base import (OUT, PG, rank_colour, shelf_slot, aisle_node, work_mark, dock_mark,
                  role_handles)

PUTAWAY = PG["putaway"]
PICK = PG["to_pickup"]  # the viewer's colour of an agent on its way to a pick
TEA = rank_colour(0, 3)  # tea is the most popular SKU
RAD = 0.28  # half the side of a shelf slot
CROSS = [(-1.0, -1.0), (0.0, -1.0), (1.0, -1.0)]
LEFT = [(-1.0, 0.0), (-1.0, 1.2), (-1.0, 2.4)]
RIGHT = [(1.0, 0.0), (1.0, 1.2), (1.0, 2.4)]
WORK = (0.0, -2.0)      # leaf under the middle of the cross-aisle
DOCK = (-2.1, -1.0)     # leaf at the left end of the cross-aisle
SHELF = {"A": ((-2.1, 0.0), LEFT[0]), "C": ((2.1, 2.4), RIGHT[2]),
         "N": ((2.1, 0.0), RIGHT[0])}
WALK = {"A": [WORK, CROSS[1], CROSS[0], LEFT[0], SHELF["A"][0]],
        "C": [WORK, CROSS[1], CROSS[2], RIGHT[0], RIGHT[1], RIGHT[2], SHELF["C"][0]]}


def _line(ax, a, b):
    ax.plot(*zip(a, b), color=PG["edge"], lw=1.6, zorder=1)


def _shelf(ax, name, fill, new=0.0, reached=False, faded=False, label=True):
    """A shelf as the viewer's slot, filled from the bottom with tea, new tea on its way
    striped on top, with a purple rim when a put-away reached it ([A104])."""
    (x, y), _ = SHELF[name]
    a = 0.4 if faded else 1.0
    shelf_slot(ax, x, y, RAD, bands=[(fill, TEA)] if fill else (), new=new, reached=reached,
               alpha=a)
    if label:
        ax.text(x, y + RAD + 0.1, name, ha="center", va="bottom",
                fontsize=10.5, color=PG["text"], alpha=a)


def _agent(ax, p, label, dx=0, dy=13):
    ax.scatter(*p, s=150, c=PICK, linewidths=0, zorder=7)
    ax.annotate(label, p, textcoords="offset points", xytext=(dx, dy), ha="center",
                va="center", fontsize=11, color=PG["text"], zorder=8)


def _route(ax, path, color, ls, lw, alpha, dx):
    """A trip drawn along the aisles it uses, shifted off the edges by dx so that two trips
    on the same edge stay apart, with an arrowhead at its end."""
    path = [(x + dx, y + dx) for x, y in path]
    xs, ys = zip(*path)
    ax.plot(xs[:-1] + (xs[-1],), ys, color=color, lw=lw, alpha=alpha, ls=ls,
            solid_capstyle="butt", zorder=2)
    ax.annotate("", xy=path[-1], xytext=path[-2], zorder=2,
                arrowprops=dict(arrowstyle="-|>,head_length=0.5,head_width=0.25", lw=lw,
                                color=color, alpha=alpha, shrinkB=RAD * 30, shrinkA=0))


def _walk(ax, path, alpha=1.0, ls="-", lw=1.8, dx=0.07):
    _route(ax, path, PICK, ls, lw, alpha, dx)


PUT = {"A": [DOCK, CROSS[0], LEFT[0], SHELF["A"][0]],
       "C": [DOCK, CROSS[0], CROSS[1], CROSS[2], RIGHT[0], RIGHT[1], RIGHT[2], SHELF["C"][0]],
       "N": [DOCK, CROSS[0], CROSS[1], CROSS[2], RIGHT[0], SHELF["N"][0]]}


def _putaway(ax, name, rad=None):
    """The put-away from the dock to the shelf, along the aisles, on the other side of the
    edges from a pick."""
    _route(ax, PUT[name], PUTAWAY, (0, (3, 2)), 1.6, 1.0, -0.07)


def _note(ax, name, text, color, below=True, alpha=1.0):
    (x, y), _ = SHELF[name]
    if below:
        ax.text(x, y - RAD - 0.12, text, ha="center", va="top", fontsize=10, color=color,
                alpha=alpha)
    else:  # above the shelf's name
        ax.text(x, y + RAD + 0.5, text, ha="center", va="bottom", fontsize=10,
                color=color, alpha=alpha)


def _base(ax, shelves):
    """The warehouse, and each shelf in `shelves` as {name: dict of _shelf arguments}."""
    ax.set_xlim(-3.3, 3.4); ax.set_ylim(-2.6, 3.0)
    ax.set_aspect("equal"); ax.axis("off")
    for aisle in (LEFT, RIGHT):
        _line(ax, aisle[0], (aisle[0][0], -1.0))
        for p0, p1 in zip(aisle, aisle[1:]):
            _line(ax, p0, p1)
    for p0, p1 in zip(CROSS, CROSS[1:]):
        _line(ax, p0, p1)
    _line(ax, CROSS[1], WORK); _line(ax, CROSS[0], DOCK)
    for (p, via) in SHELF.values():
        _line(ax, p, via)
    for p in CROSS + LEFT + RIGHT:
        aisle_node(ax, p)
    for name in SHELF:
        _shelf(ax, name, **shelves.get(name, dict(fill=0.0, label=False)))
    work_mark(ax, WORK)
    ax.annotate("workstation", WORK, textcoords="offset points", xytext=(0, -22),
                ha="center", fontsize=10.5, color=PG["text"])
    dock_mark(ax, DOCK)
    ax.annotate("dock", DOCK, textcoords="offset points", xytext=(0, -22),
                ha="center", fontsize=10.5, color=PG["text"])


def _legend(fig, extra=()):
    handles = role_handles() + list(extra) + [
        Rectangle((0, 0), 1, 1, fc=TEA, ec="none", label="tea"),
        Rectangle((0, 0), 1, 1, fc="white", ec=PUTAWAY, lw=1.4, hatch="////", label="new tea"),
        Line2D([], [], color=PICK, lw=1.8, label="pick"),
        Line2D([], [], color=PUTAWAY, lw=1.6, ls=(0, (3, 2)), label="put-away"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=len(handles), frameon=False, fontsize=9.5,
               bbox_to_anchor=(0.5, -0.01), handletextpad=0.4, columnspacing=1.0)


def arrival_tea():
    fig, axes = plt.subplots(1, 2, figsize=(10.0, 4.9))
    # (a) fixed storage: the new tea goes to its home shelf C, far from the workstation.
    ax = axes[0]
    _base(ax, {"C": dict(fill=0.25, new=0.45, reached=True), "A": dict(fill=0.0)})
    _putaway(ax, "C", -0.35)
    _walk(ax, WALK["C"])
    _note(ax, "C", "6 edges", PG["text"])
    ax.set_title("(a) Fixed storage", fontsize=11, pad=4)
    # (b) demand storage: the new tea goes to A, the shortest trip. C's old tea runs out.
    ax = axes[1]
    _base(ax, {"C": dict(fill=0.25, faded=True), "A": dict(fill=0.0, new=0.45, reached=True)})
    _putaway(ax, "A", -0.45)
    _walk(ax, WALK["A"])
    _note(ax, "A", "4 edges", PG["text"], below=False)
    ax.set_title("(b) Demand storage", fontsize=11, pad=4)
    _legend(fig)
    fig.tight_layout(rect=[0, 0.07, 1, 1])
    fig.savefig(f"{OUT}/arrival_storage.png"); plt.close(fig)


def shelf_loop():
    fig, axes = plt.subplots(1, 2, figsize=(10.0, 4.9))
    # (a) demand storage, a period later: every tea pick takes A, agents wait their turn.
    ax = axes[0]
    _base(ax, {"A": dict(fill=0.75), "C": dict(fill=0.25)})
    _agent(ax, SHELF["A"][0], r"$a_1$", dx=-30, dy=0)
    _agent(ax, LEFT[0], r"$a_2$", dx=13, dy=10)
    _agent(ax, CROSS[0], r"$a_3$", dx=13, dy=10)
    ax.text(-0.75, -0.5, "waiting", ha="left", va="center", fontsize=10, color=PG["text"])
    _note(ax, "A", "stood still 5 steps", PG["text"], below=False)
    _note(ax, "C", "stood still 1 step", PG["text"])
    ax.set_title("(a) Demand storage, one period later", fontsize=11, pad=4)
    # (b) congestion-aware storage: the next line takes C, the new tea goes to N.
    ax = axes[1]
    _base(ax, {"A": dict(fill=0.75), "C": dict(fill=0.25),
               "N": dict(fill=0.0, new=0.5, reached=True, label=False)})
    _walk(ax, WALK["A"], alpha=0.35, ls=(0, (1, 1.5)), lw=1.4)
    _walk(ax, WALK["C"])
    _note(ax, "C", "6 edges", PG["text"])
    _putaway(ax, "N", 0.35)
    ax.set_title("(b) Congestion-aware storage", fontsize=11, pad=4)
    _legend(fig, extra=[Line2D([], [], marker="o", ls="", mfc=PICK, mec=PICK, ms=8,
                               label="agent")])
    fig.tight_layout(rect=[0, 0.07, 1, 1])
    fig.savefig(f"{OUT}/shelf_loop.png"); plt.close(fig)


if __name__ == "__main__":
    arrival_tea()
    shelf_loop()
