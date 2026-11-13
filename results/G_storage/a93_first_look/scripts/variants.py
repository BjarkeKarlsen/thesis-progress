"""Experimental put-away rules for the Token Passing test of the congestion fixes.

Every variant is installed in place of the registered "congestion" rule, so an episode runs
with storage_mode "congestion" and the environment passes it the usual estimates. The state
(the moving averages) lives in a module global and is reset by `install`, one episode per
process.

Variants:
  demand_smooth  F_dem, with the popularity estimates averaged over periods (fix a)
  aisle          fix a, plus the expected waiting on the SKU's own trip, in steps: waits per
                 crossing, averaged over periods, on the trip from the docks and on to the
                 section's workstations, each leg weighed as its trips happen (fix b)
  pressure       fix a, with the pick leg weighing each of the section's workstations by its
                 share of the section's waiting at the workstation (in and out edges),
                 averaged over periods, blended with equal weights by beta (fix c)
  traffic        fix a, plus the expected number of agents met on the SKU's own trip (crossings
                 per step, averaged over periods, summed over the trip's edges), beta steps each
  shelfblock     fix a, plus the shelf's measured blocking (mean blocked steps per pick from
                 that shelf, averaged over periods, model_changes.SB) on the pick leg, beta steps each
  combo          a, b and c together: pressure weights (beta) on the pick leg, the aisle
                 waiting added on both legs with weight 1
"""
from __future__ import annotations

from functools import lru_cache

from slap_mapd_coupling.storage import arrival as A

ALPHA = 0.2  # moving-average weight of the newest period, about 5 periods of memory
STATE: dict = {}


def _ema(name, new):
    old = STATE.setdefault(name, {})
    for key in set(old) | set(new):
        old[key] = (1 - ALPHA) * old.get(key, 0.0) + ALPHA * new.get(key, 0.0)
    return dict(old)


def _common(graph, receiving, demand, units, sku_delivery, raw=False):
    rho = dict(demand) if raw else _ema("rho", demand)
    unit = dict(units) if raw else _ema("unit", units)
    storage = A.storage_vertices(graph)
    delivery = A.delivery_vertices(graph)
    receiving = delivery if receiving is None else receiving
    return rho, unit, storage, delivery, receiving, sku_delivery or {}


def _make(variant: str, beta: float):
    @lru_cache(maxsize=None)
    def edges(graph_id, a, b):
        return tuple(STATE["graph"].shortest_path_edges(a, b))

    def rule(x_prev, graph, amounts, home, demand, traversal, waiting, congestion_weight, *,
             receiving=None, trip=False, rng=None, refill_units=None, unit_estimate=None,
             sku_delivery=None):
        assert trip and refill_units is not None, "variants assume robot put-away and refills"
        STATE["graph"] = graph
        rho, unit, storage, delivery, receiving_, targets = _common(
            graph, receiving, demand, unit_estimate or {}, sku_delivery,
            raw=variant.endswith("_raw"))
        if variant.endswith("_raw"):
            variant_ = variant[: -len("_raw")]
        else:
            variant_ = variant
        put_leg = {v: A.receiving_distance(graph, v, receiving_) for v in storage}
        trip_d = {v: A.trip_distance(graph, v, receiving_, delivery) for v in storage}

        AISLE = variant in ("aisle", "combo", "traffic")
        PRESSURE = variant in ("pressure", "combo")
        if AISLE or PRESSURE:
            w = _ema("w", waiting)
        if AISLE:
            m = _ema("m", traversal)
            if variant == "traffic":
                # expected agents met on an edge: its crossings per step, averaged over periods
                per = lambda e: m.get(e, 0.0)
            else:
                per = lambda e: w.get(e, 0.0) / m[e] if m.get(e, 0.0) > 1e-9 else 0.0
            gid = id(graph)
            put_wait = {v: sum(sum(per(e) for e in edges(gid, r, v)) for r in receiving_)
                        / len(receiving_) for v in storage}
        if PRESSURE:
            touch = {}
            for e in graph.edges:
                for end in (e.source, e.target):
                    if end in delivery:
                        touch[end] = touch.get(end, 0.0) + w.get((e.source, e.target), 0.0)

        def pick_cost(sku, v):
            sec = targets.get(sku)
            ws = list(sec) if sec is not None else delivery
            if PRESSURE:
                total = sum(touch.get(x, 0.0) for x in ws)
                share = {x: (touch.get(x, 0.0) / total if total > 0 else 1 / len(ws)) for x in ws}
                weight = {x: (1 - beta) / len(ws) + beta * share[x] for x in ws}
            else:
                weight = {x: 1 / len(ws) for x in ws}
            gid = id(graph)
            # with the aisle term its weight is 1: a step of waiting counts as a step of travel
            aisle_w = (1.0 if variant == "combo" else beta) if AISLE else 0.0
            return sum(weight[x] * (graph.distance(v, x)
                                    + (aisle_w * sum(per(e) for e in edges(gid, v, x)) if AISLE else 0.0))
                       for x in ws)

        if variant in ("shelfblock", "shelfblock_raw"):
            import model_changes as MC
            base_pick = pick_cost

            def pick_cost(sku, v):  # noqa: F811
                return base_pick(sku, v) + beta * MC.SB.get(v, 0.0)

        def put_cost(v):
            return put_leg[v] + ((1.0 if variant == "combo" else beta) * put_wait[v] if AISLE else 0.0)

        def order(sku):
            picks = rho.get(sku, 0.0)
            refills = unit.get(sku, 0.0) / refill_units
            return sorted(storage, key=lambda v: (picks * pick_cost(sku, v) + refills * put_cost(v),
                                                  trip_d[v], v))

        sku_order = sorted(x_prev.skus, key=lambda k: (-rho.get(k, 0.0), k))
        return A._put_away(x_prev, amounts, sku_order, order, whole=refill_units)

    return rule


def install(variant: str, beta: float) -> None:
    STATE.clear()
    A._REGISTRY["congestion"] = _make(variant, beta)
