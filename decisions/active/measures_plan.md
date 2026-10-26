# Plan: the measures of a run, grouped (2026-10-23)

Carries out the decisions of 2026-10-23 recorded in `../../notes/measures_catalogue.md`, with the thesis changes `[A59]` (keep-up for picks and put-aways separately) and `[A60]` (checkpoint choice on validation). Small PRs from `main` of `slap-mapd-coupling` (at `1ae067f`, field-of-view fix included), left uncommitted for the author.

**Status 2026-10-23.** M1 to M4 are done, uncommitted in the main checkout, with the shelf fill (`peak_shelf_fill_share`, `mean_shelf_fill_share`), shelf capacity as a sweep setting, `--trace-seeds` and `--stop-when-overloaded` in the load sweep, and the sweep runner of `overnight.bash`. `~/worktrees/measures-m1-m3` holds an earlier copy of M1 to M3 and is out of date. M5 (checkpoint choice of `[A60]`) and M6 (summaries) are open. The queue that uses all of this is `~/Documents/thesis/bedtime.bash`.

## M1. The keep-up check by kind, and the dropped fields (`[A59]`)

- `evaluation/metrics.py` and `evaluation/evaluator.py`. Add `keeps_up_picks` and `keeps_up_putaways`, and `keeps_up` becomes both. The pick backlog includes the orders waiting for stock. `completed_share` per kind.
- Drop `keep_up_ratio`, `mean_relocated_units`, `mean_relocation_distance`, `total_service_time` and its four related fields, with their validators. Fix the module docstring, which calls total service time the result (drift, #103).
- The load sweep's capacity reading uses the new `keeps_up` (`scripts/sweep/load_sweep.py`).
- Tests. A run with every pick finished and a third of its put-aways open fails.

## M2. The new numbers

- `backlog_slope`, the least-squares slope of `backlog_by_t` over the second half, per 100 steps (`[A55]`). The trace is already logged.
- `robot_busy_share`, the share of robot-steps in which the robot holds or heads for a task.
- `orders_per_timestep` (`[A56]`) and `throughput_per_agent` (`[A33]`), both divisions.
- Tests for each.

## M3. The wait for a taken shelf (Token Passing only)

- `planners/token_passing.py`. Each step, for every waiting task, count a step if it is unavailable only because another path ends at its pickup or delivery vertex. `mean_shelf_taken_wait` over the completed picks, and the same for put-aways. `None` under every other controller.
- This answers whether the endpoint rule causes the 64-agent failure.

## M4. The timing log

- A small timer with total seconds and number of calls per part. The environment step is timed in the six stages of the method section, with routing split into building the observations and the forward pass. The crowding measure, the reward and the end-of-run measures are timed too.
- One JSON line per episode in its own file, beside the rows. Not part of `RunMetrics`.
- Training adds RLlib's own sample, update and weight-sync timers to the same record.
- The timer must cost almost nothing. Check that a 64-agent episode is no slower than 2 %.

## M5. Checkpoint choice on validation (`[A60]`)

- Every saved checkpoint plays the validation seeds. Choose by the rule of `[A60]`, and write a small table of every checkpoint's validation numbers next to the run.
- Training logs every iteration only what the catalogue lists under "Training". Check what `training/callbacks.py` (`episode_metrics`, `progress_metrics`) already logs, and add only what is missing.

## M6. Summaries and plots show the groups

- The load sweep's `summary.md` and the pilot's `summary.md` show groups 1 to 5. Diagnostics go in a second table, and validity becomes a warning at a main load.
- `thesis-progress/scripts/results/plot_parameter_sweep.py` and `plot_storage_pilot.py` follow. The pilot figure drops `loaded_total` for put-away service time.

## Order

M1 first, because every later result is read through the check. M2 and M3 next, because the rerun of the sweeps should already carry them. M4 can go at any time. M5 waits for the long run. M6 goes last, or together with the PR it summarises.
