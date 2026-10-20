# Plan: adaptive storage, implemented completely

Written 2026-10-17. Replaces the task list of `thesis-progress/decisions/done/adaptive_storage_plan.md`
(2026-10-14), which predates the real centralised arm, the `slap-mapd train` command and the
8-agent warehouse. That file's background and author decisions still hold where this one does
not override them.

Status: **approved by the author on 2026-10-17.** PR A (#170), PR B (#171) and PR C (#172) merged, each reproducing the probe exactly under Token Passing. PR D (`~/worktrees/feat-storage-spec`) and PR E (`~/worktrees/feat-relocation-cost`) done and uncommitted, independent of each other, mergeable in either order. PR F waits for the author's decision on #19.

## 0. Read this first (every agent, every PR)

Read, in order: `CLAUDE.md`, `AGENTS.md`, `SESSION_CONTEXT.md` at
`/home/bjarkek/Documents/thesis`, then this file. English, UK spelling.
Code repo: `/home/bjarkek/Documents/thesis/slap-mapd-coupling`.

Working rules:
- **One PR at a time, in the order of section 3.** Do exactly that PR. Report and stop.
- **Work in a git worktree** under `~/worktrees/<branch>`, created from the branch named as the
  PR's base. Never work in the main checkout. It carries the author's unstaged edits
  (`.gitignore`, `examples/04_decentralised_training.py`).
- **Leave the change uncommitted.** No commits, no push, no `gh` calls, no PRs. The author
  commits and opens the PR. Report the worktree path and a short list of what changed.
- **Tests.** Write the tests the PR lists. Run only the test files you changed or added, with
  `PYTHONPATH=src ~/.venvs/rl/bin/python -m pytest <files> -q --no-cov -p no:cacheprovider`
  from the worktree. `PYTHONPATH=src` matters, because the venv's editable install points at
  the main checkout. Never the full suite. It takes 25 minutes, and 123 of its tests failed
  on `fix/sample-timeout`. At least some of those already fail on `main`, and the rest are not
  sorted yet. Run `black` and `flake8` on the files you changed.
- **No training, no long simulations.** A test episode is at most a few hundred steps.
- **Do not edit the thesis.** Where a PR needs thesis wording, the coordinator writes it.
- **Do not invent values the thesis leaves open.** New study parameters get no default, or a
  default that reproduces today's behaviour exactly, as each PR says.
- In code and docstrings, cite thesis equations by name ("the storage update"), not by `eq:`
  label. Check `thesis/Chapters/2.Notation.tex` before naming a symbol in a docstring.
- Keep `slap-mapd-coupling` cloneable on its own. No references to sibling folders.
- If something in this plan contradicts the code you find, or a choice is not covered, stop and
  ask. Do not guess.

## 1. Goal

Make adaptive storage a complete part of the study, so that a run can train and be evaluated
under fixed, demand and congestion storage on the same order stream, with skewed and drifting
demand. RQ1 (does adaptive storage shorten service time) and RQ2 (does that effect differ by
controller) then have an answer. RQ3's congestion rule waits for a separate decision (PR F).

## 2. What is decided, and the evidence

Decided by the author on 2026-10-17, from the demand probe (`~/thesis_runs/demand_probe/`):

| setting | test value | code name |
|---|---|---|
| SKU popularity | Zipf, weight of rank r is `1 / (r + 1)^skew` | `demand_skew` |
| skew | 1 | |
| ranking drift | rotates by `shift` places every `period` steps | `demand_rotation_period`, `demand_rotation_shift` |
| period, shift | 200, 5 | |
| SKUs | 100, 8 units each | `storage.num_skus`, `storage.initial_units` |
| vertex capacity | 200 | `storage.vertex_capacity` |
| starting stock | blocks: most popular SKUs at the storage vertices nearest the delivery vertices | `storage.initial_placement: demand_blocks` |
| storage update | Δ = 100, ν = 48, β 3 and 10 | |
| load | 0.3 (service time readable) and 0.6 (throughput) | |

These are illustrative test values, not thesis values. They go in the new config set (PR D),
never as code defaults.

Measured in the probe (Token Passing and the night's two decentralised policies, 4 seeds):
- With rotation, fixed storage loses about 15% throughput and the demand rule wins it back.
  Without rotation the gain is near zero, so uniform or fixed-skew demand leaves RQ1 empty.
- At load 0.3 the demand rule cuts service time from 54.1 to 39.4 (Token Passing), from 32.1 to
  13.3 and from 25.1 to 14.0 (the two decentralised policies).
- The effect is larger for the learned arm than for Token Passing.
- The congestion rules did not beat the demand rule clearly, see PR F.

Also decided earlier (`adaptive_storage_plan.md` section 2): the same starting stock for every
storage rule, and the wait rule of PR C.

## 3. The PRs

The stack, each branch based on the one above it:

```
main (4728f14, with #168 sample timeout and #169 seed scheme merged)
 └ feat/demand-model          PR A  Opus
    └ feat/initial-placement  PR B  Opus
       └ feat/wait-attribution PR C Opus
          └ feat/storage-spec  PR D  Sonnet
             └ feat/relocation-cost PR E Sonnet
```

PR A starts from `origin/main` (fetch first). Each later PR starts from the worktree branch of
the PR above it, even though that branch is uncommitted: create the new worktree from the
parent branch and apply the parent's uncommitted diff (`git -C <parent worktree> diff | git
apply`), or wait until the author has committed the parent. Say which you did.

---

### PR A. Demand model (Opus) — `feat/demand-model`

Thesis: `sec:pf:tasks` (the order distribution `P_ord`) and `tab:evalparams`. Wording by the
coordinator, the PR lands after it is approved.

1. `core/experiment_config.py`. Three new fields:
   - `demand_skew: NonNegativeFloat | None = None`. None means today's uniform draw.
   - `demand_rotation_period: PositiveInt | None = None`. None means no rotation.
   - `demand_rotation_shift: PositiveInt | None = None`.
   Validators: a period needs a skew and a shift, and a shift needs a period.
2. `environment/multi_agent_env.py`, `_generate_tasks`.
   - **With `demand_skew` None, keep today's code path unchanged**, so every existing replay and
     test is bit for bit the same.
   - With a skew, the random numbers drawn stay exactly as today: one Poisson count, then three
     uniform numbers per order. Only the mapping of the SKU number changes. This keeps the order
     stream independent of storage, which pairing needs (`sec:impl:instances`).
   - The ranking at step `t` (the release step, `self._t`): the SKUs in id order, rotated left by
     `(t // period) * shift` places (mod the number of SKUs), or not rotated without a period.
     Rank 0 is the most popular.
   - Weights `1 / (r + 1)^skew` over all SKUs. Keep only the SKUs in stock (the stock
     condition), renormalise, and map the SKU number `u` through the cumulative weights with
     `bisect_right`, clipped to the last index. Pickup and delivery are drawn as today.
   - This must match the probe's `patch_order_draw` in
     `~/thesis_runs/demand_probe/demand_probe.py` exactly. Read it.
3. `training/spec.py`.
   - SKU names get three digits, `f"sku_{i:03d}"`, so id order is numeric order past 100.
   - A new optional section `demand: DemandSettings | None = None` with `skew`,
     `rotation_period`, `rotation_shift` (same validation), passed into
     `build_experiment_config`. Shipped configs stay uniform (no section).
4. Tests (new file `tests/unit/test_demand_model.py`):
   - with no skew, the orders of a seed are identical to `main`'s (same `(t, sku, pickup,
     delivery)` for 300 steps);
   - with skew and rotation, the released orders `(t, sku, delivery)` of a seed are identical
     under fixed and demand storage, while pickups may differ;
   - the most popular SKU changes exactly at multiples of the period, by the shift;
   - over a long run the SKU shares follow the Zipf weights within a tolerance;
   - the validators.

### PR B. Starting stock from expected demand (Opus) — `feat/initial-placement`

Thesis: `sec:impl:instances` (how `x_0` is built). Wording by the coordinator.

1. `training/spec.py`, `StorageSettings`: new field
   `initial_placement: Literal["by_number", "demand_blocks"] = "by_number"`. `by_number` is
   today's rule (SKU i at storage vertex i mod |V_str|), so every shipped config is unchanged.
2. `demand_blocks`:
   - storage vertices ranked by their **mean** `d_G(v, g)` over the delivery vertices, ties by
     vertex id (orders pick a delivery vertex uniformly, so the mean is the expected leg);
   - SKUs in popularity rank at `t = 0` (id order when there is no `demand` section);
   - block size `ceil(num_skus / |V_str|)`, the SKU at rank r goes to vertex number
     `r // block`, all its units;
   - raise `ValueError` if a vertex overflows its capacity, like `build_storage` does today.
   - Must match the probe's `place_by_popularity(..., "blocks")`.
3. The starting stock is built once in `build_study` and is the same for every storage rule.
4. Tests: the placement on a small instance, the same counts under every
   `evaluation_storage_mode`, overflow raises, `by_number` unchanged.

**Acceptance by the coordinator after PR B:** Token Passing episodes with the test values
(100 SKUs, blocks, skew 1, period 200, shift 5, Δ 100, ν 48, loads 0.3 and 0.6, seeds 200 000
to 200 003, horizon 2000) under fixed and demand storage must reproduce the probe's rows in
`~/thesis_runs/demand_probe/v2/rows.jsonl` exactly.

### PR C. How waits are attributed to an edge (Opus) — `feat/wait-attribution`

Thesis: `thesis-progress/decisions/decision_log.md` #21, a Method sentence by the coordinator.

1. `environment/multi_agent_env.py`, stage 5 of `step`. For every step where a robot serving a
   task stands still (exactly the steps that call `record_blocked_tick` today), charge one wait
   to the edge `(at, w*)`, where `at` is where it stands and
   `w* = argmin over out-neighbours w of c(at, w) + d_G(w, goal)`, ties by vertex id. The goal
   is the task's delivery vertex if `pickup_time` is set after the lifecycle update, else its
   pickup vertex. No wait is charged when `at` is the goal.
2. This replaces today's rule, which charges only overridden moves, to the intended move's edge.
   An overridden robot is charged by the new rule like any other standing robot, and idle robots
   are never charged (decided, section 5).
3. Update the docstring of `environment/storage_estimates.py` (lines 24 to 30).
4. Tests: under Token Passing the wait estimate is not always 0 when robots delay (task T8 of
   the old plan); the charged edge is the next one on the shortest route; a robot at its goal
   and an idle robot are not charged; a wait lands in the window of the step it happens in.

**Acceptance by the coordinator after PR C:** Token Passing under today's congestion score at
β = 3 reproduces the probe's clean `congestion` rows (Token Passing is never overridden, so the
probe and the repo agree there).

### PR D. Storage settings in the spec, evaluation under several rules, the config set (Sonnet) — `feat/storage-spec`

1. `training/spec.py`: a new optional section `storage_rule` with `epoch_length` (Δ),
   `reassignment_cap` (ν) and `congestion_weight` (β, optional), no defaults.
   `build_experiment_config` passes them when the storage mode is not fixed. A `matched` regime
   with a non-fixed `evaluation_storage_mode` requires the section, and the error says so.
2. `slap-mapd evaluate RUN_DIR --storage-modes fixed demand congestion` (the command from
   `feat/seed-scheme`). The checkpoint is still chosen on the validation seeds under the run's
   own evaluation storage mode. The chosen and the last checkpoint then play the test seeds
   under every listed mode. Rows carry `storage_mode`, and a `summary.md` gives, per adaptive
   mode, `evaluation/comparison.py::compare_paired` against fixed. A mode needing Δ, ν or β
   takes them from the spec's `storage_rule` section, or the command fails with a clear message.
3. `configs/medium/{decentralised,centralised,section,full_view}.yaml`: the 8-agent warehouse
   of the night of 2026-10-16 (the `instance` section of
   `~/thesis_runs/night_2026-10-16/configs/decentralised.yaml`), with the test values of
   section 2, arrival rate 0.6, horizon 2000, budget 500 000, a checkpoint every 3 iterations,
   every one kept, and `train_seed_count: 100` (the author's choice, so a run trains on 100
   order streams, not 5). Copy every other value from the matching shipped config. The header
   says the values are illustrative.
4. Tests: spec validation, `build_experiment_config` under each mode, the evaluate rows and
   summary with a fake episode (as in `tests/unit/test_evaluate_run.py`), and every
   `configs/medium/*.yaml` loads and builds a study.

### PR E. Relocation cost measure (Sonnet) — `feat/relocation-cost`

Relocation is instant and free in the simulator (stage 6 swaps the placement). This PR only
reports what it would cost, so the adaptive gain can be read next to it.

1. At every storage update, for each SKU, match the units that left a vertex to the units that
   arrived at another, cheapest pair first by `d_G(from, to)`, ties by vertex ids, and sum
   units times distance. Log it per update next to `relocated_units_by_update`.
2. `evaluation/metrics.py`: `mean_relocation_distance`, the mean over updates (0.0 without an
   update, like `mean_relocated_units`). Carry it into the evaluation rows.
3. Tests: a hand-made relocation with a known cost, 0 under fixed storage.

### PR F. The congestion rule (#19, #9, #10) — not in this hand-off

The clean rerun is in (`thesis-progress/decisions/done/demand_probe_2026-10-17.md`). Neither
`congestion_rho` (#19 option b) nor `congestion_v2` (option c) improved on today's score, and
today's score at β = 1 was the only congestion variant that helped. Waits for the author's
decision on #19, where option (a) (keep the score, reword K) is now the likely one. Then the
coordinator adds a PR here, if any code change is left.

## 4. The coordinator's part (this session)

- Draft the thesis wording for PR A (order distribution and its values), PR B (the starting
  stock), PR C (the wait sentence) and the open Method fixes #8, #10 and #20, following the
  writing rules of `CLAUDE.md`, and get approval before any PR lands. Each change gets a
  `% [Axx]` tag and a `thesis-progress/decisions/GAPS.md` entry. New symbols go in the notation
  table. The table already uses `s` and `P`, so skew and rotation period need other letters
  (suggested ε and T_rot).
- Launch each agent, check its worktree against this plan, and run the acceptance checks of
  PRs B and C against the probe.
- Record the probe results in `thesis-progress/decisions/done/demand_probe_2026-10-17.md`.

## 5. Decisions of the author (2026-10-17)

1. PR C: yes, the new wait rule also replaces how overridden moves are charged (to the next edge
   on the shortest route, not the intended edge), and idle robots are not charged.
2. PR B: yes, `F_dem` keeps ranking by the nearest delivery vertex until PR F. Only the starting
   stock uses the mean distance.
3. `train_seed_count: 100` in the medium configs.
4. Yes, agents run the tests of the files they change.
