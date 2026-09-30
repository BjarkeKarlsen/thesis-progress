import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import networkx as nx

from base import OUT, C, G, POS, STORAGE, DELIVERY, ENDPOINTS

# The left part of the shared warehouse (base.py's G/POS), the same graph
# fig:observation shows in full, so the task example and the observation
# example are one warehouse and one story: a_2 is assigned tau_1 at t=9,
# picks up at A at t=11 (where fig:observation shows it), delivers at D1 at
# t=14. Columns 0-2 are drawn, column 3 faded to show the warehouse goes on.
# Odd columns only exist on the two cross-aisles, as everywhere in base.py,
# so there is no middle path here, unlike the old stand-alone 5x3 grid.
SHOWN_COLS, FADED_COL = 2, 3


def _col(n):
    return int(n.split("_")[1])


def instance():
    """
    One agent, one task. Path lengths match the running example (Table
    tab:tau1timeline in 2.Introduction.tex): agent to pickup is 2 hops
    (t_assigned=9 -> t_pickup=11), pickup to delivery is 3 hops
    (t_pickup=11 -> t_finish=14).
    """
    shown = [n for n in G if _col(n) <= SHOWN_COLS]
    faded = [n for n in G if _col(n) == FADED_COL]
    fig, ax = plt.subplots(figsize=(6.2, 6.6))

    solid = [(u, v) for u, v in G.subgraph(shown).edges()]
    edge_out = [(u, v) for u, v in G.edges() if u in shown and v in faded]
    nx.draw_networkx_edges(G, POS, edgelist=solid, ax=ax, edge_color=C["edge"],
                           width=1.8, arrows=False)
    nx.draw_networkx_edges(G, POS, edgelist=edge_out, ax=ax, edge_color=C["edge"],
                           width=1.8, alpha=0.3, arrows=False)
    nx.draw_networkx_nodes(G, POS, nodelist=faded, node_color="white",
                           edgecolors=C["node"], node_size=520, alpha=0.3, ax=ax)
    roles = (
        ([n for n in shown if n not in STORAGE + DELIVERY + ENDPOINTS], "white", C["node"], "o", 520),
        ([n for n in shown if n in STORAGE], C["store_f"], C["store_e"], "o", 520),
        ([n for n in shown if n in DELIVERY], C["del_f"], C["del_e"], "s", 620),
        ([n for n in shown if n in ENDPOINTS], C["ep_f"], C["ep_e"], "D", 530),
    )
    for nl, fc, ec, shape, size in roles:
        nx.draw_networkx_nodes(G, POS, nodelist=nl, node_color=fc, edgecolors=ec,
                               node_shape=shape, node_size=size, ax=ax)

    a_start, sj, gj = "4_1", "3_0", "0_0"
    route = ["4_1", "4_0", "3_0", "2_0", "1_0", "0_0"]
    for u, v in zip(route, route[1:]):
        assert G.has_edge(u, v), (u, v)
    assert sj in STORAGE and gj in DELIVERY
    assert route.index(sj) == 2   # t_assigned -> t_pickup: 2 hops
    assert len(route) - 1 - route.index(sj) == 3  # t_pickup -> t_finish: 3 hops
    nx.draw_networkx_edges(G, POS, edgelist=list(zip(route, route[1:])),
                           edge_color=C["agent"], width=3.4, style=(0, (4, 3)), ax=ax,
                           arrows=False)
    ax.scatter(*POS[a_start], s=300, c=C["agent"], zorder=5,
               edgecolors="white", linewidths=1.3)
    ax.annotate(r"$a_2$", POS[a_start], textcoords="offset points", xytext=(18, 10),
                ha="center", color=C["agent"], fontsize=14)
    # In-node letters: storage vertices A, B, ..., delivery vertices D1, D2,
    # the same convention as fig:observation and slap_mapd_coupling.
    ax.annotate("A", POS[sj], ha="center", va="center", fontsize=11,
                fontweight="bold", color=C["store_e"], zorder=6)
    ax.annotate("D1", POS[gj], ha="center", va="center", fontsize=10,
                fontweight="bold", color=C["del_e"], zorder=6)
    # A's contents, matching Table tab:storagematrix. mugs is 0 at A,
    # which is why tau_2 in the text is illegal.
    held_at_a = [("tea", 12), ("coffee", 4), ("mugs", 0)]
    ax.annotate("\n".join(f"{sku}:{units}" for sku, units in held_at_a),
                POS[sj], textcoords="offset points",
                xytext=(14, -10 * len(held_at_a)), fontsize=8,
                linespacing=1.4, zorder=7)
    # One timestep per hop, matching fig:lifecycle's t_assigned=9 ...
    # t_finish=14.
    offsets = {a_start: (0, -22), "4_0": (0, -22), sj: (-30, 0),
               "2_0": (-30, 0), "1_0": (-30, 0), gj: (0, 22)}
    for i, node in enumerate(route):
        ax.annotate(f"$t{{=}}{9 + i}$", POS[node], textcoords="offset points",
                    xytext=offsets[node], fontsize=9, color=C["agent"],
                    ha="center", va="center",
                    bbox=dict(boxstyle="round,pad=0.20", facecolor="white",
                              edgecolor="none", alpha=0.25))
    mid = ((POS[a_start][0] + POS["4_0"][0]) / 2, POS[a_start][1])
    ax.annotate(r"$\tau_1$", mid, textcoords="offset points", xytext=(0, 14),
                fontsize=11, color=C["agent"], ha="center", fontweight="bold")

    handles = [
        Line2D([], [], marker="o", ls="", mfc=C["store_f"], mec=C["store_e"], ms=12,
               label=r"$V_{\mathrm{str}}$"),
        Line2D([], [], marker="s", ls="", mfc=C["del_f"], mec=C["del_e"], ms=12,
               label=r"$V_{\mathrm{del}}$"),
        Line2D([], [], marker="D", ls="", mfc=C["ep_f"], mec=C["ep_e"], ms=11,
               label=r"$V_{\mathrm{ep}}$"),
        Line2D([], [], marker="o", ls="", mfc="white", mec=C["node"], ms=12,
               label=r"$V_{\mathrm{mov}}$"),
        Line2D([], [], marker="o", ls="", color=C["agent"], ms=12, label="agent"),
        Line2D([], [], ls=(0, (4, 3)), color=C["agent"], lw=1.8,
               label=r"Active set $\mathcal{B}_t$ for Task $\tau_1=(5,\,A,\,D_1,\,\mathrm{tea})$"),
    ]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.02),
              ncol=3, frameon=False, fontsize=11)
    ax.set_aspect("equal"); ax.set_axis_off()
    fig.savefig(f"{OUT}/instance.png"); plt.close(fig)


if __name__ == "__main__":
    instance()
