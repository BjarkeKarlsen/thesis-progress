import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from base import OUT, C, draw_base


def instance_simple():
    """Figure 1 replacement: topology, directedness, and vertex roles only.

    No task route, no agents -- those are Sections III-B/III-D concepts the
    reader has not met yet at this point in the Problem Formulation.
    """
    fig, ax = plt.subplots(figsize=(12, 5.6))
    draw_base(ax)
    handles = [
        Line2D([], [], marker="o", ls="", mfc=C["store_f"], mec=C["store_e"], ms=12,
               label=r"storage $\mathcal{V}_{\mathrm{str}}$"),
        Line2D([], [], marker="s", ls="", mfc=C["del_f"], mec=C["del_e"], ms=12,
               label=r"delivery $\mathcal{V}_{\mathrm{del}}$"),
        Line2D([], [], marker="D", ls="", mfc=C["ep_f"], mec=C["ep_e"], ms=11,
               label=r"endpoint $\mathcal{V}_{\mathrm{ep}}$"),
        Line2D([], [], marker="o", ls="", mfc="white", mec=C["node"], ms=12,
               label="transit vertex"),
        Line2D([], [], color=C["accent"], lw=2.4, marker=">", markersize=9,
               label=r"one-way segment: $(v,w)\in E$, $(w,v)\notin E$"),
    ]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, 0.02),
              ncol=3, frameon=False, fontsize=11)
    ax.set_aspect("equal"); ax.set_axis_off()
    fig.savefig(f"{OUT}/instance_simple.png"); plt.close(fig)


if __name__ == "__main__":
    instance_simple()
