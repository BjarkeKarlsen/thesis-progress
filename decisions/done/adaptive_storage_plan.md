# Plan: adaptive storage through the learned controllers and the campaign  - DONE

Written 2026-10-14. Local only, not in a repo. Written so that a fresh agent
(Sonnet 5.5, medium effort) can execute one task at a time without asking what
the plan meant. Nothing here has been run. Every value is a proposal until the
author sets it.

## 0. Read this first (applies to every task)

Start by reading, in order: `CLAUDE.md`, `AGENTS.md`, `SESSION_CONTEXT.md` at
`/home/bjarkek/Documents/thesis`. English, UK spelling. Code repo is
`/home/bjarkek/Documents/thesis/slap-mapd-coupling` (GitHub
`BjarkeKarlsen/slap-mapd-coupling`).

Working rules:
- **One task at a time.** Do exactly the task you are given. Do not start the
  next one. Report what you did and stop.
- **Do not run code that trains or simulates while another session is
  running.** Ask the author first. Unit tests of the files you changed are
  allowed once the author says no other session is running. Tasks marked
  `[RUN]` need that go-ahead.
- **No subagents** unless the author has agreed what each one does.
- **The author opens PRs.** Never run `gh pr create`. Push only when told.
  Give PR text in chat.
- `gh pr view` fails here. Use `gh api repos/BjarkeKarlsen/slap-mapd-coupling/...`
  and parse JSON with `python3 -I -c "import sys,json; ..."`, because
  `gh api` rejects `--jq`.
- Tests: only the files you changed, with
  `~/.venvs/rl/bin/python -m pytest <files> -q --no-cov -p no:cacheprovider`.
  Never the full suite. Run `black` and `flake8` on the files you change.
- Commits: only files you changed, with explicit paths
  (`git commit -- <paths>`), then `git show --stat HEAD` to check. The
  author has unstaged edits in `.gitignore` and `examples/00b_pygame_preview.py`.
  They must never go into your commits. Use the attribution line from the
  session's system reminder.
- **Do not invent values the thesis leaves open** (Δ, ν, β and others in
  `tab:storageparams`). Make them flags with no default, and flag them.
- **Do not edit the thesis.** If a thesis change is needed, write the proposed
  wording in chat and wait.
- Keep `slap-mapd-coupling` cloneable on its own. Do not reference sibling
  folders from inside it.
- Cite thesis equations by name, not by `eq:` label, in code and docstrings.
- Separate what is measured from what is inferred in every report.
- Before moving, deleting or restructuring files across repos, propose and wait.

When you are unsure whether something is the author's decision, it is. Stop
and ask. Section 4 lists the decisions that are the author's.

## 1. Goal

Make the storage rule a switch (fixed, demand, congestion) with its
parameters, in training, evaluation, the sweep and the campaign script. Then
build a demand model and a larger instance on which adaptive storage can be
compared with fixed storage under the same controllers and seeds. The plan
does not claim adaptive storage helps.

## 2. Decisions the author has taken

- Horizon `T` should be 2000 or more (it was 630, thesis tag `[A31]`). The
  keep-up threshold and load levels get re-measured. The author runs the
  keep-up trials.
- Task rate should reach about 0.4 tasks per step before keep-up is measured,
  so the fleet must be larger.
- The comparison must hold across architectures. One `T`, the same seeds and
  the same order stream for every arm and every storage mode.
