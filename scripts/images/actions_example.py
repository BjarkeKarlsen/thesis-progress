"""
thesis-guide-images.md Section 3 ("Actions: Wait or Move"): the local action
set U(A) = {wait} u {move(w) : w in N+(A)} at a vertex A with two outgoing
edges, each annotated with its one-step cost.
"""
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mp

from base import OUT, C

POS = {"A": (0.0, 0.0), "B": (3.2, 1.6), "C": (3.2, -1.6)}
COST_AB, COST_AC, COST_WAIT = 1.0, 1.5, 0.5


def _label_off_line(p0, p1, offset, t=0.5):
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    length = math.hypot(dx, dy)
    nx_, ny_ = -dy / length, dx / length
    mx, my = p0[0] + t * dx, p0[1] + t * dy
    angle = math.degrees(math.atan2(dy, dx))
    return mx + nx_ * offset, my + ny_ * offset, angle


def actions_example():
    fig, ax = plt.subplots(figsize=(9.4, 5.6))
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-2.6, 5.2); ax.set_ylim(-2.6, 2.6)

    A = dict(arrowstyle="-|>", lw=2.4, color=C["text"])
    ax.annotate("", xy=POS["B"], xytext=POS["A"], arrowprops=A)
    ax.annotate("", xy=POS["C"], xytext=POS["A"], arrowprops=A)

    lx, ly, ang = _label_off_line(POS["A"], POS["B"], 0.32)
    ax.text(lx, ly, f"$\\mathrm{{move}}(B)$: cost $c(A,B)={COST_AB}$",
           ha="center", va="center", fontsize=11, color=C["text"], rotation=ang,
           rotation_mode="anchor")
    lx, ly, ang = _label_off_line(POS["A"], POS["C"], -0.32)
    ax.text(lx, ly, f"$\\mathrm{{move}}(C)$: cost $c(A,C)={COST_AC}$",
           ha="center", va="center", fontsize=11, color=C["text"], rotation=ang,
           rotation_mode="anchor")

    # wait self-loop: small arc to the left of A plus its own arrowhead
    loop_c = (POS["A"][0] - 0.55, POS["A"][1])
    ax.add_patch(mp.Arc(loop_c, 0.7, 0.9, theta1=290, theta2=250, lw=2.0, color=C["accent"]))
    ax.annotate("", xy=(loop_c[0] - 0.18, loop_c[1] + 0.42), xytext=(loop_c[0] - 0.10, loop_c[1] + 0.47),
               arrowprops=dict(arrowstyle="-|>", lw=2.0, color=C["accent"]))
    ax.text(loop_c[0] - 0.55, loop_c[1], f"$\\mathrm{{wait}}$:\ncost $c_{{\\mathrm{{wait}}}}={COST_WAIT}$",
           ha="right", va="center", fontsize=11, color=C["accent"])

    ax.scatter(*POS["A"], s=650, c=C["agent"], edgecolors="white", linewidths=1.6, zorder=5)
    for n in ("B", "C"):
        ax.scatter(*POS[n], s=650, c=C["store_f"], edgecolors=C["store_e"], linewidths=1.6, zorder=5)
    ax.annotate("$A$", POS["A"], textcoords="offset points", xytext=(0, -26),
               ha="center", fontsize=13, color=C["agent"])
    ax.annotate("$B$", POS["B"], textcoords="offset points", xytext=(0, 22),
               ha="center", fontsize=13, color=C["store_e"])
    ax.annotate("$C$", POS["C"], textcoords="offset points", xytext=(0, -26),
               ha="center", fontsize=13, color=C["store_e"])

    ax.text(0.0, 2.35, r"$N^{+}(A) = \{B, C\}$, so"
           r"  $\mathcal{U}(A) = \{\mathrm{wait}, \mathrm{move}(B), \mathrm{move}(C)\}$",
           ha="center", fontsize=12.5, color=C["text"])

    ax.set_title("The local action set at a vertex", fontsize=13, pad=14)
    fig.tight_layout()
    fig.savefig(f"{OUT}/actions_example.png"); plt.close(fig)


if __name__ == "__main__":
    actions_example()
