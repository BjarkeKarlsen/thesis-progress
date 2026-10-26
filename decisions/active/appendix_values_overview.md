# Where each appendix value goes

Written 2026-10-23. Every table and figure placeholder in the appendices, with the run that
fills it, the row field that gives each value and the file it is read from. The field
names and the reading order (check, result, why, cost, customer) are those of
`../../notes/measures_catalogue.md`. Where this file and the thesis differ, the thesis wins.

## How to fill a placeholder

1. Put the run's rows where the table below says. All paths are under
   `thesis-progress/results/`.
2. Redraw every figure and copy it into the thesis, from the workspace root.

   ```bash
   ~/.venvs/rl/bin/python thesis-progress/scripts/images/appendix_figures.py --copy
   ```

   A figure whose rows are missing is drawn as a placeholder that names the path it waits
   for. One appendix at a time works too, for example `appendix_load.py`.
3. Replace each `TBD` in the table with the value. Every `TBD` cell is listed below.
4. Replace the `% TODO: one or two sentences` above the figure or table with what it shows.
5. Write the value into Conclusion, and change its Source in `B.Parameters.tex` from
   *open* to *tested* or *derived*.
6. Build from `thesis/` with `python3 tools/sync_xrefs.py --build` and check that the
   undefined and multiply defined counts are 0.

Means are over seeds. A gain or a ratio against fixed storage is paired by seed
(`eq:relgain`). "of 20" counts the seeds that pass. The figure scripts do this already, so
for a table read the same numbers from the rows, or from the run's `summary.md` where it
has them.

## Status at a glance

| appendix | placeholder | rows | state |
|---|---|---|---|
| E | `fig:app:loadsweep`, `tab:app:capacity` | `arrival_rates/load_fleet<m>/` | rows for 8 to 64. `capacity.json` only for 8 agents, so 16, 32 and 64 need their capacity read again. 16 agents has no rate between 0.1 and 0.3 (`notes/parameter_sweep_2026-10-23.md`) |
| E | `fig:app:loadvalidity` | `arrival_rates/load_fleet<m>/` | drawn from real rows. Main load lines only for 8 agents |
| F | `fig:app:demandsweep` | `parameter_sweep/fleet_<m>/demand.*` | drawn for 8 agents. Copy fleets 16, 32 and 64 into `parameter_sweep/` from the sweep of 2026-10-22 |
| G | `tab:app:shelfcap` | none, derived | to calculate |
| G | `fig:app:storageperiod`, `fig:app:storagebeta` | `parameter_sweep/fleet_<m>/storage_rule.*` | drawn for 8 agents, the other fleets as above |
| H | `fig:app:horizontrace`, `fig:app:horizongain`, `tab:app:horizon` | `horizon/fleet_<m>/` | runs not built. The floor is 2000 steps (`[A61]`), the runs decide whether T must be longer |
| H | `fig:app:standstill` | `arrival_rates/load_fleet<m>/` | drawn for 8 agents only, since only it has a main load |
| I | `tab:app:window` | a window count, not built | to measure |
| I | `fig:app:rewardterms` | `training/fleet_8/<arm>/progress.jsonl` | waits for M5 |
| I | `fig:app:rewardcng`, `tab:app:deliver` | `reward_sweep/fleet_8/` | run not built, needs the author's go-ahead |
| J | `tab:app:rounds`, `tab:app:width` | validation rows per value | runs not built, need the author's go-ahead |
| J | `fig:app:trainingcurves`, `fig:app:traininghealth`, `tab:app:checkpoint` | `training/fleet_<m>/<arm>/` | waits for M5 |
| K | `tab:app:checks` | the assertion log | not found logged anywhere yet |
| K | `fig:app:timing` | `timing/fleet_<m>/<arm>/timing.jsonl` | waits for M4 |
| L | `tab:app:stock` | test runs | waits for the long run |
| L | `tab:app:check`, `tab:app:result`, `tab:app:cost`, `tab:app:backlog` | test runs | waits for the long run |

M4 and M5 are in `measures_plan.md`. The file names they will write (`progress.jsonl`,
`validation.jsonl`, `timing.jsonl`) and the fields `env_steps`, `policy_loss`,
`value_loss`, `entropy` and `kl` are assumed by the scripts. Change the script's
docstring and reader if M4 or M5 names them differently.

---

## E. Load and capacity (`E.Load.tex`)

### `fig:app:loadsweep` in `app:sweep`

`appendix_load.py`, `load_sweep_fleets()`, `app_load_sweep.png`. The Token Passing load
sweep under fixed storage, from `slap-mapd-coupling/scripts/sweep/load_sweep.py`.
(a) `backlog` against `arrival_rate / m`, (b) the share of seeds with `keeps_up_picks`
(solid) and `keeps_up_putaways` (dashed), `[A59]`. Markers from `capacity.json`.

