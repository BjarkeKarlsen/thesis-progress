"""
Reproducible thesis figures for the Problem Formulation chapter.

Run:  python figure.py
Out:  ../Images/instance.png ... ../Images/concentration.png
      (../Images is what both problem_formulation*.tex already point at
      via \graphicspath{{\subfix{../Images/}}} -- keep OUT in sync with that,
      not the other way around)

Only matplotlib + networkx are required. Every figure is a *schematic*:
positions are hand-set so the same figure is produced on every run.
"""
import math, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mp
from matplotlib.lines import Line2D
import networkx as nx
import numpy as np

OUT = "../Images"
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({
    "font.size": 12,
    "font.family": "serif",          # match a LaTeX thesis
    "savefig.bbox": "tight",
    "savefig.dpi": 300,
})

C = dict(edge="#9aa5b1", node="#5a6673", store_f="#cfe3f7", store_e="#2f6fae",
         del_f="#ffd9b3", del_e="#c9761a", ep_f="#d7f0d8", ep_e="#3f8f45",
         agent="#c0392b", accent="#2f6fae", comm="#7d3c98", text="#43505c")


# ---------------------------------------------------------------- layout
# G is directed: (v,w) in E does not imply (w,v) in E (sec:pf:env). Every
# adjacency is added in both directions except ONE_WAY, which models a
# genuine one-way aisle segment -- not a drawing convention, an actual
# asymmetry in the edge set, so a figure caption can honestly say so.
ONE_WAY = {("1_8", "2_8")}  # allowed direction only: 1_8 -> 2_8


def warehouse_graph(rows=5, cols=9, dx=1.35, dy=1.15):
    """Aisle layout: two cross-aisles (top/bottom row) + vertical racks."""
    G, pos = nx.DiGraph(), {}
    for r in range(rows):
        for c in range(cols):
            if r in (0, rows - 1) or c % 2 == 0:
                n = f"{r}_{c}"
                G.add_node(n)
                pos[n] = (c * dx, -r * dy)
    for n in list(G):
        r, c = map(int, n.split("_"))
        for dr, dc in ((0, 1), (1, 0)):
            m = f"{r+dr}_{c+dc}"
            if m not in G:
                continue
            if (n, m) in ONE_WAY or (m, n) in ONE_WAY:
                u, v = next(iter(ONE_WAY & {(n, m), (m, n)}))
                G.add_edge(u, v)
            else:
                G.add_edge(n, m)
                G.add_edge(m, n)
    return G, pos


G, POS = warehouse_graph()
STORAGE = [n for n in G if 0 < int(n.split("_")[0]) < 4 and int(n.split("_")[1]) % 2 == 0]
DELIVERY = ["0_0", "4_8"]
ENDPOINTS = ["0_4", "4_2", "0_8"]


def draw_base(ax, dim=False):
    """Draw the warehouse graph; dim=True greys it out as a background."""
    a = 0.35 if dim else 1.0
    two_way = [(u, v) for u, v in G.edges() if (v, u) in G.edges()]
    one_way = [(u, v) for u, v in G.edges() if (v, u) not in G.edges()]
    nx.draw_networkx_edges(G, POS, edgelist=two_way, ax=ax, edge_color=C["edge"],
                           width=1.6, alpha=a, arrows=False)
    nx.draw_networkx_edges(G, POS, edgelist=one_way, ax=ax, edge_color=C["accent"],
                           width=2.0, alpha=a, arrows=True, arrowsize=18,
                           node_size=460, connectionstyle="arc3,rad=0.0")
    other = [n for n in G if n not in STORAGE + DELIVERY + ENDPOINTS]
    for nl, fc, ec, shape, size in (
        (other, "white", C["node"], "o", 460),
        (STORAGE, C["store_f"], C["store_e"], "o", 460),
        (DELIVERY, C["del_f"], C["del_e"], "s", 560),
        (ENDPOINTS, C["ep_f"], C["ep_e"], "D", 470),
    ):
        nx.draw_networkx_nodes(G, POS, nodelist=nl, node_color=fc, edgecolors=ec,
                               node_shape=shape, node_size=size, ax=ax, alpha=a)


def put_agent(ax, node, label, dx=0, dy=16):
    ax.scatter(*POS[node], s=260, c=C["agent"], zorder=5,
               edgecolors="white", linewidths=1.2)
    ax.annotate(label, POS[node], textcoords="offset points", xytext=(dx, dy),
                ha="center", color=C["agent"], fontsize=14)


