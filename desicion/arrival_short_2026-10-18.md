# Arrival model on the short run policies, 2026-10-18

What the evaluation of the short run's policies under the arrival stock model measured. Run
folder: `~/thesis_runs/arrival_short_2026-10-18/` (`run_arrival_short.sh`, `STATUS.md`,
`run.log`, `summary.md`, `runs/`, `logs/`). Code `slap-mapd-coupling` `e11ade2` (PR G to J),
exported to `code/`. Nothing was trained. The analysis used throwaway scripts on the raw rows,
and no episode was rerun. Related: `arrival_storage_plan.md` (the model),
`arrival_probe_2026-10-18.md` (Token Passing probe), `short_run_2026-10-18.md` (the same
policies under the relocation model).

## Setup

- The four policies of the short run of 2026-10-17 (decentralised, centralised, section with 3
  zones, full view), each trained 10 iterations under fixed storage at load 0.6, training seed
  0. Used as trained.
- Arrival model as in the probe. `demand_sized_blocks` starting stock, arrival period Δ 100,
  margin 1, receiving at the delivery vertices, congestion rule at β 1. The stock is sized at
  the load played.
- Checkpoint chosen on 2 validation seeds at load 0.6 under fixed storage. The chosen and the
  last checkpoint then played test seeds 200 000 to 200 005 under fixed, demand and congestion
  storage at loads 0.6, 0.3 and 0.2. Token Passing on the same seeds, rules and loads.
- Mean ± standard deviation over the 6 test seeds. Gains are paired seed by seed. "6/6" counts
  the seeds where the paired difference has the stated sign. 95% intervals use the t
  distribution with 5 degrees of freedom. A service time gain is given only where both runs
  of every pair keep up (throughput at least 80% of the arrival rate).

## How to read the numbers

Read the note in this order. The soundness checks first (if they pass, the numbers can be
trusted), then the tables under "Measured" (the facts), then "Inferred, not measured" (the
interpretation, open to disagreement), then the decisions at the end.

For a gain, look at three things. The mean says whether adaptive storage helps (positive in
the gain tables). The 95% interval in brackets says whether the gain is clear, which it is
when the whole interval lies above zero. The count "6/6" says how many seeds point the same
way, 6/6 being best and 3/6 a coin flip.

- Clear: centralised at load 0.3, fixed 75.4, demand gain 48.9 [28.8, 69.0], 6/6. Demand
  storage cuts mean service time from about 75 to about 27 steps, on every seed.
- No reading: decentralised at load 0.2, gain −36.7 ± 102.9 [−144.8, 71.3], 4/6. One jammed
  seed decides the number.

**Watch the sign.** In the gain tables positive is good, since a gain is fixed minus adaptive
for times and adaptive minus fixed for throughput. In the table "Which part moved" the change
is adaptive minus fixed, so negative is good there.

| number | what it is | better |
|---|---|---|
| service time | steps from an order until its delivery | lower |
| service time gain | fixed minus adaptive service time | higher, positive means adaptive helps |
| relative gain (%) | the gain as a share of fixed service time | higher |
| throughput | tasks finished per timestep | higher |
| throughput gain | adaptive minus fixed throughput | higher |
| backlog | tasks not finished at the horizon | lower |
| backlog cut | fixed backlog minus adaptive backlog | higher |
| keep-up ratio | throughput divided by the arrival rate | higher. 0.8 or more passes, above 1 means the seed had more orders than expected |
| wait for agent | steps before a robot takes the task | lower |
| stock wait | steps waiting for stock, part of the wait for an agent | lower (below 1 here) |
| travel | steps moving | lower |
| blocked | steps standing still in traffic | lower |
| crowding | how packed the robots are | lower |
| put-away per update | distance new stock travels to its shelves | lower, it is cheaper |
| ± after a mean | spread over the 6 seeds | smaller, more consistent |
| [a, b] | 95% interval of a gain | entirely above 0, the gain is clear |
| n/6 | seeds where the gain has the stated sign | 6/6 |
| validation tasks | tasks a checkpoint finished at load 0.6 | higher |
| runtime ms | time per decision | lower (not read in this run) |

