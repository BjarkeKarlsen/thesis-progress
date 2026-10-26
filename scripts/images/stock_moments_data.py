"""Extract the data of stock_moments.py from three episode traces (format 2).

Run from the workspace root:

    python thesis-progress/scripts/images/stock_moments_data.py RUN_DIR

RUN_DIR is a load_sweep.py output with one trace per storage rule in
traces/ (made with --trace-seeds 1). The traces are several megabytes and
stay off git. This script keeps only the warehouse and, at each moment, the
units per slot by popularity rank, the picks waiting per slot and the
put-aways delivered to each slot so far, in data/stock_moments.json.
"""

import json
import os
import sys

DATA = os.path.join(os.path.dirname(__file__), "data", "stock_moments.json")
RULES = ("fixed", "demand", "random")
# After a warm-up stand-in of 1000 steps, then a quarter and a half demand
# cycle (4000 steps) later. The warm-up is set by test C (Welch's method), so
# the moments are provisional until it has run.
MOMENTS = (1000, 2000, 3000)


def _lines(path):
    with open(path) as handle:
        return [json.loads(line) for line in handle if line.strip()]


def main(run_dir):
    traces = os.path.join(run_dir, "traces")
    out = {"moments": MOMENTS, "rules": {}}
    for rule in RULES:
        (name,) = [f for f in os.listdir(traces) if f.startswith(f"{rule}_")]
        lines = _lines(os.path.join(traces, name))
        header = lines[0]
        if "warehouse" not in out:
            out["warehouse"] = {
                "positions": header["positions"],
                "roles": {str(v["id"]): [r for r in ("storage", "delivery", "receiving", "endpoint")
                                         if v[r]] for v in header["vertices"]},
                "edges": [[s, t] for s, t, _ in header["edges"]],
                "capacities": header["capacities"],
            }
            out["config"] = {k: header["config"][k] for k in
                             ("planner", "num_agents", "arrival_rate", "seed", "horizon")}
        sizes = header["skus"]
        stock = {line["t"]: line for line in lines if line["type"] == "stock"}
        putaways = [task for task in lines[-1]["tasks"] if task["kind"] == "putaway"]
        moments = {}
        for t in MOMENTS:
            line = stock[t]
            rank = {k: i for i, k in enumerate(line["ranking"])}
            moments[str(t)] = {
                "skus": len(rank),
                "slots": {
                    v: {
                        # (rank, space used) per SKU, most popular first
                        "fill": sorted((rank[k], u * sizes[k]) for k, u in e["units"].items()),
                        "waiting": e["queued"] + e["coming"],
                    }
                    for v, e in line["shelves"].items()
                },
                # The slots that a put-away has reached by t, the storage rule's decisions.
                "stored": sorted({task["to"] for task in putaways
                                  if task["finished"] is not None and task["finished"] <= t}),
            }
        out["rules"][rule] = moments
    with open(DATA, "w") as handle:
        json.dump(out, handle, separators=(",", ":"))
    print("wrote", DATA)


if __name__ == "__main__":
    main(sys.argv[1])
