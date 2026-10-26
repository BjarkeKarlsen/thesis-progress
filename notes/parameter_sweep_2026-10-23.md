# Parameter sweep, outcome (2026-10-23)

The Token Passing sensitivity sweep of 2026-10-22 is complete. It covers 4 fleets (8, 16, 32 and 64 agents) and 6 settings, with 20 seeds per point, each fleet at its main load. Rows are in `thesis-progress/results/parameter_sweep/fleet_<m>/<setting>/load_sweep.jsonl`. The figure is `thesis-progress/results/parameter_sweep/plots/sweep.png`, drawn by `thesis-progress/scripts/results/plot_parameter_sweep.py`.

## What the sweep is for

This was not written down in one place (`decisions/active/sweep.md` is empty). The plans give three uses.

1. **Choosing the storage values that the literature does not give.** These are the period Δ (`storage_rule.epoch_length`), the stock margin ε (`arrival.margin`) and the congestion weight β (`storage_rule.congestion_weight`). The rule is to look in the SLAP and dynamic SLAP literature first, and to choose by this sweep and say so where nothing fits (`thesis_plan.md` section 7).
2. **The cost graph.** It plots put-away distance against the service time gain over a sweep of the stock margin (`thesis_plan.md` section 5).
3. **A robustness check of the demand model.** Skew, rotation period and rotation shift are fixed by the thesis (`[A34]`), so their sweep only shows whether the result holds when they change (header of `scripts/sweep/parameter_sweep.bash`).

The sweep does not cover the main result itself. That needs the learned routers, and the long run (step 5 of `thesis_plan.md` section 10) produces it.

## What it found

The gain below is the main result's measure. It is how much demand storage shortens pick service time against fixed storage, paired by seed, as a share of fixed. Fixed storage keeps up on every seed at every point.

| fleet | gain at default values | keeps up (demand) | notes |
|---|---|---|---|
| 8 | 44 % | 20 / 20 everywhere | gain shrinks with a longer Δ (30 % at 400), weaker skew and slower or faster rotation |
| 16 | 2 % | 20 / 20 everywhere | 50 to 60 % *worse* at rotation period 400 or shift 2. The only fleet where β helps (+12 % from β 0.5 up) |
| 32 | 44 % | 20 / 20 everywhere | same shape as 8 agents, gain falls to 12 % at Δ 400 |
| 64 | −11 % | 0 / 20 | keeps up only with Δ ≥ 200, skew 1.5 or rotation period 100. β 4 brings 9 / 20 |

### By setting

- **Stock margin ε.** Hardly matters for the gain at any fleet. At 64 agents a larger margin helps demand keep up (15 / 20 at 2.0). The cost graph over ε would be nearly flat.
- **Period Δ.** The strongest lever. A longer Δ lowers the gain at 8 and 32 agents but is the only setting that lets demand keep up at 64 agents. Δ is also the arrival period, so fixed storage changes with it too.
- **Congestion weight β.** It changes nothing at 8 and 32 agents, where the congestion rule gives the same runs as demand. It helps at 16 agents and only partly at 64. Under Token Passing a robot is blocked for under 5 % of a pick, so the traffic the congestion rule reads is small. This is a first answer to RQ3 under Token Passing.
- **Demand settings.** 8 and 32 agents keep a clear gain over the whole range. 16 agents does not, and 64 agents loses at the default values.

### Pick service time alone hides a cost

Demand storage shortens picks by making put-aways wait. Means at the default values are below. "all" weights picks and put-aways by how many were completed.

| fleet | rule | pick | put-away | all | travel per pick | put-aways done |
|---|---|---|---|---|---|---|
| 8 | fixed | 45.4 | 68.8 | 55.3 | 11.7 | 170 / 183 |
| 8 | demand | 24.9 | 134.4 | 68.4 | 12.6 | 158 / 191 |
| 32 | fixed | 90.5 | 83.8 | 88.1 | 19.9 | 380 / 410 |
| 32 | demand | 50.0 | 208.6 | 97.9 | 22.7 | 301 / 450 |
| 64 | fixed | 144.6 | 67.9 | 116.7 | 45.6 | 420 / 451 |
| 64 | demand | 160.6 | 525.3 | 259.7 | 48.3 | 267 / 497 |

- With put-aways counted, demand is slower than fixed at every fleet size.
- Demand does not shorten the trip. Travel per pick is a little *longer* under demand. The whole pick gain is in waiting for a robot.
- In the storage pilot's test seeds, random storage is the fastest rule once put-aways count (29.1 at 8 agents and 84.1 at 64, against 54.5 and 120.4 for fixed). Random spreads each product over the most shelves.
- **Likely cause.** Token Passing hands out a task only if no other robot's path already ends at that task's pickup or delivery vertex (`planners/token_passing.py`, rule 1). Tasks aimed at the same shelf therefore queue one at a time. A rule that sends many put-aways to a few good shelves makes them queue there. This follows from the code rule but has not been measured directly.

### Load

- Each fleet's main load is 0.6 of the capacity of *fixed* storage. Demand storage's capacity was never measured. At 64 agents the main load (0.42) is above what demand can sustain.
- Fleet 16's load (0.15) was set by hand in `configs/fleet_16/decentralised.yaml`. Its load sweep found no capacity, because all 10 seeds kept up at 0.1 and only 34 of 50 at 0.3, with no rate tested in between. So 16 agents may not sit at the same point on its load curve as the other fleets, which may explain why it looks out of line.

## Open, for discussion

See the discussion of 2026-10-23. Nothing is decided yet.

1. Settled by the thesis (`[A50]`, see `measures_catalogue.md`). The result is pick service time and put-away service time is its reported cost. Open is only how to read a rule whose cost is as large as demand's at 32 and 64 agents.
2. Whether the main load should come from the lower of the two rules' capacities.
3. Fleet 16's load sweep, rerun with rates between 0.1 and 0.3.
4. Values for Δ, ε and β, once 1 and 2 are settled.

## Rerun of 2026-10-23, and what the archive still tells

The sweep was rerun with the check of `[A59]` and the new diagnostics. The 2026-10-22 results are in `results/archive_2026-10-22/`.

- **The old episodes are bit-identical to the new ones** on the same configuration, rate and seed (560 of 560 fleet-8 episodes). Every number in the archive stays valid. Only the new fields are missing.
- **The put-away check cannot be read off the old rows.** Their put-aways released and not completed include the arrival at T, which the backlog leaves out. At Δ = 400 that estimate passed 1 seed of 20, against 20 of 20 for the exact check. The sweep scripts therefore treat an old row's check as unknown.
- **Fleet 8 is complete under the new check.** Capacity 0.2, main load 0.12, the same as before, so its parameter sweep is the same episodes with the new fields.
- **Fleets 16, 32 and 64 stopped early.** The per-agent grid of `[A58]` is too high for large fleets: at 64 agents its lowest rate, 0.8, already fails. And at high rates the starting stock outgrew the shelves, which crashed the sweep before `capacity.json` was written. Both are fixed. The sweep skips a rate whose stock does not fit, stops at a rate no seed keeps up at, and refines twice around the capacity. The bedtime script (`~/Documents/thesis/bedtime.bash`) adds the rates where the archive put each capacity.
