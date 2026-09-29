"""
thesis-guide-images.md Section 5 ("Storage State: Where Items Live"): the
worked example -- x_t(k,v) as a table, plus capacity used vs cap(v) per
vertex, computed from the table rather than hand-typed.
"""
import matplotlib.pyplot as plt
import numpy as np

from base import OUT, C

SKUS = ["tea", "coffee", "mugs"]
VERTS = ["A", "B", "C"]
X = np.array([[12, 0, 5], [4, 3, 0], [0, 6, 2]])  # rows=SKUS, cols=VERTS
B = np.array([1, 2, 1])       # per-unit footprint b_k
CAP = np.array([20, 15, 10])  # cap(v)


def storage_matrix():
    used = B @ X  # capacity used per vertex

    fig, (ax_t, ax_b) = plt.subplots(1, 2, figsize=(11.0, 4.2),
                                     gridspec_kw={"width_ratios": [1.15, 1]})

    ax_t.axis("off")
    tbl = ax_t.table(cellText=X.astype(str), rowLabels=SKUS,
                     colLabels=[f"${v}$" for v in VERTS],
                     cellLoc="center", rowLoc="center", loc="center")
    tbl.auto_set_font_size(False); tbl.set_fontsize(12); tbl.scale(1.0, 2.0)
    ax_t.set_title(r"$x_t(k,v)$: units of SKU $k$ at vertex $v$", fontsize=12, pad=14)

    xs = np.arange(len(VERTS))
    ax_b.bar(xs, CAP, color="white", edgecolor=C["node"], width=0.55, label="capacity")
    ax_b.bar(xs, used, color=C["store_f"], edgecolor=C["store_e"], width=0.55, label="used")
    for i, (u, c) in enumerate(zip(used, CAP)):
        ax_b.text(i, c + 0.6, f"{u}/{c}", ha="center", fontsize=10.5, color=C["text"])
    ax_b.set_xticks(xs); ax_b.set_xticklabels([f"${v}$" for v in VERTS])
    ax_b.set_ylim(0, max(CAP) * 1.25)
    ax_b.set_ylabel(r"$\sum_k b_k\, x(k,v)$ vs $\mathrm{cap}(v)$", fontsize=10.5)
    ax_b.spines[["top", "right"]].set_visible(False)
    ax_b.legend(frameon=False, fontsize=9.5, loc="upper right")
    ax_b.set_title("Capacity used per vertex (feasible)", fontsize=12)

    fig.suptitle("Feasible storage configuration under per-vertex capacity", fontsize=13)
    fig.tight_layout()
    fig.savefig(f"{OUT}/storage_matrix.png"); plt.close(fig)


if __name__ == "__main__":
    storage_matrix()
