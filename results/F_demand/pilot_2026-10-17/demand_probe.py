"""Probe of skewed and drifting demand with the reference planner, to choose the demand values.

Nothing here is in the repo. The script patches the order draw of the simulator at run time, so
the repo's code is unchanged, and it runs Token Passing only (no training, no GPU).

The demand model under test (thesis_decisions.md #1, options b and c):
- SKU popularity follows a Zipf law. The SKU at rank r (0 is the most popular) has weight
  1 / (r + 1)^s, so s = 0 is today's uniform demand.
- Every P steps the ranking rotates by `shift` places, so the hot SKUs cool down and others
  heat up. P = 0 means no rotation (a fixed skew).
- The order stream draws the same random numbers as today (one count, then three uniform numbers
  per order). Only the mapping of the SKU number changes, from uniform to the popularity at that
  step. So for a seed the orders are identical under every storage rule, and the pairing holds.
- The starting stock is placed once from the popularity at t = 0, the same under every storage
  rule. The storage vertices are ordered by their mean distance to the delivery vertices.
  "cyclic" gives rank r the vertex r mod |V_str|, so the hot SKUs are spread over all vertices,
  nearest first. "blocks" gives the nearest vertex the first K / |V_str| ranks, the next vertex
  the next block, and so on, so the hot SKUs share the nearest vertices (class-based storage).

Two changes to the storage side, also patched at run time (thesis_decisions.md #21 and #19):
- Wait rule "standing" (the default). A step where a robot serving a task stands still is
  charged to the next edge on its shortest route to its goal, whatever kept it there. The repo
  counts a wait only when conflict resolution overrides a move ("overridden"), so under Token
  Passing, which is never overridden, the wait estimate is always 0 and F_cng equals F_dem.
- Rule "congestion_rho". F_cng with the congestion term weighted by the SKU's demand,
  score(k, v) = rho_hat(k) * (d(v) + beta * exposure(v)), so every SKU trades distance against
  congestion the same way. In the repo's score, rho_hat(k) * d(v) + beta * exposure(v), the
  congestion term weighs most for rarely ordered SKUs and least for popular ones.
- Rule "congestion_v2" (ideas 1 to 3 of 2026-10-17). Every SKU ranks vertex v by
  access(v) + beta * delay(v), both in steps per trip:
    access(v) = the mean distance from v to the delivery vertices (orders pick one uniformly);
    delay(v)  = the mean over the delivery vertices g of the sum, along the shortest path
                v -> g, of the predicted waits per crossing q(e) + c * L(e), where
                q(e) = w_hat(e) / mu_hat(e) is the measured waits per crossing (0 on an edge not
                crossed), L(e) the trips per step that the SKUs already placed in this update
                send over e, and c the slope of waits per crossing against traffic, fitted over
                all edges of the window (w_hat = c * mu_hat^2 by least squares). c has no free
                value, it comes from the window like the estimates.
  So beta = 1 counts a step of waiting like a step of travel, and a second popular SKU on the
  same corridor pays for the first one's traffic. SKUs go in descending demand, as in F_dem,
  and the relocation cap is applied the same way.

The instance is the 8-agent warehouse of the night of 2026-10-16 (94 vertices, 10 storage
vertices), read from that night's config. The number of SKUs is swept (--num-skus), with 8 units
each and a vertex capacity of 200 for every count, so the space is the same across the grid. The
night itself had 20 SKUs and capacity 100, which holds at most 100 SKUs.

With --checkpoints, a trained arm of the night replaces Token Passing. Each entry is
RUN_DIR/CHECKPOINT, for example runs/decentralised_seed0/checkpoint_000002 under the night's
folder. The arm, its encoding and the reward settings come from the run's spec, and only the
SKUs, the starting stock, the demand and the storage rule change. The night's policies were
trained on 20 SKUs under uniform demand and fixed storage, so this is a first indication only.

For every (s, P, storage rule, arrival rate, seed) one episode is played. Rows go to
OUT/rows.jsonl as they finish, a row already there is skipped, and OUT/summary.md is written at
the end, with the gain of each adaptive rule over fixed storage paired seed by seed.

    cd ~/thesis_runs/demand_probe
    PYTHONPATH=~/Documents/thesis/slap-mapd-coupling/src ~/.venvs/rl/bin/python demand_probe.py
"""

