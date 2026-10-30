# Results, one folder per appendix

Each folder holds the rows behind one appendix of `thesis/Appendices/`. Its own `README.md` says which
parts of the appendix the rows fill and the exact commands that made them.

All the rows of E, F and G come from one run, the step 12 sweep (27 to 29 October 2026), run by hand
with the commands in each folder's README. Each README also holds what its part of the run found. The
sizing arithmetic is in `G_storage/README.md`. The next run, on the new settings
(Q = 12, 5 lines per order, a section of SKUs per workstation, top-rank safety stock, the fixed evaluator
of PR #199), replaces these rows.

| folder | appendix | what | fills |
|---|---|---|---|
| `D_warehouses/` | D, warehouse generation | the instance report and the drawn warehouses | Appendix D figures and tables |
| `E_load/` | E, load and capacity | Token Passing load sweep under fixed storage, capacity and main load per fleet | `app:load:first`, `tab:app:firstsweep` |
| `F_demand/` | F, demand drift | skew, drift period and drift step at the main load | `app:demand:sweep`, `fig:app:demandsweep` |
| `G_storage/` | G, storage rule values | storage period, congestion weight, refill size, the random check, the safety stock check | `app:cal:period`, `app:cal:beta`, `app:cal:refill`, `app:cal:random`, `app:cal:safety` |
| `K_checks/` | K, checks | the Ma et al. (2017) Token Passing reproduction | `app:repro:ma` |

## What every run shares

- **Code.** `slap-mapd-coupling` at `1056911` (branch `feat/flow-and-start`) with the path cache fix of
  `12fdd59`, copied to `~/thesis_runs/queue_2026-10-27_1330/code_step12/`. Every command below runs from
  that folder, so it uses exactly that code.
- **Settings file.** `configs/step12/fleet_<m>.yaml` in that folder, one per fleet (8, 16, 32, 64 agents):
  20, 30, 50 and 100 SKUs, Q = 30, one line per order, 4, 8, 16 and 32 workstations.
- **Episode.** 10000 steps, the first 5000 left out (`--horizon 10000 --warmup 5000`), 20 seeds, each seed
  its own warehouse. Token Passing.
- **Before the commands.**

      cd ~/thesis_runs/queue_2026-10-27_1330/code_step12
      export PYTHONPATH=src
      PY=~/.venvs/rl/bin/python
      R=~/Documents/thesis/thesis-progress/results

- **Rows.** One JSON line per episode with the fields of `RunMetrics` (`evaluation/metrics.py`), in
  `load_sweep.jsonl`. Next to it `summary.md` (the check per rate), `capacity.json`, `timing.jsonl`, and
  for the sensitivity sweeps `config.yaml` (the settings file the values were varied from).
- **Lost.** The run's `.log` files were never in git (`*.log` is ignored) and were deleted in the clean-up
  of 2026-10-30. The queue's own log is still in `~/thesis_runs/queue_2026-10-27_1330/queue.log`.
- **Old runs.** Everything from before step 12 is in git history, and its run folders are in
  `~/thesis_runs/archive_old_model/`.
