"""fig:distancedifference (sec:method:model, "Distance as a difference"), proposed 2026-11-24.

A small field of view around one agent, with the distance to its target on every vertex (a)
and the same minus the agent's own distance (b). The target lies to the right, 48 steps away.
Run from the workspace root: python thesis-progress/scripts/images/distance_difference.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from base import OUT, PG, aisle_node, plt  # noqa: E402

# An aisle running left to right and a cross-aisle through the agent's vertex.
NODES = {(-2, 0): 50, (-1, 0): 49, (0, 0): 48, (1, 0): 47, (2, 0): 46,
         (0, 1): 49, (0, -1): 49}
EDGES = [((-2, 0), (-1, 0)), ((-1, 0), (0, 0)), ((0, 0), (1, 0)), ((1, 0), (2, 0)),
         ((0, 0), (0, 1)), ((0, 0), (0, -1))]
OWN = NODES[(0, 0)]

fig, axes = plt.subplots(1, 2, figsize=(8.4, 2.6))
for ax, title, value in [
    (axes[0], "(a) distance to the target", lambda d: f"{d}"),
    (axes[1], "(b) minus the agent's own", lambda d: (f"{d - OWN:+d}".replace("-", "\u2212")) if d != OWN else "0"),
]:
    for p, q in EDGES:
        ax.plot([p[0], q[0]], [p[1], q[1]], color=PG["edge"], lw=2.2, zorder=1)
    for p, d in NODES.items():
        aisle_node(ax, p, s=260, zorder=3)
        ax.text(p[0] + 0.22, p[1] + 0.22, value(d), fontsize=12, color=PG["text"],
                ha="left", va="bottom", zorder=5)
    ax.scatter(0, 0, s=150, c=PG["to_pickup"], zorder=4)
    ax.annotate("", xy=(3.1, 0), xytext=(2.35, 0),
                arrowprops=dict(arrowstyle="-|>", color=PG["transit"], lw=1.4))
    ax.text(3.15, 0, "target", fontsize=11, color=PG["transit"], va="center")
    ax.set_title(title, fontsize=12, color=PG["transit"])
    ax.set_xlim(-2.6, 3.9)
    ax.set_ylim(-1.5, 1.6)
    ax.set_aspect("equal")
    ax.axis("off")

out = os.path.join(OUT, "distance_difference.png")
fig.savefig(out)
print(out)
