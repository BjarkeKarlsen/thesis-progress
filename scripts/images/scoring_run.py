"""
thesis-guide-images.md Section 12 ("Scoring a Run"): a histogram of
per-task service times and a bar comparison of run-level metrics across two
illustrative conditions. Fixed, hand-picked numbers -- not a real
experiment -- so the figure is reproducible without a simulator run.
"""
import matplotlib.pyplot as plt

from base import OUT, C

# Illustrative per-task service times (not from a real run).
ZETA = [5, 6, 6, 7, 7, 7, 8, 8, 8, 8, 9, 9, 10, 10, 11, 12, 13, 15, 18, 22]

METRICS = [r"$\bar\zeta_T$", r"$\bar c_T$", r"$C_T$", r"$B_T$"]
FIXED = [11.5, 62.0, 0.62, 14.0]
ADAPTIVE = [9.0, 50.0, 0.41, 8.0]


def scoring_run():
    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(11.5, 4.2))

    ax0.hist(ZETA, bins=range(4, 24, 2), color=C["store_f"], edgecolor=C["store_e"])
    ax0.set_xlabel(r"service time $\zeta_j$ (timesteps)", fontsize=10.5)
    ax0.set_ylabel("number of completed tasks", fontsize=10.5)
    ax0.spines[["top", "right"]].set_visible(False)
    ax0.set_title(r"Distribution of $\zeta_j$ over $\mathcal{C}_T$", fontsize=11.5)

    # Metrics live on different scales (c_bar ~ tens, C_T in [0,1]), so
    # compare relative change vs F_fix instead of raw mixed-scale bars.
    pct_change = [100 * (a - f) / f for f, a in zip(FIXED, ADAPTIVE)]
    xs = range(len(METRICS))
    bars = ax1.bar(xs, pct_change, width=0.5, color=C["store_e"])
    for x, p in zip(xs, pct_change):
        ax1.text(x, p + 2.0, f"{p:+.0f}%", ha="center", va="bottom", fontsize=10, color=C["text"])
    ax1.set_ylim(min(pct_change) - 6, 4)
    ax1.axhline(0, color=C["edge"], lw=1.0)
    ax1.set_xticks(list(xs)); ax1.set_xticklabels(METRICS, fontsize=11)
    ax1.set_ylabel("change vs $F_{\\mathrm{fix}}$ (%)", fontsize=10.5)
    ax1.spines[["top", "right"]].set_visible(False)
    ax1.set_title("Adaptive $F$ vs $F_{\\mathrm{fix}}$, relative change\n(illustrative values)", fontsize=11.5)

    fig.suptitle("Scoring a run", fontsize=13)
    fig.tight_layout()
    fig.savefig(f"{OUT}/scoring_run.png"); plt.close(fig)


if __name__ == "__main__":
    scoring_run()
