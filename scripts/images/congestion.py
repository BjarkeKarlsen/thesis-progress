import matplotlib.pyplot as plt
import matplotlib.patches as mp

from base import OUT, C, G, POS, draw_base

ZONE = {n for n in G if int(n.split("_")[1]) <= 4}  # illustrative Y_q: columns 0-4


def congestion():
    """eq:occupancy: one instrument, delta(S,t;excl), at each architecture's window."""
    fig, axes = plt.subplots(1, 3, figsize=(15.5, 3.3))
    agents = {"4_0": "$a_1$", "2_4": "$a_2$", "0_6": "$a_3$"}

    def scatter_agents(ax, extra=(), dim_out=()):
        for n, lab in agents.items():
            faded = n in dim_out
            ax.scatter(*POS[n], s=220, c=C["agent"], zorder=5,
                       alpha=0.3 if faded else 1.0, edgecolors="white", linewidths=1.1)
            ax.annotate(lab, POS[n], textcoords="offset points", xytext=(0, 15),
                        ha="center", fontsize=12, color=C["agent"],
                        alpha=0.3 if faded else 1.0)
        for n in extra:
            ax.scatter(*POS[n], s=150, c=C["agent"], zorder=5,
                       edgecolors="white", linewidths=1.0)

    # (a) centralised -- S = V_mov, excl = empty: every agent counts
    ax = axes[0]
    draw_base(ax)
    xs = [POS[n][0] for n in G]; ys = [POS[n][1] for n in G]
    pad = 0.7
    ax.add_patch(mp.FancyBboxPatch((min(xs) - pad, min(ys) - pad),
                                   max(xs) - min(xs) + 2 * pad,
                                   max(ys) - min(ys) + 2 * pad,
                                   boxstyle="round,pad=0", fc=C["accent"], alpha=0.08,
                                   ec="none", zorder=0))
    scatter_agents(ax)
    ax.set_title("(a) centralised", fontsize=13)
    ax.text(0.5, -0.08, r"$S=V_{\mathrm{mov}}$, excl$=\emptyset$: all 3 count",
            transform=ax.transAxes, ha="center", fontsize=11.5, color=C["accent"])

    # (b) section-based -- S = one zone Y_q, excl = empty: only in-zone agents count
    ax = axes[1]
    draw_base(ax)
    zxs = [POS[n][0] for n in ZONE]; zys = [POS[n][1] for n in ZONE]
    ax.add_patch(mp.FancyBboxPatch((min(zxs) - 0.55, min(zys) - 0.6),
                                   max(zxs) - min(zxs) + 1.1,
                                   max(zys) - min(zys) + 1.2,
                                   boxstyle="round,pad=0", fc=C["accent"], alpha=0.14,
                                   ec=C["accent"], lw=1.4, ls="--", zorder=0))
    scatter_agents(ax, dim_out={"0_6"})
    ax.text(min(zxs) + 0.25, max(zys) - 0.35, "$Y_q$", ha="left", va="top",
            fontsize=13, color=C["accent"])
    ax.set_title("(b) section-based", fontsize=13)
    ax.text(0.5, -0.08, r"$S=Y_q$, excl$=\emptyset$: $a_1,a_2$ count, $a_3$ doesn't",
            transform=ax.transAxes, ha="center", fontsize=11.5, color=C["accent"])

    # (c) decentralised -- S = one agent's local window, excl = {that agent}
    ax = axes[2]
    draw_base(ax, dim=True)
    ego = "2_4"
    ax.add_patch(plt.Circle(POS[ego], 1.55, fill=True, fc=C["accent"], alpha=0.10,
                            ec=C["accent"], lw=2.0, ls=(0, (2, 3)), zorder=1))
    scatter_agents(ax, extra=("1_4",), dim_out={"4_0", "0_6"})
    ax.set_title("(c) decentralised", fontsize=13)
    ax.text(0.5, -0.08,
            r"$S=V^{(r_{\mathrm{cng}})}_i(t)$, excl$=\{a_i\}$: only the nearby dot"
            " counts",
            transform=ax.transAxes, ha="center", fontsize=11.5, color=C["accent"])

    for ax in axes:
        ax.set_aspect("equal"); ax.set_axis_off()
    fig.suptitle(r"$\delta(S,t;\mathrm{excl})$: one instrument, evaluated at each "
                 "architecture's own window", fontsize=13, y=1.1)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(f"{OUT}/congestion.png"); plt.close(fig)