# ---------------------------------------------------------------- fig 1
def fig_instance():
    fig, ax = plt.subplots(figsize=(12, 5.6))
    draw_base(ax)
    sj, gj = "2_6", "0_0"
    path = nx.shortest_path(G, sj, gj)
    nx.draw_networkx_edges(G, POS, edgelist=list(zip(path, path[1:])),
                           edge_color=C["agent"], width=3.4, style=(0, (4, 3)), ax=ax,
                           arrows=False)
    for n, lab in {"4_0": "$a_1$", "2_4": "$a_2$", "0_6": "$a_3$"}.items():
        put_agent(ax, n, lab)
    ax.annotate(r"$s_j$ (pickup)", POS[sj], textcoords="offset points",
                xytext=(12, -6), fontsize=13)
    ax.annotate(r"$g_j$ (delivery)", POS[gj], textcoords="offset points",
                xytext=(-4, -26), fontsize=13)
    handles = [
        Line2D([], [], marker="o", ls="", mfc=C["store_f"], mec=C["store_e"], ms=12,
               label=r"storage $\mathcal{V}_{\mathrm{str}}$"),
        Line2D([], [], marker="s", ls="", mfc=C["del_f"], mec=C["del_e"], ms=12,
               label=r"delivery $\mathcal{V}_{\mathrm{del}}$"),
        Line2D([], [], marker="D", ls="", mfc=C["ep_f"], mec=C["ep_e"], ms=11,
               label=r"endpoint $\mathcal{V}_{\mathrm{ep}}$"),
        Line2D([], [], marker="o", ls="", mfc="white", mec=C["node"], ms=12,
               label="transit vertex"),
        Line2D([], [], marker="o", ls="", color=C["agent"], ms=12, label="agent"),
        Line2D([], [], ls=(0, (4, 3)), color=C["agent"], lw=3,
               label=r"task $\tau_j=(r_j,s_j,g_j,k_j)$"),
        Line2D([], [], color=C["accent"], lw=2.4, marker=">", markersize=9, # adjust the mark here is off by 8 pixels in X axes
               label=r"one-way segment: $(v,w)\in E$, $(w,v)\notin E$"),

        #     ax.annotate("", xy=(1.72, -0.60), xytext=(1.78, -0.64),
        #        arrowprops=dict(arrowstyle="-|>", lw=2.2, color=C["accent"]))
    ]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, 0.02),
              ncol=4, frameon=False, fontsize=11)
    ax.set_aspect("equal"); ax.set_axis_off()
    fig.savefig(f"{OUT}/instance.png"); plt.close(fig)


# ---------------------------------------------------------------- fig 2
def fig_observation(ego="4_4", depth=2, target="0_0", r_com=3.3):
    obs = dict(nx.single_source_shortest_path_length(G, ego, cutoff=depth))
    sub = G.subgraph(obs)
    fig, ax = plt.subplots(figsize=(12, 5.6))
    draw_base(ax, dim=True)
    nx.draw_networkx_edges(sub, POS, ax=ax, edge_color=C["accent"], width=3.0, arrows=False)
    nx.draw_networkx_nodes(G, POS, nodelist=list(obs), node_size=470,
                           node_color="none", edgecolors=C["accent"], linewidths=3.0, ax=ax)
    for n in obs:                                     # eta_i(v,t)
        ax.annotate(str(nx.shortest_path_length(G, n, target)), POS[n],
                    textcoords="offset points", xytext=(13, 10), ha="left",
                    fontsize=12, color=C["accent"], weight="bold")
    for n, lab in {"4_0": "$a_1$", ego: "$a_2$", "4_8": "$a_3$"}.items():
        put_agent(ax, n, lab, dx=-17, dy=6)
    ex, ey = POS[ego]
    ax.add_patch(plt.Circle((ex, ey), r_com, fill=False, ls=(0, (2, 3)),
                            lw=2.2, color=C["comm"]))
    ang = math.radians(230)
    ax.annotate("", xy=(ex + r_com * math.cos(ang), ey + r_com * math.sin(ang)),
                xytext=(ex, ey),
                arrowprops=dict(arrowstyle="<->", color=C["comm"], lw=1.8, ls=":"))
    ax.annotate(r"$r_{\mathrm{com}}$",
                (ex + 0.55 * r_com * math.cos(ang) - 0.45,
                 ey + 0.55 * r_com * math.sin(ang) - 0.1),
                color=C["comm"], fontsize=14)
    ax.annotate(r"target $q_2(t)$", POS[target], textcoords="offset points",
                xytext=(-8, -30), fontsize=12, color=C["del_e"])
    handles = [
        Line2D([], [], color=C["accent"], lw=3,
               label=r"induced subgraph $\mathcal{G}^{(d)}_i(t)$, $d=2$"),
        Line2D([], [], ls=(0, (2, 3)), color=C["comm"], lw=2,
               label=r"communication radius $r_{\mathrm{com}}$"),
        Line2D([], [], marker="o", ls="", color=C["agent"], ms=12, label="agent"),
        Line2D([], [], marker=r"$5$", ls="", color=C["accent"], ms=13,
               label=r"$\eta_i(v,t)=d_G(v,q_i(t))$"),
    ]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, 0.06),
              ncol=2, frameon=False, fontsize=12)
    ax.set_aspect("equal"); ax.set_axis_off()
    fig.savefig(f"{OUT}/observation.png"); plt.close(fig)


