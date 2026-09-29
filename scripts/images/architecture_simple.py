"""
Per-agent model architecture: fills the fig:architecture placeholder still
marked "[Figure: ...]" in 4.Implementation.tex. Shows the pipeline local
observation + incoming messages -> Q rounds of message passing -> readout
z_i -> FC+ReLU -> masked policy head / value head, without expanding Q into
repeated boxes -- the loop-back arrow labelled "x Q" carries that instead,
so the figure stays legible at a glance.
"""
import matplotlib.pyplot as plt

from base import OUT, C
from flow import box, arrow

def architecture_simple():
    fig, ax = plt.subplots(figsize=(12.8, 5.0))
    ax.set_xlim(0, 13.2); ax.set_ylim(0, 5.4); ax.axis("off")

    obs = box(ax, 1.6, 3.7, 2.9, 1.5, "local observation\nfeatures per visible vertex", C["store_f"], C["text"])
    msg = box(ax, 1.6, 1.3, 2.9, 1.5, "incoming messages\nfrom nearby agents", C["ep_f"], C["text"])
    mp_ = box(ax, 5.4, 2.5, 2.9, 1.7, "message passing\n$Q$ rounds", C["del_f"], C["text"])
    ro = box(ax, 9.0, 2.5, 2.7, 1.7, "readout $z_i$\nown state $\\Vert$ aggregated\nmessages $\\Vert$ congestion", "#f6e7c1", C["text"])
    fc = box(ax, 12.0, 3.5, 2.2, 1.0, "FC + ReLU", "white", C["text"])
    pol = box(ax, 11.5, 1.1, 1.4, 1.4, "masked\npolicy head", "#f7d6d6", C["text"])
    val = box(ax, 13.0, 1.1, 1.4, 1.4, "value\nhead", "#e4d9f0", C["text"])
    ax.set_xlim(0, 14.4)

    arrow(ax, obs, "right", mp_, "left", C["text"], rad=0.15)
    arrow(ax, msg, "right", mp_, "left", C["text"], rad=-0.15)
    arrow(ax, mp_, "right", ro, "left", C["text"])
    arrow(ax, ro, "right", fc, "left", C["text"], rad=-0.15)
    arrow(ax, fc, "bottom", pol, "top", C["text"], rad=0.15)
    arrow(ax, fc, "bottom", val, "top", C["text"], rad=-0.15)

    lx, ly = mp_["cx"], mp_["cy"] + mp_["h"] / 2 + 0.3
    ax.annotate("", xy=(lx - 0.65, ly), xytext=(lx + 0.65, ly),
               arrowprops=dict(arrowstyle="-|>", lw=2.0, color=C["agent"],
                                connectionstyle="arc3,rad=-0.9", shrinkA=2, shrinkB=2))
    ax.text(lx, ly + 0.75, "$\\times Q$ rounds", ha="center", fontsize=9.5, color=C["agent"])

    ax.set_title("Per-agent model: observation + messages, $Q$ rounds of passing, masked head",
                 fontsize=11.5)
    fig.tight_layout()
    fig.savefig(f"{OUT}/architecture_simple.png"); plt.close(fig)


if __name__ == "__main__":
    architecture_simple()
