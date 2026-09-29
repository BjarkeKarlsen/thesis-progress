import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import networkx as nx

from base import OUT, C, G, POS, put_agent, draw_base


def instance():
    """
    One agent, one task. Path lengths are chosen to match the running
    example (Table tab:tau1timeline in 2.Introduction.tex): agent to
    pickup is 2 hops (t_assigned=9 -> t_pickup=11), pickup to delivery is
    3 hops (t_pickup=11 -> t_finish=14), so the picture doesn't silently
    contradict the numbers used in the text.
    """
    fig, ax = plt.subplots(figsize=(12, 5.6))
    draw_base(ax)
    a_start, sj, gj = "4_1", "3_0", "0_0"
    to_pickup = nx.shortest_path(G, a_start, sj)
    to_delivery = nx.shortest_path(G, sj, gj)
    assert len(to_pickup) - 1 == 2   # t_assigned -> t_pickup
    assert len(to_delivery) - 1 == 3  # t_pickup -> t_finish
    route = to_pickup + to_delivery[1:]
    nx.draw_networkx_edges(G, POS, edgelist=list(zip(route, route[1:])),
                           edge_color=C["agent"], width=3.4, style=(0, (4, 3)), ax=ax,
                           arrows=False)
    put_agent(ax, a_start, "$a_2$")
    ax.annotate(r"$s_j$ (pickup)", POS[sj], textcoords="offset points",
                xytext=(12, -6), fontsize=13)
    ax.annotate(r"$g_j$ (delivery)", POS[gj], textcoords="offset points",
                xytext=(-4, -26), fontsize=13)
    handles = [
        Line2D([], [], marker="o", ls="", mfc=C["store_f"], mec=C["store_e"], ms=12,
               label=r"storage $V_{\mathrm{str}}$"),
        Line2D([], [], marker="s", ls="", mfc=C["del_f"], mec=C["del_e"], ms=12,
               label=r"delivery $V_{\mathrm{del}}$"),
        Line2D([], [], marker="D", ls="", mfc=C["ep_f"], mec=C["ep_e"], ms=11,
               label=r"endpoint $V_{\mathrm{ep}}$"),
        Line2D([], [], marker="o", ls="", mfc="white", mec=C["node"], ms=12,
               label="transit vertex"),
        Line2D([], [], marker="o", ls="", color=C["agent"], ms=12, label="agent $a_2$"),
        Line2D([], [], ls=(0, (4, 3)), color=C["agent"], lw=3,
               label=r"route: assignment $\to$ pickup $\to$ delivery"),
        Line2D([], [], color=C["accent"], lw=2.4, marker=">", markersize=9, # adjust the mark here is off by 8 pixels in X axes
               label=r"one-way segment: $(v,w)\in E$, $(w,v)\notin E$"),

        #     ax.annotate("", xy=(1.72, -0.60), xytext=(1.78, -0.64),
        #        arrowprops=dict(arrowstyle="-|>", lw=2.2, color=C["accent"]))
    ]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, 0.02),
              ncol=4, frameon=False, fontsize=11)
    ax.set_aspect("equal"); ax.set_axis_off()
    fig.savefig(f"{OUT}/instance.png"); plt.close(fig)


if __name__ == "__main__":
    instance()
