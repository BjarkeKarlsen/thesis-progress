# Critical read of the thesis and appendices (2026-10-30)

Scope: everything `main.tex` includes (`Chapters/2`–`6`) and the appendices
`A`–`L` (not `C.ModelDetailsV1.tex`). Nothing has been changed. This file only
lists problems and questions, to be worked through one at a time.

The yardstick is the author's own rule from the comment at
`Chapters/2.Introduction.tex:147-150`:

1. **Cite, don't argue.** A standard part (MAPF action model, POSG, PPO,
   shaping, order-up-to) is cited, not defended.
2. **No forward references.** Explain one subject fully, then the next. Later
   text points back to earlier text, never the other way round.
3. **Appendix test.** Does the appendix make the thesis easier for a reader
   new to the subject, or does it hide something the main argument needs, so
   the reader has to flip back and forth?

Line numbers refer to the files as they are today.

---

## Part A. What belongs in the appendix

### A1. The model's core definitions live only in Appendix C (move back)

`app:defs` (`Appendices/C.ModelDetails.tex:375-595`) holds the formal
statement of nearly every object the main argument runs on. The main text
gives a word version and points there. A reader of Method cannot follow it
without the appendix open. Objects that only exist in the appendix:

| Object | Used in the main text at | Verdict |
|---|---|---|
| field of view `eq:localsubgraph` | Intro 1008, 1044; Background 94 | main text. Intro:1045 even says "already defined in Section pf:env", which is no longer true |
| congestion feature `eq:congestion` | Intro 1008-1027, reward, crowding | main text |
| estimates ρ̂, μ̂, ŵ `eq:estimates` | storage update, storage rules | main text (three short lines) |
| current target, distance label `eq:currenttarget`, `eq:potential` | observation, reward shaping | main text |
| free-agent condition `eq:free` | Intro 810-819 | main text, or drop the label and keep the sentence |
| pickup rule `eq:pickuprule` | Intro 754 | main text or drop. The prose already says it |
| zone partition, section policy, halo | Intro 910, 979; Impl 190 | main text. The centralised policy is in the main, its twin is not |
| observation function `eq:obsfunction` | Intro 1207 | main text, it is "the only element that depends on the architecture" |
| blocked time `eq:waiting`, mean crowding `eq:crowding` | Measures, Table `tab:measures` | main text. These are the measures RQ3 reads |
| trip distance, assignment rule | Impl 54, 129 | main text (Method) |
| features, action mask, claim mask | Impl 240-271 | main text (Method) |
| message passing, readout, move score, pooled readout | Impl 339-413 | main text. Section "Model architecture" is unreadable without them |
| decision problem `eq:decisionproblem` | Intro 1522-1528 | see Q5 |

Appendix C should keep worked examples and derivations only.

### A2. Content that now exists twice (pick one home)

The rewrite of 2.Introduction moved some things back into the main text, but
the appendix copies are still there. These are **duplicate LaTeX labels**,
so references silently resolve to one of them:

- `eq:actions`, `eq:transition`, `eq:vertexconflict`, `eq:swapconflict`:
  Intro 170-202 and C 389-418
- `eq:feasiblestorage`, `tab:storagematrix` and the capacity matrix
  example: Intro 304-360 and C 22-69
- `eq:storageupdate`, `eq:storageobjective`, `eq:coupling`: the "new part"
  and the "old part" of Intro 274-736 (both are live, not commented out)
- `eq:tripdistance`: C 526 and D 198

### A3. Appendix C sections that do belong there, or can go

- Arrivals formula `eq:arrivals` (C 84-110). Fine in the appendix, it is
  the cited order-up-to policy. Main text names and cites it.
- Ties in the storage objective (C 129-138). One sentence in the main text
  covers it (Impl 108-111 already does). Delete the appendix section.
- `tab:posg` (C 156-175). Fine as reference.
- Which congestion values a controller reads (C 212-228). One sentence in
  the main text. Delete.
- Observation example table (C 229-247). Repeats Intro 1093-1095. Delete.
- Distance-label bound (C 248-272). A standard property of shortest-path
  distance (triangle inequality). Cite, one sentence, delete the section.
  Intro 1082-1085 currently argues it and forward-refers to it.
