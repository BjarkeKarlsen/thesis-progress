# Handover: analyse the two-day queue and bring it into the appendices and the thesis

Written 2026-10-23 for the agent that picks this up after the queue has run. Read the whole file before starting, then the files it points to.

## Read first

1. `~/Documents/thesis/CLAUDE.md` and `AGENTS.md`. The writing style rules and the rule to discuss before rewriting apply to everything below. A change to the model gets an `[Axx]` tag in the chapter and an entry in `decisions/GAPS.md`. The last tag used is `[A61]`.
2. `thesis-progress/RUNS.md`, where every run writes.
3. `thesis-progress/notes/measures_catalogue.md`, what each number is for and the order a run is read in: check, result, why, cost, customer, then diagnostics and validity.
4. `thesis-progress/decisions/active/appendix_values_overview.md`, which placeholder of which appendix each value fills, and how to fill one. This handover does not repeat it.
5. `thesis-progress/notes/parameter_sweep_2026-10-23.md` and `decisions/ideas/learned_storage_pilot_plan.md`, what was found before the queue.

## What ran

`~/Documents/thesis/bedtime.bash` ran a queue. Its folder is the newest `~/thesis_runs/queue_<date_time>/`. `queue.log` has every job's start, end and failure. `code/` is the exact code it ran (`base_commit.txt` and `uncommitted.patch`). A `done_<job>` file marks a job that finished. A job missing its marker did not finish. Check the log before reading its results.

| job | what it answers | rows | fills |
|---|---|---|---|
| `sweep` | each fleet's capacity and main load under the check of `[A59]`, and how the gain, its cost and the check move with Δ, ε, β and the demand settings | `results/arrival_rates/load_fleet<m>/`, `results/parameter_sweep/fleet_<m>/` | `tab:app:capacity`, `fig:app:loadsweep`, `fig:app:loadvalidity`, `fig:app:demandsweep`, `fig:app:storageperiod`, `fig:app:storagebeta`, `fig:app:standstill` |
| `train8`, `train16`, `train32` | the decentralised arm trained under fixed storage (`fixed_only`) and under demand storage (`matched`), at each fleet's main load, the configs' budget (500 000 environment steps) | `~/thesis_runs/training/fleet_<m>/<regime>/`, progress copied to `results/training/fleet_<m>/decentralised_<regime>/progress.jsonl` | `fig:app:trainingcurves`, `fig:app:traininghealth`, `tab:app:checkpoint`, and later the main result |
| `shelfcap` | how far the shelf capacity lets a rule pile stock onto few shelves, and the smallest capacity fixed storage fits in | `results/shelf_capacity/fleet_<m>/` | `tab:app:shelfcap`, see below |
| `horizon` | the warm-up and the horizon at which the gain stops moving | `results/horizon/fleet_<m>/` (`trace_seed<k>.jsonl`, `load_sweep.jsonl` merged from `h<T>/`) | `fig:app:horizontrace`, `fig:app:horizongain`, `tab:app:horizon` |
| `pilot` | the learned storage rule with the whole-service-time credit (option A), at 8 and 64 agents | `~/thesis_runs/pilot/<date_time>/` | no appendix yet. It is a pilot (`learned_storage_pilot_plan.md`) |

Every Token Passing folder also has `timing.jsonl`, the seconds of every part of the step per episode. Training progress has `seconds_*`, `time_this_iter_s` and `timer_*`. Those fill `fig:app:timing`. The figure script expects `timing/fleet_<m>/<arm>/timing.jsonl`, so adapt its reader.

## How to analyse each job

Draw first, then read. From the workspace root:

```bash
~/.venvs/rl/bin/python thesis-progress/scripts/results/plot_parameter_sweep.py
~/.venvs/rl/bin/python thesis-progress/scripts/results/plot_storage_pilot.py ~/thesis_runs/pilot/<date_time>
~/.venvs/rl/bin/python thesis-progress/scripts/images/appendix_figures.py --copy
```

**sweep.** Read `capacity.json` and `summary.md` per fleet. Per fleet report the capacity, the first failing rate and the main load, and whether picks and put-aways each keep up at the main load. The main load is not a swept rate, so rows at it come from the parameter sweep's default points (every setting's default value is the same episode). For Δ, ε and β, the sweep gives an overview, not a tuned optimum (`[A61]`, Appendix D). Present the trade-off and let the author choose. Δ is the known trade-off, since a longer Δ lowers the gain at 8 and 32 agents but was the only setting that let demand keep up at 64 agents in the archive. The stall length is read from `longest_stand_still` at the main load, above what a healthy run reaches.