### `tab:app:capacity` in `app:sweep`

One row per fleet. Rows from `arrival_rates/load_fleet<m>/`.

| column | value | from |
|---|---|---|
| capacity | the highest rate at which every seed keeps up, and every lower rate too | `capacity.json`, `by_mode.fixed.capacity` |
| first failing rate | the lowest rate that fails | `capacity.json`, `first_failing_rate` |
| main load | 0.6 of capacity | `capacity.json`, `main_load` |
| main load per agent | main load / m | calculated |
| picks keep up | seeds with `keeps_up_picks` at the main load | rows at `arrival_rate == main_load` |
| put-aways keep up | seeds with `keeps_up_putaways` at the main load | same rows |
| backlog slope | mean `backlog_slope` at the main load | same rows, `[A55]` |

The main load is usually not a swept rate. Then run the sweep once more at the main load
alone, or take the nearest rate and say so.

Also in Conclusion. The load levels of the three-agent pilot (`app:cal:load`) are
replaced by these main loads. Update `B.Parameters.tex` for `lambda_task` and the load.

### `fig:app:loadvalidity` in `app:load:validity`

`appendix_load.py`, `load_validity()`, `app_load_validity.png`. Mean `overflow_units` (a)
and `unplaced_units` (b) against `arrival_rate / m`, fixed storage, same rows. Decision 1
of the catalogue puts them here. The sentence to write is whether both are 0 at every main
load.

---

## F. Demand drift (`F.Demand.tex`)

### `fig:app:demandsweep` in `app:demand:sweep`

`appendix_load.py`, `demand_sweep()`, `app_demand_sweep.png`. Rows
`parameter_sweep/fleet_<m>/demand.skew`, `demand.rotation_period`, `demand.rotation_shift`,
from `scripts/sweep/parameter_sweep.bash`. Paired gain of demand over fixed
(`mean_service_time`), put-away cost (`mean_putaway_service_time`, demand over fixed) and
the two keep-up shares. These values are fixed by `[A34]`, so this is a robustness check,
not a calibration. No `B.Parameters.tex` change.

---

## G. Storage rule values (`G.StorageValues.tex`)

### `tab:app:shelfcap` in `app:storage:shelfcap`

Derived, no run. One row per fleet.

| column | value | from |
|---|---|---|
| starting stock | the largest starting stock of one shelf | the starting stock formula (`app:storage`, "The starting stock") |
| arrivals per period | the largest arrivals at one shelf over one storage period at the expected demand | the arrival equation (`app:storage`, "The arrivals") |
| required load | starting stock + arrivals per period | calculated |
| margin | the same epsilon as the arrivals (proposal, `Appendixes.md` section 2) | `arrival.margin` |
| capacity | required load times margin | calculated, then confirmed by the capacity check |

It should explain why 8 agents needed 300 rather than 200. Source in `B.Parameters.tex`
becomes *derived*.

### `fig:app:storageperiod` in `app:cal:period`

`appendix_storage.py`, `storage_period()`, `app_storage_period.png`. Rows
`parameter_sweep/fleet_<m>/storage_rule.epoch_length`, demand paired with fixed at the same
Delta (Delta is also the arrival period, so fixed changes with it). Keep the value where the
gain levels off. Then Delta in `B.Parameters.tex` becomes *tested*. From the 8-agent rows the
gain falls from about 0.5 at 50 to 0.3 at 400. The 2026-10-23 note says Delta >= 200 is
the only setting that lets demand keep up at 64 agents. That trade-off is the author's call.

### `fig:app:storagebeta` in `app:cal:beta`

`appendix_storage.py`, `storage_beta()`, `app_storage_beta.png`. Rows
`parameter_sweep/fleet_<m>/storage_rule.congestion_weight` (congestion rule), paired with
the fixed rows of `storage_rule.epoch_length` at Delta = 100. (d) is mean `mean_crowding`.
On 8 agents the gain, the put-away cost and the crowding are flat over beta from 0 to 4,
so beta does nothing there. Then beta in `B.Parameters.tex` becomes *tested*.

---

## H. Evaluation horizon and stall length (`H.Horizon.tex`)

### The horizon, `fig:app:horizontrace`, `fig:app:horizongain`, `tab:app:horizon` in `app:cal:horizon`

**Floor decided 2026-10-23 (`[A61]`): `T` is 2000 or more.** `tab:evalparams` now says so,
and the configs already use 2000. The exact value is still reasoned for from these two
figures, and it can only go up.

- `appendix_measures.py`, `horizon_trace()`. Episode traces of Token Passing, fixed storage,
  main load, in `horizon/fleet_<m>/trace_seed<k>.jsonl`
  (`slap_mapd_coupling.evaluation.trace`, the step lines `t`, `completed`, `backlog`).
  Run them long, for example 4000 steps, so the settling shows. The warm-up is where the
  backlog stops rising.
