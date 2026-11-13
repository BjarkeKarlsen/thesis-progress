"""
The tea example in one small warehouse, drawn in the style of storage_update.py: white aisle
vertices, shelves as slot boxes hanging off the aisle, the workstation and the dock as leaves,
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

from base import OUT, C

PUTAWAY = "#2f6fae"
BOX = 0.62
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
    ax.plot(*zip(a, b), color=C["edge"], lw=1.6, zorder=1)


def _shelf(ax, name, fill, new=0.0, reached=False, faded=False, label=True):
    """A slot box: the room, filled from the bottom with tea, new tea on its way striped on
    top, outlined in purple when a put-away reached it."""
    (x, y), _ = SHELF[name]
    a = 0.4 if faded else 1.0
    left, bottom = x - BOX / 2, y - BOX / 2
    ax.add_patch(Rectangle((left, bottom), BOX, BOX, fc="white", lw=0, zorder=3))
    ax.add_patch(Rectangle((left, bottom), BOX, BOX * fill, fc=C["store_f"], lw=0, alpha=a,
                           zorder=4))
    if new:
        ax.add_patch(Rectangle((left, bottom + BOX * fill), BOX, BOX * new, fc="white",
                               ec=C["store_e"], lw=0.6, hatch="////", zorder=4))
    ax.add_patch(Rectangle((left, bottom), BOX, BOX, fc="none",
                           ec=C["comm"] if reached else C["node"],
                           lw=1.6 if reached else 0.9, alpha=a, zorder=5))
    if label:
        ax.text(x, bottom + BOX + 0.1, f"shelf {name}", ha="center", va="bottom",
                fontsize=10.5, color=C["text"], alpha=a)


def _agent(ax, p, label, dx=0, dy=13):
    ax.scatter(*p, s=150, c=C["agent"], edgecolors="white", linewidths=1.2, zorder=7)
    ax.annotate(label, p, textcoords="offset points", xytext=(dx, dy), ha="center",
                va="center", fontsize=11, color=C["agent"], zorder=8)


def _walk(ax, path, alpha=0.85, ls="-", lw=2.8, dx=0.07):
    path = [(x + dx, y + dx) for x, y in path]
    xs, ys = zip(*path)
    ax.plot(xs, ys, color=C["agent"], lw=lw, alpha=alpha, ls=ls, solid_capstyle="round",
            zorder=2)
    ax.annotate("", xy=path[-1], xytext=path[-2], zorder=2,
                arrowprops=dict(arrowstyle="-|>", lw=lw, color=C["agent"], alpha=alpha,
                                shrinkB=12, linestyle=ls))


def _putaway(ax, name, rad):
    (x, y), _ = SHELF[name]
    ax.annotate("", xy=(x, y - BOX / 2), xytext=DOCK, zorder=6,
                arrowprops=dict(arrowstyle="-|>", lw=2.0, color=PUTAWAY, ls=(0, (3, 2)),
                                shrinkA=12, shrinkB=2, connectionstyle=f"arc3,rad={rad}"))


def _note(ax, name, text, color, below=True, alpha=1.0):
    (x, y), _ = SHELF[name]
    if below:
        ax.text(x, y - BOX / 2 - 0.12, text, ha="center", va="top", fontsize=10, color=color,
                alpha=alpha)
    else:  # above the shelf's name
        ax.text(x, y + BOX / 2 + 0.5, text, ha="center", va="bottom", fontsize=10,
                color=color, alpha=alpha)


def _base(ax, shelves):
    """The warehouse, and each shelf in `shelves` as {name: dict of _shelf arguments}."""
    ax.set_xlim(-3.3, 3.4); ax.set_ylim(-2.6, 3.2)
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
        ax.scatter(*p, s=200, c="white", edgecolors=C["node"], zorder=3)
    for name in SHELF:
        _shelf(ax, name, **shelves.get(name, dict(fill=0.0, label=False)))
    ax.scatter(*WORK, s=380, marker="s", c=C["del_f"], edgecolors=C["del_e"], zorder=3)
    ax.annotate("workstation", WORK, textcoords="offset points", xytext=(0, -22),
                ha="center", fontsize=10.5, color=C["del_e"])
    ax.scatter(*DOCK, s=380, marker="^", c=C["rcv_f"], edgecolors=C["rcv_e"], zorder=3)
    ax.annotate("dock", DOCK, textcoords="offset points", xytext=(0, -22),
                ha="center", fontsize=10.5, color=C["rcv_e"])
    ax.text(-1.0, 2.95, "Left aisle", ha="center", fontsize=11, color=C["text"])
    ax.text(1.0, 2.95, "Right aisle", ha="center", fontsize=11, color=C["text"])


def _legend(fig, extra=()):
    handles = list(extra) + [
        Line2D([], [], color=C["agent"], lw=3.0, alpha=0.85, label="walk to the chosen tea"),
        Rectangle((0, 0), 1, 1, fc=C["store_f"], ec=C["node"], label="shelf, room taken by tea"),
        Line2D([], [], color=PUTAWAY, lw=2.0, ls=(0, (3, 2)), label="put-away of new stock"),
        Rectangle((0, 0), 1, 1, fc="white", ec=C["store_e"], hatch="////",
                  label="new tea on its way"),
        Rectangle((0, 0), 1, 1, fc="none", ec=C["comm"], lw=1.6, label="shelf a put-away reached"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=3, frameon=False, fontsize=10,
               bbox_to_anchor=(0.5, -0.01))


def arrival_tea():
    fig, axes = plt.subplots(1, 2, figsize=(10.0, 5.4))
    # (a) fixed storage: the new tea goes to its home shelf C, far from the workstation.
    ax = axes[0]
    _base(ax, {"C": dict(fill=0.25, new=0.45, reached=True), "A": dict(fill=0.0)})
    _putaway(ax, "C", -0.35)
    _walk(ax, WALK["C"])
    _note(ax, "C", "order walks\n6 edges", C["agent"])
    ax.set_title("(a) fixed storage: new tea goes\nto its home shelf C", fontsize=11, pad=6)
    # (b) demand storage: the new tea goes to A, the shortest trip. C's old tea runs out.
    ax = axes[1]
    _base(ax, {"C": dict(fill=0.25, faded=True), "A": dict(fill=0.0, new=0.45, reached=True)})
    _putaway(ax, "A", -0.45)
    _walk(ax, WALK["A"])
    _note(ax, "A", "order walks\n4 edges", C["agent"], below=False)
    _note(ax, "C", "old tea,\nruns out", C["store_e"], alpha=0.6)
    ax.set_title("(b) demand storage: new tea goes\nto A, the shortest trip", fontsize=11, pad=6)
    _legend(fig)
    fig.tight_layout(rect=[0, 0.1, 1, 1])
    fig.savefig(f"{OUT}/arrival_storage.png"); plt.close(fig)


def shelf_loop():
    fig, axes = plt.subplots(1, 2, figsize=(10.0, 5.4))
    # (a) demand storage, a period later: every tea pick takes A, agents wait their turn.
    ax = axes[0]
    _base(ax, {"A": dict(fill=0.75), "C": dict(fill=0.25)})
    _agent(ax, SHELF["A"][0], r"$a_1$", dx=-30, dy=0)
    _agent(ax, LEFT[0], r"$a_2$", dx=13, dy=10)
    _agent(ax, CROSS[0], r"$a_3$", dx=13, dy=10)
    ax.text(-0.75, -0.5, "waiting", ha="left", va="center", fontsize=10, color=C["agent"])
    _note(ax, "A", "picks stood\nstill 5 steps", C["agent"], below=False)
    _note(ax, "C", "picks stood\nstill 1 step", C["text"])
    ax.set_title("(a) demand storage: every tea pick\ntakes shelf A, and agents wait their turn",
                 fontsize=11, pad=6)
    # (b) congestion-aware storage: the next line takes C, the new tea goes to N.
    ax = axes[1]
    _base(ax, {"A": dict(fill=0.75), "C": dict(fill=0.25),
               "N": dict(fill=0.0, new=0.5, reached=True, label=False)})
    _walk(ax, WALK["A"], alpha=0.3, ls=(0, (3, 2)), lw=2.0)
    _note(ax, "A", "demand storage:\nA, 4 edges", C["agent"], below=False, alpha=0.55)
    _walk(ax, WALK["C"])
    _note(ax, "C", "next tea line:\nC, 6 edges", C["agent"])
    _putaway(ax, "N", 0.35)
    (xn, yn), _ = SHELF["N"]
    ax.text(xn, yn + BOX / 2 + 0.1, "new tea at the\nnext update", ha="center", va="bottom",
            fontsize=10, color=C["store_e"])
    ax.set_title("(b) congestion-aware storage: the next line\ntakes C, new tea goes to the quiet aisle",
                 fontsize=11, pad=6)
    _legend(fig, extra=[Line2D([], [], marker="o", ls="", mfc=C["agent"], mec="white", ms=10,
                               label="agent")])
    fig.tight_layout(rect=[0, 0.1, 1, 1])
    fig.savefig(f"{OUT}/shelf_loop.png"); plt.close(fig)


if __name__ == "__main__":
    arrival_tea()
    shelf_loop()
