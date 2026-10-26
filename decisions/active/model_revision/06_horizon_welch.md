# 06. The horizon by Welch's method (proposed tag [A66])

**Decision** D10 of `README.md`.

## Why

The gain of demand over fixed storage moved with the horizon, from 27 % at T = 1000 to 47 % at 4000 at 8
agents, and from −21 % to +32 % at 16 agents. The seed error is 1 to 5 points, so it is not noise. Two causes.
The mean service time counts every pick from step 0, including the empty start. And the demand ranking
turns once every |K| / shift × rotation period = 100 / 5 × 200 = 4000 steps, so T = 2000 stops half way
round. Fixed storage was also still getting slower at 4000 steps at 32 and 64 agents.
`../../../notes/queue_findings_2026-10-26.md`, section 6.

## Decided, the normal practice of steady-state simulation

1. **Cut the warm-up** by Welch's method. Average the output over the seeds, smooth it with a moving
   average, and cut where it stops rising (Welch, 1983. Law, *Simulation Modeling and Analysis*, the output
   analysis chapter, to check).
2. **Measure only after the cut.** The mean service time counts the picks released after the warm-up.
3. **Measure over whole demand cycles**, so no phase of the rotation is favoured. T = warm-up + k × 4000.
4. Independent seeds for the confidence interval, as now.

## Also a check of the main load

If fixed storage keeps getting slower after the warm-up is cut, the warehouse never settles at that load,
and the main load is too high for long runs. Read this before the reruns.

## Thesis text

- `thesis/Chapters/2.Introduction.tex`, `eq:meanservice` and the keep-up check (`eq:throughput`), which
  count from step 0. The window [T_warm, T] replaces it, and `[A55]`'s backlog slope is read over the same
  window.
- `thesis/Appendices/H.Horizon.tex`, rewritten around Welch's method, with the graph v1 runs of 1000 to 4000
  steps as the reason.
- `thesis/Appendices/B.Parameters.tex`, the T row (`[A61]`, "2000 or more"), and a warm-up row.
- The lifelong path-finding literature runs a fixed number of steps (Li et al., 2021, 5000 steps, to check).

## Code

- `src/slap_mapd_coupling/evaluation/metrics.py` and `evaluator.py`. Measures over the window, with
  `warmup` as a setting.
- `src/slap_mapd_coupling/evaluation/trace.py` already logs the backlog per step. Welch's plot needs a
  per-step output, for example the service time of the picks finished in each window of steps.
- `thesis-progress/scripts/images/appendix_measures.py`, `horizon_trace()` becomes the Welch plot.
- Training episodes. Decide whether training also uses T = warm-up + k × 4000. Longer episodes make training
  slower (step 10).

## The stall at fleet level (D18, proposed tag [A67])

**Why.** `[A45]` counts a stall when a robot holding a task stands still for a set number of steps. Under Token
Passing standing still is often planned. The longest stand-still in healthy graph v1 runs was 16 steps at 8
agents and up to 109 at 64, so the length would have to be huge and differ per fleet.

**Decided.** A stall is a stretch of X steps in which no robot finishes a task. That is a jam under any
controller. A healthy fleet finishes tasks all the time, and a bigger fleet finishes them more often, so one X
serves every fleet size. X is set above the longest gap between finished tasks in healthy Token Passing runs on
graph v2, read in the Welch runs of `11_reruns.md`.

**Thesis text.** `thesis/Chapters/2.Introduction.tex`, the stall paragraph after the keep-up check (around
line 1162) and its reference to `sec:impl:logging`. `thesis/Appendices/H.Horizon.tex`, `app:cal:stall`, and
`B.Parameters.tex`, the stall row.

**Code.** `src/slap_mapd_coupling/evaluation/metrics.py` (`stalled`, `longest_stand_still`), which gets the
longest gap between finished tasks instead. Training already logs `steps_since_last_completion`
(`training/callbacks.py`).

## Decided while implementing (author, 2026-10-26)

Code in `~/worktrees/refill`, uncommitted, on top of steps 04 and 05.

- **The rotation turns once every 4000 steps at every fleet (D20).** With the SKU count derived from the
  start fill (D19), a shift of 5 places made the demand cycle 2640 steps at 8 agents and 77 160 at 64. The
  shift is now a share of the SKUs, `demand.rotation_share: 0.05`, rounded and at least one place, so each
  rotation moves the same share of the SKUs at every fleet. The rounding leaves the cycle near, not at,
  4000 steps, so the derived SKU count is rounded to the nearest multiple of 20 (author, 2026-10-26) and
  every cycle is exactly 4000 steps. SKUs and start fill: 60 and 0.37 at 8 agents, 280 and 0.40 at 16,
  780 and 0.40 at 32, 1920 and 0.40 at 64. Rounding up instead gave 80 SKUs and 0.48 at 8 agents.
- **Training keeps its horizon for now.** Whether training episodes get T = warm-up + k × cycle is decided
  at step 10, with test D. `warmup` is in the spec and only changes the measures.
- **The window.** `warmup` (T_warm) in the spec and in `ExperimentConfig`, 0 by default, which measures
  the whole run as before. A task, or an order line still waiting for stock, counts when it was released in
  [T_warm, T): the mean service time and its split, the completed counts, the backlog and the keep-up
  check. Throughput is per step of the window, and the backlog slope is read over [T_warm, T] (the second
  half, as before, without a warm-up). The totals of the service time, the order measures and the robot
  busy share still cover the whole run, as diagnostics.
- **The stall (D18).** `longest_completion_gap` is the longest stretch in [T_warm, T] with no task finished,
  counted from the window start to the first finish and from the last finish to T. `stalled` compares it
  with the stall length. `longest_stand_still` stays as a diagnostic. The load sweep reports the gap.
- **Welch's script.** `scripts/sweep/welch.py` runs long Token Passing episodes, cuts each into windows of
  100 steps, averages the pick service time over seeds, smooths it by Welch's rule (m = 5) and writes a
  table, a plot and the slope of the smoothed curve over the second half (the main-load check). It gives the
  demand cycle and does not choose the warm-up.
- **Not done yet.** Test C, the configs' T and T_warm (both wait for test C), the thesis figure
  (`scripts/images/appendix_measures.py`, `horizon_trace()`), the thesis text, and the stall length X
  (from the Welch runs of `11_reruns.md`).
