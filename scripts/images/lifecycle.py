"""
The life of the tea task tau_1 (fig:lifecycle), in the look of the pygame viewer ([A104],
base.py PG). One label per moment, the time under it. The waiting stage is grey, the agent's
idle colour. The active stage takes the agent's colours of fig:taskroute (instance.py), orange
on the way to the shelf and red on the way to the workstation. The times are those of tau_1 in
instance.py: released 5, assigned 9, picked up 11, delivered 14.
"""
import matplotlib.pyplot as plt

from base import OUT, PG

T = dict(released=5, assigned=9, pickup=11, finish=14)


def lifecycle():
    fig, ax = plt.subplots(figsize=(10, 3.0))
    x = {k: 1.0 + (v - 5) * 0.85 for k, v in T.items()}
    ax.set_xlim(0.2, 10.4); ax.set_ylim(-0.2, 3.0); ax.axis("off")

    axis_y = 1.3
    ax.annotate("", xy=(10.2, axis_y), xytext=(0.4, axis_y),
                arrowprops=dict(arrowstyle="-|>", lw=1.6, color=PG["text"]))
    ax.text(10.25, axis_y - 0.05, "$t$", fontsize=13, va="top", color=PG["text"])

    events = [("released", "released"), ("assigned", "assigned"),
              ("pickup", "picked up at A"), ("finish", r"delivered at $W_1$")]
    for key, word in events:
        ax.plot([x[key]] * 2, [axis_y - 0.1, axis_y + 0.1], lw=2.2, color=PG["text"])
        ax.text(x[key], axis_y + 0.22, word, ha="center", va="bottom", fontsize=11.5,
                color=PG["text"])
        ax.text(x[key], axis_y - 0.22, f"$t={T[key]}$", ha="center", va="top", fontsize=11,
                color=PG["text"])

    def span(x0, x1, y, colour, lw=5):
        ax.plot([x0, x1], [y, y], color=colour, lw=lw, solid_capstyle="butt")

    stage_y = 0.25
    span(x["released"], x["assigned"], stage_y, PG["idle"])
    span(x["assigned"], x["pickup"], stage_y, PG["to_pickup"])
    span(x["pickup"], x["finish"], stage_y, PG["to_delivery"])
    ax.text((x["released"] + x["assigned"]) / 2, stage_y - 0.15, r"waiting, $\mathcal{Q}_t$",
            ha="center", va="top", fontsize=11.5, color=PG["text"])
    ax.text((x["assigned"] + x["finish"]) / 2, stage_y - 0.15, r"active, $\mathcal{B}_t$",
            ha="center", va="top", fontsize=11.5, color=PG["text"])
    ax.text(x["finish"] + 0.3, stage_y, r"done, $\mathcal{C}_t$", ha="left", va="center",
            fontsize=11.5, color=PG["text"])

    top = 2.55
    ax.annotate("", xy=(x["finish"], top), xytext=(x["released"], top),
                arrowprops=dict(arrowstyle="<->", lw=1.4, color=PG["text"]))
    ax.text((x["released"] + x["finish"]) / 2, top + 0.08,
            r"service time $\zeta_1 = 14 - 5 = 9$", ha="center", va="bottom", fontsize=11.5,
            color=PG["text"])
    fig.savefig(f"{OUT}/lifecycle.png"); plt.close(fig)


if __name__ == "__main__":
    lifecycle()
