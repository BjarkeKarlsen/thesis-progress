# A6. Examples, Tune, Ray checkpoints, the budget field and docs [review]

Branch `fix/one-env-adapter`, continuing after A5. Read `00_rules.md` first. In this package you may run the examples at
their smallest settings, since an example is a script and not the test suite. Report what you ran.

## Goal

Examples 02, 03, 04 and 04b run through Ray Tune with Ray's default checkpoints. The training budget is a config field,
the examples absorb the three changes of B14, `tensorboard` joins the dev extras, and the docs and the changelog
describe the new structure. The findings of the spike on Ray 2.57.0 are in `../L4_design.md`, section "Spike results".

Thesis to read: `sec:method:training` (the two regimes, the seed split, the budget row), `sec:method:rl`.

## Changes

1. Budget. Add `training_budget_env_steps: PositiveInt` with no default to `PPOHyperparameters`
   (`training/config.py`), as the thesis counts the budget in environment steps and leaves the value TBD. The examples
   pass an explicit illustrative value and say so. If another place suits better, use it and say why.
2. Tune. Examples 02, 03 and 04 build the config with `build_ppo_config` and run
   `tune.Tuner("PPO", param_space=config, run_config=tune.RunConfig(name=..., stop={"num_env_steps_sampled_lifetime":
   budget}, checkpoint_config=tune.CheckpointConfig(checkpoint_at_end=True))).fit()`. Pass the `PPOConfig` object, not
   `to_dict()`. The callbacks are already part of the config. Print the checkpoint path from the result. The run stops at
   the first iteration at or above the budget, so print the number of environment steps actually sampled.
3. Checkpoints use Ray's defaults. Delete `training/utils.py` and every `CHECKPOINT_DIR`. Example 04b takes
   `--checkpoint=<path>` and loads the module with `RLModule.from_checkpoint` on
   `<checkpoint>/learner_group/learner/rl_module/shared_policy`, built from the public constants
   `COMPONENT_LEARNER_GROUP`, `COMPONENT_LEARNER` and `COMPONENT_RL_MODULE`. Add a test that saves a tiny checkpoint and
   loads it this way, so a Ray upgrade that moves the layout fails a test and not an evaluation. Write the test, do not
   run it.
4. Absorb B14 into example 04. The three changes are in the B14 section of `../fix_prs_plan.md`. One is already on
   `main` since #134 (7bf81d4), which made example 04 evaluate on one episode per evaluation seed from `split_seeds`.
   Keep that. The two that remain are that `--regime matched` trains under the same storage rule used at evaluation
   and its parser works (check what #134 left of the parser and its test `test_example_04_cli.py`), and that evaluation
   goes through `run_episode(policy=...)` and not an ad hoc loop. Note in the example that "matched" matters only once
   the online storage estimates exist. Decision 17 stays open, so evaluation uses the policy function's rule.
   #134 also added `iteration_record` to `training/callbacks.py` and a pooled-progress line to the trace summary,
   so read the current example 04 before rewriting it.
5. Window caps. Examples 02, 04 and 04b all set `max_local_nodes=12` with `d_obs=5`, but most fields of view are larger and
   the rule from package B2 raises when the env or the PPO config is built. This covers 04b as well as 02 and 04.
   Set the cap in each example from the graph, to the largest window that arm uses, so no window is truncated, and say
   so in the example. The author asked for this on 2026-10-13. Report the values for the example 04 instance (51 movable
   vertices, fields of view of 4 to 33 vertices).
6. Instances. The examples must keep the generated instance for the aisle indices. Replace the use of
   `generate_and_validate` in 02, 03, 04 and 04b with `generate_instance` followed by the connectivity and
   well-formedness checks from `instances/validation.py`, as `generate_and_validate` does. Keep the same seed and
   parameters, and confirm the same graph results.
7. Examples 02 and 03 (`02_centralised_fixed.py`, `03_section_based.py`) become thin variants of 04 for the centralised and
   section arms, with pooling set for each. Section uses `zones_by_aisle` with an illustrative `num_zones`. If either
   needs more than a thin variant, stop and report.
8. `pyproject.toml` and `requirements-dev.txt`. Add `tensorboard>=2.21.0` to the dev extras (the author said yes on
   2026-10-13).
9. Docs. Rewrite `docs/controller_integration.md`, since the registry and the `Controller` protocol are gone. It should
   describe the `Assigner`, the planner driver and the policy function. Update the controller registry paragraph in
   the repo's `AGENTS.md`, `docs/TRAINING.md` and the README parts that name removed code (grep for `get_controller`,
   `register_controller`, `PlannerRouter`, `DecentralisedController`, `save_checkpoint`). Add a `CHANGELOG.md` entry. Keep
   the repo self-contained, with no mention of files outside it.

## What to run

Run examples 04 and 04b at the smallest settings, and 02 and 03 if they are runnable at small settings. Run example 01
(Token Passing) too. Do not run the prioritised A\* example, which is broken on `main` by decision. State the commands
and the outcome.

## Done when

The examples above run at the smallest settings, the checkpoint test is written, `training/utils.py` is gone, the dev
extras list `tensorboard`, and the docs no longer name removed code.

## Flag in the hand back

Where the budget field went, how far the run overshot the budget, the caps you set, and any example that needed more than
a thin change.
