"""
The arrival model ([A38], [A39]) in the tea/aisle picture of
two_layer_feedback.py: new stock arrives at the delivery vertex, and the
storage rule only decides which shelf it goes to. Fixed storage sends new
tea to its home shelf at the far end of the Right aisle. Adaptive storage
(drawn as the demand rule) sends it to the nearest shelf with room, while
the old tea stays where it is until it runs out. An order takes the nearest
tea, so its walk is 3 edges under fixed storage and 1 under adaptive storage.
Used as fig:storageexample in 2.Introduction.tex, replacing
two_layer_feedback.png there.
"""
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from base import OUT, C

LEFT = [(-1.0, 0.0), (-1.0, 1.2), (-1.0, 2.4)]
RIGHT = [(1.0, 0.0), (1.0, 1.2), (1.0, 2.4)]
DELIVERY = (0.0, -1.0)
HOME = RIGHT[2]   # tea's home shelf, where the old tea sits in both panels
NEAR = LEFT[0]    # the nearest shelf with room
PUTAWAY = "#2f6fae"


def _route(target):
    aisle = LEFT if target in LEFT else RIGHT
    return [DELIVERY] + aisle[:aisle.index(target) + 1]


def _line(ax, path, color, lw, dx=0.0, **kw):
    xs = [p[0] + dx for p in path]
    ax.plot(xs, [p[1] for p in path], color=color, lw=lw, solid_capstyle="round", **kw)
    ax.annotate("", xy=(xs[-1], path[-1][1]), xytext=(xs[-2], path[-2][1]),
                arrowprops=dict(arrowstyle="-|>", lw=lw, color=color,
                                linestyle=kw.get("ls", "-")))


def _panel(ax, new_tea):
    ax.set_xlim(-2.4, 2.4); ax.set_ylim(-1.8, 3.7)
    ax.set_aspect("equal"); ax.axis("off")

    for aisle in (LEFT, RIGHT):
        for p0, p1 in zip(aisle, aisle[1:]):
            ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=C["edge"], lw=1.6, zorder=1)
        ax.plot([DELIVERY[0], aisle[0][0]], [DELIVERY[1], aisle[0][1]], color=C["edge"], lw=1.6, zorder=1)

    # The order's walk to the nearest tea runs along the aisle. The put-away
    # of the new tea is drawn as an arc beside it, so the two never overlap.
    walk = _route(new_tea)
    _line(ax, walk, C["agent"], 2.8, zorder=2, alpha=0.85)
    ax.annotate("", xy=new_tea, xytext=DELIVERY, zorder=2,
                arrowprops=dict(arrowstyle="-|>", lw=2.2, color=PUTAWAY, ls=(0, (3, 2)),
                                shrinkA=14, shrinkB=16,
                                connectionstyle=f"arc3,rad={0.6 if new_tea in RIGHT else -0.35}"))
    edges = len(walk) - 1
    mid = walk[len(walk) // 2]
    ax.annotate(f"order walks\n{edges} edge{'s' if edges > 1 else ''}", mid,
                textcoords="offset points", xytext=(-58 if new_tea in RIGHT else 58, -6),
                ha="center", fontsize=10.5, color=C["agent"])

    for aisle in (LEFT, RIGHT):
        for p in aisle:
            if p not in (HOME, new_tea):
                ax.scatter(*p, s=280, c="white", edgecolors=C["node"], zorder=3)
    ax.scatter(*DELIVERY, s=380, marker="s", c=C["del_f"], edgecolors=C["del_e"], zorder=3)
    ax.annotate("delivery and\nreceiving", DELIVERY, textcoords="offset points", xytext=(0, -30),
                ha="center", fontsize=10.5, color=C["del_e"])
    ax.text(-1.0, 2.75, "Left aisle", ha="center", fontsize=11, color=C["text"])
    ax.text(1.0, 2.75, "Right aisle", ha="center", fontsize=11, color=C["text"])

    if new_tea == HOME:
        ax.scatter(*HOME, s=420, marker="D", c=C["store_f"], edgecolors=C["store_e"], zorder=4)
        ax.annotate("old + new tea", HOME, textcoords="offset points", xytext=(-16, 0),
                    ha="right", va="center", fontsize=10.5, color=C["store_e"])
    else:
        ax.scatter(*HOME, s=420, marker="D", c="white", edgecolors="white", zorder=4)
        ax.scatter(*HOME, s=420, marker="D", c=C["store_f"], edgecolors=C["store_e"],
                   alpha=0.4, zorder=5)
        ax.annotate("old tea,\nruns out", HOME, textcoords="offset points", xytext=(16, 0),
                    ha="left", va="center", fontsize=10.5, color=C["store_e"], alpha=0.6)
        ax.scatter(*new_tea, s=420, marker="D", c=C["store_f"], edgecolors=C["store_e"], zorder=4)
        ax.annotate("new tea", new_tea, textcoords="offset points", xytext=(-16, 0),
                    ha="right", va="center", fontsize=10.5, color=C["store_e"])


def arrival_storage():
    fig, axes = plt.subplots(1, 2, figsize=(9.5, 6.0))
    _panel(axes[0], new_tea=HOME)
    axes[0].set_title("(a) fixed storage: new tea goes\nto its home shelf", fontsize=11, pad=12)
    _panel(axes[1], new_tea=NEAR)
    axes[1].set_title("(b) adaptive storage: new tea goes\nto the nearest shelf with room", fontsize=11, pad=12)
    handles = [
        Line2D([], [], color=PUTAWAY, lw=2.2, ls=(0, (3, 2)), label="put-away of new stock"),
        Line2D([], [], color=C["agent"], lw=3.0, alpha=0.85, label="order's walk to the nearest tea"),
        Line2D([], [], marker="D", ls="", mfc=C["store_f"], mec=C["store_e"], ms=10, label="tea"),
        Line2D([], [], marker="s", ls="", mfc=C["del_f"], mec=C["del_e"], ms=10, label="delivery"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=4, frameon=False,
               fontsize=10, bbox_to_anchor=(0.5, 0.0))
    fig.tight_layout(rect=[0, 0.06, 1, 0.90])
    fig.savefig(f"{OUT}/arrival_storage.png"); plt.close(fig)


if __name__ == "__main__":
    arrival_storage()
