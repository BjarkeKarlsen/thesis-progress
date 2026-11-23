# Comments on Appendix A, Notation

Scope: `thesis/Appendices/A.Notation.tex` (`tab:notation`), the PDF
`A.Notation.pdf` built 2026-11-18 (pages 2 to 7, printed 1 to 6). Every row
checked against the chapters `main.tex` includes (`3.ProblemFormulation.tex`,
`4.Implementation.tex`, `5.Experiments.tex`), Appendix C
(`C.ModelDetails.tex`), `styles/eqnames.tex`, the equation numbers in
`main.aux` (20 Nov, they match `styles/xref/A.tex`), `GAPS.md` ([A30],
[A93], [A96], [A105], [A106], [A107]) and `slap-mapd-coupling` on `main`
(`8ba3048`): `configs/*` (`wait_cost`, `move_cost`,
`workstations_per_section`), `environment/storage_estimates.py`
(`ShelfStandingStill`), `evaluation/evaluator.py` (backlog).

`notation_renames.md` is no longer at the workspace root. It was moved to
the trash on 2026-10-16 with every rename applied (alpha, kappa, r and L for
the rounds, logit). `AGENTS.md` and the brief still point to it (D5).

The annotated pages are next to this file:
`appendix_A_notation_comments.pdf`. The notes sit on the PDF from before
the fixes below, so the fixed rows still show the old text there.

How to answer: tick one box per point and add a note if you want.

---

## A. Is it true (checked against the chapters and the code)

### A1. The name of the relative distance label printed as "??"
**Where:** p. 5, the row of eta-tilde.

**Fixed ([A108]).** The row used `\nameeq{eq:relativeeta}`, but
`styles/eqnames.tex` has no entry for it, so the PDF printed
"??eq:relativeeta?? (42)" (log: "No equation name for eq:relativeeta"). The
name is now written out as "relative distance label (42)", the words of
`sec:method:model`. The shared file `styles/eqnames.tex` should still get the
line `\eqname{eq:relativeeta}{relative distance label}`, then the row can go
back to `\nameeq`.

### A2. c_wait is not a parameter of the study
**Where:** p. 2, "a parameter of the study, used in the reward".

**Fixed ([A108]).** Every config has `wait_cost: 0.2`, "after van
Knippenberg et al. (2021)", and the reward paragraph says the two step costs
are his and "taken as they are". Nothing sweeps it. The row now says "used in
the reward, after van Knippenberg (2021)", like the c_move row.

### A3. The demand estimate row
**Where:** p. 4, "Causal estimate of the demand rate".

**Fixed ([A108]).** The row now names the order estimate (7) and says what
the PF says, "Order lines of SKU k per step in the last storage period".
Note the Method calls the same number "the demand estimate"
(`sec:method:storage`), the PF "the order estimate". See C12.

### A4. Two rows for symbols the model no longer has
**Where:** p. 3 and 4, "stock before the update" and "fill level".

**Fixed ([A108]).** x_t^- and x^up_t(k) appear in no chapter and no
appendix. The fill level belongs to the old top-up rule. Arrivals follow the
(R,nQ) rule of (6) since [A93]. Both rows are removed.

### A5. The backlog counts order lines, not orders
**Where:** p. 7, the rows of B_t and B^pick_T.

**Fixed ([A108]).** The formula counts Z^wait_t, which the table calls order
lines, and the code does the same (`evaluator.py:565`,
`num_waiting_orders = len(waiting_lines)`). Both rows now say order lines.
The PF still says "the orders still waiting for stock" twice in "Keeping up"
(`3.ProblemFormulation.tex:1342` and `:1391`). That is for the PF agent.

- [ ] Agree, fix the PF too
- Note:

**Fixed ([A109]).** Both sentences of "Keeping up" now say order lines.

### A6. Released picks include the lines still waiting
**Where:** p. 7, "Picks and put-aways released in the measured window".

**Fixed ([A108]).** The PF counts "one for each order line from the window
that still waits for stock at the horizon" in R^pick_T ([A96]). The row now
says so.

### A7. omega_i(t) of the reward
**Where:** p. 7, the blocked indicator.

**Fixed ([A108]).** The reward (48) uses omega_i(t), the indicator of the
task agent a_i serves, 0 with no task (`sec:method:rl`). The row only had
omega_j(t). It now has both.

