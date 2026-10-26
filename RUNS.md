# Where runs live on this PC

Decided 2026-10-23. Every run writes to one of these places, so a later run can continue from what is there and an analysis knows where to look. Nothing under `thesis_runs/` or `results/` is committed. `results/` is small and kept. `thesis_runs/` is large (checkpoints) and kept until a result is in the thesis.

| what | where | written by | continues how |
|---|---|---|---|
| Token Passing load sweeps | `thesis-progress/results/arrival_rates/load_fleet<m>/` | `overnight.bash` step 1 and 2 | a rerun skips rows already there |
| Token Passing sensitivity sweeps | `thesis-progress/results/parameter_sweep/fleet_<m>/<setting>/` | `overnight.bash` step 4 | same |
| Shelf capacity test | `thesis-progress/results/shelf_capacity/fleet_<m>/` | queue job `shelfcap` | same |
| Horizon calibration | `thesis-progress/results/horizon/fleet_<m>/traces/` (4000-step traces) and `h<T>/` (rows at horizon T) | queue job `horizon` | same |
| Archive of the 2026-10-22 sweeps | `thesis-progress/results/archive_2026-10-22/` | moved there 2026-10-23 | not rerun. The episodes are identical to new ones, only the newer fields are missing |
| Partial sweep of 2026-10-23 | `thesis-progress/results/archive_2026-10-23_partial/` | moved there 2026-10-23 before the queue | fleet 8 complete with the check of `[A59]`, fleets 16 to 64 stopped early. No shelf fill or timing fields. The queue reruns it all |
| Learned routers | `~/thesis_runs/training/fleet_<m>/<regime>/` (`fixed_only` or `matched`) | queue jobs `train8`, `train16`, `train32` | every checkpoint is kept. A `done` file marks a finished run. Resuming needs a resume option that is not built yet |
| Learned-storage pilot | `~/thesis_runs/pilot/<date_time>/` | queue job `pilot` | each night a new folder |
| Older pilot nights | `~/thesis_runs/archive/storage_pilot_2026-10-22/` and `storage_pilot_night_2026-10-22/` (moved 2026-10-23), `~/thesis_runs/storage_pilot_night_2026-10-23/` | the pilot script, before the queue | read only. The 2026-10-23 night's 64-agent stage was stopped |
| One queue | `~/thesis_runs/queue_<date_time>/` | `~/Documents/thesis/bedtime.bash` | `queue.log`, `code/` (the exact code it ran, with `uncommitted.patch`), `done_<job>` markers. `QUEUE=<that folder>` starts it again and skips done jobs |

Every row file is one JSON line per episode with the fields of `RunMetrics` (`slap-mapd-coupling/src/slap_mapd_coupling/evaluation/metrics.py`). What each field is for is in `notes/measures_catalogue.md`. Every Token Passing folder also has `timing.jsonl` (seconds per part of the step) and `summary.md` (the check per rate, and the capacity). Training writes `decentralised_<regime>_training_progress.jsonl` with the reward terms, the per-step seconds and RLlib's timers.

The figures are drawn from these folders by `thesis-progress/scripts/results/plot_parameter_sweep.py`, `plot_storage_pilot.py`, and the appendix scripts in `thesis-progress/scripts/images/appendix_*.py` (see `decisions/active/appendix_values_overview.md`).
