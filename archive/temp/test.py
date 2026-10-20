# visualize_notation_graph.py
"""
Visualise core notation for graph-based SLAP–MAPD coupling.

Uses the symbols from the LaTeX notation table:
  G_W, L, L_item, L_delivery, L_other, E_W, c(e), A, l_i^t, Z, z, u_k, q_k,
  s_t, S, Y, G_A^t, E_A^t, o_i^t, LocProj, x_i^t, h_i^t,
  π, Π_cent, Π_sec, Π_dec, a_i^t, τ_i, D_t(e),
  C_trav, C_cong, C_rob, T, γ.
"""

from __future__ import annotations

import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, List


# Each entry: parent symbol -> list of symbols it directly depends on / contains.
NOTATION_RELATIONS: Dict[str, List[str]] = {
    # Warehouse graph and locations
    "G_W": ["L", "E_W"],                   # G_W = (L, E_W)
    "L": ["L_item", "L_delivery", "L_other"],
    "E_W": ["L"],                         # edges between locations
    "c(e)": ["E_W"],                      # cost defined on edges

    # Agents and positions
    "A": ["l_i^t"],                       # agent positions indexed by A
    "l_i^t": ["L"],                       # positions are locations in L
    "a_i^t": ["A", "L", "E_W"],           # primitive action depends on agent, location, edges
    "τ_i": ["A", "L", "a_i^t"],           # trajectory of agent i

    # Orders and demand
    "Z": ["z"],                           # order distribution over orders
    "z": ["u_k", "q_k"],                  # order is item–quantity pairs
    "u_k": [],                            # item identifier (abstract)
    "q_k": ["u_k"],                       # quantity associated with item

    # Storage assignment (SLAP)
    "s_t": ["L_item", "u_k"],             # maps items to storage locations
    "S": ["s_t"],                         # class of admissible storage policies

    # Zones / sections
    "Y": ["L"],                           # partition of L into zones

    # Agent interaction graph and observations
    "G_A^t": ["A", "E_A^t"],              # agent interaction graph
    "E_A^t": ["A"],                       # edges between agents
    "o_i^t": ["L", "Z", "G_W", "G_A^t"],  # local observation from graph, orders, and interactions
    "LocProj": ["G_W", "L"],              # local projection of G_W around node in L
    "x_i^t": ["o_i^t"],                   # local feature vector from observation
    "h_i^t": ["x_i^t", "G_A^t"],          # GNN embedding from features and interaction graph

    # Routing policies and policy classes
    "π": ["o_i^t", "a_i^t"],              # policy maps observations to actions
    "Π_cent": ["π", "G_W"],               # centralised policies over full graph
    "Π_sec": ["π", "Y", "G_W"],           # section-based policies over zones
    "Π_dec": ["π", "G_A^t", "LocProj"],   # decentralised RL policies using local graphs

    # Congestion and cost functionals
    "D_t(e)": ["E_W", "A"],               # congestion statistics on edges from agent flows
    "C_trav": ["G_W", "A", "Z"],          # travel cost functional
    "C_cong": ["D_t(e)"],                 # congestion cost functional
    "C_rob": ["G_W", "A", "Z"],           # robustness cost functional

    # Time horizon and discounting
    "T": [],                              # episode length
    "γ": ["T"],                           # discount factor used over time horizon
}


def build_notation_graph(relations: Dict[str, List[str]]) -> nx.DiGraph:
    """
    Build a directed graph where nodes are symbols and edges represent
    'depends on' or 'contains' relationships.
    """
    g = nx.DiGraph()
    for parent, children in relations.items():
        g.add_node(parent)
        for child in children:
            g.add_node(child)
            g.add_edge(parent, child)
    return g


def draw_notation_graph(g: nx.DiGraph) -> None:
    """
    Draw the graph using a spring layout.
    """
    plt.figure(figsize=(12, 9))
    pos = nx.spring_layout(g, seed=42)

    nx.draw_networkx_nodes(
        g, pos,
        node_size=1400,
        node_color="#f6f6ff",
        edgecolors="#333333",
    )
    nx.draw_networkx_labels(
        g, pos,
        font_size=9,
    )
    nx.draw_networkx_edges(
        g, pos,
        arrowstyle="->",
        arrowsize=15,
        edge_color="#666666",
    )

    plt.title("Notation Graph for SLAP–MAPD Coupling", fontsize=12)
    plt.axis("off")
    plt.tight_layout()
    plt.show()


def print_notation_relations(relations: Dict[str, List[str]]) -> None:
    """
    Print adjacency list for quick inspection / LaTeX cross-checking.
    """
    for parent, children in relations.items():
        if children:
            print(f"{parent} -> {', '.join(children)}")
        else:
            print(f"{parent} -> (no direct dependencies)")


if __name__ == "__main__":
    g = build_notation_graph(NOTATION_RELATIONS)
    print("Notation relationships:")
    print_notation_relations(NOTATION_RELATIONS)
    draw_notation_graph(g)