Run these in order.

1. Record a run (about a minute). I've already recorded one, so skip this unless you want a fresh recording. If you rerun it, keep the new folder name watch_step12_b, because the sweep skips runs already in a folder.

cd ~/Documents/thesis/slap-mapd-coupling
~/.venvs/rl/bin/python scripts/sweep/load_sweep.py --config configs/step12/fleet_8.yaml --rates 0.12 --seeds 1 --storage-modes demand --horizon 2000 --trace-seeds 1 --out ~/thesis_runs/watch_step12_b

2. Watch it in the viewer:

cd ~/Documents/thesis/slap-mapd-coupling
~/.venvs/rl/bin/python -m slap_mapd_coupling.viz.pygame_renderer ~/thesis_runs/watch_step12/traces/demand_rate0.12_seed0.jsonl

If you recorded a new run in step 1, use ~/thesis_runs/watch_step12_b/traces/demand_rate0.12_seed0.jsonl instead.