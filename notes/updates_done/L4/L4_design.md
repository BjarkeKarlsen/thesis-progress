# L4 design: one learned path for all three controllers

Written 2026-10-13 after the design discussion with the author. Not built. It sits beside
`fix_prs_plan.md`, whose "Large PRs" table still describes L4 as one `MultiAgentEnv` and should be updated
once the author approves this design.

Branch `fix/one-env-adapter`, one PR from `origin/main` (0961081 when written). Code
lines below refer to that commit. The three spikes of step 0 have run. Their
results are under "Spike results". Nothing else here was run.

## Decisions taken in the design discussion

- **The simulator stays a plain class, and the RLlib env is the adapter.** `WarehouseMAPDEnv`
  (`environment/multi_agent_env.py`) keeps no Ray import and gets one step mode, `step(actions)`.
  `training/env.py` stays as the RLlib `MultiAgentEnv`, generalised to all three arms. This departs from
  the title of #104 and from the author's direction of 2026-10-13, so the PR description says so. The
  reason is that the complexity the author wants gone sits in the dual step mode and the router stack,
  and a base class removes none of it. The simulator is defined by the thesis, and RLlib is how a learner
  sees it. Merging the two classes later is a small, mechanical commit, and splitting a merged class is
  not.
- **Layout R, one RLlib agent per robot in every arm.** `config.controller` decides the window a robot's
  observation covers and nothing else. The thesis says the three arms are one game that differs only in
  `O_i` (`sec:pf:game`), the critic is per robot (`[A13]`), and the per-robot layout keeps training
  procedure, credit signal and sample counts equal across arms. Layout F (one agent for the fleet or a
  zone) is not built. It would force one scalar reward and value per agent, so `team_mean` would be
  imposed on two arms.
- **Stages 1 and 2 move to the end of `step` and into `reset`.** See "What is wrong today".
- **Ray defaults for checkpoints, and Tune for the run.** Examples 02 and 04 run through `ray.tune.Tuner`.
  Tune stops on environment steps, saves checkpoints and writes the training curves.
- **B14 is absorbed.** L4 rewrites example 04, so its three changes (the `--regime matched` parser, evaluation
  through the shared path, evaluation seeds from `split_seeds`) go into step 7. B14 cannot land first,
  because it depends on B12 and neither has a branch on `origin`. One of its three changes, evaluation on the
  evaluation seeds, is already on `main` since #134 (7bf81d4).

## What is wrong today

- **Training and evaluation see different observations.** `training/env.py:139-141` encodes the
  observation after `WarehouseMAPDEnv.step` returns. Stages 1 and 2 run at the start of the next `step`
  (`multi_agent_env.py:248-275`), before the action is used. A robot assigned at that tick acts without
  seeing its target. `DecentralisedController.route` runs after stage 2, so evaluation does see it. The
  kernel `P` of `sec:pf:game` ends a step with the assignment and the new orders, so `O_i` reads a state
  that includes them. The six-stage list of `sec:method:overview` is the same cycle starting one stage
  later, so it needs no edit.
- **Two step modes.** `step()` either asks a router (`multi_agent_env.py:253-257, 293-295`) or decodes
  `actions` (`287-292`). The router is resolved lazily (`148-150`) because `decentralised` had no controller
  yet.
- **Machinery whose only job is the second mode.** `Controller` and its registry, `routing.py`, the
  active-controller singleton, `PlannerRouter`, `SelfAssigningPlannerRouter`, `router_for` and
  `SelfAssigningRouter`.
- **Duplicated work.** δ is computed in `_record_crowding` (`multi_agent_env.py:431-446`) and again in
  `build_observation` (`observation.py:133-134`). The agent id and the `__all__`, terminated and truncated
  shaping exist in both classes (`training/env.py:138-147`, `multi_agent_env.py:356-363`).
  `encode_all_observations` has two call sites, `training/env.py:152-162` and `decentralised.py:101-110`.
- **Reward gate.** `multi_agent_env.py:470` returns 0 for every controller except `decentralised`, and
  `ExperimentConfig._controller_parameters` requires the reward weights only for it. Both are ticked in
  #103 but are still in the code on `main`. The congestion term is hard-coded to 0.0 (`multi_agent_env.py:499`).
- **Checkpoints.** `training/utils.py` wraps two Ray calls. Examples 02, 04 and 04b each hard-code
  `CHECKPOINT_DIR`. 04b builds `learner_group/learner/rl_module` by hand, which is RLlib's internal layout.

## What goes away

