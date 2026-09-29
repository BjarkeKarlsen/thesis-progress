"""
thesis-guide-images.md Section 13 ("Formal Decision Problem and Research
Question"): the factorial design -- controller architecture x storage mode
-- with an illustrative J value and whether adaptive F improves on F_fix in
each cell.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mp

from base import OUT, C

ROWS = ["centralised", "section-based", "decentralised"]
COLS = [r"$F_{\mathrm{fix}}$", "adaptive $F$"]
J = [[5.2, 4.6], [5.6, 4.9], [6.3, 5.1]]
IMPROVES = [False, True, True]  # adaptive beats fixed, per row


def decision_problem_grid():
    fig, ax = plt.subplots(figsize=(8.6, 5.6))
    cw, ch = 3.0, 1.6
    ax.set_xlim(-2.6, 2 * cw); ax.set_ylim(0, len(ROWS) * ch + 0.7)
    ax.axis("off")

    for r, row in enumerate(ROWS):
        y = (len(ROWS) - 1 - r) * ch
        ax.text(-0.25, y + ch / 2, row, ha="right", va="center", fontsize=11.5, color=C["text"])
        for c, col in enumerate(COLS):
            x = c * cw
            better = IMPROVES[r] and c == 1
            fc = C["store_f"] if better else "white"
            ax.add_patch(mp.FancyBboxPatch((x + 0.1, y + 0.1), cw - 0.2, ch - 0.2,
                                           boxstyle="round,pad=0.03", fc=fc, ec=C["node"], lw=1.3))
            mark = "$\\checkmark$ better" if better else ("worse" if c == 1 else "")
            ax.text(x + cw / 2, y + ch / 2 + 0.18, f"$\\mathcal{{J}}={J[r][c]}$",
                   ha="center", fontsize=11, color=C["text"])
            if mark:
                ax.text(x + cw / 2, y + ch / 2 - 0.28, mark, ha="center", fontsize=9.5,
                       color=C["store_e"] if better else C["node"])
    for c, col in enumerate(COLS):
        ax.text(c * cw + cw / 2, len(ROWS) * ch + 0.35, col, ha="center", fontsize=12, color=C["text"])

    ax.set_title(r"$(F^\star,\pi^\star) \in \arg\min_{F,\pi}\mathcal{J}(F,\pi)$"
                "\n(illustrative cell values)", fontsize=12.5, pad=18)
    fig.tight_layout()
    fig.savefig(f"{OUT}/decision_problem_grid.png"); plt.close(fig)


if __name__ == "__main__":
    decision_problem_grid()
