# What each number of a run is for

Started 2026-10-23, grouping agreed with the author the same day. A run writes about 50 numbers, and it got hard to tell which ones matter. Here every number has one question it answers. A number with no question is dropped. The thesis decides the roles (`sec:pf:measures`, `tab:measures` in `2.Introduction.tex`, and `app:measures` in `Appendices/C.ModelDetails.tex`). Where this note and the thesis differ, the thesis wins. The code is `evaluation/metrics.py` in `slap-mapd-coupling`, and the changes it needs are in `../decisions/active/measures_plan.md`.

## Decisions of 2026-10-23

1. **Overflow and unplaced units** go in the load and capacity appendix (`E.Load.tex`), plotted against the load. The main text mentions them only if a learned arm cannot keep up.
2. **The keep-up check is applied to picks and put-aways separately** (`[A59]`). The combined check let demand storage pass at 32 agents with a third of its put-aways unfinished.
3. **The missing numbers are added**, each with its reason, below.
4. **A timing log per part of the step** is added, kept apart from the measures.
5. **A checkpoint is chosen on validation seeds** by pick service time among those that keep up (`[A60]`), not by training return.

## How a run is read, in order

1. **Check.** May this run's service time be compared at all?
2. **Result.** How long does an order line take, from release to delivery?
3. **Why.** Which part of that time changed?
4. **Cost.** What does the result cost?
5. **Customer.** What does the customer see?

Then, only when a result needs explaining, the diagnostics. The validity numbers are checked last, so a problem with them is not missed.

## 1. Check

| number | why it is measured | thesis |
|---|---|---|
| `keeps_up` | The answer. Picks and put-aways must each finish at least `f_up` (0.8) of what was released | `eq:throughput`, `[A59]` |
| `keeps_up_picks`, `keeps_up_putaways` (new) | Shows which kind failed, so a starved put-away queue is visible | `[A59]` |
| `throughput` | What is reported instead of service time when a run does not keep up | $\Lambda_T$ |
| `completed_share` | How close the run came to the line, so 0.79 and 0.30 do not look the same | none |
| `backlog` | How much work was left at the end | $B_T$ |
| `backlog_slope` (new) | Whether the backlog was still growing over the second half. Passing the check at one horizon does not prove the backlog stays bounded | `[A55]` |
| `stalled` | Whether a robot jammed and the fleet caught up. Such a run passes the check while its service time carries the jam | stall, `app:checks` |
| `longest_stand_still` | The raw length of the worst jam, used to choose the stall length, which is TBD | none |

## 2. Result

| number | why it is measured | thesis |
|---|---|---|
| `mean_service_time` | The result. The mean time from an order line's release to its delivery, over picks | $\bar\zeta_T$, `eq:meanservice` |
| `throughput_per_agent` (new) | RQ4. Whether each robot finishes less as the fleet grows | $\Lambda_T/m$, `[A33]` |

The main result, the gain of demand over fixed storage, is computed across paired runs (`eq:rqformal`, `eq:relgain`) and is not a field of a row.

## 3. Why

| number | why it is measured | thesis |
|---|---|---|
| `mean_wait_for_agent` | The part before a robot is assigned. Grows when the fleet is too small for the load | `eq:split` |
| `mean_travel_time` | The part a robot moves. Where storage should show | `eq:split` |
| `mean_blocked_time` | The part a robot stands still. Where congestion shows | $W_T$, `eq:waiting` |
| `mean_stock_wait` | The part of the wait spent waiting for stock. Shows when stock ran out | `[A39]` |
| `mean_crowding` | How packed the robots were. Read with blocked time, since crowding that blocks nobody costs nothing | $\bar\delta_T$, `eq:crowding` |
| `robot_busy_share` (new) | The share of robot-steps spent on a task. If the wait for a robot is long while robots stand idle, the cause is the task rule, not the fleet size | none |
| `mean_shelf_taken_wait` (new) | How long a waiting task was held back because another robot's path ended at its shelf. This is the Token Passing rule suspected at 64 agents. Token Passing only | none |

## 4. Cost

| number | why it is measured | thesis |
|---|---|---|
| `mean_putaway_service_time` | What adaptive storage costs in robot time. A rule that puts stock near delivery can lengthen the put-aways | `app:measures` |
| `mean_decision_runtime_seconds` | What deciding costs the controller | $\kappa_T$, `eq:runtime` |

## 5. Customer

| number | why it is measured | thesis |
|---|---|---|
| `mean_order_completion` | How long a whole order takes. A customer waits for the last line, not the mean line | `eq:ordercompletion` |
| `orders_per_timestep` (new) | Throughput counts tasks, and a rule that splits lines over shelves finishes more tasks without serving more customers | `[A56]` |
| `num_completed_orders` | Input to the line above | `[A56]` |

## Diagnostics, by question

