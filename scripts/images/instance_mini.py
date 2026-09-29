"""
Simple companion to instance.py / instance_simple.py (sec:pf:env,
Figure fig:instance): the same four vertex roles and the same
directedness point, on an 8-vertex graph instead of the full 5x9
warehouse, so the roles are the only thing left to read.
"""
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from base import OUT, C
from mini import mini_graph, draw_mini

STORAGE = ["1_2"]
DELIVERY = ["0_0"]
ENDPOINTS = ["1_3"]
ONE_WAY = ("0_1", "0_2")  # allowed direction only: 0_1 -> 0_2


def instance_mini():
    G, pos = mini_graph(rows=2, cols=4, one_way=ONE_WAY)
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    draw_mini(ax, G, pos, storage=STORAGE, delivery=DELIVERY, endpoints=ENDPOINTS)
    handles = [
        Line2D([], [], marker="o", ls="", mfc=C["store_f"], mec=C["store_e"], ms=11,
               label=r"storage $V_{\mathrm{str}}$"),
        Line2D([], [], marker="s", ls="", mfc=C["del_f"], mec=C["del_e"], ms=11,
               label=r"delivery $V_{\mathrm{del}}$"),
        Line2D([], [], marker="D", ls="", mfc=C["ep_f"], mec=C["ep_e"], ms=10,
               label=r"endpoint $V_{\mathrm{ep}}$"),
        Line2D([], [], marker="o", ls="", mfc="white", mec=C["node"], ms=11,
               label="transit vertex"),
        Line2D([], [], color=C["accent"], lw=2.2, marker=">", markersize=8,
               label=r"$(v,w)\in E$, $(w,v)\notin E$"),
    ]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.02),
              ncol=3, frameon=False, fontsize=10)
    ax.set_aspect("equal"); ax.set_axis_off()
    fig.savefig(f"{OUT}/instance_mini.png"); plt.close(fig)


if __name__ == "__main__":
    instance_mini()
