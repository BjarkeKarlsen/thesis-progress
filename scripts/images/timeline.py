import matplotlib.pyplot as plt
from matplotlib.patches import Patch, Rectangle

from base import OUT, C

# fig:timeline in sec:pf:measures. tau_1 is the task example of
# fig:taskroute (instance.py): released 5, assigned 9, a_2 moves one edge
# per timestep and delivers at 14, so it is never blocked. tau_2 and tau_3
# are illustrative, tau_4 is stuck from t=14 and still active at T=20.
# Each row: (label, released, assigned, finish or None, blocked timesteps).
TASKS = [
    (r"$\tau_1$", 5, 9, 14, []),
    (r"$\tau_2$", 3, 3, 11, [6, 7]),
    (r"$\tau_3$", 10, 12, 18, [15]),
    (r"$\tau_4$", 11, 12, None, list(range(14, 20))),
]
HORIZON = 20


def timeline():
    """Service time split into waiting for an agent, travel and blocked."""
    n = len(TASKS)
    fig, ax = plt.subplots(figsize=(11.5, 1.0 * n + 0.6))
    for row, (lab, rel, asg, fin, blocked) in enumerate(reversed(TASKS)):
        end = fin if fin is not None else HORIZON
        ax.add_patch(Rectangle((rel, row - .3), asg - rel, .6,
                               fc=C["del_f"], ec=C["del_e"]))
        ax.add_patch(Rectangle((asg, row - .3), end - asg, .6, fc=C["store_f"],
                               ec=C["store_e"], ls="-" if fin is not None else "--"))
        for b in blocked:
            ax.add_patch(Rectangle((b, row - .3), 1, .6, fc=C["agent"],
                                   ec="white", alpha=.85))
        if fin is not None:
            travel = fin - asg - len(blocked)
            txt = f"{asg - rel} + {travel} + {len(blocked)} = {fin - rel}"
        else:
            txt = "not finished"
        ax.text(HORIZON + .6, row, txt, va="center", fontsize=12)
    ax.text(HORIZON + .6, n - .45, r"wait + travel + blocked = $\zeta_j$",
            fontsize=11, color=C["text"])
    ax.set_yticks(range(n)); ax.set_yticklabels([t[0] for t in reversed(TASKS)], fontsize=13)
    ax.axvline(HORIZON, color=C["text"], ls="--")
    ax.text(HORIZON - 1.0, -.55, f"$T={HORIZON}$", fontsize=11)
    ax.set_xlim(0, HORIZON + 8); ax.set_ylim(-.65, n - .2)
    ax.set_xticks(range(0, HORIZON + 1, 2)); ax.set_xlabel("timestep")
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.legend(handles=[Patch(fc=C["del_f"], ec=C["del_e"], label="waiting for an agent"),
                       Patch(fc=C["store_f"], ec=C["store_e"], label="travelling"),
                       Patch(fc=C["agent"], label="blocked")],
              loc="upper center", bbox_to_anchor=(.42, -.9 / n), ncol=3,
              frameon=False, fontsize=11)
    fig.savefig(f"{OUT}/timeline.png"); plt.close(fig)
