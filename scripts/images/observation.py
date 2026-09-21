import math
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import networkx as nx

from base import OUT, C, G, POS, put_agent, draw_base


def observation(ego="4_4", depth=2, target="0_0", r_com=3.3):
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
    for n, lab in {"4_0": "$a_1$", ego: "$a_2$", "4_8": "$a_3$"}.items():
        put_agent(ax, n, lab, dx=-17, dy=6)
    ex, ey = POS[ego]
    ax.add_patch(plt.Circle((ex, ey), r_com, fill=False, ls=(0, (2, 3)),
                            lw=2.2, color=C["comm"]))
    ang = math.radians(230)
    ax.annotate("", xy=(ex + r_com * math.cos(ang), ey + r_com * math.sin(ang)),
                xytext=(ex, ey),
                arrowprops=dict(arrowstyle="<->", color=C["comm"], lw=1.8, ls=":"))
    ax.annotate(r"$r_{\mathrm{com}}$",
                (ex + 0.55 * r_com * math.cos(ang) - 0.45,
                 ey + 0.55 * r_com * math.sin(ang) - 0.1),
                color=C["comm"], fontsize=14)
    ax.annotate(r"target $q_2(t)$", POS[target], textcoords="offset points",
                xytext=(-8, -30), fontsize=12, color=C["del_e"])
    handles = [
        Line2D([], [], color=C["accent"], lw=3,
               label=r"induced subgraph $\mathcal{G}^{(d)}_i(t)$, $d=2$"),
        Line2D([], [], ls=(0, (2, 3)), color=C["comm"], lw=2,
               label=r"communication radius $r_{\mathrm{com}}$"),
        Line2D([], [], marker="o", ls="", color=C["agent"], ms=12, label="agent"),
        Line2D([], [], marker=r"$5$", ls="", color=C["accent"], ms=13,
               label=r"$\eta_i(v,t)=d_G(v,q_i(t))$"),
    ]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, 0.06),
              ncol=2, frameon=False, fontsize=12)
    ax.set_aspect("equal"); ax.set_axis_off()
    fig.savefig(f"{OUT}/observation.png"); plt.close(fig)
