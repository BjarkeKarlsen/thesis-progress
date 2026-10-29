# Step 12 sweep

**Answers.** Each step 12 fleet's capacity and main load under Token Passing, how the settings of the
sensitivity sweeps change the result, and the SKU count and Q of part D (D25).
**Run.** `bedtime.bash step12`, queue `~/thesis_runs/queue_2026-10-27_1330`, 27/10 13:40 to 29/10 16:26,
code `1056911` with the path cache fix of `12fdd59` copied in on 29/10 07:39 (the rows before it match the
new code exactly). `scripts/sweep/overnight.bash` on `configs/step12/fleet_{8,16,32,64}.yaml`, Token
Passing, 10000 steps with the first 5000 left out, 20 seeds per point, each seed its own warehouse (D27).
**Overview with every test and finding.** https://claude.ai/artifact/8tht3tBrq9Agtp7Vi4Y9sw

## Completeness

Every fleet has a `capacity.json` with a main load, and every sensitivity sweep has all its rows (3600).
One worker was killed by the kernel's out-of-memory killer at 27/10 16:07, which stopped pass 1 of the
finer rates for fleet 64 (`BrokenProcessPool` in `arrival_rates/load_fleet64/sweep.log`). Pass 2 ran the
same rates and filled every seed.

## Capacity and main load

Keep-up at the main load is read from the default rows of the sensitivity sweeps (fixed storage, Q = 30).
The pick part is recounted with ship tasks on the pick side, as step 12 says (see "Measurement problems").

| fleet | capacity | first failing | main load | keeps up | backlog slope /100 steps | longest gap between finishes | old capacity (`E_load`) |
|---|---|---|---|---|---|---|---|
| 8 | 0.175 | 0.2 | 0.105 | 20 / 20 | -0.03 | 66 | 0.2 |
| 16 | 0.25 | 0.3 | 0.15 | 20 / 20 | 0.03 | 27 | 0.2 |
| 32 | 0.3 | 0.4 | 0.18 | 20 / 20 | 0.06 | 21 | 0.6 |
| 64 | 0.4 | 0.6 | 0.24 | 20 / 20 | -0.07 | 21 | 0.5 |

Picks and put-aways both keep up on every seed at every main load. Against the old model, fleet 8 lost a
little, fleet 16 gained, fleet 32 halved and fleet 64 lost a fifth. The two are not like for like. The old
run had 2000 steps and no warm-up, and step 12 adds a shipping trip per order, random workstations, docks
along the whole left wall and a new warehouse per seed. Per robot the capacity falls from 0.022 at 8
agents to 0.006 at 64, as the warehouse and its trips grow with the fleet (longest trip 36 to 82).

The keep-up check passes rates where the backlog still grows. At each capacity the backlog rises by 1 to
2 tasks per 100 steps and a pick takes 2 to 5 times as long as at the lowest rate swept. The main loads
sit where the backlog is flat. Fleets 32 and 64 stop refining at a quarter of a grid step, so their
capacities are only known to 0.1 and 0.2.

## Sizing (part D, D25)

### The arithmetic

- The main load counts order lines per step, and a line asks for 1 to 5 units, 3 on average. Units
  ordered per step: 3 x load. In this sweep every order had one line, since `configs/step12/` sets no
  `lines_per_order`. The rerun has 5 lines per order on average (`[A46]`), which leaves the units per
  step, and so the refill arithmetic, unchanged.
- The refill rule orders back exactly what was ordered, in lots of Q (`refill_amounts`), so over a demand
  cycle of C = 4000 steps a SKU gets its share of the units divided by Q.
- The ranking rotates by 5 % of the SKUs every 200 steps, so over one cycle every SKU passes through every
  rank and its share averages 1 / n. The "middle-ranked SKU" of D25 is read as this mean. A SKU held still
  at the middle rank would get about half of it at Zipf skew 1.
- Refills per SKU per cycle: R = 3 x load x C / (n Q) = 12000 x load / (n Q).
- A line takes one pick and 3 / Q put-aways, and an order of L lines one ship task, so put-aways are
  (3 / Q) / (1 + 1 / L + 3 / Q) of all trips, whatever the fleet and the SKU count. With one line per
  order, as in this sweep, that is 3 / (2Q + 3).

The formula matches the sweep. Refills per SKU per 4000 steps, measured (fixed storage) and from the
formula, at Q = 15, 30 and 60:

| fleet | n | Q = 15 | Q = 30 | Q = 60 |
|---|---|---|---|---|
| 8 | 20 | 4.0 (4.2) | 1.9 (2.1) | 0.8 (1.1) |
| 16 | 30 | 3.8 (4.0) | 1.8 (2.0) | 0.8 (1.0) |
| 32 | 50 | 2.7 (2.9) | 1.2 (1.4) | 0.5 (0.7) |
| 64 | 100 | 1.7 (1.9) | 0.8 (1.0) | 0.3 (0.5) |

The measured count is a little lower because it is taken over the whole episode, whose start stock
covers the first orders.

### Two things the sweep's configs got wrong

- **The demand cycle was not 4000 steps at 16 and 32 agents.** The rotation moves
  `max(1, round(0.05 n))` SKUs. With 30 SKUs that is 2, so the ranking turns in 3000 steps, and with 50
  it is 2 again (Python rounds 2.5 to 2), so it turns in 5000. D20 holds only when n is a multiple of 20.
