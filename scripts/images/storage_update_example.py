"""
thesis-guide-images.md Section 6 ("Storage Updates: Slow Feedback Loop"):
the D/K/R tradeoff terms the storage rule balances when deciding whether to
relocate a SKU. The before/after tea-relocation intuition itself is covered
separately by two_layer_feedback.py, so this figure is just the tradeoff,
not another warehouse map.
"""
import matplotlib.pyplot as plt

from base import OUT, C


def storage_update_example():
    fig, ax = plt.subplots(figsize=(5.0, 3.6))

    terms = ["$D$\naccess\ndistance", "$K$\ncongestion\nexposure", "$R$\nrelocation\ncost"]
    before = [3.0, 4.0, 0.0]
    after = [1.6, 1.2, 0.8]
    xs = range(len(terms))
    w = 0.35
    ax.bar([x - w / 2 for x in xs], before, width=w, color=C["edge"], label="before")
    ax.bar([x + w / 2 for x in xs], after, width=w, color=C["store_e"], label="after")
    ax.set_xticks(list(xs)); ax.set_xticklabels(terms, fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, fontsize=9)
    ax.set_title("Tradeoff terms of the storage objective", fontsize=10.5)

    fig.tight_layout()
    fig.savefig(f"{OUT}/storage_update_example.png"); plt.close(fig)


if __name__ == "__main__":
    storage_update_example()
