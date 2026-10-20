# A2. The Assigner argument, one step mode and the planner driver [review]

Branch `fix/one-env-adapter`, continuing after A1. Read `00_rules.md` first, then the golden comparison section in it.

## Goal

Remove the second step mode and the router stack that exists only to serve it. After this commit the simulator has one
`step(actions)`, a planner drives it from outside, and Token Passing's own task rule enters through one plain argument.
`DecentralisedController` and the controller registry still exist (package A5 deletes them), and a temporary driver
keeps their evaluation path working.

Thesis to read: `sec:method:overview`, `sec:method:controllers` (the reference baseline paragraph and the shared
assignment rule), `sec:pf:game`.

## Changes

1. `controllers/assignment.py`. Add `Assigner`, a runtime-checkable Protocol with `reset(episode_seed)` and
   `assign(graph, fleet, tasks, t) -> dict[TaskId, AgentId]`. The shared greedy rule stays a function there.
2. `environment/multi_agent_env.py`.
   - Constructor argument `assigner: Assigner | None = None`. `reset(seed)` calls `assigner.reset(seed)` before the
     assignment of `t = 0`. Stage 2 uses the assigner if given, otherwise the shared greedy rule with the episode
     priority.
   - `step(actions)` takes the mapping of agent id to slot, with no default. Remove the `actions=None` branch, the
     lazy `_controller`, the eager planner router from A1, the import of `get_router`, and the router timing. Keep
     decoding with `action_for_slot`, `last_proposed` and `last_overridden`.
   - `EpisodeLog` gains `record_routing_runtime(seconds)`. Whoever produces the actions times itself and records.
3. New `planners/driver.py`, no Ray. `plan_slots(planner, env)` calls
   `planner.plan(env.graph, env.fleet, env.tasks, env.t)` and converts each action with `slot_for_action`.
   `step_with_planner(env, planner)` times the planning and conversion, records it, and calls `env.step`. Tests use it
   in place of `env.step()`.
4. `evaluation/evaluator.py::run_episode`.
   - Planner config. `planner = get_planner(config.planner)`. Pass `assigner=planner` when it is a
     `SelfAssigningPlanner`. Loop with `step_with_planner`. `planner.reset` is called by the env through the assigner. A
     planner that is not an assigner (prioritised A\*) has no state, so nothing to reset.
   - Controller config (temporary). Keep working through the registry with a small private helper that calls
     `get_controller(config.controller)`, resets it with the seed, and converts its `route` output to slots. Mark it
     temporary. Package A5 deletes it.
   - The trace writer and `_to_run_metrics` are unchanged.
5. Delete `planners/router.py`, `PlannerRouter`, `SelfAssigningPlannerRouter`, `router_for`, `SelfAssigningRouter`
   (in `controllers/base.py`), `routing.py`, and their exports in `planners/__init__.py`. Keep the `Planner` and
   `SelfAssigningPlanner` protocols and `planners/registry.py`. Shorten the protocol docstrings.
6. Update every caller of `env.step()` with no argument to use `step_with_planner`: `evaluation/evaluator.py`,
   `examples/01_baseline_fixed_centralised.py` (the Token Passing example), and the test files. For
   `examples/01_baseline_fixed_prioritised_astar.py` make only the call changes. That example cannot build its
   instance on `main` and the author decided not to fix it, so do not touch anything else in it.
7. Rewrite the tests that used the router classes (`test_self_assigning_router.py`, the router tests in
   `test_prioritised_astar_planner.py`, `get_router` in `test_trace.py`).

## Tests

- A stub `Assigner` is reset before the assignment of `t = 0`, and again on every `env.reset(seed=...)` with the new
  seed.
- A planner passed as `assigner` is asked for the assignment, and the shared rule is used when there is none.
- `step` with no argument is a `TypeError`.
- `plan_slots` converts every action kind (wait and each move slot) and agrees with `action_for_slot`.
- The correctness checks (no conflicts, feasible storage, task lifecycle, bit for bit replay) run through
  `step_with_planner` for both planners.

## Done when

The golden comparison shows identical metrics, with the trace classified as in A1. `git grep` for `get_router`,
`PlannerRouter`, `SelfAssigningRouter` and `router_for` returns nothing in `src`, `tests` and `examples`.

## Flag in the hand back

Any place where a temporary path remains, and the test files you had to change.
