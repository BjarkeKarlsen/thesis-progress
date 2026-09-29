import matplotlib.pyplot as plt

from base import OUT, C
from mini import mini_graph, draw_mini, put_agent


def joint_action():
    """
    Illustrates pi^route: information -> u_t = (u_1(t),...,u_m(t)), one
    simultaneous joint action, not a sequence of per-agent moves. Three
    agents on one small grid at a single timestep t: two move (a
    highlighted arrow, agent color), one waits (a dashed ring), and the
    resulting joint action tuple is written out directly underneath.
    """
    G, POS = mini_graph(rows=3, cols=4)
    fig, ax = plt.subplots(figsize=(8, 5.2))
    draw_mini(ax, G, POS)

    # (start vertex, target vertex or None if waiting, action)
    agents = {
        "a_1": ("1_0", "1_1", "move"),
        "a_2": ("0_2", None, "wait"),
        "a_3": ("2_3", "2_2", "move"),
    }

    for label, (node, target, action) in agents.items():
        put_agent(ax, POS, node, f"${label}$")
        if action == "move":
            x0, y0 = POS[node]
            x1, y1 = POS[target]
            ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                       arrowprops=dict(arrowstyle="-|>", lw=3.2, color=C["agent"],
                                       shrinkA=15, shrinkB=15))
        else:
            x0, y0 = POS[node]
            ring = plt.Circle((x0, y0), 0.24, fill=False, ls=(0, (3, 2)),
                              lw=1.8, color=C["agent"])
            ax.add_patch(ring)
            ax.annotate("wait", (x0, y0), textcoords="offset points",
                       xytext=(0, -28), ha="center", fontsize=9.5, color=C["agent"])

    ax.set_aspect("equal"); ax.set_axis_off()

    lines = ["Joint action at $t$", "",
            r"$u_t = (u_1(t),\, u_2(t),\, u_3(t))$",
            r"$= (\mathrm{move},\, \mathrm{wait},\, \mathrm{move})$"]
    ax.text(0.5, -0.05, "\n".join(lines), transform=ax.transAxes, va="top",
           ha="center", fontsize=11, linespacing=1.7,
           bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor=C["agent"]))

    fig.savefig(f"{OUT}/joint_action.png"); plt.close(fig)


if __name__ == "__main__":
    joint_action()