### A8. W_T is per completed pick
**Where:** p. 7, "Blocked time per completed task".

**Fixed ([A108]).** (31) averages over C^pick_T, the completed picks.

### A9. Rows for symbols the reader never meets, or meets once
**Where:** p. 2 and 3.

- p_i, the route. No chapter or appendix uses it.
- `\mathrm{priority}`. The priority order is used everywhere, the symbol
  nowhere.
- c-hat, the one-step cost. Defined in Appendix C (C.7) and never used again.
  The Method only points to it for c_wait.
- C_t is listed twice, under the costs and under the task stages.

The table is meant for symbols a reader meets more than once (`AGENTS.md`).

- [ ] Drop p_i and C_t (cost group), keep the priority order without a symbol, keep c-hat
- [ ] Drop all four
- Note:

### A10. The fleet is written two ways
**Where:** p. 2, "Set of agents".

The PF writes it as plain A in "Agents and collisions"
(`3.ProblemFormulation.tex:87`) and calligraphic A everywhere else,
also in the POSG table. One local fix in the PF.

- [ ] Agree
- Note:

**Fixed ([A109]).** "Agents and collisions" now writes the fleet as
calligraphic A.

### A11. "Storage epoch"
**Where:** p. 4, F, "at each storage epoch".

The equation name is "storage update", and the PF uses "storage update"
throughout `sec:pf:storage`. "Storage epoch" is left in `sec:pf:coupling`,
the Method loop (step 6) and the Experiments, once each.

- [ ] Say storage update everywhere
- Note:

### A12. Checked and matching
- Every equation number in the Name column matches `main.aux` (20 Nov) and
  Appendix C (C.2 to C.7).
- Graph rows, V_str "shelves", V_dock "docks", N^+(v), d_G, the zone
  partition (15).
- The task tuple, s_j "pickup place", g_j "delivery place", the release time
  of a pick that waited ([A105]).
- r_t(k,v), Q (10 at every fleet size), h(k) with four workstations
  (`workstations_per_section: 4`), hat h_t(k).
- omega-hat: the average of the last five readings with a pick
  (`ShelfStandingStill`, `deque(maxlen=SHELF_READINGS)`), an input to F and to
  the pickup rule under congestion-aware storage.
- D, K and beta as in (38), with beta = 0 for demand storage.
- q_i(t) with the idle target ([A97]), eta, delta, the communication graph,
  o_i(t), the learning problem, U_i, d_max, O_i.
- pi^cen, pi^sec, pi^dec ([A106]), the masks, the readouts, the move score,
  the value head, Phi_i, the reward weights, the credit (49).
- Lambda_T, f_up, the served share ([A96]), the order service time, the
  split, mean crowding, runtime.

---

## B. Reasons and sources

### B1. Only the step costs carry a source
**Where:** p. 2, c_move and now c_wait.

The distance label is Knippenberg's, the crowding feature follows Pham, the
pickup place and delivery place are Ma et al.'s s_j and g_j. Only the two
step costs cite. In a reference table I would cite none and leave sources to
the chapters, or cite every borrowed symbol. Be critical. I think none is
cleaner, but then c_wait and c_move lose their "after Knippenberg".

- [ ] Cite none
- [ ] Cite every borrowed symbol
- Note:

---

## C. Names, plain words, symbols

### C1. Symbols used more than once with no row
- d^trip_t(k,v), the trip distance. Five times in `sec:method:storage`, in
  (C.2) and three times in Appendix D. The most important one missing.
- pi_theta, the policy being trained, in the learning objective (26) and the
  sentence after it ([A106]). Its row was replaced by pi^dec.
- m_v^(r), the message a vertex gathers in round r, in (43) and Appendix C.
  It also clashes with the fleet size m (see C3).
- gain_n, the seed index n and zeta-bar^(n)_T of the gain test and (37).
- x^new_t(k,v), the units placed at this update, three times in (38) and the
  sentence before it.
- C^pick_T, the completed picks of (31).

- [ ] Add d^trip, pi_theta, gain_n with n
- [ ] Also m_v^(r), x^new, C^pick_T
- Note:

### C2. w: neighbour vertex and workstation (known)
**Where:** p. 2, "v, w in V".

