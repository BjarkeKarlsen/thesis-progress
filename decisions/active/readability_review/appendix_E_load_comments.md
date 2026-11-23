# Comments on Appendix E, "Load and capacity"

Scope: `thesis/Appendices/E.Load.tex` (PDF `thesis/Appendices/E.Load.pdf`, 7
pages, built 2026-11-18, annotated from a copy taken before the fixes below).
Read as its own short paper, with the thesis only where it points to it.
Checked against `results/E_load` (README, `capacity.json`, `summary.md`,
`served_check/`), `results/F_demand/fleet_<m>/demand.skew` (the rows at the
main load), the first sweep at `524ef5a`, `results/README.md`,
`SESSION_CONTEXT.md`, `GAPS.md` ([A58], [A59], [A61], [A75], [A77], [A96],
[A103]), `main.pdf` (eq. 27, VI-H, VIII-A) and `slap-mapd-coupling` on `main`
(`8ba3048`): `evaluation/evaluator.py`, `planners/token_passing.py`,
`storage/arrival.py`, `environment/multi_agent_env.py`, the fleet configs.

The annotated pages are next to this file: `appendix_E_load_comments.pdf`.

How to answer: tick one box per point and add a note if you want. Points
marked **Fixed ([A108])** are already applied.

---

## A. Is it true (checked against the code and the result files)

### A3. How precisely the capacity is known
**Where:** p. 3, "until the capacity is precise enough to set the
experiment", p. 6 and p. 7, "At 32 and 64 agents the capacity is only known
to within 0.1 and 0.2".

The runs added one pass of three finer rates, a quarter of a grid step
apart, and pass 2 found nothing to refine (`results/E_load/README.md`). At
8 and 16 agents the finer rates are also a quarter step apart (0.025,
0.05). So every fleet is known to within a quarter of a grid step, not only
32 and 64. Say "a quarter of a grid step" in Method and drop the two later
sentences.

- [ ] Agree
- Note:

### A4. "Required to be small"
**Where:** p. 5, "the use of other shelves is required to be small".

Nothing in the code or the sweep checks it, and there is no number. At 64
agents 10 % of the arriving units go off their home shelf. Either give a
bound or say it is read off Fig. E.2, not a check.

- [ ] Give a bound (which?)
- [ ] Say it is a reading
- Note:

---

## B. Reasons and sources

### B1. Why 0.6?
**Where:** p. 3, "The value 0.6 leaves room below capacity while still
giving the agents regular work".

"Regular work" is weak. At the main loads the agents hold a task only 32 to
56 % of the time. The real reasons are already in the appendix: near
capacity a small saving in travel turns into a large saving in waiting (p.
2), and the check passes rates where the fleet is already overloaded (p.
6). Say 0.6 is our own choice and give those reasons here. With A1 the
loads are about 0.5 of capacity anyway.

- [ ] Agree
- Note:

### B2. Why f_up = 0.8, and is it set here?
**Where:** p. 2, "the keep-up threshold f_up", and p. 5, E.4.4.

The Summary lists f_up as a value set here, but E.4.4 says it is never
varied. Be critical: at 8 agents the main load releases about 450 lines in
the window. 0.8 lets about 90 stay unfinished, while at most 8 can be in
progress. So 0.8 is loose, and that is why the check passes overloaded
rates. I think the hunch holds. Give the reason for 0.8 (or say it is ours),
and move E.4.4 to Method, since it is a setting, not a result.

- [ ] Agree, give the reason and move it
- Note:

### B3. "The learned controllers ... do not have this wait"
**Where:** p. 7, last paragraph of E.4.6.

True for the path-end wait. But the learned controllers queue and can lock
at a workstation ([A91]). Do they really wait less there? Say what they
have instead, or take it to the Discussion. It also repeats VI-H word for
word.

- [ ] Agree
- Note:

### B4. The main loads are set by Token Passing's wait
**Where:** p. 7, "so the main loads are set by that wait as much as by
travel".

So the learned controllers run at a load picked for a router that idles at
the workstation. Is that fair for RQ1? I think it is fine for the gain
(paired within a controller), but it should be in the Discussion.

- [ ] Add to the Discussion
- Note:

---

## C. Names, plain words, symbols

### C2. Two symbols for one sentence
**Where:** p. 3, lambda_main = 0.6 lambda_capacity.

