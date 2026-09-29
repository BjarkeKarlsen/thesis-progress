"""
thesis-guide-images.md Section 8 ("Controllers: Who Decides What"): the same
small graph viewed under the three architectures -- centralised sees
everything, section-based sees only its own zone, decentralised sees only
one agent's local neighbourhood.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mp
import networkx as nx

from base import OUT, C
from mini import mini_graph, draw_mini, put_agent

EGO = "1_1"
# Shared data limits for every panel: with aspect="equal", letting (b)'s
# zone boxes grow its limits would shrink its graph and lift its title.
XLIM, YLIM = (-0.6, 3.9), (-2.6, 0.6)
# Fill of "the observed region": one colour per controller, distinct from
# (b)'s blue/orange zone fills so no two panels read as the same view.
CENT_F, CENT_E = C["ep_f"], C["ep_e"]
DEC_F, DEC_E = "#eadcf2", C["comm"]


def _region(ax, nodes, pos, fc, ec):
    """Rounded box around `nodes`, drawn behind the graph."""
    xs = [pos[n][0] for n in nodes]; ys = [pos[n][1] for n in nodes]
    ax.add_patch(mp.FancyBboxPatch((min(xs) - 0.45, min(ys) - 0.45),
                                   max(xs) - min(xs) + 0.9, max(ys) - min(ys) + 0.9,
                                   boxstyle="round,pad=0.05", fc=fc, ec=ec,
                                   lw=1.4, zorder=0))
    return xs, ys


def _panel(ax, G, pos, mode):
    # One visual rule across all panels: the shaded region is what decides
    # a_i's next move; only what lies outside it is dimmed.
    if mode == "centralised":
        ax.set_title("(a) centralised: sees the whole graph", fontsize=11)
        _region(ax, list(G), pos, CENT_F, CENT_E)
        draw_mini(ax, G, pos)
    elif mode == "section":
        ax.set_title("(b) section-based: sees only its own zone", fontsize=11)
        y1 = [n for n in G if int(n.split("_")[1]) < 2]
        y2 = [n for n in G if int(n.split("_")[1]) >= 2]
        for nodes, fc, ec in ((y1, C["store_f"], C["store_e"]),
                              (y2, C["del_f"], C["del_e"])):
            _region(ax, nodes, pos, fc, ec)
        # Edges between zones belong to neither section controller's view.
        cross = [(u, v) for u, v in G.edges() if (u in y1) != (v in y1)]
        inside = G.copy(); inside.remove_edges_from(cross)
        draw_mini(ax, inside, pos)
        nx.draw_networkx_edges(G, pos, edgelist=cross, ax=ax, edge_color=C["edge"],
                               width=1.8, alpha=0.35, arrows=False)
    else:
        ax.set_title("(c) decentralised: one agent's local window only", fontsize=11)
        window = set(nx.single_source_shortest_path_length(G, EGO, cutoff=1))
        # Plus-shaped region around the 1-hop window (a box would also cover
        # the diagonal neighbours, which a_i cannot see): one bar per axis,
        # outlined first, then filled again on top to hide the inner outlines.
        r, c = EGO.split("_")
        bars = ([n for n in window if n.split("_")[0] == r],
                [n for n in window if n.split("_")[1] == c])
        for bar in bars:
            _region(ax, bar, pos, DEC_F, DEC_E)
        for bar in bars:
            _region(ax, bar, pos, DEC_F, "none")
        draw_mini(ax, G, pos, dim=True)
        draw_mini(ax, G.subgraph(window), pos)
    put_agent(ax, pos, EGO, r"$a_i$")


def controllers_example():
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.4))
    for ax, mode in zip(axes, ("centralised", "section", "decentralised")):
        G, pos = mini_graph(rows=3, cols=4, dx=1.1, dy=1.0)
        _panel(ax, G, pos, mode)
        ax.set_xlim(*XLIM); ax.set_ylim(*YLIM)
        ax.set_aspect("equal"); ax.set_axis_off()
    fig.tight_layout()
    fig.savefig(f"{OUT}/controllers_example.png"); plt.close(fig)


if __name__ == "__main__":
    controllers_example()
