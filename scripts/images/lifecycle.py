import matplotlib.pyplot as plt

from base import OUT, C


def lifecycle():
    """
    Colors are chosen to match fig:taskroute (instance.py), not just to
    look distinct: pickup uses the storage-vertex blue (C["store_e"]),
    finish uses the delivery-vertex orange (C["del_e"]), assignment uses
    the agent's own red (C["agent"]). Released has no vertex of its own,
    so it gets the one role color unused elsewhere (C["comm"]). The two
    figures then share one color language instead of two clashing ones.
    Concrete values are those of the running example tau_1 (see
    tab:tau1timeline / the instance.py route): released=5, assigned=9,
    pickup=11, finish=14.
    """
    fig, ax = plt.subplots(figsize=(12, 3.9))
    ax.set_xlim(0, 10); ax.set_ylim(0, 3.4); ax.axis("off")
    ax.annotate("", xy=(9.7, 1.25), xytext=(0.3, 1.25),
                arrowprops=dict(arrowstyle="-|>", lw=2.2, color=C["text"]))
    ax.text(9.75, 1.05, "$t$", fontsize=13)
    events = [
        (1.2, r"$t_j^{\mathrm{released}}$", "release", "$t=5$", C["comm"]),
        (3.6, r"$t_j^{\mathrm{assigned}}$", "assignment", "$t=9$", C["agent"]),
        (5.6, r"$t_j^{\mathrm{pickup}}$", r"pickup at $s_j$", "$t=11$", C["store_e"]),
        (8.8, r"$t_j^{\mathrm{finish}}$", r"delivery at $g_j$", "$t=14$", C["del_e"]),
    ]
    for x, sym, word, val, col in events:
        ax.plot([x, x], [1.02, 1.48], lw=3.2, color=col)
        ax.annotate(sym + "\n" + word, (x, 1.58), ha="center", fontsize=12, color=col)
        ax.annotate(val, (x, 0.92), ha="center", fontsize=11, color=col)

    def span(x0, x1, y, lab, col):
        ax.annotate("", xy=(x1, y), xytext=(x0, y),
                    arrowprops=dict(arrowstyle="<->", lw=2.0, color=col))
        ax.text((x0 + x1) / 2, y - 0.33, lab, ha="center", fontsize=12, color=col)

    span(1.2, 3.6, 0.55, r"$\tau_j\in\mathcal{Q}_t$  (waiting)", C["comm"])
    span(3.6, 8.8, 0.55, r"$\tau_j\in\mathcal{B}_t$  (active)", C["agent"])
    span(1.2, 8.8, 2.85, r"service time $\zeta_j=t_j^{\mathrm{finish}}-t_j^{\mathrm{released}}=9$", C["text"])
    ax.text(9.15, 0.22, r"$\tau_j\in\mathcal{C}_t$", fontsize=12, color=C["del_e"])
    fig.savefig(f"{OUT}/lifecycle.png"); plt.close(fig)


if __name__ == "__main__":
    lifecycle()
