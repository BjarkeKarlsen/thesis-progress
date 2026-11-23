"""
The pickup rule on one order line (fig:pickuprule), in the look of the pygame viewer ([A104],
base.py PG). A line asks for 4 tea at workstation W1. Shelf A is 3 moves from W1 and has 1 tea
free, shelf C is 6 moves away and has 5. The line takes 1 from A and the other 3 from C, so it
gives two picks, served here by two agents, a_1 and a_2. This is the pickup rule of the code
(environment/multi_agent_env.py, holders sorted by distance to the workstation, each giving one
task for min(units still missing, units it holds free)).
"""
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

from base import OUT, PG, rank_colour, shelf_slot, aisle_node, work_mark, role_handles

AISLE_X = [0.0, 1.2, 2.4, 3.6, 4.8]
AISLE_Y = 0.0
WORK = (6.0, 0.0)
SHELF = {"C": (0.0, 1.3), "A": (3.6, 1.3)}  # C: 1 + 5 = 6 moves to W1, A: 1 + 2 = 3 moves
FREE = {"A": 1, "C": 5}
TAKE = {"A": 1, "C": 3}
ROOM = 10
HALF = 0.4
TEA = rank_colour(0, 3)


def trip(ax, shelf, off, label_xy, text):
    """A pick's trip from its shelf to W1, in the to-the-workstation colour, along the aisle."""
    sx, sy = SHELF[shelf]
    xs = [sx + 0.1, sx + 0.1, WORK[0] - 0.25]
    ys = [sy - HALF - 0.05, AISLE_Y - off, AISLE_Y - off]
    ax.plot(xs[:2], ys[:2], color=PG["to_delivery"], lw=1.8, zorder=2)
    ax.annotate("", xy=(xs[2], ys[2]), xytext=(xs[1], ys[1]), zorder=2,
                arrowprops=dict(arrowstyle="-|>,head_length=0.5,head_width=0.25", lw=1.8,
                                color=PG["to_delivery"], shrinkA=0, shrinkB=0))
    ax.text(*label_xy, text, ha="center", va="top", fontsize=10.5, color=PG["text"])


def pickup_rule():
    fig, ax = plt.subplots(figsize=(8.0, 3.6))
    ax.set_xlim(-1.0, 7.0); ax.set_ylim(-0.95, 2.3)
    ax.set_aspect("equal"); ax.axis("off")

    for x0, x1 in zip(AISLE_X, AISLE_X[1:] + [WORK[0]]):
        ax.plot([x0, x1], [AISLE_Y, AISLE_Y], color=PG["edge"], lw=1.6, zorder=1)
    for x, y in SHELF.values():
        ax.plot([x, x], [AISLE_Y, y], color=PG["edge"], lw=1.6, zorder=1)
    for x in AISLE_X:
        aisle_node(ax, (x, AISLE_Y))
    work_mark(ax, WORK, s=420)
    ax.text(WORK[0], WORK[1] + 0.42, "$W_1$\nline for 4 tea", ha="center", va="bottom",
            fontsize=10.5, color=PG["text"])

    for name, (x, y) in SHELF.items():
        shelf_slot(ax, x, y, HALF, bands=[(FREE[name] / ROOM, TEA)])
        ax.text(x, y + HALF + 0.12, f"{name}   {FREE[name]} tea free", ha="center",
                va="bottom", fontsize=10.5, color=PG["text"])

    trip(ax, "A", 0.12, (4.75, -0.34), "pick 1, 1 tea, 3 moves")
    trip(ax, "C", 0.24, (1.8, -0.34), "pick 2, 3 tea, 6 moves")
    for name, lab in (("A", "$a_1$"), ("C", "$a_2$")):
        x, y = SHELF[name]
        ax.scatter(x - 0.62, y, s=120, c=PG["to_delivery"], zorder=5)
        ax.text(x - 0.62, y + 0.28, lab, ha="center", va="bottom", fontsize=12,
                color=PG["text"])

    handles = role_handles(("storage", "delivery", "")) + [
        Rectangle((0, 0), 1, 1, fc=TEA, ec="none", label="tea"),
        Line2D([], [], color=PG["to_delivery"], lw=1.8, label="to the workstation"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=len(handles), frameon=False,
               fontsize=9.5, bbox_to_anchor=(0.5, -0.02), handletextpad=0.4, columnspacing=1.0)
    fig.tight_layout(rect=[0, 0.1, 1, 1])
    fig.savefig(f"{OUT}/pickup_rule.png"); plt.close(fig)


if __name__ == "__main__":
    pickup_rule()
