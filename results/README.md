# Results, one folder per appendix

Each folder holds the rows behind one appendix of `thesis/Appendices/`, and its own `README.md` says what it
answers, which figures and tables it fills, and the commands that made it. The commands are run one at a
time from the root of `slap-mapd-coupling`, not through `bedtime.bash`. `bedtime.bash` still writes the old
layout (`arrival_rates/`, `parameter_sweep/`, ...) and is not used for these folders.

| folder | appendix | what |
|---|---|---|
| `D_warehouses/` | D, warehouse generation | the instance report and the drawn warehouses |
| `E_load/` | E, load and capacity | the Token Passing load sweep, capacity and main load per fleet |
| `F_demand/` | F, demand drift | skew, rotation period and rotation shift at the main load |
| `G_storage/` | G, storage rule values | Δ, β, ε and the shelf capacity at the main load |
| `H_horizon/` | H, horizon and stall | traces of 4000 steps and rows at horizons 1000 to 4000 |
| `J_training/` | I and J | progress logs of the trained routers (checkpoints stay in `~/thesis_runs/training/`) |
| `plots/` | none | working plots, not thesis figures |
| `logs/` | none | the logs of the 2026-10-23 queue |
| `archive/` | none | earlier sweeps, kept for reference |

## What every folder shares

- **Graph v1.** Every row so far is on the warehouses of `instances/generator.py::fleet_defaults` as of
  October 2026: |V| = 16 m, m/2 storage vertices placed at random on aisle vertices, every edge two-way.
  If the generator changes, these folders move to `archive/graph_v1/` and the commands are run again.
- **Code.** The queue of 2026-10-23 ran `slap-mapd-coupling` at `1ae067f` plus the uncommitted changes in
  `~/thesis_runs/queue_2026-10-23_2344/code/uncommitted.patch`. The fleet 32 matched training was
  finished from its checkpoint at `e1abc67` (`~/thesis_runs/queue_2026-10-25_1902/code/`).
- **Rows.** One JSON line per episode with the fields of `RunMetrics` (`evaluation/metrics.py`). What each
  field is for is in `../notes/measures_catalogue.md`. Every Token Passing folder also has `timing.jsonl`,
  `summary.md` (the check per rate) and `capacity.json`.
- **Running.** Every command below starts from the `slap-mapd-coupling` root with `PY=~/.venvs/rl/bin/python`
  and `R=~/Documents/thesis/thesis-progress/results`. A sweep run again skips the rows it already has.
- **Figures.** From the workspace root, `~/.venvs/rl/bin/python thesis-progress/scripts/images/appendix_figures.py`
  redraws every appendix figure into `thesis-progress/scripts/Images/`. `--copy` also copies them into
  `thesis/Images/`.
