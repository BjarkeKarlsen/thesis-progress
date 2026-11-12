"""The numbers behind [A91], agents that lock at a workstation on a one-lane aisle.

Three commands, run from a `slap-mapd-coupling` checkout with the venv's python, since `layout`
builds warehouses with its code and reads its configs:

    cd ~/worktrees/train-0c5427b
    ~/.venvs/rl/bin/python ~/Documents/thesis/thesis-progress/scripts/workstation_lock.py \
        layout --fleet 8 [--test-seeds 20]
    ... workstation_lock.py traces TRACE.jsonl [TRACE.jsonl ...] [--held 500]
    ... workstation_lock.py frame TRACE.jsonl --t 1500

`layout` counts the warehouse seeds of a fleet (training, validation and test seeds of
configs/fleet_<m>/decentralised.yaml) with a section whose workstations all hang off a one-lane
aisle vertex. A one-lane aisle vertex has at most 3 neighbours: the aisle before it, the aisle after
it and the workstation, so an agent queuing on it blocks the only way out. `--test-seeds` lists that
many test seeds instead of the config's count.

`traces` reads per-step traces (trace_episode.py, `slap-mapd evaluate --trace-seeds`) and says which
are locked. A seed is locked when at least two agents each hold the same task for `--held` steps or
more at the same time (author, 2026-11-12). The default 500 is a quarter of a 2000-step episode.

`frame` writes the agents and the warehouse near the busiest workstation at step `--t` to
scripts/images/data/workstation_lock_t<t>.json, which scripts/images/workstation_lock.py draws.

The results and the exact commands are in results/limitations/workstation_lock/README.md.
"""

import argparse
import collections
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FRAMES = HERE / "images" / "data"


def lane_workstations(out_neighbours, workstations):
    """The workstations whose every neighbour is a one-lane aisle vertex (at most 3 neighbours)."""
    return [w for w in workstations if all(len(out_neighbours(a)) <= 3 for a in out_neighbours(w))]


def layout(args):
    from slap_mapd_coupling.training.config import SeedSplitConfig, split_seeds
    from slap_mapd_coupling.training.spec import build_instance, load_spec, seed_spec

    spec = load_spec(Path(f"configs/fleet_{args.fleet}/decentralised.yaml"))
    split = split_seeds(SeedSplitConfig(
        training_seed=spec.experiment.seed,
        train_seed_count=spec.train_seed_count,
        validation_seed_count=spec.validation_seed_count,
        test_seed_count=args.test_seeds or spec.test_seed_count,
    ))
    groups = {"train": split.train, "validation": split.validation, "test": split.test}
    result = {"fleet": args.fleet, "rule": "every neighbour of every workstation of one section "
              "has at most 3 neighbours", "groups": {}}
    for name, seeds in groups.items():
        locked_layout = []
        for seed in seeds:
            graph = build_instance(seed_spec(spec, seed)).graph
            sections = collections.defaultdict(list)
            for v, vertex in graph.vertices.items():
                if vertex.role.delivery:
                    sections[vertex.section].append(v)
            if any(len(lane_workstations(graph.out_neighbours, ws)) == len(ws)
                   for ws in sections.values()):
                locked_layout.append(seed)
        result["groups"][name] = {"seeds": len(seeds), "with_layout": len(locked_layout),
                                  "share": round(len(locked_layout) / len(seeds), 3),
                                  "which": locked_layout}
        print(f"fleet {args.fleet} {name}: {len(locked_layout)} of {len(seeds)} seeds "
              f"({len(locked_layout) / len(seeds):.0%}) have a section on one-lane aisles"
              + (f", {locked_layout}" if name == "test" else ""))
    total = sum(g["seeds"] for g in result["groups"].values())
    hit = sum(g["with_layout"] for g in result["groups"].values())
    print(f"fleet {args.fleet} all: {hit} of {total} ({hit / total:.0%})")
    print(json.dumps(result))