# ---------------------------------------------------------------- fig 3
def _draw_loop_panel(ax, feedback):
    """One panel of the loop: feedback=True is the coupled model, False is F_fix."""
    ax.set_xlim(0, 12); ax.set_ylim(0, 6.4); ax.axis("off")
    storage_txt = (
        "Storage layer  $F$\nslow: every $\\Delta$ steps\n"
        "$x_t=F(x_{t-\\Delta},\\hat\\rho_t,\\hat\\mu_t,\\hat w_t)$"
        if feedback else
        "Storage layer  $F_{\\mathrm{fix}}$\n$F_{\\mathrm{fix}}(x,\\cdot)=x$\n"
        "ignores the estimates below"
    )
    boxes = [
        (0.5, 4.0, 3.2, 1.5, storage_txt, C["store_f"]),
        (4.4, 4.0, 3.2, 1.5, "Task generation\n$\\tau_j=(r_j,s_j,g_j)$\n"
                             "pickup $s_j$ drawn from $x_t$", "#f6e7c1"),
        (8.3, 4.0, 3.2, 1.5, "MAPD controller  $\\pi$\nfast: every timestep\n"
                             "assignment + collision-free routing", C["ep_f"]),
        (4.4, 0.8, 3.2, 1.4, "Causal traffic estimate\n"
                             "$\\hat\\mu_t(e),\\ \\hat w_t(e),\\ \\hat\\rho_t$", "#f7d6d6"),
    ]
    for x, y, w, h, txt, col in boxes:
        ax.add_patch(mp.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.14",
                                       fc=col, ec=C["text"], lw=1.5))
        ax.text(x + w / 2, y + h / 2, txt, ha="center", va="center", fontsize=11.5)
    A = dict(arrowstyle="-|>", lw=2.0, color=C["text"])
    ax.annotate("", xy=(4.4, 4.75), xytext=(3.7, 4.75), arrowprops=A)
    ax.annotate("", xy=(8.3, 4.75), xytext=(7.6, 4.75), arrowprops=A)
    red = lambda rad: dict(arrowstyle="-|>", lw=2.0, color=C["agent"],
                           connectionstyle=f"arc3,rad={rad}")
    ax.annotate("", xy=(7.6, 1.5), xytext=(9.9, 4.0), arrowprops=red(0.2))
    ax.text(9.4, 2.5, "measure", color=C["agent"], fontsize=12)
    if feedback:
        ax.annotate("", xy=(2.1, 4.0), xytext=(4.4, 1.5), arrowprops=red(0.2))
        ax.text(1.6, 2.5, "feedback\n(slow loop)", color=C["agent"], fontsize=12,
                ha="center")
    else:
        # Genuine absence, not a ghosted arrow -- nothing is drawn between the
        # stats box and the storage box, because under F_fix nothing connects them.
        ax.text(1.9, 2.5, "no feedback:\n$x_t$ held fixed", color=C["node"],
                fontsize=12, ha="center", style="italic")
    ax.text(6.0, 5.95, "fast loop: one environment timestep",
            fontsize=11, ha="center", color=C["text"])


