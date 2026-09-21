import math
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from base import OUT, C, G, POS


def normalised_entropy(p):
    p = np.asarray(p, float); p = p[p > 0]
    return float(-(p * np.log(p)).sum() / math.log(len(p)))


def concentration(seed=0):
    """Schematic illustration of H_T and C_T.

    NOTE: the two usage patterns are *illustrative* and must be replaced by
    measured mu_T(e) from a real run before the figure is used as a result.
    """
    # Traffic concentration doesn't care which direction an edge is traversed
    # in, only how unevenly $E$ is used -- an undirected view keeps that
    # count from double-booking the single one-way segment in $G$.
    rng = np.random.default_rng(seed)
    UG = G.to_undirected()
    edges = list(UG.edges())
    corridor = set(map(frozenset, zip(nx.shortest_path(UG, "4_0", "4_8")[:-1],
                                      nx.shortest_path(UG, "4_0", "4_8")[1:])))
    patterns = {
        "dispersed": np.full(len(edges), 10.0) + rng.integers(0, 3, len(edges)),
        "concentrated": np.array([60.0 if frozenset(e) in corridor else 3.0 for e in edges]),
    }
    probs = {k: w / w.sum() for k, w in patterns.items()}
    gmax = max(p.max() for p in probs.values())

    fig, axes = plt.subplots(1, 2, figsize=(13, 4.8))
    for ax, (name, p) in zip(axes, probs.items()):
        wv = dict(zip(edges, p))
        widths = [0.8 + 13 * (wv[e] / gmax) for e in edges]
        colors = [C["agent"] if wv[e] / gmax > 0.5 else "#9fb3c8" for e in edges]
        nx.draw_networkx_edges(UG, POS, edgelist=edges, width=widths,
                               edge_color=colors, ax=ax, arrows=False)
        nx.draw_networkx_nodes(UG, POS, node_size=80, node_color="white",
                               edgecolors=C["node"], ax=ax)
        H = normalised_entropy(p)
        ax.set_aspect("equal"); ax.axis("off")
        ax.text(0.5, 1.08, f"{name} traffic", transform=ax.transAxes,
                ha="center", fontsize=14)
        ax.text(0.5, 0.98, f"$H_T$ = {H:.2f},   $C_T = 1-H_T$ = {1-H:.2f}",
                transform=ax.transAxes, ha="center", fontsize=13, color=C["text"])
    axes[0].text(1.05, -0.10,
                 r"edge width $\propto p_T(e)=\mu_T(e)/\sum_{e'}\mu_T(e')$"
                 " (same scale in both panels)",
                 transform=axes[0].transAxes, ha="center", fontsize=12, color=C["node"])
    fig.savefig(f"{OUT}/concentration.png"); plt.close(fig)
