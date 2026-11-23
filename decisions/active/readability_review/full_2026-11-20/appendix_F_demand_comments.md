# Comments on Appendix F, "Demand drift"

Scope: `thesis/Appendices/F.Demand.tex` (its own PDF, 5 pages, rebuilt
2026-11-20 after the three fixes below). Read as a short paper of its own.
Checked against `slap-mapd-coupling` on `main` (`8ba3048`):
`environment/multi_agent_env.py` (`popularity_ranking`, `zipf_weights`,
`_draw_order_lines`, the section split), `core/experiment_config.py`
(`rotation_shift`), `evaluation/evaluator.py` (`mean_service_time`),
`configs/fleet_8/*.yaml`, `scripts/sweep/load_sweep.py`. Against the result
rows `thesis-progress/results/F_demand/fleet_<m>/demand.*/load_sweep.jsonl`
(recomputed per seed), the first sweep in `524ef5a`
(`results/F_demand/README.md`), the pilot in
`decisions/done/demand_probe_2026-10-17.md`, the D29 measurement in
`decisions/active/model_revision/README.md`, the PF (`sec:pf:tasks`,
`eq:meanservice`, `eq:relgain`), the Experiments chapter (`sec:impl:instances`,
"The orders"), Appendix B and GAPS ([A34], [A68], [A75], [A77], [A105]).
No paper is cited in the appendix. Silva et al. 2020 (`papers/`) was checked
for a source of skewed demand.

The annotated pages are next to this file: `appendix_F_demand_comments.pdf`.

How to answer: tick one box per point and add a note if you want.

---

## A. Is it true (checked against the code, the rows and the probe)

### A1. The sweep measures the pick, the thesis result is the order
**Where:** p. 2, Setting, "The gain is how much demand storage shortens ...".

**Fixed ([A108]).** The sentence said "the mean order service time". The
sweep reads `mean_service_time`, which is the mean over picks
(`evaluator.py:555`), and every number in Results says "a pick". It now says
the pick, and that it is eq. (37) with the pick in place of the order.

What is left for you: [A68] made the order the result. The same rows carry
`mean_order_completion`. Paired by seed, the order gain at the thesis values
is 14.1, 17.5, 17.7 and 14.6 percent at 8, 16, 32 and 64 agents, against
10.9, 13.9, 13.2 and 10.2 for the pick. So the appendix undersells the gain
on the measure the thesis uses. Report the order gain too, or say why the
pick is read here?

- [ ] Add the order gain beside the pick gain
- [ ] Keep the pick and give the reason
- Note:

### A2. The Zipf share is not 1/(r+1) once there are sections
**Where:** p. 2, "the SKU in rank r ... is asked for in proportion to 1/(r+1)".

**Code:** an order first picks a workstation uniformly, then draws its lines
from that workstation's section without replacement, by the Zipf weights
renormalised over the section (`_draw_order_lines`). Every section then gets
the same number of orders, whatever its SKUs' ranks. So from 16 agents on (2
or more sections) a SKU's share overall is not proportional to 1/(r+1), and
drawing 5 of 20 without replacement flattens it further. At 8 agents there is
one section, so only the second effect applies. The Experiments chapter says
the same "in proportion to 1/(r+1)". Say "its weight is 1/(r+1) within its
section"?

- [ ] Agree, reword here and in `sec:impl:instances`
- Note:

**Fixed ([A109]).** Here and in "The orders" of the Experiments, the SKU in
rank r now "gets the weight 1/(r+1)". An order picks a workstation first and
draws distinct SKUs of its section by the weights scaled to sum to one, so
every section gets the same share of orders and a SKU's share is only
roughly in proportion to 1/(r+1).

### A3. What the drift does to the top SKUs
**Fixed ([A108]).** "The most popular SKUs cool down and others take their
place" became "Every SKU climbs that many places, and the most popular ones
drop to the bottom". `popularity_ranking` rotates the list left, so the top
SKUs go from rank 0 to the last ranks in one step. The same "cool down"
sentence is in `5.Experiments.tex` ("The orders"), outside this scope.
**Fixed ([A109]).** The Experiments now say the same as this appendix.

### A4. One warehouse per seed
**Fixed ([A108]).** "each fleet on its own warehouse" became "each seed on
its own warehouse of the fleet's size". The configs set
`warehouse_per_seed: true`, and `load_sweep.py:117` plays each seed on its
own warehouse.