Descriptions, not scores:
- **Direct share of the gain.** How much of the gain comes from shorter routes (travel plus
  blocked) rather than a shorter queue. A high share makes the gain a cleaner comparison
  across arms.
- **Wait cut per step of direct saving.** How much the queue multiplies a route saving. It is
  large when the fleet runs near its limit.
- **Split SKUs.** How many SKUs sit on more than one shelf.
- **Agents per decision.** The factor the arms are compared by.

## Soundness checks

| check | result | numbers |
|---|---|---|
| every evaluation finished | passed | 36 test rows per arm and load (2 checkpoints x 3 rules x 6 seeds), 12 groups. Token Passing 54 rows. 8 validation rows per folder |
| same test seeds everywhere | passed | seeds 200 000 to 200 005 in all 81 groups of router, role, rule and load |
| every row under the arrival model | passed | `stock_model` "arrival" in all 486 test rows and all validation rows. No row relocates anything, and every row has 20 arrivals |
| Token Passing reproduces the probe | passed | all 36 rows at margin 1 (loads 0.2, 0.3 and 0.6, fixed and demand) equal `rows_exact.jsonl` exactly in tasks completed, service time and its three parts, stock wait, units arrived, put-away, unplaced and overflow units |
| arrived units the same under every rule | passed | identical under fixed, demand and congestion for every router, role, load and seed. They are also identical across routers, since they depend only on the order stream |
| unplaced units 0 | passed | 0 in all 486 rows. Fixed storage overflows its home shelf at load 0.6 on seeds 200 003 (13 units) and 200 004 (4 units), the same for every router. That is where its split SKUs (1.8 and 0.45 per update) come from |
| service time equals its parts | passed | wait for agent + travel + blocked equals service time to 1e-13. The stock wait is never larger than the wait for agent |

What the checks turned up that limits the reading.

1. **The chosen checkpoint is the last one in every arm.** Both roles are `checkpoint_000003`,
   the fourth saved checkpoint (iteration 10), and the chosen and last rows are identical in
   all 216 pairs. There is no disagreement to report. Validation tasks at load 0.6 for the four
   checkpoints: decentralised 297, 540, 676, 719; centralised 235, 470, 597, 600; section 239,
   494, 600, 639; full view 249, 480, 522, 541. Every arm was still improving.
2. **Fixed storage is the same as the template model in distribution, not run for run, for
   the learned arms.** Token Passing differs by at most 3 tasks per seed, as in the probe. The
   learned arms differ by up to 18 tasks (centralised), 14 (section), 55 (decentralised, load
   0.3) and 107 (full view, load 0.6). On several seeds the rows are identical (centralised 4 of
   6 at load 0.3, full view 5 of 6). The means agree: centralised 75.4 in both models at load
   0.3, section 53.9 against 53.6. The fixed baseline of each paired comparison is its own run,
   so the gains are unaffected.
3. **The keep-up test lets a jammed run through at load 0.2.** It compares throughput with the
   nominal rate, and the orders released per seed vary from 348 to 442 at load 0.2 (400
   expected). Seed 200 005 can reach at most 0.87, every router sits at 0.86 or 0.87 there. On
   seed 200 000 the decentralised arm under demand and congestion storage finishes 336 of 378
   orders, with mean service time 273 (26.7 under fixed) and blocked time 19.0 (6.1 under
   fixed). It passes at 0.84. Full view under fixed storage on seed 200 002 passes at 0.96 with
   service time 173.