| question | numbers |
|---|---|
| Are the put-aways keeping up? | `num_released_putaways`, `num_completed_putaways` |
| How spread out is the stock? | `mean_split_skus`, `mean_tasks_per_line` |
| Does old stock hold the best shelves? (what "stored stock never moves" costs) | `mean_cold_prime_share`, `mean_unit_age_at_pick` |
| What is the backlog made of? | `num_waiting_tasks`, `num_active_tasks`, `num_waiting_orders`, `num_lines_waited` |
| How much stock arrives? | `num_storage_updates`, `mean_arrived_units` |

## Validity

| number | why it is measured | where it is reported |
|---|---|---|
| `overflow_units` | Fixed storage put stock off its home shelf because the shelf was full, so "fixed" was not quite fixed | load and demand appendix |
| `unplaced_units` | Arriving stock fitted on no shelf | load and demand appendix |

Both are 0 at every main load measured so far. They appear above capacity under fixed storage: overflow at 16 agents from load 0.3 and at 32 and 64 agents from 0.6, unplaced at 8 and 16 agents from 0.3. An evaluation at a main load warns when either is above 0.

## Dropped

| number | why it goes |
|---|---|
| `keep_up_ratio` | Throughput over the expected rate. The thesis dropped this test (`[A49]`), and it counts put-aways in the throughput but not in the rate, so a healthy 8-agent run reads 1.7 |
| `mean_relocated_units`, `mean_relocation_distance` | From the model where stock was moved for free. Stock on a shelf never moves now (`2.Introduction.tex`, lines 431 and 1351), so both are always 0. Moving stored stock by robots would be a model extension, future work |
| `total_service_time` and its three parts, `total_service_time_finished` | No thesis claim uses them since `[A50]`. The `metrics.py` docstring still calls total service time "the result", which is drift for #103 |

## Timing log, apart from the measures

**Why.** The field-of-view calculation once made a 64-agent episode 16 times slower, and nothing showed where the time went. One record per episode, in its own file, gives the total seconds and the number of calls of each part. A part taking most of the step then shows at once.

The parts follow the six stages of the step in the method section (`4.Implementation.tex`, lines 30 to 45), with stage 3 split in two:

1. order release and task creation
2. assignment
3. routing, as (a) building the observations (field of view, window tables) and (b) the policy's forward pass
4. conflict resolution
5. applying the moves, the task lifecycle and the log
6. storage update and put-aways

They are followed by the parts outside the stages: the crowding measure, the reward, and the measures at the end of a run. In training, RLlib's own timers for sampling, the update and the weight sync are added.

`mean_decision_runtime_seconds` stays a measure, because the thesis reports it as a cost. The timing log is for engineering only.

## What each phase records

| phase | its purpose | what it records |
|---|---|---|
| **Training**, every iteration | Is it learning, and is it healthy? | the return split into its reward terms (shaping, delivery, override, wait, move, crowding), since the shaping term dominates the total. Episode length, completed tasks, environment steps so far. PPO health: policy loss, value loss, entropy, KL or clip fraction. The timing log |
| **Validation**, every saved checkpoint, on the validation seeds | Choose the checkpoint (`[A60]`), and draw the learning curve in thesis terms | `keeps_up` and its two parts, `mean_service_time`, `mean_putaway_service_time` |
| **Test**, once, 20 paired seeds | The thesis results | groups 1 to 5, the diagnostics and validity in a table of their own, the timing log |

The training curves come from validation, not from the training return.

## Storage pilot only (not in the thesis)

| number | why it is measured |
|---|---|
| `loaded_total`, `mean_loaded_pick`, `mean_loaded_putaway` | The pilot's training signal, the time robots carry stock. Not a thesis measure. The pilot is judged on groups 1 to 4 like any run |
| `mean_return`, `policy_loss`, `value_loss`, `entropy`, `clip_fraction` | Training health. Entropy near 0 means the policy stopped exploring |
| `choices`, `episodes_played`, `seconds`, `play_seconds` | Bookkeeping, replaced by the timing log |

Judged on the thesis numbers, the night run of 2026-10-22 reads as follows (`../decisions/ideas/learned_storage_pilot_plan.md`).

| stage | rule | keeps up | pick service (result) | put-away service (cost) |
|---|---|---|---|---|
| 8 agents | fixed | 20 / 20 | 44.4 | 68.3 |
| 8 agents | demand | 20 / 20 | 24.7 | 130.5 |
| 8 agents | learned | 20 / 20 | 21.9 | 72.7 |
| 64 agents | fixed | 20 / 20 | 150.2 | 68.4 |
| 64 agents | learned | 0 / 20 | none | none |

These use the old combined check. Under `[A59]` they are read again.

## Still open

- The thesis says on line 433 of `2.Introduction.tex` that an update costs "the distance the arriving stock travels". `tab:measures` and the code use the put-away service time. The sentence should follow `tab:measures`.
- The stall length (`tab:evalparams`), to be suggested from `longest_stand_still` in the Token Passing sweeps.
