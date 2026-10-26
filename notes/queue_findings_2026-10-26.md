# What the queue of 2026-10-23 found, and where it goes

Read on 2026-10-26. The queue is `~/thesis_runs/queue_2026-10-23_2344`. Every job finished. `train32` was stopped by a TERM during the matched run and finished from its checkpoint in `~/thesis_runs/queue_2026-10-25_1902` (25/10, 23:36). All numbers are Token Passing at each fleet's main load, T = 2000, 20 seeds, paired by seed, unless a line says otherwise. The gain is pick service time of demand over fixed, as a share of fixed. Nothing in `thesis/` has been changed.

## 1. Main loads (sweep)

| fleet | capacity | first failing | main load | per agent | longest stand-still in passing runs |
|---|---|---|---|---|---|
| 8 | 0.2 | 0.225 | 0.12 | 0.015 | 14 to 16 |
| 16 | 0.2 | 0.25 | 0.12 | 0.0075 | 47 to 55 |
| 32 | 0.6 | 0.7 | 0.36 | 0.011 | 36 to 46 |
| 64 | 0.5 | 0.6 | 0.3 | 0.0047 | 87 to 109 |

- Past the capacity only picks fail. Put-aways keep up at every rate under fixed storage.
- Fleet 64 dropped from 0.42 to 0.3, fleet 16 from 0.15 to 0.12. `configs/fleet_64/*.yaml` (0.42) and `configs/fleet_16/*.yaml` (0.15) are out of date. Training used the right rates, because `bedtime.bash` passes `--arrival-rate`. The storage pilot's 64-agent stage ran at the old 0.42.
- Capacity per agent does not grow or shrink smoothly with the fleet. 16 and 64 agents sustain half of what 8 and 32 do. Cause not checked.
- Fleet 16's sweep starts at 0.2, so its capacity is "the lowest rate tested passes". Its 0.3 to 0.6 rows are 50-seed rows from before `[A59]`.
- Overflow and unplaced units are 0 at every main load. Fixed storage overflows at its own capacity at 8 agents (14.5 units at 0.2) and at 32 agents (73 units at 0.6).

## 2. Why tasks wait: the endpoint rule, now measured

The open question of 2026-10-22 ("about half the fleet is busy while hundreds of tasks wait") is answered by the new fields.

- `robot_busy_share` is 0.25 to 0.40 at every fleet and rule. Robots stand idle while tasks wait.
- Most of a pick's wait for a robot is time the task is held because another robot's path ends at its shelf or delivery vertex. At 64 agents under fixed storage the wait for a robot is 56 steps, with 45 of them counted as shelf taken. The two counts overlap, so they are not added.
- Demand put-aways at 64 agents wait 466 of 484 steps for a taken shelf, against 24 under fixed. At 32 agents it is 194 of 209. The wait for a taken receiving vertex is 0 everywhere.
- Travel per pick is the same or a little longer under demand (8 agents 12.6 against 11.7, 32 agents 22.7 against 19.9). The whole pick gain is in waiting.

So under Token Passing, what a storage rule changes is mostly how many tasks aim at the same shelf, not how far robots drive.

## 3. Random storage (pilot)

`~/thesis_runs/pilot/2026-10-24_1021`, 20 test seeds.

| fleet | rule | keeps up | pick | put-away |
|---|---|---|---|---|
| 8 | fixed | 20 | 44.4 | 68.3 |
| 8 | demand | 19 | 24.7 | 130.5 |
| 8 | random | 20 | 24.8 | 34.8 |
| 8 | learned | 20 | 25.5 | 32.9 |
| 64 (load 0.42) | fixed | 20 | 150.2 | 68.4 |
| 64 (load 0.42) | demand | 0 | 167.3 | 530.7 |
| 64 (load 0.42) | random | 20 | 99.2 | 56.2 |
| 64 (load 0.42) | learned | 20 | 113.4 | 51.4 |

- Random storage gives the whole pick gain of demand storage at 8 agents, at a quarter of its put-away time, and beats fixed by a third at 64 agents.
- The learned rule learns to behave like random, close on picks and slightly better on put-aways. At 64 agents it was stopped at 4 hours (83 iterations) and is behind random on picks.
- This fits section 2. Spreading a product over many shelves is what helps under Token Passing.
- **For the main text, not an appendix.** The main result compares demand with fixed. Without random as a reference, a reader cannot tell a gain from placing popular stock near delivery from a gain from spreading stock. To discuss.

## 4. Parameter sweep (sensitivity)