4. **Single seeds jam for the two arms that route each agent alone.** Decentralised: seed 200
   000 under adaptive storage at load 0.2, under congestion storage at 0.3 (298), and seed 200
   002 under demand storage at 0.6 (583 against 399). Full view jams on several seeds under
   every rule. The centralised and section arms and Token Passing show no jam on any seed.
5. **Validation ran at load 0.6 in every folder**, as in the short run. The checkpoint is
   chosen at the training load.

## Measured

### 1. The gain of adaptive storage over fixed

**Load 0.6.** No router keeps up under any rule (keep-up ratio 0.32 to 0.63 under fixed
storage), so throughput and backlog are compared.

| router | fixed throughput | demand gain | 95% interval | congestion gain | 95% interval | backlog cut, demand |
|---|---|---|---|---|---|---|
| centralised | 0.302 ± 0.005 | +0.041 ± 0.007, 6/6 | [0.034, 0.049] | +0.047 ± 0.004, 6/6 | [0.043, 0.051] | 83 (54 to 91) |
| section | 0.319 ± 0.007 | +0.042 ± 0.007, 6/6 | [0.034, 0.049] | +0.040 ± 0.008, 6/6 | [0.031, 0.048] | 84 (63 to 102) |
| decentralised | 0.349 ± 0.018 | +0.025 ± 0.058, 4/6 | [−0.036, 0.085] | +0.053 ± 0.028, 6/6 | [0.024, 0.083] | 49 (−146 to 158) |
| full view | 0.265 ± 0.040 | +0.021 ± 0.037, 4/6 | [−0.018, 0.060] | +0.049 ± 0.021, 6/6 | [0.026, 0.071] | 42 (−59 to 145) |
| Token Passing | 0.375 ± 0.005 | +0.072 ± 0.007, 6/6 | [0.064, 0.080] | +0.072 ± 0.006, 6/6 | [0.065, 0.078] | 144 (121 to 163) |

The demand rule raises throughput by 13.7% (centralised), 13.1% (section) and 19.1% (Token
Passing). The decentralised result turns on seed 200 002, where demand storage jams.

**Load 0.3.** Under fixed storage the centralised and section arms, the decentralised arm and
Token Passing keep up on 6 of 6 seeds, full view on 0 of 6.

| router | fixed service time | demand gain | 95% interval | congestion gain | 95% interval |
|---|---|---|---|---|---|
| centralised | 75.4 ± 20.1 | 48.9 ± 19.2, 6/6 | [28.8, 69.0] | 49.2 ± 18.9, 6/6 | [29.3, 69.1] |
| section | 53.9 ± 10.3 | 31.1 ± 9.5, 6/6 | [21.1, 41.1] | 31.3 ± 9.9, 6/6 | [20.9, 41.6] |
| decentralised | 38.0 ± 11.6 | not all keep up (5 pairs: 3.8 ± 8.1, 3/5) | | not all keep up (5 pairs: 15.9 ± 15.5, 5/5) | |
| full view | 217.6 ± 97.3 | none keep up | | none keep up | |
| Token Passing | 52.8 ± 11.8 | 23.1 ± 10.1, 6/6 | [12.5, 33.7] | 22.2 ± 9.1, 6/6 | [12.6, 31.7] |

The demand rule cuts service time by 65% (centralised), 58% (section) and 44% (Token Passing).

**Load 0.2.** Every router keeps up on every seed under every rule, by the test as defined
(see check 3).

| router | fixed service time | demand gain | 95% interval | congestion gain | 95% interval |
|---|---|---|---|---|---|
| centralised | 29.9 ± 3.8 | 10.1 ± 3.8, 6/6 | [6.2, 14.1] | 10.1 ± 3.7, 6/6 | [6.3, 14.0] |
| section | 24.1 ± 1.4 | 6.8 ± 1.1, 6/6 | [5.7, 8.0] | 6.8 ± 1.1, 6/6 | [5.6, 7.9] |
| decentralised | 22.2 ± 3.7 | −36.7 ± 102.9, 4/6 | [−144.8, 71.3] | −36.2 ± 103.2, 5/6 | [−144.5, 72.1] |
| full view | 60.3 ± 55.6 | 16.7 ± 54.9, 3/6 | [−40.9, 74.3] | −17.4 ± 125.1, 3/6 | [−148.7, 113.9] |
| Token Passing | 33.7 ± 7.6 | 14.7 ± 5.6, 6/6 | [8.8, 20.6] | 14.6 ± 5.6, 6/6 | [8.8, 20.5] |

