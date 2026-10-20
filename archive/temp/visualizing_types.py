# visualize_types.py
"""
Visualise how the core warehouse/MAPD types are connected.

Usage:
    pip install networkx matplotlib
    python visualize_types.py
"""

from __future__ import annotations

import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, List

# Nodes are class/type names, edges are "has-a" or "uses" relationships.
ENTITY_RELATIONS: Dict[str, List[str]] = {
    # Warehouse structure
    "WarehouseGraph": ["Vertex", "Edge"],
    "Vertex": ["VertexKind"],
    "Edge": ["Vertex"],

    # Items and storage
    "ItemUnit": ["ItemType"],
    "StoragePlacement": ["ItemUnit", "Vertex"],
    "StoragePolicySnapshot": ["ItemType", "Vertex"],
    "StoragePolicyState": ["StoragePlacement", "StoragePolicySnapshot"],

    # Orders and tasks
    "Order": ["ItemUnit"],
    "MAPDTask": ["ItemUnit", "Vertex"],

    # Agents and system state
    "AgentState": ["AgentInternalState", "Vertex"],
    "JointSystemState": ["AgentState"],

    # Observations and controller
    "LocalObservationGraph": ["Vertex", "NodeFeatures", "EdgeFeatures"],
    "MAPDControllerConfig": ["ControllerArchitecture", "Vertex"],

    # Policies and feedback
    "TransportHistory": ["Vertex"],
    "PolicyPair": ["StorageFeedbackFunction", "RoutingPolicy", "StoragePolicyState", "TransportHistory"],
}


def build_relation_graph(relations: Dict[str, List[str]]) -> nx.DiGraph:
    g = nx.DiGraph()
    for parent, children in relations.items():
        g.add_node(parent)
        for child in children:
            g.add_node(child)
            g.add_edge(parent, child)
    return g


def draw_relation_graph(g: nx.DiGraph) -> None:
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(g, seed=42)

    nx.draw_networkx_nodes(g, pos, node_size=1200, node_color="#f0f0f0", edgecolors="#333333")
    nx.draw_networkx_labels(g, pos, font_size=9)
    nx.draw_networkx_edges(g, pos, arrowstyle="->", arrowsize=15, edge_color="#555555")

    plt.axis("off")
    plt.tight_layout()
    plt.show()


def print_relations(relations: Dict[str, List[str]]) -> None:
    """
    Text-only representation for quick inspection or headless environments.
    """
    for parent, children in relations.items():
        print(f"{parent} -> {', '.join(children)}")


if __name__ == "__main__":
    graph = build_relation_graph(ENTITY_RELATIONS)
    print("Type relationships:")
    print_relations(ENTITY_RELATIONS)
    draw_relation_graph(graph)