from __future__ import annotations

import argparse
import itertools
import json
import statistics
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

HERE = Path(__file__).resolve().parent
NIGHT_CONFIG = Path.home() / "thesis_runs" / "night_2026-10-16" / "configs" / "decentralised.yaml"
FIELDS = (
    "num_completed_tasks",
    "throughput",
    "backlog",
    "mean_service_time",
    "mean_wait_for_agent",
    "mean_travel_time",
    "mean_blocked_time",
    "mean_crowding",
    "num_storage_updates",
    "mean_relocated_units",
)


def by_number(skus) -> list[str]:
    """SKU names in numeric order. Sorting the names as text puts sku_100 before sku_11."""
    return sorted(skus, key=lambda name: int(name.rsplit("_", 1)[1]))


def popularity_order(skus: list[str], t: int, period: int, shift: int) -> list[str]:
    """The SKUs from most to least popular at step t. Rank 0 starts at sku_00."""
    if period <= 0:
        return list(skus)
    turns = (t // period) * shift
    offset = turns % len(skus)
    return skus[offset:] + skus[:offset]


def zipf_weights(count: int, skew: float) -> list[float]:
    raw = [1.0 / (rank + 1) ** skew for rank in range(count)]
    total = sum(raw)
    return [w / total for w in raw]


def patch_order_draw(skew: float, period: int, shift: int) -> None:
    """Replaces WarehouseMAPDEnv._generate_tasks with the popularity draw. Runs in a worker."""
    import bisect

    from slap_mapd_coupling.core.tasks import Task
    from slap_mapd_coupling.environment.multi_agent_env import WarehouseMAPDEnv

    def generate_tasks(self) -> list:
        num_new = int(self._order_rng.poisson(self.config.arrival_rate))
        if num_new == 0:
            return []
        draws = self._order_rng.random((num_new, 3))
        vertices_by_sku = {
            sku_id: sorted(vertex for vertex, count in per_vertex.items() if count > 0)
            for sku_id, per_vertex in sorted(self.storage.counts.items())
        }
        delivery_vertices = sorted(
            v for v, vertex in self.graph.vertices.items() if vertex.role.delivery
        )
        ranked = popularity_order(by_number(vertices_by_sku), self._t, period, shift)
        weights = zipf_weights(len(ranked), skew)
        # Out of stock SKUs keep their rank but get no weight, as the stock condition requires.
        in_stock = [(sku, w) for sku, w in zip(ranked, weights) if vertices_by_sku[sku]]
        if not in_stock or not delivery_vertices:
            return []
        total = sum(w for _, w in in_stock)
        cumulative, running = [], 0.0
        for _, w in in_stock:
            running += w / total
            cumulative.append(running)
        new_tasks = []
        for u_sku, u_pickup, u_delivery in draws:
            index = min(bisect.bisect_right(cumulative, u_sku), len(in_stock) - 1)
            sku_id = in_stock[index][0]
            pickup_candidates = vertices_by_sku[sku_id]
            new_tasks.append(
                Task(
                    task_id=self._next_task_id,
                    release_time=self._t,
                    pickup_vertex=pickup_candidates[int(u_pickup * len(pickup_candidates))],
                    delivery_vertex=delivery_vertices[int(u_delivery * len(delivery_vertices))],
                    sku=sku_id,
                )
            )
            self._next_task_id += 1
        return new_tasks

    WarehouseMAPDEnv._generate_tasks = generate_tasks


_WAITS = {"attributed": 0}
_ORIGINALS: dict = {}


def reset_patches() -> None:
    """Puts back the repo's own functions. Worker processes are reused between episodes, so
    without this a patch of one episode would leak into the next (a congestion episode would
    run another rule, and the wait rule would stack and charge every wait several times)."""
    import slap_mapd_coupling.storage.congestion as congestion
    from slap_mapd_coupling.environment.multi_agent_env import EpisodeLog, WarehouseMAPDEnv
    from slap_mapd_coupling.storage import registry

    if not _ORIGINALS:
        _ORIGINALS.update(
            step=WarehouseMAPDEnv.step,
            tick=EpisodeLog.record_blocked_tick,
            generate=WarehouseMAPDEnv._generate_tasks,
            score=congestion.score,
            rule=registry._REGISTRY["congestion"],
        )
    WarehouseMAPDEnv.step = _ORIGINALS["step"]
    EpisodeLog.record_blocked_tick = _ORIGINALS["tick"]
    WarehouseMAPDEnv._generate_tasks = _ORIGINALS["generate"]
    congestion.score = _ORIGINALS["score"]
    registry._REGISTRY["congestion"] = _ORIGINALS["rule"]


def patch_wait_attribution() -> None:
    """Charges a standing-still step of a robot serving a task to the next edge on its route.
    Hooks EpisodeLog.record_blocked_tick, which the env calls for exactly those steps, inside
    the step and before the storage update, so the wait lands in the right window. A robot
    overridden on a move is skipped, because the env has already charged that move's edge."""
    from slap_mapd_coupling.environment.multi_agent_env import EpisodeLog, WarehouseMAPDEnv

    original_step = WarehouseMAPDEnv.step
    original_tick = EpisodeLog.record_blocked_tick

    def step(self, *args, **kwargs):
        self.log._probe_env = self
        return original_step(self, *args, **kwargs)

    def record_blocked_tick(self, task_id):
        original_tick(self, task_id)
        env = getattr(self, "_probe_env", None)
        if env is None:
            return
        task = next(t for t in env.tasks if t.task_id == task_id)
        agent = task.assigned_agent
        if agent is None or agent in env.last_overridden:
            return
        at = env.fleet.locations()[agent]
        goal = task.delivery_vertex if task.pickup_time is not None else task.pickup_vertex
        if at == goal:
            return
        if not hasattr(env, "_probe_cost"):
            env._probe_cost = {(e.source, e.target): e.cost for e in env.graph.edges}
        cost = env._probe_cost
        nxt = min(env.graph.out_neighbours(at),
                  key=lambda w: (cost[(at, w)] + env.graph.distance(w, goal), w))
        env._estimator.record_wait((at, nxt))
        _WAITS["attributed"] += 1

    WarehouseMAPDEnv.step = step
    EpisodeLog.record_blocked_tick = record_blocked_tick


def patch_demand_weighted_congestion() -> None:
    """F_cng's score with the congestion term weighted by the SKU's demand."""
    import slap_mapd_coupling.storage.congestion as congestion

    def score(graph, sku_id, vertex, delivery, demand_estimate, traversal_estimate,
              waiting_estimate, congestion_weight):
        nearest = congestion.nearest_delivery_point(graph, vertex, delivery)
        base = graph.distance(vertex, nearest) + congestion_weight * congestion.congestion_exposure(
            graph, vertex, nearest, traversal_estimate, waiting_estimate)
        # A SKU with no orders in the window still ranks its vertices by the same trade-off.
        return max(demand_estimate.get(sku_id, 0.0), 1e-9) * base

    congestion.score = score


def patch_congestion_v2() -> None:
    """Replaces the registered "congestion" rule with congestion_v2 in this process."""
    import slap_mapd_coupling.storage.congestion as congestion
    from slap_mapd_coupling.core.storage_state import StorageState
    from slap_mapd_coupling.storage import registry
    from slap_mapd_coupling.storage.base import no_orders_in_window
    from slap_mapd_coupling.storage.demand import delivery_vertices, storage_vertices
    from slap_mapd_coupling.storage.relocation import apply_relocation_cap

    paths_cache: dict = {}

    def f_v2(x_prev, graph, reassignment_cap, congestion_weight, demand_estimate,
             traversal_estimate, waiting_estimate):
        if no_orders_in_window(demand_estimate):
            return x_prev
        storage, delivery = storage_vertices(graph), delivery_vertices(graph)
        key = id(graph)
        if key not in paths_cache:
            paths_cache[key] = {
                v: [congestion._shortest_path_edges(graph, v, g) for g in delivery]
                for v in storage
            }
        paths = paths_cache[key]
        access = {v: statistics.mean(graph.distance(v, g) for g in delivery) for v in storage}

        # Waits per crossing rise with traffic, w_hat(e) / mu_hat(e) = c * mu_hat(e).
        squares = sum(mu * mu for mu in traversal_estimate.values())
        slope = (sum(waiting_estimate.get(e, 0.0) * mu for e, mu in traversal_estimate.items())
                 / squares if squares > 0 else 0.0)
        measured = {e: waiting_estimate.get(e, 0.0) / mu
                    for e, mu in traversal_estimate.items() if mu > 0.0}

        def waits_per_crossing(e, load):
            return measured.get(e, 0.0) + slope * load.get(e, 0.0)

        def delay(v, load):
            return statistics.mean(sum(waits_per_crossing(e, load) for e in path)
                                   for path in paths[v])

        load: dict = {}
        remaining = dict(x_prev.capacities)
        counts = {k: {} for k in x_prev.skus}
        placements = []
        for sku_id in sorted(x_prev.skus, key=lambda k: (-demand_estimate.get(k, 0.0), k)):
            units = sum(x_prev.counts.get(sku_id, {}).values())
            size = x_prev.skus[sku_id].unit_capacity
            rho = demand_estimate.get(sku_id, 0.0)
            ranked = sorted(storage, key=lambda v: (
                access[v] + congestion_weight * delay(v, load), v))
            left = units
            for v in ranked:
                if left <= 0:
                    break
                fit = int(remaining[v] // size)
                if fit <= 0:
                    continue
                place = min(fit, left)
                counts[sku_id][v] = counts[sku_id].get(v, 0) + place
                remaining[v] -= place * size
                left -= place
                placements.append((sku_id, v))
                # This SKU's trips from v, split over the delivery vertices.
                share = rho * place / units / len(delivery) if units else 0.0
                for path in paths[v]:
                    for e in path:
                        load[e] = load.get(e, 0.0) + share
        x_target = StorageState(skus=x_prev.skus, capacities=x_prev.capacities, counts=counts)
        priority = [(k, v) for k, v in placements if x_target.units(k, v) > x_prev.units(k, v)]
        return apply_relocation_cap(x_prev, x_target, priority, reassignment_cap)

    registry._REGISTRY["congestion"] = f_v2


def place_by_popularity(graph, skus, counts, placement="cyclic"):
    """The starting stock with the most popular SKUs nearest the delivery vertices (t = 0)."""
    delivery = [v for v, vertex in graph.vertices.items() if vertex.role.delivery]
    storage = sorted(
        (v for v, vertex in graph.vertices.items() if vertex.role.storage),
        key=lambda v: (statistics.mean(graph.distance(v, d) for d in delivery), v),
    )
    placed = {}
    ranked = by_number(skus)  # sku_00 is rank 0 at t = 0
    block = -(-len(ranked) // len(storage))  # ceil, so every SKU has a vertex
    for i, sku_id in enumerate(ranked):
        units = sum(counts[sku_id].values())
        vertex = storage[i % len(storage)] if placement == "cyclic" else storage[i // block]
        placed[sku_id] = {vertex: units}
    used = {}
    for sku_id, per_vertex in placed.items():
        for vertex, units in per_vertex.items():
            used[vertex] = used.get(vertex, 0.0) + units * skus[sku_id].unit_capacity
    return placed, used


def load_night_spec(path: Path):
    """A night config (YAML) or run spec (JSON). They predate the seed scheme of #169, so their
    eval_seed_count becomes the validation and test counts of the new split."""
    import yaml

    from slap_mapd_coupling.training.spec import TrainingSpec

    data = yaml.safe_load(path.read_text(encoding="utf-8"))  # YAML reads JSON too
    if "eval_seed_count" in data:
        data.pop("eval_seed_count")
        data.setdefault("validation_seed_count", 2)
        data.setdefault("test_seed_count", 6)
    return TrainingSpec.model_validate(data)


def learned_setup(job: dict, storage_settings_update: dict):
    """The study of a night run, with the probe's SKUs and capacity, and its policy."""
    import torch

    torch.set_num_threads(1)
    from slap_mapd_coupling.training.policy import ModulePolicy
    from slap_mapd_coupling.training.spec import (
        build_experiment_config,
        build_storage,
        build_study,
    )
    from slap_mapd_coupling.training.trainer import load_module

    run = Path(job["router_dir"])
    spec = load_night_spec(next(run.glob("*_spec.json")))
    study = build_study(spec)
    storage = spec.storage.model_copy(update=storage_settings_update)
    skus, capacities, counts = build_storage(storage, study.instance.graph)
    checkpoint = next(run.glob(f"*/PPO_*/{job['router_checkpoint']}"))
    policy = ModulePolicy(load_module(checkpoint))
    base = build_experiment_config(spec, job["seed"])
    return study, skus, capacities, counts, base, policy


def play(job: dict) -> dict:
    import slap_mapd_coupling.storage.congestion  # noqa: F401 -- registers the rules
    import slap_mapd_coupling.storage.demand  # noqa: F401
    import slap_mapd_coupling.storage.fixed  # noqa: F401
    from slap_mapd_coupling.evaluation.evaluator import run_episode
    from slap_mapd_coupling.training.spec import build_instance, build_storage

    reset_patches()
    patch_order_draw(job["skew"], job["period"], job["shift"])
    if job["wait_rule"] == "standing":
        patch_wait_attribution()
    if job["rule"] == "congestion_rho":
        patch_demand_weighted_congestion()
    if job["rule"] == "congestion_v2":
        patch_congestion_v2()
    _WAITS["attributed"] = 0
    storage_update = {"num_skus": job["num_skus"], "initial_units": job["units"],
                      "vertex_capacity": job["capacity"]}
    if job["router"] == "token_passing":
        spec = load_night_spec(Path(job["config"]))
        instance = build_instance(spec)
        skus, capacities, counts = build_storage(
            spec.storage.model_copy(update=storage_update), instance.graph)
        e = spec.experiment
    else:
        study, skus, capacities, counts, base, policy = learned_setup(job, storage_update)
        instance = study.instance
    counts, used = place_by_popularity(instance.graph, skus, counts, job["placement"])
    over = {v: u for v, u in used.items() if u > job["capacity"]}
    if over:
        raise ValueError(f"the {job['placement']} placement overfills vertices {over}")
    rule = "congestion" if job["rule"].startswith("congestion") else job["rule"]
    adaptive = rule != "fixed"
    from slap_mapd_coupling.core.experiment_config import ExperimentConfig

    storage_fields = dict(
        storage_mode=rule,
        storage_epoch_length=job["delta"] if adaptive else None,
        reassignment_cap=job["nu"] if adaptive else None,
        congestion_weight=job["beta"] if rule == "congestion" else None,
    )
    start = time.time()
    if job["router"] != "token_passing":
        config = ExperimentConfig.model_validate({
            **base.model_dump(), **storage_fields,
            "arrival_rate": job["rate"], "horizon": job["horizon"], "seed": job["seed"]})
        metrics = run_episode(
            instance.graph, skus, counts, capacities, config, policy=policy,
            encoding_config=study.arm.encoding, zones=study.arm.zones, pooling=study.arm.pooling)
        return row_of(job, start, metrics)
    config = ExperimentConfig(
        storage_mode=rule,
        planner="token_passing",
        congestion_sensitive=False,
        communication=False,
        num_agents=e.num_agents,
        arrival_rate=job["rate"],
        keep_up_threshold=e.keep_up_threshold,
        seed=job["seed"],
        horizon=job["horizon"],
        wait_cost=e.wait_cost,
        observation_depth=e.observation_depth,
        storage_epoch_length=job["delta"] if adaptive else None,
        reassignment_cap=job["nu"] if adaptive else None,
        congestion_weight=job["beta"] if rule == "congestion" else None,
    )
    metrics = run_episode(instance.graph, skus, counts, capacities, config)
    return row_of(job, start, metrics)


def row_of(job: dict, start: float, metrics) -> dict:
    return {
        "router": job["router"],
        **{k: job[k] for k in ("num_skus", "placement", "units", "capacity", "skew", "period",
                               "shift", "rule", "wait_rule", "rate", "seed", "delta", "nu",
                               "beta", "horizon")},
        "waits_attributed": _WAITS["attributed"],
        "seconds": round(time.time() - start, 1),
        **{name: getattr(metrics, name) for name in FIELDS},
    }


KEY = ("router", "wait_rule", "num_skus", "placement", "skew", "period", "rule", "rate", "seed", "delta",
       "nu", "beta")


def key(row: dict) -> tuple:
    return tuple(row.get(k, "token_passing") if k == "router" else row[k] for k in KEY)


def summary(out: Path) -> None:
    rows = [json.loads(line) for line in (out / "rows.jsonl").read_text().splitlines() if line]
    def paired(r):
        return (r.get("router", "token_passing"), r["wait_rule"], r["num_skus"], r["placement"], r["skew"], r["period"], r["rate"],
                r["seed"])

    fixed = {paired(r): r for r in rows if r["rule"] == "fixed"}
    groups: dict[tuple, list[dict]] = {}
    for r in rows:
        groups.setdefault((r.get("router", "token_passing"), r["rate"], r["num_skus"], r["placement"], r["skew"], r["period"],
                           r["rule"], r["delta"], r["nu"], r["beta"]), []).append(r)

    def mean_sd(values):
        if not values:
            return "n/a"
        sd = f" ± {statistics.stdev(values):.3f}" if len(values) > 1 else ""
        return f"{statistics.mean(values):.3f}{sd}"

    lines = [
        "Token Passing on the 8-agent warehouse, mean ± spread over seeds. The gain is adaptive "
        "minus fixed throughput, paired by seed, for the same skew and rotation.",
        "",
        "| router | rate | SKUs | placement | skew s | period P | rule | Δ | ν | β | throughput | "
        "gain over fixed | service time | travel | blocked | crowding | relocated per update | "
        "waits charged per step |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for (router, rate, num_skus, placement, skew, period, rule, delta, nu, beta), items in sorted(
        groups.items(), key=lambda kv: tuple(str(x).zfill(8) for x in kv[0])
    ):
        gains = [r["throughput"] - fixed[paired(r)]["throughput"]
                 for r in items if paired(r) in fixed and rule != "fixed"]
        adaptive = rule != "fixed"
        lines.append(
            f"| {router} | {rate} | {num_skus} | {placement} | {skew} | {period or 'none'} | {rule} | "
            f"{delta if adaptive else ''} | "
            f"{nu if adaptive else ''} | {beta if rule.startswith('congestion') else ''} | "
            f"{mean_sd([r['throughput'] for r in items])} | {mean_sd(gains) if adaptive else ''} | "
            f"{statistics.mean(r['mean_service_time'] or 0 for r in items):.1f} | "
            f"{statistics.mean(r['mean_travel_time'] or 0 for r in items):.1f} | "
            f"{statistics.mean(r['mean_blocked_time'] or 0 for r in items):.2f} | "
            f"{statistics.mean(r['mean_crowding'] or 0 for r in items):.3f} | "
            f"{statistics.mean(r['mean_relocated_units'] for r in items):.1f} | "
            f"{statistics.mean(r['waits_attributed'] / r['horizon'] for r in items):.2f} |"
        )
    (out / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--config", type=Path, default=NIGHT_CONFIG)
    parser.add_argument("--out", type=Path, default=HERE / "out")
    parser.add_argument("--num-skus", type=int, nargs="+", default=[20, 50, 100, 200])
    parser.add_argument("--placements", nargs="+", default=["cyclic", "blocks"],
                        choices=["cyclic", "blocks"])
    parser.add_argument("--units", type=int, default=8, help="starting units per SKU")
    parser.add_argument("--capacity", type=float, default=200.0, help="vertex capacity")
    parser.add_argument("--skews", type=float, nargs="+", default=[0.0, 0.5, 1.0, 1.5])
    parser.add_argument("--periods", type=int, nargs="+", default=[0, 500, 200],
                        help="steps between rotations, 0 for a fixed skew")
    parser.add_argument("--shift", type=int, default=5, help="places the ranking rotates by")
    parser.add_argument("--rules", nargs="+",
                        default=["fixed", "demand", "congestion", "congestion_rho"],
                        choices=["fixed", "demand", "congestion", "congestion_rho",
                                 "congestion_v2"])
    parser.add_argument("--wait-rule", default="standing", choices=["standing", "overridden"])
    parser.add_argument("--deltas", type=int, nargs="+", default=[100, 200], help="Δ")
    parser.add_argument("--nus", type=int, nargs="+", default=[16], help="ν, units per update")
    parser.add_argument("--betas", type=float, nargs="+", default=[1.0, 10.0, 100.0], help="β")
    parser.add_argument("--rates", type=float, nargs="+", default=[0.6])
    parser.add_argument("--horizon", type=int, default=2000)
    parser.add_argument("--seeds", type=int, nargs="+", default=list(range(200_000, 200_006)))
    parser.add_argument("--jobs", type=int, default=6)
    parser.add_argument("--checkpoints", nargs="+", default=None,
                        help="RUN_DIR/CHECKPOINT of night runs to play instead of Token Passing")
    parser.add_argument("--quick", action="store_true",
                        help="a 2 to 4 minute look: 20 and 100 SKUs, both placements, skew 1 "
                        "fixed or rotating every 200 steps, Δ 100, ν 16, β 1 and 100, 4 seeds. "
                        "Rows go to OUT/../quick unless --out is given")
    args = parser.parse_args(argv)
    if args.quick:
        args.num_skus, args.placements, args.skews, args.periods = [20, 100], ["cyclic", "blocks"], [1.0], [0, 200]
        args.deltas, args.nus, args.betas, args.rates = [100], [16], [1.0, 100.0], [0.6]
        args.seeds = list(range(200_000, 200_004))
        if args.out == HERE / "out":
            args.out = HERE / "quick"
    args.out.mkdir(parents=True, exist_ok=True)
    rows_path = args.out / "rows.jsonl"
    done = set()
    if rows_path.exists():
        done = {key(json.loads(line)) for line in rows_path.read_text().splitlines() if line}

    routers = [("token_passing", None, None)]
    if args.checkpoints:
        routers = [(f"{Path(c).parent.name}/{Path(c).name}", str(Path(c).parent), Path(c).name)
                   for c in args.checkpoints]
    jobs = []
    grid = itertools.product(
        routers, args.num_skus, args.placements, args.skews, args.periods, args.rates, args.seeds
    )
    for (router, router_dir, router_checkpoint), num_skus, placement, skew, period, rate, seed in grid:
        if skew == 0.0 and period != args.periods[0]:
            continue  # rotating a uniform popularity changes nothing
        settings = [("fixed", None, None, None)] if "fixed" in args.rules else []
        for rule in [r for r in args.rules if r != "fixed"]:
            betas = args.betas if rule.startswith("congestion") else [None]
            settings += [(rule, d, n, b) for d in args.deltas for n in args.nus for b in betas]
        for rule, delta, nu, beta in settings:
            job = {"config": str(args.config), "router": router, "router_dir": router_dir,
                   "router_checkpoint": router_checkpoint,
                   "num_skus": num_skus, "placement": placement,
                   "units": args.units, "capacity": args.capacity, "skew": skew, "period": period,
                   "shift": args.shift, "rule": rule, "wait_rule": args.wait_rule,
                   "rate": rate, "seed": seed,
                   "delta": delta, "nu": nu, "beta": beta, "horizon": args.horizon}
            if key(job) not in done:
                jobs.append(job)
    print(f"{len(jobs)} episodes to play, {len(done)} already done", flush=True)
    with ProcessPoolExecutor(max_workers=args.jobs) as pool:
        futures = {pool.submit(play, job): job for job in jobs}
        for count, future in enumerate(as_completed(futures), 1):
            job = futures[future]
            try:
                row = future.result()
            except Exception as error:  # one broken episode must not stop the rest
                print(f"failed {key(job)}: {error!r}", file=sys.stderr, flush=True)
                continue
            with rows_path.open("a", encoding="utf-8") as sink:
                sink.write(json.dumps(row) + "\n")
            print(f"{count}/{len(jobs)} {key(row)}: {row['throughput']:.3f} in "
                  f"{row['seconds']} s", flush=True)
    if rows_path.exists():
        summary(args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
