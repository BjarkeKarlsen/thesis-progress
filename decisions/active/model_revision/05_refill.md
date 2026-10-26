# 04 and 05. Stock without the floor, arriving in fixed refills (proposed tags [A64], [A65])

**Decisions** D8 and D9 of `README.md`, agreed 2026-10-26. Steps 04 and 05 are done together in one session,
because both rewrite the arrival model. `04_stock.md` holds the reasons for removing the floor and the margin.
This file is the brief. Read `README.md` (decisions, order, risks, rules, "Where things live") first, then this
file to the end before writing code.

## Scope of this step

- **In:** the refill rule, the starting stock from a service level, refills placed whole on one slot, the
  storage rules' leg weights, the slot capacity check, configs, tests, and test B.
- **Out:** the graph (step 02, done before this), the rename (03, so keep `delivery` and `receiving` as names),
  the horizon and the stall (06), training, and any text in `thesis/`. After test B, propose the thesis wording
  to the author and wait.

## Before starting

- Step 02 must be in place (graph v2 and the random rule), since test B repeats test A on graph v2. Build on
  the step 02 worktree or on `main` after its PR, whichever the author says.
- `slap-mapd-coupling` `main` is at `e1abc67` and the main checkout holds uncommitted M1 to M4 work. Do not
  disturb it. Work in a worktree, leave the work uncommitted, report the path. The author opens the PRs.
- Python is `~/.venvs/rl/bin/python`. Tests: `~/.venvs/rl/bin/python -m pytest tests/unit -q`.
- The four correctness invariants of `slap-mapd-coupling/AGENTS.md` hold for every change to `storage/` and
  `environment/`: no conflicts, every storage configuration within capacity, every task in one lifecycle set,
  and bit-for-bit replay under a fixed seed.

## Why

**The floor.** Each SKU is filled up to max(x_min, ⌈(1+ε) n_k⌉) every period, n_k being its units ordered in the
last period. x_min = 8 is per SKU over the whole warehouse. With 100 SKUs the floor alone is 800 units, while
about 36 units are ordered per period at 8 agents. So the floor sets nearly all stock, ε reaches only the 1 to 5
most popular SKUs, and the graph v1 sweep of ε from 0.25 to 2 changed nothing (`results/G_storage/fleet_*/
arrival.margin/`).

**The refills.** Every period each SKU is topped up by about what was sold, often a handful of units, and every
(SKU, slot) the units land on is one put-away. At 8 agents about 180 of the roughly 430 tasks per episode are
put-aways, 4 in 10 robot trips and about 1.4 picks per put-away. Demand storage sends that many put-aways to the
best slots, which is what made it fail its put-aways at 32 and 64 agents. Letting a robot carry more changes
nothing, because a put-away already carries everything that arrived for its SKU and slot.

## Decided

Put-aways stay lifelong MAPD tasks, dock to slot, as in `[A47]`. Only how much arrives, and when, changes.

- **Refills of Q units.** Each SKU counts the units ordered since its last refill (picked, promised and waited
  for alike). At every delivery, a SKU gets ⌊counted / Q⌋ refills of Q units, and the remainder carries over.
  In words: "stock is replaced a refill at a time".
- **One delivery per Δ.** Every Δ steps a delivery arrives at the docks, holding every refill that is due.
  Popular SKUs are in nearly every delivery, slow ones rarely. Δ keeps its role (`07_text_reasons.md`).
- **One refill, one put-away, one slot.** A refill is placed whole on one slot. It is never split over slots.
  If no slot has room for a whole refill, it is unplaced and counted, as unplaced units are now.
- **Named a refill.** One sentence says it stands for a pallet or a case, which is why the amount is fixed. No
  pallet volume, rack levels or other pallet detail.
- **Q** is one number for every SKU, in units. A design value, about 10 picks per refill (Q = 30 with lines of
  about 3 units, `units_per_line` 1 to 5), tested in appendix G at a few values (step 11).
- **The service level replaces ε and the floor.** Each SKU starts with S_k = Q + the service-level quantile of
  its units ordered in one period at its t = 0 popularity. Under the refill rule a SKU's stock plus its stock on
  the way then stays between S_k − Q and S_k, so a period's demand runs it out only with the complement of the
  service level. The default 0.99 is a convention, cited. This is the (R, nQ) periodic review policy of
  inventory control. Axsäter (2015), *Inventory Control*, already in `thesis/references.bib` as
  `axsater2015inventory`, and already cited for the order-up-to policy (`2.Introduction.tex`, line 378). Check
  the chapter and page before citing.
