"""
fig:controllers-example. The same small graph under each controller's window
(controllers_example.py), with the three agents of congestion_mini.py. A panel fades the agents
its controller does not decide for. The crowding feature delta is no longer drawn here ([A106]),
since it is only met later, in "What a decentralised agent sees". Short panel titles ([A104]).
"""
import matplotlib.pyplot as plt
import networkx as nx

from base import OUT, C
from mini import mini_graph
from controllers_example import _panel, XLIM, YLIM, EGO

AGENTS = {"0_0": r"$a_1$", "1_2": r"$a_2$", EGO: r"$a_3$"}
ZONE_1 = lambda n: int(n.split("_")[1]) < 2
READ = {
    "centralised": set(AGENTS),
    "section": {a for a in AGENTS if ZONE_1(a)},
    "decentralised": {EGO},
}


def _agents(ax, G, pos, read):
    for n, lab in AGENTS.items():
        on = n in read
        ax.scatter(*pos[n], s=230, c=C["agent"], zorder=6, alpha=1.0 if on else 0.3,
                   edgecolors="white", linewidths=1.2)
        ax.annotate(lab, pos[n], textcoords="offset points", xytext=(0, 15), ha="center",
                    fontsize=11, color=C["agent"], alpha=1.0 if on else 0.35, zorder=7)


def controllers_window():
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.4))
    for ax, mode in zip(axes, ("centralised", "section", "decentralised")):
        G, pos = mini_graph(rows=3, cols=4, dx=1.1, dy=1.0)
        _panel(ax, G, pos, mode, agent=False)
        _agents(ax, G, pos, READ[mode])
        ax.set_xlim(*XLIM); ax.set_ylim(*YLIM)
        ax.set_aspect("equal"); ax.set_axis_off()
    axes[0].set_title("(a) Centralised", fontsize=11, color=C["text"])
    axes[1].set_title("(b) Section-based", fontsize=11, color=C["text"])
    axes[2].set_title("(c) Decentralised", fontsize=11, color=C["text"])
    fig.tight_layout()
    fig.savefig(f"{OUT}/controllers_window.png"); plt.close(fig)


if __name__ == "__main__":
    controllers_window()
