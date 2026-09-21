import matplotlib.pyplot as plt

from base import OUT, C


def _wf_panel(ax, pos, edges, endpoints, agents, title, note, note_color):
    ax.set_xlim(-0.9, 2.9); ax.set_ylim(-1.7, 1.7)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(title, fontsize=12.5)
    for a, b in edges:
        ax.plot([pos[a][0], pos[b][0]], [pos[a][1], pos[b][1]],
                color=C["edge"], lw=2.0, zorder=1)
    for n, p in pos.items():
        if n in endpoints:
            ax.scatter(*p, marker="D", s=380, facecolor=C["ep_f"],
                       edgecolor=C["ep_e"], linewidths=1.6, zorder=3)
        else:
            ax.scatter(*p, marker="o", s=280, facecolor="white",
                       edgecolor=C["node"], linewidths=1.6, zorder=3)
    for n, lab in agents.items():
        p = pos[n]
        ax.scatter(p[0], p[1], s=140, c=C["agent"], zorder=5,
                   edgecolors="white", linewidths=1.0)
        ax.annotate(lab, p, textcoords="offset points", xytext=(0, 15),
                    ha="center", fontsize=11, color=C["agent"])
    ax.text(0.5, -0.08, note, transform=ax.transAxes, ha="center",
            fontsize=10.5, color=note_color)


def wellformed():
    """Ma et al. (2017) well-formed MAPD instances, m=2 agents."""
    fig, axes = plt.subplots(1, 3, figsize=(15.5, 4.4))

    # (a) well-formed: 3 endpoints on a hub, no endpoint sits on another's path
    pos_a = {"hub": (1.0, 0.0), "e1": (0.0, 1.2), "e2": (2.0, 1.2), "e3": (1.0, -1.4)}
    edges_a = [("hub", "e1"), ("hub", "e2"), ("hub", "e3")]
    _wf_panel(axes[0], pos_a, edges_a, {"e1", "e2", "e3"},
              {"e1": "$a_1$", "e2": "$a_2$"}, "(a) well-formed",
              r"3 non-task endpoints $\geq m{=}2$; no path blocked", C["ep_e"])

    # (b) not well-formed: only 1 non-task endpoint for m=2 agents
    pos_b = {"hub": (1.0, 0.0), "e1": (0.0, 1.2), "t1": (2.0, 1.2), "t2": (1.0, -1.4)}
    edges_b = [("hub", "e1"), ("hub", "t1"), ("hub", "t2")]
    _wf_panel(axes[1], pos_b, edges_b, {"e1"},
              {"e1": "$a_1$", "t1": "$a_2$"}, "(b) not well-formed",
              r"only 1 non-task endpoint $<m{=}2$", C["agent"])
    axes[1].annotate("no endpoint\nto park at", pos_b["t1"],
                     textcoords="offset points", xytext=(30, -4), fontsize=9,
                     color=C["agent"], ha="left")

    # (c) not well-formed: every e1<->e3 path is forced through endpoint e2
    pos_c = {"e1": (0.0, 0.0), "e2": (1.4, 0.0), "e3": (2.8, 0.0)}
    edges_c = [("e1", "e2"), ("e2", "e3")]
    _wf_panel(axes[2], pos_c, edges_c, {"e1", "e2", "e3"},
              {"e1": "$a_1$", "e3": "$a_2$"}, "(c) not well-formed",
              r"every $e_1{\to}e_3$ path crosses endpoint $e_2$", C["agent"])

    fig.suptitle("Well-formed MAPD instances (Ma et al., 2017)", fontsize=13, y=1.05)
    fig.tight_layout(rect=[0, 0, 1, 0.90])
    fig.savefig(f"{OUT}/wellformed.png"); plt.close(fig)
