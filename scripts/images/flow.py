"""
Shared helper for the box-and-arrow "pipeline" figures (methodloop_simple,
architecture_simple, ...): boxes are placed by centre + size, and arrows are
always drawn edge-to-edge between two boxes so nothing has to be hand-tuned
in absolute coordinates -- the usual source of mismatched/overlapping
arrows when box positions change later.
"""
import matplotlib.patches as mp

SIDES = {
    "right": lambda b: (b["cx"] + b["w"] / 2, b["cy"]),
    "left": lambda b: (b["cx"] - b["w"] / 2, b["cy"]),
    "top": lambda b: (b["cx"], b["cy"] + b["h"] / 2),
    "bottom": lambda b: (b["cx"], b["cy"] - b["h"] / 2),
}


def box(ax, cx, cy, w, h, text, color, ec, fontsize=10):
    ax.add_patch(mp.FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                                   boxstyle="round,pad=0.12", fc=color, ec=ec, lw=1.5))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fontsize)
    return {"cx": cx, "cy": cy, "w": w, "h": h}


def arrow(ax, b_from, side_from, b_to, side_to, color, lw=2.0, rad=0.0, label=None,
          label_color=None, label_dy=0.18):
    p1, p2 = SIDES[side_from](b_from), SIDES[side_to](b_to)
    ax.annotate("", xy=p2, xytext=p1,
               arrowprops=dict(arrowstyle="-|>", lw=lw, color=color,
                                connectionstyle=f"arc3,rad={rad}",
                                shrinkA=2, shrinkB=2))
    if label:
        mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
        ax.text(mx, my + label_dy, label, ha="center", fontsize=9.5,
               color=label_color or color)
