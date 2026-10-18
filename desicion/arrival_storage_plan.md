# Storage decided at arrival: the idea and a plan

Discussion paper, written 2026-10-18. **Status: adopted by the author on 2026-10-18
(decision 1).** PR G done and uncommitted in `~/worktrees/feat-arrival-config` (branch
`feat/arrival-config` from `main` at `9b6be93`). PR H done and uncommitted in
`~/worktrees/feat-arrival-stock`, on top of G. PR I in `~/worktrees/feat-arrival-rules`, on top
of H. PR J in `~/worktrees/feat-arrival-eval`, on top of I. All four pass acceptance (section 6). Decisions 2 to 9 are still open, apart from
what PR G builds in (see section 6). The thesis is not changed yet. Evidence: `arrival_probe_2026-10-18.md`. Related:
`short_run_2026-10-18.md` (the relocation options it replaces), `stock_template_2026-10-17.md`
(the stock questions it settles), `research_goals_2026-10-18.md` (the main result it serves).

## 1. The idea

Picks empty the shelves. Every storage period new stock arrives at the receiving point, and the
storage rule decides which shelves it goes to. Stock already on a shelf is never moved. Fixed
storage always puts new stock on the SKU's home shelf. Adaptive storage puts it where demand is
now. A SKU can sit on several shelves at once, old stock on one and new stock on another, and an
order picks from the shelf nearest its delivery point.

This is how the dynamic SLAP is usually defined, deciding where goods go "upon entry or reentry
into the system" (Waubert de Puiseau et al. 2022, already cited). It also gives the author's
earlier ideas a home. Receiving nodes are where stock arrives, and split inventory is how a SKU
can have stock near more than one endpoint.

## 2. Why, in short

Measured in the arrival probe (Token Passing, 6 test seeds):

- **Larger gain.** Service time gain at load 0.3 is 22.8 [12.7, 33.0] against 13.0 [4.8, 21.2]
  under today's relocation model, and 14.8 against 10.1 at load 0.2. Throughput gain at load
  0.6 is +0.072 against +0.053. Every seed agrees.
- **No free relocation.** Today's adaptive rule moves 256 units of distance per update inside
  the warehouse for free. Under arrival nothing moves, and the put-away the rule chooses is
  *shorter* than fixed storage's (54 against 110 per update at load 0.3).
- **Fixed storage is unchanged.** Arrival fixed equals today's fixed storage task for task at
  load 0.2 and within 3 tasks at 0.3 and 0.6. The baseline of the study stays the same.
- **No spreading problem, no leftovers, no cap.** Units run out, so a SKU spreads only as far
  as its stock. The cap ν and its split SKUs leave the model.
- **Most of the gain is the arrival mechanism.** The nearest-shelf pickup alone adds about 2
  timesteps at load 0.3, deciding at arrival about 8 more.

## 3. What it costs, and the risks

- **The model changes in four places.** Stock runs out, the storage update becomes put-away,
  an order can wait for stock, and the pickup rule changes. Every adaptive-storage result so far
  is replaced (the fixed ones are not).
- **New values.** The margin of stock above recent demand, the arrival period, the receiving
  vertices, and how tight shelf capacity is. The probe used margin 1, the arrival period Δ =
  100, the delivery vertices, and today's capacity. The gain shrinks with a larger margin
  (18.7 at margin 2 against 22.8 at margin 1, load 0.3).
- **Cold stock on prime shelves.** Under the demand rule 73% to 79% of the prime shelves'
  used capacity holds SKUs ranked 20 or lower. It costs nothing at today's loose capacity
  (about half used). With tight capacity the rule would run out of good shelves. That is the
  case healing moves exist for, and it should be stated as a limit.
- **The result depends on where stock arrives.** Receiving at the delivery side favours the
  adaptive rule in put-away cost. Receiving on the far side would not. Not measured.
- **Pairing must be kept by construction.** Stock is taken when an order is released, not
  when it is picked up, and the SKU of an order is drawn without looking at stock. Otherwise the
  order stream would depend on the controller.
