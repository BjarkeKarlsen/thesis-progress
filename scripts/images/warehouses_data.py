"""Extract the warehouses of warehouses.py (app:instances): four seeds of the
8-agent warehouse, and seed 42 at every fleet size.

Each warehouse is the one the episode seed draws under configs/step12 ([A73]
a warehouse per episode, [A74] stacked blocks), built by the code's own
build_seed_warehouse. Run from the workspace root:

    PYTHONPATH=slap-mapd-coupling/src ~/.venvs/rl/bin/python \
        thesis-progress/scripts/images/warehouses_data.py

It writes data/warehouses_step12.json, keyed "seeds" and "sizes".
"""
import json
import os
from pathlib import Path

from slap_mapd_coupling.training.spec import build_seed_warehouse, load_spec

CONFIGS = Path("slap-mapd-coupling/configs/step12")
OUT = os.path.join(os.path.dirname(__file__), "data", "warehouses_step12.json")
SEEDS = (42, 43, 44, 45)
FLEETS = (8, 16, 32, 64)
SIZE_SEED = 42


def _export(fleet, seed):
    instance = build_seed_warehouse(load_spec(CONFIGS / f"fleet_{fleet}.yaml"), seed).instance
    graph = instance.graph
    roles = {v: next((r for r in ("storage", "delivery", "receiving", "endpoint")
                      if getattr(vertex.role, r)), "")
             for v, vertex in graph.vertices.items()}
    return {
        "fleet": fleet,
        "seed": seed,
        "positions": {v: instance.positions[v] for v in graph.vertices},
        "roles": roles,
        "edges": [(e.source, e.target, e.one_way) for e in graph.edges],
    }


def main():
    data = {
        "seeds": [_export(8, seed) for seed in SEEDS],
        "sizes": [_export(fleet, SIZE_SEED) for fleet in FLEETS],
    }
    with open(OUT, "w") as handle:
        json.dump(data, handle)
    for key, items in data.items():
        print(key, [(d["fleet"], d["seed"], len(d["roles"])) for d in items])


if __name__ == "__main__":
    main()
