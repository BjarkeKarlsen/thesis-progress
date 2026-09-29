"""
The six-stage environment step: fills the fig:methodloop placeholder still
marked "[Figure: ...]" in 4.Implementation.tex. Stages 1,2,4,5,6 are shared
by every controller; only stage 3 (routing) swaps between the three
architectures of Table tab:information.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mp

from base import OUT, C
from flow import box, arrow

BOXES = [
    ("orders", 1.7, 4.6, 2.6, 1.4, "1. Orders $\\to$ tasks\nnew task enters the queue", "#f6e7c1"),
    ("assign", 4.9, 4.6, 2.6, 1.4, "2. Task assignment\n(shared by all controllers)", C["store_f"]),
    ("route", 8.1, 4.6, 2.8, 1.4, "3. Routing\none proposed move per agent\n(controller-specific)", C["ep_f"]),
    ("resolve", 8.1, 1.4, 2.8, 1.4, "4. Conflict resolution\npriority-order override", "#f7d6d6"),
    ("step", 4.9, 1.4, 2.6, 1.4, "5. Environment step\nmove agents, update state, log", C["del_f"]),
    ("storage", 1.7, 1.4, 2.6, 1.4, "6. Storage epoch\n(only on storage-epoch steps)", C["store_f"]),
]

INSERTS = ["centralised", "section-based", "decentralised"]


def methodloop_simple():
    fig, ax = plt.subplots(figsize=(11.6, 5.8))
    ax.set_xlim(0, 10.2); ax.set_ylim(0, 6.2); ax.axis("off")

    b = {}
    for key, cx, cy, w, h, txt, col in BOXES:
        b[key] = box(ax, cx, cy, w, h, txt, col, C["text"], fontsize=10.5)

    # interchangeable inserts at stage 3, stacked inside the bottom of the box
    x0, y0 = b["route"]["cx"] - b["route"]["w"] / 2, b["route"]["cy"] - b["route"]["h"] / 2
    iw = b["route"]["w"] / 3
    for k, name in enumerate(INSERTS):
        ax.add_patch(mp.FancyBboxPatch((x0 + k * iw + 0.06, y0 + 0.1), iw - 0.12, 0.4,
                                       boxstyle="round,pad=0.03", fc="white",
                                       ec=C["accent"], lw=1.1))
        ax.text(x0 + (k + 0.5) * iw, y0 + 0.3, name, ha="center", va="center", fontsize=7.4)

    arrow(ax, b["orders"], "right", b["assign"], "left", C["text"])
    arrow(ax, b["assign"], "right", b["route"], "left", C["text"])
    arrow(ax, b["route"], "bottom", b["resolve"], "top", C["text"])
    arrow(ax, b["resolve"], "left", b["step"], "right", C["text"])
    arrow(ax, b["step"], "left", b["storage"], "right", C["text"])
    arrow(ax, b["storage"], "top", b["orders"], "bottom", C["agent"], rad=-0.4,
          label="next timestep", label_color=C["agent"], label_dy=0.0)

    ax.set_title("The environment step: stages 1, 2, 4, 5, 6 shared; stage 3 swaps controller",
                 fontsize=11.5)
    fig.tight_layout()
    fig.savefig(f"{OUT}/methodloop_simple.png"); plt.close(fig)


if __name__ == "__main__":
    methodloop_simple()