The decentralised loss is seed 200 000 alone (−246.7). The other five seeds gain 3.9, −1.4,
12.1, 6.8 and 4.8, a mean of 5.2 ± 4.9 [−0.4, 10.9]. Leaving out a seed is a diagnostic here,
not a result.

**Which part moved**, demand rule minus fixed, paired. Negative is a cut.

| load | router | wait for agent | of which stock wait | travel | blocked |
|---|---|---|---|---|---|
| 0.3 | centralised | −42.6 ± 19.2, 6/6 | −0.014 | −4.70 ± 0.60, 6/6 | −1.59 ± 0.31, 6/6 |
| 0.3 | section | −24.9 ± 9.4, 6/6 | −0.010 | −5.27 ± 0.81, 6/6 | −0.98 ± 0.26, 6/6 |
| 0.3 | decentralised (5 pairs) | +0.4 ± 6.3, 3/5 lower | −0.017 | −3.97 ± 0.84, 5/5 | −0.28 ± 1.28, 3/5 |
| 0.3 | Token Passing | −20.1 ± 9.9, 6/6 | −0.002 | −3.06 ± 0.23, 6/6 | +0.04 ± 0.03, 1/6 lower |
| 0.2 | centralised | −2.66 ± 2.49, 6/6 | −0.001 | −5.56 ± 0.98, 6/6 | −1.88 ± 0.50, 6/6 |
| 0.2 | section | −0.86 ± 0.60, 6/6 | 0.000 | −5.04 ± 0.51, 6/6 | −0.94 ± 0.12, 6/6 |
| 0.2 | decentralised | +39.2 ± 95.7, 4/6 lower | −0.011 | −3.66 ± 1.65, 6/6 | +1.17 ± 5.93, 4/6 lower |
| 0.2 | Token Passing | −11.4 ± 5.4, 6/6 | −0.003 | −3.34 ± 0.40, 6/6 | +0.03 ± 0.04, 1/6 lower |

Travel falls on every seed for every router at every load. The stock wait is 0.09 per task at
load 0.2, 0.16 to 0.20 at 0.3 and 0.56 to 0.83 at 0.6, under every rule. It changes by at most
0.02 between rules, so it plays no part in the gain. Orders still waiting for stock at the
horizon are 0 on every seed except one at load 0.3 (1 order) and one at 0.6 (8 orders), the
same for every router and rule.

### 2. Against the relocation model

Demand gain under the relocation model (`short_run_2026-10-18.md`) and under the arrival model,
and the change, paired by seed.

| router | service time gain at 0.3, relocation | arrival | change | travel saved at 0.3, relocation | arrival | throughput gain at 0.6, relocation | arrival | change |
|---|---|---|---|---|---|---|---|---|
| centralised | 42.9 (57%) | 48.9 (65%) | +6.0 ± 6.1 [−0.4, 12.3], 6/6 | 3.56 | 4.70 | +0.037 | +0.041 | +0.005 [−0.006, 0.015], 4/6 |
| section | 27.7 (52%) | 31.1 (58%) | +3.5 ± 3.6 [−0.3, 7.2], 6/6 | 3.76 | 5.27 | +0.038 | +0.042 | +0.004 [−0.004, 0.011], 4/6 |
| decentralised | 5 pairs: 1.7 | 5 pairs: 3.8 | no reading | 3.73 | 3.93 | +0.045 | +0.025 | −0.020 [−0.063, 0.022], 1/6 |
| full view | none keep up | none keep up | | 2.31 | 3.84 | +0.046 | +0.021 | −0.025 [−0.068, 0.019], 2/6 |
| Token Passing | 13.0 (25%) | 23.1 (44%) | +10.1 ± 7.0 [2.8, 17.4], 6/6 | 1.66 | 3.06 | +0.053 | +0.072 | +0.018 [0.003, 0.034], 5/6 |

