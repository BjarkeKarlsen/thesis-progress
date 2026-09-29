"""
Shared setup for the *simple* companion figures: a small (<=8 vertex)
warehouse graph, built with the same generator logic as base.py's full
5x9 grid but tiny enough that a single mechanism -- not the layout -- is
what the reader has to parse.

Kept separate from base.py so the existing (complex) figures are never
touched by anything in this module.
"""
import networkx as nx

from base import C


def mini_graph(rows=2, cols=4, dx=1.4, dy=1.2, one_way=None):
    """A small full-grid graph, bidirectional except `one_way=(u, v)`,
    which removes the (v, u) edge to give one genuine one-way segment."""
    G, pos = nx.DiGraph(), {}
    for r in range(rows):
        for c in range(cols):
            n = f"{r}_{c}"
            G.add_node(n)
            pos[n] = (c * dx, -r * dy)
    for n in list(G):
        r, c = map(int, n.split("_"))
        for dr, dc in ((0, 1), (1, 0)):
            m = f"{r + dr}_{c + dc}"
            if m in G:
                G.add_edge(n, m)
                G.add_edge(m, n)
    if one_way is not None:
        u, v = one_way
        if G.has_edge(v, u):
            G.remove_edge(v, u)
    return G, pos


def draw_mini(ax, G, pos, storage=(), delivery=(), endpoints=(), dim=False):
    """Draw a mini graph with the same role colours/shapes as base.draw_base."""
    a = 0.35 if dim else 1.0
    two_way = [(u, v) for u, v in G.edges() if (v, u) in G.edges()]
    one_way = [(u, v) for u, v in G.edges() if (v, u) not in G.edges()]
    nx.draw_networkx_edges(G, pos, edgelist=two_way, ax=ax, edge_color=C["edge"],
                           width=1.8, alpha=a, arrows=False)
    nx.draw_networkx_edges(G, pos, edgelist=one_way, ax=ax, edge_color=C["accent"],
                           width=2.2, alpha=a, arrows=True, arrowsize=20,
                           node_size=520, connectionstyle="arc3,rad=0.0")
    other = [n for n in G if n not in set(storage) | set(delivery) | set(endpoints)]
    for nl, fc, ec, shape, size in (
        (other, "white", C["node"], "o", 520),
        (list(storage), C["store_f"], C["store_e"], "o", 520),
        (list(delivery), C["del_f"], C["del_e"], "s", 620),
        (list(endpoints), C["ep_f"], C["ep_e"], "D", 530),
    ):
        if nl:
            nx.draw_networkx_nodes(G, pos, nodelist=nl, node_color=fc, edgecolors=ec,
                                   node_shape=shape, node_size=size, ax=ax, alpha=a)


def put_agent(ax, pos, node, label, dx=0, dy=17, color=None):
    c = color or C["agent"]
    ax.scatter(*pos[node], s=290, c=c, zorder=5, edgecolors="white", linewidths=1.3)
    ax.annotate(label, pos[node], textcoords="offset points", xytext=(dx, dy),
                ha="center", color=c, fontsize=13)
