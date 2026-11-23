"""
One storage update on the stock of tab:storagematrix ([A87], fig:storageupdate), drawn in the
look of the pygame viewer ([A104], base.py PG): small white aisle positions, shelves as square
slots filled from the bottom with one band per SKU (most popular lowest, the viewer's rank
colours), the dock as the purple triangle, and the put-aways in the put-away colour along the
aisle. A slot a put-away reached gets a purple rim.

Three pallets of 3 units of tea arrive at the dock. A pallet goes whole onto one shelf (the
pallet rule of the code, storage/arrival.py `_put_away`). Shelf A is full, B and C each have
room for one pallet, so pallets 1 and 2 go to B and C, and pallet 3 fits nowhere and is left
unplaced. Tea and mugs take one unit of room per unit and coffee two, as in the example.
"""
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

from base import OUT, PG, rank_colour, shelf_slot, aisle_node, dock_mark, role_handles

AISLE_Y = 0.0
AISLE_X = [0.0, 1.2, 2.4, 3.6, 4.8]
DOCK = (-1.2, 0.0)  # a leaf at the left end of the aisle
SHELF = {"A": (1.2, 1.3), "B": (2.4, 1.3), "C": (3.6, 1.3)}
ROOM = {"A": 20, "B": 15, "C": 10}
SIZE = {"tea": 1, "coffee": 2, "mugs": 1}
RANK = ["tea", "coffee", "mugs"]  # most popular first
STOCK = {"A": {"tea": 12, "coffee": 4}, "B": {"coffee": 3, "mugs": 6},
         "C": {"tea": 5, "mugs": 2}}  # tab:storagematrix
NEW = {"B": 3, "C": 3}  # tea on its way, one pallet each
HALF = 0.4  # half the side of a slot


def colour(sku):
    return rank_colour(RANK.index(sku), len(RANK))


def storage_update():
    fig, ax = plt.subplots(figsize=(8.0, 3.8))
    ax.set_xlim(-2.3, 5.3); ax.set_ylim(-0.95, 2.3)
    ax.set_aspect("equal"); ax.axis("off")

    for x0, x1 in zip(AISLE_X, AISLE_X[1:]):
        ax.plot([x0, x1], [AISLE_Y, AISLE_Y], color=PG["edge"], lw=1.6, zorder=1)
    for v in SHELF.values():
        ax.plot([v[0], v[0]], [AISLE_Y, v[1]], color=PG["edge"], lw=1.6, zorder=1)
    ax.plot([DOCK[0], AISLE_X[0]], [AISLE_Y, AISLE_Y], color=PG["edge"], lw=1.6, zorder=1)
    for x in AISLE_X:
        aisle_node(ax, (x, AISLE_Y))
    dock_mark(ax, DOCK)
    ax.annotate("dock", DOCK, textcoords="offset points", xytext=(-16, 0), ha="right",
                va="center", fontsize=10.5, color=PG["text"])

    for name, (x, y) in SHELF.items():
        room = ROOM[name]
        held = sorted(STOCK[name].items(), key=lambda kv: RANK.index(kv[0]))
        bands = [(SIZE[k] * n / room, colour(k)) for k, n in held]
        taken = sum(SIZE[k] * n for k, n in held)
        shelf_slot(ax, x, y, HALF, bands=bands, new=NEW.get(name, 0) / room,
                   reached=name in NEW)
        ax.text(x, y + HALF + 0.12, f"{name}   {taken}/{room}", ha="center", va="bottom",
                fontsize=10, color=PG["text"])

    # The two pallets that fit go whole to B and C. Each put-away follows the aisle from the
    # dock and turns up the spur to its shelf, drawn just below and beside the edges.
    for name, off in (("B", -0.09), ("C", -0.18)):
        sx, sy = SHELF[name]
        xs = [DOCK[0] + 0.15, sx + 0.09, sx + 0.09]
        ys = [AISLE_Y + off, AISLE_Y + off, sy - HALF - 0.04]
        ax.plot(xs[:2], ys[:2], color=PG["putaway"], lw=1.6, ls=(0, (3, 2)), zorder=2)
        ax.annotate("", xy=(xs[2], ys[2]), xytext=(xs[1], ys[1]), zorder=2,
                    arrowprops=dict(arrowstyle="-|>,head_length=0.5,head_width=0.25", lw=1.6,
                                    color=PG["putaway"], ls=(0, (3, 2)), shrinkA=0, shrinkB=0))
    ax.text(DOCK[0], 0.6, "3 pallets,\n3 tea each", ha="center", va="bottom", fontsize=10,
            color=PG["text"])
    ax.text(DOCK[0], -0.4, "pallet 3:\nno room", ha="center", va="top", fontsize=10,
            color=PG["text"])

    handles = role_handles(("storage", "receiving", "")) + [
        Rectangle((0, 0), 1, 1, fc=colour(k), ec="none", label=k) for k in RANK
    ] + [
        Rectangle((0, 0), 1, 1, fc="white", ec=PG["putaway"], lw=1.4, hatch="////",
                  label="new tea"),
        Line2D([], [], color=PG["putaway"], lw=1.6, ls=(0, (3, 2)), label="put-away"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=len(handles), frameon=False,
               fontsize=9.5, bbox_to_anchor=(0.5, -0.02), handletextpad=0.4, columnspacing=1.0)
    fig.tight_layout(rect=[0, 0.08, 1, 1])
    fig.savefig(f"{OUT}/storage_update.png"); plt.close(fig)


if __name__ == "__main__":
    storage_update()