w is a neighbour vertex in this row, in the move score (46) and in the claim
mask (C.6). Fig. 15 calls the workstation w, and the trip distance (C.2)
sums over workstations w in hat h_t(k). The workstations of the examples are
W_1, W_2, and W is also W_T (mean blocked time) and W-bar_s(v) in (40).

Proposal: workstations are W_1, W_2 in every figure and formula, w is only
ever a vertex. Rename the mean blocked time to omega-bar_T. It is the mean of
the indicator omega_j, so the letters then tell the story (see C11).

- [ ] Agree
- [ ] Other:
- Note:

### C3. "Message" means three things (known)
**Where:** p. 6, xi_j, xi-bar_w, phi_r.

- xi_j(t), the agent message (44).
- xi-bar_w(t), named "vertex message". It is the message of the agent
  standing on w, so the name says the opposite of what it is.
- phi_r, the "message function", and m_v^(r) of (43), what a vertex gathers
  from its neighbours in one round.

Proposal: "message" only for agents (xi). xi-bar_w is "the message at w".
For (43) say "what a vertex gathers from its neighbours", and if m_v^(r) gets
a row, give it a letter that is not m.

- [ ] Agree
- Note:

### C4. Zone and section (known, controllers C1)
**Where:** p. 2, Y_q "zone", p. 3 h(k) "SKU's section", p. 6 pi^sec
"section-based policy", p. 5 s^(q)_t "zone-local state".

The table repeats the mix in its own names. Whatever the author picks in
`method_controllers_comments.md` C1, the rows follow.

- [ ] Follow C1 there
- Note:

### C5. s: pickup place, state and period
s_j is where a task picks up, s_t the state, s^(q)_t a zone's state, and in
(40) s is a storage period (W-bar_s(v), S_t(v)). Be critical. s_j comes from
Ma et al. and s_t is the RL norm, and they seldom meet in one formula. I
would keep both and only rename the period index in (40).

- [ ] Rename the period index only
- [ ] Leave it
- Note:

### C6. h(k) reads as "home"
**Where:** p. 3, "SKU's section".

h(k) is the section, but fixed storage has home shelves, and Appendix C
writes "with h(k) in place of hat h_t(k) for the homes of F_fix". h is also
the vertex embedding h_v^(r) and the pooled mean h-bar_i(t). A reader will
take h(k) for a home shelf.

- [ ] Rename the section (letter?)
- [ ] Keep h(k)
- Note:

### C7. B and Q, each twice
- Backlog B_t and active tasks calligraphic B_t sit in the same formula,
  B_t = |Q_t| + |B_t| + |Z^wait_t|.
- Pallet size Q next to calligraphic Q_t, the waiting tasks. The rename of
  30 Sep (round count Q to L) removed exactly this clash and its footnote.
  [A75] brought Q back as the refill, now pallet, size.

Be critical. The fonts differ, so a careful reader copes. The backlog
formula is where it hurts, because both B are in one line.

- [ ] Rename the backlog
- [ ] Leave both
- Note:

### C8. q four ways
q is the units of a line and q_j of a task, q^(i) the share shelf v_i gives
in the pickup rule (10), the zone index in Y_q, s^(q)_t, u^(q), and the
current target q_i(t). The 30 Sep decision kept these because they never
meet. Two things are new. q^(i) puts a shelf index in the superscript where
s^(q)_t puts a zone. And q_i(t), the target of agent i, and q_j, the units of
task j, differ only by the index letter, while (19) defines q_i(t) from task
j. Be critical. I think the hunch holds for the target, less for the rest.

- [ ] Rename the current target (letter?)
- [ ] Leave it
- Note:

### C9. v_1, v_2 numbered twice
`sec:pf:env` numbers every vertex once, V = {v_1, ..., v_|V|}, "only used to
break ties". The pickup rule (10) then calls the shelves v_1, v_2 by their
distance to the workstation. The same names, another order.

- [ ] Write the listed shelves as v_(1), v_(2)
- [ ] Leave it
- Note:

### C10. omega and omega-hat
**Where:** p. 4, omega-hat_t(v).