- CRAMP comparison, put-away service time, κ_T (C 283-306). Fine, or one
  line each in the main text.
- Blocked time against the edge estimate (C 329-336). Useful
  clarification, could be one sentence in Measures.
- Deadlines and re-tasking (C 337-372). Fine in the appendix, but the main
  text (Intro 1617-1625) already says most of it.
- "Capacity at the docks" (C 373-374) is an **empty subsection**.

### A4. Well-formedness was removed from the main text but is still relied on

The paragraph is commented out (Intro 262-271), but:

- Impl 159: "Its guarantee depends on that task rule (Section~pf:agents)".
  The section no longer mentions the guarantee.
- Impl 566-570 refers to the well-formedness check and to a "choice ...
  noted as open there" in pf:env that is no longer there.

Appendix D is the right home for the definition. The main text needs one
sentence where Token Passing is introduced (Method, controllers) saying the
warehouses are built so that its guarantee holds, with the pointer.

### A5. Experiment appendices D–L

These are calibration papers and belong in appendices. Two results are part
of the argument, not calibration, and need one sentence each in the main
text:

- **App E**: the main load is 0.6 × Token Passing's capacity. This sets the
  operating point of RQ1. Impl 703 only says "come from a pilot".
- **App K**: Token Passing reproduces Ma et al. This is the evidence that the
  simulator is right. The main text only mentions it from Measures
  (Intro 1408), not where validation is discussed (Impl 718-726).

App H fills in stalls, which the main text sends to `sec:impl:logging`
(Intro 1395), but that section does not define a stall.

---

## Part B. Reading order and forward references

### B1. Background comes after the Problem Formulation

`main.tex` order: Introduction (incl. Project Description and Problem
Formulation) → Background → Method. The Problem Formulation uses MAPF,
MAPD, POSG, GNN, parameter sharing and lifelong service time, which are only
explained afterwards. Background then forward-refers into the formulation
(`nref{eq:potential}`, `eq:localsubgraph`, `eq:commgraph`,
`sec:pf:observations`) to explain itself. This is the largest reading-order
problem in the thesis. See Q1.

### B2. Count of forward references in the Problem Formulation

From Intro line 98 on, ignoring comments: 21 references into appendices and
17 into Method or Implementation (`sec:method:rl` ×4, `sec:method:model`
×4, `sec:method:resolution` ×2, `sec:impl:logging` ×2, ...). Most can go
once A1 is done and the "how it is computed later" sentences are cut.

### B3. Storage section: two versions, and it uses tasks before they exist

- The "new part" (Intro 274-476) and "old part" (479-658) both compile.
- The new part ends with the stock condition `eq:coupling` and reservations
  `r_t` (453-468), using `k_j, s_j, q_j, t_j^released`. Tasks are defined
  one subsection later (`eq:task`, 698). The old part then defines the stock
  condition again in the task section (723).
- The new part's notation clashes with the rest of the thesis:
  `τ_t` (demand) vs task `τ_j`, `θ_t` (traversals) vs policy weights `θ`,
  `w_t` vs vertex `w`, `K` the congestion term vs `K` the SKU set (old part
  uses `𝒦`), `λ` as weight vs `λ_task`, and it mentions `α` (447) but the
  formula has none. The old part's `ρ̂, μ̂, ŵ, β` match Method and the
  appendices.
- New part's third condition is `= y_t(k)`, old part's is `≤ y_t(k)`. The
  old one is right, since units that fit nowhere are not placed.
- New part uses `V_rcv`, old part `V_dock`. See D3.

Suggested order: storage state and capacity → how stock changes and the
storage update → storage objective. Stop there. The stock condition and
reservations go in the task section, which then points back to `x_t`.

### B4. Controllers section is overloaded and runs ahead

`sec:pf:controllers` (Intro 836-1027) covers controllers, zones, the critic
design, the centralised factorisation, the claim rule, the section and
decentralised policies, shared assignment, and the congestion feature.

- It uses `o_i(t)`, the field of view and `δ_i(t)` before
  `sec:pf:observations` introduces them.
- The critic paragraph (920-931) is a training choice and refers to
  `sec:method:model`. It belongs in Method/Training, where the credit
  `eq:credit` is.
