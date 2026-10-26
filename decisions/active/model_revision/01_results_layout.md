# 01. Results in one folder per appendix (done)

**Status.** Done on 2026-10-26, during the discussion and before the author had said to start. The author
asked to keep it and remove nothing. Only moves, no data deleted.

## What was done

- `thesis-progress/results/` now holds `D_warehouses/` (was `instances/`), `E_load/fleet_<m>/` (was
  `arrival_rates/load_fleet<m>/`), `F_demand/fleet_<m>/demand.*`, `G_storage/fleet_<m>/` (the storage rule
  and margin settings of the parameter sweep, and `shelf_capacity/`), `H_horizon/fleet_<m>/`,
  `J_training/fleet_<m>/decentralised_<regime>/`, `plots/`, `logs/` and `archive/`.
- `results/README.md` and a `README.md` in each appendix folder say what the rows answer, which figures and
  tables they fill, and the commands that made them, run one at a time and not through `bedtime.bash`.
- The paths in `thesis-progress/scripts/images/appendix_load.py`, `appendix_measures.py`,
  `appendix_storage.py`, `appendix_controllers.py`, `appendix_training.py`, `load_sweep.py` and
  `scripts/results/plot_parameter_sweep.py` point at the new folders.

## Still to do

- `thesis-progress/RUNS.md` still describes the old layout. Update it.
- `bedtime.bash` and `slap-mapd-coupling/scripts/sweep/overnight.bash` and `parameter_sweep.bash` still write
  the old layout. Either point them at the new folders or note in their header that they are not used.
- `appendix_controllers.py` and `appendix_training.py` read `J_training/fleet_<m>/<arm>/`, but the runs are
  named `decentralised_fixed_only` and `decentralised_matched`. Adapt the reader with step 10 or the reruns.
- When step 02 lands, move the graph v1 folders into `archive/graph_v1/`, keeping the same layout, and let
  the reruns write to the empty folders.
