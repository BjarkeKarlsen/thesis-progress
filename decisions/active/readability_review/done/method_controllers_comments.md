# Comments on "Choosing together"

Scope: `4.Implementation.tex`, `sec:method:controllers` (PDF pages 40 and 41
of `main.pdf`, built 2026-11-18, no newer `.tex`). Checked against the
Introduction (RQ1), the Problem Formulation (`sec:pf:controllers`,
`sec:pf:observations`, the section of a SKU in `sec:pf:tasks`), Appendix C
(`eq:halo`, `eq:claimmask`), `GAPS.md` ([A5], [A6], [A25], [A29], [A32],
[A106]), van Knippenberg et al. 2021 (`papers/knippenberg21a.pdf`) and
`slap-mapd-coupling` on `main` (`8ba3048`): `training/env.py`,
`environment/spaces.py`, `resolution/conflict_resolution.py`
(`move_blocked`), `environment/observation.py`, `environment/zones.py`,
`models/gnn_encoder.py`.

The annotated pages are next to this file:
`method_controllers_comments.pdf` (pages 40 and 41 of the thesis).

Fixed and decided points are removed (full file in `full_2026-11-20/`).

How to answer: tick one box per point and add a note if you want. Nothing in
the thesis has been changed.

---

## B. Reasons and sources

### B1. The centralised controller does not really see the whole warehouse
**Where:** p. 41, "Seeing the whole window", "In a large warehouse one
earlier choice changes the mean very little. So the centralised controller
mostly learns from choices close to the agent".

Be critical. Table IV says the centralised routing sees "the whole
warehouse". This paragraph says it sees L rounds around the agent plus a
blurred mean. I think the hunch holds. What really sets the centralised
controller apart is then the claim mask (no clashes) and the shared credit,
not seeing more. That changes what RQ1 compares. Say it plainly here, and
add it to the Discussion. The heading "Seeing the whole window" also says
the opposite of the paragraph.

- [ ] Agree, say it here and in the Discussion
- [ ] Disagree
- Note:

### B2. Why a mean, and where is it from?
**Where:** p. 41, eq. (47).

A mean loses who chose what. Why a mean and not something that keeps it?
The readout over all vertices is Gilmer et al.'s readout phase, so cite it,
or say it is our own. "Owns" is new: say "all vertices for the centralised
controller, the zone for the section-based". Then V_i^pool may not be
needed.

- [ ] Agree
- Note:

### B3. Where is the halo from?
**Where:** p. 41, "a halo H_q".

GAPS [A6] calls it "the standard way to run a GNN on a partitioned graph".
Cite a source for it, or say it is ours.

- [ ] Cite (which paper?)
- [ ] Say it is ours
- Note:

### B4. Only the section-based controller is overridden at a zone border
**Where:** p. 41, "The zones run in parallel, and two zones may still send
agents onto the same empty vertex at the border".

The centralised controller is never overridden, so it never pays the
override term. The section-based one pays it at zone borders. Is that fair
for RQ1, or is it part of what deciding in zones costs? One sentence of
reason.

- [ ] Agree, add the reason
- [ ] Add to the Discussion
- Note:

---

## C. One name per idea

### C1. Zone and section
**Where:** p. 41, "Each zone does the same on its own part of the
warehouse".

A *section* is the group of workstations a SKU belongs to (PF, the task
part). The *section-based* controller then works in *zones*. The reader
will think a zone is a section. Are they the same? The code cuts the zones
as blocks of consecutive aisles (`zones_by_aisle`, called from
`training/arm.py`), 3 zones in the trained configs (the scaling probe uses
more), and the sections by workstation. How the zones are drawn is not
said anywhere in the thesis, and `tab:modelparams` still says p is "TBD
(sweep)".

- [ ] Rename the controller (for example zone-based)
- [ ] Rename the storage sections
- [ ] Keep both, say they differ and how zones are drawn
- Note:

---

## D. Reading order and repetition

### D1. The claim mask paragraph retells the PF rule
**Where:** p. 40, "The claim mask".

The three cases are the PF rule again (vertex rule, swap rule, no stepping
onto an agent that has not chosen). Here we only need "the rule enters as a
second mask, and waiting is never switched off". v is not named here. The
reader last met v as a neighbour in the PF example. The override term of
the reward (48) is defined in VI-F, after this.

- [ ] Agree
- Note:

### D2. The section-based paragraph holds six ideas and two repeats
**Where:** p. 41, "Section-based".

Halo, crowding, other zones, handover, parallel zones, p = 1. "An agent
belongs to the next zone from the timestep it enters it" and "With p = 1
... is the centralised one" are already in the PF. Split the paragraph and
cut the two repeats.

- [ ] Agree
- Note:

### D3. "Share the reward", and the third "difference in results"
**Where:** p. 41, "The three learned controllers share the network, the
masks, the reward and the training".

The credit in VI-G differs: fleet mean, zone mean, own reward. The PF says
whose reward is one of the three things that follow from how many agents
one decision covers. "Differ only" leaves it out. This is also the third
time we say a difference in results comes from the controller (Method
opening, PF "What the controllers share"). Merge with the PF point or drop.

- [ ] Agree, name the credit
- [ ] Drop the paragraph
- Note:

### D4. Text about the text, and runtime twice
**Where:** p. 40, "This subsection gives how the network carries them out"
and "A timestep therefore takes m runs".

Drop the first. The PF already says one run per agent. Keep the runtime
point once, here or in the PF.

- [ ] Agree
- Note:

---

## E. Figure

### E1. A figure for the halo and the claim mask
A small graph with one zone, its halo strip, and a1, a2 in the three claim
mask cases. Fig. 8 shows the windows but not the halo, and the claim mask
is hard to follow from words alone.

- [ ] Agree
- [ ] No figure
- Note:

---

## F. What reads well
- The opening line says what changes in one sentence.
- "Waiting is never switched off, so an agent always has an action left."
- The reason one shared pass is rejected (no agent would see another's
  choice).
- Zones in parallel with border clashes left to conflict resolution, said
  plainly.

## The three changes that would help the reader most
1. Say what the centralised controller really sees after the mean, and take
   it to the Discussion (B1).
2. Settle zone and section (C1), and say how zones are drawn.
3. Fix the halo sentences to match the code and give the real reason for its
   range (A1, A2).