The arrival model raises the centralised and section gains on every seed, by 6.0 and 3.5
steps, with intervals that just reach below zero. It adds travel saving of 1.15 [0.68, 1.61]
(centralised), 1.51 [0.36, 2.67] (section) and 1.40 [1.01, 1.78] (Token Passing) steps per
task.

### 3. The gain across arms

Demand against fixed. The direct part is travel plus blocked time, the part a task saves on
its own route. The queue part is the cut in the wait for an agent.

| load | router | agents per decision | fixed service time | gain | travel saved (share of fixed travel) | blocked cut | wait cut | direct share of the gain |
|---|---|---|---|---|---|---|---|---|
| 0.2 | centralised | 8 | 29.9 | 10.1 (34%) | 5.56 (28%) | 1.88 | 2.66 | 74% |
| 0.2 | section | about 3 | 24.1 | 6.8 (28%) | 5.04 (26%) | 0.94 | 0.86 | 87% |
| 0.2 | decentralised | 1 | 22.2 | −36.7, one jam (5 seeds: 5.2) | 3.66 (24%) (5 seeds: 4.24, 28%) | −1.17 (5 seeds: 1.17) | −39.2 (5 seeds: −0.17) | 5 seeds: 103% |
| 0.2 | Token Passing | reference | 33.7 | 14.7 (44%) | 3.34 (25%) | −0.03 | 11.41 | 22% |
| 0.3 | centralised | 8 | 75.4 | 48.9 (65%) | 4.70 (22%) | 1.59 | 42.6 | 13% |
| 0.3 | section | about 3 | 53.9 | 31.1 (58%) | 5.27 (24%) | 0.98 | 24.9 | 20% |
| 0.3 | decentralised | 1 | 38.0 | 5 pairs: 3.8 (10%) | 3.97 | 0.28 | −0.4 | |
| 0.3 | Token Passing | reference | 52.8 | 23.1 (44%) | 3.06 (24%) | −0.04 | 20.1 | 13% |

- Every router saves 22% to 28% of its travel. The learned arms also cut blocked time by about
  the same share (centralised 28%, section 26% at load 0.2).
- Under fixed storage at load 0.2 the centralised arm travels 20.1 and is blocked 6.7 steps per
  task, the section arm 19.4 and 3.6, the decentralised arm 15.5 and 5.1.
- The wait cut per step of direct saving at load 0.3 is 6.8 (centralised), 4.0 (section) and
  6.6 (Token Passing). The fixed wait for an agent there is 47.6, 27.8 and 39.7.
- Token Passing waits 20.0 steps for an agent under fixed storage even at load 0.2, against 1.0
  to 3.1 for the three learned controllers.

### 4. Load 0.2

- Every router keeps up on every seed under every rule, by the 80% test.
- The wait for an agent under fixed storage is 3.1 (centralised), 1.0 (section) and 1.6
  (decentralised), so most of the learned arms' gain is direct (74% and 87%).
- The intervals are the narrowest of the three loads: ±4.0 (centralised) and ±1.1 (section),
  against ±20 and ±10 at load 0.3.
- The test passes jammed runs (check 3), and the decentralised gain at load 0.2 is decided by
  one of them.

### 5. Cost

Put-away distance per update (edge cost, from the receiving vertex to the shelf).

