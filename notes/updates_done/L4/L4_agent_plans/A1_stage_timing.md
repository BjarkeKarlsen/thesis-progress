# A1. Stages 1 and 2 move to the end of `step` and into `reset` [review]

Branch `fix/one-env-adapter`, from `origin/main`. First commit of Track A. Read `00_rules.md` first, then the golden
comparison section in it.

## Goal

A robot must see the task it was assigned before it chooses its action. Today `training/env.py:139-141` builds the
observation after `WarehouseMAPDEnv.step` returns, but orders and assignment (stages 1 and 2) run at the start of the
next `step` (`environment/multi_agent_env.py:248-275`). A learned policy therefore acts blind to a task assigned in
that same tick, while the controller used for evaluation sees it. The thesis kernel ends a step with the assignment
and the new orders (`sec:pf:game`), so the observation of the next step already holds them. The six-stage list in
`sec:method:overview` is the same cycle starting one stage later and needs no edit.

Thesis to read: `sec:method:overview`, `sec:pf:game`, `sec:method:controllers` (the assignment rule). Planner runs must
not change at all.

## Changes (`environment/multi_agent_env.py`)

1. `reset`. After the episode state is built and `log.backlog_by_t` has its first entry, run stage 1 (draw and append
   the orders for `t = 0`) and stage 2 (assignment for `t = 0`, with its timing appended to
   `log.assignment_runtime_seconds`). Keep the backlog append before the release, as it is today.
2. `step`. Remove stages 1 and 2 from the start. `active_by_agent` is still taken at the start, from the task list
   that the previous step or `reset` already assigned.
3. At the very end of `step`, after `self._t` has advanced, run stages 1 and 2 for the new `t`. Do not run them on the
   step that ends the episode (when `t` reaches `horizon`). Otherwise tasks are released and assigned beyond the
   horizon, the final assignment is wasted work and the task list gains an extra released task. With the skip the
   random draws and the number of `assignment_runtime_seconds` entries equal today's, because `reset` supplies the
   draw for `t = 0` and the last step supplies none.
4. Everything else keeps its place, including the backlog append in stage 5, which still precedes the release for the
   next `t`, and `_record_crowding(before_fleet)` at the start of the step.
5. A planner that picks its own tasks (Token Passing) is now asked for the assignment inside `reset`, before any step.
   Resolve the router eagerly in `__init__`, before `reset()`, when `config.planner` is set, so its `reset(seed)` runs
   before the assignment of `t = 0`. For a controller config keep the lazy resolution, since the shared greedy rule needs
   no router. This is temporary and package A2 replaces it with an `assigner` argument. Say so in a comment that points
   to nothing outside the repo.
6. Update the module docstring where it describes the order of the stages, in two or three sentences.

## Tests

- After `reset` on a hand-built fixture with an order released at `t = 0` and a free robot, the task is already
  assigned. A test in `test_training_env.py` shows that the observation returned by `reset` for that robot carries its
  target (the distance label to the pickup is not the one for a robot with no task).
- The first step with no order leaves the observation consistent with the next assignment.
- No task has `release_time` equal to `horizon` after the last step, and `len(log.assignment_runtime_seconds)` equals
  the horizon.
- Update every existing test that assumed the old timing (a task list that is empty after `reset`, counts after a
  given number of steps). List each one in the hand back.

## Done when

The golden comparison shows identical metrics. List every trace field that differs and classify it. Fields that read the
task list after a step (the released count) may shift by one tick. Any difference in positions, actions, overridden
flags, completed counts or backlog is a failure, so stop and report.

## Flag in the hand back

That training observations change (the intended fix), and that the first assignment now happens in `reset`.
