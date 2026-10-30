# G. Storage rule values

**Answers.** The storage period, the congestion weight and the refill size, the random storage check,
and why the safety stock is sized at the most popular rank.
**Fills.** Appendix G, `app:cal:period`, `app:cal:beta`, `app:cal:refill` (with `tab:app:skus`),
`app:cal:random` and `app:cal:safety`.
**Settings file.** `configs/step12/fleet_<m>.yaml`, copied as `config.yaml` into every folder. Setup in
`../README.md`.

## Commands, per fleet m

Each runs at the fleet's main load from `../E_load/fleet_<m>/capacity.json` (0.105, 0.15, 0.18 and 0.24),
one setting varied at a time:

    $PY scripts/sweep/load_sweep.py --config configs/step12/fleet_$m.yaml --rates $LOAD --seeds 20 \
        --storage-modes $MODES --vary $SETTING --values $VALUES \
        --horizon 10000 --warmup 5000 --out $R/G_storage/fleet_$m/$SETTING

| folder | `$SETTING` | `$MODES` | `$VALUES` | fills |
|---|---|---|---|---|
| `storage_rule.epoch_length` | `storage_rule.epoch_length` | `fixed demand congestion` | `50 100 200 400` | `app:cal:period` |
| `storage_rule.congestion_weight` | `storage_rule.congestion_weight` | `congestion` | `0.0 0.5 1.0 2.0 3.0 4.0` | `app:cal:beta` |
| `arrival.refill_units` | `arrival.refill_units` | `fixed demand random` | `15 30 60` | `app:cal:refill`, `app:cal:random` |

## The safety stock check, `safety_check/`

Fleet 8 at its main load, Q = 15, fixed storage, every SKU's safety stock sized at rank 0 by
`safety_check/top_rank_stock.py`, which replaces `refill_starting_stock` for the run:

    $PY $R/G_storage/safety_check/top_rank_stock.py --config configs/step12/fleet_8.yaml \
        --rates 0.105 --seeds 20 --storage-modes fixed --vary arrival.refill_units --values 15 \
        --horizon 10000 --warmup 5000 --workers 1 --out $R/G_storage/safety_check

The rows of the run of 2026-10-29 were in a scratch folder and are lost. Its result, the orders that
waited for stock falling from 5.7 % to 0.0 %, is in the sizing section below. Run the command again to get
the rows back (about 15 minutes).

## Findings

- **Storage period.** Stock arrives only at a storage update, so a long period also makes refills late.
  The wait for stock grows from 0.6 to 5.3 steps at 8 agents and from 3.6 to 15.8 at 64, and every rule
  slows down. The gain holds at every period (4 to 15 %). The period stays 100.
- **Congestion weight.** Weights 0 to 4 give the same pick time within 1.5 steps. A weight of 0 gives
  exactly demand storage. A pick is blocked for only 1 to 3 steps, 2 to 3 % of its time, and at most about
  7 even far above capacity, so the weight has nothing to work on under Token Passing. It stays 1.
- **Random check.** Random storage is 22, 22, 12 and 13 % slower than fixed at 8, 16, 32 and 64 agents,
  and faster on at most 3 of 20 seeds. So the gain of demand storage comes from knowing demand.
- **Refill size.** Refills per SKU per 4000 steps follow 12000 x load / (n Q), matched within 0.2.
  Doubling Q halves the put-aways. Every Q keeps up and the gain hardly moves with Q. The orders that waited
  for stock at Q = 15, 30, 60: 5.7, 2.8, 0.9 % at 8 agents and 14.1, 7.0, 2.9 % at 64. Decided: Q = 12 at
  every fleet and n = 250 x main load rounded to a multiple of 20 (`[A75]`).
- **Fixed storage overflows.** It puts 90 to 270 units per run off their home shelf, up to 620 at skew 1.5.
- **Safety stock.** Sized at each SKU's starting rank it was too small once the drift took the SKU to the
  top. Sized at the most popular rank (fleet 8, Q = 15), the orders that waited fell from 5.7 % to 0.0 %
  and a pick got 14 % faster, for a mean shelf fill of 24 % against 17 %. Decided: every SKU gets the
  top-rank safety stock (`[A75]`).

## Sizing the SKU count, Q and the safety stock (part D, D25)

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
