import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import networkx as nx

from base import OUT, C, G, POS, DELIVERY, put_agent, draw_base


# Matches the worked example in the thesis text (tab:observationexample):
# the field of view holds 5 vertices besides a_1's own, 2 of them occupied
# (delta_1 = 2/5), and exactly one agent (a_4) sits just outside the bound.
# Also the eta example: a_1 chooses between B (eta=4) and C (eta=6).
def observation(ego="4_1", depth=2, target="0_0"):
    obs = dict(nx.single_source_shortest_path_length(G, ego, cutoff=depth))
    sub = G.subgraph(obs)
    fig, ax = plt.subplots(figsize=(12, 5.6))
    draw_base(ax, dim=True)
    nx.draw_networkx_edges(sub, POS, ax=ax, edge_color=C["accent"], width=3.0, arrows=False)
    nx.draw_networkx_nodes(G, POS, nodelist=list(obs), node_size=470,
                           node_color="none", edgecolors=C["accent"], linewidths=3.0, ax=ax)
    for n in obs:                                     # eta_i(v,t)
        ax.annotate(str(nx.shortest_path_length(G, n, target)), POS[n],
                    textcoords="offset points", xytext=(13, 10), ha="left",
                    fontsize=12, color=C["accent"], weight="bold")
    for n, lab in {ego: "$a_1$", "3_0": "$a_2$", "4_3": "$a_3$", "4_4": "$a_4$"}.items():
        put_agent(ax, n, lab, dx=-17, dy=6)
    # a_1's target is drawn at full strength so it stands out from the
    # dimmed warehouse. Delivery vertices are named D1, D2, ... inside the
    # marker, the same convention as instance.py.
    nx.draw_networkx_nodes(G, POS, nodelist=[target], node_color=C["del_f"],
                           edgecolors=C["del_e"], node_shape="s", node_size=560, ax=ax)
    for i, n in enumerate(DELIVERY, start=1):
        ax.annotate(f"D{i}", POS[n], ha="center", va="center", fontsize=10,
                    fontweight="bold", color=C["del_e"], zorder=6,
                    alpha=1.0 if n == target else 0.35)
    # a_1's two moves, named in the text: B is shorter but a_2 sits on its
    # route to D1, C is longer. Replaces the separate potential_example figure.
    # Solid white fill so the edges through them do not cross the letters.
    nx.draw_networkx_nodes(G, POS, nodelist=["4_0", "4_2"], node_size=470, node_color="white",
                           edgecolors=C["accent"], linewidths=3.0, ax=ax)
    # a_2 stands on storage vertex A, the pickup of tau_1 in fig:taskroute:
    # this is the same warehouse at t=11, when a_2 picks up the tea.
    ax.annotate("A", POS["3_0"], textcoords="offset points", xytext=(15, -17),
                ha="center", va="center", fontsize=12, fontweight="bold",
                color=C["store_e"], zorder=6)
    for n, lab in (("4_0", "B"), ("4_2", "C")):
        ax.annotate(lab, POS[n], ha="center", va="center", fontsize=12,
                    fontweight="bold", color=C["text"], zorder=6)
    # Kept to plain words; the symbols (eta_1, d_obs, delta_1) are in the caption.
    handles = [
        Line2D([], [], color=C["accent"], lw=3, label="field of view"),
        Line2D([], [], marker="o", ls="", color=C["agent"], ms=12, label="agent"),
        Line2D([], [], marker="s", ls="", mfc=C["del_f"], mec=C["del_e"], ms=13,
               label="delivery vertex"),
        # A letter, not a sample digit, so it cannot be read as a vertex value.
        Line2D([], [], ls="", marker=r"$\mathbf{n}$", color=C["accent"], ms=11,
               label="fewest steps from that vertex to D1"),
    ]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, 0.04),
              ncol=4, frameon=False, fontsize=12)
    ax.set_aspect("equal"); ax.set_axis_off()
    fig.savefig(f"{OUT}/observation.png"); plt.close(fig)