- `appendix_measures.py`, `horizon_gain()`. Test rows of Token Passing under fixed and
  demand storage in `horizon/fleet_<m>/load_sweep.jsonl`, run at horizons warm-up + k x 200
  for k = 1 to 10. The gain is paired by seed at each horizon. k is the smallest value at
  which the estimate stops moving.
- `tab:app:horizon`. Per fleet, the warm-up from the first figure, k from the second,
  T = warm-up + 200 k. Check that T covers several storage periods Delta.

Then `T` in `B.Parameters.tex` and `tab:evalparams`, and the configs, change together. That
is a model change, so it gets an `[Axx]` tag and a `GAPS.md` entry.

### `fig:app:standstill` in `app:cal:stall` (new subsection)

`appendix_measures.py`, `stand_still()`, `app_stand_still.png`. `longest_stand_still` of
the load sweep rows at the rate nearest each fleet's main load. The stall length is set
above what a healthy run reaches. Then "stall" in `B.Parameters.tex` changes from TBD.
On 8 agents the longest stand-still runs from 4 to 15 steps.

---

## I. Observation depth and reward weights (`I.Reward.tex`)

### `tab:app:window` in `app:cal:depth`

One row per fleet. |V| is filled from `[A57]`. "vertices in the window" is the mean number of
vertices within `d_obs = 5` of an agent, over agents, steps and seeds. Nothing logs it yet.
A short script over the instances in `results/instances/instances/fleet_<m>/` with a
breadth-first search from every vertex gives it without a run (a mean over vertices, not
over where agents stand, so say which). "share of V" is that over |V|. It shows whether
depth 5 of van Knippenberg et al. (2021), Table 5, transfers. Check the paper before citing.

### `fig:app:rewardterms` in `app:cal:reward`

`appendix_controllers.py`, `reward_terms()`, `app_reward_terms.png`. Each
`return_<term>` of `training/callbacks.py` divided by `episode_step * m`, mean over the
last tenth of the iterations in `training/fleet_8/<arm>/progress.jsonl`. It answers whether
the crowding term is about 20 times smaller than the step costs (`Appendixes.md` section 5).

### `fig:app:rewardcng` in `app:cal:reward`

`appendix_controllers.py`, `reward_cng()`, `app_reward_cng.png`. Rows
`reward_sweep/fleet_8/reward.congestion_weight/load_sweep.jsonl`, with `varied` and
`value` as in the parameter sweep and one trained checkpoint per arm and value. Fields
`mean_crowding`, `mean_blocked_time`, `throughput`. Choose the smallest `n_cng` that
lowers blocked time without lowering throughput. Needs the author's go-ahead (training runs).

### `tab:app:deliver` in `app:cal:reward`

`n_deliver` in {1, 10}, 8 agents, fixed storage, test seeds. "keeps up" counts `keeps_up`,
"mean service time" is `mean_service_time`, "throughput" is `throughput`. Rows
`reward_sweep/fleet_8/reward.deliver_reward/load_sweep.jsonl`. Needs the go-ahead.

---

## J. Model and training (`J.Training.tex`)

The number of validation seeds is open. The tables use "of 10" as a placeholder.

### `tab:app:rounds` in `app:cal:rounds` and `tab:app:width` in `app:cal:width`

L in {0, 1, 2, 3} and width in {32, 64}, 8 agents, one training seed each, each arm at the
checkpoint `[A60]` chooses. Columns on the validation seeds: `keeps_up` count,
`mean_service_time`, `mean_putaway_service_time` (the validation measures of the
catalogue). Rows `training/fleet_8/<arm>_L<L>/validation.jsonl` and `<arm>_w<width>`,
names to be fixed when the runs are set up. Needs the go-ahead. For width, check van
Knippenberg et al. (2021), Section 4.2, first. If they give it, cite it and drop the table.

### `fig:app:trainingcurves` in `app:cal:budget`

`appendix_training.py`, `training_curves()`, `app_training_curves.png`. Rows
`training/fleet_<m>/<arm>/validation.jsonl`, one per checkpoint and validation seed, with
`env_steps`. (a) the share with `keeps_up`, (b) mean `mean_service_time`. The ring is the
`[A60]` choice, computed in the script. The budget is where the slowest arm levels off.
Then the budget in `B.Parameters.tex` becomes *tested*.

### `fig:app:traininghealth` in `app:cal:budget`

`appendix_training.py`, `training_health()`, `app_training_health.png`. From
`progress.jsonl`, `policy_loss`, `value_loss`, `entropy`, `kl` against `env_steps`.

### `tab:app:checkpoint` in `app:cal:checkpoint`