- Starting stock `x_0` is placed once from expected demand, popular SKUs
  nearest the delivery vertices, the same `x_0` for every storage rule (#95).
- Waits attributed to an edge: a step where an agent serving a task stands
  still, charged to the next edge on its route to its target. Wording for
  `eq:estimates` is drafted in chat first, then the code.
- Δ, ν and β are swept from the campaign script, with no defaults, on a bigger
  warehouse with more agents.

## 3. Background an agent needs

State of the code on 2026-10-14 (read, not measured):
- `origin/main` was at `70828f8`. #154 (order stream independent of storage,
  closes #149), #155 (skip without orders, closes #148) and #156 (online
  estimates, closes #60) were open. Fixed against adaptive is only paired once
  #149 is on `main`.
- Orders pick a random (SKU, pickup vertex) among stocked pairs
  (`src/slap_mapd_coupling/environment/multi_agent_env.py`, around line 412),
  so they have no popularity and depend on storage until #154 lands.
- The storage update on `main` passes empty estimates `{}, {}, {}` (stage 6 of
  `multi_agent_env.py`) until #156 lands.
- The example 04 instance has 3 agents (`FLEET_SIZE`), 4 storage vertices, 1
  SKU. Adaptive storage cannot help there. It stays as the plumbing check.
- `ILLUSTRATIVE_BUDGET_ENV_STEPS` is 4200 in
  `examples/04_decentralised_training.py`, and an iteration samples one whole
  episode. That is about 2 episodes at T=2000.
- `/home/bjarkek/Documents/thesis/storage_mode_wip.patch` changes examples 04
  and 04b. It applies cleanly to `main` but is not green.

How adaptive storage works in one episode (thesis `sec:pf:coupling`): an
episode starts from `x_0`. The rule `F` runs at `t = Δ, 2Δ, ...` and sees only
the last Δ steps. Nothing carries over between episodes. There are at most
`floor(T/Δ)` updates. At T=2000, Δ of 50, 100, 200, 400 gives 40, 20, 10, 5.

The demand model (#94): each SKU has a share of demand (Zipf-like skew). Every
P steps the ranking rotates. The episode seed fixes when each order arrives and
which SKU it asks for, drawn from the popularity at that moment, so every
controller and storage rule sees the identical stream. No rule is told the
ranking. Without rotation `x_0` is already best and adaptive can only lose.

## 4. Decisions that are the author's (ask, never decide)

- Rotation period P, and whether it is fixed or swept.
- Skew exponent, number of SKUs, number of storage vertices, fleet size.
- Values of Δ, ν, β. Proposed sweep: Δ in {50, 100, 200, 400}, β in
  {0, 0.5, 1} where β=0 must reproduce the demand rule, ν sized once the
  instance is known.
- Training episodes at T=2000 for the matched regime and the training budget.
- Any thesis wording (`tab:evalparams`, `[A31]`, `eq:estimates`).
- Whether a skipped storage update counts as an update. The thesis already
  says it keeps `x_t = x_{t-Δ}` and counts as zero units moved. Log applied
  and skipped separately.

## 5. Tasks

Each task: precondition, steps, done when, stop and ask if.

### T0. Check the prerequisites (read-only)

Precondition: none.
Steps:
1. `git fetch origin`, then `git log origin/main --oneline | head`.
2. For PRs 154, 155, 156 call
   `gh api repos/BjarkeKarlsen/slap-mapd-coupling/pulls/<n>` and read `state`
   and `merged_at`.
Done when: you report, for each of the three, merged or not, and the
`origin/main` head.
Stop if any is not merged. Report and do nothing else. Tasks T2 to T6 need all
three on `main`.

### T1. [RUN] Measurements

Precondition: author confirms no other session is running.
Steps, each as a separate small run with its own output file:
1. Token Passing throughput against fleet size, fixed storage, a saturating
   arrival rate, 6 seeds, several fleet sizes the author names.
2. Keep-up share at `T=2000` for the arrival rates the author names, 6 seeds.
3. Seconds per training iteration at `T=2000`.
Done when: you give a table of measured numbers per run and say which are
measured and which are inferred.
Stop and ask if the author has not named the fleet sizes or rates.

### T2. Storage switch, tests first

Precondition: T0 passed. Branch `feat/storage-mode` from `origin/main`.
Steps:
1. `git apply --check ../storage_mode_wip.patch`, then apply it.
2. Rewrite
   `tests/unit/test_example_04_cli.py::test_matched_regime_trains_under_the_evaluation_storage_rule`
   for the new `storage` argument. It currently pins the removed constant
   `EVALUATION_STORAGE_MODE`.
3. Add tests for: every flag combination of `storage_problem` (fixed takes no
   parameters, demand needs epoch and cap, congestion also needs weight,
   demand takes no weight); `build_config` under regime `fixed_only` (always
   fixed) and `matched` (uses `storage`) for each mode; `evaluation_config`
   uses `storage`; example 04b takes the same flags and builds the same config
   as example 04.
4. Run the tests of the files you changed, black, flake8. Commit.
Done when: those tests pass and the commit stat shows only your files.

### T3. Sweep takes storage modes

Precondition: T2 done.
Steps in `examples/05_full_comparison.py`:
1. Add `--storage-modes` (a list, default `fixed`) and the three parameter
   flags with the same meaning as `example_04.add_storage_arguments`. No
   defaults for the parameters.
2. Loop every planner and checkpoint over every mode.
3. Each row gets `storage_mode`, the parameters used, and the full
   `metrics.model_dump(mode="json")` under `"metrics"`, so
   `evaluation/comparison.py::compare_paired` can be fed from the sweep file.
   The `condition` label stays the arm.
4. Update `tests/unit/test_example_05_sweep.py` and the docstring.
Done when: tests pass, and a test shows a row carries the mode, the
parameters and a `metrics` dict that `RunMetrics` can load.

### T4. Campaign script and report

Precondition: T3 done.
Steps:
1. `scripts/run_campaign.py`: add `--eval-storage-modes` and the three
   parameter flags, forwarded to the sweep stage only. Do not add training
   under adaptive storage.
2. `viz/study_report.py`: `sweep_stats` and the load figure group by storage
   mode as well as condition and rate, with labels like
   `centralised [demand]`.
3. Update `tests/unit/test_run_campaign.py`, and add a test that two modes of
   the same arm are not mixed.
Done when: tests pass, commits are small.

### T5. [RUN] First look with Token Passing

Precondition: T2 to T4 done and the author confirms no other session is
running.
Steps: Token Passing on the example 04 instance, fixed against demand against
congestion, arrival rate 0.25, horizon as the author says, 6 seeds,
`--storage-epoch 100 --reassignment-cap 8 --congestion-weight 1.0`. Flag these
parameters as illustrative.
Report: relocated units per update, completion share, mean service time and
its three parts, and whether the released tasks are identical across modes for
each seed.
State that the instance has one SKU and uniform demand, so adaptive storage
cannot help. The point is that the switch works and the pairing is valid.

### T6. Draft thesis wording (no repo changes)

Precondition: none. Output goes in chat only.
Write proposed wording for: the `eq:estimates` attribution rule in section 2,
and the `tab:evalparams` and `[A31]` horizon rows once T1 has numbers. Follow
the "Thesis writing style" section of `CLAUDE.md` (no dashes, no colons or
semicolons joining clauses, plain words). Do not edit the thesis.

### T7. Demand model and larger instance (#94, #95)

Precondition: T0 passed, and the author has given the section 4 values.
If any value is missing, stop and ask. Do not pick one.
Steps:
1. Add the demand model: popularity shares by skew exponent, rotation every P
   steps, orders drawn from the popularity at that step with the order random
   stream seeded from the episode seed only.
2. Place `x_0` once from expected demand, popular SKUs nearest the delivery
   vertices, the same for every storage rule.
3. Build a new instance beside example 04 (more agents, storage vertices,
   SKUs). Leave example 04 unchanged.
4. Tests: released tasks identical across storage modes for a seed, `x_0`
   identical across rules, rotation changes the ranking at multiples of P.
Done when: tests pass. Report the instance size and the measured capacity if
T1 has run.

### T8. Wait attribution in the code

Precondition: the author approved the T6 wording for `eq:estimates`.
Steps: charge a step where an agent serving a task stands still to the next
edge on its route to its target, in the online wait estimate. Add a test that
under Token Passing the wait estimate is not always 0 when agents delay.
Done when: tests pass.

### T9. [RUN] The comparison

Precondition: T7 and T8 done, author confirms the values and that no other
session is running.
Steps: run the campaign on the new instance, sweeping Δ, ν and β, with
fixed-trained policies evaluated under all three rules. Matched training only
if the author approves the budget.
Report measured results per condition and storage mode, with the paired
comparison of `eq:rqformal`. Do not claim a benefit that the paired intervals
do not show.

## 6. Order

T0 first. T1 and T6 can start any time (T1 only with the go-ahead). T2, T3, T4
in order after T0. T5 after T4. T7 after the author's values. T8 after T6 is
approved. T9 last.

## 7. Suitability for a medium-effort agent

T0, T2, T3, T4 and T6 are mechanical and well bounded. T5 and T9 are
mechanical but must be reported carefully. T7 and T8 touch the model and need
the author's values or approved wording first, so an agent must stop if they
are missing.
