"""The real 8-agent warehouse (data/warehouse_m8.json, from instance_data.py)
for the chapter figures that draw it: instance_simple.py whole, instance.py and
observation.py as a crop of the top-left corner. One warehouse, so the reader
meets the same place in every figure.
"""
import json
import os
from collections import deque

from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch

from base import C

DATA = os.path.join(os.path.dirname(__file__), "data", "warehouse_m8.json")

STYLE = {  # face, edge, marker, size
    "": ("white", C["node"], "o", 260),
    "storage": (C["store_f"], C["store_e"], "o", 300),
    "delivery": (C["del_f"], C["del_e"], "s", 340),
    "receiving": (C["rcv_f"], C["rcv_e"], "^", 340),
    "endpoint": (C["ep_f"], C["ep_e"], "D", 260),
}
LEGEND = {
    "storage": (r"$V_{\mathrm{str}}$", "o", 10),
    "delivery": (r"$V_{\mathrm{work}}$", "s", 10),
    "receiving": (r"$V_{\mathrm{rcv}}$", "^", 10),
    "endpoint": (r"$V_{\mathrm{ep}}$", "D", 9),
    "": (r"$V_{\mathrm{mov}}$", "o", 10),
}


class Warehouse:
    """The warehouse, or the part of it with x <= x_faded and y >= y_min. Vertices
    with x > x_max are kept as `faded`, drawn pale to show the warehouse goes on."""

    def __init__(self, x_max=None, x_faded=None, y_min=None):
        with open(DATA) as handle:
            data = json.load(handle)
        x_cut = x_faded if x_faded is not None else x_max
        keep = {int(v) for v, (x, y) in data["positions"].items()
                if (x_cut is None or x <= x_cut) and (y_min is None or y >= y_min)}
        self.pos = {int(v): tuple(p) for v, p in data["positions"].items() if int(v) in keep}
        self.roles = {int(v): r for v, r in data["roles"].items() if int(v) in keep}
        self.faded = {v for v in keep if x_max is not None and self.pos[v][0] > x_max}
        self.edges = {(u, v): one_way for u, v, one_way in data["edges"]
                      if u in keep and v in keep}

    def successors(self, v):
        """The vertices one move from v. A two-way edge is stored once."""
        out = [w for (u, w), _ in self.edges.items() if u == v]
        out += [u for (u, w), one_way in self.edges.items() if w == v and not one_way]
        return out

    def steps(self, source, cutoff=None):
        """Fewest moves from source to every vertex reachable in the part kept."""
        dist, queue = {source: 0}, deque([source])
        while queue:
            v = queue.popleft()
            if cutoff is not None and dist[v] == cutoff:
                continue
            for w in self.successors(v):
                if w not in dist:
                    dist[w] = dist[v] + 1
                    queue.append(w)
        return dist

    def draw(self, ax, dim=(), node_scale=1.0, alpha_dim=0.3):
        """Edges, one-way edges as arrows, and the vertices by role. Vertices in
        `dim` and the faded ones are drawn pale."""
        pale = set(dim) | self.faded
        for (u, v), one_way in self.edges.items():
            alpha = alpha_dim if u in pale or v in pale else 1.0
            if one_way:
                ax.add_patch(FancyArrowPatch(self.pos[u], self.pos[v], arrowstyle="-|>",
                                             mutation_scale=12 * node_scale ** 0.5,
                                             color=C["node"], lw=1.4, shrinkA=8 * node_scale,
                                             shrinkB=8 * node_scale, alpha=alpha, zorder=1))
            else:
                ax.plot(*zip(self.pos[u], self.pos[v]), color=C["edge"], lw=1.8,
                        alpha=alpha, zorder=1)
        for role, (face, edge, marker, size) in STYLE.items():
            for alpha, group in ((1.0, [v for v in self.pos if v not in pale]),
                                 (alpha_dim, [v for v in self.pos if v in pale])):
                nodes = [v for v in group if self.roles[v] == role]
                if nodes:
                    ax.scatter([self.pos[v][0] for v in nodes], [self.pos[v][1] for v in nodes],
                               s=size * node_scale, c=face, edgecolors=edge, marker=marker,
                               linewidths=1.4, alpha=alpha, zorder=3)

    def legend_handles(self):
        """One legend entry per vertex role, in the order of LEGEND."""
        return [Line2D([], [], marker=marker, ls="", mfc=STYLE[role][0], mec=STYLE[role][1],
                       ms=ms, label=label)
                for role, (label, marker, ms) in LEGEND.items()]
