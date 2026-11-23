"""
Shared setup for the Problem Formulation chapter figures: the warehouse
graph, its layout, the shared colour palette, and the common draw helpers
every fig_*.py module builds on.

OUT is what both problem_formulation*.tex point at via
\\graphicspath{{\\subfix{../Images/}}} -- keep it in sync with that, not the
other way around.
"""
import os
import matplotlib
matplotlib.use("Agg")
import networkx as nx

OUT = "thesis-progress/scripts/Images"
os.makedirs(OUT, exist_ok=True)

import matplotlib.pyplot as plt
plt.rcParams.update({
    "font.size": 12,
    "font.family": "serif",          # match a LaTeX thesis
    "mathtext.fontset": "cm",        # math in labels in the thesis font, not sans
    "savefig.bbox": "tight",
    "savefig.dpi": 300,
})

#TODO fix the colors to match the thesis color palette, here rcv_f and rcv_e are not the same as in the thesis, they are too light and not visible enough
C = dict(edge="#9aa5b1", node="#5a6673", store_f="#cfe3f7", store_e="#2f6fae",
         del_f="#ffd9b3", del_e="#c9761a", rcv_f="#f8c8a0", rcv_e="#d48c4a", ep_f="#d7f0d8", ep_e="#3f8f45",
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


RECEIVE = ["0_2", "4_6"]


def draw_base(ax, dim=False):
    """Draw the warehouse graph; dim=True greys it out as a background."""
    a = 0.35 if dim else 1.0
    two_way = [(u, v) for u, v in G.edges() if (v, u) in G.edges()]
    #one_way = [(u, v) for u, v in G.edges() if (v, u) not in G.edges()]
    nx.draw_networkx_edges(G, POS, edgelist=two_way, ax=ax, edge_color=C["edge"],
                           width=1.6, alpha=a, arrows=False)
    #nx.draw_networkx_edges(G, POS, edgelist=one_way, ax=ax, edge_color=C["accent"],
    #                       width=2.0, alpha=a, arrows=True, arrowsize=18,
    #                       node_size=460, connectionstyle="arc3,rad=0.0")
    other = [n for n in G if n not in STORAGE + DELIVERY + RECEIVE + ENDPOINTS]
    for nl, fc, ec, shape, size in (
        (other, "white", C["node"], "o", 460),
        (STORAGE, C["store_f"], C["store_e"], "o", 460),
        (DELIVERY, C["del_f"], C["del_e"], "s", 560),
        (ENDPOINTS, C["ep_f"], C["ep_e"], "D", 470),
        (RECEIVE, C["rcv_f"], C["rcv_e"], "v", 560),
    ):
        nx.draw_networkx_nodes(G, POS, nodelist=nl, node_color=fc, edgecolors=ec,
                               node_shape=shape, node_size=size, ax=ax, alpha=a)

def draw_base_mini(ax, dim=False):
    """Draw the warehouse graph; dim=True greys it out as a background."""
    a = 0.35 if dim else 1.0
    two_way = [(u, v) for u, v in G.edges() if (v, u) in G.edges()]
    #one_way = [(u, v) for u, v in G.edges() if (v, u) not in G.edges()]
    nx.draw_networkx_edges(G, POS, edgelist=two_way, ax=ax, edge_color=C["edge"],
                           width=1.6, alpha=a, arrows=False)
    #nx.draw_networkx_edges(G, POS, edgelist=one_way, ax=ax, edge_color=C["accent"],
    #                       width=2.0, alpha=a, arrows=True, arrowsize=18,
    #                       node_size=460, connectionstyle="arc3,rad=0.0")
    other = [n for n in G if n not in STORAGE + DELIVERY + RECEIVE + ENDPOINTS]
    for nl, fc, ec, shape, size in (
        (other, "white", C["node"], "o", 460),
        (STORAGE, C["store_f"], C["store_e"], "o", 460),
        (DELIVERY, C["del_f"], C["del_e"], "s", 560),
        (ENDPOINTS, C["ep_f"], C["ep_e"], "D", 470),
        (RECEIVE, C["rcv_f"], C["rcv_e"], "v", 560),
    ):
        nx.draw_networkx_nodes(G, POS, nodelist=nl, node_color=fc, edgecolors=ec,
                               node_shape=shape, node_size=size, ax=ax, alpha=a)




def put_agent(ax, node, label, dx=0, dy=16):
    ax.scatter(*POS[node], s=260, c=C["agent"], zorder=5,
               edgecolors="white", linewidths=1.2)
    ax.annotate(label, POS[node], textcoords="offset points", xytext=(dx, dy),
                ha="center", color=C["agent"], fontsize=14)


# ---------------------------------------------------------------- the pygame viewer's look
# [A104] Every thesis figure follows the pygame viewer of slap-mapd-coupling
# (viz/theme.py ROLE_STYLES, viz/pygame_renderer.py _PHASE_COLOURS, _RANK_STOPS, _draw_slots).
# The values are copied here so this repo does not import the other one.
PG = dict(
    edge="#9aa5b1", transit="#5a6673", one_way="#2f6fae", text="#43505c",
    slot_rim="#2f6fae",                       # a shelf: a white square slot, blue rim
    work_f="#ffd9b3", work_e="#c9761a",       # a workstation: orange square
    dock_f="#e6d9f2", dock_e="#7a4fa3",       # a dock: purple triangle
    park_f="#d7f0d8", park_e="#3f8f45",       # a parking endpoint: green diamond
    idle="#8a949e", to_pickup="#e08a1e", to_delivery="#c0392b",
    putaway="#7a4fa3", ship="#1f8a70",        # agent colour by what it does
)
RANK_STOPS = ("#b2182b", "#f4a582", "#92c5de", "#d1e5f0")  # popularity, most popular first


def rank_colour(rank, count):
    """The viewer's colour of popularity rank `rank` of `count` SKUs, rank 0 the most popular."""
    def rgb(h):
        return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
    share = 0.0 if count <= 1 else rank / (count - 1)
    stops = [rgb(c) for c in RANK_STOPS]
    at = share * (len(stops) - 1)
    i = min(int(at), len(stops) - 2)
    w = at - i
    return "#%02x%02x%02x" % tuple(round(a + (b - a) * w) for a, b in zip(stops[i], stops[i + 1]))


def shelf_slot(ax, x, y, half, bands=(), new=0.0, reached=False, alpha=1.0, zorder=3):
    """A shelf as the viewer's slot: a white square with a blue rim, filled from the bottom,
    one band per SKU with the most popular lowest. `bands` is [(share of the room, colour)].
    New stock on its way is striped on top in the put-away colour, and a slot a put-away
    reached gets a purple rim, the put-away colour."""
    from matplotlib.patches import Rectangle
    side = 2 * half
    ax.add_patch(Rectangle((x - half, y - half), side, side, fc="white", ec="none",
                           zorder=zorder))  # opaque even when faded, so no edge shows through
    bottom = y - half
    for share, colour in bands:
        ax.add_patch(Rectangle((x - half, bottom), side, side * share, fc=colour, lw=0,
                               alpha=alpha, zorder=zorder + 1))
        bottom += side * share
    if new > 0:
        ax.add_patch(Rectangle((x - half, bottom), side, side * new, fc="white",
                               ec=PG["putaway"], lw=0.6, hatch="////", alpha=alpha,
                               zorder=zorder + 1))
    ax.add_patch(Rectangle((x - half, y - half), side, side, fc="none",
                           ec=PG["putaway"] if reached else PG["slot_rim"],
                           lw=2.0 if reached else 1.3, alpha=alpha, zorder=zorder + 2))


def aisle_node(ax, p, s=70, zorder=3):
    """An aisle position as in the viewer: a small white circle with a grey rim."""
    ax.scatter(*p, s=s, c="white", edgecolors=PG["transit"], linewidths=1.2, zorder=zorder)


def work_mark(ax, p, s=260, zorder=3):
    ax.scatter(*p, s=s, marker="s", c=PG["work_f"], edgecolors=PG["work_e"], linewidths=1.4,
               zorder=zorder)


def dock_mark(ax, p, s=300, zorder=3):
    ax.scatter(*p, s=s, marker="^", c=PG["dock_f"], edgecolors=PG["dock_e"], linewidths=1.4,
               zorder=zorder)


def role_handles(roles=("storage", "delivery", "receiving", "")):
    """Legend marks of the viewer for the roles a small figure shows."""
    from matplotlib.lines import Line2D
    marks = {"storage": ("shelf", "s", "white", PG["slot_rim"], 10),
             "delivery": ("workstation", "s", PG["work_f"], PG["work_e"], 10),
             "receiving": ("dock", "^", PG["dock_f"], PG["dock_e"], 10),
             "endpoint": ("parking", "D", PG["park_f"], PG["park_e"], 9),
             "": ("aisle", "o", "white", PG["transit"], 6)}
    return [Line2D([], [], marker=m, ls="", mfc=f, mec=e, ms=ms, label=lab)
            for lab, m, f, e, ms in (marks[r] for r in roles)]


# The viewer's mark of each vertex role, for figures that draw a whole warehouse ([A104]):
# face, edge, marker, and marker area relative to a shelf. An aisle position is small, as in
# the viewer (radius r // 2), a shelf an empty slot, a workstation the filled square.
ROLE_MARK = {
    "": ("white", PG["transit"], "o", 0.3),
    "storage": ("white", PG["slot_rim"], "s", 1.0),
    "delivery": (PG["work_f"], PG["work_e"], "s", 1.0),
    "receiving": (PG["dock_f"], PG["dock_e"], "^", 1.2),
    "endpoint": (PG["park_f"], PG["park_e"], "D", 0.8),
}
