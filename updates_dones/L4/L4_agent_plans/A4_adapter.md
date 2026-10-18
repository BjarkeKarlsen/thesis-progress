# A4. The RLlib adapter for every arm [review]

Branch `fix/one-env-adapter`, continuing after A3. First bring in the packages B1, B2 and B3 with `git cherry-pick`
(or merge their branches), in that order. Read `00_rules.md` first.

## Goal

`training/env.py` stays the RLlib `MultiAgentEnv`. It is generalised to all three arms with one RLlib agent per robot.
`config.controller` decides the window of a robot's observation and nothing else. The simulator stays a plain class.

Thesis to read: `sec:method:controllers`, `sec:method:rl`, `sec:method:model` (the readout paragraphs), `sec:method:training`
(credit signal), `sec:pf:game`.

## Changes

1. `training/env.py` (class `WarehouseMAPDMultiAgentEnv`).
   - Remove the guard that allows only `decentralised`. Constructor adds `zones` (required for the section arm,
     checked with `check_partition`), `credit_signal` (no default) and `pooling` (no default, taken from the encoder
     config). Raise for `team_mean` with the decentralised arm and for the decentralised arm with pooling on, since
     the thesis lets only the centralised and section readouts pool. Flag both in the hand back.
   - Windows. Decentralised uses the field of view. Centralised uses all movable vertices. Section uses the zone of
     the robot's current vertex plus its halo, with the halo of each zone computed once at construction.
     Pool vertices follow the author's decision: the whole graph for centralised, the zone only for section.
   - At construction call `check_windows` for every movable vertex a robot can stand on, so a rollout worker never meets
     an oversized window or a missing neighbour. B2's `check_windows` does not require a window for every movable
     vertex and does not check that window vertices are movable, so this package must check both. A `windows`
     mapping that misses a robot raises in the encoder, so build one for every robot at every step.
   - The centralised window is all movable vertices. The thesis text in `sec:method:rl` says "all of V", but
     non-movable vertices carry no edges and the field of view is defined on the movable vertices. Use `V_mov`
     (the largest padded window then equals the number of movable vertices) and flag the wording in the hand
     back, as a possible thesis fix for the author.
   - Use the single builder `encode_all_observations` with the windows and the pool vertices. If the core's
     `congestion_by_agent` can be passed through without more scope, do so. Otherwise leave the builder's own value
     and say so.
   - Credit signal. `per_agent` returns the core's rewards. `team_mean` replaces each robot's reward by the mean
     over its group, the whole fleet for centralised and the robots in the same zone at the start of the step for
     section.
   - Expose the core as `core`. Keep one agent per robot, ids `str(robot_id)`, action space `Discrete(d_max + 1)`.
   - Move the `CreditSignal` type here if `training/config.py` would otherwise import in a circle.
2. `training/config.py::build_ppo_config`. Accept all arms. Remove the guard that rejects `team_mean`. Pass `zones`,
   the credit signal and pooling to the env creator. Keep the checks for the discount, communication and the caps.
3. `training/callbacks.py`. Replace every access to `._env` with `.core`, and make `progress_metrics` take the core.
4. Docstrings in the files you touch. Remove the statements that only the decentralised arm is trained.

## Tests

- Each arm builds, and the observations match the window (shapes per arm, `pool_mask` only for the arms that pool).
- The zone of a robot follows its vertex when it crosses a boundary, and the section window changes with it.
- `team_mean` gives the fleet mean for centralised and the zone mean at the start of the step for section.
  `team_mean` with the decentralised arm raises. The section arm without `zones` raises. A window larger than the cap
  raises at construction.
- Callbacks work on the adapter for all three arms (the invariants and the progress counters).
- One PPO iteration through `build_ppo_config` for each controller. For the centralised and section arms run it with
  `pooling="mean"`, and for the decentralised arm with `pooling="none"`. Package B3 could not write this test because
  the adapter only accepted the decentralised arm. Until this package lands, `build_ppo_config` with `pooling="mean"`
  builds a module that expects a `pool_mask` the adapter never sends. Make `build_ppo_config` and the adapter agree
  on pooling and raise a clear error on a mismatch. Write the tests, do not run them.

## Done when

The tests are written and the existing training tests are adapted. The golden comparison is not affected by this
package, so run it only if you changed a file in `environment/`.

## Flag in the hand back

The two new errors, where `CreditSignal` lives, and whether the core's congestion value was passed through.