| fleet | gain | picks keep up | put-aways keep up | put-away time, demand over fixed |
|---|---|---|---|---|
| 8 | 44 % | 20 | 20 | 2.0 |
| 16 | 1 % | 20 | 20 | 3.1 |
| 32 | 44 % | 20 | 0 | 2.5 |
| 64 | −12 % | 20 | 0 | 8.1 |

- **Stock margin ε.** Flat. Gain and put-away cost hardly move from 0.25 to 2.0 at any fleet. At 64 agents 2.0 brings the gain to −2 %, still 1 of 20 put-aways keeping up.
- **Congestion weight β.** At 8 agents every value gives the very same episodes as β = 0. At 32 agents nothing changes either. At 16 agents any β from 0.5 up gives the same small help (gain 1 % to 6 %, put-away cost 3.1 to 2.6). At 64 agents it lowers the put-away time (484 to 383 at β = 4) but keeps up on 1 of 20 at most. A first answer to RQ3 under Token Passing: the congestion rule adds almost nothing, because blocking is 2 to 4 % of a pick.
- **Period Δ.** The trade-off of 2026-10-23 holds. The gain falls with Δ (8 agents 49 % at 50 to 29 % at 400, 32 agents 47 % to 12 %). Δ = 400 is the only value at which demand's put-aways keep up at 64 agents (20 of 20, gain −4 %) and the best at 32 (12 of 20). Δ = 200 now gives 9 of 20 at 64 agents, not the pass the archive showed at load 0.42.
- **Demand settings (robustness, `[A34]` values).** 8 agents keeps a gain from 21 % to 53 % over every value, and 32 agents from 31 % to 48 % (picks only, put-aways fail). 16 agents swings from −40 % (shift 2) to +15 % (period 100). 64 agents swings from −30 % to +10 %.

## 5. Shelf capacity (shelfcap)

- Fixed storage fits with no overflow at every capacity tested, apart from 160 at 32 agents (2.4 units). The smallest capacity it fits in is 260, 170, 200 and 140 for 8, 16, 32 and 64 agents. This is the reason the handover proposed. Today's configs (300 and 200) pass.
- Under fixed storage the capacity changes nothing at all. The episodes are identical at every value.
- Under demand storage the capacity is a lever, and its direction depends on the fleet.
  - 8 agents. A larger capacity helps a lot. At 400 the put-away cost disappears (0.92 of fixed) and the gain is 50 %. At 260 the gain is 33 %. Cause not checked, since peak fill is 1.00 at both.
  - 16 agents. A larger capacity raises the put-away cost (2.6 to 4.1) with no pick gain.
  - 32 and 64 agents. A larger capacity is worse. At 64 agents, 140 gives a gain of 2 % with 6 of 20 put-aways keeping up, while 400 gives −10 % and 0 of 20.
- So the capacity is not neutral for the comparison. It has to be fixed by a reason that does not look at demand's result, which the "smallest that fixed fits in" rule gives.

## 6. Horizon

**The gain has not settled by T = 2000, and at 16 and 64 agents its sign depends on T.**

| fleet | 1000 | 1500 | 2000 | 3000 | 4000 |
|---|---|---|---|---|---|
| 8 | 27 % | 37 % | 44 % | 38 % | 47 % |
| 16 | −21 % | −10 % | 1 % | 23 % | 32 % |
| 32 | 42 % | 48 % | 44 % | 37 % | 36 % |
| 64 | 3 % | −2 % | −12 % | −10 % | 6 % |

The standard error over seeds is 1 to 5 points, so these moves are real.

- Fixed storage does not reach a steady state either. Its pick service time keeps rising with T (32 agents 70 at 1000 to 119 at 4000, 64 agents 84 to 144), and the backlog in the 4000-step traces is still rising at 32 and 64 agents.
- At 64 agents demand's put-aways fail at every T up to 3000 and pass on 20 of 20 at 4000, with the backlog falling over the second half (slope −4.2). Its put-away failure at T = 2000 may be a long start-up, not a lasting overload.
- At 16 agents demand is worse than fixed early and better late.
- Every other value in this note was measured at T = 2000. If T changes, the capacity, the main loads and the storage values may change with it.
- Cause not checked. A guess to test is that fixed storage, set from the starting demand, falls behind as demand drifts, while stock keeps arriving at the same shelves.

## 7. Stall length

The longest stand-still in passing runs grows with the fleet and the instance: 16 at 8 agents, 55 at 16, 46 at 32 and 109 at 64. One value for every fleet would have to be above 110. One per fleet could be about twice each fleet's value.