def held_times(path):
    """Per step, how long each agent has held its current task. Yields (t, step, {agent: steps})."""
    start = {}
    with open(path) as f:
        header = json.loads(f.readline())
        yield None, header, None
        for line in f:
            step = json.loads(line)
            if step["type"] != "step":
                continue
            t = step["t"]
            for agent, state in step["agents"].items():
                if state["task"] is None:
                    start.pop(agent, None)
                elif start.get(agent, (None,))[0] != state["task"]:
                    start[agent] = (state["task"], t)
            yield t, step, {a: t - s for a, (_, s) in start.items()}


def traces(args):
    rows = []
    for path in args.trace:
        first, completed, last_t = None, 0, 0
        for t, step, held in held_times(path):
            if t is None:
                config = step["config"]
                continue
            long_held = sorted(a for a, h in held.items() if h >= args.held)
            if first is None and len(long_held) >= 2:
                first = (t, long_held)
            completed, last_t = step["completed"], t
        row = {"trace": str(path), "seed": config["seed"], "agents": config["num_agents"],
               "storage": config["storage_mode"], "communication": config["communication"],
               "locked": first is not None, "from_t": first and first[0],
               "agents_at_lock": first and first[1], "completed": completed, "steps": last_t}
        rows.append(row)
        print(f"{Path(path).name}: {'LOCKED from t = %d, agents %s' % first if first else 'not locked'}"
              f", {completed} tasks in {last_t} steps")
    print(f"{sum(r['locked'] for r in rows)} of {len(rows)} locked (two agents holding a task "
          f"for {args.held} steps or more at once)")
    if args.out:
        Path(args.out).write_text(json.dumps(rows, indent=1))


def frame(args):
    for t, step, held in held_times(args.trace):
        if t is None:
            header = step
        elif t == args.t:
            break
    else:
        raise SystemExit(f"no step {args.t} in {args.trace}")
    vertices = {v["id"]: v for v in header["vertices"]}
    out = collections.defaultdict(set)
    for a, b, _ in header["edges"]:
        out[a].add(b)
    goals = collections.Counter(s["goal"] for s in step["agents"].values()
                                if s["phase"] == "to_delivery")
    target = goals.most_common(1)[0][0]
    section = vertices[target]["section"]
    workstations = [v for v, x in vertices.items() if x["delivery"] and x["section"] == section]
    data = {
        "trace": str(args.trace), "t": args.t, "seed": header["config"]["seed"],
        "agents_in_fleet": header["config"]["num_agents"], "workstation": target,
        "section_workstations": workstations,
        "lane_workstations": lane_workstations(lambda v: out[v], workstations),
        "completed": step["completed"],
        "positions": header["positions"],
        "edges": [[a, b] for a, b, _ in header["edges"]],
        "roles": {v: ("delivery" if x["delivery"] else "storage" if x["storage"] else
                      "dock" if x["receiving"] else "endpoint" if x["endpoint"] else "aisle")
                  for v, x in vertices.items()},
        "agents": {a: {"at": s["at"], "intent": s["intent"], "goal": s["goal"],
                       "phase": s["phase"], "held": held.get(a)}
                   for a, s in step["agents"].items()},
    }
    path = FRAMES / f"workstation_lock_t{args.t}.json"
    FRAMES.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=1))
    print(f"wrote {path}, workstation {target}, {data['completed']} tasks done by t = {args.t}")


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("layout")
    p.add_argument("--fleet", type=int, required=True)
    p.add_argument("--test-seeds", type=int, default=None)
    p.set_defaults(run=layout)
    p = sub.add_parser("traces")
    p.add_argument("trace", nargs="+")
    p.add_argument("--held", type=int, default=500)
    p.add_argument("--out", default=None)
    p.set_defaults(run=traces)
    p = sub.add_parser("frame")
    p.add_argument("trace")
    p.add_argument("--t", type=int, required=True)
    p.set_defaults(run=frame)
    args = parser.parse_args()
    args.run(args)


if __name__ == "__main__":
    main()
