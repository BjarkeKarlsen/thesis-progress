# Comments on "A reference point"

Scope: `4.Implementation.tex`, `sec:method:reference` (PDF page 45 of
`main.pdf`, printed page 44, built 2026-11-20 15:33). Checked against the
Background (`sec:bg:mapf`, `sec:rw:mapf`), the Problem Formulation (the
well-formed paragraph, `eq:task`, the scope item "One agent per workstation
at a time"), the Method opening loop, `sec:method:assignment`,
`sec:method:resolution` (Fig. 15), the Results (`tab:exp:served`,
`tab:exp:locks`, RQ2), Appendix E (`app:load:next`), `GAPS.md` ([A5],
[A19], [A28], [A77], [A91], [A99], [A106]), Ma et al. 2017
(`papers/3091125.3091243.pdf`), van Knippenberg et al. 2021
(`papers/knippenberg21a.pdf`) and `slap-mapd-coupling` on `main`
(`8ba3048`): `planners/token_passing.py`, `planners/base.py`,
`planners/driver.py`, `instances/generator.py`,
`tests/unit/test_token_passing_planner.py`.

The annotated page is next to this file: `method_reference_comments.pdf`.

**Fixed in the thesis on 2026-11-20 ([A108]):** A1, A2.

How to answer: tick one box per point and add a note if you want.

---

## A. Is it true (checked against the code and the paper)

### A1. Token Passing runs under every storage rule
**Fixed ([A108]).** The text said "Token Passing also runs under demand
storage". The Results report it under fixed, demand and congestion-aware
storage (`tab:exp:served`, `tab:exp:locks`, the RQ2 paragraph). Now "Token
Passing runs under every storage rule".

### A2. The vertex rule is not Ma et al.'s, so "kept as published" was not true
**Fixed ([A108]).** Ma et al. (Section 3.1) forbid only two agents on one
vertex and two agents swapping. So an agent may follow another into the
vertex it leaves. The code holds a vertex from one step before arrival to
one step after leaving (`token_passing.py`, docstring and `_reservations`),
and [A28] logs it as a difference. The text gave the rule but not that it
differs, and the last paragraph said Token Passing "is kept as published".
Now "Unlike in Ma et al., where an agent may follow another into the vertex
it is leaving, ..." and "Token Passing's task rule is kept as published".

### A3. The loop at the Method start does not fit Token Passing (outside this section)
**Where:** p. 35, "All controllers, and the Token Passing reference, run in
the same loop", step 2 "by the same rule for every controller" and step 3
"chooses one intended move ... from what it sees (Table information)".

`method_storage_comments.md` A3 already says step 2 differs. Step 3 differs
too. Token Passing does its token round in step 2 (`assign` of the
`SelfAssigningPlanner`, `base.py`), and in step 3 it only returns the next
vertex of the path it planned (`plan`, `driver.py`). It does not choose
from a window of Table information, it reads every path in the token.

**Proposal for the loop:** "Token Passing runs in the same loop, but it
chooses its own tasks in step 2 and in step 3 follows the path it planned."

- [ ] Agree
- [ ] Disagree
- Note:

### A4. Is "a reference point" still the whole role? Be critical
**Where:** p. 45, "It checks that the learned controllers can compete with
a classic planner".

Since [A99] the Results measure service time and the gain of demand storage
for Token Passing only, because the learned controllers do not keep up.
Token Passing also sets the main load (Appendix E, 0.6 of its capacity) and
several storage values (Appendix G). So the reader meets a "reference point
outside the main comparison" and then finds it carries the main result. My
view: the hunch holds. One sentence here should say that Token Passing sets
the load, and the Discussion should say why the reference became the only
measurable case. Whether the first sentence ("not part of the comparison
the research questions make") still stands is your call.

- [ ] Agree, say it here
- [ ] Leave it, the Results explain it
- Note:

### A5. "Do not have this wait" is one-sided. Be critical

**Fixed ([A109]).**
**Where:** p. 45, "The learned controllers take their tasks by the
assignment rule and do not have this wait."

True, the assignment rule ignores who is heading for a workstation. But the
learned controllers lock at the same workstations (Fig. 15, [A91]), and
Token Passing never does. My view: add one clause, "but they can lock
there instead (Section When moves still clash)", so the reader gets both
sides of the same queue.

- [ ] Agree
- [ ] Disagree
- Note:

### Checked and matching
- An agent whose path has ended asks for the token, one at a time in order
  of index (`assign`, `sorted(locations)`, `_asks`).
- The task closest in moves to its pickup, among tasks whose pickup and
  delivery vertex are not where another path ends (`_take_a_task`, hop
  distance, ties by task id). Ma et al. also take the smallest h-value to
  the pickup.
- Every other agent stands where its path ends from then on (`_reservations`,
  `resting`). Same as Ma et al. ("an agent rests ... forever").
- No task, stay, or move to the nearest free endpoint if it stands where a
  waiting task delivers (`_stay_or_park`). Ma et al., Line 14 and 16. The
  code only parks on non-task endpoints, which is what "endpoint" means in
  the PF.
- Conflict resolution never changes a plan. A test asserts it on generated
  well-formed warehouses (`test_token_passing_planner.py`, `last_overridden`).
- Token Passing does not use the assignment rule (`SelfAssigningPlanner`
  replaces it as the env's assigner).
- Every warehouse is well-formed. `generate_valid_instance` rejects a layout
  that fails `check_well_formedness`, and no run config turns it off.
- Only one agent heads for a workstation at a time. Follows from the task
  rule, since the agent's path ends on the workstation. The same holds for
  a shelf and a dock. Appendix E.4.6 measures the wait (74 to 158 steps
  against 17 to 25 moving).
- Knippenberg et al. compare with A*, ICBS and ICTS (Section 6.1). True as
  a fact, see B4 for whether it fits.

---

## B. Reasons and sources

### B1. Why Token Passing, and not TPTS or prioritised A*?
**Where:** p. 45, "Token Passing ... is the only router that does not
learn".

The choice has no reason in the text. The Background says Token Passing
with Task Swaps finishes tasks sooner. [A28] gives why not prioritised A*
(it stalls in dead-end corridors). Why not TPTS is not logged. I guess:
less computation, the same promise on well-formed warehouses, and no
re-tasking, which the learned controllers do not have either. One clause.

- [ ] Agree, reason: ...
- Note:

### B2. Why Token Passing never locks at a workstation (carry forward, [A91])

**Fixed ([A109]).**
**Where:** p. 45, the vertex rule and the well-formed sentence. And p. 42,
"Token Passing plans ahead and does not meet this circle".

Both halves of the reason are here, but nothing connects them to Fig. 15.
[A91] says it: a path keeps a vertex from one step before arrival to one
step after leaving, and every warehouse is well-formed, so it does not lock.
"Plans ahead" in `sec:method:resolution` is not the reason and points
forward to this section.

**Proposal**, after "So conflict resolution never has to change a plan":
"Two agents therefore never ask for each other's vertex, so Token Passing
never meets the circle at a workstation of Figure~\ref{fig:workstationlock}."
And in `sec:method:resolution` drop "Token Passing plans ahead and does not
meet this circle" (that section's agent owns the edit).

Note: the order matters. Fig. 15 comes before this section, so pointing
back is fine here.

- [ ] Agree
- Note:

### B3. The order of the agents is our choice
**Where:** p. 45, "the agents ask one at a time in order of index".

Ma et al. send the token "to each agent that requests it, one after the
other" and leave the order open. The code docstring says so. Two words,
"we choose", or "in order of index, which Ma et al. leave open".

- [ ] Agree
- Note:

### B4. "The role that A*, ICBS and ICTS play". Be critical
**Where:** p. 45, last sentence of the long paragraph.

Knippenberg et al. (Section 6.1, Table 2) run them on one-shot MAPF
benchmark maps and count solved instances within 30 seconds. Ours is a
lifelong warehouse scored by service time. So the role is only alike in
"a classic method to compare with". ICBS and ICTS are also never explained.
My view: drop the sentence. The first paragraph already gives the role.

- [ ] Drop it
- [ ] Keep it
- Note:

---

## C. Names, plain words, symbols

### C1. "End vertex"
**Where:** p. 45, "pickup and end vertices", "on to the end vertex", "the
end vertex of a waiting task".

The PF names it "where it delivers", `g_j` (and `s_j` for the pickup), as
Ma et al. do. "End" also clashes with "where another agent's path ends" in
the same sentence. Use `s_j` and `g_j`, or "where it picks up and where it
delivers".

- [ ] Agree
- Note:

### C2. "Router"
**Where:** p. 45, "the only router that does not learn", "because the
router is not what this thesis tests".

[A106] made "controller" the one name. Token Passing is not one of the
controllers, and the Introduction calls it "a classic planner". Use
"planner" both times.

- [ ] Agree
- Note:

### C3. "Space-time A*"
**Where:** p. 45, "plans a path to the pickup and on to the end vertex by
space-time A*".

Not in the Background. Plain words: "It then plans the shortest path, in
steps, to the pickup and on to where the task delivers, keeping clear of the
paths already in the token." Cite A* if the name stays.

- [ ] Agree
- Note:

### C4. "Its guarantee holds only on well-formed warehouses"
**Where:** p. 45.

Which guarantee? The PF says it ("to promise that every task is finished").
"Only" reads as if well-formed were needed. Ma et al. show it is enough,
and [A28] says the text must not call it necessary. Proposal: "It promises
to finish every task when the warehouse is well-formed, and every warehouse
is built to be one."

- [ ] Agree
- Note:

### C5. "Than its agent drives"
**Where:** p. 45, "a line can wait longer for its turn than its agent
drives".

The style rule says "move to", not "drive". "...longer for its turn than
its trip takes."

- [ ] Agree
- Note:

---

## D. Reading order and repetition

### D1. The second paragraph restarts the first
**Where:** p. 45, "Token Passing ... is the only router that does not
learn".

The first paragraph already says it is a classic planner next to the
learned controllers. The Background (Lifelong MAPD solvers) already says
the token holds every path and each agent picks its own task. Point back to
it and keep only what is added here: the order, which task, the parking
rule, the vertex rule.

- [ ] Agree
- Note:

### D2. One long paragraph with five ideas
**Where:** p. 45, the paragraph from "Token Passing" to "(2021)".

It holds how a task is chosen, how a path is planned, the vertex rule and
conflict resolution, the own task rule, the guarantee and Knippenberg. Split
in two: how it chooses a task (with "so it does not use the assignment
rule"), and how it plans a path (with the vertex rule, the lock of B2 and
the guarantee).

- [ ] Agree
- Note:

### D3. "Chooses its own tasks" said three times
Here, at the end of `sec:method:assignment` (pointing forward to here), and
proposed for the loop (A3). Say it in the loop and here, and drop the
forward reference in the assignment section, or keep it there as the one
place and say it here only as "as said in Who takes which task".

- [ ] Loop and here
- [ ] Assignment section and here
- Note:

### D4. The workstation wait is also a scope item in the PF
**Where:** p. 45, "Token Passing lets only one agent head for a workstation
at a time", and p. 34, scope item "One agent per workstation at a time".

The PF already says it and why it is kept. Here keep the mechanism in one
sentence (it follows from the task rule, since a path ends on the
workstation) and how the gain is read, and point back to the scope item.

- [ ] Agree
- Note:

---

## E. Figures

### E1. A figure for the task rule? Be critical
A small picture: a1's path ends on workstation w, a2 is free, the pick to
w waits and a2 takes a task elsewhere. The rule "whose pickup and delivery
are not where another path ends" is the hardest sentence here, and the wait
it causes is what the Results lean on. My view: helpful, but low priority.
The words work once C1 is fixed.

- [ ] Figure
- [ ] No figure
- Note:

---

## F. What reads well
- The token round is told in the order it happens: ask, take a task, plan,
  others stay put, or park.
- "Every other agent is taken to stand where its path ends from then on."
  Short and exact.
- The workstation paragraph gives the cause and then how to read the gain.

## The three changes that would help the reader most
1. Say why Token Passing never locks, here, and drop "plans ahead" from
   When moves still clash (B2).
2. Say what Token Passing does for the thesis now: it sets the load and is
   the one controller whose gain is measured (A4).
3. Split the long paragraph and use the PF's names, `s_j`, `g_j`, planner
   (D2, C1, C2).