## 8. Training (decentralised arm, 500 000 steps)

| fleet | regime | iterations | tasks done of released, last iteration | best | seconds per iteration, learner share |
|---|---|---|---|---|---|
| 8 | fixed_only | 42 | 416 of 433 (96 %) | 420 | 170, 91 % |
| 8 | matched | 42 | 426 of 440 (97 %) | 430 | 168, 95 % |
| 16 | fixed_only | 42 | 355 of 433 (82 %) | 388 | 366, 92 % |
| 16 | matched | 42 | 352 of 436 (81 %) | 371 | 369, 92 % |
| 32 | fixed_only | 63 | 938 of 1096 (86 %) | 1081 | 542, 87 % |
| 32 | matched | 63 | 950 of 1162 (82 %) | 1030 | 531, 87 % |

- 8 agents learns smoothly and levels off near the end. 16 and 32 agents learn, but the return falls back mid-run (16 agents to half at iteration 22, 32 matched at iteration 32), and they end near the keep-up line of 0.8. 500 000 steps look short for 16 and 32 agents. This is read from training episodes, not validation, so it is a hint, not a result.
- No checkpoint has been chosen by `[A60]`. M5 (`measures_plan.md`) is not built, and `evaluate_run.py` still chooses by most tasks completed.
- `progress.jsonl` has the reward terms and the timers but no `policy_loss`, `value_loss`, `entropy` or `kl`. `fig:app:traininghealth` cannot be drawn from these runs.
- Only the decentralised arm was trained. The centralised and section-based rows of `tab:app:checkpoint` stay open.

## Where each finding goes

| appendix | placeholder | fill now? | needs first |
|---|---|---|---|
| E | `tab:app:capacity`, `fig:app:loadsweep`, Summary, Conclusion | yes, section 1 | your decision on T (section 6), since every row is at T = 2000 |
| E | `app:load:validity` | yes, 0 at every main load | |
| E | `app:cal:load`, B's `λ_task` row | replace the pilot loads 0.15 to 0.4 with the four main loads, *tested* | |
| F | `fig:app:demandsweep`, Summary, Conclusion | yes, section 4 | |
| G | `app:cal:margin` | yes, flat, keep 1.0 | |
| G | `app:cal:beta` | yes, section 4 | which β to keep, given it does nothing at 8 and 32 |
| G | `app:cal:period` | figure yes | your choice of Δ (gain against keeping up) |
| G | `tab:app:shelfcap` | change from *derived* to *tested*, columns change | agree the rule "smallest capacity fixed fits in" |
| H | `fig:app:horizontrace`, `fig:app:horizongain`, `tab:app:horizon` | figures yes | the decision in section 6. `[A61]` set T ≥ 2000. A change is an `[Axx]` tag |
| H | `app:cal:stall`, `fig:app:standstill`, B's stall row | yes | one value or one per fleet |
| I | `fig:app:rewardterms` | yes, from the `return_*` fields | the figure script reads `results/training/`, check it reads these files |
| I | `tab:app:window` | yes, no run needed (breadth-first count over the instances) | |
| J | `app:cal:budget` | a sentence that 500 000 looks short at 16 and 32 | M5, then validation curves |
| J | `fig:app:traininghealth` | no | PPO statistics in the progress log |
| J | `tab:app:checkpoint` | no | M5 |
| K | `fig:app:timing` | yes, `timing.jsonl` in every Token Passing folder, plus `seconds_*` and `timer_*` in training | adapt the script's reader to these paths |
| L | Token Passing rows of `tab:app:check`, `tab:app:result`, `tab:app:cost`, `tab:app:backlog` | yes, the default points of the parameter sweep | T |
| none | random storage, the endpoint rule | main text | section 3 |

## Decisions for the author, in order

1. **The horizon.** Run longer (for example 4000 or more, or until fixed storage settles) and redo the sweep, or keep 2000 and report the gain as horizon-dependent. This comes first because it decides whether the other values stand.
2. **Random storage as a reference rule** in the main comparison, and how the thesis explains that the gain under Token Passing comes from spreading stock.
3. Δ, β and ε. ε is flat. β does nothing at 8 and 32 agents. Δ trades gain against demand keeping up.
4. The shelf capacity rule.
5. The stall length, one value or per fleet.
6. The training budget at 16 and 32 agents, after M5.
7. Configs: fleet 16 to 0.12 and fleet 64 to 0.3. Rerun the 64-agent pilot stage at 0.3 if the pilot stays.