def fig_loop():
    # Each panel keeps the same 12-in-wide scale the original single-panel
    # version used (1 data unit = 1 in) -- halving the width without shrinking
    # the boxes/font is what caused the earlier text-overflow bug.
    fig, axes = plt.subplots(1, 2, figsize=(24.0, 5.3))
    _draw_loop_panel(axes[0], feedback=True)
    axes[0].set_title("(a) adaptive storage — this thesis's coupled model",
                      fontsize=13)
    _draw_loop_panel(axes[1], feedback=False)
    axes[1].set_title(r"(b) $F_{\mathrm{fix}}$ baseline — feedback removed",
                      fontsize=13)
    fig.tight_layout()
    fig.savefig(f"{OUT}/loop.png"); plt.close(fig)


# ---------------------------------------------------------------- fig 4
def fig_lifecycle():
    fig, ax = plt.subplots(figsize=(12, 3.6))
    ax.set_xlim(0, 10); ax.set_ylim(0, 3.2); ax.axis("off")
    ax.annotate("", xy=(9.7, 1.25), xytext=(0.3, 1.25),
                arrowprops=dict(arrowstyle="-|>", lw=2.2, color=C["text"]))
    ax.text(9.75, 1.05, "$t$", fontsize=13)
    for x, lab, col in [(1.2, "$r_j$\nrelease", C["accent"]),
                        (3.6, "assignment", C["del_e"]),
                        (5.6, r"pickup at $s_j$", C["ep_e"]),
                        (8.8, r"$d_j$ delivery at $g_j$", C["agent"])]:
        ax.plot([x, x], [1.02, 1.48], lw=3.2, color=col)
        ax.annotate(lab, (x, 1.58), ha="center", fontsize=12, color=col)

    def span(x0, x1, y, lab, col):
        ax.annotate("", xy=(x1, y), xytext=(x0, y),
                    arrowprops=dict(arrowstyle="<->", lw=2.0, color=col))
        ax.text((x0 + x1) / 2, y - 0.33, lab, ha="center", fontsize=12, color=col)

    span(1.2, 3.6, 0.80, r"$\tau_j\in\mathcal{Q}_t$  (waiting)", C["accent"])
    span(3.6, 8.8, 0.80, r"$\tau_j\in\mathcal{B}_t$  (active)", C["del_e"])
    span(1.2, 8.8, 2.55, r"service time $\zeta_j=d_j-r_j$", C["text"])
    ax.text(9.15, 0.47, r"$\tau_j\in\mathcal{C}_T$", fontsize=12, color=C["ep_e"])
    fig.savefig(f"{OUT}/lifecycle.png"); plt.close(fig)


# ---------------------------------------------------------------- fig 5
def fig_conflicts():
    P = {"u": (0, 0), "v": (1, 0), "w": (2, 0)}
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.2))

    def panel(ax, title, names):
        ax.set_xlim(-0.5, 2.5); ax.set_ylim(-1.5, 1.0)
        ax.set_aspect("equal"); ax.axis("off")
        ax.text(1.0, 0.85, title, ha="center", fontsize=13)
        for a, b in zip(names, names[1:]):
            ax.plot([P[a][0], P[b][0]], [0, 0], color=C["edge"], lw=2.0, zorder=1)
        for n in names:
            ax.add_patch(plt.Circle(P[n], 0.16, fc="white", ec=C["node"], lw=1.8, zorder=3))
            ax.text(P[n][0], P[n][1] - 0.34, n, ha="center", fontsize=12)

    def ag(ax, n, lab, col):
        ax.scatter(*P[n], s=200, c=col, zorder=5)
        ax.text(P[n][0], P[n][1] + 0.28, lab, ha="center", fontsize=13, color=col)

    def arr(ax, x0, x1, y, col):
        ax.annotate("", xy=(x1, y), xytext=(x0, y),
                    arrowprops=dict(arrowstyle="-|>", lw=2.4, color=col))

    ax = axes[0]; panel(ax, "(a) vertex conflict", ("u", "v", "w"))
    ag(ax, "u", "$a_i$", C["agent"]); ag(ax, "w", "$a_j$", C["accent"])
    arr(ax, 0.05, 0.85, -0.7, C["agent"]); arr(ax, 1.95, 1.15, -0.7, C["accent"])
    ax.text(1.0, -1.25, r"$\ell_i(t{+}1)=\ell_j(t{+}1)$", ha="center", fontsize=12.5)

    ax = axes[1]; panel(ax, "(b) swap conflict", ("u", "v"))
    ag(ax, "u", "$a_i$", C["agent"]); ag(ax, "v", "$a_j$", C["accent"])
    arr(ax, 0.05, 0.95, -0.62, C["agent"]); arr(ax, 0.95, 0.05, -0.92, C["accent"])
    ax.text(1.0, -1.32, r"$\ell_i(t)=\ell_j(t{+}1)\ \wedge\ \ell_j(t)=\ell_i(t{+}1)$",
            ha="center", fontsize=11.5)

    ax = axes[2]; panel(ax, "(c) feasible joint transition", ("u", "v", "w"))
    ag(ax, "u", "$a_i$", C["agent"]); ag(ax, "w", "$a_j$", C["accent"])
    arr(ax, 0.05, 0.85, -0.7, C["agent"])
    ax.add_patch(mp.Arc((2.0, -0.7), 0.42, 0.42, theta1=200, theta2=520,
                        lw=2.2, color=C["accent"]))
    ax.annotate("", xy=(1.72, -0.60), xytext=(1.78, -0.64),
                arrowprops=dict(arrowstyle="-|>", lw=2.2, color=C["accent"]))
    ax.text(2.0, -1.25, r"$a_j$ waits, cost $c_{\mathrm{wait}}$",
            ha="center", fontsize=12.5, color=C["accent"])
    fig.savefig(f"{OUT}/conflicts.png"); plt.close(fig)


