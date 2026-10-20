# Arrival probe, 2026-10-18

What the arrival probe measured. Question from the author: what if picks empty the shelves,
and the storage rule decides where to put new stock when it arrives, instead of relocating
stock that is already there? Probe folder: `~/thesis_runs/arrival_probe_2026-10-18/`
(`probe.py`, `attribution.py`, `summarise.py`, `rows.jsonl`, `rows_nearest.jsonl`,
`summary.txt`). Code copied from `slap-mapd-coupling` `9b6be93` into `code/`. Nothing in the
repo or the thesis was changed. Token Passing only, nothing trained.

## Setup

- The 8-agent warehouse of the short run (94 vertices, 10 storage, 4 delivery vertices),
  horizon 2000, 100 SKUs, Zipf skew 1, ranking moves 5 places every 200 steps.
  `configs/medium/decentralised.yaml` with the planner swapped for Token Passing.
- Test seeds 200 000 to 200 005, loads 0.2, 0.3 and 0.6. Mean ± sd over seeds, gains paired by
  seed, 95% intervals with the t distribution (5 degrees of freedom), "6/6" counts seeds with
  the stated sign.
- Three models, each with a fixed and an adaptive rule.
  - **Template**, today's model. Stock never runs out. Pickup at a holder drawn uniformly.
    `F_fix` keeps the starting stock, `F_dem` relocates up to ν = 48 units every Δ = 100
    steps. The repo's own `run_episode`.
  - **Template, nearest pickup** (`attribution.py`). As template, but the pickup is the holder
    nearest the order's delivery vertex. Separates the pickup rule from the arrival mechanism.
  - **Arrival**, the model under test (`ArrivalEnv` in `probe.py`).
    - An order takes one unit when it is released, from the holder nearest its delivery
      vertex. With no unit anywhere, it waits for stock. Its service time counts from the
      order. The stock wait is also reported on its own.
    - The SKU is drawn from the Zipf ranking over all SKUs, never filtered by stock, with the
      repo's random numbers. The orders are identical under both rules (checked by hash).
    - Every Δ = 100 steps stock arrives at the delivery vertices (the I/O point). Each SKU is
      filled up to S_k = max(8, ceil((1 + margin) x its orders in the last window)), plus any
      orders still waiting. The amounts depend only on the order stream, so they are the same
      under both rules.
    - Fixed (dedicated storage): new units go to the SKU's home shelf, or the nearest shelf
      with room if home is full.
    - Demand: SKUs in descending demand of the last window, new units to the shelves nearest a
      delivery vertex that have room. Stock already on a shelf never moves.
    - Starting stock S_k from expected demand at t = 0, at least 8 units, in blocks of 10 SKUs
      per shelf as `demand_blocks`. Margin 1 in the main runs, 0.5 and 2 as a check.
    - Put-away cost: each arriving unit travels from the nearest delivery vertex to its shelf,
      in edge cost, under both rules.