| load | units arriving | fixed | demand | congestion | per unit, fixed / demand | relocation model, demand (distance moved inside the warehouse) |
|---|---|---|---|---|---|---|
| 0.6 | 70.0 | 244.6 | 160.2 | 160.7 to 162.1 | 3.49 / 2.29 | 365 |
| 0.3 | 30.9 | 109.5 | 53.3 | 53.4 to 54.3 | 3.54 / 1.72 | 256 |
| 0.2 | 20.8 | 73.0 | 31.7 | 31.7 to 31.8 | 3.52 / 1.53 | not measured |

Fixed and demand put-away is identical for every router, since it reads only the order stream.
The congestion rule's differs by under 1% between routers. Under the demand rule 54 (load 0.2)
to 71 (load 0.6) SKUs sit on more than one shelf after an update. Fleet task travel saved per
100 steps under the demand rule is 73 to 109 at load 0.2 and 84 to 150 at load 0.3 (timesteps,
not edge cost).

### Congestion storage at β 1 against demand storage

Paired, congestion minus demand. For the routers that keep up the service time difference is
−0.3 to +0.9 at load 0.3 and −0.6 to +0.1 at load 0.2, every interval spanning zero. At load
0.6 the centralised arm gains +0.005 [0.001, 0.010], 6/6, and the others show no clear sign.
Put-away differs by less than 1.

## Inferred, not measured

- **The arrival model works with the learned arms without retraining.** Every check passed,
  and the fixed-storage baseline matches the relocation model's in its means. Run for run it
  differs for the learned arms, most likely because their actions are sampled and a rare
  stock-out shifts the order stream's timing for one task, after which the sampled routes
  diverge.
- **RQ1 is a yes for every router that does not jam.** Demand storage shortens service time on
  every seed for the centralised and section arms and Token Passing at loads 0.2 and 0.3, and
  raises throughput at 0.6 on every seed. For the decentralised arm and full view the answer
  depends on which seeds jam.
- **The arrival model raised the learned arms' gain less than Token Passing's.** It adds about
  the same travel saving to every router (1.2 to 1.5 steps per task). For Token Passing that
  nearly doubles its saving (1.66 to 3.06), for the learned arms it adds a third to a half on
  top of a saving that was already larger (3.6 to 3.8). So Token Passing went from 25% to 44%,
  the learned arms from 57% to 65% and 52% to 58%.
- **The gain across arms follows how long and how blocked each arm's routes are under fixed
  storage, not how many agents one decision covers.** Every arm saves about a quarter of its
  travel and blocked time. The centralised arm gains more than the section arm mainly because
  it travels further and is blocked twice as long under fixed storage, so a quarter of it is
  more. After 10 iterations this reflects how far each arm has learned, as in the short run.
  A fair comparison across arms needs the relative cut in the route time (travel plus
  blocked) next to the service time gain.
- **At load 0.3 the queue multiplies the direct saving by 4 to 7.** The multiplier is largest
  where fixed storage leaves the longest wait (centralised and Token Passing), so the gain at
  0.3 measures closeness to the fleet's limit as much as the storage rule.
- **Load 0.2 is the right load for the main result, with one change to the keep-up test.**
  The learned arms' gain there is mostly direct, the intervals are narrow, and every arm keeps
  up. But the 80% test against the nominal rate cannot tell a jammed run from a seed with few
  orders. Two candidates for the author: judge keep-up against the orders actually released on
  the seed, or add a bound on the backlog at the horizon. Either would flag the decentralised
  run on seed 200 000 (336 of 378 orders done, backlog 42). That is a thesis decision (the
  keep-up test of `sec:pf:measures`), not a code fix.
- **Token Passing's wait is not only a queue.** It waits 20 steps at load 0.2, where the learned
  arms wait 1 to 3, so most of its gain there goes through the wait for an agent (78%). Its
  gain at load 0.2 is therefore not directly comparable in its split with the learned arms'.
  Probably the cause is how Token Passing assigns tasks (only to a free agent whose path can be
  planned), not checked here.