- **The congestion rule under arrival is untested.** It would place arrivals by the
  congestion-aware score instead of distance alone. Not in the probe.

Alternatives considered, each set aside in one line:
- relocation with a per-SKU cap, because it keeps the free instant moves;
- unit-proportional pickup, because it gives split inventory no use;
- nearest pickup without stock running out, because it collapses into stock everywhere;
- robots carrying put-away, because it adds a second task type and retraining for every arm.

## 4. Decisions asked of the author

1. **Adopt the arrival model** as the storage model of the thesis? (Recommended.)
2. **Keep today's model as an option in the code**, `stock_model: template`, the default, so
   every existing config and result replays unchanged? (Recommended. The thesis describes only
   the arrival model, and the template rows serve as the check.)
3. **Margin** ε of stock above the last period's demand. Probe value 1. A sweep of 0.5, 1, 2
   is cheap (evaluation only).
4. **Arrival period.** Reuse Δ, so stock arrives at each storage update? (Recommended.)
5. **Receiving vertices.** The delivery vertices, one I/O side as Silva et al. (2020) assume
   (recommended), or a separate receiving set on the far edge, as a check.
6. **Shelf capacity.** Keep today's (about half used), or tighten it so cold stock on prime
   shelves matters? Recommended: keep it, and state the limit.
7. **Floor of units per SKU.** 8, today's `initial_units`. (Recommended, it is not new.)
8. **Congestion rule** under arrival: place arrivals by `eq:storagegreedy`'s score. Test value
   β = 1, as the short run suggests.
9. **Healing moves** (moving cold stock off prime shelves): not now. Discussion only.

## 5. Thesis changes

**Applied 2026-10-18, uncommitted in `thesis/`, as `[A38]` (storage at arrival), `[A39]` (pickup
rule, waiting orders) and `[A40]` (put-away distance), with `GAPS.md` entries.** The text below
was the proposal. The applied wording differs in detail. `eq:relocation` became `eq:putaway`, and
the new equations are `eq:arrivals` and `eq:pickuprule`. Still open: the two figures and the
values of `tab:storageparams`.

Tags are given when applied, after those reserved by `stock_template_2026-10-17.md` and
`research_goals_2026-10-18.md`. Each gets a `GAPS.md` entry. Symbols to check against
`tab:notation` first. Free now: `\varepsilon` (margin), `V_{\mathrm{rcv}}` (receiving
vertices). The order-up-to level needs a letter that is not a bar (bars are means) or a hat
(hats are estimates), for example `x^{\mathrm{up}}_t(k)`.

### `sec:pf:storage` (`2.Introduction.tex`)

- The stock state changes when an order takes a unit and when new stock arrives. Today's text
  says it stays fixed between updates (line 444).
- The storage update becomes the put-away of arriving stock. Proposed wording:

  > Every $\Delta$ timesteps new stock arrives at the receiving vertices, and the storage rule
  > decides which shelves it goes to. Stock already on a shelf stays where it is. Each SKU is
  > filled up to what the last period's orders suggest, with a margin, so the amount that
  > arrives does not depend on the rule. Formally, ...

- The reassignment term R and the cap ν leave the storage objective, since nothing is relocated.

### `sec:pf:tasks`

- An order takes one unit when it is released, from the shelf holding its SKU that is nearest
  its delivery vertex. With no unit in stock it waits, and its service time counts from the
  order. Proposed wording:

  > An order takes its unit from the shelf nearest its delivery vertex that holds the SKU. If
  > no shelf holds one, the order waits until stock arrives, and that wait counts towards its
  > service time.

- The stock condition (`eq:coupling`) stays, read at the time the unit is taken.
- The sentence on depletion and replenishment (lines 601 to 604) is replaced. Stock now runs
  out and is refilled.

### `sec:pf:measures`

- The relocation measure becomes the put-away distance per update, the distance arriving stock
  travels from the receiving vertices to its shelves, reported for every rule.
