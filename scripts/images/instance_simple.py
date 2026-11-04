import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from base import OUT, C
from m8 import Warehouse


def instance_simple():
    """The whole 8-agent warehouse (m8.py), the first one the reader meets
    (fig:instance). Every role vertex is a leaf off the aisles ([A47] [A70]), and
    the central pair of lanes is the one-way loop ([A74])."""
    wh = Warehouse()
    fig, ax = plt.subplots(figsize=(10, 7.2))
    wh.draw(ax, node_scale=0.55)
    handles = wh.legend_handles() + [
        Line2D([], [], marker=">", ls="-", color=C["node"], lw=1.4, ms=7,
               label="one-way edge"),
    ]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.01),
              ncol=3, frameon=False, fontsize=12)
    ax.set_aspect("equal"); ax.set_axis_off()
    fig.savefig(f"{OUT}/instance_simple.png"); plt.close(fig)


if __name__ == "__main__":
    instance_simple()
