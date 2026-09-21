import matplotlib.pyplot as plt
import matplotlib.patches as mp

from base import OUT, C


def _draw_loop_panel(ax, feedback):
    """One panel of the loop: feedback=True is the coupled model, False is F_fix."""
    ax.set_xlim(0, 12); ax.set_ylim(0, 6.4); ax.axis("off")
    storage_txt = (
        "Storage layer  $F$\nslow: every $\\Delta$ steps\n"
        "$x_t=F(x_{t-\\Delta},\\hat\\rho_t,\\hat\\mu_t,\\hat w_t)$"
        if feedback else
        "Storage layer  $F_{\\mathrm{fix}}$\n$F_{\\mathrm{fix}}(x,\\cdot)=x$\n"
        "ignores the estimates below"
    )
    boxes = [
        (0.5, 4.0, 3.2, 1.5, storage_txt, C["store_f"]),
        (4.4, 4.0, 3.2, 1.5, "Task generation\n$\\tau_j=(r_j,s_j,g_j)$\n"
                             "pickup $s_j$ drawn from $x_t$", "#f6e7c1"),
        (8.3, 4.0, 3.2, 1.5, "MAPD controller  $\\pi$\nfast: every timestep\n"
                             "assignment + collision-free routing", C["ep_f"]),
        (4.4, 0.8, 3.2, 1.4, "Causal traffic estimate\n"
                             "$\\hat\\mu_t(e),\\ \\hat w_t(e),\\ \\hat\\rho_t$", "#f7d6d6"),
    ]
    for x, y, w, h, txt, col in boxes:
        ax.add_patch(mp.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.14",
                                       fc=col, ec=C["text"], lw=1.5))
        ax.text(x + w / 2, y + h / 2, txt, ha="center", va="center", fontsize=11.5)
    A = dict(arrowstyle="-|>", lw=2.0, color=C["text"])
    ax.annotate("", xy=(4.4, 4.75), xytext=(3.7, 4.75), arrowprops=A)
    ax.annotate("", xy=(8.3, 4.75), xytext=(7.6, 4.75), arrowprops=A)
    red = lambda rad: dict(arrowstyle="-|>", lw=2.0, color=C["agent"],
                           connectionstyle=f"arc3,rad={rad}")
    ax.annotate("", xy=(7.6, 1.5), xytext=(9.9, 4.0), arrowprops=red(0.2))
    ax.text(9.4, 2.5, "measure", color=C["agent"], fontsize=12)
    if feedback:
        ax.annotate("", xy=(2.1, 4.0), xytext=(4.4, 1.5), arrowprops=red(0.2))
        ax.text(1.6, 2.5, "feedback\n(slow loop)", color=C["agent"], fontsize=12,
                ha="center")
    else:
        # Genuine absence, not a ghosted arrow -- nothing is drawn between the
        # stats box and the storage box, because under F_fix nothing connects them.
        ax.text(1.9, 2.5, "no feedback:\n$x_t$ held fixed", color=C["node"],
                fontsize=12, ha="center", style="italic")
    ax.text(6.0, 5.95, "fast loop: one environment timestep",
            fontsize=11, ha="center", color=C["text"])


def loop():
    # Each panel keeps the same 12-in-wide scale the original single-panel
    # version used (1 data unit = 1 in) -- halving the width without shrinking
    # the boxes/font is what caused the earlier text-overflow bug.
    fig, axes = plt.subplots(1, 2, figsize=(24.0, 5.3))
    _draw_loop_panel(axes[0], feedback=False)
    axes[0].set_title(r"(b) $F_{\mathrm{fix}}$ baseline — feedback removed",
                      fontsize=13)
    _draw_loop_panel(axes[1], feedback=True)
    axes[1].set_title("(a) adaptive storage — this thesis's coupled model",
                      fontsize=13)
    
    fig.tight_layout()
    fig.savefig(f"{OUT}/loop.png"); plt.close(fig)
