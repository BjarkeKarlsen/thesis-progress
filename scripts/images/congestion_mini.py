"""
Simple companion to controllers_example.py (Figure fig:controllers-example):
same small graph, same Y1/Y2 column split, same ego vertex ("1_1"). This
figure illustrates eq:congestion, delta_i(t), the *single* field-of-view
occupancy fraction defined once for every agent regardless of architecture.
There is no separate window size per architecture any more (that was the
pre-simplification design); the three panels differ only in *how many*
agents' own readings a given architecture gets to read, decentralised gets
one (its own), section-based gets every agent whose own position is in its
zone (and, since a field of view is not clipped at the zone boundary, that
reading may itself already reach a little past the edge), centralised gets
every agent.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mp
import networkx as nx

from base import OUT, C
from mini import mini_graph, draw_mini

EGO = "1_1"
AGENTS = {"0_0": "$a_1$", "1_2": "$a_2$", EGO: "$a_3$"}


def field_of_view(G, agent):
    return set(nx.single_source_shortest_path_length(G, agent, cutoff=1))


def delta(G, agent, agents_at):
    fov = field_of_view(G, agent)
    others = [n for n in agents_at if n in fov and n != agent]
    return len(others) / max(1, len(fov) - 1)


def _scatter(ax, pos, faded=()):
    for n, lab in AGENTS.items():
        f = n in faded
        ax.scatter(*pos[n], s=230, c=C["agent"], zorder=5, alpha=0.3 if f else 1.0,
                   edgecolors="white", linewidths=1.2)
        ax.annotate(lab, pos[n], textcoords="offset points", xytext=(0, 15),
                    ha="center", fontsize=11, color=C["agent"], alpha=0.35 if f else 1.0)


def _highlight_readings(ax, G, pos, active, deltas):
    """Draw the union of active agents' fields of view, and label each
    active agent with its own delta_i(t)."""
    union_edges = set()
    for a in active:
        fov = field_of_view(G, a)
        sub = G.subgraph(fov)
        union_edges |= set(sub.edges())
    if union_edges:
        nx.draw_networkx_edges(G, pos, edgelist=list(union_edges), ax=ax,
                               edge_color=C["accent"], width=2.4, arrows=False)
        window_nodes = {n for e in union_edges for n in e}
        nx.draw_networkx_nodes(G, pos, nodelist=list(window_nodes), node_size=520,
                               node_color="none", edgecolors=C["accent"],
                               linewidths=2.2, ax=ax)
    for a in active:
        x, y = pos[a]
        ax.annotate(rf"$\delta={deltas[a]:.2f}$", (x, y),
                    textcoords="offset points", xytext=(0, -22),
                    ha="center", fontsize=10, color=C["accent"])


def congestion_mini():
    G, pos = mini_graph(rows=3, cols=4, dx=1.1, dy=1.0)
    deltas = {a: delta(G, a, AGENTS) for a in AGENTS}
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.6))

    # # (a) decentralised: only ego's own reading
    # ax = axes[0]
    # draw_mini(ax, G, pos, dim=True)
    # active = [EGO]
    # faded = set(AGENTS) - set(active)
    # _scatter(ax, pos, faded=faded)
    # _highlight_readings(ax, G, pos, active, deltas)
    # ax.set_title("decentralised: its own reading only", fontsize=11)

    # # (b) section-based: every agent whose own position is in zone Y1
    # ax = axes[1]
    # draw_mini(ax, G, pos, dim=True)
    # y1 = [n for n in G if int(n.split("_")[1]) < 2]
    # xs = [pos[n][0] for n in y1]; ys = [pos[n][1] for n in y1]
    # ax.add_patch(mp.FancyBboxPatch((min(xs) - 0.45, min(ys) - 0.45),
    #                                max(xs) - min(xs) + 0.9, max(ys) - min(ys) + 0.9,
    #                                boxstyle="round,pad=0.05", fc=C["store_f"], ec=C["store_e"],
    #                                lw=1.4, alpha=0.4, zorder=0))
    # active = [a for a in AGENTS if a in y1]
    # faded = set(AGENTS) - set(active)
    # _scatter(ax, pos, faded=faded)
    # _highlight_readings(ax, G, pos, active, deltas)
    # ax.set_title("section-based: every agent in $Y_1$\n(reach past the "
    #              "boundary is the boundary protocol)", fontsize=10.5)

    # # (c) centralised: every agent
    # ax = axes[2]
    # draw_mini(ax, G, pos)
    # active = list(AGENTS)
    # _scatter(ax, pos)
    # _highlight_readings(ax, G, pos, active, deltas)
    # ax.set_title("centralised: every agent's reading", fontsize=11)

     # (a) centralised: every agent
    ax = axes[0]
    draw_mini(ax, G, pos)
    active = list(AGENTS)
    _scatter(ax, pos)
    _highlight_readings(ax, G, pos, active, deltas)
    ax.set_title("centralised: every agent's reading", fontsize=11)

    # (b) section-based: every agent whose own position is in zone Y1
    ax = axes[1]
    draw_mini(ax, G, pos, dim=True)
    y1 = [n for n in G if int(n.split("_")[1]) < 2]
    xs = [pos[n][0] for n in y1]; ys = [pos[n][1] for n in y1]
    ax.add_patch(mp.FancyBboxPatch((min(xs) - 0.45, min(ys) - 0.45),
                                   max(xs) - min(xs) + 0.9, max(ys) - min(ys) + 0.9,
                                   boxstyle="round,pad=0.05", fc=C["store_f"], ec=C["store_e"],
                                   lw=1.4, alpha=0.4, zorder=0))
    active = [a for a in AGENTS if a in y1]
    faded = set(AGENTS) - set(active)
    _scatter(ax, pos, faded=faded)
    _highlight_readings(ax, G, pos, active, deltas)
    ax.set_title("section-based: every agent in $Y_1$\n(reach past the "
                 "boundary is the boundary protocol)", fontsize=10.5)

    # (c) decentralised: only ego's own reading
    ax = axes[2]
    draw_mini(ax, G, pos, dim=True)
    active = [EGO]
    faded = set(AGENTS) - set(active)
    _scatter(ax, pos, faded=faded)
    _highlight_readings(ax, G, pos, active, deltas)
    ax.set_title("decentralised: its own reading only", fontsize=11)

    for ax in axes:
        ax.set_aspect("equal"); ax.set_axis_off()
        y0, y1_ = ax.get_ylim()
        ax.set_ylim(y0 - 0.3, y1_ + 0.15)
    fig.tight_layout()
    fig.savefig(f"{OUT}/congestion_mini.png"); plt.close(fig)


if __name__ == "__main__":
    congestion_mini()
