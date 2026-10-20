# Plan: code for `[A47]`, robots carry the put-away

**Status 2026-10-19. Changed by the author: all six steps on one branch,
`feat/putaway`, from `origin/feat/cold-stock`, in one session.** The thesis does not hold
`[A47]` yet, so `A47_putaway_draft.md` stands in for it and the "stop if the thesis disagrees"
check is skipped for `[A47]` text. The per-step branch names below are history.

**Done 2026-10-19, uncommitted** in the worktree
`/tmp/claude-1000/-home-bjarkek-Documents-thesis/80420b23-81c9-4590-82a6-f425220878cb/scratchpad/feat-putaway`
(branch `feat/putaway`). P1 to P6 are all in. With the defaults, every shipped config gives the
same instance and the arrival episodes the same tasks, stock and measures as `feat/cold-stock`.
Points for the author:
- `instances/validation.py` (not listed) now counts V_rcv as task endpoints. `docs/MODELS.md`
  says eight features.
- Fixed 2026-10-19 in thesis and code: the arrivals equation now counts stock on its way as
  stock, so it is not ordered again (`[A47]`, GAPS.md).
- The examples draw the receiving vertices (theme, matplotlib, pygame), and 00, 00a, 00b, 01,
  01b `--render`, 01c, 02 and 04 build instances with them. 01 A* and 02 had stale generator
  options (`num_aisles`, `aisle_length`) and now use the current bounds.
- The logged B_t is taken before stage 1, so it leaves out the tasks released at t. The thesis
  B_t includes them. Total service time follows the thesis, so "the area under the backlog"
  holds for the thesis B_t, not for `backlog_by_t`. Put-aways released at T are left out of
  B_T, as picks released at t are left out of B_t.
- Put-aways per arrival is a new field, `num_released_putaways`. The thesis text is `[A47]`, drafted in `A47_putaway_draft.md` at the workspace
root and applied to `thesis/` by a separate session. The rationale is the `[A47]` entry of
`thesis-progress/decisions/GAPS.md`.

Work through the steps **in order**. The
session makes the change in a git worktree and reports the worktree's path. The author runs
the checks, commits, pushes and opens the PR.

After P6 the author runs Token Passing on the 8-agent warehouse to test the whole model, and
then trains one arm on it. The larger warehouses (W2 of `code_changes_plan_2026-10-19.md`)
come after that.

---

## Rules for every run (read first)

### Setup

1. Read `AGENTS.md` and `CLAUDE.md` at the workspace root, then
   `slap-mapd-coupling/AGENTS.md` and `slap-mapd-coupling/CLAUDE.md`.
2. Read the thesis sections the step names with `python3 thesis_section.py <label> ...`, run
   from the workspace root. **Don't pull `thesis/`**. Read it as it is. Look for the lines
   tagged `% [A47]`. The thesis is the source of truth. If the step and the thesis disagree,
   stop and report it. `A47_putaway_draft.md` explains the intent, but the thesis wins.
3. Work in a new git worktree, never in the author's checkout of `slap-mapd-coupling`, which
   may hold uncommitted work. Don't run `git checkout`, `git stash`, `git reset` or
   `git pull` there. Each step starts from `origin/<previous step's branch>`, which the
   author has committed and pushed, so the PRs stack. If that remote branch does not exist
   yet, stop and report it.

   ```
   git -C slap-mapd-coupling fetch origin
   git -C slap-mapd-coupling worktree add <scratchpad>/<branch> -b <branch> <base>
   ```

   Work only inside the worktree, with `PYTHONPATH=<worktree>/src PYTHONDONTWRITEBYTECODE=1`.
   Python is `~/.venvs/rl/bin/python`.

### Hand-off

- **Leave the changes uncommitted in the worktree.** Don't commit, don't push.
- You may run the test files you touched, with
  `~/.venvs/rl/bin/python -m pytest -q -p no:cacheprovider --no-cov <files>`. Don't run the
  whole suite (it takes over 20 minutes), black, flake8 or mypy. The author does.
