import matplotlib.pyplot as plt

from base import OUT, C


def lifecycle():
    fig, ax = plt.subplots(figsize=(12, 3.6))
    ax.set_xlim(0, 10); ax.set_ylim(0, 3.2); ax.axis("off")
    ax.annotate("", xy=(9.7, 1.25), xytext=(0.3, 1.25),
                arrowprops=dict(arrowstyle="-|>", lw=2.2, color=C["text"]))
    ax.text(9.75, 1.05, "$t$", fontsize=13)
    for x, lab, col in [(1.2, "$r_j$\nrelease", C["accent"]),
                        (3.6, "assignment", C["del_e"]),
                        (5.6, r"pickup at $s_j$", C["ep_e"]),
                        (8.8, r"$d_j$ delivery at $g_j$", C["agent"])]:
        ax.plot([x, x], [1.02, 1.48], lw=3.2, color=col)
        ax.annotate(lab, (x, 1.58), ha="center", fontsize=12, color=col)

    def span(x0, x1, y, lab, col):
        ax.annotate("", xy=(x1, y), xytext=(x0, y),
                    arrowprops=dict(arrowstyle="<->", lw=2.0, color=col))
        ax.text((x0 + x1) / 2, y - 0.33, lab, ha="center", fontsize=12, color=col)

    span(1.2, 3.6, 0.80, r"$\tau_j\in\mathcal{Q}_t$  (waiting)", C["accent"])
    span(3.6, 8.8, 0.80, r"$\tau_j\in\mathcal{B}_t$  (active)", C["del_e"])
    span(1.2, 8.8, 2.55, r"service time $\zeta_j=d_j-r_j$", C["text"])
    ax.text(9.15, 0.47, r"$\tau_j\in\mathcal{C}_T$", fontsize=12, color=C["ep_e"])
    fig.savefig(f"{OUT}/lifecycle.png"); plt.close(fig)
