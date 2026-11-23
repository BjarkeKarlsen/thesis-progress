# Comments on Appendix D, "Warehouse generation"

Scope: `thesis/Appendices/D.Warehouses.tex` and its own PDF
(`D.Warehouses.pdf`, built 2026-11-18, 8 pages, cover on page 1). Page
numbers below are PDF pages of that file. Checked against
`slap-mapd-coupling` on `main` (`8ba3048`): `instances/generator.py`
(`_build_v2`, `_v2_stations_and_slots`, `fleet_defaults`),
`environment/zones.py`, `training/arm.py`, `training/spec.py`
(`_num_sections`, `instance_params`), `training/warehouses.py`,
`storage/arrival.py` (`trip_distance`, `_refill_scores`), the configs of the
trained runs (`configs/fleet_8/*`, `configs/fleet_16/*`) and
`configs/step12/fleet_{8,16,32,64}.yaml`. Also van Knippenberg et al. 2021
(`papers/knippenberg21a.pdf`, Section 4, Tables 4 and 5), GAPS [A57], [A62],
[A70], [A71], [A73], [A74], [A76], [A77], and the Experiments chapter
(`tab:exp:warehouses`) and Method (`sec:method:controllers`) for the
sections and zones.

The instance report was run again on the step 12 configs (50 seeds per
fleet) into the scratchpad, because the table in the appendix predates
`18fefda` (2026-10-31, [A77]).

The annotated pages are next to this file:
`appendix_D_warehouses_comments.pdf` (pages 2 to 7 of `D.Warehouses.pdf`,
the version before the fixes).

How to answer: tick one box per point and add a note if you want. The
points marked **Fixed ([A108]).** are already applied in the `.tex`.

---

## A. Is it true (checked against the code)

### A4. The two figures are from the old warehouse too
**Where:** p. 6, Fig. D.2, "(b) m = 16, |V| = 348", and p. 7, Fig. D.3.

At 16 agents the warehouse now has |V| = 368. In both figures the
workstations are scattered one by one. Since [A77] they come in groups of
four neighbouring rack faces, one group per section (at 8 agents one group
of four). The reader of the appendix sees a warehouse no run used. Redraw
both from the current configs, in the pygame viewer style of [A104]
(`base.py`), which these figures do not follow yet (green diamonds for
parking, no purple rim).

- [ ] Agree, redraw both
- Note:

### A5. The workstations come in sections, and the appendix never says so
**Where:** p. 4, "Workstations take rack faces selected from the seed and
are also attached as leaves."

Code (`_v2_stations_and_slots`): the seed draws one rack face per section,
and the section's four workstations are the free rack faces nearest to it,
counted in steps along the aisles. There are m/8 sections (1, 2, 4, 8), and
each serves 20 SKUs. That is the most important thing the warehouse does
for storage, because a SKU then has one place to aim for. The appendix
only says "rack faces selected from the seed", and the word "section" never
appears. Proposal: "The seed draws one rack face for each section of SKUs,
and the four free rack faces nearest to it, counted in steps along the
aisles, become that section's workstations." Plus one clause on why, with a
pointer to the Experiments chapter.

- [ ] Agree
- Note:

### A6. The zones of the section-based controller are not explained here, and they do not line up with the sections
**Where:** nowhere in Appendix D. The Method says only "The zones are
blocks of neighbouring aisles" (`4.Implementation.tex`, [A107]).

Code (`zones_by_aisle`, `training/arm.py`): the aisles are cut into p blocks
of consecutive aisles, as equal as possible, the earlier blocks taking the
extra aisle (7 aisles into 3 zones give 3, 2 and 2). A vertex joins the zone
of its aisle band, so a zone is a strip from the front lane to the back
lane, and it cuts across every block, the cross lanes and the one-way loop.
Every trained config uses p = 3 at every fleet size.