- **Don't touch GitHub.** No issues, comments or PRs.
- **The final reply is the worktree's path**, and one line per test file run with its result.
  If the step stopped early, add one line saying why.

### Hard limits

- Never edit anything in `thesis/` or `thesis-progress/`.
- **Keep the step small.** Stop and report, without coding around it, if
  - the thesis and this plan disagree,
  - a step needs a file this plan does not list, or a new design choice,
  - an existing test would have to change for a reason the step does not name.
- **Old runs must replay.** Every new option defaults to today's behaviour. With the defaults,
  every existing config gives the same instance, the same tasks and the same metrics as on
  `main`. The only exception is step P1's vertex feature, which the author has accepted.
- **Don't invent values.** A value the thesis marks TBD becomes a config field with default
  `None` and a comment saying it is TBD.
- The four correctness checks of `slap-mapd-coupling/AGENTS.md` (no vertex or swap conflicts,
  capacity respected, one lifecycle set per task, bit-for-bit replay) must still hold. Under
  `[A47]` "capacity respected" means shelf stock plus stock on its way.

### Writing in code

- **Cite equations by name, never by label.** Write "the storage update", not
  `eq:storageupdate`. The names are in `thesis/styles/eqnames.tex`. Section and table labels
  (`sec:...`, `tab:...`) stay.
- **Symbols follow `thesis/Chapters/2.Notation.tex`.** `[A47]` adds $x^{\mathrm{in}}_t$
  (units on their way), $\zeta^{\mathrm{tot}}_T$ (total service time) and
  $d^{\mathrm{trip}}(v)$ (the trip distance).
- **Shorten docstrings you touch.** Don't rewrite files the step doesn't list.
- **UK spelling** (behaviour, organise, colour).
- Write a test that fails without the change, next to the code it tests.
- RLlib's new API stack only. No step should need to touch `training/` beyond `spec.py`.

---

### Decision the author makes before P1

**How many receiving vertices.** The thesis leaves the count open. P1 adds the field with
default 0, so no value is needed to write the code. P5 needs one for the 8-agent config.
Suggested: 4, the same as the delivery vertices, since about 30 put-aways leave at once at
every arrival. If no answer is recorded here when P5 starts, P5 stops.

> Answer (2026-10-19): a config field, `num_receiving_vertices`, default 0 so old runs replay.
> Each `medium_putaway` config sets it to its own number of delivery vertices.

---

## P1. The receiving role

Branch `feat/receiving-role` from `origin/feat/cold-stock`.

Thesis: `python3 thesis_section.py sec:pf:storage sec:impl:instances`. Read the receiving
vertices on one side, and the role placement in `sec:impl:instances`.

What the thesis says. Receiving vertices are a role of their own, drawn at random from one end
row of the warehouse, the inbound side. Storage, delivery and parking vertices are drawn at
random from the rest.

Change.
- `core/graph.py`. `VertexRole.receiving: bool = False`. It requires `movable` like the other
  roles, and `is_task_endpoint` includes it.
- `instances/generator.py`.
  - `GeneratorParams.num_receiving_vertices: NonNegativeInt = 0`, counted in
    `num_role_vertices`.
  - The end row is row 0 of the grid, the corridor that joins every aisle
    (`_create_transit_segments`). The receiving vertices are drawn from the row-0 vertices, and
    the other roles from the rest. The well-formedness check covers all role vertices together,
    as today.
  - **With `num_receiving_vertices = 0` the random draws must be exactly today's**, so every
    existing seed gives the same instance. Draw the receiving vertices only when the count is
    above 0.
  - `_assign_roles` sets `receiving`.
- `environment/observation.py`. `role_flags` returns receiving as a fifth flag, and `transit`
  excludes it. Update `VertexFeatures` to match.
- `models/gnn_encoder.py`. `NODE_FEATURE_DIM` from 7 to 8. Checkpoints from before this step no
  longer load. The author has accepted this, since every policy is retrained.
- `planners/token_passing.py`. A receiving vertex is never a parking vertex (the list near line
  210 that excludes storage and delivery).
- `core/experiment_config.py`. `ReceivingVertices = Literal["delivery", "receiving"]`.
  `"receiving"` means the vertices with the receiving role.
