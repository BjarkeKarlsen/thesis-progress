"""
fig:crowding ([A106]). The crowding feature delta_i(t) of eq:congestion on the small graph of
fig:controllers-example, in its own figure in "How crowded the neighbourhood is", so the
controllers figure no longer shows a feature the reader meets only later. The three agents of
congestion_mini.py, each with its reading. Agent a_3's field of view (1 hop here) is drawn, since
the caption explains its reading: one other agent among its four neighbours, so 0.25.
"""
import matplotlib.pyplot as plt
import networkx as nx

from base import OUT, C
from mini import mini_graph
from congestion_mini import AGENTS, EGO, delta, field_of_view


def crowding():
    fig, ax = plt.subplots(figsize=(5.6, 3.4))
    G, pos = mini_graph(rows=3, cols=4, dx=1.1, dy=1.0)
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color=C["edge"], width=1.6, arrows=False)
    fov = field_of_view(G, EGO)
    nx.draw_networkx_edges(G, pos, edgelist=list(G.subgraph(fov).edges()), ax=ax,
                           edge_color=C["accent"], width=2.6, arrows=False)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=420, node_color="white",
                           edgecolors=C["node"], linewidths=1.2)
    nx.draw_networkx_nodes(G, pos, nodelist=list(fov), ax=ax, node_size=420,
                           node_color="white", edgecolors=C["accent"], linewidths=2.2)
    for n, lab in AGENTS.items():
        ax.scatter(*pos[n], s=200, c=C["agent"], zorder=5, edgecolors="white", linewidths=1.2)
        ax.annotate(lab, pos[n], textcoords="offset points", xytext=(-15, 12), ha="center",
                    fontsize=11, color=C["agent"])
        ax.annotate(rf"$\delta={delta(G, n, AGENTS):.2f}$", pos[n], textcoords="offset points",
                    xytext=(13, -17), ha="left", fontsize=10, color=C["text"],
                    bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none", alpha=0.85))
    ax.set_aspect("equal"); ax.set_axis_off()
    ax.margins(0.12)
    fig.tight_layout()
    fig.savefig(f"{OUT}/crowding.png"); plt.close(fig)


if __name__ == "__main__":
    crowding()
