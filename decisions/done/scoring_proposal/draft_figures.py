"""Draft figures for scoring_proposal.tex. Not thesis figures yet.
Run from the workspace root."""
import math, sys
sys.path.insert(0, "thesis-progress/scripts/images")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import networkx as nx
from base import C, G, POS, DELIVERY, draw_base, put_agent

OUT = "scoring_proposal"
UG = G.to_undirected()
EDGES = [frozenset(e) for e in UG.edges()]
AGENTS = {"4_1": "$a_1$", "3_0": "$a_2$", "4_3": "$a_3$", "4_4": "$a_4$"}  # as in observation.png
CORR = ["4_4", "4_3", "4_2", "4_1", "4_0", "3_0", "2_0", "1_0", "0_0"]       # a_4 to D1
CORR_E = {frozenset(p) for p in zip(CORR, CORR[1:])}
D2_AISLE = {frozenset(p) for p in (("0_8", "1_8"), ("1_8", "2_8"), ("2_8", "3_8"), ("3_8", "4_8"))}


def H(counts, n_norm):
    c = [x for x in counts.values() if x > 0]; n = sum(c)
    return -sum(x / n * math.log(x / n) for x in c) / math.log(n_norm)


patterns = {
    "spread out": {e: 2 for e in EDGES},
    "mostly one corridor": {e: 6 if e in CORR_E else (0 if e in D2_AISLE else 1) for e in EDGES},
    "one corridor only": {e: 9 if e in CORR_E else 0 for e in EDGES},
}

fig, axes = plt.subplots(3, 1, figsize=(11, 14))
for ax, (name, cnt) in zip(axes, patterns.items()):
    draw_base(ax, dim=True)
    used = [tuple(e) for e in EDGES if cnt[e] > 0]
    nx.draw_networkx_edges(UG, POS, edgelist=used, ax=ax, edge_color=C["accent"],
                           width=[1.0 + 1.1 * cnt[frozenset(e)] for e in used], arrows=False)
    for e in EDGES:
        if cnt[e] >= 3:
            u, v = tuple(e); x = (POS[u][0] + POS[v][0]) / 2; y = (POS[u][1] + POS[v][1]) / 2
            vert = POS[u][0] == POS[v][0]
            ax.annotate(str(cnt[e]), (x, y), xytext=(14, 0) if vert else (0, -20), textcoords="offset points", va="center",
                        ha="center", fontsize=12, weight="bold", color=C["accent"])
    for n, lab in AGENTS.items():
        put_agent(ax, n, lab, dx=0, dy=14)
    for i, n in enumerate(DELIVERY, start=1):
        ax.annotate(f"D{i}", POS[n], ha="center", va="center", fontsize=10,
                    fontweight="bold", color=C["del_e"], zorder=6)
    used_n = sum(1 for x in cnt.values() if x > 0)
    ax.set_title(f"{name}:  {sum(cnt.values())} traversals on {used_n} of {len(EDGES)} edges\n"
                 f"current ($\\log|E^+_T|$): $H_T$ = {H(cnt, used_n):.2f}      "
                 f"proposed ($\\log|E|$): $H_T$ = {H(cnt, len(EDGES)):.2f}", fontsize=13)
    ax.set_aspect("equal"); ax.set_axis_off()
fig.savefig(f"{OUT}/concentration_draft.png", dpi=200, bbox_inches="tight"); plt.close(fig)

# Timeline of the tasks of tab:throughputexample, with blocked steps.
from matplotlib.patches import Patch
TASKS = [("$\\tau_1$", 5, 9, 14, []), ("$\\tau_2$", 3, 3, 11, [6, 7]), ("$\\tau_3$", 10, 12, 18, [15])]


def timeline(tasks, fname):
    n = len(tasks)
    fig, ax = plt.subplots(figsize=(11, 1.0 * n + 0.6))
    for row, (lab, rel, asg, fin, blocked) in enumerate(reversed(tasks)):
        end = fin if fin is not None else 20
        ax.add_patch(Rectangle((rel, row - .3), asg - rel, .6, fc=C["del_f"], ec=C["del_e"]))
        ax.add_patch(Rectangle((asg, row - .3), end - asg, .6, fc=C["store_f"], ec=C["store_e"],
                               ls="-" if fin is not None else "--"))
        for b in blocked:
            ax.add_patch(Rectangle((b, row - .3), 1, .6, fc=C["agent"], ec="white", alpha=.85))
        txt = (f"$\\zeta$ = {fin-rel},  blocked {len(blocked)}" if fin is not None
               else f"not finished,  blocked {len(blocked)}")
        ax.text(20.6, row, txt, va="center", fontsize=11)
    ax.set_yticks(range(n)); ax.set_yticklabels([t[0] for t in reversed(tasks)], fontsize=13)
    ax.axvline(20, color=C["text"], ls="--"); ax.text(20.1, n - .55, "$T=20$", fontsize=11)
    ax.set_xlim(0, 27); ax.set_ylim(-.6, n - .3); ax.set_xticks(range(0, 21, 2)); ax.set_xlabel("timestep")
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.legend(handles=[Patch(fc=C["del_f"], ec=C["del_e"], label="waiting (not yet assigned)"),
                       Patch(fc=C["store_f"], ec=C["store_e"], label="active (assigned)"),
                       Patch(fc=C["agent"], label="blocked step")],
              loc="upper center", bbox_to_anchor=(.45, -.9 / n), ncol=3, frameon=False, fontsize=11)
    fig.savefig(f"{OUT}/{fname}", dpi=200, bbox_inches="tight"); plt.close(fig)


