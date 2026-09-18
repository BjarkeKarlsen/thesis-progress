# visualize_notation_graph_grid.py
"""
Grid-style visualization of SLAP–MAPD notation.

Nodes are arranged in rows/columns to avoid overlap and to mimic a
warehouse-grid style layout (warehouse, demand/storage, agents, policies).
"""

from __future__ import annotations

import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, List


NOTATION_RELATIONS: Dict[str, List[str]] = {
    # Warehouse graph and locations
    "G_W": ["L", "E_W"],
    "L": ["L_item", "L_delivery", "L_other"],
    "E_W": ["L"],
    "c(e)": ["E_W"],

    # Agents and positions
    "A": ["l_i^t"],
    "l_i^t": ["L"],
    "a_i^t": ["A", "L", "E_W"],
    "τ_i": ["A", "L", "a_i^t"],

    # Orders and demand
    "Z": ["z"],
    "z": ["u_k", "q_k"],
    "u_k": [],
    "q_k": ["u_k"],

    # Storage assignment
    "s_t": ["L_item", "u_k"],
    "S": ["s_t"],

    # Zones / sections
    "Y": ["L"],

    # Interaction graph and observations
    "G_A^t": ["A", "E_A^t"],
    "E_A^t": ["A"],
    "o_i^t": ["L", "Z", "G_W", "G_A^t"],
    "LocProj": ["G_W", "L"],
    "x_i^t": ["o_i^t"],
    "h_i^t": ["x_i^t", "G_A^t"],

    # Policies and classes
    "π": ["o_i^t", "a_i^t"],
    "Π_cent": ["π", "G_W"],
    "Π_sec": ["π", "Y", "G_W"],
    "Π_dec": ["π", "G_A^t", "LocProj"],

    # Congestion and costs
    "D_t(e)": ["E_W", "A"],
    "C_trav": ["G_W", "A", "Z"],
    "C_cong": ["D_t(e)"],
    "C_rob": ["G_W", "A", "Z"],

    # Time and discount
    "T": [],
    "γ": ["T"],
}


def build_notation_graph(relations: Dict[str, List[str]]) -> nx.DiGraph:
    g = nx.DiGraph()
    for parent, children in relations.items():
        g.add_node(parent)
        for child in children:
            g.add_node(child)
            g.add_edge(parent, child)
    return g


def get_grid_positions(nodes: List[str]) -> Dict[str, tuple]:
    """
    Assign fixed (x, y) positions to nodes in conceptual rows.
    You can adjust coordinates to match warehouse_grid.py aesthetics.
    """

    # Define conceptual rows: top = warehouse; then demand/storage;
    # then agents/interaction; bottom = policies/costs/time.
    row_y = {
        "warehouse": 3.0,
        "demand_storage": 2.0,
        "agents_interaction": 1.0,
        "policies_costs_time": 0.0,
    }

    # Manual ordering within each row for clearer layout.
    rows: Dict[str, List[str]] = {
        "warehouse": ["G_W", "L", "E_W", "c(e)", "Y"],
        "demand_storage": ["Z", "z", "u_k", "q_k", "L_item", "L_delivery", "L_other", "s_t", "S"],
        "agents_interaction": ["A", "l_i^t", "a_i^t", "τ_i", "G_A^t", "E_A^t", "o_i^t", "LocProj", "x_i^t", "h_i^t"],
        "policies_costs_time": ["π", "Π_cent", "Π_sec", "Π_dec",
                                "D_t(e)", "C_trav", "C_cong", "C_rob",
                                "T", "γ"],
    }

    # Start with empty pos dict; some nodes may not be listed above.
    pos: Dict[str, tuple] = {}

    # Assign positions row by row.
    for row_name, symbols in rows.items():
        y = row_y[row_name]
        # Center symbols around x = 0 by spacing them evenly.
        n = len(symbols)
        if n == 0:
            continue
        x_start = - (n - 1) * 1.2 / 2.0  # 1.2 is horizontal spacing
        for idx, sym in enumerate(symbols):
            if sym in nodes:  # only place if node exists in graph
                x = x_start + idx * 1.2
                pos[sym] = (x, y)

    # For any remaining nodes not in rows, fall back to a small spring layout
    remaining = [n for n in nodes if n not in pos]
    if remaining:
        subgraph = nx.DiGraph()
        subgraph.add_nodes_from(remaining)
        # Simple layout clustered near bottom-right
        sub_pos = nx.spring_layout(subgraph, seed=42)
        for n, (x, y) in sub_pos.items():
            pos[n] = (x + 6.0, y - 1.0)

    return pos


def draw_notation_graph_grid(g: nx.DiGraph) -> None:
    plt.figure(figsize=(14, 8))

    nodes = list(g.nodes())
    pos = get_grid_positions(nodes)

    nx.draw_networkx_nodes(
        g, pos,
        node_size=1600,
        node_color="#fafafa",
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
        edge_color="#777777",
        connectionstyle="arc3,rad=0.1",  # small arcs to reduce visual clutter
    )

    # Add faint horizontal lines to emphasize row structure (like aisles/zones).
    for y in [3.0, 2.0, 1.0, 0.0]:
        plt.axhline(y=y, color="#e0e0e0", linewidth=0.5, zorder=0)

    plt.title("Grid-style notation graph for SLAP–MAPD coupling", fontsize=12)
    plt.axis("off")
    plt.tight_layout()
    plt.show()


def print_notation_relations(relations: Dict[str, List[str]]) -> None:
    for parent, children in relations.items():
        if children:
            print(f"{parent} -> {', '.join(children)}")
        else:
            print(f"{parent} -> (no direct dependencies)")


if __name__ == "__main__":
    g = build_notation_graph(NOTATION_RELATIONS)
    print("Notation relationships:")
    print_notation_relations(NOTATION_RELATIONS)
    draw_notation_graph_grid(g)