- Waiting for stock is part of waiting before assignment. It is reported on its own when it is
  not small.

### Scope (`sec:pf:scope`)

- Replace "Abstract inventory relocation" with an item saying that stock arrives in periodic
  batches and its put-away is not carried by the robots.
- Add the limit that cold stock is never moved off prime shelves.

### `sec:method:storage` (`4.Implementation.tex`)

- F_fix puts arrivals on the home shelf, F_dem on the shelves nearest a delivery vertex with
  room, F_cng by the congestion-aware score. The hard cap paragraph goes.
- `tab:storageparams`: ν goes, ε comes in, Δ becomes the arrival period.

### `sec:impl:instances`

- The starting stock is sized from the expected demand at t = 0 with the same margin, at least
  8 units per SKU, and placed in blocks as now.

### `tab:notation`

- New: ε, V_rcv, the order-up-to level, the put-away distance. Removed or changed: ν, ν_t and
  ν̄_T.

## 6. Code plan

Same working rules as `adaptive_storage_impl_plan.md` section 0. One PR at a time, in a
worktree from `main`, left uncommitted, tests for the changed files only, no training, the
thesis edited by the coordinator only. Thesis wording lands before the code PRs that need it.

```
main
 └ feat/arrival-config      PR G
    └ feat/arrival-stock    PR H
       └ feat/arrival-rules PR I
          └ feat/arrival-eval PR J
```

### PR G. Settings, no behaviour change

**Done 2026-10-18, uncommitted.** As built:
- `ExperimentConfig`: `stock_model` ("template" default), `stock_margin`, `stock_floor`,
  `stock_receiving` ("delivery" only), all required under "arrival", rejected under
  "template". Under "arrival" every storage mode needs Delta and none takes nu.
- Spec: an `arrival` section (`margin`, `receiving`, no defaults). Its presence switches the
  model on. `storage_rule.reassignment_cap` is now optional. Template adaptive modes still
  require it, and the arrival model refuses it. The floor is `storage.initial_units`, which
  builds in decision 7. Splitting it into its own field is easy if the author decides
  otherwise.
- `demand_sized_blocks`: sized by the spec's arrival rate, Delta and margin. It is identical
  to the probe's starting stock at loads 0.2, 0.3 and 0.6 and margins 0.5, 1 and 2.
- The simulator raises `NotImplementedError` for "arrival" until PR H.
- For PR J: `evaluate_run` builds the study from the training spec, so with `--arrival-rate`
  the sized stock would stay sized for the training load. The probe sized it for the load it
  played. PR J should build the test study from the test spec.

Planned:

- `core/experiment_config.py`. `stock_model: Literal["template", "arrival"] = "template"`, and
  `stock_margin: NonNegativeFloat | None = None`, required under `arrival`, with no default.
- `training/spec.py`. A `stock` section with `model`, `margin`, `receiving: "delivery"`. The
  starting placement `demand_sized_blocks` (units from expected demand at t = 0 with the
  margin, floor `initial_units`, blocks as `demand_blocks`).
- Tests. Validators, and every shipped config builds the same `ExperimentConfig` as before.

### PR H. Stock that runs out, and the pickup rule

