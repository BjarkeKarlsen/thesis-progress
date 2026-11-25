# Step time test from main, 8 to 128 agents

Mean runtime kappa_T (eq:runtime: assignment and routing together, as Ma et al. 2017) of every
controller as the fleet grows. Fills the scaling part of Appendix L (`app:results:scaling`,
`tab:app:scaling`) and `fig:exp:time` in the Experiments chapter. Figure script:
`thesis-progress/scripts/images/scaling_steptime.py`. Replaces `../step_time/` (older code, before
the speed-up PRs #213 to #215, Token Passing from the load sweep).

## What ran

- **Code.** main `bdfda94` (`~/worktrees/main-bdfda94`), 24 November 2026, 12:47 to 14:38 on the PC.
  `steptime_main.sh`, `timing_probe.py`, `resources.py`, `measure_cmd.py` here are the copies that ran.
- **Learned.** The long congestion-aware 16-agent policy of each controller at its chosen checkpoint
  ([A111]), the same checkpoints as the performance test, in the warehouse of 8, 16, 32, 64 and 128
  agents at that fleet's main load (0.09, 0.18, 0.3, 0.6, 1.2). Section-based: 2 sections at 8, 3m/16
  up to 64, 16 at 128 (one per aisle). Seed 200000, 3000 steps, timed over the last 1000
  (`window_decision_runtime_seconds`). Network on the GPU (RTX 2070 SUPER), one CPU thread.
- **Token Passing.** Same seed, warehouse, load and congestion-aware storage, on the CPU, one thread,
  played for 2000 and for 3000 steps. kappa over the last 1000 steps = (assignment + routing at 3000
  minus at 2000) / 1000, from `token_passing/tp_<m>_<T>/timing.jsonl`. The same two timers the
  evaluator sums for kappa_T (`evaluator.py`, total_runtime).
- **Quiet PC.** Before each episode the script waits for no game and load under 2.5. PC load during
  the rows 1.3 to 2.1. Each row records RAM, CPU, GPU use and other GPU programs (`res_*`).

## Five seeds (2026-11-24, what the thesis uses)

`steptime_seeds.sh` added seeds 200001 to 200004 for every controller and fleet (`seeds/`), and
`steptime_section_seeds.sh` section-based seeds 200001 and 200002 at 32 and 64 (`section_seeds/`).
Token Passing: `seeds/tp_<m>_<T>/timing.jsonl`, one row per seed 200000 to 200004. 86 runs exit 0,
PC load 1.3 to 2.3. `fig:exp:time` and `tab:app:scaling` give the mean over the five seeds with the
lowest and highest seed. kappa in ms, mean [min, max]:

| agents | decentralised | with messages | section-based | centralised | Token Passing |
|---|---|---|---|---|---|
| 8 | 3.5 [3.2, 3.6] | 4.6 [4.5, 4.8] | 15.6 [14.8, 16.9] | 19.8 [19.5, 20.3] | 0.31 [0.23, 0.35] |
| 16 | 4.7 [4.5, 4.9] | 5.7 [5.5, 6.1] | 33.7 [23.5, 38.9] | 43.7 [41.8, 45.5] | 0.78 [0.69, 0.86] |
| 32 | 7.0 [7.0, 7.1] | 8.8 [8.6, 8.9] | 52.8 [36.7, 66.0] | 96.7 [90.2, 108] | 2.4 [2.2, 2.7] |
| 64 | 11.5 [10.9, 11.9] | 16.0 [15.8, 16.3] | 68.6 [57.7, 86.7] | 223 [217, 238] | 11.7 [11.0, 12.6] |
| 128 | 21.2 [21.0, 21.5] | 35.6 [35.3, 36.0] | 149 [128, 175] | 496 [469, 507] | 78.0 [69.6, 91.6] |

## Result on seed 200000 alone, kappa in ms over steps 2000 to 3000

| agents | decentralised | with messages | section-based | centralised | Token Passing |
|---|---|---|---|---|---|
| 8 | 3.2 | 4.5 | 15.5 | 19.5 | 0.28 |
| 16 | 4.5 | 5.5 | 23.5 | 41.8 | 0.72 |
| 32 | 7.1 | 8.6 | 63.3 | 90.2 | 2.8 |
| 64 | 10.9 | 15.8 | 59.6 | 217 | 12.1 |
| 128 | 21.1 | 35.5 | 155.7 | 469 | 69.5 |


## Notes

- Whole step time (`seconds_per_step`, learned; timed parts minus `assignment`, Token Passing) is
  higher, mostly the warehouse's own work: Token Passing 0.8, 1.8, 5.0, 17.4, 83 ms.
- Token Passing gets slower as the warehouse fills (0.43 ms whole step over the first 2000 steps,
  0.79 over the last 1000, at 8 agents). The learned arms stay level within the window (first/last
  100 steps in `logs/`).
- These runs measure time only. The served share of one seed over 1000 steps is not a result.
- Peak RAM: learned 1.2 to 1.45 GB, Token Passing 0.65 to 1.15 GB.