- **The jams belong to the routers, not to the storage rule.** The decentralised arm and full
  view jam on single seeds under fixed storage too (full view at load 0.2 and 0.3, the
  decentralised arm at load 0.3 in the short run). With 6 seeds, which rule a jam lands on is
  luck. Demand storage does gather traffic near the delivery vertices (crowding rises a little
  for every learned arm), which may make jams more likely, but this run cannot show it.
- **Adaptive storage costs less than fixed under the arrival model, for every arm.** It saves
  41 (load 0.2) to 84 (load 0.6) put-away per update against fixed storage, and saves task
  travel on top. The relocation model's 256 to 365 per update of extra movement is gone.
- **The congestion rule at β 1 is the demand rule in practice.** It places stock almost
  exactly where the demand rule does, and no measure separates them. RQ3 at β 1 has nothing to
  report under the arrival model.

## Limits

One training seed, so arm and seed are confounded. 10 iterations, with every arm still
improving and choosing its last checkpoint. Policies trained under the template model and
fixed storage, then evaluated under the arrival model, so they never saw adaptive storage or
waiting orders. 6 test seeds, with intervals of ±20 steps on the centralised gain at load 0.3.
One instance, one setting of the arrival model (margin 1, Δ 100, receiving at the delivery
vertices, loose shelf capacity). Checkpoint chosen at load 0.6. Runtime not read, since four
evaluations ran side by side.

## What this means for the thesis

No number from this run goes into the thesis as a result. The policies trained 10 iterations
on one training seed. The run checks that the plan for the long run holds.

1. **The main result keeps its form.** The paired service time gain of demand over fixed
   storage per controller. Under the arrival model it is larger and cleaner, and adaptive
   storage costs less than fixed, which supports `[A38]` to `[A40]`.
2. **RQ1 is a yes** for every controller that does not jam (centralised, section, Token
   Passing).
3. **RQ2 is not answered yet.** The centralised arm gains most because its routes are longer
   and more blocked under fixed storage, so it has more to save. That reflects how far each
   arm learned in 10 iterations, not how many agents one decision covers. The long run answers
   it.
4. **Decisions for the thesis text.** Load 0.2 as the main load with 0.3 beside it (the
   decision queue in `SESSION_CONTEXT.md`, item 4). A keep-up test that a jammed run cannot
   pass (`sec:pf:measures`). RQ3 at β 1 as a limit, since the congestion rule behaves as the
   demand rule.

## What this means for the long run

1. **Train under the arrival model, as planned.** Nothing here argues against it. Fixed storage
   behaves as before in its means, and the adaptive rules now cost less than fixed storage.
2. **Main load 0.2, with 0.3 beside it.** At 0.2 the gain is mostly the route saving, which is
   what RQ2 needs. Load 0.3 shows how the queue multiplies it. Keep 0.6 for throughput.
3. **Decide the keep-up test before the long run** (against released orders, or with a backlog
   bound). Otherwise one jammed seed decides the decentralised arm's main result.
4. **Report the gain with its split and as a share of route time.** The arms differ mostly in
   how much route time they have to save. If the long run's arms converge to similar routes
   under fixed storage, the service time gain alone becomes a fair comparison. If not, the
   share is the comparison.
5. **Seeds.** 3 training seeds and 10 to 12 test seeds, as planned. The decentralised arm and
   full view jam on single seeds, and only more seeds separate a jam from an effect.
6. **Congestion rule.** At β 1 it adds nothing under the arrival model. Either drop it from the
   long run and keep RQ3 as a limit, or test a larger β once, by evaluation only.
7. **Cost graph.** Put-away against service time gain over a margin sweep, evaluation only,
   as `arrival_storage_plan.md` section 7 proposes.
8. **Checkpoint choice** at the measurement load, or say in the thesis that it is the training
   load. Still open from the short run.