**Done 2026-10-18, uncommitted** in `~/worktrees/feat-arrival-stock` (branch
`feat/arrival-stock` from `feat/arrival-config`, PR G's uncommitted diff applied). As built:
- `_release_orders` under "arrival": the template draw (count, then three numbers per order),
  the SKU over every SKU by the cumulative Zipf weights, orders queued as `Order(release_time,
  sku, delivery_vertex)` and recorded in the demand estimate at release. The queue is served in
  release order from the holder nearest the delivery vertex (ties by id). `stock_wait_by_task`
  is logged, and `B_t` counts waiting orders.
- Stage 6 raises `NotImplementedError` at the first arrival epoch until PR I. PR G's
  constructor guard is gone.
- Up to the first arrival, the tasks, stock and queue are identical to the probe's
  `ArrivalEnv` (Token Passing, loads 0.3 and 0.6, 3 seeds, fixed and demand). No stock-out
  happens in that window, so the waiting path is covered by unit tests only.
- The backlog differs from the probe's, which left out waiting orders. PR J's acceptance
  compares tasks, service time, stock wait and put-away, not backlog.
- The plan's test "an order with no stock is served at the next arrival" moves to PR I.

Planned:

- `environment/multi_agent_env.py`, under `stock_model == "arrival"` only. The template path
  stays bit for bit the same.
  - Stage 1. Draw the SKU from the full Zipf ranking, never filtered by stock, with today's
    random numbers. Queue the order. Then serve the queue in order, taking one unit from the
    holder nearest the order's delivery vertex (ties by vertex id). A served order becomes a
    task with `release_time` set to the order time. An unserved order stays queued.
  - Record when each task was served, for the stock wait.
  - The backlog `B_t` counts queued orders too.
- Tests.
  - The orders `(t, sku, delivery)` of a seed are identical under fixed and demand storage.
  - With stock everywhere, the arrival orders equal the template orders.
  - A unit is taken at release, and an order with no stock waits and is served at the next
    arrival.
  - The nearest holder is chosen, with ties by id.
  - The template path is unchanged (today's replay tests).

### PR I. Arrival and put-away rules

**Done 2026-10-18 by a subagent, uncommitted** in `~/worktrees/feat-arrival-rules` (branch
`feat/arrival-rules`, G and H applied). As built:
- `storage/arrival.py` holds `arrival_amounts` (exact window count `round(rho_hat x Delta)`),
  `PutAwayResult`, its own put-away registry, and one fill loop shared by "fixed" (home shelf
  first, overflow counted), "demand" and "congestion" (score, beta required). Put-away is
  measured `d_G(g, v)` from the receiving vertex to the shelf.
- The environment's stage 6 calls `_arrive` under the arrival model and `_update_storage`
  (the old code, moved unchanged) under the template model. New logs record put-away distance,
  units arrived, unplaced and overflow per update, and split SKUs.
- Choices flagged by the subagent:
  - fixed storage raises at construction if a SKU starts with no units, since it has no home;
  - an arrival with no orders in the window is not skipped, so the floor still arrives;
  - no `examples/` script or docs entry was added (docs now in PR J).
- `d_G` between storage and delivery vertices is symmetric up to about 1e-15 on the medium
  instance.
- **Acceptance (coordinator):** full 2000-step Token Passing episodes at loads 0.2, 0.3 and
  0.6, 6 seeds, fixed and demand, margin 1. All 36 are identical to `rows_exact.jsonl` in
  tasks, service time, travel, blocked time, stock wait, units arrived and put-away.

Planned:

- New `storage/arrival.py`. The arrival amounts: up to `max(floor, ceil((1 + margin) x orders
  in the window))` plus the queued orders, the same for every rule. Placement:
  - fixed: home shelf, overflow to the nearest shelf with room;
  - demand: SKUs by descending demand, nearest shelves with room;
  - congestion: as demand, shelves ranked by the congestion-aware score.

  Registered under the existing names, chosen by `stock_model`.
- Stage 6 calls the arrival rule under `arrival`. Logged per update: put-away distance, units
  arrived, units unplaced, split SKUs.
- Tests. The amounts are identical under every rule, the placement order, no unit is lost, the
  capacity is respected, and overflow and unplaced units are logged.

### PR J. Measures, evaluation, configs

**Done 2026-10-18 by a subagent, uncommitted** in `~/worktrees/feat-arrival-eval` (branch
`feat/arrival-eval`, G, H and I applied, so this worktree holds the whole stack). As built:
- `RunMetrics` gains `stock_model`, `mean_stock_wait`, `num_waiting_orders`,
  `mean_putaway_distance`, `mean_arrived_units`, `mean_split_skus`, `unplaced_units` and
  `overflow_units`, all with defaults. The backlog check adds waiting orders. New checks
  require template rows to keep the arrival fields at their defaults, the stock wait to be
  part of the wait for an agent, and arrival rows to relocate nothing.
- `compare_paired` refuses a template/arrival pair and summarises put-away, split SKUs and
  stock wait for arrival runs only.
- `evaluate_run` builds the test study at the test load (`build_test_study`), so the sized
  stock follows `--arrival-rate`. `summary.md` gains put-away and stock-wait columns for
  arrival runs.
- `configs/medium_arrival/*.yaml`: margin 1 and beta 1, flagged as illustrative and pending
  decisions 3 and 8.
- `docs/storage_rule_integration.md` gains a section on put-away rules. There is no
  `examples/` script.
- Flagged: `_relocation_distance` (on `main` since #174) iterates a set of SKU ids, so
  `mean_relocation_distance` can differ in its last digit between processes with different
  `PYTHONHASHSEED`. This is an existing bug, not from this stack. Sorting the SKUs fixes it.
  It needs an issue.
- **Acceptance (coordinator), through `run_episode` and `RunMetrics`:**
  - `configs/medium_arrival/decentralised.yaml` with Token Passing, loads 0.2, 0.3 and 0.6, 6
    seeds, fixed and demand: 36 of 36 identical to `rows_exact.jsonl` in every measure.
  - `configs/medium` (template), loads 0.3 and 0.6, fixed, demand and congestion: 36 of 36
    identical to the short run's Token Passing rows.

**Committing the stack.** Each worktree holds its PR plus everything below it, uncommitted.
Commit G in `~/worktrees/feat-arrival-config`. Then in `~/worktrees/feat-arrival-stock` run
`git reset feat/arrival-config` (a mixed reset: the branch moves onto G's commit and the files
stay), so only H is left as changes, and commit it. Do the same for I (`git reset
feat/arrival-stock`) and J (`git reset feat/arrival-rules`).

Planned:

- `evaluation/metrics.py` and `evaluator.py`. `mean_stock_wait`, `mean_putaway_distance`,
  `num_waiting_orders`, `mean_split_skus`. The relocation fields stay 0 under arrival.
- `slap-mapd evaluate` and `summary.md` report them.
- `configs/medium_arrival/{decentralised,centralised,section,full_view}.yaml`, with the
  author's values from section 4.
- Tests as in `tests/unit/test_evaluate_run.py`.

**Acceptance by the coordinator after PR J.** Token Passing with margin 1 reproduces the
probe's arrival rows in `~/thesis_runs/arrival_probe_2026-10-18/rows.jsonl` exactly (tasks
completed, service time and its parts, stock wait, put-away). The template rows still reproduce
the short run's Token Passing rows.

## 7. After the code

1. **Retraining is probably not needed for fixed storage.** The learned arms do not see
   stock, and fixed storage behaves as today. The long run trains fresh anyway, so this is a
   check, not a plan.
2. **Then the long run** with the changes in `short_run_2026-10-18.md`. That is 3 training
   seeds, 500 000 timesteps, 10 to 12 test seeds and loads 0.2, 0.3 and 0.6. It uses the
   arrival model, with fixed, demand and congestion (β 1) storage.
3. **Cost graph.** Put-away distance against the service time gain, per controller, over the
   margin sweep. This replaces the cap sweep of the relocation model.

## 8. What it settles elsewhere

- `short_run_2026-10-18.md`, relocation options 1 and 2 and whole-SKU moves are replaced.
- `stock_template_2026-10-17.md`:
  - decision 1 (put-away reading) becomes the model itself;
  - decision 3 (unit-proportional pickup) is replaced by the nearest-shelf pickup;
  - decision 2 (each SKU keeps its units) is replaced by the stock balance, where arrivals
    refill what was picked;
  - decision 4 (the one-epoch lag) is no longer needed, since nothing switches instantly.
- `research_goals_2026-10-18.md` change 11 becomes the scope items of section 5 above.