The blocked indicator omega_j(t) and the standing-still estimate
omega-hat_t(v) share a letter. That is good if it is on purpose, because
omega-hat is the mean of the blocked steps of recent picks at a shelf. Then
say it in the omega-hat row ("the blocked steps omega of recent picks from
v, averaged"). Appendix C, `app:measures:blocked`, already compares them.

- [ ] Agree, say it in the row
- Note:

### C11. Words in the Meaning column that the chapters do not use
- "boundary protocol" (H_q, s^(q)_t). The chapters say halo and "a strip just
  past its edge".
- "Admissible" (F calligraphic, Pi). The PF says "the set of them" and "the
  set of controllers studied".
- "transition kernel". The PF table says transition rule, its text both.
- "Vertices at which an idle agent may remain without blocking transit". The
  PF says "where an idle agent waits out of the way".
- x_t "at vertex v", cap(v) "Storage capacity of vertex", b_k "Capacity
  consumed". The PF says shelf and room ([A103], [A105]).
- V_i^(d_obs) "Its vertices, those within ...". "Its" points at nothing in a
  table.

- [ ] Use the chapters' words in all six
- Note:

### C12. One name per idea, outside this table
Found while checking rows. Each is one word in another file.
- "demand estimate" (`sec:method:storage`, Appendix H) and "order estimate"
  (the equation name) for hat rho.
- "parking vertex" (`sec:method:rl` twice, Experiments twice, Appendix D) and
  "endpoint" (PF, Token Passing paragraph) for V_ep.
- "end vertex" in the Token Passing paragraph (`4.Implementation.tex:637`,
  `:639`, `:642`), after [A105] made it "where the task delivers".
- "storage vertex" in Appendix C (`C.ModelDetails.tex:23`). [A105] keeps it
  only in Appendix D.

- [ ] Agree, one name each
- Note:

### C13. The Name column shows the equation's name
**Where:** p. 7, B^pick_T "keep-up check (27)".

Where a row has an equation, the Name column shows the equation's name, not
the symbol's. Mostly fine. But B^pick_T is not in (27), only in the sentence
after it. Call it "backlog by kind" with no number.

- [ ] Agree
- Note:

---

## D. Reading order and repetition

### D1. A reader of the appendix alone cannot place the numbers
**Where:** p. 2, the caption.

An appendix is its own paper. (15) is an equation of the thesis, (C.3) one
of Appendix C, and neither is said. One sentence above the table: "Numbers
in brackets are equations of the thesis, C.n those of Appendix C."

- [ ] Agree
- Note:

### D2. The cost group header is text about the table
**Where:** p. 2, "five symbols share the base letter c, each with a
distinct role".

It explains the table, not the symbols, and the five only holds because C_t
is counted, which is not a cost and is listed again under Tasks. Header
"Movement cost", drop the C_t row there (A9).

- [ ] Agree
- Note:

### D3. Rows not in reading order
Z^wait_t sits between s_j and g_j. t_z comes after zeta^ord_z, which uses
it. lambda_task is last under Tasks, but the reader meets it in the
research question. Put each group in the order the chapters introduce the
symbols.

- [ ] Agree
- Note:

### D4. A second copy of the table
`Chapters/2.Notation.tex` holds the same table with the same labels
(`app:notation`, `tab:notation`). `main.tex` does not include it, and it was
identical to this file before the fixes above. The [A108] fixes went into
`A.Notation.tex` only.

- [ ] Delete `2.Notation.tex`
- [ ] Keep it in sync
- Note:

### D5. `notation_renames.md` is gone
`AGENTS.md` ("Known clashes and the suggested renames are in
`notation_renames.md`") and the subagent brief point to it. It went to the
trash on 2026-10-16, with every rename applied. Either point to C2 to C9 of
this file, or drop the sentence.

- [ ] Drop the sentence
- [ ] Point here
- Note:

---

## E. Figures

None. A table is the right form.

---

## F. What reads well
- One row per symbol, a short name and a meaning in words.
- The group headers make a symbol easy to find.
- The equation names (vertex rule, task definition) are the same words the
  chapters use, so the table and the text meet.
- The [Axx] tags on the rows say where each row came from.

## The three changes that would help the reader most
1. Settle the clashes the reader will trip on: w (C2), message (C3), zone and
   section (C4), h(k) (C6). Each needs one choice, then the table, the
   chapters and the figures follow.
2. Add the missing symbols, first of all d^trip, pi_theta and gain_n (C1),
   and drop the ones nobody meets (A9).
3. Tell the standalone reader what (15) and (C.3) are, and order the rows as
   the chapters introduce them (D1, D3).
