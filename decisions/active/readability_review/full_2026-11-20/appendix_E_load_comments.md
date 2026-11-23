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

### A1. The capacities were found with the old keep-up check
**Where:** p. 2, "This is the keep-up check in (27)", and Table E.1.

The Setting paragraph states the [A96] check (work served in the measured
steps, counting work released earlier). Tables E.1 and E.2 were read with
the old check. The rerun near the capacity edge with the new check
(`results/E_load/fleet_<m>/served_check/`) gives one tested step higher at
every fleet: 0.175, 0.35, 0.6 and 1.2 (main loads 0.105, 0.21, 0.36, 0.72).
So the main loads used everywhere (0.09, 0.18, 0.3, 0.6) now sit at about
0.5 of capacity, not 0.6. This is already open in `SESSION_CONTEXT.md`
("Capacities under the served check"), with the proposal to keep the loads,
since every run trained on them, and say so here. Note that the served
check only replayed the rates near the edge, not the lower grid rates.

- [ ] Keep the loads, add a paragraph and a column with the served-check capacity
- [ ] Rerun with the new capacities
- Note:

### A2. "Released during the run"
**Fixed ([A108]).** E.4.4 said a run passes when it finishes the share of
the work "released during the run". That contradicts eq. (27) and the
Setting paragraph. Now "released in the measured steps, counting work
released earlier too".

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

### A5. The Token Passing rule checks the shelf too
**Fixed ([A108]).** E.4.6 said an agent takes only a task "whose workstation
is not where another agent's path ends". The code (`_take_a_task` in
`planners/token_passing.py`) and VI-H check both the pickup and the end
vertex. Now "whose shelf and workstation".

### A6. Checked and matching
- Table E.1 against `capacity.json` of every fleet: capacity, first failing
  rate, main load. Per agent: 0.011, 0.011, 0.009, 0.009.
- Order work and put-aways keep up 20 of 20, backlog trend -0.03, -0.05,
  -0.25, -1.0 (F_demand rows at skew 1, fixed storage: -0.027, -0.045,
  -0.245, -1.005).
- Table E.2 against the first sweep (`524ef5a`), and capacity per agent
  0.022 to 0.006, longest trip 36 to 82.
- Capacity per agent 0.019 and 0.016 in the updated run.
- Overflow 146, 338, 705 and 1740 units per run, over the whole run
  (`overflow_units_by_update` is summed over every update), 5.8 to 10.0 % of
  the pallet units. No unit unplaced at any main load.
- A pick moves 17.0 to 25.1 steps, waits 74.2 to 158.3 for an agent, 67.9
  to 156.5 of them with another path ending at its workstation
  (`mean_pick_wait_delivery_taken`), 74 to 84 % of the service time. Agents
  busy 32 to 56 %. (The E_load README says 67 to 156 and 30 to 56. The text
  is right, the README is off.)
- lambda_task is order lines per step (`arrival_rate / mean lines` orders
  per step in `multi_agent_env.py`).
- f_up = 0.8 in every config. The grid 0.0125 m to 0.1 m in eight steps.
- 10000 steps, 5000 warm-up, 20 seeds. The backlog slope counts only the
  measured window.
- The two counting errors and the 7 of 20 seeds at 0.175 (first sweep
  README).
- Fixed storage sends a pallet whole to its home shelf, then to the next
  shelf by distance (`storage/arrival.py`).
- Eq. (27), Sections V-D and VI-H, Appendices D, F and G resolve to the
  right places.

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

### C1. "Section VIII-A0c"
**Where:** p. 2, p. 4 and p. 6.

`sec:impl:instances` is a `\paragraph` label in `5.Experiments.tex`, so the
number prints as "VIII-A0c". Every appendix that cites it shows the same.
Point to "Section VIII-A, The warehouses" in words, or move the label to the
subsection. Not my file, so not fixed.

- [ ] Agree
- Note:

**Fixed ([A109]).** The label moved to the subsection, so it prints VIII-A.

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
