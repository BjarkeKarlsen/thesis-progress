import matplotlib.pyplot as plt
import matplotlib.patches as mp

from base import OUT, C


def conflicts():
    P = {"u": (0, 0), "v": (1, 0), "w": (2, 0)}
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.2))

    def panel(ax, title, names):
        ax.set_xlim(-0.5, 2.5); ax.set_ylim(-1.5, 1.0)
        ax.set_aspect("equal"); ax.axis("off")
        ax.text(1.0, 0.85, title, ha="center", fontsize=13)
        for a, b in zip(names, names[1:]):
            ax.plot([P[a][0], P[b][0]], [0, 0], color=C["edge"], lw=2.0, zorder=1)
        for n in names:
            ax.add_patch(plt.Circle(P[n], 0.16, fc="white", ec=C["node"], lw=1.8, zorder=3))
            ax.text(P[n][0], P[n][1] - 0.34, n, ha="center", fontsize=12)

    def ag(ax, n, lab, col):
        ax.scatter(*P[n], s=200, c=col, zorder=5)
        ax.text(P[n][0], P[n][1] + 0.28, lab, ha="center", fontsize=13, color=col)

    def arr(ax, x0, x1, y, col):
        ax.annotate("", xy=(x1, y), xytext=(x0, y),
                    arrowprops=dict(arrowstyle="-|>", lw=2.4, color=col))

    ax = axes[0]; panel(ax, "(a) vertex conflict", ("u", "v", "w"))
    ag(ax, "u", "$a_i$", C["agent"]); ag(ax, "w", "$a_j$", C["accent"])
    arr(ax, 0.05, 0.85, -0.7, C["agent"]); arr(ax, 1.95, 1.15, -0.7, C["accent"])
    ax.text(1.0, -1.25, r"$\ell_i(t{+}1)=\ell_j(t{+}1)$", ha="center", fontsize=12.5)

    ax = axes[1]; panel(ax, "(b) swap conflict", ("u", "v"))
    ag(ax, "u", "$a_i$", C["agent"]); ag(ax, "v", "$a_j$", C["accent"])
    arr(ax, 0.05, 0.95, -0.62, C["agent"]); arr(ax, 0.95, 0.05, -0.92, C["accent"])
    ax.text(1.0, -1.32, r"$\ell_i(t)=\ell_j(t{+}1)\ \wedge\ \ell_j(t)=\ell_i(t{+}1)$",
            ha="center", fontsize=11.5)

    ax = axes[2]; panel(ax, "(c) feasible joint transition", ("u", "v", "w"))
    ag(ax, "u", "$a_i$", C["agent"]); ag(ax, "w", "$a_j$", C["accent"])
    arr(ax, 0.05, 0.85, -0.7, C["agent"])
    ax.add_patch(mp.Arc((2.0, -0.7), 0.42, 0.42, theta1=200, theta2=520,
                        lw=2.2, color=C["accent"]))
    ax.annotate("", xy=(1.72, -0.60), xytext=(1.78, -0.64),
                arrowprops=dict(arrowstyle="-|>", lw=2.2, color=C["accent"]))
    ax.text(2.0, -1.25, r"$a_j$ waits, cost $c_{\mathrm{wait}}$",
            ha="center", fontsize=12.5, color=C["accent"])
    fig.savefig(f"{OUT}/conflicts.png"); plt.close(fig)
