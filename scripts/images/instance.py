import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from base import OUT, C
from m8 import Warehouse

# The top-left corner of the real 8-agent warehouse (m8.py), from the left wall
# down to the upper one-way lane of the central loop. a_2 is assigned tau_1 at
# t=9, drives into shelf A, picks up at t=11, backs out to the aisle and delivers
# at W1 at t=14. Every role vertex is a leaf ([A47] [A70]), so the route enters
# and leaves A by the same edge.
CROP = dict(x_max=6.0, x_faded=7.5, y_min=9.0)

# Vertex ids of the crop that the story uses.
A_START, SHELF_A, WORKSTATION = 87, 168, 159
ROUTE = [87, 86, 168, 86, 80, 159]
# Stock under each shelf, the 01c_storage_state_on_instance.py style. A matches
# Table tab:storagematrix, mugs 0 is why tau_2 in the text breaks the stock
# condition. The other shelves are illustrative.
STOCK = {
    168: [("tea", 12), ("coffee", 4), ("mugs", 0)],
    158: [("coffee", 6)],
    178: [("mugs", 5)],
    172: [("tea", 3), ("mugs", 2)],
    157: [("coffee", 2)],
}
def instance():
    """
    One agent, one task. Path lengths match the running example (Table
    tab:tau1timeline in 2.Introduction.tex): agent to pickup is 2 hops
    (t_assigned=9 -> t_pickup=11), pickup to delivery is 3 hops
    (t_pickup=11 -> t_finish=14).
    """
    wh = Warehouse(**CROP)
    pos, roles, edges = wh.pos, wh.roles, wh.edges

    route_edges = list(zip(ROUTE, ROUTE[1:]))
    for edge in route_edges:
        assert edge in edges, edge
    assert roles[SHELF_A] == "storage" and roles[WORKSTATION] == "delivery"
    assert ROUTE.index(SHELF_A) == 2   # t_assigned -> t_pickup: 2 hops
    assert len(ROUTE) - 1 - ROUTE.index(SHELF_A) == 3  # t_pickup -> t_finish: 3 hops

    fig, ax = plt.subplots(figsize=(6.4, 5.6))
    wh.draw(ax)

    xs, ys = zip(*(pos[v] for v in ROUTE))
    ax.plot(xs, ys, color=C["agent"], lw=3.0, ls=(0, (4, 3)), zorder=2)
    ax.scatter(*pos[A_START], s=150, c=C["agent"], zorder=5, edgecolors="white", linewidths=1.2)
    ax.annotate(r"$a_2$", pos[A_START], textcoords="offset points", xytext=(0, 13),
                ha="center", color=C["agent"], fontsize=14)
    # In-node letters: storage vertex A and delivery workstation W1, the same convention
    # as fig:observation and slap_mapd_coupling.
    ax.annotate("A", pos[SHELF_A], ha="center", va="center", fontsize=9,
                fontweight="bold", color=C["store_e"], zorder=6)
    ax.annotate("W1", pos[WORKSTATION], ha="center", va="center", fontsize=7,
                fontweight="bold", color=C["del_e"], zorder=6)
    for v, held in STOCK.items():
        ax.annotate("\n".join(f"{sku}:{units}" for sku, units in held), pos[v],
                    textcoords="offset points", xytext=(0, -11), ha="center", va="top",
                    fontsize=6.5, linespacing=1.2, zorder=7)
    # One timestep per hop, matching fig:lifecycle's t_assigned=9 ... t_finish=14.
    # The route passes vertex 86 twice, at t=10 and t=12.
    times = {}
    for i, v in enumerate(ROUTE):
        times.setdefault(v, []).append(str(9 + i))
    offsets = {87: (0, -15), 86: (0, 15), 168: (0, 15), 80: (-20, -14), 159: (24, 0)}
    for v, ts in times.items():
        ax.annotate(f"$t{{=}}{','.join(ts)}$", pos[v], textcoords="offset points",
                    xytext=offsets[v], fontsize=8, color=C["agent"], ha="center", va="center",
                    bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none",
                              alpha=0.8), zorder=8)

    handles = wh.legend_handles() + [
        Line2D([], [], marker="o", ls="", color=C["agent"], ms=10, label="agent"),
        Line2D([], [], ls=(0, (4, 3)), color=C["agent"], lw=1.8,
               label=r"Active set $\mathcal{B}_t$ for Task $\tau_1=(5,\,A,\,W_1,\,\mathrm{tea})$"),
    ]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.01),
              ncol=3, frameon=False, fontsize=10)
    ax.set_aspect("equal"); ax.set_axis_off()
    fig.savefig(f"{OUT}/instance.png"); plt.close(fig)


if __name__ == "__main__":
    instance()
