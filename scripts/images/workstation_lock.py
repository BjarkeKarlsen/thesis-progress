"""Figure for [A91]: agents locked at a workstation on a one-lane aisle.

(a) the whole warehouse of test seed 200000 at the step the lock forms, the section boxed. (b) to (d)
that section at three steps, with the agents and the move each one asks for. Reads
data/workstation_lock_t<t>.json, written by `thesis-progress/scripts/workstation_lock.py frame`
(results/limitations/workstation_lock/README.md has the command). Run from the workspace root:

    python3 thesis-progress/scripts/images/workstation_lock.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from base import C, OUT, plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, Rectangle  # noqa: E402

DATA = os.path.join(os.path.dirname(__file__), "data", "workstation_lock_t{}.json")
STEPS = (900, 1157, 1500)  # the queue forms, the lock forms, still locked
STYLE = {  # role: marker, face, edge, size
    "aisle": ("o", "white", C["node"], 60),
    "storage": ("o", C["store_f"], C["store_e"], 60),
    "delivery": ("s", C["del_f"], C["del_e"], 90),
    "dock": ("^", C["del_f"], C["del_e"], 90),
    "endpoint": ("D", C["ep_f"], C["ep_e"], 50),
}


def draw(ax, d, box=None, scale=1.0, agents=True, labels=False):
    pos = {int(v): tuple(p) for v, p in d["positions"].items()}
    inside = (lambda v: True) if box is None else (
        lambda v: box[0] <= pos[v][0] <= box[1] and box[2] <= pos[v][1] <= box[3])
    seen = set()
    for a, b in d["edges"]:
        if (b, a) in seen or not (inside(a) or inside(b)):
            continue
        seen.add((a, b))
        (x0, y0), (x1, y1) = pos[a], pos[b]
        ax.plot([x0, x1], [y0, y1], color=C["edge"], lw=1.2 * scale, zorder=1)
    for role, (marker, face, edge, size) in STYLE.items():
        vs = [int(v) for v, r in d["roles"].items() if r == role and inside(int(v))]
        ax.scatter([pos[v][0] for v in vs], [pos[v][1] for v in vs], marker=marker, c=face,
                   edgecolors=edge, s=size * scale ** 2, linewidths=1.0, zorder=2)
    if not agents:
        return pos
    for name, a in d["agents"].items():
        x, y = pos[a["at"]]
        ax.scatter(x, y, s=60 * scale ** 2, c=C["agent"], edgecolors="white", linewidths=1.0,
                   zorder=4)
        if labels:
            ax.annotate(f"$a_{{{name}}}$", (x, y), textcoords="offset points", xytext=(-6, 13),
                        color=C["agent"], fontsize=11, zorder=5)
            if a["intent"] is not None and a["intent"] != a["at"]:
                ax.add_patch(FancyArrowPatch(pos[a["at"]], pos[a["intent"]], arrowstyle="-|>",
                                             mutation_scale=12, color=C["agent"], lw=1.3,
                                             shrinkA=8, shrinkB=8, zorder=3,
                                             connectionstyle="arc3,rad=0.35"))
    return pos


def main():
    frames = [json.load(open(DATA.format(t))) for t in STEPS]
    d = frames[1]
    pos = {int(v): tuple(p) for v, p in d["positions"].items()}
    ws = d["section_workstations"]
    xs = [pos[w][0] for w in ws]
    ys = [pos[w][1] for w in ws]
    box = (min(xs) - 3.2, max(xs) + 3.2, min(ys) - 1.6, max(ys) + 1.6)

    fig, axes = plt.subplots(2, 2, figsize=(12, 6.2))
    fig.subplots_adjust(hspace=0.02, wspace=0.04)
    ax = axes[0][0]
    draw(ax, d, scale=0.7)
    ax.add_patch(Rectangle((box[0], box[2]), box[1] - box[0], box[3] - box[2], fill=False,
                           ec=C["comm"], lw=1.6, ls="--", zorder=6))
    ax.set_title(f"(a) the warehouse at $t = {STEPS[1]}$", fontsize=12)
    for ax, f, letter in zip((axes[0][1], axes[1][0], axes[1][1]), frames, "bcd"):
        draw(ax, f, box=box, scale=1.3, labels=True)
        ax.set_xlim(box[0] - 0.6, box[1] + 0.6)
        ax.set_ylim(box[2] - 0.6, box[3] + 0.6)
        wx, wy = pos[f["workstation"]]
        ax.annotate("$w$", (wx, wy), textcoords="offset points", xytext=(0, -24), ha="center",
                    color=C["del_e"], fontsize=13)
        ax.set_title(f"({letter}) $t = {f['t']}$, {f['completed']} tasks done", fontsize=12)
    for ax in axes.flat:
        ax.set_aspect("equal")
        ax.invert_yaxis()  # as the trace viewer draws it, row 0 at the top
        ax.axis("off")
    path = os.path.join(OUT, "workstation_lock.png")
    fig.savefig(path)
    print("wrote", path)


if __name__ == "__main__":
    main()