# ---------------------------------------------------------------- fig 6
def normalised_entropy(p):
    p = np.asarray(p, float); p = p[p > 0]
    return float(-(p * np.log(p)).sum() / math.log(len(p)))


def fig_concentration(seed=0):
    """Schematic illustration of H_T and C_T.

    NOTE: the two usage patterns are *illustrative* and must be replaced by
    measured mu_T(e) from a real run before the figure is used as a result.
    """
    # Traffic concentration doesn't care which direction an edge is traversed
    # in, only how unevenly $E$ is used -- an undirected view keeps that
    # count from double-booking the single one-way segment in $G$.
    rng = np.random.default_rng(seed)
    UG = G.to_undirected()
    edges = list(UG.edges())
    corridor = set(map(frozenset, zip(nx.shortest_path(UG, "4_0", "4_8")[:-1],
                                      nx.shortest_path(UG, "4_0", "4_8")[1:])))
    patterns = {
        "dispersed": np.full(len(edges), 10.0) + rng.integers(0, 3, len(edges)),
        "concentrated": np.array([60.0 if frozenset(e) in corridor else 3.0 for e in edges]),
    }
    probs = {k: w / w.sum() for k, w in patterns.items()}
    gmax = max(p.max() for p in probs.values())

    fig, axes = plt.subplots(1, 2, figsize=(13, 4.8))
    for ax, (name, p) in zip(axes, probs.items()):
        wv = dict(zip(edges, p))
        widths = [0.8 + 13 * (wv[e] / gmax) for e in edges]
        colors = [C["agent"] if wv[e] / gmax > 0.5 else "#9fb3c8" for e in edges]
        nx.draw_networkx_edges(UG, POS, edgelist=edges, width=widths,
                               edge_color=colors, ax=ax, arrows=False)
        nx.draw_networkx_nodes(UG, POS, node_size=80, node_color="white",
                               edgecolors=C["node"], ax=ax)
        H = normalised_entropy(p)
        ax.set_aspect("equal"); ax.axis("off")
        ax.text(0.5, 1.08, f"{name} traffic", transform=ax.transAxes,
                ha="center", fontsize=14)
        ax.text(0.5, 0.98, f"$H_T$ = {H:.2f},   $C_T = 1-H_T$ = {1-H:.2f}",
                transform=ax.transAxes, ha="center", fontsize=13, color=C["text"])
    axes[0].text(1.05, -0.10,
                 r"edge width $\propto p_T(e)=\mu_T(e)/\sum_{e'}\mu_T(e')$"
                 " (same scale in both panels)",
                 transform=axes[0].transAxes, ha="center", fontsize=12, color=C["node"])
    fig.savefig(f"{OUT}/concentration.png"); plt.close(fig)


# ---------------------------------------------------------------- fig 7
ZONE = {n for n in G if int(n.split("_")[1]) <= 4}  # illustrative Y_q: columns 0-4