The zones and the sections are drawn independently. At 8 agents there is
one section and three zones. Over seeds 0 to 19 the four workstations of a
section span two zones in 2 of 20 sections at 8 agents, 5 of 40 at 16 and
6 of 80 at 32 (scratch script on the generator). So "section-based" does
not mean one zone per SKU section, and a reader will assume it does. This
adds to C1 of `method_controllers_comments.md` (zone and section).

The warehouse appendix is where the shape of a zone can be shown. Proposal:
one short paragraph on how the zones are cut, one sentence that they do not
follow the sections, and the zone strips and section groups drawn in Fig.
D.2. Whether p = 3 stays fixed is the open `tab:modelparams` point already
in the queue.

- [ ] Agree, explain and draw zones and sections here
- [ ] Explain the zones in the Method only
- [ ] Make zones follow sections instead (a model change)
- Note:

### A7. "Within four steps of a lane"
**Where:** p. 4, "This keeps every rack face within four steps of a lane at
every fleet size."

An inner aisle hangs from the near lane and can be four rows long, so its
last aisle vertex is four steps from the lane, and the rack face beside it
is five. "Every aisle vertex" would be four. Small, but GAPS [A74] uses the
same words, so I left it for you.

- [ ] Say "every aisle vertex within four steps"
- [ ] Say "every rack face within five steps"
- Note:

### A8. The loop is joined by every aisle, not only the outer two
**Where:** p. 4, "the two outer aisles join their ends, so together they
form a loop".

Code: "Every aisle crosses the main pair", with a two-way edge between the
two one-way rows at every aisle (Fig. D.2 shows it). True as written, but
the reader pictures one big ring. Say every aisle crosses the pair, so an
agent can turn back at any aisle.

- [ ] Agree
- Note:

---

## B. Reasons and sources

### B1. The one-way central pair and the links are van Knippenberg's too
**Where:** p. 4, "The idea of a generated graph with unit costs that is not
a lattice comes from Knippenberg".

His train-yard graphs (Section 4, Fig. 4) have "two uni-directional lanes
in the center", other two-way lanes joined by "diagonal edges", at least one
between two neighbouring lanes, and start and goal nodes with one or two
neighbours. That is our loop, our links and our leaves. GAPS [A62] says it
was checked in the paper. So more is borrowed than the text says. Cite him
where the loop and the links are made, and say what is ours (rack blocks,
cross lanes, rack faces as leaves).

- [ ] Agree
- Note:

### B2. "The size ... in Knippenberg" holds only at 64 agents
**Where:** p. 7, "The size and the parking count have a source, the size in
Knippenberg".

His Table 4 uses 128, 256, 1024 and 2048 nodes with 32 and 64 agents, and
Table 5 1024 nodes. 16 nodes per agent is 1024 at 64 agents. At 32 agents
his sizes give 4, 8, 32 or 64 per agent, not 16. So the source backs one
point, and "per agent" is our rule. Be critical: I think the text should
say "16 per agent, his 1024 nodes for 64 agents, kept per agent at the
other sizes".

- [ ] Agree
- Note:

### B3. Why 5 shelves per agent, and why parking on rack faces?
**Where:** p. 5, the size paragraph.

The reasons are in the Experiments chapter and [A71]/[A77] (storage kept
scarce, two shelves per SKU, so the rules differ). The appendix should
stand alone, so one clause each.

- [ ] Agree
- Note:

### B4. Why blocks of four rows?
**Where:** p. 4, "This keeps every rack face within four steps of a lane".

That is what it does, not why it matters. [A74] has the reason: with deeper
blocks congestion grew with the fleet partly because of the layout, which
muddies the comparison across fleet sizes. One clause.

- [ ] Agree
- Note:

### B5. "Two agents per dock has a reason"
**Where:** p. 7, "The ratio of two agents per dock has a reason but no
source and no test."

What is the reason? It is not given anywhere in the appendix. Either state
it in one clause or drop "has a reason".

- [ ] Agree
- Note:

---

## C. Names, plain words, symbols

### C1. Storage vertex or shelf
The Setting and the generation text say "storage vertex", the trip
paragraph, the Results and the table say "shelf". The notation table calls
V_str "shelves". One name. I would use shelf everywhere and define it once.