| Item | Where | Replaced by |
|---|---|---|
| Lazy router, `actions=None` path | `multi_agent_env.py:148-150, 201-202, 253-257, 286-296` | one `step(actions)` |
| `Controller` protocol, registry, `routing.py` | `controllers/base.py:12-48`, `controllers/registry.py`, `routing.py` | nothing. `controllers/section_based.py` is a one-line docstring that registers nothing. `main.py` `simulate`, `train` and `sweep` only raise `NotImplementedError`. |
| `SelfAssigningRouter` | `controllers/base.py:50-70` | the `Assigner` argument |
| `PlannerRouter`, `SelfAssigningPlannerRouter`, `router_for` | `planners/router.py`, `planners/__init__.py` | the planner driver |
| Active-controller singleton | `controllers/decentralised.py:189-213` | the policy function |
| `DecentralisedController` as a controller | `controllers/decentralised.py:56-170` | the policy function, which reads the observation the adapter returns |
| `training/utils.py` | 27 lines | direct Ray calls |
| Hand-built RL module path | `examples/04b_evaluate_checkpoint.py:255-265` | `Algorithm.from_checkpoint` and `get_module` |
| Second δ pass | `observation.py:133-134` | δ computed once in the core and passed on |

Evidence that nothing else uses them. `get_router` is called only at `multi_agent_env.py:256` and
`evaluator.py:51`, plus two tests. `set_active_decentralised_controller` is used only in tests and docs.
Rewrite `test_controller_registry.py`, `test_self_assigning_router.py`, most of
`test_decentralised_controller.py` and `docs/controller_integration.md`.

## The simulator core (`environment/multi_agent_env.py`)

- `reset(seed)` draws the episode state, calls `assigner.reset(seed)` if there is one, then runs stages 1
  and 2 for `t=0`.
- `step(actions)` takes one slot per robot. It decodes the slots, resolves conflicts, applies the joint
  action, runs the storage update, computes rewards, advances `t`, then runs stages 1 and 2 for the new `t`.
  `backlog_by_t` is still appended where it is now, so its values do not change.
- The generator draws orders in the same order as today, because stage 1 still runs after the previous
  storage update. This is what makes planner runs bit for bit equal to `main`.
- **`Assigner`.** A two-method protocol, `reset(seed)` and `assign(graph, fleet, tasks, t)`, in
  `controllers/assignment.py`. The constructor takes `assigner=None`, which means the shared greedy rule
  with the episode priority. `TokenPassingPlanner` already has both methods and is passed as is. The reset
  has to happen before the `t=0` assignment, or the token loses its first committed paths.
- **Reward for every arm.** Remove the gate. `ExperimentConfig._controller_parameters` requires the four reward
  weights for any `controller`. A planner run has no weights and gets zero rewards. δ is computed once per step
  (the loop `_record_crowding` already runs), logged as the crowding sum, and passed to `compute_agent_reward`
  as δ at the step the action was chosen in.
- **Public surface kept.** `fleet`, `t`, `tasks`, `log`, `graph`, `config`, `last_proposed`, `last_overridden`,
  `storage`. Add `record_routing_runtime(seconds)` on the log so whoever produces the actions can time them.
- `encoding_config` is not an argument here. The core builds no observations, and planner runs never need
  padding caps.

## The adapter (`training/env.py`, an RLlib `MultiAgentEnv`)

- It owns a core env and exposes it as `core`. The callbacks and the trace use `core` instead of `_env`.
- Constructor: the core's arguments, plus `encoding_config`, `train_seeds`, `zones` (section only),
  `credit_signal`. One agent per robot, ids `str(robot_id)`, action space `Discrete(d_max+1)`.
- Observation per robot: the existing `{"action_mask", "observations"}` Dict, built by
  `encode_all_observations` (L2b), which stays the only builder. L3's slot arrays arrive through it in
  `observations` with the same keys and shapes, so the module does not change.
- **Window.** `build_observation` gets a window argument.

| `config.controller` | Window the encoder runs on | Messages |
|---|---|---|
| decentralised | the `d_obs` field of view | optional |
| centralised | all of `V_mov` | none |
| section | `Y_q` plus `H_q` for the zone owning `l_i(t)` | none |

- δ stays defined on the `d_obs` field of view for every arm (`eq:congestion`), not on the window.
- **Caps.** A window larger than `max_local_nodes` raises when the adapter is built, for the centralised
  and section arms. Silent truncation by `eta` would change the window. This touches decision 15 and goes in
  the PR description.
- **Credit signal.** `per_agent` leaves the rewards alone. `team_mean` replaces each robot's reward by the mean
  over its group, the whole fleet for centralised and the zone that owns the robot at the start of the step for
  section. `team_mean` with `decentralised` raises. `build_ppo_config` passes the value from
  `PPOHyperparameters` to the env creator, so `ExperimentConfig` gains no field. The guard in
  `build_ppo_config` that rejects `team_mean` goes.
