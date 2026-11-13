"""
fig:controllers-example, merged with the old fig:congestion ([A93] figure review, 2026-11-13).
The same small graph under each architecture's window (controllers_example.py), with the three
agents of congestion_mini.py and their crowding feature delta_i(t). A panel writes delta only next
to the agents its controller decides for and fades the others, so one figure shows both what a
controller sees and whose readings it gets. delta is the same field-of-view count for every agent
(eq:congestion), 1 hop here.
"""
import matplotlib.pyplot as plt
import networkx as nx

from base import OUT, C
from mini import mini_graph
from controllers_example import _panel, XLIM, YLIM, EGO
from congestion_mini import delta

AGENTS = {"0_0": r"$a_1$", "1_2": r"$a_2$", EGO: r"$a_3$"}
ZONE_1 = lambda n: int(n.split("_")[1]) < 2
READ = {
    "centralised": set(AGENTS),
    "section": {a for a in AGENTS if ZONE_1(a)},
    "decentralised": {EGO},
}


def _agents(ax, G, pos, read):
    deltas = {a: delta(G, a, AGENTS) for a in AGENTS}
    for n, lab in AGENTS.items():
        on = n in read
        ax.scatter(*pos[n], s=230, c=C["agent"], zorder=6, alpha=1.0 if on else 0.3,
                   edgecolors="white", linewidths=1.2)
        ax.annotate(lab, pos[n], textcoords="offset points", xytext=(0, 15), ha="center",
                    fontsize=11, color=C["agent"], alpha=1.0 if on else 0.35, zorder=7)
        if on:
            ax.annotate(rf"$\delta={deltas[n]:.2f}$", pos[n], textcoords="offset points",
                        xytext=(14, -18), ha="left", fontsize=10, color=C["accent"], zorder=7,
                        bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.85))


def controllers_window():
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.4))
    for ax, mode in zip(axes, ("centralised", "section", "decentralised")):
        G, pos = mini_graph(rows=3, cols=4, dx=1.1, dy=1.0)
        _panel(ax, G, pos, mode, agent=False)
        _agents(ax, G, pos, READ[mode])
        ax.set_xlim(*XLIM); ax.set_ylim(*YLIM)
        ax.set_aspect("equal"); ax.set_axis_off()
    axes[0].set_title("(a) centralised: whole graph, every reading", fontsize=11)
    axes[1].set_title("(b) section-based: its zone, its agents' readings", fontsize=11)
    axes[2].set_title(r"(c) decentralised: $a_3$'s window, its own reading", fontsize=11)
    fig.tight_layout()
    fig.savefig(f"{OUT}/controllers_window.png"); plt.close(fig)


if __name__ == "__main__":
    controllers_window()