- [ ] Shelf everywhere
- Note:

### C2. Too many names for the floor
"Aisle network", "walkable vertices", "aisle vertices", "plain aisle
vertices", "lanes", "cross lanes", "central loop", "one-way lanes", "rack
rows", "rack faces". The code's names leak in ("walkable"). Pick: aisle
vertex for any vertex an agent can stand on that has no role, and name the
lanes once with a figure.

- [ ] Agree
- Note:

### C3. Parking vertex and endpoint
The notation table calls V_ep "endpoints", the appendix "parking vertices",
and "endpoint" here also means any of the four role sets (Ma's sense). The
reader gets two meanings of endpoint. Say "parking vertices V_ep" in the
notation table too.

- [ ] Agree
- Note:

### C4. "d^trip min to max" in the table
These are the means over the seeds of each seed's shortest and longest
trip. The caption says "means over the seeds", but a reader can read it as
the range over all seeds. Say "mean shortest and mean longest".

- [ ] Agree
- Note:

---

## D. Reading order and repetition

### D1. The Summary retells D.3
p. 2, third paragraph ("enough parking vertices ... finite-task condition
is also met"). D.3 says it all again a page later. Keep one line in the
Summary.

- [ ] Agree
- Note:

### D2. D.3 is long on Token Passing
p. 3, "The guarantee also depends on the Token Passing mechanism" and "The
guarantee means ...". These are about Token Passing, not the warehouse.
Does the reader of a warehouse appendix need them? One sentence that the
guarantee needs Token Passing's own rules would do. Also "If the run were
continued past the measurement horizon, the completeness result concerns
the completion of that finite task set" is hard to read.

- [ ] Shorten to one sentence
- [ ] Keep
- Note:

### D3. The lone check sentence
p. 4, "The generator still checks this property for every warehouse ...".
It sat alone after the docks paragraph and pointed to "this property" (now
fixed to "well-formedness", [A108]). It still floats. Merge it with the
leaf paragraph, which is where well-formedness by construction is argued.

- [ ] Agree
- Note:

### D4. The links appear only in the Conclusion
p. 7, "one link per pair of aisles in each block". The generation text never
says there are links between neighbouring aisles, at rows drawn from the
seed. Say it where the shape is made (and see B1).

- [ ] Agree
- Note:

### D5. The trip distance sits inside "How a warehouse is generated"
p. 5. It is a measure of the warehouse, not a step of generating it, and
it splits generation from the sizes. Move it to the Results, before the
spread it explains.

- [ ] Agree
- Note:

### D6. Empty rows in Table D.1
p. 6, rows 128 and 1024 with no numbers. Your own note says a scale test
is wanted. Until it runs, the empty rows look like a mistake. Drop them or
fill them.

- [ ] Drop for now
- [ ] Run the generator at 128 (it is quick) and fill the row
- Note:

---

## E. Figures

### E1. Redraw Fig. D.2 and D.3 (see A4) and show sections and zones (A6)
Your note at the workstation paragraph asks for a drawing there. One panel
of the 16-agent warehouse with the two sections' workstation groups and the
three zone strips marked would answer A5, A6 and that note at once.

- [ ] Agree
- Note:

### E2. Fig. D.1 is fine
Clear, and the caption names the one point (e2 blocks every path).

---

## F. What reads well
- "A warehouse is built from aisles, not drawn by hand, and every vertex
  with a role hangs off the aisles as a leaf." Leads with the idea.
- The well-formed proof in plain words: a leaf has one neighbour, so no
  path passes through it.
- "The comparison therefore changes the method, not the warehouse it was
  given."
- The Conclusion says plainly what is tested for feasibility only.

## The three changes that would help the reader most
1. Say how the workstations form sections, and how the zones are cut, and
   that they do not line up (A5, A6). Draw both (E1).
2. Redraw the two warehouse figures from the current configs (A4).
3. Credit van Knippenberg for the loop, the links and the leaves, and say
   what is ours (B1, B2).