- **Seeds.** Cycling through `train_seeds` stays here.
- `build_ppo_config` accepts every arm.

## The planner baselines

- `planners/driver.py` (new, no Ray): `plan_slots(planner, env)` calls `planner.plan(graph, env.fleet, env.tasks, env.t)`
  and converts with `slot_for_action`. This works because the state the planner reads is the state after
  stage 2.
- `Planner` and `SelfAssigningPlanner` protocols and `planners/registry.py` stay.
- `run_episode` builds the core with `assigner=planner` when the planner has `assign`, and calls the driver
  then `step` in a loop.

## Centralised and section-based networks (#86)

- **Thesis.** The centralised arm runs the encoder on `G` and reads each robot at `l_i(t)`. The section arm
  runs it on `Y_q` plus `H_q` (`eq:halo`, cost range `d_obs`), with the halo carrying features and no heads.
  Ownership passes on entry, and with `p = 1` the section arm equals the centralised one. Both drop the message
  term.
- **Zones are not defined in the thesis, so this is a design choice.** `eq:partition` only requires a disjoint
  cover of `V_mov`. There is no `p` and no rule for drawing zones. The author decided on 2026-10-13 that zones
  follow the aisles (see "Notes on the answers"). A zone is a block of consecutive aisles, and every movable
  vertex belongs to the zone of its aisle, cross-aisle vertices included. The env takes `zones` as an input and
  checks `eq:partition`, so the helper that builds them is the only part that depends on the instance. It lives in
  a new `environment/zones.py` with no Ray import, with `zones_by_aisle(aisle_index, num_zones)`,
  `halo(graph, zone, d_obs)` and `check_partition`. `num_zones` is a config field with no default.
- **Encoder.** L2a's encoder takes any padded edge list, so a whole graph or a zone is one padded view. No
  encoder code changes under layout R.
- **Head.** L3's head reads `z_i` and `h_w`, with `xibar_w` dropped because communication is off. Every
  outgoing neighbour must lie in the window. A neighbour across a zone boundary lies in the halo when the edge
  cost is at most `d_obs`. The check is the one `check_slot_targets` makes for the field of view.
- **Left TBD.** `[A8]` (how `eta_i` enters the pass, and global pooling) stays TBD with no config field. Layout R
  gives one pass per robot, which is `[A8]` option 1, and the two thesis sentences that say the encoder "runs
  once per timestep on `G`" and that agents "share one graph pass" need rewording. The suggested wording is that
  every router's encoder runs on its window for each robot, with shared weights, and that a single shared pass
  is an equivalent implementation when `eta_i` is not per robot. Without pooling, `z_i` only reflects `L`
  hops, so the arms may differ little when `L` is small. That affects every layout.

## Training and evaluation with Ray

- **Run entry point.** Examples 02 and 04 build the `PPOConfig` from `build_ppo_config` and run it with
  `ray.tune.Tuner`. `tune.RunConfig(stop={"num_env_steps_sampled_lifetime": budget})` holds the training budget,
  and `tune.CheckpointConfig(checkpoint_at_end=True)` saves. The budget is decision 2 (a). Until the author
  decides, the example passes it explicitly and there is no default. A budget in environment steps is equal across
  arms, because every arm samples `m` agent steps per environment step.
- **Checkpoints use Ray's defaults.** No `CHECKPOINT_DIR`. The path comes from the trial's `Result.checkpoint`, and
  Ray writes under `~/ray_results/<name>/<trial>/checkpoint_000000`. 04b takes `--checkpoint=<path>`. Spike 0C
  showed two loads that work. `RLModule.from_checkpoint(<ckpt>/learner_group/learner/rl_module/shared_policy)`
  needs no Ray and no env, but the three-level path is a layout detail of 2.57.0, so build it from the public
  constants `COMPONENT_LEARNER_GROUP`, `COMPONENT_LEARNER` and `COMPONENT_RL_MODULE` and guard it with a test
  that loads a fresh checkpoint. `Algorithm.from_checkpoint(path).get_module("shared_policy")` leaves the layout
  to Ray, but needs `register_env` with the same name and creator first, and starts Ray. Use the first for
  evaluation in 04b and the second where the env is already registered.
- **Dashboard.** Tune writes CSV, JSON and TensorBoard files for every trial by default. `tensorboardX` is
  installed. The `tensorboard` viewer is not. The Ray dashboard on port 8265 shows actors, tasks and logs, and I
  expect no training curves there without Prometheus and Grafana, so the curves are read in TensorBoard from
  the trial folder under `storage_path` (default `~/ray_results`). Spike 0C confirmed this. The dashboard serves
  actors, tasks, jobs and logs only, and TensorBoard serves the scalars, tagged `ray/tune/...`.