- **The quantile is computed from the order generator itself**, not from a formula. Orders are Poisson with
  Zipf SKUs and 1 to 5 units per line (`environment/multi_agent_env.py`, around line 900), so the units of one
  SKU in one period follow a compound distribution. Simulate many periods of the order process once at setup,
  with a fixed seed, and take the empirical quantile per popularity rank. That is exact for the model and needs
  no distribution assumption.
- **Stock-outs** stay possible and rare. The existing rule stays: a line that finds no free stock waits, and is
  served after the next delivery (`[A39]`). Its units already count towards the next refill, so the q^wait term
  of `eq:arrivals` goes. The wait for stock is reported as a validity check that should stay near 0.
- **Unit sizes stay, for room only.** A unit takes 0.5, 1 or 2 of a slot's room (`unit_capacities`), so a refill
  of a bulky SKU takes up to 2Q room. They do not change Q or the SKU ranking.
- **Slot capacity is derived.** Fixed storage puts a SKU's starting stock and its refills on its home slot first,
  and a SKU never holds more than S_k. So every slot must hold max_k S_k × b_k (b_k the unit size), which also
  covers one refill of the bulkiest SKU. Use that, rounded up, as `vertex_capacity`, and report it per fleet.
  Then fixed storage never overflows by construction.
- **The storage rules weigh each leg by how often it happens.** The pick leg (slot to workstation) by picks per
  step, the put-away leg (dock to slot) by refills per step. Today `[A47]` weighs both by ρ̂ "because a SKU is
  put away about as often as it is picked" (`4.Implementation.tex`, lines 101 and 102), which stops being true.
  For SKU k at slot v: ρ̂_t(k) · d(v, workstations) + (ρ̂^unit_t(k) / Q) · d(dock, v). The ratio of the two weights
  is about the mean units per line over Q for every SKU, so the slot order is nearly the same for all SKUs.
  Implement it per SKU anyway.
- **The demand rule ranks by demand, and the text says so.** `[A52]` calls it cube-per-order
  (`4.Implementation.tex`, line 82), which would rank by size and demand together. Fix the text, not the rule.
- **Keep the old rule reachable.** Add `arrival.rule: "topup" | "refill"` (default `"topup"`), so every older
  config and the graph v1 archive still run as before. New configs use `"refill"`. Same idea as the `layout`
  switch of step 02.

## Open, flag to the author rather than choosing

1. **Mean or nearest workstation for the pick leg.** Orders pick a workstation uniformly, so the expected pick
   leg is the mean distance to the workstations. `trip_distance` (`storage/arrival.py`, line 161) uses the
   nearest, while the starting placement (`training/spec.py`, `_demand_blocks`) uses the mean. With
   workstations along the whole front, the two differ. The mean matches the model. Propose it.
2. **The service level value.** 0.99 is the proposal. Report how many lines wait for stock at it in test B.
3. **The risk period.** The quantile covers one period. Stock on its way to a slot is not yet pickable, so the
   true risk period is Δ plus the put-away time. Report the stock wait in test B before adding anything.

## What exists today (code)

`src/slap_mapd_coupling/storage/arrival.py`:

- `arrival_amounts` (line 123): today's top-up, max(floor, ⌈(1+ε) n_k⌉) plus `waiting_by_sku` less what is on
  hand. The refill rule replaces it, behind `arrival.rule`.
- `_put_away` (line 195): the fill loop every rule shares. Each SKU in `sku_order` places its units on its
  slots in `shelf_order(k)`, as many on each as fit. It splits a SKU over slots. Under the refill rule each
  refill goes whole to the first slot in the order with room for Q × b_k.
- `putaway_fixed`, `putaway_demand`, `putaway_congestion` (lines 251 to 345), registered by
  `register_putaway_rule`. Under robot put-away (`trip=True`) they rank slots by `trip_distance`, and the
  congestion rule scores ρ̂ · d^trip(v) + β · exposure. The leg weights change here.
- `trip_distance` (line 161), `trip_exposure` (line 179).

`src/slap_mapd_coupling/environment/multi_agent_env.py`:

