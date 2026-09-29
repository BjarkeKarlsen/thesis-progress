"""
thesis-guide-images.md Section 10 ("The Learning Problem: POSG View"): state
-> per-agent observation -> shared policy -> joint action -> dynamics ->
next state, closing the loop.
"""
import matplotlib.pyplot as plt

from base import OUT, C
from flow import box, arrow


def posg_schematic():
    fig, ax = plt.subplots(figsize=(11.6, 5.2))
    ax.set_xlim(0, 12.4); ax.set_ylim(-0.5, 4.6); ax.axis("off")

    s_t = box(ax, 1.4, 2.5, 2.0, 1.3, "state\n$s_t$", "#f6e7c1", C["text"])
    obs = box(ax, 4.4, 2.5, 2.3, 1.3, "observations\n$o_i(t) = O_i(s_t)$", C["store_f"], C["text"])
    pol = box(ax, 7.5, 2.5, 2.3, 1.3, "shared policy\n$\\pi_\\theta(\\cdot\\mid o_i(t))$", C["ep_f"], C["text"])
    act = box(ax, 10.5, 2.5, 1.6, 1.3, "actions\n$u_i(t)$", "#f7d6d6", C["text"])
    dyn = box(ax, 5.9, 0.6, 3.4, 1.3, "dynamics\n$s_{t+1}\\sim P(\\cdot\\mid s_t, u_t)$", "#e4d9f0", C["text"])

    arrow(ax, s_t, "right", obs, "left", C["text"])
    arrow(ax, obs, "right", pol, "left", C["text"])
    arrow(ax, pol, "right", act, "left", C["text"])
    arrow(ax, act, "bottom", dyn, "right", C["text"], rad=0.25)
    arrow(ax, dyn, "left", s_t, "bottom", C["agent"], rad=-0.25, label="next $t$",
         label_color=C["agent"])

    ax.text(6.0, 4.2, "$\\mathcal{M} = (\\mathcal{A}, \\mathcal{S}, \\{\\mathcal{U}_i\\}, "
           "P, \\{\\mathcal{O}_i\\}, \\{O_i\\}, \\{R_i\\}, \\gamma)$",
           ha="center", fontsize=12, color=C["text"])
    ax.set_title("The POSG view: one environment timestep", fontsize=13, pad=16)
    fig.tight_layout()
    fig.savefig(f"{OUT}/posg_schematic.png"); plt.close(fig)


if __name__ == "__main__":
    posg_schematic()