def fig_congestion():
    """eq:occupancy: one instrument, delta(S,t;excl), at each architecture's window."""
    fig, axes = plt.subplots(1, 3, figsize=(15.5, 3.3))
    agents = {"4_0": "$a_1$", "2_4": "$a_2$", "0_6": "$a_3$"}

    def scatter_agents(ax, extra=(), dim_out=()):
        for n, lab in agents.items():
            faded = n in dim_out
            ax.scatter(*POS[n], s=220, c=C["agent"], zorder=5,
                       alpha=0.3 if faded else 1.0, edgecolors="white", linewidths=1.1)
            ax.annotate(lab, POS[n], textcoords="offset points", xytext=(0, 15),
                        ha="center", fontsize=12, color=C["agent"],
                        alpha=0.3 if faded else 1.0)
        for n in extra:
            ax.scatter(*POS[n], s=150, c=C["agent"], zorder=5,
                       edgecolors="white", linewidths=1.0)

    # (a) centralised -- S = V_mov, excl = empty: every agent counts
    ax = axes[0]
    draw_base(ax)
    xs = [POS[n][0] for n in G]; ys = [POS[n][1] for n in G]
    pad = 0.7
    ax.add_patch(mp.FancyBboxPatch((min(xs) - pad, min(ys) - pad),
                                   max(xs) - min(xs) + 2 * pad,
                                   max(ys) - min(ys) + 2 * pad,
                                   boxstyle="round,pad=0", fc=C["accent"], alpha=0.08,
                                   ec="none", zorder=0))
    scatter_agents(ax)
    ax.set_title("(a) centralised", fontsize=13)
    ax.text(0.5, -0.08, r"$S=V_{\mathrm{mov}}$, excl$=\emptyset$: all 3 count",
            transform=ax.transAxes, ha="center", fontsize=11.5, color=C["accent"])

    # (b) section-based -- S = one zone Y_q, excl = empty: only in-zone agents count
    ax = axes[1]
    draw_base(ax)
    zxs = [POS[n][0] for n in ZONE]; zys = [POS[n][1] for n in ZONE]
    ax.add_patch(mp.FancyBboxPatch((min(zxs) - 0.55, min(zys) - 0.6),
                                   max(zxs) - min(zxs) + 1.1,
                                   max(zys) - min(zys) + 1.2,
                                   boxstyle="round,pad=0", fc=C["accent"], alpha=0.14,
                                   ec=C["accent"], lw=1.4, ls="--", zorder=0))
    scatter_agents(ax, dim_out={"0_6"})
    ax.text(min(zxs) + 0.25, max(zys) - 0.35, "$Y_q$", ha="left", va="top",
            fontsize=13, color=C["accent"])
    ax.set_title("(b) section-based", fontsize=13)
    ax.text(0.5, -0.08, r"$S=Y_q$, excl$=\emptyset$: $a_1,a_2$ count, $a_3$ doesn't",
            transform=ax.transAxes, ha="center", fontsize=11.5, color=C["accent"])

    # (c) decentralised -- S = one agent's local window, excl = {that agent}
    ax = axes[2]
    draw_base(ax, dim=True)
    ego = "2_4"
    ax.add_patch(plt.Circle(POS[ego], 1.55, fill=True, fc=C["accent"], alpha=0.10,
                            ec=C["accent"], lw=2.0, ls=(0, (2, 3)), zorder=1))
    scatter_agents(ax, extra=("1_4",), dim_out={"4_0", "0_6"})
    ax.set_title("(c) decentralised", fontsize=13)
    ax.text(0.5, -0.08,
            r"$S=V^{(r_{\mathrm{cng}})}_i(t)$, excl$=\{a_i\}$: only the nearby dot"
            " counts",
            transform=ax.transAxes, ha="center", fontsize=11.5, color=C["accent"])

    for ax in axes:
        ax.set_aspect("equal"); ax.set_axis_off()
    fig.suptitle(r"$\delta(S,t;\mathrm{excl})$: one instrument, evaluated at each "
                 "architecture's own window", fontsize=13, y=1.1)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(f"{OUT}/congestion.png"); plt.close(fig)


# ---------------------------------------------------------------- fig 8
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


def fig_wellformed():
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


if __name__ == "__main__":
    fig_instance(); fig_observation(); fig_loop()
    fig_lifecycle(); fig_conflicts(); fig_concentration()
    fig_congestion(); fig_wellformed()
    print("wrote figures to", os.path.abspath(OUT))
