# Comments on Appendix H, "Evaluation horizon and stall length"

Scope: `thesis/Appendices/H.Horizon.tex` (`app:horizon`), all four pages of
`H.Horizon.pdf` (rebuilt 2026-11-20 after the fixes below). Checked against
the Problem Formulation (`sec:pf:measures`, the keep-up and stall
paragraphs), Appendices E, G and L and `5.Experiments.tex` (the 10000-step
runs), `GAPS.md` ([A45], [A61], [A69], [A96]), the model revision plans
(`active/model_revision/06_horizon_welch.md`, D10, D18, D22),
`results/E_load/fleet_<m>/` (`load_sweep.jsonl`, `capacity.json`),
`results/L_results/fleet_16/*/README.md`, the old `results/H_horizon/`
(git `b3007e8^`), `scripts/images/appendix_measures.py`, and
`slap-mapd-coupling` on `main` (`8ba3048`): `evaluation/evaluator.py`
(`longest_completion_gap`, line 328, `stalled`, line 694),
`evaluation/metrics.py` (lines 92 to 141), `core/experiment_config.py`
(lines 83 to 101), `environment/multi_agent_env.py` (lines 307 to 316, 643
to 649), `configs/fleet_<m>/*.yaml`.

The annotated pages are next to this file: `appendix_H_horizon_comments.pdf`.

How to answer: tick one box per point and add a note if you want. Only the
points marked **Fixed** were changed in the thesis.

---

## A. Is it true

### A1. The appendix does not say which horizon we used
**Where:** p. 1 (Summary), "The horizon is at least 2000 steps", and the
Method.

