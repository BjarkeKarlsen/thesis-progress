"""Extract the warehouses of warehouses.py (app:instances): four seeds of the
8-agent warehouse, and seed 42 at every fleet size.

Each warehouse is the one the episode seed draws under the training configs
configs/fleet_<m>/section.yaml ([A73] a warehouse per episode, [A74] stacked
blocks, [A77] workstations in groups of four per category), built by the
code's own build_seed_warehouse. The section config is read so the export also
holds the zones of the section-based controller (zones_by_aisle, num_zones 3).
The instance section is the same in every arm's config and in configs/step12.
Run from the workspace root:

    PYTHONPATH=slap-mapd-coupling/src ~/.venvs/rl/bin/python \
        thesis-progress/scripts/images/warehouses_data.py

SMC_ROOT points at another copy of slap-mapd-coupling (for example an export of
origin/main), whose configs are then read. Set PYTHONPATH to its src too.

It writes data/warehouses_fleet.json, keyed "seeds" and "sizes". Per warehouse:
positions, roles, edges, "category" (each workstation's category, named by the
smallest workstation id of its group) and "zone" (each movable vertex's zone).
"""
import json
import os
from pathlib import Path

from slap_mapd_coupling.training.spec import build_seed_warehouse, load_spec

CONFIGS = Path(os.environ.get("SMC_ROOT", "slap-mapd-coupling")) / "configs"
OUT = os.path.join(os.path.dirname(__file__), "data", "warehouses_fleet.json")
SEEDS = (42, 43, 44, 45)
FLEETS = (8, 16, 32, 64)
SIZE_SEED = 42


def _export(fleet, seed):
    warehouse = build_seed_warehouse(load_spec(CONFIGS / f"fleet_{fleet}" / "section.yaml"), seed)
    instance = warehouse.instance
    graph = instance.graph
    roles = {v: next((r for r in ("storage", "delivery", "receiving", "endpoint")
                      if getattr(vertex.role, r)), "")
             for v, vertex in graph.vertices.items()}
    category = {v: (v if vertex.section is None else vertex.section)
                for v, vertex in graph.vertices.items() if vertex.role.delivery}
    zone = {v: z for z, members in enumerate(warehouse.zones or ()) for v in members}
    return {
        "fleet": fleet,
        "seed": seed,
        "positions": {v: instance.positions[v] for v in graph.vertices},
        "roles": roles,
        "edges": [(e.source, e.target, e.one_way) for e in graph.edges],
        "category": category,
        "zone": zone,
        "aisle": {v: instance.aisle_index[v] for v in graph.vertices},
    }


def main():
    data = {
        "seeds": [_export(8, seed) for seed in SEEDS],
        "sizes": [_export(fleet, SIZE_SEED) for fleet in FLEETS],
    }
    with open(OUT, "w") as handle:
        json.dump(data, handle)
    for key, items in data.items():
        print(key, [(d["fleet"], d["seed"], len(d["roles"]),
                     len(set(d["category"].values())), len(set(d["zone"].values())))
                    for d in items])


if __name__ == "__main__":
    main()
