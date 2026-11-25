import collections, json, sys
from pathlib import Path
from slap_mapd_coupling.training.spec import load_spec
from slap_mapd_coupling.training.warehouses import WarehousePool

def lane(g, w):
    return all(len(g.out_neighbours(a)) <= 3 for a in g.out_neighbours(w))

out = {}
for m in (8, 16, 32, 64):
    spec = load_spec(Path(f"configs/fleet_{m}/decentralised.yaml"))
    spec = spec.model_copy(update={"warehouse_store": str(Path.home() / "thesis_runs/warehouses")})
    pool = WarehousePool(spec, Path.home() / "thesis_runs/warehouses")
    seeds = list(range(200000, 200020))
    pool.prepare(seeds)
    for s in seeds:
        g = pool.warehouse(s).instance.graph
        cats = collections.defaultdict(list)
        for v, vx in g.vertices.items():
            if vx.role.delivery:
                cats[vx.section].append(v)
        lane_ws = sum(lane(g, w) for ws in cats.values() for w in ws)
        all_ws = sum(len(ws) for ws in cats.values())
        full = sum(all(lane(g, w) for w in ws) for ws in cats.values())
        out[f"{m}_{s}"] = dict(categories=len(cats), workstations=all_ws, lane_ws=lane_ws, cats_all_lane=full)
    print(m, "seeds with a category all on one-lane:", sum(out[f'{m}_{s}']['cats_all_lane'] > 0 for s in seeds), "of 20;",
          "lane workstations share", round(sum(out[f'{m}_{s}']['lane_ws'] for s in seeds) / sum(out[f'{m}_{s}']['workstations'] for s in seeds), 2),
          "categories", out[f'{m}_200000']['categories'], "ws", out[f'{m}_200000']['workstations'], flush=True)
json.dump(out, open(sys.argv[1], "w"), indent=0)