- **There is room for more slots than the configs used.** The configs set 2n slots and the generator
  leaves the other rack faces out. On 20 warehouses per fleet, the rack faces left after the workstations
  and the m parking faces allow at most 45, 95, 174 and 368 slots (n up to 22, 47, 87 and 184).

### Decided (author, 2026-10-29)

One Q at every fleet, Q = 12, so put-aways are the same share of trips everywhere, 17 % with the rerun's
5 lines per order (11 % with one line). The SKU count follows the load,
n = 12000 x load / (4 Q) = 250 x load, rounded to a multiple of 20.

| fleet | main load | 250 x load | n | slots 2n (most that fit) | refills per SKU per cycle | put-aways per 5000 steps |
|---|---|---|---|---|---|---|
| 8 | 0.105 | 26 | 20 | 40 (45) | 5.3 | 131 |
| 16 | 0.15 | 38 | 40 | 80 (95) | 3.8 | 188 |
| 32 | 0.18 | 45 | 40 | 80 (174) | 4.5 | 225 |
| 64 | 0.24 | 60 | 60 | 120 (368) | 4.0 | 300 |

The main loads come from this sweep's settings. The rerun changes the work per line in two ways. A
smaller Q adds put-aways, and 5 lines per order removes four shipments in five. So its capacities and
main loads will move, and the rule is applied once more to them. An order of 5 lines needs 5 distinct
SKUs, which every n above allows.
Fewer SKUs than today at 32 and 64 agents, more at 16.

### The check against the Q sweep

All Q values kept up on every seed at every fleet, and the gain of demand over fixed storage hardly moved
with Q. The waits for stock are the open point. The share of orders that waited for stock (fixed storage,
counted over the whole episode, see "Measurement problems"):

| fleet | Q = 15 | Q = 30 | Q = 60 |
|---|---|---|---|
| 8 | 5.7 % | 2.8 % | 0.9 % |
| 16 | 8.7 % | 4.5 % | 1.7 % |
| 32 | 12.6 % | 6.7 % | 2.0 % |
| 64 | 14.1 % | 7.0 % | 2.9 % |

D25 aims at about 1 %. The likely cause is the safety stock, not Q itself. S_k is Q plus the 99 %
quantile of one epoch's units at the SKU's rank at t = 0 (`refill_starting_stock`), but the ranking
rotates, so every SKU becomes the most popular for a while. That quantile is 25, 29, 30 and 33 units at
rank 0 and only 5 to 7 at the middle rank. A SKU that started mid-ranked holds Q + 7 units when it reaches
the top. At Q = 60 that still covers the top rank's epoch, at Q = 15 it does not, which fits the table.

**Checked 2026-10-29.** Fleet 8 at its main load, Q = 15, fixed storage, the same 20 seeds, with every
SKU's safety stock sized at rank 0 (S_k = Q + 25) instead of its starting rank. A scratch run, not a code
change (`refill_starting_stock` replaced for the run, rows not kept in the repo).

| safety stock sized at | orders that waited | mean stock wait | pick service time | mean shelf fill | overflow units (fixed) |
|---|---|---|---|---|---|
| each SKU's starting rank (the sweep) | 5.7 % | 2.35 | 49.6 | 17 % | 95 |
| rank 0, every SKU | 0.0 % | 0.02 | 42.9 | 24 % | 185 |

The waits go away, so the rotation, not Q, causes them. Picks get 14 % faster, because the stock wait
was part of the pick's wait. The cost is more stock on the shelves and more of fixed storage's units off
their homes. Sizing every SKU at rank 0 overshoots the 1 % aim. A rank between would hit it more closely.

**Decided (author, 2026-10-29).** Size every SKU's safety stock at the most popular rank, S_k = Q + the 99 %
quantile of one epoch's units at rank 0. Under the rotation every SKU reaches the top once per cycle, so
this is what the service level of D25 needs to hold over the whole cycle. A model change, to
`refill_starting_stock` in `training/spec.py` and the starting stock in the thesis, logged as
"D25, safety stock" in `model_revision/README.md`, with an `[Axx]` tag when the text is written. With it, Q = 12 should leave about as few waits as Q = 15 did here,
since the cover at the bottom of a lot is the rank 0 quantile either way.

## Measurement problems

- **The rows' pick keep-up leaves out completed ship tasks.** `evaluator.py` gives `keep_up_parts` the
  completed picks only, while the backlog it compares them with includes waiting ship tasks. The fields
  `keeps_up` and `keeps_up_picks` of every row are too strict, and so is the "picks keep up" column of
  every `summary.md` (fleet 8 at 0.175 shows 7 of 20 where the recount gives 20). The capacities stand,
  because the sweep recounts the check from the row with ship tasks on the pick side (`row_keeps_up`).
- **The order measures include the warm-up.** `order_metrics` is given `env.tasks`, the whole episode, so
  order completion, completed orders and lines that waited count the first 5000 steps too, and
  `orders_per_timestep` divides by 10000.
- **At 8 agents, rotation shares 0.025 and 0.05 are the same run.** Both round to one SKU.

## What reruns once the open points are settled

The full sweep (`bedtime.bash step12`) on the final configs, after the step 12 settings move into
`configs/fleet_<m>/` as part D says, with Q = 12, the SKU counts above, 5 lines per order
(`lines_per_order: {distribution: shifted_poisson, mean: 5}`), the class-based homes of
`b44db09`, the evaluator fixes if agreed, and fewer workers for fleet 64. About 27 hours at this run's
speed. Before it, the open question of the random workstation (`model_revision/README.md`, "Still open")
changes how demand is spread, and so possibly the sizing.