- **Evaluation numbers stay in our evaluator.** `RunMetrics`, the paired test and the trace come from a
  single-process, deterministic `run_episode`. Tune and RLlib evaluation runners are not used for thesis scores.
- **Evaluation of a learned arm.** `run_episode(..., policy=...)` builds the adapter, so training and
  evaluation build observations in one place. The policy function takes an `RLModule`, runs
  `forward_inference`, and samples a legal slot with the seeded stream `DecentralisedController` uses
  (decision 17 stays open). It does not know how the module was loaded.
- **Runtime κ(t).** The policy function records its forward pass and sampling through
  `record_routing_runtime`. The adapter records its observation build the same way. Whether the observation
  build counts as routing time goes in the PR description.
- **Not in L4.** The sweep command with `Tuner` over the TBD-by-sweep rows, and `ray.remote` over the study grid.
  Both are follow-up PRs.

## #103 items closed

- the two "config" reward-gating items
- the reward's congestion term
- the action mask for all arms
- `build_ppo_config` accepting all arms, and `team_mean`
- the timing of the mean runtime
- the encoder over a whole graph or a zone (from #64)
- the ad hoc evaluation seeds and the `--regime matched` parser (B14)
- #86 and #104, with #104's title only partly met (see the first decision)

Tick these as stale on `main`, found while designing: gamma passed to PPO (#112), training seeds used (#116),
action-sampling seed from `reset` (#117), and "δ is None unless configured".

## Tests and golden checks

- **Golden comparison.** On `origin/main`, record `RunMetrics` (runtime fields excluded) and the B15 trace
  for prioritised A\* and Token Passing, three seeds each. After every commit they must be identical.
- The four checks, with the replay test updated to the new observation shape, for both planners and for an
  untrained module in each arm.
- New unit tests for stage timing (a robot assigned at the start of a tick sees its target in the observation it
  acts on), the `Assigner` reset order, the three windows, the halo and `check_partition`, the cap error, the
  credit transform, `team_mean` with decentralised raising, and the reward with a non-zero congestion term.
- One PPO iteration through `build_ppo_config` for each controller, and one Tune run of two iterations.
- Example 01 for Token Passing (the A\* example is broken on `main` and left as it is), 02 (`02_storage_ladder.py`, plus `02_centralised_fixed.py` which becomes runnable), 04 and
  04b at the smallest settings. 04b needs a retrained checkpoint.
- The commands in "Checks before pushing" in `fix_prs_plan.md`.

## Work packages for agents

**The agent-ready plans are in `L4_agent_plans/`, one file per package.** They supersede the commit order in this
section. The order there is A1 stage timing, A2 `Assigner`, one step mode and planner driver, A3 reward, A4 adapter,
A5 policy function, A6 examples and Ray, with B1 zones, B2 window and B3 pooling as parallel packages. The reason is in
the README of that folder. The stage move cannot come before the `Assigner` without leaving the self-assigning router
broken, so A1 resolves it eagerly as a temporary step. The repo rules say agents never run `pytest`, `black`, `flake8`
or `mypy` and never push, so the plans have agents write the tests and hand back the commands. "Done when" lines
below that mention tests mean tests written, not tests run. The example 01 fix in the old list is dropped, by
the author's decision.

Rules for every agent. Read "Rules for every run" in `fix_prs_plan.md`, `AGENTS.md`, and the repo's `CLAUDE.md`. Work in
a git worktree off `origin/main`, never the main checkout. Run with
`PYTHONPATH=<worktree>/src /home/bjarkek/.venvs/rl/bin/python`. Do not push to `main`, do not merge, do not run
`gh pr create`, and do not open issues. Do not edit `thesis/`. Write in UK spelling with no dashes as punctuation
and no colons or semicolons joining clauses. A value the thesis marks TBD stays a config parameter with no default.

**Step 0, three read-only spikes, run in parallel.**

- **0A. Golden capture (done, see "Spike results").** Write a script in the scratchpad that runs prioritised A\* and Token Passing for
  three seeds on the example 01 instance, and saves `RunMetrics` (runtime fields excluded) and the trace JSONL.
  Output is a folder of files and the script. Done when running it twice gives identical files.
- **0B. Cost of one pass per robot (done, passes the gate, see "Spike results").** Time the encoder forward pass for `m` robots over a whole padded graph at
  the example 04 instance size, for `m` in 6, 10 and 20, with `L` in 1 and 2. Report seconds per step and
  the ratio to the decentralised field of view. This is the gate for layout R. If one training step is more
  than about ten times the decentralised cost, stop and report to the author.
- **0C. Ray spike (done, see "Spike results").** On the current code, check on Ray 2.57.0 that `tune.Tuner` runs a two-iteration PPO from
  `build_ppo_config`, that `stop` on `num_env_steps_sampled_lifetime` works, where the default checkpoint lands,
  whether `Algorithm.from_checkpoint` works after `register_env` in a fresh process, and which files Tune writes.
  Report the exact calls.

**Track B, can start with step 0. New files only, no env change.**

- **B1. `environment/zones.py`, `aisle_index` and tests.** Add `aisle_index: dict[VertexId, int]` to
  `GeneratedInstance`, derived when the instance is built (the lattice column of the vertex), so zones do not
  depend on display positions, which the generator calls "visualization metadata only". Then `zones_by_aisle`,
  `halo` and `check_partition`, pure functions with no Ray. Done when the tests cover `p = 1` (empty halo, one zone
  equal to `V_mov`), `p` equal to the number of aisles, a split of 7 aisles into 3 zones (3, 2 and 2 aisles), a
  disjoint cover on a generated instance including its cross-aisle vertices, a halo across a zone boundary,
  determinism, and `num_zones` above the number of aisles raising.
- **B2. Window in the observation builder.** Add the window argument to `build_observation` and
  `encode_all_observations`, keeping the default (the `d_obs` ball) so nothing changes yet. δ stays on the
  field of view. Add the cap check for the larger windows. Done when existing tests pass and new tests cover the
  three windows.
- **B3. Pooling.** After B2. Add the pooling field to `GNNEncoderConfig` with no default, a masked mean readout over
  `pool_mask`, and the `pool_mask [N]` key in `encoded_observation_space`, `as_rllib_dict` and
  `encode_all_observations`. The head input width follows the pooling setting. Done when tests show the mean
  ignores padding and halo vertices, pooling is absent when the field says none, a loss reaches the encoder
  through the pooled term, the padded logits still match the unbatched oracle, and one PPO iteration runs
  through `build_ppo_config`.

**Track A, one worktree and one branch `fix/one-env-adapter`. Commits in order, each passing the tests alone.**

0. Not a step. `examples/01_baseline_fixed_prioritised_astar.py` cannot build its instance on `main`, and the
   author decided on 2026-10-13 not to fix it in this work. It is left as it is, and nothing here is checked
   through it.
1. **Stages 1 and 2 move to the end of `step` and into `reset`.** Both step modes still work. Done when the
   golden comparison is identical and a new test shows a robot assigned at the start of a tick sees its target.
2. **`Assigner`.** Add the protocol and constructor argument, call `reset` before the `t=0` assignment, and
   replace the `SelfAssigningRouter` check in the env. Done when the golden comparison is identical and Token
   Passing still passes its tests with `assigner=planner`.
3. **One step mode and the planner driver.** Delete the `actions=None` path, the lazy router, `routing.py`, the
   router classes and `SelfAssigningRouter`. Add `planners/driver.py` and rewrite `run_episode`, examples 01 and
   the tests that call `step()` with no argument. Done when the golden comparison is identical and
   `test_correctness_invariants.py` passes through the driver.
4. **Reward for every arm.** Remove the gate, relax the config validator, compute δ once and pass it on.
   Done when a test shows a non-zero congestion term and the golden comparison is identical for planner runs.
5. **The adapter for every arm.** Cherry-pick B1 and B2. Wire the windows, `zones`, caps, `credit_signal`,
   `core`, and `build_ppo_config` for all arms. Update the callbacks to use `core`. Done when one PPO iteration
   runs for each controller and `test_training_progress.py` passes.
6. **Policy function and runtime.** Add the policy function and `run_episode(policy=...)`. Delete
   `DecentralisedController` as a controller, the singleton, `controllers/registry.py`, `controllers/base.py`,
   `controllers/section_based.py` and their tests. Move κ(t) timing. Done when a learned arm evaluates through
   `run_episode` with an untrained module and the four checks pass.
7. **Examples, checkpoints and docs.** Use the findings of 0C. Rewrite examples 02, 04 and 04b around
   `Tuner` and Ray's checkpoint calls, and absorb B14. Raise `max_local_nodes` in example 04 so no window is
   truncated (author, 2026-10-13), and say so in the example. Add the training budget field (see the notes on the
   answers). Add `tensorboard` to the dev extras in `pyproject.toml` (author, 2026-10-13). Delete `training/utils.py`. Rewrite
   `docs/controller_integration.md`, `docs/TRAINING.md` and the README parts that name the removed code. Done when
   the examples run at the smallest settings.

Hand back. The golden comparison output, the commands in "Checks before pushing" in `fix_prs_plan.md`, the results of 0B and 0C,
and a list of every choice flagged for the PR description.

## Flagged choices for the PR description

- The simulator and the RLlib adapter stay two classes, against the title of #104.
- Stages 1 and 2 moved to the end of `step`, which changes what a trained policy sees at an assignment.
- Layout R. One pass per robot in every arm, which is `[A8]` option 1.
- Pooling. Centralised pools over the whole graph and section-based over its zone only, not the halo. Decentralised
  does not pool.
- Windows larger than `max_local_nodes` raise instead of truncating (decision 15). Example 04's cap of 12 already
  truncates the decentralised field of view, so the example's cap is raised (author, 2026-10-13).
- `team_mean` group is the zone that owns the robot at the start of the step.
- Whether the adapter's observation build counts as routing time in κ(t).
- Old checkpoints do not load.

## Questions for the author

1. The zone rule, (a), (b) or (c) above. Is the thesis wording acceptable? Didnot find the reference. 
2. Global pooling (`[A8]`). Leave it TBD, or decide it before L4 so that the arms differ? What would be the best? is it not just a average pooling 
3. The credit signal (`[A9]`). Build the transform and leave it unset? Leave it unset, but i want a preparation for it. No gonna be part of the thesis
4. Decision 2, the training budget field. Decide before step 7, or pass it explicitly in the examples? what mae sense 
5. May I open gap issues for the zone rule and the two thesis sentences? None are opened yet.
6. `tensorboard` 2.21.0 is now installed in `~/.venvs/rl`. Add it to the dev extras in `pyproject.toml` in step 7? yes
7. Fix example 01 for prioritised A\* as its own PR before L4, or as commit 0 here? don't fix
8. The cap rule and example 04. The example truncates its field of view at 12 nodes while most fields of view are
   larger. Raise the cap in the example (and say so), apply the raising rule only to the centralised and section
   arms, or leave it to decision 15? yes rause the cap

## Notes on the answers (2026-10-13)

Settled by the author's answers above.
- **Question 3.** The credit signal stays unset, with no default. L4 builds the `team_mean` transform and its tests
  as preparation only. It is not part of the thesis experiments and gets no thesis wording.
- **Question 5.** Not answered, so no gap issue is opened.
- **Question 6.** `tensorboard` goes into the dev extras in step 7.
- **Question 7.** Example 01 for prioritised A\* is left broken. Nothing in L4 is checked through it.
- **Question 8.** The cap in example 04 is raised so that no window is truncated. The raising rule then applies to
  every arm, including the decentralised one.

Still open. My view on each, for the author to decide.

**Question 1, the zone rule. Decided by the author on 2026-10-13, zones follow the aisles.** There is no
reference for any partition rule, and none is invented. The rule is defined in one sentence in the thesis as a
design choice.
- **The rule.** Number the aisles left to right and split them into `p` blocks of consecutive aisles, as equal as
  possible, with the earlier blocks taking the extra aisle. A movable vertex belongs to the block of its aisle.
  On the example 04 instance (7 aisles, 51 movable vertices) `p = 2` gives aisles 0 to 3 and 4 to 6, and `p = 3`
  gives 3, 2 and 2 aisles. `p = 1` is the whole graph, and `p` equal to the number of aisles is one zone per
  aisle. Checked on that instance, where cross-aisle vertices sit on the lattice column of an aisle.
- **Why this one.** It follows the physical meaning of "section", and it is easy to defend without a citation.
  The nearest-seed rule is dropped. Another reader can still object that aisles are a layout choice of the
  generator. A hand-built graph simply passes its own `zones`.
- **What it needs.** `generate_and_validate`, which examples 02, 04 and 04b use, returns only the graph and
  discards the instance. The examples must keep the `GeneratedInstance` (or its `aisle_index`) for the section
  arm. This is a small change to the examples in step 7 and adds `aisle_index` to the generator (B1).
- **Open for the author.** The value of `p` is a sweep parameter, with no default. I have no basis to suggest one.

**Question 2, global pooling. Decided by the author on 2026-10-13, pool each arm over its own space.**
Pooling is the masked mean of the final-layer embeddings over the arm's window, appended to `z_i`. It is the
standard graph-level readout, and it fits `[A18]` because attention is listed as future work. It is needed because
without it `z_i` reflects only the vertices within `L` hops of the robot's own vertex, so a larger window adds
nothing (`sec:method:model` says the same).
- **Where each arm pools.** Centralised pools over the whole graph. Section-based pools over its zone. Decentralised
  has no pooled term, which matches the thesis row "centralised and section-based readout". The arms are trained
  and run separately, so the readouts do not interact. A difference in architecture between arms is already part
  of the thesis ("they differ only in the graph the encoder runs on and in which agents it produces action
  heads for"), and the pooled term follows that window.
- **The right amount of space.** Pool over real vertices only, never over padding. For the section arm, pool over
  the zone `Y_q` and not the halo, because the halo is read-only context with no heads. That needs a
  fixed-shape `pool_mask [N]` in `observations`, 1 for vertices to pool over and 0 for halo and padding. For the
  centralised arm it equals `node_mask`. This choice, zone only against zone plus halo, is flagged for the author.
- **Config.** `GNNEncoderConfig` gets a pooling field with no default, because the thesis marks the row TBD. The
  author's decision fills the row, and the thesis edit to `eq:readout` and `tab:modelparams` is the author's.
- **Cost.** `z_dim` grows by `D` for the arms that pool, and the merged L3 head input widens with it. It is a
  small change to merged code, so it is its own small PR in Track B (package B3) before step 5.
- **Caveats.** A mean over many vertices dilutes a local signal, so a far-away jam may barely move it. A sum or a
  max would behave differently. I have not tested any of them, so mean pooling is a plausible choice and not a
  verified one. The pooled term also widens the readout slightly, which adds a little to the cost measured in
  spike 0B.

**Question 4, the training budget. Decided in this plan, on my recommendation, because the author left it to me.**
The thesis already counts the budget in environment steps (`tab:trainparams`), so decision 2 option (a)
follows the text. Step 7's Tune stop needs the number anyway. Add the field now in the training config next to
`PPOHyperparameters`, not in `ExperimentConfig`, as `training_budget_env_steps: PositiveInt` with no default, and
pass an explicitly illustrative value in the examples. The stop overshoots by up to one `train_batch_size`, so
report the steps actually sampled. The value stays TBD in the thesis. This is cheap to reverse, and the author
can overrule it.

**Question 5, gap issues. Still open.** Opening an issue is visible outside this folder, so I am not doing it
without a yes. I recommend opening three, in English with the usual labels. The first is the zone rule (a design
choice the thesis does not define, with the aisle rule above). The second is the two sentences in
`sec:method:controllers` and the `[A8]` paragraph that say the encoder runs once per timestep on `G` and that agents
share one graph pass. The third is the pooling decision, covering the `eq:readout` and `tab:modelparams` rows.

## Spike results (2026-10-13)

Run by subagents, read-only against a clean worktree of `origin/main` (0961081). Scripts and outputs are in the
scratchpad of the session that wrote this plan. I have not re-run them.

**0A. Golden capture. Done.**
- Two runs of the capture script gave byte-identical metrics and traces for all 12 files.
- Setup. Prioritised A\* and Token Passing, seeds 0, 1 and 2, fixed storage, horizon 1000, about a minute in
  total. The instance and storage come from `examples/01_baseline_fixed_centralised.py` (6 agents, generator
  seed 42). Each planner uses its own example's `build_config` with only `horizon` overridden.
  `mean_decision_runtime_seconds` is excluded as the only wall-clock field. The traces have no timing.
- Compare with `./compare_golden.sh golden <new_run>`, which prints `IDENTICAL` on a match. Rerun with
  `PYTHONPATH=<worktree>/src ... capture_golden.py --out <dir> [--worktree <dir>]`.
- The script loads the example files by path. If L4 rewrites example 01, copy the builders into the script first.
- **Finding.** `examples/01_baseline_fixed_prioritised_astar.py` cannot build its instance on `main`
  (`GeneratorParams` rejects `num_aisles`, `aisle_length`, `num_cross_aisles`). The A\* arm ran on the Token
  Passing instance. The author decided not to fix the example (see the answers to the questions).
- **Finding.** Prioritised A\* seed 2 completes 5 tasks in 1000 ticks, against 14 and 27 for seeds 0 and 1. This
  is probably the livelock noted in the example (#55). It is valid golden data but not a healthy baseline. Token
  Passing completes 83, 49 and 98.

**0B. Cost of one pass per robot. Done. Layout R passes the gate.**
- Method. Real repo code, torch only, CPU, 8 threads, no Ray. The model is `GNNPolicyValueModel` with
  `hidden_width` 32 and `communication=False`, on the example 04 instance (51 movable vertices, 130 directed
  edges, `d_max` 4). Inputs come from `encode_all_observations`. The whole-graph window was built without editing
  the repo, by setting `observation_depth` very large and `max_local_nodes` to 51. Fleet sizes 6, 10 and 20 are
  synthetic because the instance has only 3 endpoints. Timing is the median of 96 interleaved samples per cell.
  The machine was busy with the parallel spikes, so absolute milliseconds are inflated and the ratios are the
  reliable part. The minimum-time ratios agree within about 10%. I have not re-run it.
- Result for one training step (forward plus backward, `L=2`). The whole-graph window costs 1.1 to 2.5 times the
  example 04 decentralised window at rollout batch size, and 3.3 to 4.7 times at training minibatch sizes (128
  to 1024 rows). Against the unrestricted decentralised window (`d_obs=5`, no truncation) it costs about 1.5
  times. `L=1` gives lower absolute times and similar ratios.
- Gate. The stop line was more than about ten times. The worst cell is 4.7 times. The per-iteration estimate for
  the example 04 batch is 2.5 to 2.8 times, estimated from per-row costs and not measured end to end. It
  leaves out environment simulation, Ray overhead and GAE, which are the same for every arm.
- Observation build in Python per environment step is about twice as slow for the whole graph (7.7 ms against
  3.8 ms at `m` = 20). It grows linearly with `m` and is not negligible next to the forward pass at rollout
  batch size.
- Memory. 5,572 bytes per whole-graph sample, against 1,360 for example 04's 12-node window. A 600-step rollout is
  about 67 MB at `m` = 20.
- Limit. A rough linear model puts the ratio at ten times near 120 movable vertices, so a larger instance than
  example 04 needs this check again.
- The zone plus halo window sits between the two windows, so it costs less than the whole graph.
- **Finding.** Example 04 sets `max_local_nodes` to 12, but a `d_obs=5` field of view has 4 to 33 vertices (mean
  17.3), and 73% of vertices exceed 12. So the decentralised arm in the example already truncates by `eta`
  (decision 15, #66), which is why its cost looks so low. The fair comparison is the unrestricted window.
- **Finding.** Under the plan's rule that a window larger than `max_local_nodes` raises, the centralised and
  section arms need `max_local_nodes` of at least 51 on this instance. The same rule would reject example 04's
  decentralised setting, so the example needs a larger cap, or the rule is limited to the two wider arms.
- Layout R means one pass per robot because `eta` is per robot, which is `[A8]` option 1.

**0C. Ray, Tune and checkpoints on Ray 2.57.0. Done, with current code.**
- `tune.Tuner("PPO", param_space=config, run_config=tune.RunConfig(name=..., storage_path=..., stop={...},
  checkpoint_config=tune.CheckpointConfig(checkpoint_at_end=True)))` ran a 2-iteration PPO from
  `build_ppo_config`. Pass the `PPOConfig` object, not `to_dict()`. `TrainingProgressCallbacks` is part of the
  config and needs no extra wiring. The `register_env` closure travels inside the config.
- `stop={"num_env_steps_sampled_lifetime": N}` stops at the first iteration whose total reaches N, so it
  overshoots by up to one `train_batch_size`. The key is at the top level of the result.
- `Result.metrics` keeps every key `format_iteration` reads.
- Default checkpoint. `~/ray_results/<name>/<trial>/checkpoint_000000`. With only `checkpoint_at_end=True` there is
  one checkpoint, numbered 0. The folder holds `algorithm_state.pkl`, `env_runner/` and
  `learner_group/learner/rl_module/shared_policy/`. Tune also writes `result.json`, `progress.csv` and
  `events.out.tfevents.*` per trial.
- `Algorithm.from_checkpoint` works in a fresh process after `register_env`, and fails with "Environment ...
  doesn't exist" without it. Ray need not be started first. Each call leaves an empty timestamp folder in
  `~/ray_results`.
- `RLModule.from_checkpoint(<ckpt>/learner_group/learner/rl_module/shared_policy)` works with no Ray and no env
  and gives the same logits as the `Algorithm` route. `RLModule.from_checkpoint(<ckpt root>)` fails.
- The Ray dashboard on port 8265 shows no training curves. TensorBoard 2.21.0, started with `--logdir` on the
  results folder, served the scalars (125 tags, prefixed `ray/tune/`). Tune's printed `--logdir` hint points at
  the wrong folder.
- `forward_inference` changes the batch dict in place, so build a fresh batch per call. Tune prints a long config
  table that `verbose` does not silence.
- `tensorboard` 2.21.0 was installed into `~/.venvs/rl`. It is not in `pyproject.toml` yet.

## Measured while designing

Importing the plain env takes 0.19 s, and importing `training/env.py` (which pulls in Ray) takes 2.36 s.
The adapter is 162 lines. Ray 2.57.0 has `tune.Tuner`, `RunConfig`, `CheckpointConfig` and the
`num_env_steps_sampled_lifetime` metric key, and `tensorboardX` is installed. Nothing else in this section was
run.
