import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D
from matplotlib.lines import Line2D
import networkx as nx

from base import OUT, C
from mini import mini_graph, draw_mini, put_agent

# A small, self-contained warehouse instead of cropping the full 5x9 one
# (base.py's G/POS): the route only ever needs 2 columns and 5 rows, so a
# tiny grid keeps every marker, label and info box legible without
# chopping the shared graph in half mid-node.
STORAGE = ["1_0", "2_0", "3_0", "1_2", "2_2", "3_2"]
DELIVERY = ["0_0"]
ENDPOINTS = ["0_2"]
ONE_WAY = ("1_2", "2_2")  # allowed direction only: 1_2 -> 2_2


def instance():
    """
    One agent, one task. Path lengths are chosen to match the running
    example (Table tab:tau1timeline in 2.Introduction.tex): agent to
    pickup is 2 hops (t_assigned=9 -> t_pickup=11), pickup to delivery is
    3 hops (t_pickup=11 -> t_finish=14), so the picture doesn't silently
    contradict the numbers used in the text.
    """
    G, POS = mini_graph(rows=5, cols=3, one_way=ONE_WAY)
    fig, ax = plt.subplots(figsize=(7.5, 6.6))
    draw_mini(ax, G, POS, storage=STORAGE, delivery=DELIVERY, endpoints=ENDPOINTS)
    legend_center = 0.5
    a_start, sj, gj = "4_1", "3_0", "0_0"
    # mini_graph is a full dense grid (unlike base.py's sparse aisle
    # graph), so more than one shortest path exists between these nodes.
    # The route is spelled out explicitly rather than left to
    # nx.shortest_path's arbitrary tie-breaking.
    route = ["4_1", "4_0", "3_0", "2_0", "1_0", "0_0"]
    for u, v in zip(route, route[1:]):
        assert G.has_edge(u, v), (u, v)
    assert route[2] == sj and route[-1] == gj
    assert route.index(sj) == 2   # t_assigned -> t_pickup: 2 hops
    assert len(route) - 1 - route.index(sj) == 3  # t_pickup -> t_finish: 3 hops
    nx.draw_networkx_edges(G, POS, edgelist=list(zip(route, route[1:])),
                           edge_color=C["agent"], width=3.4, style=(0, (4, 3)), ax=ax,
                           arrows=False)
    put_agent(ax, POS, a_start, "")
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
    # A's contents, same "sku:count" convention as
    # slap_mapd_coupling's plot_storage_contents (units > 0 only, labelled
    # underneath the vertex): tea 12, coffee 4, matching
    # Table tab:storagematrix exactly. mugs is left out because it is 0
    # at A, which is also why tau_2 in the task box above is illegal.
    held_at_a = [("tea", 12), ("coffee", 4), ("mugs", 0)]
    ax.annotate("\n".join(f"{sku}:{units}" for sku, units in held_at_a),
                POS[sj], textcoords="offset points",
                xytext=(12, -10 * len(held_at_a)), fontsize=8,
                linespacing=1.4, zorder=7)
    # One timestep per hop, matching fig:lifecycle's t_assigned=9 ...
    # t_finish=14: makes each step of the route individually identifiable,
    # not just the route's two named endpoints. Offsets are hand-placed
    # per node to clear the existing agent/A/D1 labels and markers, and
    # each gets a white halo so it never visually merges with the route
    # line or a node underneath it even if placement is imperfect at
    # other figure widths.
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
               label=r"Active set $\mathcal{B}_t$ for Task $\tau_1=(5,\,A,\,D_1,\,\mathrm{tea})$"),
    ]
    oneway_handle = Line2D([], [], color=C["accent"], lw=2.4, marker=">",
                           markersize=9, label=r"one-way segment")
    handles.append(oneway_handle)
    leg = ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(legend_center, -0.05),
                    ncol=3, frameon=False, fontsize=11,
                    handler_map={oneway_handle: HandlerLine2D(numpoints=2)})
    # HandlerLine2D doesn't propagate markevery from the original handle
    # to the legend's own copy, so pin it directly on the rendered legend
    # line instead: mark only the last of its two points, putting the
    # arrowhead at the end of the sample bar rather than its middle.
    for lh in leg.legend_handles:
        if lh.get_label() == "one-way segment":
            lh.set_markevery([len(lh.get_xdata()) - 1])
    ax.set_aspect("equal"); ax.set_axis_off()


    # Small in-place tag on the route itself, same color as the label
    # above and the route/agent, reinforcing which task this route is
    # without the reader needing to hold the box-to-route link in mind.
    mid = ((POS[a_start][0] + POS["4_0"][0]) / 2, POS[a_start][1])
    ax.annotate(r"$\tau_1$", mid, textcoords="offset points", xytext=(0, 14),
                fontsize=11, color=C["agent"], ha="center", fontweight="bold")

    fig.savefig(f"{OUT}/instance.png"); plt.close(fig)


if __name__ == "__main__":
    instance()
