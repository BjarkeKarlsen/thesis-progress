import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import networkx as nx

from base import OUT, C, G, POS, put_agent, draw_base


def instance():
    fig, ax = plt.subplots(figsize=(12, 5.6))
    draw_base(ax)
    sj, gj = "2_6", "0_0"
    path = nx.shortest_path(G, sj, gj)
    nx.draw_networkx_edges(G, POS, edgelist=list(zip(path, path[1:])),
                           edge_color=C["agent"], width=3.4, style=(0, (4, 3)), ax=ax,
                           arrows=False)
    for n, lab in {"4_0": "$a_1$", "2_4": "$a_2$", "0_6": "$a_3$"}.items():
        put_agent(ax, n, lab)
    ax.annotate(r"$s_j$ (pickup)", POS[sj], textcoords="offset points",
                xytext=(12, -6), fontsize=13)
    ax.annotate(r"$g_j$ (delivery)", POS[gj], textcoords="offset points",
                xytext=(-4, -26), fontsize=13)
    handles = [
        Line2D([], [], marker="o", ls="", mfc=C["store_f"], mec=C["store_e"], ms=12,
               label=r"storage $\mathcal{V}_{\mathrm{str}}$"),
        Line2D([], [], marker="s", ls="", mfc=C["del_f"], mec=C["del_e"], ms=12,
               label=r"delivery $\mathcal{V}_{\mathrm{del}}$"),
        Line2D([], [], marker="D", ls="", mfc=C["ep_f"], mec=C["ep_e"], ms=11,
               label=r"endpoint $\mathcal{V}_{\mathrm{ep}}$"),
        Line2D([], [], marker="o", ls="", mfc="white", mec=C["node"], ms=12,
               label="transit vertex"),
        Line2D([], [], marker="o", ls="", color=C["agent"], ms=12, label="agent"),
        Line2D([], [], ls=(0, (4, 3)), color=C["agent"], lw=3,
               label=r"task $\tau_j=(r_j,s_j,g_j,k_j)$"),
        Line2D([], [], color=C["accent"], lw=2.4, marker=">", markersize=9, # adjust the mark here is off by 8 pixels in X axes
               label=r"one-way segment: $(v,w)\in E$, $(w,v)\notin E$"),

        #     ax.annotate("", xy=(1.72, -0.60), xytext=(1.78, -0.64),
        #        arrowprops=dict(arrowstyle="-|>", lw=2.2, color=C["accent"]))
    ]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, 0.02),
              ncol=4, frameon=False, fontsize=11)
    ax.set_aspect("equal"); ax.set_axis_off()
    fig.savefig(f"{OUT}/instance.png"); plt.close(fig)
