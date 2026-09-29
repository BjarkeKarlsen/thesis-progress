"""
thesis-guide-images.md Section 1 ("Big Picture: Two Coupled Layers"): the
tea/aisle intuition example -- no feedback (tea stuck far up the busy Right
aisle) vs feedback (tea moved to the Left aisle, traffic balances out).
Deliberately not the formal graph notation; this is the very first,
plain-language figure in the guide.

A second item (coffee, fixed on the Right aisle in both panels) is drawn so
every traffic segment has an actual destination -- with only tea, "traffic
balances across both aisles" has nothing to justify traffic on the aisle
tea isn't on. Each aisle's traffic stops exactly at its farthest item;
nothing is drawn past the last item on a route.
"""
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from base import OUT, C

LEFT = [(-1.0, 0.0), (-1.0, 1.2), (-1.0, 2.4)]
RIGHT = [(1.0, 0.0), (1.0, 1.2), (1.0, 2.4)]
DELIVERY = (0.0, -1.0)
COFFEE = RIGHT[1]  # fixed in both panels


def _draw_item(ax, pos, label, fc, ec, dx=16):
    ax.scatter(*pos, s=420, marker="D", c=fc, edgecolors=ec, zorder=4)
    ax.annotate(label, pos, textcoords="offset points", xytext=(dx, 0),
               ha="left" if dx > 0 else "right", fontsize=10.5, color=ec)


def _panel(ax, tea_node):
    ax.set_xlim(-2.2, 2.2); ax.set_ylim(-1.8, 3.7)
    ax.set_aspect("equal"); ax.axis("off")

    for aisle in (LEFT, RIGHT):
        for p0, p1 in zip(aisle, aisle[1:]):
            ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=C["edge"], lw=1.6, zorder=1)
        ax.plot([DELIVERY[0], aisle[0][0]], [DELIVERY[1], aisle[0][1]], color=C["edge"], lw=1.6, zorder=1)

    # Each aisle's traffic runs delivery -> its farthest item on that
    # aisle, and no further -- so a route always ends at something, never
    # at an empty node.
    for aisle in (LEFT, RIGHT):
        items_here = [p for p in (tea_node, COFFEE) if p in aisle]
        if not items_here:
            continue
        last_idx = max(aisle.index(p) for p in items_here)
        path = [DELIVERY] + aisle[:last_idx + 1]
        for p0, p1 in zip(path[:-1], path[1:]):
            ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=C["agent"], lw=2.8,
                   alpha=0.75, solid_capstyle="round", zorder=2)
        ax.annotate("", xy=path[-1], xytext=path[-2],
                   arrowprops=dict(arrowstyle="-|>", lw=2.8, color=C["agent"], alpha=0.9))

    for aisle in (LEFT, RIGHT):
        for p in aisle:
            if p not in (tea_node, COFFEE):
                ax.scatter(*p, s=280, c="white", edgecolors=C["node"], zorder=3)
    ax.scatter(*DELIVERY, s=380, marker="s", c=C["del_f"], edgecolors=C["del_e"], zorder=3)
    ax.annotate("delivery", DELIVERY, textcoords="offset points", xytext=(0, -18),
               ha="center", fontsize=10.5, color=C["del_e"])
    ax.text(-1.0, 2.65, "Left aisle", ha="center", fontsize=11, color=C["text"])
    ax.text(1.0, 2.65, "Right aisle", ha="center", fontsize=11, color=C["text"])

    _draw_item(ax, tea_node, "tea", C["store_f"], C["store_e"],
              dx=16 if tea_node[0] >= 0 else -16)
    _draw_item(ax, COFFEE, "coffee", C["ep_f"], C["ep_e"], dx=-16)


def two_layer_feedback():
    fig, axes = plt.subplots(1, 2, figsize=(9.5, 6.0))
    _panel(axes[0], tea_node=RIGHT[2])
    axes[0].set_title("(a) fixed storage: tea stays put,\ntraffic stays concentrated",
                      fontsize=11, pad=12)
    _panel(axes[1], tea_node=LEFT[0])
    axes[1].set_title("(b) after one update: tea relocated,\ntraffic balances across both aisles",
                      fontsize=11, pad=12)
    handles = [
        Line2D([], [], color=C["agent"], lw=3.0, alpha=0.8, label="agent traffic"),
        Line2D([], [], marker="D", ls="", mfc=C["store_f"], mec=C["store_e"], ms=10, label="tea storage"),
        Line2D([], [], marker="D", ls="", mfc=C["ep_f"], mec=C["ep_e"], ms=10, label="coffee storage"),
        Line2D([], [], marker="s", ls="", mfc=C["del_f"], mec=C["del_e"], ms=10, label="delivery"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=4, frameon=False,
              fontsize=10, bbox_to_anchor=(0.5, 0.0))
    fig.tight_layout(rect=[0, 0.06, 1, 0.90])
    fig.savefig(f"{OUT}/two_layer_feedback.png"); plt.close(fig)


if __name__ == "__main__":
    two_layer_feedback()