- `storage/arrival.py`. `_put_away` takes the receiving vertices as an argument instead of
  calling `delivery_vertices(graph)`, so the put-away distance is measured from them. The env
  passes them from `config.stock_receiving`.
- `training/spec.py`. The `instance` section passes `num_receiving_vertices` through.
  `ArrivalSettings.receiving: "receiving"` is rejected when the instance has no receiving
  vertex.

Test.
- For every config under `configs/`, the instance with the default count equals the one on
  `main`: same vertices, roles and edges. Compare against a role and edge digest computed in
  the test from a fixed seed, not a stored fixture.
- With `num_receiving_vertices: 4` on the medium instance parameters, there are 4 receiving
  vertices, all on row 0, and the instance is well-formed.
- `role_flags` of a receiving vertex sets the receiving flag and no other, transit included.
- Token Passing never parks on a receiving vertex.

Stop if no seed of the medium parameters gives a well-formed instance with 4 receiving
vertices on row 0.

---

## P2. Put-away tasks and stock on its way

Branch `feat/putaway-tasks` from `feat/receiving-role`.

Thesis: `python3 thesis_section.py sec:pf:storage sec:pf:tasks`. Read the storage update with
$x^{\mathrm{in}}_t$, the paragraph on robots carrying the stock, the task definition with two
kinds, and the stock condition.

What the thesis says. Every shelf a SKU's arriving units are put on gives one put-away task. It
is released at the epoch, picks the units up at the receiving vertex nearest the shelf (ties by
vertex id) and delivers them to the shelf. Until it is delivered the units are on their way,
$x^{\mathrm{in}}_t$. They take up room on the shelf but cannot be picked. On delivery they move
from $x^{\mathrm{in}}_t$ to $x_t$. A put-away has no stock condition. Free agents take picks and
put-aways from one queue, oldest first.

Change.
- `core/experiment_config.py`. `stock_putaway: Literal["instant", "robots"] = "instant"`,
  arrival model only. `"instant"` is today's behaviour.
- `core/tasks.py`. `Task.kind: Literal["pick", "putaway"] = "pick"`. Fix the two comments that
  say the pickup vertex is in V_str and the delivery vertex in V_del.
- `environment/multi_agent_env.py`, under `stock_putaway == "robots"` only.
  - Keep `self._in_transit: dict[SkuId, dict[VertexId, int]]`, reset in `reset()`.
  - `_arrive`. Pass the put-away rule the stock on the shelf plus the stock on its way, so its
    capacity check reserves the room. The units it placed are its result minus what it was
    given. `self.storage` (the shelf stock) does not change. Add the placed units to
    `self._in_transit`. Make one put-away task per (SKU, shelf) with units placed, in SKU id
    then vertex id order, released at the arrival step (`self._t + 1`, as in `_arrive` today).
  - `_advance_task_lifecycle`. When a put-away completes, move its units from
    `self._in_transit` to `self.storage`.
  - The cold-stock lots of G2 (`self._lots`) get the units when the put-away is delivered, not
    when they arrive, so the age at pick is time on the shelf.
  - Picks keep reading `self.storage` only, so the stock condition and the pickup rule need no
    change.
  - `stock_wait_by_task` and `order_line_by_task` stay pick-only. Check that `_backlog` counts
    waiting and active put-aways.
- `evaluation/evaluator.py`. Only what is needed so a robots run still builds a valid
  `RunMetrics` row: `mean_stock_wait` over completed picks. The new measures are P4.

Test.
- Under `"instant"`, an arrival episode on `configs/medium_arrival` replays its tasks and
  metrics exactly as before this step.
- Under `"robots"`, at an arrival the shelf stock is unchanged, the stock on its way holds the
  placed units, and there is one put-away per (SKU, shelf) with the right quantity and the
  nearest receiving vertex as its pickup.
- A line for units that are only on their way waits. It is served at the first stage 1 after the
  put-away is delivered, not before.
- Shelf stock plus stock on its way stays within every shelf's capacity at every step of a
  Token Passing episode with several arrivals.