- module docstring (lines 55 to 80): the arrival model and robot put-away, to update.
- `_arrive` (line 618): stage 6. Closes the estimate window, builds `waiting_by_sku`, calls `arrival_amounts`,
  calls the put-away rule, and creates one put-away task per (SKU, slot) placed, from the dock nearest the
  slot. Units on their way are `_in_transit`. Under the refill rule, the per-SKU counter of units ordered since
  the last refill lives here, and each refill becomes one put-away task.
- the order process (around line 900): Poisson orders, lines per order, units per line.

`src/slap_mapd_coupling/training/spec.py`:

- `StorageSettings` (around line 60): `unit_capacities`, `vertex_capacity`, `initial_units` (the floor),
  `initial_placement` (`"demand_sized_blocks"` sizes the starting stock).
- `ArrivalSettings` (line 161): `margin` (ε), `receiving`, `putaway`, `lines_per_order`, `units_per_line`,
  `cold_stock_top_k`. Add `rule`, `refill_units` (Q) and `service_level`. `margin` and `initial_units` are not
  used by the refill rule.
- `StockSizing` (line 186), `_sized_units` (around line 490): the starting stock formula with the floor and ε.
  The refill rule sizes it as S_k instead.
- `_demand_blocks`: the starting placement, popular SKUs on the slots nearest the workstations (mean distance).

`src/slap_mapd_coupling/core/experiment_config.py`: `stock_margin`, `stock_floor` (lines 109 to 115), and the
validator `_arrival_stock_parameters` (around line 146). Add the refill settings and their checks.

Configs: `configs/fleet_*/*.yaml`, the `storage:` (`initial_units: 8`, `vertex_capacity`) and `arrival:`
(`margin: 1.0`) sections. The sweep `scripts/sweep/parameter_sweep.bash` sweeps `arrival.margin`, which goes.

Tests to read first: `tests/unit/test_arrival_config.py`, `test_arrival_evaluation.py`,
`test_putaway_configs.py`.

## Tests

- a SKU gets a refill only once Q of it has been ordered since its last one, and n refills when n × Q have;
- every refill is exactly Q units, is one put-away task, and goes whole to one slot;
- a refill that fits no slot is unplaced and counted, and no slot ever exceeds its capacity;
- the deliveries are the same under fixed, demand, congestion and random storage on the same seed;
- a SKU's stock plus stock on the way stays within (S_k − Q, S_k];
- the starting stock S_k is Q plus the simulated quantile, and fixed storage never overflows at the derived
  capacity;
- the leg weights: with a large Q the put-away leg hardly matters, with Q = 1 both legs weigh about the same;
- `arrival.rule: "topup"` gives bit-for-bit the runs of today's model;
- replay is deterministic under a fixed seed.

## Test B, after the code works

**Question.** On graph v2, what does the refill rule change against test A, and how many storage decisions does a
run still have? (risk 3 of `README.md`)

1. The same main load as test A (8 agents), and the same commands with the refill configs:
   `scripts/sweep/load_sweep.py --config configs/fleet_8/decentralised.yaml --rates <test A's main load>
   --seeds 20 --storage-modes fixed demand random --out <dir>`.
2. Report everything test A reported, plus: the share of robot trips that are put-aways, the number of refills
   per run (the storage decisions), how many SKUs got at least one refill, the wait for stock, the derived slot
   capacity, and S_k for the top and bottom SKUs.
3. Then Q at 15, 30 and 60 (`--vary arrival.refill_units --values 15 30 60`, with fixed, demand and random), to
   see whether fewer storage decisions shrink the gain.

Write the rows to `thesis-progress/results/tests/B_refill/` with a `README.md` like the other results folders.
Read the result with the author before step 06.

## Thesis text, after test B and the author's approval

- `thesis/Chapters/2.Introduction.tex`, lines 374 to 382: "Each SKU is filled up to what the last period's
  orders suggest, with a margin and a floor, plus the units that lines still wait for. This is the order-up-to
  policy of inventory control". It becomes the refill rule, still Axsäter (2015), and the refill as a stand-in
  for a pallet or case in one sentence.
- `thesis/Appendices/C.ModelDetails.tex`, `app:storage:arrivals` (`eq:arrivals`, around line 98, its tea
  example with margin 1 and floor 8) and `app:storage:stock` (the starting stock, around line 130). The
  formal statements go back into the chapters when the thesis is reworked (`appendix_papers_handoff.md`).
