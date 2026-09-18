"""warehouse_visuals.py

Visualisations for a grid-based warehouse environment:
- warehouse layout with node types (storage, delivery, other)
- storage demand heatmap
- edge flow heatmap

This script uses matplotlib and numpy. Plug your own data structures for
locations, storage assignment, and edge flows.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np
import matplotlib.pyplot as plt


# ----------------------------- Data classes -----------------------------

@dataclass
class WarehouseGridConfig:
    """Configuration for a grid-based warehouse layout.

    rows, cols: size of the grid.
    node_types: dict mapping (row, col) -> string in {"item", "delivery", "other"}.
    """

    rows: int
    cols: int
    node_types: Dict[Tuple[int, int], str]


@dataclass
class StorageDemand:
    """Demand per storage node.

    demand: dict mapping (row, col) -> non-negative float (e.g. order frequency).
    """

    demand: Dict[Tuple[int, int], float]


@dataclass
class EdgeFlows:
    """Flow per directed edge in the grid.

    flows: dict mapping ((r1, c1), (r2, c2)) -> non-negative float
           (e.g. number of traversals or cumulative travel time).
    """

    flows: Dict[Tuple[Tuple[int, int], Tuple[int, int]], float]


# ----------------------------- Helper utils -----------------------------

NODE_TYPE_COLORS = {
    "item": "#4caf50",      # green
    "delivery": "#2196f3",  # blue
    "other": "#9e9e9e",    # grey
}


def _init_base_grid(config: WarehouseGridConfig) -> Tuple[np.ndarray, np.ndarray]:
    """Create coordinate arrays for plotting the grid as a background.

    Returns:
        X, Y: meshgrid arrays for imshow/plot.
    """

    rows, cols = config.rows, config.cols
    x = np.arange(cols + 1)
    y = np.arange(rows + 1)
    X, Y = np.meshgrid(x, y)
    return X, Y


# ----------------------------- Layout plot -----------------------------

def plot_layout(config: WarehouseGridConfig, ax: plt.Axes | None = None) -> plt.Axes:
    """Plot the warehouse layout with node types on a grid.

    Args:
        config: WarehouseGridConfig with rows, cols, node_types.
        ax: optional matplotlib Axes to draw on.

    Returns:
        The Axes with the layout plotted.
    """

    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 6))

    X, Y = _init_base_grid(config)

    # Draw grid lines
    ax.set_xticks(np.arange(0, config.cols + 1, 1))
    ax.set_yticks(np.arange(0, config.rows + 1, 1))
    ax.grid(True, which="both", color="#e0e0e0", linewidth=0.8)

    # Draw node type markers
    for (r, c), t in config.node_types.items():
        color = NODE_TYPE_COLORS.get(t, "#000000")
        ax.scatter(c + 0.5, r + 0.5, s=80, color=color, edgecolors="black")

    ax.set_xlim(0, config.cols)
    ax.set_ylim(config.rows, 0)  # invert y-axis so row 0 is at the top
    ax.set_aspect("equal")
    ax.set_xlabel("Column")
    ax.set_ylabel("Row")
    ax.set_title("Warehouse layout: node types")

    return ax


# ----------------------------- Storage heatmap -----------------------------

def plot_storage_demand_heatmap(
    config: WarehouseGridConfig,
    demand: StorageDemand,
    ax: plt.Axes | None = None,
) -> plt.Axes:
    """Plot storage demand as a heatmap over item nodes.

    Args:
        config: warehouse grid config.
        demand: StorageDemand with demand per (row, col) item node.
        ax: optional Axes.
    """

    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 6))

    # Base layout
    plot_layout(config, ax=ax)

    # Build a matrix of demand values (rows x cols), zeros elsewhere.
    mat = np.zeros((config.rows, config.cols), dtype=float)
    for (r, c), val in demand.demand.items():
        if 0 <= r < config.rows and 0 <= c < config.cols:
            mat[r, c] = val

    # Overlay heatmap using alpha
    im = ax.imshow(
        mat,
        cmap="Reds",
        alpha=0.6,
        origin="upper",
        extent=[0, config.cols, config.rows, 0],
    )
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label("Storage demand / order frequency")

    ax.set_title("Storage demand heatmap over item nodes")

    return ax


# ----------------------------- Edge flow heatmap -----------------------------

def plot_edge_flows(
    config: WarehouseGridConfig,
    flows: EdgeFlows,
    ax: plt.Axes | None = None,
) -> plt.Axes:
    """Plot edge flows on top of the warehouse layout.

    Args:
        config: warehouse grid config.
        flows: EdgeFlows with flow per directed edge.
        ax: optional Axes.
    """

    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 6))

    # Base layout
    plot_layout(config, ax=ax)

    # Determine max flow for scaling line width
    max_flow = max(flows.flows.values()) if flows.flows else 1.0

    for (src, dst), val in flows.flows.items():
        (r1, c1), (r2, c2) = src, dst
        x1, y1 = c1 + 0.5, r1 + 0.5
        x2, y2 = c2 + 0.5, r2 + 0.5

        # Line width scaled by relative flow
        lw = 0.5 + 3.0 * (val / max_flow)
        ax.arrow(
            x1,
            y1,
            x2 - x1,
            y2 - y1,
            length_includes_head=True,
            head_width=0.2,
            head_length=0.2,
            linewidth=lw,
            color="#f44336",
            alpha=0.7,
        )

    ax.set_title("Edge flow heatmap (thicker arrows = more traffic)")

    return ax


# ----------------------------- Demo usage -----------------------------

if __name__ == "__main__":
    # Small demo configuration (3x4 grid)
    cfg = WarehouseGridConfig(
        rows=3,
        cols=4,
        node_types={
            (0, 0): "item",
            (0, 1): "item",
            (0, 2): "item",
            (0, 3): "delivery",
            (1, 0): "other",
            (1, 1): "other",
            (1, 2): "other",
            (1, 3): "delivery",
            (2, 0): "other",
            (2, 1): "item",
            (2, 2): "item",
            (2, 3): "other",
        },
    )

    demand = StorageDemand(
        demand={
            (0, 0): 10.0,
            (0, 1): 5.0,
            (0, 2): 2.0,
            (2, 1): 8.0,
            (2, 2): 3.0,
        }
    )

    flows = EdgeFlows(
        flows={
            ((0, 0), (0, 1)): 30.0,
            ((0, 1), (0, 2)): 45.0,
            ((0, 2), (0, 3)): 60.0,
            ((2, 1), (1, 1)): 20.0,
            ((1, 1), (1, 3)): 15.0,
        }
    )

    # Plot examples
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    plot_layout(cfg, ax=axes[0])
    plot_storage_demand_heatmap(cfg, demand, ax=axes[1])
    plot_edge_flows(cfg, flows, ax=axes[2])
    plt.tight_layout()
    plt.show()
