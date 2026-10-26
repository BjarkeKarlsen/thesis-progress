# 11. Reruns on the revised model

Once steps 02 to 06 are merged. Every graph v1 result moves to `thesis-progress/results/archive/graph_v1/`
first (step 01). Run each step on its own, with the commands in each `results/<appendix>/README.md`, not
through `bedtime.bash`.

## Order

1. **Pilot, 8 agents.** Token Passing, fixed, demand and random storage, 20 seeds. Does demand now beat random
   on picks, and does travel per pick drop? If random still wins, that is a finding about Token Passing, not
   the graph. Read it with the author before going on.
2. **Welch.** Long traces at each fleet under fixed storage, to set the warm-up and the measuring window
   (step 06). Check that fixed storage settles at the candidate load.
3. **Load sweep** (`E_load/`), each fleet's capacity and main load, measured over the window.
4. **Storage values** (`G_storage/`). Random storage against demand at every fleet (D17). Δ and β to confirm the reasons of step 07. The refill size Q at a
   few values (step 05), and the slot capacity (one refill of the bulkiest SKU, fixed storage fits).
5. **Demand robustness** (`F_demand/`).
6. **Ma et al. reproduction** (step 08), any time after the grid loader.
7. **Training** (`J_training/`), with `--gpu` (step 10) and the checkpoint choice of `[A60]` built (M5 of
   `../measures_plan.md`).

## Before step 1

- The configs' arrival rates. Fleet 16 says 0.15 and fleet 64 says 0.42, while graph v1's sweep found 0.12
  and 0.3. The reruns set new main loads anyway, so change them in step 3.
- Update `thesis-progress/RUNS.md`.
