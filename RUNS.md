# Where runs live on this PC

Updated 2026-10-30, after the clean-up that kept only the step 12 sweep.

| what | where |
|---|---|
| Token Passing rows, one folder per appendix | `thesis-progress/results/<letter>_<topic>/` (`E_load`, `F_demand`, `G_storage`), see `results/README.md` for which folder fills which appendix part and the exact commands |
| The step 12 queue, its code copy and log | `~/thesis_runs/queue_2026-10-27_1330/` (`code_step12/` is the code every command in `results/` runs from) |
| Stored warehouse tables (one warehouse per seed) | `~/thesis_runs/warehouses/` |
| Everything from before step 12 | git history of `thesis-progress`, and `~/thesis_runs/archive_old_model/` (old queues, watch runs, pilots, and the old learned routers in `training/`, which no longer load) |
| New learned routers | `~/thesis_runs/training/fleet_<m>/<regime>/`, written by the `train<m>` jobs of `bedtime.bash` |

Every row file is one JSON line per episode with the fields of `RunMetrics`
(`slap-mapd-coupling/src/slap_mapd_coupling/evaluation/metrics.py`). What each field is for is in
`notes/measures_catalogue.md`. `bedtime.bash` still writes the old layout (`arrival_rates/`,
`parameter_sweep/`), so move its rows into the appendix folders after a run.
