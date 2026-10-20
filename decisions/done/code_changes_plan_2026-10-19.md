# Plan: code for `[A43]` to `[A46]` (costs, relative gain, keep-up, order lines)

**Status 2026-10-19. Steps 1 to 8 done, merged into `main` as #178 to #186 (step 5 merged last, as #186).** Only the gated step G2 is left.

Earlier status: The arrival stack (PR G to J, #175 to #177) and the RLlib clean-up are on `main` (`6a3aedd`), so step 0 passes. Steps 1 to 8 are agreed thesis changes. Step G2 at the end waits for the author's decision and must not be started before it.

One spec per step, for an implementing session (Sonnet 5.5 or similar). Work through the steps
**in order**, **one per session**, and stop after each one. The session makes the change in a
git worktree and reports the worktree's path. The author runs the checks, commits, pushes and
opens the PR.

The thesis text for these changes is in the local working copy of `thesis/`, uncommitted, tagged
`% [A43]`, `% [A44]` and `% [A45]`. The rationale is in the matching entries of
`thesis-progress/decisions/GAPS.md`. The planning context is `thesis-progress/decisions/active/thesis_plan.md`.

---

## Rules for every run (read first)

### Setup

1. Read `AGENTS.md` and `CLAUDE.md` at the workspace root, then
   `slap-mapd-coupling/AGENTS.md` and `slap-mapd-coupling/CLAUDE.md`.
2. Read the thesis sections the step names with `python3 thesis_section.py <label> ...`, run
   from the workspace root. The new text is uncommitted in `thesis/`, so **don't pull
   `thesis/`**. Read it as it is. The thesis is the source of truth. If the step and the
   thesis disagree, stop and report it.
3. Work in a new git worktree, never in the author's checkout of `slap-mapd-coupling`, which
   may hold uncommitted work. Don't run `git checkout`, `git stash`, `git reset` or
   `git pull` there. Step 1 starts from `origin/main`. Every later step starts from
   `origin/<previous step's branch>`, which the author has committed and pushed, so the PRs
   stack. If that remote branch does not exist yet, stop and report it.

   ```
   git -C slap-mapd-coupling fetch origin
   git -C slap-mapd-coupling worktree add <scratchpad>/<branch> -b <branch> <base>
   ```

   Work only inside the worktree, with `PYTHONPATH=<worktree>/src PYTHONDONTWRITEBYTECODE=1`.

### Hand-off

- **Leave the changes uncommitted in the worktree.** Don't commit, don't push, and don't run
  pytest, black, flake8 or mypy. The author runs the checks, commits, pushes and opens the PR.
- **Don't touch GitHub.** No issues, comments or PRs.
- **The final reply is the worktree's path.** Leave the worktree in place. If the step stopped
  early, add one line saying why.

### Hard limits

- Never edit anything in `thesis/` or `thesis-progress/`.
- **Keep the step small.** Stop and report, without coding around it, if
  - the thesis and this plan disagree,
  - a step needs a file this plan does not list, or a new design choice,
  - a stored checkpoint or test fixture would have to be regenerated.
- **Don't invent values.** A value the thesis marks TBD becomes a config field with default
  `None` and a comment saying it is TBD. Don't pick a number.
- The four correctness checks of `slap-mapd-coupling/AGENTS.md` (no vertex or swap conflicts,
  capacity respected, one lifecycle set per task, bit-for-bit replay) must still hold.

### Writing in code

- **Cite equations by name, never by label.** Write "the keep-up check", not
  `eq:throughput`. The names are in `thesis/styles/eqnames.tex`. Section and table labels
  (`sec:...`, `tab:...`) stay.
- **Symbols follow `thesis/Chapters/2.Notation.tex`.**
- **Shorten docstrings you touch.** Don't rewrite files the step doesn't list.
- **UK spelling** (behaviour, organise, colour).
- Write a test that fails without the change, next to the code it tests.
- RLlib's new API stack only, as `slap-mapd-coupling/AGENTS.md` says. None of these steps
  should need to touch `training/`.

---

## Step 0. Precondition, no code

The evaluator changes of steps 3 to 5 sit on top of the arrival model (PR G to J,
branches `feat/arrival-config`, `feat/arrival-stock`, `feat/arrival-rules`,
`feat/arrival-eval`). Check that `origin/main` contains them, for example that
`ExperimentConfig` has a `stock_model` field and `RunMetrics` has `mean_putaway_distance`.
If it does not, **stop and report** that the arrival stack must be merged first. Do not
base the work on the arrival branches yourself.

---

## Step 1. Unit edge costs and the new wait cost (`[A43]`, part 1)

Branch `feat/unit-edge-costs` from `origin/main`.

Thesis: `python3 thesis_section.py sec:impl:instances sec:method:rl`. Read the `[A43]`
sentence in `sec:impl:instances` and the `tab:rlparams` rows.

What the thesis says. Every edge of a generated instance costs 1. The wait cost
`c_wait` is 0.2, after van Knippenberg et al. (2021).

Change.
- Every config under `configs/` (including `configs/medium/` and `configs/medium_arrival/`)
  and every example or script that sets `random_edge_costs: true` sets it to `false`, with
  `default_edge_cost: 1.0`. Find them with `grep -rn random_edge_costs`.
- Every `wait_cost: 0.1` in those files becomes `0.2`. Keep the existing comment that one
  value serves the graph and the reward, and add "after van Knippenberg et al. (2021)".
- No change to `instances/generator.py` itself. The option stays for other uses.

Test. A test that builds the medium arrival instance from its config and asserts every edge
costs 1 and `wait_cost` is 0.2.

Stop if a test fixture or stored instance depends on the random costs and would need to be
regenerated.

---

## Step 2. The move cost in the reward (`[A43]`, part 2)

Branch `feat/move-cost` from `feat/unit-edge-costs`.

Thesis: `python3 thesis_section.py sec:method:rl`. Read the reward and the `[A43]` paragraph
after the `[A30]` paragraph.

What the thesis says. The reward gains the term `- c_move * 1[a_i moves at t]`. Every move pays
`c_move`, whether the agent serves a task or not. `c_move` is 0.1.

Change.
- `core/experiment_config.py`. A field `move_cost: NonNegativeFloat | None = None`, next to
  `deliver_reward` and `override_penalty`, required wherever those two are required (see the
  validator that lists them).
- `environment/reward_function.py`. A `move` term, `-move_cost * moved`, in the reward terms
  and their sum, logged as a sixth key next to the existing five. `moved` is 1 when the
  agent's realised position at `t+1` differs from its position at `t`. A move that conflict
  resolution turned into a wait is not a move.
- `environment/multi_agent_env.py`. Pass `moved` and `move_cost` where the reward is built
  (around the place `stood_still` is computed).
- Every config that sets `deliver_reward` sets `move_cost: 0.1`, with the comment
  "c_move, after van Knippenberg et al. (2021)".

Test. One agent that moves, one that chooses to wait and one that is overridden. Only the
first pays `move_cost`. The sum of the six terms equals the reward.

Stop if existing checkpoints would fail to load. They should not, since the observation is
unchanged.

---

## Step 3. The keep-up check against released tasks, with the backlog slope (`[A45]`, part 1)

Branch `feat/keep-up-slope` from `feat/move-cost`.

Thesis: `python3 thesis_section.py sec:pf:measures sec:impl:logging`. Read the "Keeping up"
paragraph, the keep-up check, `tab:measures` and `tab:evalparams`.

What the thesis says. A run keeps up if it finishes at least `f_up` of the tasks released in
that run, `|C_T| / (|C_T| + B_T) >= f_up`, and the slope `chi_T` of a least-squares line through
`B_t` over the second half of the run, `T/2 <= t <= T`, is at most `chi_max`. `f_up` is 0.8 and
`chi_max` is TBD. Throughput `Lambda_T = |C_T| / T` stays a reported measure.

Change.
- `core/experiment_config.py`. A field `backlog_slope_max: float | None = None` (chi_max,
  TBD, set from the Token Passing load sweep), next to `keep_up_threshold`.
- `evaluation/metrics.py`. New fields `completed_share` (`|C_T| / (|C_T| + B_T)`) and
  `backlog_slope` (chi_T, per timestep). `keeps_up` is `None` unless both thresholds are set,
  and otherwise both conditions. Keep `keep_up_ratio` with its comment changed to say it is
  throughput over the nominal rate and no longer the check.
- `evaluation/evaluator.py`. Compute both from `env.log.backlog_by_t` and the completed count.
  Fit the slope with plain least squares (numpy is fine).
- `training/evaluate_run.py` and `viz/study_report.py` only if they read `keeps_up` in a way
  that breaks. Do not change how they summarise otherwise.

Test. A synthetic backlog trace that levels off passes, one that grows linearly fails, and one
that jumps once and then stays flat passes. A run where 336 of 378 released tasks finish has
`completed_share` 336/378.

---

## Step 4. Stalls (`[A45]`, part 2)

Branch `feat/stall-count` from `feat/keep-up-slope`.

Thesis: `python3 thesis_section.py sec:pf:measures sec:impl:logging`. Read the paragraph on
a fleet that jams and catches up, and the stall row of `tab:evalparams`.

What the thesis says. An episode in which an agent holding a task stands still longer than
the stall length is counted as a stall. The number of such episodes is reported per
controller. The stall length is TBD.

Change.
- `environment/multi_agent_env.py`. In the log, keep for each task the longest run of
  consecutive blocked ticks, next to `blocked_ticks_by_task` (the same place
  `record_blocked_tick` is called). A tick that is not blocked ends the run.
- `core/experiment_config.py`. A field `stall_length: PositiveInt | None = None` (TBD).
- `evaluation/metrics.py`. Fields `longest_stand_still` (the longest run over all tasks, also
  tasks still active at the horizon) and `stalled: bool | None` (`None` when `stall_length`
  is unset).
- `evaluation/evaluator.py`. Fill both.

Test. A hand-built episode, or a unit test of the log, where one task is blocked for 3, then
moves, then is blocked for 5 ticks. The longest run is 5.

Stop if keeping the run length would change the replay of any existing test.

---

## Step 5. The relative gain (`[A44]`)

Branch `feat/relative-gain` from `feat/stall-count`.

Thesis: `python3 thesis_section.py sec:pf:measures`. Read the paragraph after the gain test
and the relative gain.

What the thesis says. Between controllers the gain is compared as a share of route time under
fixed storage. Per seed, `gain_n / (mean travel + mean blocked time of the fixed-storage run)`,
with its 95% interval over seeds, as in the gain test.

Change.
- `evaluation/comparison.py`. `PairedComparison` gains `mean_relative_gain`,
  `relative_ci_low` and `relative_ci_high`, computed with the same interval helper as the gain,
  from the fixed run's `mean_travel_time + mean_blocked_time` on each seed. Only for the
  service-time comparison, and only where the gain itself is computed.
- `training/evaluate_run.py`. One more column in the summary table, the relative gain with its
  interval.

Test. Two seeds with known fixed-storage travel and blocked times and known gains give the
expected relative gain and interval.

---

## Steps 6 to 8. Orders with several lines and amounts (`[A46]`, agreed and in the thesis)

Thesis: `python3 thesis_section.py sec:pf:tasks sec:pf:storage sec:pf:measures sec:impl:instances sec:impl:logging`.
Read every passage tagged `% [A46]`, the pickup rule, the arrivals, the estimates and the order
completion time.

What the thesis says, in short. An order is several order lines, each a SKU and a quantity.
All lines share the order's release time and delivery vertex. A line takes its units from the
shelves nearest the delivery vertex first. If the nearest holder has enough, the line is one
task. Otherwise it takes what that holder has, then the rest from the next nearest, and every
holder it takes from is one task carrying `q_j` units. Units no holder has wait for stock, and
become tasks when stock arrives, with the order's release time. `rho_hat_t(k)` counts lines,
and a second estimate `rho_hat^unit_t(k)` counts units and drives the fill level of the
arrivals. Waiting lines add the units they still miss. Order completion time is the longest
service time among an order's tasks. Lines per order have mean 5 (distribution TBD). Units per
line are uniform on 1 to 5. `lambda_task` is order lines per timestep.

Applies under `stock_model: arrival` only. Under `template` nothing changes, so earlier runs
replay. With the new config fields unset, an order is one line of one unit, today's behaviour.

### Step 6. Order lines in the order stream

Branch `feat/order-lines` from `feat/relative-gain`.

- `core/experiment_config.py`. Fields `lines_per_order` (the distribution and its mean, no
  default, `None` meaning one line, TBD in the thesis) and `units_per_line` (an inclusive
  range, `None` meaning 1). Reject them under the template model.
- `core/tasks.py`. `Task` gains `quantity` (`q_j`, default 1), `order_id` and `line_index`.
- `environment/multi_agent_env.py`. The arrival-model order path (the one that draws
  `poisson(self.config.arrival_rate)` for the arrival model) draws orders with mean
  `arrival_rate / mean lines`, so `arrival_rate` stays lines per timestep. Each order draws its
  line count, then that many distinct SKUs from the Zipf weights without replacement, one
  delivery vertex, and a quantity per line, all from the order RNG and never from stock. The
  `Order` record becomes a line record with order id, line index, SKU, quantity still missing
  and delivery vertex.

Test. With a fixed seed the stream is identical under fixed and demand storage. Lines of one
order share release time and delivery vertex. SKUs within an order are distinct. The mean
number of lines per timestep is close to `arrival_rate` over a long stream.

Stop if the template-model path would change.

### Step 7. The pickup rule over several shelves, and arrivals in units

Branch `feat/line-pickup` from `feat/order-lines`.

- `environment/multi_agent_env.py`. The pickup rule as the thesis states it, holders ordered
  by distance to the delivery vertex with ties by vertex id, one task per holder used, each
  taking `min(missing, held)` units. The remainder stays as a waiting line and is served the
  same way when stock arrives. The backlog counts waiting lines.
- `core/tasks.py`. The stock condition checks `x >= quantity`.
- `environment/storage_estimates.py`. Add the unit estimate next to `rho_hat`, which now
  counts lines.
- `storage/arrival.py`. The fill level uses units ordered, and waiting lines add their missing
  units. Placement order (`_by_demand`) keeps using `rho_hat`, the line count.
- `training/spec.py`. `demand_sized_blocks` sizes the starting stock in units, using the mean
  of `units_per_line` from the config, not a constant.

Test. Hand-built stock of 1 unit at the nearer shelf and 5 at the further one. A line for 4
units gives two tasks, 1 and 3 units. A line for 7 gives two tasks and leaves 1 unit waiting.
The four correctness checks still pass, including capacity and replay.

### Step 8. Order completion time and tasks per line

Branch `feat/order-metrics` from `feat/line-pickup`.

- `environment/multi_agent_env.py`. Log the order and line of every task.
- `evaluation/metrics.py`. `mean_order_completion` (the order completion time, mean over
  orders whose tasks are all completed), `num_completed_orders`, `mean_tasks_per_line` and
  `num_lines_waited` (lines that waited for stock).
- `evaluation/evaluator.py`. Fill them.
- `training/evaluate_run.py`. One summary column, the order completion time under each rule.

Test. An order with two lines finishing at 10 and 14, released at 2, has completion time 12.

## Follow-up for the author, not a coding session

- **Token Passing load sweep** (specified as W1 to W3 below), after step 8 since order lines make arrivals burstier, on every warehouse (8, 16, 32 and 64 agents). It gives the
  capacity of each warehouse, so the main load (0.6 of capacity) becomes an arrival rate, and
  the healthy backlog slopes give `chi_max`.
- **Stall length**, read from the same sweep and the arrival run's jammed seed.
- **Retraining.** Steps 1 and 2 change the reward and the edge costs, so every policy is
  trained again. That is the long run.

---

## G2. A measure of cold stock on prime shelves (done 2026-10-19, uncommitted)

Definitions agreed 2026-10-19. A SKU is cold when it is outside the top `k` of the current
popularity ranking, `k = 10`. The prime shelves are the storage vertices nearest the delivery
vertices on average (the order the starting placement fills them in), as many as hold the top
`k` SKUs when each holds `ceil(|K| / |V_str|)` of them. On the 8-agent warehouse (100 SKUs, 10
shelves) that is one shelf.

Built in the worktree `feat/cold-stock` from `origin/main`. Evaluation only, so replay and
checkpoints are unchanged.
- `ExperimentConfig.cold_stock_top_k` and `ArrivalSettings.cold_stock_top_k`, arrival model
  only, `None` leaves the measure off. Set to 10 in `configs/medium_arrival/`.
- `RunMetrics.mean_cold_prime_share`, the share of the prime shelves' capacity holding cold
  SKUs after each arrival, averaged over arrivals.
- `RunMetrics.mean_unit_age_at_pick`, the steps a unit sat on its shelf before it was taken.
  A shelf gives up its oldest units first. Starting stock arrived at `t = 0`.
- Also fixes `test_an_arrival_config_differs_from_its_medium_namesake_in_the_stock_only`,
  which fails on `main` since step 6 added two fields to the `arrival` section.

Not in the thesis yet. It needs a sentence in `sec:pf:measures` and a row in `tab:measures`.

---

## Warehouses for 16, 32 and 64 agents, and the Token Passing load sweep

**Updated 2026-10-19.** `[A47]` (robots carry the put-away) comes first, as P1 to P6 of
`putaway_code_plan_2026-10-19.md`. W3 moved there as P6, with W1's shelf spread folded in, now
measured as the trip distance. Only W2 is left here, and it follows the pilot training run.
W2's table also needs a receiving vertex count per size, scaled like the rest.

The sweep gives each warehouse's capacity, so the main load (0.6 of capacity) becomes an
arrival rate. The same runs give `chi_max` and the stall length. Three steps, in order, each
from the previous step's branch.

### Decided 2026-10-19. The delivery vertices stay at random

The generator gives the storage, delivery and parking roles to random vertices
(`instances/generator.py`, stage 3), as Ma et al. (2017) draw pickup and delivery locations
at random. The thesis is changed to say so (`[A47]`, drafted, waiting for the author). The
cost is that a larger warehouse may have a smaller gap between near and far shelves, so the
gap is measured on every size.

### W1. The spread of shelf distances, per warehouse

Branch `feat/shelf-spread` from `origin/main` (or from `feat/cold-stock` once it is pushed).

- `instances/` (next to the generator, not in it). A function that, for an instance, returns
  each storage vertex's mean distance to the delivery vertices, and the ratio of the largest
  to the smallest.
- `scripts/load_sweep.py` (W3) prints it at the top of `summary.md`. Until W3 exists, a small
  `scripts/shelf_spread.py --config <spec.yaml>` prints it.

Test. On the 8-agent arrival config the mean distances run from 4 to 11 edges.

### W2. Configs for 16, 32 and 64 agents

Branch `feat/large-warehouses` from W1's branch.

`thesis_plan.md` (section 4.3) mentions instances for 12 and 16 agents (178 and 221 vertices)
that are not in `configs/` on `main`. Find their generator values first, and use them for 16
agents if they exist.

Scaling rule, to be confirmed by the author. Everything per agent stays as on the 8-agent
warehouse, so about 12 vertices, 1.25 shelves and 0.5 delivery vertices per agent. The SKU
count stays at 100, so the popularity law is the same on every size.

| agents | vertices (about) | storage vertices | delivery vertices |
|---|---|---|---|
| 8 | 94 | 10 | 4 |
| 16 | 190 | 20 | 8 |
| 32 | 380 | 40 | 16 |
| 64 | 750 | 80 | 32 |

- `configs/arrival_16/`, `configs/arrival_32/`, `configs/arrival_64/`, each a copy of
  `configs/medium_arrival/` with `num_agents`, the `instance` section and `arrival_rate` changed.
  `arrival_rate` stays a placeholder with the comment "set from the Token Passing load sweep".
  `max_num_aisles` and `max_aisle_length` grow until the instance reaches the vertex count.
- `num_zones` of the section arm scales with the fleet, about 3 agents per zone (`p = 3` at 8
  agents), so 5, 11 and 21. TBD in the thesis, so mark it as such.
- Stop if no seed gives a well-formed instance within the generator's attempt limit.

Test. Each config builds a study, the instance is well-formed, and its vertex count is within
15% of the table.

### W3. The load sweep script

Branch `feat/load-sweep` from W2's branch.

`examples/05_full_comparison.py` sweeps loads, but on example 04's instance, not on a training
spec, so it cannot read the arrival configs.

- `scripts/load_sweep.py --config <spec.yaml> --rates 0.1 0.2 ... --seeds N --out DIR`. Token
  Passing under fixed storage on the spec's instance and arrival model, the test seeds of the
  spec's seed split, one episode per (rate, seed). One JSON row per episode with the
  `RunMetrics` fields, into `DIR/load_sweep.jsonl`, and started again it skips rows already
  written.
- `DIR/summary.md`. Per rate, the mean over seeds of throughput, completed share, backlog
  slope and longest stand-still. The capacity is the highest mean throughput over the rates,
  and the arrival rate at 0.6 of it. No `chi_max` or stall length is chosen. The author reads
  them off the table.

Test. A two-rate, one-seed sweep on the 8-agent config writes two rows and a summary, and a
second start writes nothing new.

After W3 the author runs the sweep on every size, fills in `arrival_rate`, `chi_max`
(`backlog_slope_max`) and `stall_length`, and starts the retraining.

---

## Make sure that all the images is up to date with the coding plan and how it have been changed. 
images located in /thesis-progress/scripts/images