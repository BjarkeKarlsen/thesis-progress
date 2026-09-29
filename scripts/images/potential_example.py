"""
Worked example for the target-distance potential (eta_i(v,t) = d_G(v, q_i(t))):
a tiny graph where the agent at A can move to B or C, each vertex annotated
with its own shortest-path distance to the target T. Numbers are computed by
networkx, not hand-typed, so they always match the drawn graph.
"""
import matplotlib.pyplot as plt
import networkx as nx

from base import OUT, C

def _graph():
    G = nx.DiGraph()
    chainB = ["A", "B", "b1", "b2", "b3", "T"]                    # d_G(B,T) = 4
    chainC = ["A", "C", "c1", "c2", "c3", "c4", "c5", "c6", "T"]  # d_G(C,T) = 7
    for chain in (chainB, chainC):
        for u, v in zip(chain, chain[1:]):
            G.add_edge(u, v)
    return G


POS = {
    "A": (0.0, 0.0),
    "B": (1.3, 0.9), "b1": (2.6, 0.9), "b2": (3.9, 0.9), "b3": (5.2, 0.9),
    "C": (1.3, -0.9), "c1": (2.6, -0.9), "c2": (3.9, -0.9), "c3": (5.2, -0.9),
    "c4": (6.5, -0.9), "c5": (7.8, -0.9), "c6": (9.1, -0.9),
    "T": (10.4, 0.0),
}


def potential_example():
    G = _graph()
    eta_B = nx.shortest_path_length(G, "B", "T")
    eta_C = nx.shortest_path_length(G, "C", "T")

    fig, ax = plt.subplots(figsize=(12.8, 5.4))
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_ylim(-2.6, 2.5)

    rest = [e for e in G.edges() if e not in (("A", "B"), ("A", "C"))]
    nx.draw_networkx_edges(G, POS, edgelist=rest, ax=ax, edge_color=C["edge"], width=1.6,
                           arrows=True, arrowsize=14, node_size=420)
    nx.draw_networkx_edges(G, POS, edgelist=[("A", "B")], ax=ax, edge_color=C["store_e"],
                           width=3.2, arrows=True, arrowsize=18, node_size=420)
    nx.draw_networkx_edges(G, POS, edgelist=[("A", "C")], ax=ax, edge_color=C["edge"],
                           width=1.6, alpha=0.6, arrows=True, arrowsize=14, node_size=420)
    small = [n for n in G if n not in ("A", "B", "C", "T")]
    nx.draw_networkx_nodes(G, POS, nodelist=small, node_color="white",
                           edgecolors=C["node"], node_size=260, ax=ax)
    nx.draw_networkx_nodes(G, POS, nodelist=["A"], node_color=C["agent"],
                           edgecolors="white", linewidths=1.5, node_size=520, ax=ax)
    nx.draw_networkx_nodes(G, POS, nodelist=["B", "C"], node_color=C["store_f"],
                           edgecolors=C["store_e"], node_size=460, ax=ax)
    nx.draw_networkx_nodes(G, POS, nodelist=["T"], node_color=C["del_f"],
                           edgecolors=C["del_e"], node_shape="s", node_size=560, ax=ax)

    for n, lab, dy in (("A", "$A$  (agent)", 22), ("B", "$B$", 22), ("C", "$C$", 18),
                        ("T", "$T = q_i(t)$  (target)", 22)):
        ax.annotate(lab, POS[n], textcoords="offset points", xytext=(0, dy),
                   ha="center", fontsize=12, color=C["text"])

    ax.annotate(f"$\\eta_i(B,t) = {eta_B}$", POS["B"], textcoords="offset points",
               xytext=(5, -24), ha="left", fontsize=12, color=C["store_e"])
    ax.annotate(f"$\\eta_i(C,t) = {eta_C}$", POS["C"], textcoords="offset points",
               xytext=(5, -24), ha="left", fontsize=12, color=C["node"])


    fig.tight_layout()
    fig.savefig(f"{OUT}/potential_example.png"); plt.close(fig)

if __name__ == "__main__":
    potential_example()