- `thesis/Chapters/4.Implementation.tex`: line 82 (cube-per-order, `[A52]`), lines 96 to 105
  (`eq:storagegreedy` and the `[A47]` sentence on equal leg weights), line 127 (the arrivals are the same under
  every rule, still true).
- `thesis/Appendices/A.Notation.tex`: remove line 92 (ε) and line 93 (x_min). Add Q, S_k and the service level.
  α (storage weights, line 89) and γ (discount) are taken, so choose the service level's symbol from the table.
- `thesis/Appendices/B.Parameters.tex`: lines 31 and 32 (ε, x_min) become Q (*design*, tested in G), the service
  level (*cited*), and the slot capacity (*derived*).
- `thesis/Appendices/G.StorageValues.tex`: `app:cal:margin` becomes the Q test, `app:storage:shelfcap` the
  derived capacity.
- The `[A64]` and `[A65]` entries in `thesis-progress/decisions/GAPS.md`.

## Rejected, one clause each in the text

- Full pallets with pallet volume and rack levels: four new parameters for the same effect.
- Taking put-aways out of the robot fleet: it removes the most direct coupling, where every storage choice is at
  once a robot task.
- One delivery per Δ with each SKU's period demand: today's rule, still 4 in 10 trips.
- A refill carrying several SKUs to one slot: the number of trips would then depend on the storage rule.

## Decided while implementing (author, 2026-10-26)

- **Order lines of 1 to 5 units.** No fleet config set `units_per_line`, so test A ran with lines of one
  unit. The refill configs now use `units_per_line: [1, 5]` (`[A46]`). `lines_per_order` stays unset.
  `arrival_rate` stays lines per step, so there are about 3 times the units and the same number of lines.
- **The pick leg is the mean distance to the workstations,** under the refill rule only (open point 1).
  The author had no preference, and the mean matches the uniform workstation draw and the starting
  placement. One function (`storage/arrival.py::pick_distance`), easy to switch. The congestion term still
  follows the trip through the nearest workstation.
- **Every fleet starts equally full (D19).** With 100 SKUs at every fleet the shelves started 61 % full at
  8 agents and 3 % at 64, so storage had a different problem at each fleet. Now `storage.start_fill` sets
  the share of the shelves' capacity the starting stock fills, and the number of SKUs is derived from it,
  the fewest that reach it (`training/spec.py::derived_num_skus`). **f = 0.4.** The start is the fullest
  the shelves get, since a SKU then moves between S_k − Q and S_k, so a run averages about 0.6 f, about
  a quarter full. 0.6 was rejected: near 2 SKUs per slot the large fleets top out at 56 to 58 %, so the
  derived count jumped to 5.4 SKUs per slot at 32 agents. At f = 0.4 the counts are smooth:

  | fleet | slots | SKUs | per slot |
  |---|---|---|---|
  | 8 | 58 | 66 | 1.14 |
  | 16 | 230 | 278 | 1.21 |
  | 32 | 575 | 782 | 1.36 |
  | 64 | 1356 | 1929 | 1.42 |

  Step 06 rounds these to the nearest multiple of 20 (D20): 60, 280, 780 and 1920 SKUs, so 8 agents
  starts at 0.37.

  The fill rises with the SKU count as a sawtooth, because the derived capacity follows the fullest slot,
  which holds the most popular SKUs. Zipf with the same skew over more SKUs spreads demand thinner (the top
  SKU's share falls from about 21 % at 8 agents), and each SKU gets fewer refills. Name both in the text.
- **To test later, for appendix G:** f at a few values (`--vary storage.start_fill`, for example 0.3, 0.4,
  0.5) next to the Q test, to show how much the gain depends on how full the warehouse starts.
- **Test B is postponed** (author, 2026-10-26). The code is done first. Run it before step 06.
- **Derived capacity caveat.** A SKU's inventory position stays at most S_k, but units promised to a pick
  not yet picked up still take room, so a slot can briefly hold more than its starting stock. Fixed
  storage had no overflow in a 1000-step test run. Report overflow in test B.

## Done when

- the tests above pass (`tests/unit/test_refill.py`), and the tests of the changed modules still pass;
- test B is run and reported, with its folder and README;
- the three open points above are reported to the author with what test B showed;
- the worktree path, the changed files and anything decided along the way are reported, with nothing committed.
