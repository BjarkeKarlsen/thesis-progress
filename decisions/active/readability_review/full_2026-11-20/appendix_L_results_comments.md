# Comments on Appendix L, "Full results"

Scope: `thesis/Appendices/L.Results.tex`, its own PDF (`L.Results.pdf`, 10
pages, rebuilt 2026-11-20 after the [A108] fixes). Read as its own paper,
with the thesis only where it points. Checked against `GAPS.md` ([A91],
[A95], [A96] with its revision of 2026-11-17, [A99]), the PF ("Keeping up",
`eq:meanservice`, `tab:measures`), `A.Notation.tex`, `slap-mapd-coupling` on
`main` (`8ba3048`): `evaluation/evaluator.py` (`longest_two_agent_hold`, the
order measures), `evaluation/metrics.py`. Every number was recomputed from
the rows themselves:

- learned controllers: `~/thesis_runs/evaluation/fleet_<m>/<arm>/<rule>/evaluation_served_horizon10000_warmup5000/test.jsonl`
  through `thesis-progress/scripts/served_counts.py` (`recount`), runtime from
  `runtime_gpu/`
- Regime 1: `.../fixed/evaluation_served_congestion_horizon10000_warmup5000/`
- Token Passing at 16: `~/thesis_runs/tp_testseeds_2026-11-16/rows/load_sweep.jsonl`
- first tests and validation: `.../evaluation_horizon10000_warmup5000/` and
  `results/L_results/fleet_16/overview.md`

The annotated pages are next to this file: `appendix_L_results_comments.pdf`.
Page numbers below are the printed ones (the cover is unnumbered, so printed
p. n is PDF page n + 1).

How to answer: tick one box per point and add a note if you want. Points
marked **Fixed ([A108]).** are already applied in the appendix.

---

## A. Is it true (checked against the result files and the code)

### A1. The decentralised fixed row at 16 agents mixes two policies
**Where:** p. 5 to 9, every 16-agent table, the "decentralised" row under
fixed storage, and p. 7 "weak in validation, at 0.088 tasks per step".

The served replay of 17 Nov (`rerun20`, code `131b6b1`) chose the
checkpoint again, on the 2 validation seeds its spec lists, and took
`checkpoint_000024`. The first test (13 Nov) and the runtime run chose on 5
validation seeds and played `checkpoint_000019`. [A96] says "Checkpoints
already chosen stay". The `rerun20` check compared the new rows only with
the 6-seed replay, which had the same new checkpoint, so it was not caught.

What the row now holds:
- from checkpoint 24 (replay): served share 0.12, ΛT 0.025, ΛT/m 0.0016,
  the lock cell 20 / 20 and both Regime 1 numbers (0.025, 0.028)
- from checkpoint 19 (first test): backlog slope 17.82, crowding 0.19, the
  whole backlog row (220.6, 0.0, 879.9, 893.8, 167.6, 0.0), the whole stock
  row (19.1, 1.04, 0.30, 3444), κT 0.0113, and validation 0.088
- the replay gives for the same cells 17.90, 0.13, (133.2, 0.0, 892.2,
  896.1, 109.3, 0.0), (11.4, 1.10, 0.27, 3708). At 1250 steps the first test
  locks on 17 of 20, the replay on 20.

The same happened at 8 agents (served replays on 2 validation seeds):
section-based fixed 27 to 10, section-based demand 13 to 10, decentralised
fixed 24 to 12, decentralised demand 16 to 22, with messages demand 18 to
15. The 8-agent lock row in Table L.6 is from these replays. Not a local fix,
it needs a choice of policy, and the Experiments tables read the same rows.

- [ ] Keep the replay's checkpoints, refill every cell from the replay rows
- [ ] Go back to the 5-seed choice and replay those checkpoints with the served counts
- Note:

### A2. Validation against test (Fig. L.2) uses the old count
**Where:** p. 3, "The policies do much better in the short validation runs
than in the long test runs", and Fig. L.2.

