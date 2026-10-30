# E. Load and capacity

**Answers.** The capacity of each fleet under fixed storage, the highest rate at which every seed keeps up
with order work and put-aways, every lower rate too, and the main load, 0.6 of it.
**Fills.** `app:load:first` and `tab:app:firstsweep` of Appendix E. The main loads are used by every run in
F and G. `tab:app:capacity` waits for the next run.
**Settings file.** `configs/step12/fleet_<m>.yaml`. Setup in `../README.md`.

| fleet | capacity | first failing | main load |
|---|---|---|---|
| 8 | 0.175 | 0.2 | 0.105 |
| 16 | 0.25 | 0.3 | 0.15 |
| 32 | 0.3 | 0.4 | 0.18 |
| 64 | 0.4 | 0.6 | 0.24 |

## Commands, per fleet m

1. The grid, rates per agent 0.0125 to 0.1, stopping at the first rate no seed keeps up at:

       $PY scripts/sweep/load_sweep.py --config configs/step12/fleet_$m.yaml --seeds 20 \
           --stop-when-overloaded --workers 8 --horizon 10000 --warmup 5000 \
           --out $R/E_load/fleet_$m \
           --rates-per-agent 0.0125 0.025 0.0375 0.05 0.0625 0.075 0.0875 0.1

2. Finer rates between the last passing and the first failing rate, the same command with `--rates` in
   place of `--rates-per-agent`:

   | fleet | `--rates` |
   |---|---|
   | 8 | `0.125 0.15 0.175` |
   | 16 | `0.25 0.3 0.35` |
   | 32 | `0.1 0.2 0.3` |
   | 64 | `0.2 0.4 0.6` (run twice, the first stopped when a worker ran out of memory) |

3. The main load is `by_mode.fixed.main_load` in `fleet_<m>/capacity.json`.

## Findings

- **The main loads are safe.** At every main load all 20 seeds keep up with order work and put-aways,
  and the backlog stays flat (growth per 100 steps -0.03, 0.03, 0.06 and -0.07).
- **Capacity per agent falls as the fleet grows**, from 0.022 at 8 agents to 0.006 at 64. The warehouse
  grows with the fleet, so trips get longer (longest trip 36 to 82 steps).
- **The keep-up check passes overloaded rates.** At each capacity the backlog still grows by 1 to 2 tasks
  per 100 steps and a pick takes 2 to 5 times as long as at the lowest rate. That is why the main load sits
  at 0.6 of the capacity.
- **Fleets 32 and 64 are coarse.** Their capacities are known to within 0.1 and 0.2 only. The error can
  only make the main load lower than it could be.
- **Orders wait for stock more as the load rises**, at 8 agents from 2.8 % of orders at 0.1 to 5.1 % at
  capacity, at 64 agents from 5.4 % to 15 %.
- **Two counting errors in the code** (fixed in PR #199). The stored keep-up flag left finished shipments
  out, so it was too strict (fleet 8 at 0.175 said 7 of 20 seeds, the right count is 20). The capacities
  here were read with the right count. Four measures counted the warm-up (order completion, orders that
  waited, total service time, robots busy). None changes the capacities or the gains.
- **Against the old model** (graph v1) the capacities moved from 0.2, 0.2, 0.6 and 0.5 to 0.175, 0.25, 0.3
  and 0.4. Not like for like: the old runs had 2000 steps and no warm-up, and step 12 adds shipping.

## Completeness

Every fleet has a `capacity.json` with a main load, and every sensitivity sweep has all its rows (3600).
One worker was killed by the kernel's out-of-memory killer at 27/10 16:07, which stopped pass 1 of the
finer rates for fleet 64 (`BrokenProcessPool` in the sweep log of fleet 64, not kept). Pass 2 ran the
same rates and filled every seed.

## What reruns once the open points are settled

The full sweep (`bedtime.bash step12`) on the final configs, after the step 12 settings move into
`configs/fleet_<m>/` as part D says, with Q = 12, the SKU counts above, 5 lines per order
(`lines_per_order: {distribution: shifted_poisson, mean: 5}`), the class-based homes of
`b44db09`, the evaluator fixes if agreed, and fewer workers for fleet 64. About 27 hours at this run's
speed. Before it, the open question of the random workstation (`model_revision/README.md`, "Still open")
changes how demand is spread, and so possibly the sizing.