- The congestion feature paragraph talks about its reward weight before
  any reward exists (1004-1006, 1021).

Suggested order: what a decentralised agent sees (field of view, distance
label, crowding) first, then the controllers, which can then say "the
section-based controller sees the zone version of the same thing".

### B5. Smaller ordering issues

- Intro 797: forward reference to `eq:waiting` (blocked time) in the task
  lifecycle, before blocked time is defined.
- Intro 1395: stall, sent to `sec:impl:logging`, which does not define it.
- Intro 1323: Δ "set by a sweep (Table storageparams)", an appendix table.
  Fine as a pointer, but it is the only sentence about it.
- Intro 1264-1274: credit per decision group, forward to `sec:method:training`.
- Intro 104-116 promises the order "environment, agents, storage, work,
  controllers, what a decentralised agent can see, ...". If B4 is accepted,
  update this paragraph.

---

## Part C. "Cite, don't argue"

- **MAPF action model** is cited twice (Intro 140 and 185). Keep one.
- **Counting-function storage state** (Intro 292-302 and again 490-503).
  Three bullets defend a standard modelling choice plus "a simpler map would
  ...". One sentence is enough.
- **POSG** (Intro 1150-1182). "A partially observable stochastic game is
  the standard model" has `% TODO cite`. The plain-language list of all
  eight parts is textbook. Cite, keep the tuple, keep only what is specific
  to this thesis (the observation function differs per architecture).
- **Chain rule** for the centralised policy (Intro 954-958). Cite Wen
  et al., cut the justification.
- **Potential-based shaping** (Impl 287-297). Argued in Background (65-71)
  and again in Method, including "a naive reward ... loiters". Cite Ng and
  Devlin once.
- **Action masking against van Knippenberg** (Impl 255-262). The contrast is
  fine in one clause. "RLlib has no built-in masking" is an implementation
  detail inside Method.
- **Congestion and emergence** (Background 112-153). Tragedy of the commons
  is a long argument for "congestion is an externality". Also uses the
  banned "internalises" (119), dashes, and refers to a
  "congestion-sensitivity factor" that no longer exists (see D9).
- **Related work** describes centralisation as a spectrum of "information
  regimes" (Background 245), a banned term.

---

## Part D. Inconsistencies found along the way

- **D1. What is the main result?** Intro 75-77 and App C 275-277: "gain in
  mean service time of **picks**" / "share of route time". Measures
  (Intro 1399, A68): the result is **order** service time `ζ̄_T`. App F 46
  also says picks. One of them has to win.
- **D2. Order completion is defined twice, differently.** Intro 680: an order
  is complete when it **leaves** at a dock. Intro 1459: complete when its
  **last line is delivered**, "defined in Appendix measures", which does not
  define it.
- **D3. Vertex-set names.** `V_work`/`V_del` and "delivery vertices"/
  "workstations" (App D), `V_dock`/`V_rcv` and "docks"/"receiving vertices".
- **D4. Starting stock contradicts itself.** Impl 673-684 and App H: `x_0`
  is random per seed. App C 113-128: `x_0` is computed from popularity, and
  "a random start would make fixed storage a weak baseline". Impl instead
  solves that through home shelves that are not the `x_0` shelves.
- **D5. Token Passing scope.** Impl 161-163: only under fixed storage at the
  main loads. Experiments `tab:exp:rq1` has a "reference planner" row with
  gains under `F_dem` and `F_cng`.
- **D6. Related work says** the baselines this thesis compares against use
  CBS (Background 197-198). Token Passing here uses space-time A*.
- **D7. Stale TODO** at Background 204-209 says PICO and CRAMP could not be
  found, while both are cited (`li2022pico`, `pham2024...`).
- **D8. Experiments mock-up** says "the simulator currently draws pickups
  uniformly" (5.Experiments, Orders paragraph) and opens with "moving stock
  in response to traffic", but stored stock never moves.
- **D9. Congestion switch.** Background 151 and 224, and App C 243, refer to
  a congestion-sensitivity factor/ablation. Intro 1004-1006 says the weight
  is the same for every controller and not varied.