- Replay of a robots episode is bit-for-bit deterministic. Every task, put-aways included, has
  one lifecycle set at every step.

Stop if Token Passing assumes anywhere that a pickup vertex is a storage vertex or a delivery
vertex is a delivery role vertex. Report where.

---

## P3. The trip distance in the storage rules

Branch `feat/trip-distance` from `feat/putaway-tasks`.

Thesis: `python3 thesis_section.py sec:method:storage`. Read the trip distance and the three
rules.

What the thesis says. Every rule judges a shelf by the trip of a unit through it,
$d^{\mathrm{trip}}(v) = \min_{g \in V_{\mathrm{rcv}}} d_G(g, v) + \min_{g \in V_{\mathrm{del}}} d_G(v, g)$,
with no weight. $F_{\mathrm{fix}}$ sends overflow and $F_{\mathrm{dem}}$ sends every SKU to the
shelves in order of $d^{\mathrm{trip}}$. The congestion-aware score is
$\hat\rho_t(k)\, d^{\mathrm{trip}}(v) + \beta \sum_{e} \hat\mu_t(e)\hat w_t(e)$ over the edges of the
trip, the shortest path from the nearest receiving vertex to $v$ and on to the nearest delivery
vertex.

Change.
- `storage/arrival.py`. A function `trip_distance(graph, vertex, receiving, delivery)`, and a
  shelf order by it, ties by vertex id. Under `stock_putaway == "robots"` the three put-away
  rules use the trip. Under `"instant"` they stay exactly as today. Pass the mode, or the
  receiving vertices with `None` for the old behaviour, through the `PutAwayRule` protocol.
- The congestion score sums the traffic estimates over both legs of the trip. Write the path
  helper next to the rules. Don't change the template model's helpers in `storage/base.py` or
  wherever `ranked_storage_vertices_for` lives, since the template rules must replay.

Test.
- On a hand-built small graph, a shelf next to the delivery vertex but far from the receiving
  vertex loses to a shelf halfway between, under the demand rule, when its trip is longer.
- The congestion score of a shelf counts traffic on an edge of the receiving leg.
- Under `"instant"` every rule's placement on the medium arrival config is as on `main`.

---

## P4. Total service time

Branch `feat/total-service` from `feat/trip-distance`.

Thesis: `python3 thesis_section.py sec:pf:measures`. Read the service time paragraph, the total
service time, its split into totals, the keep-up note on put-aways, the gain and the relative
gain.

What the thesis says. The result is $\zeta^{\mathrm{tot}}_T$. It sums, over every task released
by $T$, $\min(t^{\mathrm{finish}}, T) - t^{\mathrm{released}}$, plus $T - t^{\mathrm{released}}$
for every order line still waiting for stock at $T$. The three parts are summed the same way,
open tasks up to $T$. Mean service time is reported over picks only. The keep-up check counts
put-aways and excludes nothing at the horizon. The gain and the relative gain use the totals.

Change.
- `evaluation/metrics.py`. New fields:
  - `total_service_time` ($\zeta^{\mathrm{tot}}_T$), `total_wait_for_agent`,
    `total_travel_time`, `total_blocked_time`. An open task adds its wait up to its
    assignment or $T$, and after assignment its moving and blocked ticks up to $T$. A waiting
    order line adds all its time to the wait. The four add up, so add a validator like
    `_split_adds_up`.
  - `total_service_time_finished`, the same sum over completed tasks only. The author wants
    both in the Token Passing test, to see how much the open work changes the total.
  - `num_completed_putaways` and `mean_putaway_service_time` (`None` without one).
  - `mean_service_time` and its three means become picks only, which is today's value for
    every existing run, since every task there is a pick. Say so in the comment.
- `evaluation/evaluator.py`. Fill them. `completed_share` and the backlog already count
  put-aways once P2 has run, so check that and don't change them.
- `evaluation/comparison.py`. The service-time comparison compares `total_service_time`. The
  relative gain divides by the fixed run's `total_travel_time + total_blocked_time`. Keep the
  mean pick gain as an extra field next to it.
