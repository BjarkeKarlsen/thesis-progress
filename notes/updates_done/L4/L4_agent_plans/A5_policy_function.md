# A5. The policy function, learned evaluation and deleting the controller stack [review]

Branch `fix/one-env-adapter`, continuing after A4. Read `00_rules.md` first, then the golden comparison section.

## Goal

A trained module is evaluated through the same adapter that trained it, so a policy sees exactly the observations it
saw in training. `DecentralisedController`, the registry, the active-controller singleton and the temporary driver
from A2 are deleted.

Thesis to read: `sec:method:model`, `sec:method:rl`, `sec:impl:logging`, `sec:impl:cost` (the runtime measure),
`sec:method:training`.

## Changes

1. New `training/policy.py` (it may import Ray). `ModulePolicy(module, ...)` with `reset(episode_seed)` and
   `__call__(observations, t) -> dict[str, int]`.
   - Stack the per-robot observation dicts the adapter returns into one batch (move the stacking helper from
     `controllers/decentralised.py`), call `module.forward_inference` once, and pick one legal slot per robot.
   - Sample with the same rule as today: the softmax of the raw logits with illegal slots zeroed and the result
     renormalised, from a stream seeded with `(episode_seed + offset, t, agent_id)`, so replay is bit for bit. Keep the
     offset constant. Whether evaluation samples or takes the most likely action is decision 17 and stays open, so
     do not change it. Say in the docstring that this is the open choice.
   - It does not know how the module was loaded. `reset` must be called before use, and `__call__` raises if not.
   - Build a fresh batch per call, since `forward_inference` can change the batch dict in place.
2. `evaluation/evaluator.py::run_episode`. Add `policy`, `encoding_config`, `zones` and `pooling` arguments, all
   optional. For a planner config nothing changes and Ray is not imported. For a controller config require `policy`
   (otherwise `ValueError`), import the adapter inside this branch, build it with `train_seeds=(config.seed,)`, call
   `reset(seed=config.seed)`, and loop `obs -> policy -> adapter.step`. The trace writer, `_to_run_metrics` and the
   four checks read `adapter.core`. Delete the temporary controller driver from A2.
3. Runtime. The policy records its forward pass and sampling through `core.log.record_routing_runtime`. The adapter
   records its observation build the same way. The measure of the mean decision runtime then covers producing the joint
   action for a learned arm, not only decoding slots. Keep the assignment timing where it is.
4. Delete `controllers/decentralised.py`, `controllers/registry.py`, `controllers/base.py` and
   `controllers/section_based.py`. Keep `controllers/assignment.py`. Remove their tests and the registry mentions in
   `tests/unit/test_multi_agent_env.py`.
5. Move the worthwhile tests of `test_decentralised_controller.py` to `tests/unit/test_policy.py`.

## Tests

- One module call per step, and the actions equal per-agent calls.
- Actions are always legal, and reproducible for a fixed `(seed, t, agent)`.
- `reset` is required.
- `run_episode` with an untrained module for each of the three arms over a short horizon. Collision free, feasible
  storage, bit for bit replay and the lifecycle check hold, and the trace file is written.
- `run_episode` with a controller config and no policy raises.
- The planner path stays Ray free. Import `evaluation.evaluator` with Ray blocked and run a planner episode (use the
  import-blocking style of the existing tests if one exists, otherwise assert that `ray` is not in `sys.modules`
  after a planner run in a fresh process).
- Planner runs are unchanged. Run the golden comparison.

## Done when

`git grep` for `DecentralisedController`, `get_controller`, `register_controller` and
`set_active_decentralised_controller` returns nothing in `src`, `tests` and `examples` except the old example files that
package A6 rewrites (list them). The golden comparison is identical for the planner runs.

## Flag in the hand back

That the observation build counts as routing time, and decision 17.