timeline(TASKS, "timeline_draft.png")
# Decision D: tau_4 is assigned at 12, gets stuck at 14 and never finishes.
timeline(TASKS + [("$\\tau_4$", 11, 12, None, list(range(14, 20)))], "timeline_stuck_draft.png")


# Version 3: the same patterns scored by the share of the busiest 10% of edges.
def top_share(cnt, frac=0.10):
    k = math.ceil(frac * len(cnt)); c = sorted(cnt.values(), reverse=True)
    return k, sum(c[:k]) / sum(c)


fig, axes = plt.subplots(3, 1, figsize=(11, 14))
for ax, (name, cnt) in zip(axes, patterns.items()):
    draw_base(ax, dim=True)
    used = [tuple(e) for e in EDGES if cnt[e] > 0]
    nx.draw_networkx_edges(UG, POS, edgelist=used, ax=ax, edge_color=C["accent"],
                           width=[1.0 + 1.1 * cnt[frozenset(e)] for e in used], arrows=False)
    for e in EDGES:
        if cnt[e] >= 3:
            u, v = tuple(e); x = (POS[u][0] + POS[v][0]) / 2; y = (POS[u][1] + POS[v][1]) / 2
            vert = POS[u][0] == POS[v][0]
            ax.annotate(str(cnt[e]), (x, y), xytext=(14, 0) if vert else (0, -20),
                        textcoords="offset points", va="center", ha="center",
                        fontsize=12, weight="bold", color=C["accent"])
    for n, lab in AGENTS.items():
        put_agent(ax, n, lab, dx=0, dy=14)
    for i, n in enumerate(DELIVERY, start=1):
        ax.annotate(f"D{i}", POS[n], ha="center", va="center", fontsize=10,
                    fontweight="bold", color=C["del_e"], zorder=6)
    k, sh = top_share(cnt)
    ax.set_title(f"{name}:  the busiest {k} of {len(EDGES)} edges carry "
                 f"{round(sh * 72)} of 72 traversals,  $\\Gamma_T$ = {sh:.0%}", fontsize=13)
    ax.set_aspect("equal"); ax.set_axis_off()
fig.savefig(f"{OUT}/concentration_share_draft.png", dpi=200, bbox_inches="tight"); plt.close(fig)


# Version 4: service time split into waiting for an agent, travelling and blocked.
def timeline_split(tasks, fname):
    n = len(tasks)
    fig, ax = plt.subplots(figsize=(11.5, 1.0 * n + 0.6))
    for row, (lab, rel, asg, fin, blocked) in enumerate(reversed(tasks)):
        end = fin if fin is not None else 20
        ax.add_patch(Rectangle((rel, row - .3), asg - rel, .6, fc=C["del_f"], ec=C["del_e"]))
        ax.add_patch(Rectangle((asg, row - .3), end - asg, .6, fc=C["store_f"], ec=C["store_e"],
                               ls="-" if fin is not None else "--"))
        for b in blocked:
            ax.add_patch(Rectangle((b, row - .3), 1, .6, fc=C["agent"], ec="white", alpha=.85))
        if fin is not None:
            w, b = asg - rel, len(blocked); tr = fin - asg - b
            txt = f"{w} + {tr} + {b} = {fin - rel}"
        else:
            txt = "not finished"
        ax.text(20.6, row, txt, va="center", fontsize=12)
    ax.text(20.6, n - .45, "wait + travel + blocked = $\\zeta_j$", fontsize=11, color=C["text"])
    ax.set_yticks(range(n)); ax.set_yticklabels([t[0] for t in reversed(tasks)], fontsize=13)
    ax.axvline(20, color=C["text"], ls="--"); ax.text(19.0, -.55, "$T=20$", fontsize=11)
    ax.set_xlim(0, 28); ax.set_ylim(-.65, n - .2); ax.set_xticks(range(0, 21, 2)); ax.set_xlabel("timestep")
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.legend(handles=[Patch(fc=C["del_f"], ec=C["del_e"], label="waiting for an agent"),
                       Patch(fc=C["store_f"], ec=C["store_e"], label="travelling"),
                       Patch(fc=C["agent"], label="blocked")],
              loc="upper center", bbox_to_anchor=(.42, -.9 / n), ncol=3, frameon=False, fontsize=11)
    fig.savefig(f"{OUT}/{fname}", dpi=200, bbox_inches="tight"); plt.close(fig)


timeline_split(TASKS + [("$\\tau_4$", 11, 12, None, list(range(14, 20)))], "timeline_split_draft.png")
