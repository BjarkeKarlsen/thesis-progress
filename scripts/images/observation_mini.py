"""
Simple companion to observation.py (sec:pf:observations, eq:localsubgraph,
eq:potential, eq:commgraph, eq:congestion, Figure fig:observation): all
three bounds -- observation depth d, congestion radius r_cng, and
communication radius r_com -- on an 8-vertex graph, with only three agents
so "one is invisible" is legible at a glance.
"""
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mp
import networkx as nx

from base import OUT, C
from mini import mini_graph, draw_mini, put_agent

EGO, DEPTH, TARGET = "1_1", 1, "2_5"
NEAR, FAR = "1_3", "1_5"  # near: outside obs window, inside comm range; far: outside both
R_CNG, R_COM = 2.1, 2.3


def observation_mini():
    G, pos = mini_graph(rows=3, cols=6, dx=1.0, dy=1.0)
    window = set(nx.single_source_shortest_path_length(G, EGO, cutoff=DEPTH))
    sub = G.subgraph(window)

    fig, ax = plt.subplots(figsize=(8.0, 4.6))
    draw_mini(ax, G, pos, dim=True)
    nx.draw_networkx_edges(sub, pos, ax=ax, edge_color=C["accent"], width=3.0, arrows=False)
    nx.draw_networkx_nodes(G, pos, nodelist=list(window), node_size=520, node_color="none",
                           edgecolors=C["accent"], linewidths=3.0, ax=ax)
    for n in window:  # eta_i(v,t) = d_G(v, target)
        ax.annotate(str(nx.shortest_path_length(G, n, TARGET)), pos[n],
                    textcoords="offset points", xytext=(14, 11), ha="left",
                    fontsize=12, color=C["accent"], weight="bold")

    ax.add_patch(mp.Circle(pos[EGO], R_COM, fill=False, ls="--", lw=1.6,
                           edgecolor=C["comm"], zorder=1))
    ax.add_patch(mp.Circle(pos[EGO], R_CNG, fill=True, fc=C["agent"], alpha=0.08,
                           ec=C["agent"], ls=":", lw=1.6, zorder=1))

    def _dist(n): return math.hypot(pos[n][0] - pos[EGO][0], pos[n][1] - pos[EGO][1])
    nodes_in_cng = [n for n in G if _dist(n) <= R_CNG]
    agents_in_cng = [a for a in (NEAR, FAR) if _dist(a) <= R_CNG]
    delta = len(agents_in_cng) / max(1, len(nodes_in_cng) - 1)
    ax.text(pos[EGO][0], pos[EGO][1] - R_CNG - 0.35,
           f"$\\delta_i(t) = {len(agents_in_cng)}/{len(nodes_in_cng) - 1} = {delta:.2f}$",
           ha="center", va="top", fontsize=10.5, color=C["agent"])

    put_agent(ax, pos, EGO, r"$a_i$")
    put_agent(ax, pos, NEAR, r"$a_j$" + "\n(message only)", color=C["comm"], dy=-30)
    ax.scatter(*pos[FAR], s=290, c=C["agent"], alpha=0.3, zorder=5,
               edgecolors="white", linewidths=1.3)
    ax.annotate(r"$a_k$ (invisible)", pos[FAR], textcoords="offset points",
                xytext=(0, 17), ha="center", color=C["agent"], alpha=0.5, fontsize=12)

    ax.set_aspect("equal")
    ax.set_xlim(pos[EGO][0] - R_COM - 0.5, pos[FAR][0] + 0.8)
    ax.set_ylim(pos[EGO][1] - R_COM - 0.9, pos[EGO][1] + R_COM + 0.8)
    ax.set_axis_off()
    fig.savefig(f"{OUT}/observation_mini.png"); plt.close(fig)


if __name__ == "__main__":
    observation_mini()