### A5. "Under uniform demand the gain is zero"
**Where:** p. 2, "Under uniform demand the gain is zero whatever the
controller". Also the Summary, "Under uniform demand no placement beats
another".

Be critical. Not measured. Demand storage still sends arriving stock to the
free shelves nearest the workstations, while fixed homes under uniform demand
are arbitrary. So demand storage may still shorten travel. I think "zero" is
too strong. Say "small", or run the skew 0 point once.

- [ ] Soften
- [ ] Measure skew 0
- Note:

### A6. The pilot: "almost nothing" and "most of it back"
**Where:** p. 3, Pilot, and the Conclusion, "gained almost nothing".

**Probe:** without the drift the gain was +0.002 to +0.045 throughput,
depending on the start, against a level of about 0.43, so up to about 10
percent. With the drift fixed storage lost about 15 percent (true), and the
demand rule won back +0.078 of 0.066 lost with 20 SKUs (all of it) and
+0.034 of 0.069 with 100 SKUs (half). Give the range, or say "much less than
with the drift".

- [ ] Agree, give the numbers
- Note:

### A7. The pilot moved 5 places, not 5 percent
**Where:** p. 2, Method, the pilot paragraph, and p. 4, "They are the values
of the pilot".

The probe rotated by 5 places every 200 steps, so 25 percent of 20 SKUs and
5 percent of 100. The Conclusion is careful (it names only the exponent and
the period as pilot values), but the reader cannot tell where 5 percent came
from. One clause in the pilot paragraph.

- [ ] Agree
- Note:

### A8. At 8 agents the sections are not what changed
**Where:** p. 4, "In the updated run every SKU belongs to a section ... so
storage has a place to aim for. Demand storage now cuts the driving ... 19 to
23 percent".

**Code and config:** at 8 agents there are 4 workstations and 20 SKUs, so one
section, and every order may still go to any workstation. Yet the travel cut
at 8 agents rose from 9 to 11 percent to 22 percent. Be critical. I think the
gain at 8 comes from the rule now scoring the mean distance to the section's
workstations ([A77]), from 5 lines per order and Q = 10, not from a target.
Say the section argument holds from 16 agents on.

- [ ] Agree
- Note:

### A9. The horizon of the sweep is missing
**Where:** p. 2, Method.

The rows run 10000 steps and read the last 5000 (`--horizon 10000 --warmup
5000`, `results/F_demand/README.md`). The appendix never says it. It matters
here, because the drift period of 400 gives a cycle of 8000 steps, longer than
the 5000 that are read, so that point sees only part of a cycle. One sentence.

- [ ] Agree
- Note:

### A10. Checked and matching
- Rotation by `max(1, round(share x SKUs))`: 30 and 50 SKUs give 2, so 3000
  and 5000 steps. 2.5 and 5 percent of 20 SKUs both give 1, the same run.
- 160 SKUs at 5 percent is 8 places. 20 SKUs x 200 steps is 4000 steps.
- Updated run at the thesis values: pick gain 10.9, 13.9, 13.2, 10.2 percent
  (11, 14, 13, 10 in the text), range 8.8 to 14.5 ("9 to 15"). All 20 seeds
  keep up at every point. The skew moves the gain by at most 3.5 points (32
  agents, 11.0 to 14.5).
- Put-away cost, ratio of means: 10.3, 12.0, 12.9, 14.5 percent, range 8.5 to
  16.2 ("10, 12, 13 and 15", "9 to 16").
- Travel of a pick: 17.0 to 13.2 steps at 8 agents, 22, 23, 22 and 19 percent
  at the thesis values ("19 to 23").
- First sweep (`524ef5a`): 9, 9, 5 and 10 percent, 16 to 19 of 20 seeds, 3 to
  13 percent over the range, 28 and 7 percent of orders waiting for stock at
  64 agents, travel cut 9 to 11 percent, one line per order.
- D29: 3 steps, 11/16/24/34 against 12.5/17/25/35 steps, "3 to 10 percent"
  (as in the measurement note, from the unrounded distances).
- Pilot: 8 agents, 94 vertices, horizon 2000, 4 to 6 seeds, throughput,
  relocation with a cap.
- Lines per order: 1 + Poisson(4), mean 5. Workstation drawn uniformly. The
  SKU split over sections is a seeded shuffle, fixed for the run.
