"""Extract the 8-agent warehouse that instance.py, instance_simple.py and
observation.py draw (m8.py loads it).

The warehouse is the one of configs/step12/fleet_8.yaml (seed 42, stacked blocks,
[A74]). Run from the workspace root:

    PYTHONPATH=slap-mapd-coupling/src ~/.venvs/rl/bin/python \
        thesis-progress/scripts/images/instance_data.py

It writes data/warehouse_m8.json, so the figure scripts run without
slap_mapd_coupling.
"""
import json
import os
from pathlib import Path

from slap_mapd_coupling.training.spec import build_instance, load_spec

CONFIG = Path("slap-mapd-coupling/configs/step12/fleet_8.yaml")
OUT = os.path.join(os.path.dirname(__file__), "data", "warehouse_m8.json")


def main():
    instance = build_instance(load_spec(CONFIG))
    graph = instance.graph
    roles = {}
    for v, vertex in graph.vertices.items():
        roles[v] = next((r for r in ("storage", "delivery", "receiving", "endpoint")
                         if getattr(vertex.role, r)), "")
    data = {
        "positions": {v: instance.positions[v] for v in graph.vertices},
        "roles": roles,
        "edges": [(e.source, e.target, e.one_way) for e in graph.edges],
    }
    with open(OUT, "w") as handle:
        json.dump(data, handle, indent=1)
    print(f"wrote {OUT}: {len(roles)} vertices, {len(data['edges'])} edges")


if __name__ == "__main__":
    main()
