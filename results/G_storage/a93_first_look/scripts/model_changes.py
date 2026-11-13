"""Experimental model changes for the quick test, patched into the environment at run time.

install("ws,pick,reloc") turns on any of:
  ws     an order goes to the least busy workstation of its section (fewest open lines: pick
         tasks not delivered plus lines still waiting for stock). The order's own random draw is
         kept and only fixes the section, so the order stream is the same as today.
  pick   a line picks from the holder with the least distance + expected waiting on the way to
         its workstation (waits per crossing, averaged over about 5 storage periods), instead of
         the nearest holder.
  reloc  an idle agent moves stock that is in the way: when no task is waiting and an agent is
         free, and no relocation is open, the unreserved units of a SKU with no order line in
         about 5 periods are moved off one of the best quarter of shelves to the free shelf
         farthest from the workstations, if that is at least 4 steps worse. The move is a
         put-away kind task from shelf to shelf: the units stay reserved at the old shelf until
         picked up, and the room at the new shelf is held as stock on its way.
The averages are kept on the estimator when a storage window closes.
"""
from __future__ import annotations

import inspect
import textwrap

from slap_mapd_coupling.core.tasks import Task, free_agents
from slap_mapd_coupling.environment import multi_agent_env as M
from slap_mapd_coupling.environment import storage_estimates as SE

ALPHA = 0.2
UNUSED = 0.002  # lines per step, averaged: about no line in 5 periods
GOOD_SHARE = 0.25
MIN_GAIN = 4


def _patch_estimator():
    orig = SE.WindowEstimator.close_window

    def close_window(self, window_length):
        est = orig(self, window_length)
        for name, new in (("_ema_w", est.waiting), ("_ema_m", est.traversal), ("_ema_rho", est.demand)):
            old = getattr(self, name, {})
            for key in set(old) | set(new):
                old[key] = (1 - ALPHA) * old.get(key, 0.0) + ALPHA * new.get(key, 0.0)
            setattr(self, name, old)
        return est

    SE.WindowEstimator.close_window = close_window


def _expected_wait(env, v, w):
    est = env._estimator
    wt, mt = getattr(est, "_ema_w", {}), getattr(est, "_ema_m", {})
    cache = env.__dict__.setdefault("_cng_paths", {})
    edges = cache.get((v, w))
    if edges is None:
        edges = cache[(v, w)] = tuple(env.graph.shortest_path_edges(v, w))
    return sum(wt.get(e, 0.0) / mt[e] for e in edges if mt.get(e, 0.0) > 1e-9)


def _least_busy(env, section, lines):
    stations = env._section_workstations[section]
    load = {w: 0 for w in stations}
    t = env._t
    for task in env.tasks:
        if task.kind == "pick" and task.delivery_vertex in load and task.status(t) != "completed":
            load[task.delivery_vertex] += 1
    for line in env._waiting_orders:
        if line.delivery_vertex in load:
            load[line.delivery_vertex] += 1
    for line in lines:
        if line.delivery_vertex in load:
            load[line.delivery_vertex] += 1
    return min(stations, key=lambda w: (load[w], w))


def _rebuild(method, replacements):
    src = textwrap.dedent(inspect.getsource(method))
    for old, new in replacements:
        assert src.count(old) == 1, f"patch target not found once: {old!r}"
        src = src.replace(old, new)
    scope = dict(vars(M), _expected_wait=_expected_wait, _least_busy=_least_busy, SB=SB)
    exec(compile(src, f"<patched {method.__name__}>", "exec"), scope)
    return scope[method.__name__]


def _relocate(env):
    t = env._t
    if env.__dict__.get("_reloc_open"):
        open_ids = env._reloc_open
        open_ids &= {task.task_id for task in env.tasks if task.status(t) != "completed"}
        if open_ids:
            return
    if any(task.status(t) == "waiting" for task in env.tasks) or env._waiting_orders:
        return
    if not free_agents(env.fleet, env.tasks, t):
        return
    rho = getattr(env._estimator, "_ema_rho", None)
    if rho is None:
        return  # no window closed yet
    if "_reloc_near" not in env.__dict__:
        shelves = sorted(env._storage_capacities)
        env._reloc_near = {v: min(env.graph.distance(v, w) for w in env._delivery_vertices)
                           for v in shelves}
        ranked = sorted(shelves, key=lambda v: (env._reloc_near[v], v))
        env._reloc_good = set(ranked[: max(1, int(len(ranked) * GOOD_SHARE))])
    near, good = env._reloc_near, env._reloc_good
    free = env._unreserved(env.storage).counts
    used = {}
    for sku_id, per_vertex in env._shelf_and_transit().counts.items():
        size = env._skus[sku_id].unit_capacity
        for v, n in per_vertex.items():
            used[v] = used.get(v, 0.0) + n * size
    candidates = sorted(
        ((near[v], v, sku_id, n) for sku_id, per_vertex in free.items()
         if rho.get(sku_id, 0.0) < UNUSED for v, n in per_vertex.items() if n > 0 and v in good),
    )
    for _, v, sku_id, n in candidates:
        size = env._skus[sku_id].unit_capacity * n
        targets = [u for u in near if u != v
                   and env._storage_capacities[u] - used.get(u, 0.0) >= size - 1e-9
                   and near[u] - near[v] >= MIN_GAIN]
        if not targets:
            continue
        target = max(targets, key=lambda u: (near[u], -u))
        reserved = env._reserved.setdefault(sku_id, {})
        reserved[v] = reserved.get(v, 0) + n
        transit = env._in_transit.setdefault(sku_id, {})
        transit[target] = transit.get(target, 0) + n
        task = Task(task_id=env._next_task_id, release_time=t, pickup_vertex=v,
                    delivery_vertex=target, sku=sku_id, quantity=n, kind="putaway")
        env._next_task_id += 1
        env.tasks.append(task)
        env.__dict__.setdefault("_reloc_open", set()).add(task.task_id)
        env.__dict__["_reloc_count"] = env.__dict__.get("_reloc_count", 0) + 1
        return