- Not rechecked: "0.1 to 0.3 percent of the lines wait for stock" (the rows
  carry no line count). Taken from the README.

---

## B. Reasons and sources

### B1. Where does the Zipf law come from?
**Where:** p. 2, Setting.

No citation. Is the Zipf law our own choice, or borrowed? Silva et al. 2020
(already in `references.bib` as `silva2020integrating_slap_opp`) use skewed
demand by Pareto classes (80/15/5 and 50/30/20). Cite it as the usual way
storage studies skew demand, or say the Zipf law is our own choice.

- [ ] Cite Silva et al.
- [ ] Say it is our own
- Note:

### B2. Why 200 steps?
**Where:** p. 4, "have no source".

Honest, good. But B.Parameters gives the storage period Delta = 100 as "half
the rotation period". So 200 is tied to Delta. Say that link here, it is the
only reason the reader can get.

- [ ] Agree
- Note:

### B3. The third change is an oversight, not a finding
**Where:** p. 4, "Three things change, each for a reason the sweep showed".

The single line came from the runs leaving the setting unset (said on p. 4).
The sweep did not show a reason for it. Say "two things the sweep showed, and
one setting that was missing".

- [ ] Agree
- Note:

---

## C. Names, plain words, symbols

### C1. "Section VIII-A0c"
**Where:** p. 2.

`sec:impl:instances` sits on the paragraph "The warehouses", so it prints as
VIII-A0c, and the Zipf law is in the next paragraph, "The orders". Fix the
label in the Experiments chapter (main session), or point to Section VIII-A
by words.

- [ ] Agree
- Note:

**Fixed ([A109]).** `sec:impl:instances` now sits on the subsection
"Motivation and Setup", so every reference prints VIII-A.

### C2. "The same sweep", "the sweep"
**Where:** p. 3, "The same sweep showed that demand storage had no clear
place"; p. 5, "instead of the single line of the sweep".

The paragraph just above is the updated run, these mean the initial run. Say
"the initial run" each time.

- [ ] Agree
- Note:

### C3. "Paired by seed" before it is explained
**Where:** p. 2, Setting, then explained in Method ("Both rules see the same
orders under a seed").

Move the reason up, or drop "paired by seed" from the Setting.

- [ ] Agree
- Note:

### C4. "One place where it is needed"
**Where:** p. 5, second bullet.

A section is served by four workstations, so it is a group of places. "One
area" or "one group of workstations".

- [ ] Agree
- Note:

---

## D. Reading order, repetition

### D1. The Summary repeats itself and names a run the reader does not know
p. 2. The three values are said twice in five lines, and "the updated Token
Passing run" appears before two runs are mentioned.

- [ ] Agree
- Note:

### D2. The pilot is told three times
The Summary, the Pilot subsection and the Conclusion all say "the drift is
what made storage matter", and the Experiments chapter says it too. Keep the
numbers in the Pilot subsection and one sentence elsewhere.

- [ ] Agree
- Note:

### D3. Two runs in one subsection
p. 3. "Demand skew and drift" holds both runs, and "Where an order goes" jumps
back to the initial run, then forward again. Order by run: the initial run
(results, the two rounding faults, where an order goes, one line per order),
then the changes, then the updated run. The Conclusion would then not need to
list the changes again.

- [ ] Agree
- Note:

---

## E. Figures

### E1. Fig. F.1
- The keep-up row is 1.0 at every point. One sentence says it, and the figure
  could lose a row.
- The gain axis is a share (0.1), the text says percent. Use one.
- The figure shows the pick gain. If A1 adds the order gain, the figure
  should follow.
- Caption length is fine (22 words).

- [ ] Agree
- Note:

---

## F. What reads well
- "The sweep does not choose the values. A demand model tuned for the largest
  gain would favour demand storage." Clear reason, short.
- The Conclusion says plainly that the values have no source.
- "Two settings did not do what the thesis says" reports faults honestly.
- The cost in the put-aways is given beside the gain.

---

## The three changes that would help the reader most
1. Report the gain on the order service time, the thesis result, beside the
   pick (A1). The rows already hold it, and it is larger.
2. Tell the two runs in order, one after the other, and cut the repeats of the
   pilot (D2, D3, C2).
3. Say what the demand really is once there are sections (A2, A8): weights
   within a section, and at 8 agents one section, so the "place to aim for"
   argument starts at 16 agents.