One row per fleet and learned arm. "training steps" is the `env_steps` of the chosen
checkpoint, the rest as in `tab:app:rounds`, from the same `validation.jsonl`. M5 writes a
table of every checkpoint next to the run. Take the chosen row from it.

---

## K. Simulator checks (`K.Checks.tex`)

### `tab:app:checks` in `app:repro:results` (new subsection)

One row per assertion of `app:repro:checks`. "runs checked" is how many runs the assertion
ran on, "runs failed" how many raised it. Find out whether the assertions are logged per
run in `slap-mapd-coupling`. If they are not, the handoff says to leave a TODO rather than
claim a result.

### `fig:app:timing` in `app:repro:results`

`appendix_checks.py`, `timing()`, `app_timing.png`. The timing log of the catalogue,
`timing/fleet_<m>/<arm>/timing.jsonl`, one line per episode with
`{"parts": {part: {"seconds", "calls"}}}`. The part names in the script (`release`,
`assignment`, `observations`, `forward`, `resolution`, `moves`, `storage`, `crowding`,
`reward`, `measures`) are proposals for M4. Drawn for Token Passing and the decentralised
arm. Change `arms` in the call to show others.

---

## L. Full results (`L.Results.tex`)

### The test runs in full, `app:results:tests`

Test phase, 20 paired seeds, main load. One block per fleet, the 8-agent block drawn,
rows storage rule (fixed, demand, congestion) by controller. Every cell is a mean over
seeds of the test rows unless it says "of 20".

`tab:app:check`, group 1, check.

| column | field |
|---|---|
| picks keep up | count of `keeps_up_picks` |
| put-aways keep up | count of `keeps_up_putaways` |
| completed share | `completed_share` |
| backlog slope | `backlog_slope` |
| stalled runs | count of `stalled` |

`tab:app:result`, groups 2 and 3, result and why.

| column | field |
|---|---|
| $\bar\zeta_T$ | `mean_service_time`. For a run that does not keep up, report its throughput instead and mark the cell |
| wait for robot | `mean_wait_for_agent` |
| travel | `mean_travel_time` |
| blocked | `mean_blocked_time` |
| stock wait | `mean_stock_wait` |
| crowding | `mean_crowding` |
| robots busy | `robot_busy_share` |
| shelf taken | `mean_shelf_taken_wait`, Token Passing only (M3). Today's rows carry `mean_pick_wait_pickup_taken` and `mean_pick_wait_delivery_taken` instead. Decide which goes in |

`tab:app:cost`, groups 4 and 5, cost and customer, plus throughput.

| column | field |
|---|---|
| put-away service | `mean_putaway_service_time` |
| runtime $\kappa_T$ | `mean_decision_runtime_seconds` |
| order completion | `mean_order_completion` |
| orders per step | `orders_per_timestep` |
| $\Lambda_T$ | `throughput` |
| $\Lambda_T/m$ | `throughput_per_agent` |

`tab:app:backlog`, diagnostics, what the backlog is made of.

| column | field |
|---|---|
| waiting tasks | `num_waiting_tasks` |
| active tasks | `num_active_tasks` |
| waiting orders | `num_waiting_orders` |
| lines waited | `num_lines_waited` |
| put-aways released | `num_released_putaways` |
| put-aways done | `num_completed_putaways` |

The gain itself, `eq:rqformal` and `eq:relgain`, is computed across paired runs and belongs
in the main text, not in these tables. Validity (`overflow_units`, `unplaced_units`) at the
main load is a warning, reported in E.

---

### `tab:app:stock` in `app:results:stock`

Test runs at the main load, 20 paired seeds, one block per fleet (8 agents drawn). Rows are
storage rule by controller. All are means over seeds of the test rows.

| column | field |
|---|---|
| split SKUs | `mean_split_skus` |
| tasks per line | `mean_tasks_per_line` |
| old stock on prime | `mean_cold_prime_share` |
| unit age at pick | `mean_unit_age_at_pick` |
| updates | `num_storage_updates` |
| arrived units | `mean_arrived_units` |

These are diagnostics. Write about them only where a result needs explaining.

---

---

## Not placed in an appendix

- `arrival.margin` is swept (`parameter_sweep/fleet_<m>/arrival.margin`) but has no
  placeholder. It hardly changes the gain (`notes/parameter_sweep_2026-10-23.md`). If the
  author wants the cost graph over the margin (`thesis_plan.md` section 5), it can go in G
  with `sweep_figure` like Delta.
- `keep_up_ratio`, `mean_relocated_units`, `mean_relocation_distance` and the
  `total_service_time` fields are dropped by the catalogue and appear nowhere.
- The main result, the per-controller gain, and RQ4's throughput per agent across fleets,
  belong in the results chapter, not here.