def install(changes: str) -> None:
    flags = {c for c in changes.split(",") if c}
    unknown = flags - {"ws", "pick", "reloc", "pickb"}
    assert not unknown, unknown
    if not flags:
        return
    _patch_estimator()
    cls = M.WarehouseMAPDEnv
    if "ws" in flags:
        line = "section = self._section_of[delivery]\n"
        src = textwrap.dedent(inspect.getsource(cls._draw_order_lines))
        indent = src.split(line)[0].rsplit("\n", 1)[1]
        cls._draw_order_lines = _rebuild(cls._draw_order_lines, [(
            indent + line, indent + line + indent + "delivery = _least_busy(self, section, lines)\n")])
    if "pick" in flags:
        cls._release_orders = _rebuild(cls._release_orders, [(
            "key=lambda v: (self.graph.distance(v, line.delivery_vertex), v),",
            "key=lambda v: (self.graph.distance(v, line.delivery_vertex)"
            " + _expected_wait(self, v, line.delivery_vertex), v),")])
    if "pickb" in flags:
        # a line picks from the holder with the least distance + measured blocking of that shelf
        cls._release_orders = _rebuild(cls._release_orders, [(
            "key=lambda v: (self.graph.distance(v, line.delivery_vertex), v),",
            "key=lambda v: (self.graph.distance(v, line.delivery_vertex) + SB.get(v, 0.0), v),")])
    if "reloc" in flags:
        orig_assign = cls._release_and_assign
        orig_advance = cls._advance_task_lifecycle

        def _release_and_assign(self):
            if self.config.stock_model == "arrival":
                # new orders first, then a relocation only if nothing waits
                new_tasks = self._release_orders()
                self.tasks.extend(new_tasks)
                _relocate(self)
                self._release_orders, saved = (lambda: []), self._release_orders
                try:
                    orig_assign(self)
                finally:
                    del self._release_orders
            else:
                orig_assign(self)

        def _advance_task_lifecycle(self, next_t):
            tasks = orig_advance(self, next_t)
            for task in tasks:
                if (task.task_id in self.__dict__.get("_reloc_open", ())
                        and task.pickup_time == next_t):
                    self._pick_up_units(task, next_t)
            return tasks

        cls._release_and_assign = _release_and_assign
        cls._advance_task_lifecycle = _advance_task_lifecycle


# ---------------------------------------------------------------- shelf blocking signal
# SB[v]: mean blocked steps per pick picked up at shelf v, averaged over periods (alpha). Updated at
# every storage update from the picks finished in the period. PROBE_OUT, when set, saves every
# period's raw per-shelf numbers for the diagnostic.
SB: dict = {}
SB_RAW: list = []


def _shelf_blocking_hook():
    import atexit, os, pickle
    cls = M.WarehouseMAPDEnv
    orig = cls._arrive

    def _arrive(self, delta):
        t = self._t + 1
        done = {}
        seen = self.__dict__.setdefault("_sb_seen", set())
        for task in self.tasks:
            if task.kind != "pick" or task.task_id in seen or task.finish_time is None:
                continue
            seen.add(task.task_id)
            b = self.log.blocked_ticks_by_task.get(task.task_id, 0)
            s, n = done.get(task.pickup_vertex, (0, 0))
            done[task.pickup_vertex] = (s + b, n + 1)
        raw = {v: s / n for v, (s, n) in done.items()}
        for v in set(SB) | set(raw):
            if v in raw:
                SB[v] = (1 - ALPHA) * SB.get(v, raw[v]) + ALPHA * raw[v]
        SB_RAW.append(dict(t=t, raw=done, ema=dict(SB)))
        return orig(self, delta)

    cls._arrive = _arrive
    out = os.environ.get("PROBE_OUT")
    if out:
        def dump():
            import slap_mapd_coupling.environment.multi_agent_env as MM  # noqa: F401
            pickle.dump(SB_RAW, open(out, "wb"))
        atexit.register(dump)


if __import__("os").environ.get("SHELF_SIGNAL"):
    _shelf_blocking_hook()