New values in the arrival model, chosen for the probe and not decided: the margin (1), the
floor of 8 units (today's `initial_units`), arrivals once per Δ, and receiving at the delivery
vertices.

## Checks

| check | result |
|---|---|
| template rows reproduce the short run's Token Passing rows | passed, 24 of 24 identical (loads 0.3 and 0.6) |
| arrival orders identical under fixed and demand | passed, same hash on every seed, load and margin |
| arrival fixed equals template fixed | passed. Tasks completed are identical on all 6 seeds at load 0.2, and within 3 at 0.3 and 0.6, where the only difference is the rare stock-out |
| no unit lost | passed, 0 unplaced units in every row |
| stock waits equal under both rules | passed, by design. 0.09 (load 0.2), 0.17 (0.3), 0.70 to 0.82 (0.6) timesteps per task |

## Measured

### The gain of adaptive over fixed storage, three models

Service time gain at loads 0.2 and 0.3 (every run keeps up), throughput gain at 0.6 (no run
keeps up). Arrival at margin 1.

| | template | template, nearest pickup | arrival |
|---|---|---|---|
| fixed service time, 0.2 | 33.7 | 33.7 | 33.7 |
| service time gain, 0.2 | 10.1 ± 4.2 [5.6, 14.5], 6/6 | 11.9 [6.3, 17.5] | **14.8 ± 5.6 [8.9, 20.7], 6/6** |
| fixed service time, 0.3 | 52.2 | 52.2 | 52.8 |
| service time gain, 0.3 | 13.0 ± 7.8 [4.8, 21.2], 6/6 | 14.9 [6.3, 23.5] | **22.8 ± 9.7 [12.7, 33.0], 6/6** |
| throughput gain, 0.6 | +0.053 ± 0.011, 6/6 | +0.063 | **+0.072 ± 0.007, 6/6** |
| travel saved per task, 0.3 | 1.66 | 1.96 | **3.04** |
| blocked time change, 0.3 | +0.13 | +0.11 | +0.04 |

Relative to fixed storage, the arrival rule cuts service time by 44% at load 0.2 and 43% at
0.3, against 30% and 25% in today's model.

### Cost

| per update (100 steps), load 0.3 | template fixed | template demand | arrival fixed | arrival demand |
|---|---|---|---|---|
| stock moved inside the warehouse, d_G | 0 | 256 | 0 | 0 |
| put-away from the delivery vertices, d_G | not modelled | not modelled | 110 | 54 |
| units arriving | | | 31 | 31 |

At load 0.6 put-away is 245 (fixed) against 161 (demand), at 0.2 it is 73 against 32. Under
the arrival model the adaptive rule costs **less** than fixed storage, because new stock goes
to shelves near the receiving point.

### What the stock looks like

- Split inventory is used heavily. Under the demand rule 54 to 74 of the 100 SKUs sit on more
  than one shelf after an update, against 0 under fixed storage.
- Cold stock stays on the prime shelves. Of the capacity used on the two shelves nearest a
  delivery vertex, 73% to 79% belongs to SKUs ranked 20 or lower under the demand rule (80% to
  83% under fixed). Capacity never binds (0 unplaced units, overflow only in fixed storage at
  margin 2 and load 0.6), so this costs nothing here.
- Stock-outs are rare. 2 orders per episode at load 0.2, 4 at 0.3, 42 of about 1 200 at 0.6.

### Margin check

| margin | gain at 0.3 | throughput gain at 0.6 |
|---|---|---|
| 0.5 | 23.1 ± 10.0, 6/6 | +0.082 ± 0.009, 6/6 |
| 1 | 22.8 ± 9.7, 6/6 | +0.072 ± 0.007, 6/6 |
| 2 | 18.7 ± 11.1, 6/6 | +0.058 ± 0.005, 6/6 |

A larger margin leaves more old stock on far shelves and shrinks the gain. At margin 2 and
load 0.6 fixed storage overflows its home shelves (287 units), which helps it.

## Inferred, not measured

- **The arrival model gives a larger, cleaner gain than relocation, at a lower cost.** It
  follows the drift without a cap. Every unit picked comes back to where demand is now, and
  nothing is moved inside the warehouse.
- **Most of the extra gain comes from deciding at arrival, not from the pickup rule.** The
  nearest pickup adds about 2 timesteps at load 0.3, deciding at arrival about 8 more.
- **The reading of the probe of 2026-10-17 holds.** Fixed storage is the same in both models,
  so the gains compare like for like.
- **The spreading problem does not appear.** Units run out, so a SKU is split only as far as
  its stock reaches.
- **Cold stock on prime shelves is the known weakness, and it is invisible here** because
  capacity is loose (about 1 000 of 2 000 capacity units used). With tight capacity the
  arrival rule would run out of good shelves, and healing moves (moving cold stock out) would
  matter. The instance's capacity is part of the result.
- **Put-away cost depends on where stock arrives.** Receiving at the delivery vertices (one
  I/O side, as Silva et al. 2020 assume) favours the adaptive rule. Receiving on the far edge
  would not. Not measured.

## Limits

Token Passing only. One instance, 6 test seeds. The margin, the floor of 8 units, arrivals
once per Δ, the receiving vertices and loose capacity are probe choices. Orders take one unit.
The learned arms were not run, because their checkpoints were trained on today's model.

## What follows, if the author adopts the arrival model

- Model: picks lower `x_t`, the storage update becomes put-away of arriving stock, the stock
  condition can make an order wait, and the pickup is the holder nearest the delivery vertex.
  Thesis changes in `sec:pf:storage`, `sec:pf:tasks`, the scope list (stock runs out and is
  refilled) and `sec:method:storage`. The relocation cap ν leaves the model, and Δ becomes
  the arrival period.
- The relocation measure becomes put-away distance, reported for every rule.
- The main result keeps its form: the paired service-time gain per controller.
- Decisions it needs: the margin, the arrival period, the receiving vertices, and whether
  capacity should be tighter.
- Code: an `ArrivalEnv`-style change in `environment/multi_agent_env.py` and a new storage
  rule, in a small PR, then retraining (the learned arms see the new pickups).

## Second run, exact version (`probe_exact.py`, `rows_exact.jsonl`)

Same day, run as the acceptance baseline for the implementation (PR I and J). Two changes, both
made in the repo implementation. The window's order count is `round(rho_hat x Delta)` instead
of the float product, which could come out a hair above an integer and add a unit. Put-away
distance is measured from the receiving vertex to the shelf, `d_G(g, v)`, instead of the
reverse. The 84 arrival episodes were rerun, and the template rows are unchanged. 40 of the 84
rows differ in tasks completed or service time, and none of the readings move materially.

| | first run | exact |
|---|---|---|
| service time gain, load 0.2, margin 1 | 14.8 | 14.7 |
| service time gain, load 0.3, margin 1 | 22.8 | 23.1 |
| throughput gain, load 0.6, margin 1 | +0.072 | +0.072 |
| put-away per update, load 0.3, fixed / demand | 110 / 54 | 109 / 53 |
| service time gain, load 0.6, margin 2 (no run keeps up) | 24.7 | 27.1 |

The tables above stay as measured in the first run.