Every run we report plays 10000 steps with the first 5000 left out: the
Token Passing load sweep and sensitivity runs (`E.Load.tex` line 76,
`G.StorageValues.tex` line 206, all `load_sweep.jsonl` rows have
`horizon` 10000, `warmup` 5000), the fleet 16 tests (`L.Results.tex` line
23, `results/L_results/fleet_16/*/README.md`) and the Experiments
(`5.Experiments.tex` lines 515 and 521). Only training and validation use
2000 (the configs' `horizon: 2000`). This appendix, which should be the
one that sets T and the warm-up, still says "at least 2000, whether longer
is read from ..." and has a TBD table. The 5000 comes from model revision
D22 ("a warm-up of about 5000 steps"), which has no `[Axx]` entry in
`GAPS.md`. `5.Experiments.tex` line 177 still says "a warm-up of TBD steps".

- [ ] Rewrite H around T = 10000 and the 5000 warm-up, with the reason (new [Axx])
- [ ] Keep it open and run the calibration first
- Note:

**Fixed ([A109]).** Summary, Method, Table H.1 and Conclusion now say every reported test run lasts T = 10000 with the first 5000 left out (D22, E and L rows), training episodes 2000. `5.Experiments.tex` "warm-up of TBD steps" replaced. B1 (whole cycles) left open.

### A2. The stall in the code is a fleet-level gap
**Where:** p. 1, "an agent that stands still too long marks a stall", the
Setting ("A stall is a stretch in which an agent holding a task stands
still longer than the stall length") and the Method.

**Code:** `stalled = longest_completion_gap > stall_length`
(`evaluator.py` line 694). `longest_completion_gap` is the longest
stretch in the measured window in which no agent finished a task
(`evaluator.py` line 328). `longest_stand_still`, the measure this appendix
and Fig. H.3 read, is kept only as a diagnostic, "since under Token Passing
standing still is often planned" (`metrics.py` line 130). That is decision
D18 (`06_horizon_welch.md`): one agent's stand-still under Token Passing
was 16 steps at 8 agents and up to 109 at 64, so its stall length would
have to be huge and differ per fleet. The PF stall paragraph says the agent
version too, so this is a PF point as well. The comment in
`experiment_config.py` line 99 still says the agent version, against its
own evaluator. No config sets `stall_length`, so no run has counted a stall
yet.

Be critical of D18 too. In the E rows the gap depends on the load much more
than on the fleet: at 8 agents it is 15 to 24 steps at rate 0.2 but 27 to
219 at 0.1, and the main load (0.09) is below every swept rate. So "one X
for every fleet" does not hold either. A gap measured in tasks rather than
steps, or a gap relative to the expected time between finishes, would be
fairer.

- [ ] Use the fleet-level gap (D18), change PF and H to match the code
- [ ] Keep the agent stand-still, change the code
- Note:

**Fixed ([A109]).** Stall is now the fleet-level gap of the code (D18) in the PF (`sec:pf:measures`), H Setting and Method, K and B.5. Stall length stays TBD, no config sets `stall_length`. The critique of D18 (load dependence) is left for the author.

### A3. The three figures are from the old model
**Where:** Fig. H.1, H.2 and H.3.

`thesis/Images/app_horizon_*.png` and `app_stand_still.png` were drawn on
26 October from `results/H_horizon/` (runs of 24 October, graph v1, 100
SKUs, 3 trace seeds of 4000 steps, 20 seeds at T = 1000 to 4000 from step
0). Those rows were removed in `b3007e8` ("keep only the step 12 sweep").
Running `appendix_measures.py` today would draw H.1 and H.2 as placeholders.

- Fig. H.2 says "drift periods k after the warm-up", but those runs had no
  warm-up cut. The script sets `warm = min(horizons) % 200 = 0`, so the x
  axis is just T / 200.
- Fig. H.3 does not match today's E rows. At 64 agents the current rows give
  a longest stand-still of 19 to 64 over all rates, the figure 55 to 87. At
  8 agents the rate nearest the main load (0.1) gives 6 to 16.
- `longest_stand_still` covers the whole run, the warm-up included
  (`env.log.longest_blocked_run_by_task`, never cut to the window), unlike
  what `E.Load.tex` line 282 says of "every other measure".

- [ ] Redraw from step 12 runs (needs new H runs for H.1 and H.2)
- [ ] Drop H.2 and keep H.1 as the Welch plot
- Note:

**Partly fixed ([A109]).** Not redrawn. Each caption now says the figure comes from the earlier graph runs of 24 October (H.1, H.2 from `results/H_horizon` at `b3007e8^`, H.3 matches the E rows at `81a7a38`). H.2 "after the warm-up" and H.3 showing the stand-still remain.

### A4. The conclusion is out of date
**Where:** p. 2, "The stall length waits for the load sweep to be run again".

The load sweep was run again on 31 October (step 12). What it waits for now
is the choice in A2 and a value.

- [ ] Agree, rewrite with A1 and A2
- Note:

**Fixed ([A109]).** Conclusion rewritten: horizon settled, sweep rerun 31 October, stall length open, no run counts stalls yet.

### A5. Small mistakes fixed

**Fixed ([A108]).** "A run lasts T timesteps, and every measure of Section
V-J is taken over it." The measures leave the warm-up out (PF "Keeping up",
`metrics.py` line 92, the window [T_warm, T)). The sentence is now "A run
lasts T timesteps.", and the warm-up paragraph ends with "The measures of
Section V-J leave the warm-up out."

**Fixed ([A108]).** "a agent" became "an agent".

**Fixed ([A108]).** The stall pointed to Section VII-B (`sec:impl:logging`),
which never mentions stalls. It now points to Section V-J
(`sec:pf:measures`), where the stall is defined.

**Fixed ([A108]).** The source comment under the Method said "whether the
measures leave out the warm-up. The thesis measures every run from t = 0".
Both are no longer true ([A96]). The comment now records the 10000/5000 runs,
and a second comment notes that the code's stall flag reads
`longest_completion_gap`.

### A6. Checked and matching
- Demand drifts every 200 steps (`rotation_period: 200` in every
  `configs/fleet_<m>/*.yaml`).
- Δ = 100 in the configs (`storage_rule.epoch_length: 100`).
- Every SKU starts alone on a shelf drawn at random (`initial_placement:
  random_slots`, [A69]).
- 2000 steps hold ten drift periods and twenty storage periods.
- `longest_stand_still` is the longest run of steps an agent holding a task
  stood still, by its own choice or overridden (`multi_agent_env.py` lines
  643 to 649), as the Fig. H.3 caption says.
- Token Passing does not deadlock on these warehouses: every warehouse is
  well-formed by construction ([A62], `app:wellformed`).
- Labels: `tab:evalparams` is Table B.5, `eq:throughput` is (27),
  `sec:pf:measures` is V-J, `app:wellformed` is D.3.

---

## B. Reasons and sources

### B1. Drift period or demand cycle as the unit of the horizon
**Where:** p. 1, "Demand drifts every 200 steps", and the Method, "the
warm-up plus k drift periods".

The drift moves 5 % of the SKUs every 200 steps, so the ranking turns once
in 4000 steps (D20). D10 decided T = warm-up + k × 4000, whole cycles, "so
no phase of the rotation is favoured". The appendix uses k drift periods of
200 and never names the 4000-step cycle. 5000 measured steps is one and a
quarter cycles, so this matters for A1.

- [ ] Use whole cycles (D10), say the 4000 here
- [ ] Keep drift periods, give the reason
- Note:

### B2. Where the warm-up cut comes from
**Where:** p. 1, "It ends where the backlog stops rising".

This is Welch's method, the normal practice of steady-state simulation (D10
cites Welch 1983 and Law, *Simulation Modeling and Analysis*). Cite it.
Also say which output it is read on. `scripts/sweep/welch.py` averages the
pick service time per 100 steps, not the backlog.

