# Comments on Appendix B, "Parameters and where each value comes from"

Scope: `thesis/Appendices/B.Parameters.tex` (its own PDF, 4 pages, rebuilt
2026-11-20 after the fixes below). It is a reference table, so it is checked
for truth more than for flow. Checked against `slap-mapd-coupling` on `main`
(`8ba3048`): `configs/fleet_8`, `configs/fleet_16` (and `fleet_32`,
`fleet_64` for the counts), `training/spec.py`, `training/config.py`,
`core/experiment_config.py`, `environment/multi_agent_env.py`,
`environment/storage_estimates.py`, `environment/zones.py`,
`training/arm.py`. Also against Appendices E, F, G, H, I and J,
`4.Implementation.tex` (`sec:method:storage`, `sec:method:training`),
`5.Experiments.tex`, `GAPS.md` ([A31], [A46], [A58], [A73], [A91], [A96],
[A106]), van Knippenberg et al. 2021 (Tables 1 and 5,
`papers/knippenberg21a.pdf`) and Krnjaic et al. 2022 (their configuration
table, `papers/2212.11498v3.pdf`). Equation numbers checked against
`main.aux` of 2026-11-20 and they all match.

The annotated pages are next to this file:
`appendix_B_parameters_comments.pdf` (pages 2 to 4 of `B.Parameters.pdf`).

A note on the code: every config header says "The arm, model, PPO and
checkpoint sections are illustrative, not thesis values". The trained runs
used them, so that header is out of date. Not changed (code repo).

How to answer: tick one box per point and add a note if you want.

---

## A. Is it true (checked against the code, GAPS and the appendices)

### A13. Stall and lock
**Where:** p. 4, "stall, TBD, open".

The stall length is still open (H waits for it). The lock rule of [A91]
(a seed is locked when two agents each hold one task for 500 steps or more)
is set and reported in the results (`tab:exp:locks`), but has no row. The PF
still defines the stall.

- [ ] Add a lock row, 500 steps, set
- [ ] Does the stall stay in the PF?
- Note:

**Partly fixed ([A109]).** Stall row now reads the fleet-level gap, still TBD. The lock row is not part of this fix.

---

## B. Reasons and sources

### B1. "set" is not in the legend
**Where:** p. 2, the opening paragraph.

The legend has cited, derived, tested, open and design. The tables use
"set" ten times. What is "set" against "open"? Service level 0.99 is set,
skew 1 is open, units per line is open, and all three are our choice. Add
"set" to the legend, or split them into design and open.

- [ ] Add "set" to the legend
- [ ] Use only the five kinds
- Note:

### B2. Skew open, drift tested
**Where:** p. 4. Appendix F treats both the same (pilot values, and the
sweep shows the gain holds over the range). F has a TODO asking you this.
Pick one word for both.

- [ ] Both tested
- [ ] Both open
- Note:

### B3. Reasons in the Source column
**Where:** p. 2, beta "a step standing still counts as a step of travel"
and Delta "half the rotation period". Neither is a source kind. Write
"design" (beta) and "derived" (Delta), and keep the reason in the
appendix.

- [ ] Agree
- Note:

### B4. "Fixed before the main runs"
**Where:** p. 2, the last sentence of the opening, and the captions of B.1,
B.2 and B.5. The main runs are done, and B.1 has no TBD left. Say which
values the runs used and which are still open, once A6 to A13 are
answered.

- [ ] Agree
- Note:

### B5. "Below the cheapest edge"
**Where:** p. 2, c_wait. Every edge costs 1 now, so the clause adds little.
It came from the old example with edges of 0.5. Drop it, or say why the
wait must cost less than a step.

- [ ] Drop
- [ ] Keep with the reason
- Note:

### B6. Two "set" rows without a pointer
**Where:** p. 4, "workstations per section" and "|V_str|". F.5 argues the
sections and G.4.4 the sizing. Point there.

- [ ] Agree
- Note:

---

## C. Names, plain words, symbols

### C1. "Router" and "wider routers"
**Where:** p. 3, four times in B.3. [A106] made "controller" the one name.
Say "the centralised and section-based controllers".

- [ ] Agree
- Note:

### C2. Zones and sections in one appendix
B.3 has "zones p" and B.5 "SKUs per section". The open point of
`method_controllers_comments.md` C1 applies here too.

### C3. A bare eta_i
**Where:** p. 3, "with that agent's eta_i". Say "its own distance labels".

- [ ] Agree
- Note:

### C4. "FC layers"
**Where:** p. 3, hidden width. Code language. Write "vertex embedding
width" and add "head hidden width" (A7).

- [ ] Agree
- Note:

### C5. "PPO core", "epochs/update", "coeff."
**Where:** p. 3. "PPO core" says nothing three times, and the slash and
abbreviations read like code. One plain meaning per row.

- [ ] Agree
- Note:

### C6. "fixed (ablation, none)"
**Where:** p. 3, pooled embedding. Which ablation? The full-view setting
left in [A106], and no config turns pooling off. Drop it unless a run
exists.

- [ ] Drop
- Note:

### C7. Two kinds of round
**Where:** p. 3, L "rounds" and "communication rounds". Call the second
"message hops per timestep".

- [ ] Agree
- Note:

---

## D. Reading order and repetition

### D1. Design rows in a parameter table
**Where:** p. 3, B.3. Five of ten rows (one pass per agent, claim mask,
padding, policy head, critic input) are choices without a number, and they
retell the Method. Be critical. I think they can go, and the table then
lists values only. A reader of an appendix of values looks for numbers.

- [ ] Keep only values
- [ ] Keep as is
- Note:

### D2. Warehouse and demand values under "Evaluation"
**Where:** p. 4, B.5. Q, |K|, |V_str|, sections, skew, drift and lines per
order describe the warehouse and its demand, not how a run is scored. A
table of their own would be easier to find.

- [ ] Agree
- Note:

---

## F. What reads well
- The legend of source kinds is a good idea. A reader sees at once what
  is borrowed and what is ours.
- Every cited value names the table it comes from.
- The references point to the subsection that holds the test.

## The three changes that would help the reader most
1. Give every value the trained runs used, even where the source is still
   open (A6 to A13). A reader of this appendix cannot tell today that every
   run had L = 2, width 32, three zones and 500 000 steps.
2. Settle the source kinds (B1 to B3), so "set", "open" and "tested" each
   mean one thing.
3. Keep only values in B.3 and give the warehouse and demand values their
   own table (D1, D2).
