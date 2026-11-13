import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from base import OUT, C
from m8 import Warehouse

# The top-left corner of the real 8-agent warehouse (m8.py), the same as
# fig:taskroute but one aisle wider, at t=12. a_2 has picked up the tea of
# tau_1 at A and is back on the aisle on its way to W1. a_1 is also heading
# for W1. Matches the worked example in the thesis text: the field of view
# holds 5 vertices besides a_1's own, 2 of them occupied (delta_1 = 2/5), and
# a_4 sits just outside it. a_1 chooses between v (eta=3), with a_2 just past
# it, and w (eta=5).
CROP = dict(x_max=10.5, x_faded=12.0, y_min=9.0)
EGO, DEPTH, TARGET, SHELF_A = 88, 2, 159, 168
AGENTS = {88: "$a_1$", 86: "$a_2$", 81: "$a_3$", 98: "$a_4$"}
MOVES = {87: "$v$", 89: "$w$"}  # aisle vertices, not shelves: B and C name shelves (Table I)


def observation():
    wh = Warehouse(**CROP)
    full = Warehouse()
    view = wh.steps(EGO, cutoff=DEPTH)
    assert len(view) - 1 == 5
    assert sum(v in view for v in AGENTS if v != EGO) == 2   # delta_1 = 2/5
    assert all(v in view for v in MOVES)
    eta = {v: full.steps(v)[TARGET] for v in view}
    assert (eta[87], eta[89]) == (3, 5)

    fig, ax = plt.subplots(figsize=(9.6, 5.6))
    wh.draw(ax, dim=[v for v in wh.pos if v not in view and v != TARGET])
    for (u, v) in wh.edges:
        if u in view and v in view:
            ax.plot(*zip(wh.pos[u], wh.pos[v]), color=C["accent"], lw=3.0, zorder=2)
    ax.scatter([wh.pos[v][0] for v in view], [wh.pos[v][1] for v in view], s=300,
               c="none", edgecolors=C["accent"], linewidths=3.0, zorder=4)
    for v in view:                                    # eta_1(v,t)
        ax.annotate(str(eta[v]), wh.pos[v], textcoords="offset points", xytext=(10, 8),
                    ha="left", fontsize=11, color=C["accent"], weight="bold", zorder=8)
    for v, label in AGENTS.items():
        ax.scatter(*wh.pos[v], s=150, c=C["agent"], zorder=5, edgecolors="white",
                   linewidths=1.2)
        ax.annotate(label, wh.pos[v], textcoords="offset points", xytext=(-14, 8),
                    ha="center", color=C["agent"], fontsize=13, zorder=8)
    # a_1's two moves, named in the text. B is shorter but a_2 is just past it,
    # C is longer.
    for v, label in MOVES.items():
        ax.annotate(label, wh.pos[v], ha="center", va="center", fontsize=12,
                    color=C["text"], zorder=6)
    ax.annotate("A", wh.pos[SHELF_A], ha="center", va="center", fontsize=9,
                fontweight="bold", color=C["store_e"], alpha=0.5, zorder=6)
    ax.annotate("W1", wh.pos[TARGET], ha="center", va="center", fontsize=7,
                fontweight="bold", color=C["del_e"], zorder=6)
    # Kept to plain words, the symbols (eta_1, d_obs, delta_1) are in the caption.
    handles = [
        Line2D([], [], color=C["accent"], lw=3, label="field of view"),
        Line2D([], [], marker="o", ls="", color=C["agent"], ms=11, label="agent"),
        Line2D([], [], marker="s", ls="", mfc=C["del_f"], mec=C["del_e"], ms=11,
               label="workstation"),
        # A letter, not a sample digit, so it cannot be read as a vertex value.
        Line2D([], [], ls="", marker=r"$\mathbf{n}$", color=C["accent"], ms=10,
               label="fewest steps from that vertex to W1"),
    ]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.01),
              ncol=2, frameon=False, fontsize=11)
    ax.set_aspect("equal"); ax.set_axis_off()
    fig.savefig(f"{OUT}/observation.png"); plt.close(fig)


if __name__ == "__main__":
    observation()
