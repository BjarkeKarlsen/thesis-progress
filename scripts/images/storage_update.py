"""
One storage update on the stock of tab:storagematrix ([A87], fig:storageupdate), drawn in the
style of arrival_storage.py and stock_moments.py: white aisle vertices, shelves as slot boxes
hanging off the aisle, the dock as the V_dock triangle, and the put-away of new stock as
the dashed blue arrow. A slot box is the shelf's room, filled from the bottom with the room
taken, and outlined in purple when a put-away reached it, as in stock_moments.py.

Three refills of 3 units of tea arrive at the dock. A refill goes whole onto one shelf (the
refill rule of the code, storage/arrival.py `_put_away`). Shelf A is full, B and C each have
room for one refill, so refills 1 and 2 go to B and C, and refill 3 fits nowhere and is left
unplaced. Tea takes one unit of room per unit, so the numbers are those of the example.
"""
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

from base import OUT, C

PUTAWAY = "#2f6fae"
AISLE_Y = 0.0
AISLE_X = [0.0, 1.2, 2.4, 3.6, 4.8]
DOCK = (-1.2, 0.0)  # a leaf at the left end of the aisle
SHELF = {"A": (1.2, 1.3), "B": (2.4, 1.3), "C": (3.6, 1.3)}
ROOM = {"A": (20, 20, 0), "B": (15, 12, 3), "C": (10, 7, 3)}  # room, taken before, new on its way
BOX = 0.8  # side of a slot box, in position units


def storage_update():
    fig, ax = plt.subplots(figsize=(8.0, 4.6))
    ax.set_xlim(-1.9, 5.3); ax.set_ylim(-1.25, 2.6)
    ax.set_aspect("equal"); ax.axis("off")

    # The aisle, the shelves hanging off it, and the dock.
    for x0, x1 in zip(AISLE_X, AISLE_X[1:]):
        ax.plot([x0, x1], [AISLE_Y, AISLE_Y], color=C["edge"], lw=1.6, zorder=1)
    for v in SHELF.values():
        ax.plot([v[0], v[0]], [AISLE_Y, v[1]], color=C["edge"], lw=1.6, zorder=1)
    ax.plot([DOCK[0], AISLE_X[0]], [AISLE_Y, AISLE_Y], color=C["edge"], lw=1.6, zorder=1)
    for x in AISLE_X:
        ax.scatter(x, AISLE_Y, s=260, c="white", edgecolors=C["node"], zorder=3)
    ax.scatter(*DOCK, s=420, marker="^", c=C["rcv_f"], edgecolors=C["rcv_e"], zorder=3)
    ax.annotate("dock", DOCK, textcoords="offset points", xytext=(0, -24), ha="center",
                fontsize=10.5, color=C["rcv_e"])

    # Each shelf is a slot box at its vertex, as in stock_moments.py: the box is the shelf's
    # room, filled from the bottom with the room taken, and the new tea on its way striped on
    # top. A slot a put-away reached is outlined in the put-away colour of stock_moments.py.
    for name, (room, taken, new) in ROOM.items():
        x, y = SHELF[name]
        left, bottom = x - BOX / 2, y - BOX / 2
        ax.add_patch(Rectangle((left, bottom), BOX, BOX, fc="white", lw=0, zorder=3))
        ax.add_patch(Rectangle((left, bottom), BOX, BOX * taken / room, fc=C["store_f"], lw=0,
                               zorder=4))
        if new:
            ax.add_patch(Rectangle((left, bottom + BOX * taken / room), BOX, BOX * new / room,
                                   fc="white", ec=C["store_e"], lw=0.6, hatch="////", zorder=4))
        ax.add_patch(Rectangle((left, bottom), BOX, BOX, fc="none",
                               ec=C["comm"] if new else C["node"], lw=1.6 if new else 0.8,
                               zorder=5))
        ax.text(x, bottom + BOX + 0.12, f"shelf {name}\nroom {taken}/{room}", ha="center",
                va="bottom", fontsize=10, color=C["text"])

    # The two refills that fit go whole to B and C, as put-aways from the dock.
    for name, rad in (("B", 0.55), ("C", 0.5)):
        ax.annotate("", xy=(SHELF[name][0], SHELF[name][1] - BOX / 2), xytext=DOCK, zorder=6,
                    arrowprops=dict(arrowstyle="-|>", lw=2.0, color=PUTAWAY, ls=(0, (3, 2)),
                                    shrinkA=12, shrinkB=2, connectionstyle=f"arc3,rad={rad}"))
    ax.text(DOCK[0], 0.85, "3 refills\nof 3 tea", ha="center", va="center", fontsize=10,
            color=C["store_e"])
    ax.text(DOCK[0] - 0.3, -1.0, "refill 3 fits nowhere, left unplaced", ha="left", va="center",
            fontsize=10, color=C["agent"])

    handles = [
        Line2D([], [], color=PUTAWAY, lw=2.0, ls=(0, (3, 2)), label="put-away of a whole refill"),
        Rectangle((0, 0), 1, 1, fc=C["store_f"], ec=C["node"], label="shelf, room taken"),
        Rectangle((0, 0), 1, 1, fc="white", ec=C["store_e"], hatch="////",
                  label="new tea on its way"),
        Rectangle((0, 0), 1, 1, fc="none", ec=C["comm"], lw=1.6, label="shelf a put-away reached"),
        Line2D([], [], marker="^", ls="", mfc=C["rcv_f"], mec=C["rcv_e"], ms=10, label="dock"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=3, frameon=False, fontsize=10,
               bbox_to_anchor=(0.5, -0.02))
    fig.tight_layout(rect=[0, 0.1, 1, 1])
    fig.savefig(f"{OUT}/storage_update.png"); plt.close(fig)


if __name__ == "__main__":
    storage_update()