- `training/evaluate_run.py`. The summary table leads with the total gain and the relative gain.
  The mean pick gain and the order completion time follow.

Test.
- The timeline example of `fig:timeline` (`thesis-progress/scripts/images/timeline.py` holds
  its numbers: released 5, 3, 10, 11, assigned 9, 3, 12, 12, finished 14, 11, 18 and open, T =
  20) gives a total of 34 and totals of the parts that add up to it.
- With no waiting order line, `total_service_time` equals the sum of `backlog_by_t` over
  `t < T`.
- A line still waiting for stock at $T$, released at $T - 7$, adds 7.
- Under the template model and under `"instant"`, `mean_service_time` is the value on `main`.
- Two seeds with known totals give the expected total gain and relative gain.

---

## P5. Configs for the put-away model

Branch `feat/putaway-configs` from `feat/total-service`.

Needs the author's answer on the number of receiving vertices 
(Step 0). Stop if it is missing.

Change.
- `configs/medium_putaway/`, four files, each its namesake in `configs/medium_arrival/` with
  - `num_receiving_vertices` in the `instance` section, the author's value,
  - `receiving: receiving` and `putaway: robots` in the `arrival` section (add `putaway` to
    `ArrivalSettings` in `training/spec.py`, passed to `stock_putaway`),
  - a header comment in the style of the arrival configs, saying what differs.
- No other config changes.

Test.
- Every file builds a study, and its instance is well-formed with the receiving vertices on row
  0.
- Each differs from its `medium_arrival` namesake only in those fields, in the style of
  `test_an_arrival_config_differs_from_its_medium_namesake_in_the_stock_only`.
- One Token Passing episode of 300 steps under every storage rule runs, delivers at least one
  put-away, and keeps the four correctness checks.

---

## P6. The Token Passing runner

Branch `feat/load-sweep` from `feat/putaway-configs`. This is W3 of
`code_changes_plan_2026-10-19.md`, moved here, with the shelf spread of W1 folded in.

`examples/05_full_comparison.py` sweeps loads but on example 04's instance, not on a training
spec, so it cannot read the new configs.

Change.
- `scripts/load_sweep.py --config <spec.yaml> --rates 0.1 0.2 ... --seeds N --storage-modes
  fixed demand congestion --out DIR`. Token Passing on the spec's instance and stock model,
  the test seeds of the spec's seed split, one episode per (rule, rate, seed). One JSON row per
  episode with the `RunMetrics` fields, into `DIR/load_sweep.jsonl`. Started again, it skips
  rows already written.
- `DIR/summary.md`.
  - At the top, the trip distance $d^{\mathrm{trip}}(v)$ of every storage vertex, smallest,
    largest and their ratio.
  - Per rule and rate, the mean over seeds of throughput, completed share, backlog slope,
    longest stand-still, total service time (both versions), mean pick service time, put-aways
    per arrival and their mean service time, put-away distance and unplaced units.
  - The capacity per rule, the highest mean throughput over the rates, and the arrival rate at
    0.6 of it.
  - No `chi_max` or stall length is chosen. The author reads them off the table.

Test. A two-rate, one-seed, one-rule sweep on a `medium_putaway` config writes two rows and a
summary, and a second start writes nothing new.

## 7 Fix the examples that now miss the nodes that has been implemented.

---



## After P6, for the author

1. **Token Passing test.** Run `scripts/load_sweep.py` on `configs/medium_putaway/` under all
   three rules over a range of rates. Check the model behaves: put-aways get delivered, lines
   wait for stock on its way and then get served, shelves stay within capacity, the backlog
   saw-tooth settles at low load. Read the capacity, `chi_max` and the stall length, and
   compare the two totals.
2. **Choose the main load** at 0.6 of capacity and set `arrival_rate`, `backlog_slope_max` and
   `stall_length` in `configs/medium_putaway/`.
3. **Train one arm** on the complete system, as a pilot before the long run (decentralised is
   the fastest).
4. Then W2 of `code_changes_plan_2026-10-19.md`, the larger warehouses, with the receiving
   vertex count scaled with the rest.