- **D10. Meta-text.** Impl 7-18 ("Nothing below changes a definition"),
  Impl 535-539 ("per the contract stated at the top of this file"),
  Impl 40-41 ("a reader who stops here already knows ..."), Intro 110-116.
- **D11. Small slips.** Intro 143 "vertex;." Intro 1588 "involvment",
  "Therefore, no humans". Intro 775 and 1051 "running example" (rule says
  name it). Dashes in Background and Impl 290, 325. A comment-to-self at
  Intro 163 and a spacing note at D 82.

---

## Status after the author's answers (2026-10-30)

- **Q1 closed.** Background stays where it is. B1 is dropped as a change. Only
  the Background's forward references into the formulation remain an issue.
- **Q2.** Standard rules from the literature (vertex rule, swap rule, move rule,
  action set) do not need to be in the main text and can be cited. Every
  definition is decided one at a time, and the author is asked before any is
  moved.
- **Q3.** Under discussion. The new part is the main explanation and
  `C.ModelDetailsV1.tex` the deep one (timing of arriving stock, arrivals,
  objective and ties). The old part goes. See the answer in chat for the
  differences that still need a decision.
- **Q6 answered by GAPS `[A68]`.** The result is the mean order service time,
  from release until the order leaves at a dock. `[A68]` revises `[A50]`. So
  D1 and D2 are drift. Intro 75-77, App C 275-277 ("share of route time"),
  App F 46 and the order completion paragraph at Intro 1459-1465 are out of
  date.
- **D4 answered by GAPS `[A69]`.** One random start for every rule, with
  class-based homes for fixed storage. App C 113-128 is out of date.

## Part E. Questions for the author

**Q1. Background before or after the Problem Formulation?** Today the
formulation comes first and Background explains itself through it. Should
Background (and Related Work) move before the Problem Formulation, so the
formulation can just cite? Or should Background stay short and the
formulation carry its own citations?

**Q2. Which definitions go back into the main text?** A1 suggests nearly all
of `app:defs`. This goes against the earlier choice "for now only change
appendices" and "thesis keeps argument and design". Is moving formal
definitions back allowed now, or should the main text instead drop the
equation numbers and refer to the objects only in words?

**Q3. Which storage section survives, the new or the old?** And in
particular which notation (`ρ̂, μ̂, ŵ, β` against `τ_t, θ_t, w_t, λ`)? The
old one matches Method and the appendices.

**Q4. Should the storage objective `D + βK` stay in the Problem
Formulation?** It is never solved, `D` and `K` have no formal definition
anywhere, and the rules are greedy orderings. One option is to state the
rules directly and describe the objective in words only.

**Q5. Is the decision problem needed?** The main text says the thesis does
not solve it, and its only formal statement is in the appendix. Either
bring it into the main text as the frame the RQs compare inside, or drop it
and keep the paired gain test as the formal statement.

**Q6. Is the main result order service time or pick service time?** (D1.)
And does "order completion" mean leaving at the dock or the last line
arriving? (D2.)

**Q7. Where should the critic design and the per-group credit be
explained?** In the Problem Formulation (as now, as a defining difference
between architectures) or only in Method/Training, with the formulation
saying in one sentence that each controller is trained on what it sees?

**Q8. Should the observation subsection come before the controllers?** (B4.)

**Q9. Which experiment results get one sentence in the main text?** Proposal:
the main-load rule (App E) and the Token Passing reproduction (App K).
Anything else, for example the drift pilot (App F), which Impl already
mentions?

**Q10. Well-formedness.** Is one sentence by Token Passing plus App D
enough, now that the main paragraph is gone?

**Q11. Is `x_0` random or from popularity?** (D4.) And is Token Passing run
under all three storage rules or only fixed? (D5.)

## Figure to redraw

- `fig:loop` (`loop.pdf`): panel (b) shows the backward path for "adaptive
  storage", but only the congestion-aware rule reads the traffic (`[A44]`).
  The demand-only rule reads the orders only. Panel (b) should show the
  congestion-aware rule, or the figure should get a third panel. The caption
  "Only in (b) do the estimates choose the shelves" has the same issue. Text
  in `sec:pf:coupling` already says this (2026-10-30).
