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
