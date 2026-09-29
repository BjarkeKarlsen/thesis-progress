"""
thesis-guide-images.md Section 2 ("The Warehouse as a Graph"): a 4-vertex
example -- A delivery, B/C storage, D transit -- with one one-way segment
and the shortest-path distance from A to C annotated. Built on mini_graph,
the same generator base.py's full 5x9 grid uses (two cross-aisles + racks),
just scaled down to rows=2, cols=2, so this is a genuine small instance of
the model rather than an unrelated toy graph.
"""
import matplotlib.pyplot as plt
import networkx as nx

from base import OUT, C
from mini import mini_graph, draw_mini

NAMES = {"0_0": "A", "0_1": "B", "1_1": "C", "1_0": "D"}  # display letters


def graph_basics():
    G, pos = mini_graph(rows=2, cols=2, dx=2.6, dy=2.0, one_way=("0_1", "1_1"))
    dist_AC = nx.shortest_path_length(G, "0_0", "1_1")

    fig, ax = plt.subplots(figsize=(9.0, 6.0))
    ax.set_aspect("equal"); ax.axis("off")

    draw_mini(ax, G, pos, storage=["0_1", "1_1"], delivery=["0_0"])

    labels = {"0_0": "$A$\ndelivery", "0_1": "$B$\nstorage",
              "1_1": "$C$\nstorage", "1_0": "$D$\ntransit"}
    for n, lab in labels.items():
        ax.annotate(lab, pos[n], textcoords="offset points",
                   xytext=(0, -40 if n in ("1_1", "1_0") else 34),
                   ha="center", fontsize=12, color=C["text"])

    ax.annotate("one-way: $(B,C)\\in E$, $(C,B)\\notin E$", (pos["0_1"][0] + 0.55, pos["0_1"][1] - 1.0),
               ha="left", va="center", fontsize=10.5, color=C["accent"])
    ax.annotate(f"$d_G(A,C) = {dist_AC}$  (via $A\\to B\\to C$)",
               (sum(p[0] for p in pos.values()) / 4, min(p[1] for p in pos.values()) - 0.9),
               ha="center", fontsize=11.5, color=C["text"])
    ax.set_xlim(min(p[0] for p in pos.values()) - 1.0, pos["0_1"][0] + 4.2)
    ax.set_ylim(min(p[1] for p in pos.values()) - 1.6, max(p[1] for p in pos.values()) + 1.2)

    ax.set_title("The warehouse as a directed graph (a 2x2 corner of the full grid)", fontsize=13)
    fig.tight_layout()
    fig.savefig(f"{OUT}/graph_basics.png"); plt.close(fig)


if __name__ == "__main__":
    graph_basics()