`fleet16_val_vs_test.png` is from 16 Nov and draws the test throughput as
the old count (tasks released and finished in the window). Validation has no
warm-up, so its count is the same under both. With the revised count the
gap mostly goes:

| controller, rule | validation | test, old count | test, revised |
|---|---|---|---|
| centralised fixed | 0.158 | 0.036 | 0.143 |
| centralised demand | 0.138 | 0.026 | 0.138 |
| section-based fixed | 0.225 | 0.131 | 0.178 |
| decentralised congestion | 0.210 | 0.104 | 0.186 |
| with messages fixed | 0.136 | 0.004 | 0.091 |

So the paragraph's point (validation hides a slow fall behind) is mostly an
effect of the old count. The policies are slow in both. `5.Experiments.tex`
line 582 says the same thing ("Every learned policy did better in
validation than in the test"), and centralised demand now ties.

- [ ] Agree, redraw Fig. L.2 from the revised counts and rewrite the paragraph
- Note:

### A3. Fig. L.1 is from before the revised counts
**Where:** p. 3, Fig. L.1, "Share of the arriving work served on 16 agents".

The PNG is from 16 Nov 14:24. [A96] (2) says `fleet16_results.py` then drew
an estimate from the backlog slope. The revised counts are of 17 Nov. The
TODO in the `.tex` says the same.

- [ ] Redraw from `served_counts.py`
- Note:

### A4. The 8-agent block and Regime 1 can be filled now
**Where:** p. 1, 2 and 8, Tables L.1 to L.4 and L.11 (all TBD), p. 8, Table
L.10, the TBD rows, and the cell "TBD" in Table L.6.

Everything is home. All twelve 8-agent rows have served counts, Token
Passing has played the 8-agent test seeds (`tp_testseeds8_2026-11-17`, 20 of
20 keep up, longest hold 54), and the Regime 1 rows of all four controllers
at 16 agents have 20 seeds. Ready values:
- Table L.6, 8 agents, centralised fixed: **0 / 0** (served replay,
  checkpoint 13, 20 seeds).
- Table L.10, section-based: 0.178, 0.184, **0.007 [−0.013, 0.026]**, own
  policy 0.198. Better on 10 of 20, worse on 9.
- Table L.10, with messages: 0.091, 0.081, **−0.011 [−0.025, 0.004]**, own
  policy 0.084. Fewer on 15 of 20.
- Both intervals hold zero, so "The storage rule on its own changes nothing
  the test can measure" now holds for all four. The 6-seed numbers in the
  TODO (messages fewer on all 6, [−0.068, −0.001]) no longer hold.
- 8 agents, served share: centralised 0.86, 0.90, 0.81; section-based 0.87,
  0.81, 0.91; decentralised 0.84, 0.87, 0.82; with messages 0.96, 0.66, 0.82
  (fixed, demand, congestion-aware). Keep-up 13, 15, 11; 14, 12, 14; 12, 13,
  11; 18, 9, 13. Subject to A1.

- [ ] Fill them (after A1 is settled)
- Note:

### A5. "Better congestion-aware rows come from the training run" holds for two of four
**Where:** p. 7, "The better congestion-aware rows of Section L.1.2 come
from the training run, not from storage".

True for the centralised and the decentralised controllers (better on all
20 seeds). For section-based, the policy trained under congestion-aware
storage (0.198) beats the fixed-trained one under the same rule (0.184) on
only 8 of 20 seeds. For messages 0.084 against 0.081, on 11. Once A4 is in,
say which controllers it holds for.

- [ ] Agree
- Note:

### A6. Order service time counts from the first task, not from the order
**Where:** Table L.8, the order column (now headed ζ̄T).

The PF counts an order from its release, `t_z^released`. The code
(`evaluator.py`, the order measures) counts from the earliest release time
of its tasks. A pick task is made only once its stock is on a shelf, so for
an order whose lines all waited for stock the code starts later. Only
orders with no line still waiting are counted. Small, and Token Passing
barely waits for stock (0.03), but the learned rows wait a lot (stock wait
208 to 1454). A drift for #103, not a text fix.

- [ ] Record in #103
- Note:

### A7. Checked and matching
- Every 16-agent cell of Tables L.5, L.7, L.8 and L.9 for Token Passing and
  for the learned controllers, except the decentralised fixed row (A1) and
  decentralised congestion-aware, where the first test and the replay of the
  same checkpoint differ in the last digit (2306.4 against 2306.9, 2930.1
  against 2933.3). The tables take the first test. Not worth a change.
- The 16-agent lock counts at 500 and 1250 steps, all twelve cells, and
  the 8-agent cells against the served replays.
- The 16-agent paragraph: 0.12 to 0.69, 0.63 and 0.69, 7 and 5 seeds, 0.66
  and 2, about half, 0.28 to 0.37, 0.12.
- Decision time: 109.5 to 110.0 ms, 72.2 to 73.7 ms, 11.3 to 14.6 ms
  (GPU, `runtime_gpu`), Token Passing 1.9 to 2.0 ms from the load sweep. The
  test-seed runs show 3.7 ms, as the text says they shared the machine.
- Token Passing on the same 20 test seeds at 16 agents
  (`tp_testseeds_2026-11-16`), 20 of 20 keep up, no lock.
- Regime 1, centralised and decentralised: 0.143 and 0.143, −0.001
  [−0.006, 0.005], better on 9; 0.025 and 0.028, 0.002 [−0.005, 0.010],
  better on 10. Own policy 0.161 and 0.186, better on all 20.
- Λ_T/m is Λ_T over 16 in every row.

**Fixed ([A108]).** The lock rule. The text said "two agents hold the same
task". The code takes, at each step, the second longest hold of the tasks
held then (`longest_two_agent_hold`), so two agents each hold their own task
([A91] says the same). Now "two agents each hold their own task for 500
steps or more at the same time".

**Fixed ([A108]).** "Locks are rare at 8 agents" with 10, 7 and 6 of 20 in
the table beside it. Now "Fewer seeds lock at 8 agents, at most 10 of 20."

**Fixed ([A108]).** ζ̄T headed the pick service column of Tables L.2 and
L.7. ζ̄T is the order service time (PF `eq:meanservice`, notation table, and
[A68]). The pick column is now "pick service" and the order column of Tables
L.3 and L.8 carries "order service ζ̄T". The code comment in `metrics.py`
(`mean_service_time  # zeta_bar_T`) is out of date since [A68], a note for
#103.

**Fixed ([A108]).** "an controller" to "a controller".

---

## B. Reasons and sources

### B1. Why is the gain only in the main text?
**Where:** p. 1, "The gain over fixed storage is in the main text, and only
where every seed keeps up".

An appendix of full results is where I would look for the gain and its
interval. Give it here too, for Token Passing at both fleets, or say why
not.

- [ ] Add the gain rows here
- [ ] Keep it in the main text, give the reason
- Note:

### B2. Why are the pick service times shown at all for runs that fall behind?
**Where:** p. 3, "So the pick service times in the tables are not compared
between rules", and Table L.7.

If they grow with the horizon and are not compared, what does the reader do
with 3655 against 1377? Either say what they show (how far behind) or grey
them out for runs that do not keep up.

- [ ] Say what they show
- [ ] Mark them for runs that do not keep up
- Note:

### B3. The lock thresholds need a reason here
**Where:** p. 5, "500 steps", "the stricter threshold of 1250 steps".

[A91] sets 500. 1250 is in neither GAPS nor the Experiments chapter. Where does it come from? One clause each, since this
appendix must read on its own.

- [ ] Agree
- Note:

---

## C. Names, plain words, symbols

### C1. The measures are never introduced
**Where:** p. 1, before Table L.1, and every table head.

As its own paper the reader meets served share, backlog slope, stalled
runs, warm-up, wait for agent, stock wait, crowding, shelf taken, lines
waited, split SKUs, old stock on prime, unit age, updates, arrived units,
ζ̄T, κT, ΛT and m without a word. Most are in the PF and Appendix C
(measures). One short paragraph that says what each table measures and where
the definitions are. The backlog slope also needs its unit.

- [ ] Agree
- Note:

### C2. "Shelf taken" and "stalled runs"
**Where:** Table L.7, last column (n/a for every learned row), Table L.5,
last column (0 everywhere).

"Shelf taken" is `mean_pick_wait_pickup_taken`, the wait while another
agent holds the shelf. Why only Token Passing? "Stalled runs" is 0 in every
row, and the lock table now does that job. Drop it, or say what it adds.

- [ ] Define shelf taken, drop stalled runs
- Note:

### C3. "Keeps up" is shown in parts, but the text uses the whole
**Where:** p. 2, "keeps up on 7 and 5 of the 20 seeds", against Table L.5
(8 and 7 under fixed).

A run keeps up when both picks and put-aways do. The table shows the two
apart. Add a "keeps up" column or say it in the caption.

- [ ] Add the column
- Note:

### C4. "A few"
**Where:** p. 2, "No learned controller keeps up at 16 agents on more than a
few seeds".

Section-based fixed keeps up on 7 of 20. Say "on more than 7 of 20".

- [ ] Agree
- Note:

---

## D. Reading order and repetition

### D1. The 8-agent heading sits after its tables
**Where:** p. 2, "L.1.1 8 agents:" printed right above "L.1.2 16 agents".

The run-in heading has no text after it, so the four [H] tables come first.
The reader sees 8-agent tables under no heading. One sentence after the
heading, or a display heading, fixes it.

- [ ] Agree
- Note:

### D2. Token Passing's pairing comes after it is used
**Where:** p. 3, "Token Passing plays the same 20 test seeds as the learned
controllers, so every row is paired seed by seed".

This is what makes the rows comparable, so it belongs in the opening, with
"Token Passing is the reference". Paired with what is not said either.

- [ ] Move it up
- Note:

### D3. "Serves only about an eighth" three times
**Where:** p. 2 "serves only 0.12", p. 7 "the one trained under fixed
storage 0.028", p. 7 "serves only about an eighth of the work under either
rule".

The last paragraph of L.2 is a lone line that repeats the two above. Merge
it into the Regime 1 paragraph.

- [ ] Agree
- Note:

### D4. The stock section has no text
**Where:** p. 8, "L.3 Stock in the test runs".

Two tables and no sentence. What should the reader take from them? The one
number I would explain is old stock on prime, 0.42 under demand storage
against 0.29 under fixed for Token Passing. "Arrived units" is 51.6 in every
row and "updates" 100 in every row, so they tell nothing per row.

- [ ] Add one or two sentences
- [ ] Drop the constant columns
- Note:

---

## E. Figures

### E1. Fig. L.1 and Fig. L.2 need redrawing
See A2 and A3. Both are from 16 Nov, before the revised counts.

- [ ] Redraw both
- Note:

### E2. Fig. L.3 restates the text
**Where:** p. 3, "The centralised controller ... takes 110 ms per step".

The paragraph gives every number the figure shows. Keep one sentence
(decision time follows how much a controller reads) and point to the figure.

- [ ] Agree
- Note:

---

## F. What reads well
- "The policy stays the same, so any change comes from the storage rule
  alone." Clear reason for Regime 1.
- "Each controller has one training run per rule, so this cannot tell
  training under the rule apart from a better training run." Honest and
  short.
- The keep-up first, then the parts, then cost, then backlog. The order of
  the tables follows how a run is read.
- Token Passing timed on its own machine, said plainly with the reason.

## The three changes that would help the reader most
1. Settle which checkpoint is the chosen policy (A1), then fill every table
   and redraw both figures from the revised counts (A2 to A4).
2. Open the appendix with one paragraph on what is measured and how Token
   Passing is paired (C1, D2), so it reads on its own.
3. Rewrite the validation paragraph from the revised counts (A2), since its
   point mostly goes away.
