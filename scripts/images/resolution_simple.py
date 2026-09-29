"""
The conflict-resolution operator (sec:method:resolution): a fixed
priority order sigma, agents processed one at a time, each accepted
unless it would violate eq:vertexconflict/eq:swapconflict against an
already-finalised successor, in which case it is overridden to wait.

No existing figure shows this procedure -- conflicts.py only shows the
two forbidden joint transitions it exists to rule out, not the
mechanism that rules them out.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mp

from base import OUT, C

P = {"u": (0, 0), "v": (1.3, 0), "w": (2.6, 0)}


def _base_panel(ax, title):
    ax.set_xlim(-0.6, 3.2); ax.set_ylim(-1.3, 1.1)
    ax.set_aspect("equal"); ax.axis("off")
    ax.text(1.3, 0.95, title, ha="center", fontsize=12)
    for a, b in (("u", "v"), ("v", "w")):
        ax.plot([P[a][0], P[b][0]], [0, 0], color=C["edge"], lw=2.0, zorder=1)
    for n in P:
        ax.add_patch(mp.Circle(P[n], 0.16, fc="white", ec=C["node"], lw=1.8, zorder=3))
        ax.text(P[n][0], P[n][1] - 0.35, n, ha="center", fontsize=11)


def _arrow(ax, a, b, color, style="-|>", alpha=1.0):
    ax.annotate("", xy=(P[b][0], P[b][1] + 0.22), xytext=(P[a][0], P[a][1] + 0.22),
                arrowprops=dict(arrowstyle=style, lw=2.4, color=color, alpha=alpha),
                zorder=2)


def resolution_simple():
    fig, axes = plt.subplots(1, 3, figsize=(13, 3.6))

    # (a) proposed joint action: both a1, a2 propose moving onto v
    ax = axes[0]
    _base_panel(ax, r"proposed: $\sigma=(a_1,a_2)$")
    _arrow(ax, "u", "v", C["accent"], alpha=0.55)
    _arrow(ax, "w", "v", C["accent"], alpha=0.55)
    ax.text(P["u"][0], 0.55, "$a_1$", ha="center", fontsize=12, color=C["agent"])
    ax.text(P["w"][0], 0.55, "$a_2$", ha="center", fontsize=12, color=C["agent"])
    ax.scatter(*P["u"], s=260, c=C["agent"], zorder=4, edgecolors="white", linewidths=1.2)
    ax.scatter(*P["w"], s=260, c=C["agent"], zorder=4, edgecolors="white", linewidths=1.2)

    # (b) process a_{sigma(1)} = a1: no finalised successor yet to conflict with -> accepted
    ax = axes[1]
    _base_panel(ax, r"process $a_{\sigma(1)}=a_1$: accepted")
    _arrow(ax, "u", "v", C["del_e"])
    ax.text(0.65, 0.42, r"$\checkmark$", ha="center", fontsize=15, color=C["del_e"])
    _arrow(ax, "w", "v", C["accent"], alpha=0.4)
    ax.scatter(*P["v"], s=260, c=C["agent"], zorder=4, edgecolors="white", linewidths=1.2)
    ax.text(P["v"][0], 0.55, "$a_1$", ha="center", fontsize=12, color=C["agent"])
    ax.text(P["w"][0], 0.55, "$a_2$", ha="center", fontsize=12, color=C["agent"])
    ax.scatter(*P["w"], s=260, c=C["agent"], zorder=4, edgecolors="white", linewidths=1.2)

    # (c) process a_{sigma(2)} = a2: v is now occupied by a1's finalised successor -> overridden
    ax = axes[2]
    _base_panel(ax, r"process $a_{\sigma(2)}=a_2$: overridden $\to$ wait")
    ax.scatter(*P["v"], s=260, c=C["agent"], zorder=4, edgecolors="white", linewidths=1.2)
    ax.text(P["v"][0], 0.55, "$a_1$", ha="center", fontsize=12, color=C["agent"])
    _arrow(ax, "w", "v", C["del_e"], alpha=0.6)
    ax.plot([1.95, 2.25], [0.10, 0.34], color=C["agent"], lw=2.6, zorder=5)
    ax.plot([1.95, 2.25], [0.34, 0.10], color=C["agent"], lw=2.6, zorder=5)
    ax.scatter(*P["w"], s=260, c=C["agent"], zorder=4, edgecolors="white", linewidths=1.2)
    ax.text(P["w"][0], 0.55, r"$a_2$: wait", ha="center", fontsize=12, color=C["agent"])
    ax.text(P["w"][0], -0.75, "override flag set", ha="center", fontsize=10, color=C["text"])

    fig.tight_layout()
    fig.savefig(f"{OUT}/resolution_simple.png"); plt.close(fig)


if __name__ == "__main__":
    resolution_simple()