Neither symbol is used again. "The main load is 0.6 of the capacity" says
it.

- [ ] Drop the display
- Note:

### C3. "Did not go round in 4000 steps"
**Where:** p. 3, third bullet.

With 30 and 50 SKUs it went round in 3000 and 5000 steps ([A75]). Say "not
in exactly 4000 steps", or give the numbers.

- [ ] Agree
- Note:

### C4. "The updated run confirms the values"
**Where:** p. 4, first line under Fig. E.1.

Which values? The updated run changed every main load. "Demand storage
beats fixed storage at every fleet size" is a result of Appendix F, with no
number or pointer here.

- [ ] Agree
- Note:

### C5. Two backlog measures
**Where:** p. 5, the note under Table E.1, and Fig. E.1 (a).

The figure shows the backlog at the end, the table its growth per 100
steps. Name both, or show one.

- [ ] Agree
- Note:

### C6. "The rules' own pallets"
**Where:** p. 5, E.4.5.

Reads odd after the pallet rename. Method says it plainly ("once the stock
placed by the storage rule has replaced the random start"). It is also a
repeat of Method.

- [ ] Agree
- Note:

### C7. "Drives"
**Where:** p. 7, "a pick drives 17 to 25 steps", "not driving".

The thesis says "move to", not "drive".

- [ ] Agree
- Note:

---

## D. Reading order and repetition

### D1. Results open with history
**Where:** p. 3, E.4.1, and E.4.5.

The reader wants the capacities first. The two runs, the five problems and
the initial run come before the updated run's own description (E.4.6),
which comes after its table (E.4.2). Proposal: the load sweep, stock that
does not fit, the updated run's wait, then one subsection "The initial run"
at the end with the five problems and Table E.2.

- [ ] Agree
- Note:

### D2. The Summary has no result
**Where:** p. 2, Summary.

It says how the rate is chosen, not what it came out as. Give 0.09, 0.18,
0.3 and 0.6 lines per step for 8 to 64 agents, and the one finding (picks
wait mostly for their workstation).

- [ ] Agree
- Note:

### D3. Said three and four times
- "Because it needs no training": Setting, Method, E.4.1.
- The capacity rule: Summary, Method, E.4.2, Conclusion.
- The backlog is shown next to the check: Setting, E.4.2 note, E.4.4, E.4.5.

Keep each once, in Method, and point back.

- [ ] Agree
- Note:

### D4. The counting errors, said twice
**Where:** p. 6, "Neither changes the capacities or the gains above", and
the paragraph after the list.

"The gains above" are not in this appendix (they are in Appendix F). The
paragraph after the list repeats the sentence before it. Keep one, and say
where the gains are.

- [ ] Agree
- Note:

---

## E. Figures

### E1. Fig. E.1, dashed lines and hidden markers
Panel (b) draws picks solid and put-aways dashed (`appendix_load.py`), but
neither the legend nor the caption says so. 8 and 16 agents have the same
capacity and main load per agent (0.019 and 0.011), and so do 32 and 64
(0.016 and 0.009), so one marker hides the other. Add "put-aways dashed" to
the legend, and offset or outline the hidden markers.

- [ ] Agree
- Note:

### E2. Fig. E.2, the dotted lines
The four main loads are within 0.002 per agent of each other, so the dotted
lines read as one. Fine if the only point is "no failed placement at the
main load".

- [ ] Fine as is
- [ ] One line, or a shaded band
- Note:

---

## F. What reads well
- "The load matters because a fleet close to capacity can turn a small
  saving in travel into a large saving in the wait for an agent." The real
  reason, in plain words.
- "The keep-up check passes some rates where the fleet is already
  overloaded." Honest and with numbers.
- E.4.6 explains the workstation wait step by step, with the cause and why
  Token Passing is kept as published.
- Every number in Table E.1, E.2 and E.4.3 matches the result files.

## The three changes that would help the reader most
1. Settle A1: say the capacities came from the old check, and what the new
   check gives, or rerun. Then give the real reason for 0.6 and 0.8 (B1, B2).
2. Put the result first: the Summary with the main loads, and the
   history of the initial run at the end (D1, D2).
3. Say each rule once, in Method (D3), and fix the broken "VIII-A0c" number (C1).
