import matplotlib.pyplot as plt

from base import OUT, C


def _wf_panel(ax, pos, edges, endpoints, agents, title, note, note_color):
    ax.set_xlim(-0.7, 3.1); ax.set_ylim(-1.75, 1.55)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(title, fontsize=15)
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
                    ha="center", fontsize=14, color=C["agent"])
    ax.text(0.5, -0.08, note, transform=ax.transAxes, ha="center",
            fontsize=13, color=note_color)


def wellformed():
    """Ma et al. (2017) well-formed MAPD instances, m=2 agents."""
    fig, axes = plt.subplots(1, 3, figsize=(13.0, 3.8))

    # (a) well-formed: 3 endpoints on a hub, no endpoint sits on another's path
    pos_a = {"hub": (1.0, 0.0), "e1": (0.0, 1.2), "e2": (2.0, 1.2), "e3": (1.0, -1.4)}
    edges_a = [("hub", "e1"), ("hub", "e2"), ("hub", "e3")]
    _wf_panel(axes[0], pos_a, edges_a, {"e1", "e2", "e3"},
              {"e1": "$a_1$", "e2": "$a_2$"}, "(a) well-formed",
              r"3 non-task endpoints $\geq m{=}2$, no path blocked", C["ep_e"])

    # (b) not well-formed: only 1 non-task endpoint for m=2 agents
    pos_b = {"hub": (1.0, 0.0), "e1": (0.0, 1.2), "t1": (2.0, 1.2), "t2": (1.0, -1.4)}
    edges_b = [("hub", "e1"), ("hub", "t1"), ("hub", "t2")]
    _wf_panel(axes[1], pos_b, edges_b, {"e1"},
              {"e1": "$a_1$", "t1": "$a_2$"}, "(b) not well-formed",
              r"only 1 non-task endpoint $<m{=}2$", C["agent"])
    axes[1].annotate("no endpoint\nto park at", pos_b["t1"],
                     textcoords="offset points", xytext=(18, -4), fontsize=12,
                     color=C["agent"], ha="left")

    # (c) not well-formed: every e1<->e3 path is forced through endpoint e2
    pos_c = {"e1": (0.0, 0.0), "e2": (1.4, 0.0), "e3": (2.8, 0.0)}
    edges_c = [("e1", "e2"), ("e2", "e3")]
    _wf_panel(axes[2], pos_c, edges_c, {"e1", "e2", "e3"},
              {"e1": "$a_1$", "e3": "$a_2$"}, "(c) not well-formed",
              r"every $e_1{\to}e_3$ path crosses endpoint $e_2$", C["agent"])
    for n in ("e1", "e2", "e3"):  # the names the note uses
        axes[2].annotate(f"${n[0]}_{n[1]}$", pos_c[n], textcoords="offset points",
                         xytext=(0, -24), ha="center", fontsize=13, color=C["text"])

    # No title in the figure: the caption names it and cites Ma et al. (2017).
    fig.tight_layout()
    fig.savefig(f"{OUT}/wellformed.png"); plt.close(fig)
