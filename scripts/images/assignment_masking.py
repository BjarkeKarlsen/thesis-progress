"""
Two mechanics from sec:method:controllers and sec:method:rl that decide
what an agent is even allowed to attempt:
  (a) eq:assignmentrule -- greedy task assignment, oldest task first,
      nearest free agent, removed from the pool before the next task.
  (b) eq:mask -- the policy head's logits for moves that don't exist at
      the current vertex are set to -inf before the softmax.
Drawn on tiny abstract examples, not the warehouse grid.
"""
import matplotlib.pyplot as plt
import numpy as np

from base import OUT, C

A = {"a1": (0.0, 0.0), "a2": (0.0, -1.6)}
S = {"s1": (2.4, 0.35), "s2": (2.4, -1.25)}
D = {("a1", "s1"): 2.0, ("a2", "s1"): 2.9, ("a1", "s2"): 2.9, ("a2", "s2"): 1.5}
MATCH = {"s1": "a1", "s2": "a2"}  # s1 processed first (oldest), then s2


def _panel_assignment(ax):
    ax.set_xlim(-0.6, 3.0); ax.set_ylim(-2.1, 1.0)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("(a) task assignment: $i^\\star(j)=\\arg\\min_i d_G(\\ell_i(t),s_j)$", fontsize=11)
    for (a, s), dist in D.items():
        matched = MATCH[s] == a
        ax.plot([A[a][0], S[s][0]], [A[a][1], S[s][1]],
               color=C["del_e"] if matched else C["edge"],
               lw=2.6 if matched else 1.2, alpha=1.0 if matched else 0.5, zorder=1)
        mx, my = (A[a][0] + S[s][0]) / 2, (A[a][1] + S[s][1]) / 2
        ax.text(mx, my + 0.08, f"{dist:.1f}", fontsize=9, ha="center",
               color=C["del_e"] if matched else C["node"],
               alpha=1.0 if matched else 0.6)
    for n, p in A.items():
        ax.scatter(*p, s=280, c=C["agent"], zorder=3, edgecolors="white", linewidths=1.3)
        ax.annotate(f"${n[0]}_{n[1]}$", p, textcoords="offset points", xytext=(-16, 0),
                   ha="right", va="center", fontsize=12, color=C["agent"])
    for n, p in S.items():
        ax.scatter(*p, marker="s", s=280, fc=C["del_f"], ec=C["del_e"], zorder=3, linewidths=1.5)
        lab = f"$s_{n[1]}$" + ("\n(oldest, processed 1st)" if n == "s1" else "\n(processed 2nd)")
        ax.annotate(lab, p, textcoords="offset points", xytext=(16, 0),
                   ha="left", va="center", fontsize=9.5, color=C["del_e"])


def _panel_masking(ax):
    ax.set_title("(b) action masking: logits for moves that don't exist $\\to-\\infty$",
                fontsize=11)
    labels = ["wait", "move($w_1$)", "move($w_2$)", "move(slot 4)"]
    valid = [True, True, True, False]
    logits = [0.4, 1.1, -0.3, None]
    masked = [l if v else -3.0 for l, v in zip(logits, valid)]
    colors = [C["store_e"] if v else C["node"] for v in valid]
    bars = ax.bar(labels, [m if v else 0.15 for m, v in zip(masked, valid)], color=colors)
    for b, v in zip(bars, valid):
        if not v:
            b.set_alpha(0.25)
    for i, (b, v) in enumerate(zip(bars, valid)):
        if not v:
            ax.text(b.get_x() + b.get_width() / 2, 0.22, "$-\\infty$", ha="center",
                   fontsize=11, color=C["agent"])
            ax.plot([b.get_x(), b.get_x() + b.get_width()], [0.15, 0.15],
                    color=C["agent"], lw=1.2)
    ax.set_ylabel("logit $\\ell(\\cdot)$ (before softmax)", fontsize=10)
    ax.set_ylim(-0.6, 1.6)
    ax.axhline(0, color=C["edge"], lw=1.0)
    ax.spines[["top", "right"]].set_visible(False)
    ax.text(0.5, 1.42, r"$v$ has $|N^{+}(v)|=2 < d_{\max}=3$", fontsize=9.5,
           color=C["text"], ha="center")


def assignment_masking():
    fig, axes = plt.subplots(1, 2, figsize=(12.4, 4.0))
    _panel_assignment(axes[0])
    _panel_masking(axes[1])
    fig.tight_layout()
    fig.savefig(f"{OUT}/assignment_masking.png"); plt.close(fig)


if __name__ == "__main__":
    assignment_masking()
