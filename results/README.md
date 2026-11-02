# Results, one folder per appendix

Each folder holds the rows behind one appendix of `thesis/Appendices/`. Its own `README.md` says which
parts of the appendix the rows fill and the exact commands that made them.

All the rows of E, F and G come from one run, the second step 12 sweep (31 October to 1 November 2026),
run by the bedtime queue (`bedtime.bash step12`, queue `~/thesis_runs/queue_2026-10-31_1610/`). Each
folder's README holds what its part of the run found, and how it compares with the first step 12 sweep
(27 to 29 October), whose rows are in git history at `524ef5a`.

| folder | appendix | what | fills |
|---|---|---|---|
| `D_warehouses/` | D, warehouse generation | the instance report and the drawn warehouses | Appendix D figures and tables |
| `E_load/` | E, load and capacity | Token Passing load sweep under fixed storage, capacity and main load per fleet | `app:load:first`, `tab:app:firstsweep` |
| `F_demand/` | F, demand drift | skew, drift period and drift step at the main load | `app:demand:sweep`, `fig:app:demandsweep` |
| `G_storage/` | G, storage rule values | storage period, congestion weight, refill size, the random check, the safety stock check | `app:cal:period`, `app:cal:beta`, `app:cal:refill`, `app:cal:random`, `app:cal:safety` |
| `K_checks/` | K, checks | the Ma et al. (2017) Token Passing reproduction | `app:repro:ma` |

## What every run shares

- **Code.** `slap-mapd-coupling` `main` at `18fefda`, copied to
  `~/thesis_runs/queue_2026-10-31_1610/code_step12/`. Every command below runs from that folder.
- **Settings file.** `configs/step12/fleet_<m>.yaml`, one per fleet (8, 16, 32, 64 agents). Everything
  scales with the fleet (`[A77]`). Per agent 16 walkable vertices, 5 shelves, 2.5 SKUs, half a
  workstation and one parking vertex, so 20, 40, 80, 160 SKUs and 4, 8, 16, 32 workstations. Each SKU
  belongs to a section of 20 SKUs, served by 4 workstations on neighbouring rack faces (`[A76]`,
  `[A77]`). An order goes to one workstation and takes all its lines from that section. Q = 10,
  5 lines per order (shifted Poisson), every SKU's safety stock sized at the most popular rank, the
  counting fixes of PR #199.
- **Episode.** 10000 steps, the first 5000 left out (`--horizon 10000 --warmup 5000`), 20 seeds, each seed
  its own warehouse. Token Passing.
- **The queue.** `scripts/sweep/overnight.bash` ran the load sweep (E), then
  `scripts/sweep/parameter_sweep.bash` at each fleet's main load (F and G), one fleet after another, on
  8 workers (6 at fleet 64). To repeat it by hand:

      cd ~/thesis_runs/queue_2026-10-31_1610/code_step12
      export PYTHONPATH=src
      PY=~/.venvs/rl/bin/python
      R=~/Documents/thesis/thesis-progress/results

- **Rows.** One JSON line per episode with the fields of `RunMetrics` (`evaluation/metrics.py`), in
  `load_sweep.jsonl`. Next to it `summary.md` (the check per rate), `capacity.json`, `timing.jsonl`, and
  for the sensitivity sweeps `config.yaml` (the settings file the values were varied from).
- **Logs.** `*.log` is not in git. The queue's logs are in `~/thesis_runs/queue_2026-10-31_1610/`
  (`queue.log`, `logs/`). The first sweep's untracked files are in
  `~/thesis_runs/queue_2026-10-27_1330/old_results_untracked/`.
- **Old runs.** Everything from before step 12 is in git history, and its run folders are in
  `~/thesis_runs/archive_old_model/`.
