"""
warehouse_grid.py

Builds and visualises the warehouse as a grid-shaped instance of
WarehouseGraph (see warehouse_types.py): a directed graph G = (V, E) laid out
on a 2D grid, with V partitioned into V^S (storage), V^D (depots), V^B
(bases/charging), V^O (transit-only aisles/cross-aisles).

Layout pattern (classic "fishbone"-free warehouse block layout):
  - Storage blocks are rows of racks (V^S), grouped into aisles.
  - Vertical cross-aisles between blocks and a horizontal front/back
    cross-aisle are transit-only vertices (V^O).
  - Depot/pickup-dropoff vertices (V^D) sit along the bottom edge.
  - Base/charging vertices (V^B) sit along the top-left corner.

This script also drops in a handful of example MAPD tasks and one agent path
so the picture matches the thesis notation: an agent moving from its base,
through transit vertices, to a storage pick vertex, then to a depot delivery
vertex.

Run:
    pip install matplotlib
    python warehouse_grid.py

Output:
    output/warehouse_grid.png
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Tuple, Set, Optional

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

OUTPUT_DIR = "output"

VertexId = Tuple[int, int]  # (row, col) grid coordinate used directly as id


class VertexKind(Enum):
    STORAGE = auto()   # V^S
    DEPOT = auto()      # V^D
    BASE = auto()        # V^B
    TRANSIT = auto()      # V^O


KIND_COLOR = {
    VertexKind.STORAGE: "#8fbfe0",
    VertexKind.DEPOT: "#f4a261",
    VertexKind.BASE: "#90be6d",
    VertexKind.TRANSIT: "#e9e9e9",
}
KIND_LABEL = {
    VertexKind.STORAGE: r"$V^{S}$ storage",
    VertexKind.DEPOT: r"$V^{D}$ depot",
    VertexKind.BASE: r"$V^{B}$ base/charging",
    VertexKind.TRANSIT: r"$V^{O}$ transit",
}


@dataclass
class GridWarehouse:
    """
    A grid-shaped realisation of G = (V, E) for visualisation purposes.
    """
    rows: int
    cols: int
    kind_of: Dict[VertexId, VertexKind] = field(default_factory=dict)
    edges: Set[Tuple[VertexId, VertexId]] = field(default_factory=set)

    def add_vertex(self, v: VertexId, kind: VertexKind) -> None:
        self.kind_of[v] = kind

    def add_edge(self, u: VertexId, v: VertexId, bidirectional: bool = True) -> None:
        self.edges.add((u, v))
        if bidirectional:
            self.edges.add((v, u))

    def vertices_of_kind(self, kind: VertexKind) -> List[VertexId]:
        return [v for v, k in self.kind_of.items() if k == kind]


def build_grid_warehouse(
    n_storage_rows: int = 6,
    n_storage_cols: int = 10,
    aisle_block_width: int = 2,
    n_depots: int = 4,
    n_bases: int = 2,
) -> GridWarehouse:
    """
    Construct a grid warehouse.

    Rows 0            -> top transit / base row
    Rows 1..n_storage_rows -> storage rows, split into blocks by vertical
                              transit (cross-aisle) columns every
                              `aisle_block_width` storage columns
    Row  n_storage_rows+1  -> bottom transit row
    Row  n_storage_rows+2  -> depot row (V^D)
    """
    rows = n_storage_rows + 3
    # total columns = storage columns + one cross-aisle column after every
    # aisle_block_width storage columns + a leading/trailing transit column
    storage_col_positions: List[int] = []
    col = 1
    grid_cols = [0]  # left transit column
    count_in_block = 0
    for i in range(n_storage_cols):
        grid_cols.append(col)
        storage_col_positions.append(col)
        col += 1
        count_in_block += 1
        if count_in_block == aisle_block_width:
            grid_cols.append(col)  # cross-aisle column
            col += 1
            count_in_block = 0
    grid_cols.append(col)  # right transit column
    cols = col + 1

    wh = GridWarehouse(rows=rows, cols=cols)

    storage_col_set = set(storage_col_positions)

    for r in range(rows):
        for c in range(cols):
            if r == 0:
                kind = VertexKind.BASE if c < n_bases else VertexKind.TRANSIT
            elif r == rows - 1:
                kind = VertexKind.DEPOT if c < n_depots else VertexKind.TRANSIT
            elif 1 <= r <= n_storage_rows and c in storage_col_set:
                kind = VertexKind.STORAGE
            else:
                kind = VertexKind.TRANSIT
            wh.add_vertex((r, c), kind)

    for r in range(rows):
        for c in range(cols):
            if (r, c + 1) in wh.kind_of:
                wh.add_edge((r, c), (r, c + 1))
            if (r + 1, c) in wh.kind_of:
                wh.add_edge((r, c), (r + 1, c))

    return wh


def find_transit_neighbor(wh: GridWarehouse, v: VertexId) -> Optional[VertexId]:
    """Find an adjacent transit vertex to connect a storage cell for routing."""
    r, c = v
    for dr, dc in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        nb = (r + dr, c + dc)
        if wh.kind_of.get(nb) == VertexKind.TRANSIT:
            return nb
    return None


def example_task_path(wh: GridWarehouse) -> List[VertexId]:
    """
    Build an illustrative path: base -> transit corridor -> pick (storage)
    -> transit corridor -> depot (delivery), mimicking one MAPD task
    tau = (q, v_pick, v_del).
    """
    bases = wh.vertices_of_kind(VertexKind.BASE)
    storages = wh.vertices_of_kind(VertexKind.STORAGE)
    depots = wh.vertices_of_kind(VertexKind.DEPOT)
    if not bases or not storages or not depots:
        return []

    start = bases[0]
    pick = storages[len(storages) // 2]
    delivery = depots[-1]

    pick_transit = find_transit_neighbor(wh, pick) or pick

    def straight_path(a: VertexId, b: VertexId) -> List[VertexId]:
        path = [a]
        r, c = a
        tr, tc = b
        while c != tc:
            c += 1 if tc > c else -1
            path.append((r, c))
        while r != tr:
            r += 1 if tr > r else -1
            path.append((r, c))
        return path

    path = straight_path(start, pick_transit)
    path += [pick]
    path += straight_path(pick_transit, delivery)[1:]
    return path


def draw_grid_warehouse(wh: GridWarehouse, task_path: Optional[List[VertexId]] = None) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(14, 9))

    for (u, v) in wh.edges:
        (r1, c1), (r2, c2) = u, v
        ax.plot([c1, c2], [-r1, -r2], color="#bbbbbb", linewidth=0.6, zorder=1)

    for v, kind in wh.kind_of.items():
        r, c = v
        color = KIND_COLOR[kind]
        rect = mpatches.Rectangle((c - 0.4, -r - 0.4), 0.8, 0.8,
                                   facecolor=color, edgecolor="#555555", linewidth=0.4, zorder=2)
        ax.add_patch(rect)

    if task_path:
        xs = [c for (_, c) in task_path]
        ys = [-r for (r, _) in task_path]
        ax.plot(xs, ys, color="#d62828", linewidth=2.4, zorder=3,
                 marker="o", markersize=3, label="example task trajectory")
        ax.scatter([xs[0]], [ys[0]], color="#90be6d", s=140, edgecolor="black",
                    zorder=4, label="agent start (base, V^B)")
        ax.scatter([xs[-1]], [ys[-1]], color="#f4a261", s=140, edgecolor="black",
                    zorder=4, label="delivery (V^D)")

    handles = [mpatches.Patch(color=KIND_COLOR[k], label=KIND_LABEL[k]) for k in VertexKind]
    if task_path:
        handles += [
            plt.Line2D([0], [0], color="#d62828", lw=2.4, marker="o", markersize=4,
                       label="example task trajectory"),
        ]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.03),
              ncol=3, frameon=False, fontsize=9)

    ax.set_title(
        "Grid-shaped warehouse graph  $G=(V,E)$,  "
        r"$V = V^{S}\cup V^{D}\cup V^{B}\cup V^{O}$",
        fontsize=13,
    )
    ax.set_aspect("equal")
    ax.axis("off")
    fig.tight_layout()
    return fig


def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    wh = build_grid_warehouse(
        n_storage_rows=6,
        n_storage_cols=12,
        aisle_block_width=3,
        n_depots=4,
        n_bases=2,
    )
    path = example_task_path(wh)
    fig = draw_grid_warehouse(wh, task_path=path)

    out_path = os.path.join(OUTPUT_DIR, "warehouse_grid.png")
    fig.savefig(out_path, dpi=200)
    plt.close(fig)

    n_storage = len(wh.vertices_of_kind(VertexKind.STORAGE))
    n_depot = len(wh.vertices_of_kind(VertexKind.DEPOT))
    n_base = len(wh.vertices_of_kind(VertexKind.BASE))
    n_transit = len(wh.vertices_of_kind(VertexKind.TRANSIT))
    n_edges = len(wh.edges)

    print(f"Saved {out_path}")
    print(f"|V^S|={n_storage}, |V^D|={n_depot}, |V^B|={n_base}, |V^O|={n_transit}, |E|={n_edges}")


if __name__ == "__main__":
    main()