- [ ] Cite Welch / Law, read on service time
- [ ] Keep the backlog, say it is ours
- Note:

### B3. Is Token Passing's longest stand-still the right yardstick?
**Where:** p. 1, "its longest stand-still shows how long an agent waits in
ordinary traffic".

Be critical. Token Passing plans its waits, so its stand-stills are long and
grow with the fleet (E rows, up to 64 steps at 64 agents). A learned agent
waits differently. I think the hunch holds, which is D18's reason. This
belongs with A2.

- [ ] Agree, follow A2
- Note:

---

## C. Names and plain words

### C1. "stand-still", "stall", "jam"
Three words for nearby things. "Stall" is the measure, "jam" the thing it
catches, "stand-still" the input. Fine if each is said once, but the
Summary and Setting both define the stall. Keep one definition.

- [ ] Agree
- Note:

**Fixed ([A109]).** The Summary now only asks the question. The Setting holds the one definition.

### C2. "Calibration:" in the headings
"Calibration: the evaluation horizon" and "Calibration: the stall length"
render as run-in headings ending on a colon ("H.4.1 Calibration: the
evaluation horizon:"). "The horizon" and "The stall length" are enough.

- [ ] Agree
- Note:

---

## D. Reading order and repetition

### D1. The keep-up sentence floats
**Where:** p. 1, "The keep-up check (27) looks at one horizon, so passing
it does not prove that the backlog stays bounded."

A repeat of the PF, with no link to the warm-up before or the stall after.
Tie it to the backlog trace of Fig. H.1 (that is why we show the backlog
over time) or drop it.

- [ ] Tie to Fig. H.1
- [ ] Drop
- Note:

### D2. "Scores mostly the warm-up"
**Where:** p. 1, "A horizon that is too short scores mostly the warm-up".

Now the warm-up is left out, a short horizon scores few measured steps and
part of a demand cycle, not the warm-up. One clause to change, but it
depends on A1 and B1.

- [ ] Agree
- Note:

**Fixed ([A109]).** Now "A horizon that is too short measures only a few steps and a few drifts".

### D3. Empty Results subsections after the figures
The two Results subsections hold only comments, and the figures float
above them, so the reader sees a table, two lone headings and then the
Conclusion. Once the sentences are written, put each figure in its own
subsection.

- [ ] Agree
- Note:

---

## E. Figures

### E1. Fig. H.1, old model
See A3. If the trace stays, redraw it on step 12 runs at the main load,
with the 5000 cut drawn.

### E2. Fig. H.2, "after the warm-up" is not true
See A3. With T = 10000 and 5000 left out, this figure may not be needed.
Decide with A1.

### E3. Fig. H.3, old rows and the wrong measure
See A2 and A3. If the stall is the fleet-level gap, the figure should show
`longest_completion_gap` of the step 12 rows near each main load.

- [ ] Redraw all three after A1 and A2
- Note:

---

## F. What reads well
- The question in the Summary is clear: how long a run must be, and how long
  an agent may stand still.
- "It needs no training, so the values do not move while the learned
  controllers improve." A good reason in one sentence.
- "A stall length that is too short counts ordinary waiting as a jam, and
  one that is too long misses the jams." Plain and to the point.

## The three changes that would help the reader most
1. Say the horizon we actually use, 10000 steps with 5000 left out, and why
   (A1, B1). Every other appendix already reports it.
2. Settle what a stall is, the agent stand-still of the text or the
   fleet-level gap of the code (A2), and change PF, H and the code comment
   together.
3. Redraw the three figures from step 12 runs, or drop H.2 (A3).