**train.** No checkpoint has been evaluated yet. `[A60]` chooses a checkpoint on the validation seeds by the shortest pick service time among those that keep up. `slap_mapd_coupling/training/evaluate_run.py` exists but chooses the checkpoint that completes the most tasks, which is drift from `[A60]` (fix it first, step M5 of `measures_plan.md`). Then evaluate the chosen checkpoint on the 20 test seeds under fixed and demand storage, paired. A run with no `done` file stopped early, and its last checkpoint is still usable. Resuming training is not built (`feat/train-resume` points at an old commit and holds no resume code).

**shelfcap.** The proposed reason for the shelf capacity, to discuss with the author before it goes in. The capacity is a property of the warehouse, set so the baseline fits. Fixed storage must never overflow at the main load, otherwise "fixed" is not fixed. So the capacity is the smallest tested value at which `overflow_units` and `unplaced_units` are 0 on every seed under fixed storage, rounded up. Then report what the capacity does to demand storage: `peak_shelf_fill_share`, `mean_shelf_fill_share`, the endpoint waits, the pick gain, the put-away cost and the check, against the capacity. The values tested start at the fullest shelf fixed storage reached in one episode with unlimited shelves (254.5, 159, 149.5 and 129 units for 8, 16, 32 and 64 agents) and go to about three times it. With unlimited shelves, demand storage put 451.5, 382.5, 857.5 and 1014.5 units on one shelf, so the capacity is what limits how far it concentrates. `tab:app:shelfcap` was planned as derived with no run. With these rows it can be tested instead, and its caption and Source in `B.Parameters.tex` change with it.

**horizon.** `[A61]` set the floor. T is 2000 or more. Read the warm-up from the traces (where the backlog stops rising) and the horizon at which the paired gain stops moving from `load_sweep.jsonl` (rows carry `horizon`). If it is above 2000, every run so far was at 2000, so say what changes and ask the author before rerunning anything.

**pilot.** Judge it like any run: the check, then pick service time, then put-away service time, paired against fixed, demand and random. Option A was chosen on 2026-10-23. Option B (pick time plus a penalty for put-aways falling behind) is the fallback if A gives up too much pick time. Whether the learned storage rule enters the thesis at all is open. `notes/how_the_system_works.md` recommends keeping the rules and naming it future work.

## What is known already (do not rediscover it)

- Under the check of `[A59]`, demand storage under Token Passing fails the put-away part at 32 and 64 agents almost everywhere. Its picks keep up.
- The cause is Token Passing's endpoint rule meeting a rule that sends many put-aways to the same few shelves. At 64 agents a demand put-away waits 510 steps for a shelf another robot's path ends at, out of a put-away service time of 531, against 16 under random storage. The wait for a taken receiving vertex is 0 everywhere.
- The archived sweep of 2026-10-22 (`results/archive_2026-10-22/`) has the same episodes as new runs, but its rows cannot be checked by kind (`row_keeps_up` returns None for them).
- In a training iteration at 8 agents, the learner update takes about 78 of 95 seconds and playing the episodes about 17.

## Not to do

- Do not open pull requests or commit in `slap-mapd-coupling`. The author opens them. The code changes of 2026-10-23 are uncommitted in the main checkout: the check by kind, the new numbers, the endpoint wait, the shelf fill, the timing log, and the sweep scripts. They are listed in `measures_plan.md` as M1 to M4. The pilot's code is uncommitted in `~/worktrees/pilot-learned-storage`.
- Do not commit or push `thesis/`. It syncs with Overleaf, and its changes since 2026-10-16 are uncommitted.
- Do not rewrite thesis prose before the author agrees. Propose the sentence, then apply it.
- Do not rerun a job into a folder with rows from different code without moving them first. Every sweep skips the rows it already has.

## Open decisions for the author

1. Δ, ε and β, from the sweep's overview.
2. The shelf capacity and its reason, from `shelfcap`.
3. The horizon, if the calibration puts it above 2000.
4. The stall length.
5. Whether the learned storage rule is in the thesis.
6. The number of validation seeds and the checkpoint frequency (`app:cal:checkpoint`).
