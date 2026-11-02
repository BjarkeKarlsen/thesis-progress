# E. Load and capacity

**Answers.** The capacity of each fleet under fixed storage, the highest rate at which every seed keeps up
with order work and put-aways, every lower rate too, and the main load, 0.6 of it.
**Fills.** `tab:app:capacity` and `app:load:next` of Appendix E. The main loads are used by every run in
F and G. `tab:app:firstsweep` keeps the first sweep (rows in git history at `524ef5a`).
**Settings file.** `configs/step12/fleet_<m>.yaml`. Setup in `../README.md`.

| fleet | capacity | first failing | main load | main load per agent |
|---|---|---|---|---|
| 8 | 0.15 | 0.175 | 0.09 | 0.011 |
| 16 | 0.3 | 0.35 | 0.18 | 0.011 |
| 32 | 0.5 | 0.6 | 0.3 | 0.009 |
| 64 | 1.0 | 1.2 | 0.6 | 0.009 |

## Commands, per fleet m

What `scripts/sweep/overnight.bash` ran:

1. The grid, rates per agent 0.0125 to 0.1, stopping at the first rate no seed keeps up at:

       $PY scripts/sweep/load_sweep.py --config configs/step12/fleet_$m.yaml --seeds 20 \
           --stop-when-overloaded --workers 8 --horizon 10000 --warmup 5000 \
           --out $R/E_load/fleet_$m \
           --rates-per-agent 0.0125 0.025 0.0375 0.05 0.0625 0.075 0.0875 0.1

2. Finer rates between the last passing and the first failing rate, the same command with `--rates` in
   place of `--rates-per-agent`. Pass 1 ran the rates below. Pass 2 found nothing left to refine.

   | fleet | `--rates` |
   |---|---|
   | 8 | `0.125 0.15 0.175` |
   | 16 | `0.25 0.3 0.35` |
   | 32 | `0.5 0.6 0.7` |
   | 64 | `1 1.2 1.4` (6 workers) |

3. The main load is `by_mode.fixed.main_load` in `fleet_<m>/capacity.json`.

The main loads lie below the lowest grid rate, so the rows at the main load are in F and G (the thesis
values of each sensitivity sweep, for example `../F_demand/fleet_<m>/demand.skew` at skew 1).

## Findings

- **The main loads are safe.** At every main load all 20 seeds keep up with order work and put-aways
  under fixed and demand storage. The backlog falls slightly (growth per 100 steps under fixed storage
  -0.03, -0.05, -0.25 and -1.0 at 8, 16, 32 and 64 agents).
- **Capacity now grows with the fleet.** The warehouse grows by the same amount per agent, so capacity
  per agent stays near 0.019 (0.016 at 32 agents). In the first sweep it fell from 0.022 to 0.006.
- **Picks wait for the workstation, not for travel.** This is the issue the run found. At the main load
  a pick drives 17 to 25 steps but waits 67 to 156 steps before a robot takes it. Over 80 % of its
  service time a robot's path already ends at its workstation (`mean_pick_wait_delivery_taken`, 74, 79,
  83 and 84 % of the pick service time at 8, 16, 32 and 64 agents). Meanwhile the robots hold a task only
  30 to 56 % of the time. Token Passing gives a task only to a robot whose path does not end where
  another path ends, and all 5 lines of an order go to the same workstation, so they go one at a time.
- **Against the first sweep.** There each order went to any workstation and had one line, and the wait
  for the workstation was 36 to 45 % of a pick. With sections of 4 workstations, 5 lines per order and
  fewer workstations per SKU, the same rule now dominates the pick. So the main loads are low, and the
  pick service time is mostly this wait. The idling is Token Passing's rule as published, kept as a
  limitation (author, 2026-11-02, step 4). No extra entry points per workstation.
- **Fixed storage overflows more.** It puts 146, 338, 705 and 1740 units per run off their home shelf at
  the main loads (99 to 238 in the first sweep). No unit is left unplaced.
