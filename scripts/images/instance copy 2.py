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
    # Reserve empty space to the right of the graph itself for the info
    # boxes below, so they sit beside the graph rather than on top of its
    # rightmost column of nodes. legend_center is where the graph's own
    # midpoint now falls in axes-fraction terms, used below so the
    # legend stays centered under the graph, not the wider canvas.
    xmin, xmax = ax.get_xlim()
    pad = 5.0
    legend_center = ((xmin + xmax) / 2 - xmin) / (xmax - xmin + pad)
    ax.set_xlim(xmin, xmax + pad)
    a_start, sj, gj = "4_1", "3_0", "0_0"
    to_pickup = nx.shortest_path(G, a_start, sj)
    to_delivery = nx.shortest_path(G, sj, gj)
    assert len(to_pickup) - 1 == 2   # t_assigned -> t_pickup
    assert len(to_delivery) - 1 == 3  # t_pickup -> t_finish
    route = to_pickup + to_delivery[1:]
    nx.draw_networkx_edges(G, POS, edgelist=list(zip(route, route[1:])),
                           edge_color=C["agent"], width=3.4, style=(0, (4, 3)), ax=ax,
                           arrows=False)
    put_agent(ax, a_start, "")
    # In-node letters, same convention as the storage-matrix example
    # (Table tab:storagematrix) and slap_mapd_coupling's own
    # assign_vertex_names/plot_node_names: storage vertices get A, B, C,
    # ...; delivery vertices get D1, D2, .... Centered on the marker,
    # colored by role, so s_j / g_j (the abstract task-tuple symbols) and
    # A / D1 (the concrete vertices they resolve to here) are both visible
    # at once instead of only one or the other.
    ax.annotate("A", POS[sj], ha="center", va="center", fontsize=11,
                fontweight="bold", color=C["store_e"], zorder=6)
    ax.annotate("D1", POS[gj], ha="center", va="center", fontsize=10,
                fontweight="bold", color=C["del_e"], zorder=6)
    #ax.annotate(r"$s_j$ (pickup)", POS[sj], textcoords="offset points",
                #xytext=(12, -6), fontsize=13)
    #ax.annotate(r"$g_j$ (delivery)", POS[gj], textcoords="offset points",
                #xytext=(-4, -26), fontsize=13)
    # One timestep per hop, matching fig:lifecycle's t_assigned=9 ...
    # t_finish=14: makes each step of the route individually identifiable,
    # not just the route's two named endpoints. Offsets are hand-placed
    # per node to clear the existing agent/A/D1/s_j/g_j labels and
    # markers, and each gets a white halo so it never visually merges
    # with the route line or a node underneath it even if placement is
    # imperfect at other figure widths.
    offsets = {a_start: (0, -20), "4_0": (0, -20), sj: (-28, 0),
              "2_0": (-28, 0), "1_0": (-28, 0), gj: (0, 20)}
    for i, node in enumerate(route):
        t = 9 + i
        ax.annotate(f"$t{{=}}{t}$", POS[node], textcoords="offset points",
                    xytext=offsets[node], fontsize=9, color=C["agent"], ha="center", va="center",
                    bbox=dict(boxstyle="round,pad=0.20", facecolor="white",
                             edgecolor="none", alpha=0.25))
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
               label=r"route"),
        Line2D([], [], color=C["accent"], lw=2.4, marker=">", markersize=9, # set marker at the end of the line  # adjust the mark here is off by 8 pixels in X axes
               label=r"one-way segment: $(v,w)\in E$, $(w,v)\notin E$"),

        #     ax.annotate("", xy=(1.72, -0.60), xytext=(1.78, -0.64),
        #        arrowprops=dict(arrowstyle="-|>", lw=2.2, color=C["accent"]))
    ]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(legend_center, -0.15),
              ncol=4, frameon=False, fontsize=11)
    ax.set_aspect("equal"); ax.set_axis_off()

    # Task info box, top-right (top-left collides with g_j = "0_0", which
    # sits at data coordinates (0,0), i.e. the graph's own top-left
    # corner). Same "boxed side note" convention as
    # slap_mapd_coupling's plot_storage_capacity_list. Kept to the
    # concrete instantiation only, the abstract tuple is already in the
    # surrounding text (eq:task), not repeated on the figure.
    task_lines = ["Task", "", r"$\tau_1=(5,\,A,\,D_1,\,\mathrm{tea})$"]
    ax.text(1.0, 1.06, "\n".join(task_lines), transform=ax.transAxes, va="top",
           ha="left", fontsize=11, linespacing=1.6,
           bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor=C["node"]))

    # Storage box directly under the task box: A's capacity and how much
    # of it this task's SKU (tea) occupies, in the same "used/max" format
    # as slap_mapd_coupling's plot_storage_capacity_list.
    storage_lines = ["Storage at A", "", "tea: 12 units", "capacity: 12/20"]
    ax.text(1.0, 0.74, "\n".join(storage_lines), transform=ax.transAxes, va="top",
           ha="left", fontsize=11, linespacing=1.6,
           bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor=C["store_e"]))

    fig.savefig(f"{OUT}/instance.png"); plt.close(fig)


if __name__ == "__main__":
    instance()
