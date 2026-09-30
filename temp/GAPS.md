# GAPS: every controller arm as a GCN

Companion notes to `GAPS.tex`, for the architecture change agreed on
2026-09-29. `GAPS.tex` explains the REVISION 2 fixes (`[Gxx]`, `[Kxx]`,
`[Mxx]`). This file explains the `[Axx]` tags.

**Decision.** All three routing arms (centralised, section-based,
decentralised) become GCN policies trained with PPO, following the
centralised vs decentralised setup of van Knippenberg, Holenderski and
Menkovski (2021). Prioritised planning (space-time A\*) stays as a
non-learned reference.

**Why.** Before the change, the centralised and section-based arms were
planners and only the decentralised arm was learned. So RQ2 compared
algorithm classes as well as information regimes, and any difference
between arms mixed the two. With one encoder family, one training
algorithm and one budget per arm, only the window of
`tab:information` differs. That is the contrast RQ2 asks about, and it is
what the thesis contract promises. It also turns the tragedy of the
commons into a measured contrast. A centralised learner on the team
objective internalises congestion by construction, a zone learner does so
only inside its zone, and a decentralised learner with its own `R_i` does
not.

**Where the edits live.** The changes were drafted in `_gcn` copies and
adopted on 2026-09-29 by renaming them over
`thesis/Chapters/2.Introduction.tex` and
`thesis/Chapters/4.Implementation.tex` (commit `f1a3027`). Each change is
tagged inline as `% [Axx]`. Those chapters, as `thesis/main.tex` includes
them, are the source of truth for the model (see the workspace
`AGENTS.md`).

The older drafts in `thesis-progress/temp/` (`problem_formulation_fixed.tex`,
`method_implementation_skeleton.tex`) are history and are not updated.

Severity key, same as `GAPS.tex`, plus one new kind.
**Design change** means a considered change of what the study does.
**Gap** means underspecified where the text otherwise commits to full formality.
**Error** means wrong as stated.

---

## Problem Formulation (`2.Introduction.tex`)

### [A1] Framing: learned arms plus a reference planner (Design change)

- **Where.** Introduction paragraph "This thesis investigates", Aim and
  scope item "controller architecture", RQ2.
- **Change.** Says all three controllers are graph-neural policies trained
  by one RL procedure and differ only in what they condition on, with a
  non-learned prioritised planner as reference. RQ2 now asks about
  controllers "that share one learning method and differ only in the
  information they condition on".
- **Why.** States the new experimental contrast where a reader meets the
  research questions.

### [A2] Who decides: reference controller and routing-rule column (Design change)

- **Where.** `sec:pf:controllers`, after "heuristics, optimisation methods,
  or learned policies", and `tab:information`.
- **Change.** A paragraph states that every architecture's routing rule is
  a learned policy from one family, and adds one reference controller
  outside that family. `tab:information` gains a "Routing rule" column
  (learned / planner) and a "Reference" row with the global window. The
  two long columns are now `p{4.2cm}` so the table fits the text width.
- **Why.** Π must name the planner explicitly if it is evaluated under
  `eq:rqformal`. The planner plays the role that A\*, ICBS and ICTS play
  in Knippenberg's Table 2.

### [A3] Policy forms for the centralised and section-based arms (Design change)

- **Where.** `sec:pf:controllers`, new paragraph after "centralised training
  with decentralised execution". New labels `eq:centralisedpolicy`,
  `eq:sectionpolicy`.
- **Change.** Centralised arm:
  `u_t ~ ∏_i π^cen_θ(u_i(t) | s_t, i)`. Section-based arm, for `ℓ_i(t) ∈ Y_q`:
  `u_i(t) ~ π^sec_θ(· | s_t^(q), i)`, where `s_t^(q)` is the zone-local
  state including what the boundary protocol passes across. The
  decentralised policy keeps the plain `π_θ`.
- **Why.** A factored policy, one action distribution per agent, avoids a
  distribution over the exponentially large joint action set. This is
  Knippenberg's "single-agent RL" setup. The factors are sampled
  independently, so the paragraph also states that conflict resolution
  handles the remaining infeasible joint actions identically for all
  controllers.
- **Correction to an earlier claim.** An earlier discussion draft rejected a
  learned centralised arm because of the exponential joint action space.
  The factored form removes that objection. The real cost is poor scaling
  with graph size (Knippenberg Table 4, 14% solved at 2048 nodes vs 63%
  for the decentralised setup).

### [A4] Objective, loop and research formula (Design change)

- **Where.** Paragraph after `eq:objective`, the loop sentence in
  `sec:pf:coupling`, and the paragraph after `eq:rqformal`.
- **Change.** `eq:objective` applies to each of the three learned
  controllers, with θ ranging over that controller's own parameters. The
  planner has no θ and is not trained against it. The loop sentence now
  says every learned controller factors into per-agent distributions. The
  planner is evaluated under the same factorial design, so each learned
  arm's margin can also be read against it.
- **Why.** The old text allowed any one regime to be learned. Now all
  three are.

### [A12] The learning problem still described one learned arm (Error + Gap)

- **Where.** `sec:pf:game` throughout, one sentence in
  `sec:method:resolution`. New label `eq:obsfunction`.
- **Change.**
  - **Observation function per architecture.** New `eq:obsfunction`:
    `O_i(s_t) = (s_t, i)` centralised, `(s_t^(q), i)` with `ℓ_i(t) ∈ Y_q`
    section-based, `o_i(t)` decentralised. Every other element of `M` is
    shared, so the three learned arms play three versions of one game that
    differ only in `O_i`, which is RQ2. The centralised version is fully
    observed. Apart from messages, each narrower observation can be
    computed from the next wider one. `tab:posg`'s `𝒪_i` and `O_i` rows
    point to `eq:obsfunction` instead of `o_i(t)`.
  - **Opening paragraph.** No longer says every agent acts "without seeing
    the whole warehouse" or "from `o_i(t)`".
  - **`P` contains the shared, non-learned rules.** `tab:posg`'s `P` row
    now lists conflict resolution and the assignment rule next to
    `eq:transition` and `eq:storageupdate`, with one sentence saying why
    (neither is any agent's action, both are the same for every
    controller). This is what [A6] relies on when it calls conflict
    resolution part of the environment.
  - **Priority order is part of the state.** `sec:method:resolution` draws
    the resolution priority once per episode from the seed, and called the
    operator a function of "the state and the episode seed", while
    `sec:pf:scope` said "deterministic given the state". Now the order is
    in `tab:posg`'s `𝒮` row, and the Method sentence says the state
    includes it. Both chapters agree and `P` stays stochastic only through
    order arrivals.
  - **Objective vs. credit signal.** New sentence after the [A4]
    paragraph. `eq:objective` is the shared target, and how an update
    credits reward (team mean over controlled agents, or own `R_i`) is the
    [A9] training choice. Removes the apparent contradiction between one
    shared objective and the predicted commons ordering.
  - **Smaller fixes in the same section.** Masked actions get zero
    probability under the policy, not under `P`. `R_i(t)` is stated as
    shorthand for `R_i(s_t, u_t, s_{t+1})`. `O_i` is stated as deterministic
    including messages, since the message payload of `sec:method:rl` reads
    positions and targets from `s_t`. `δ_i(t)` is readable from every
    window, not only part of `o_i(t)`.
- **Why.** [A4] patched only the paragraph after `eq:objective`. The rest
  of the section still assumed only the decentralised arm was learned.
  These were also points 1 to 3 of `learning_problem_guide.tex`, which is
  updated to match.

### [A13] The critic sees the same window as the policy (Design change)

- **Where.** `sec:pf:controllers`, the sentence after "Parameter sharing
  is appropriate". `sec:method:model`, new paragraph after [A8], and a new
  "critic input" row in `tab:modelparams`.
- **Change.** The conditional definition of centralised training with
  decentralised execution is replaced by a commitment. This thesis does
  not use it. Every router's value head reads the same embedding `z_i` as
  its policy head, so the critic conditions on `(s_t, i)`, `(s_t^(q), i)`
  or `o_i(t)`, the same window as that router's policy (`eq:obsfunction`).
  The critic's target is the return under the router's credit signal
  (`tab:trainparams`), which for the decentralised router is its own
  `R_i`.
- **Why.** Chosen by the author over a global critic for every router
  (MAPPO style). Two reasons. It is better for the commons contrast. A
  decentralised learner with a local critic and its own `R_i` gets no
  training signal that prices the congestion it causes outside its
  window, which is the effect the contrast is meant to measure. A global
  critic would partly teach it that cost and blur the contrast. It is
  also the cleaner concept. The architectures then differ in how they
  train as well as in how they act, so "the architecture is its window"
  holds end to end, not only at execution. The accepted cost is that a
  weaker decentralised result combines seeing less when acting with
  learning from a noisier critic. The text states the global critic as
  the standard alternative that is not used.
- **Code.** No change needed. `slap-mapd-coupling`'s `rl_module.py`
  already feeds one `z_i` to both actor and critic.

### [A14] Messages are learned embeddings, part of the policy (Design change)

- **Where.** `sec:pf:controllers` (decentralised policy and
  `tab:information`), `sec:pf:observations` (intro, "Messages from nearby
  agents", `eq:observation`, `tab:observationexample`), `sec:pf:game` (the
  nesting paragraph), `3.Background.tex` ("Precedents for local
  communication"), `sec:method:controllers`, `sec:method:rl`,
  `sec:method:model` (new `eq:message`), `tab:modelparams`,
  `2.Notation.tex`, `references.bib`, and the architecture figure.
- **Change.**
  - The hand-picked message `(d_G(l_i, l_j), eta_j)` is replaced by a
    learned message `xi_j(t) = MSG_theta(h^(L)_{l_j(t)})`, a fully
    connected head over the sender's own final embedding, trained end to
    end through the policy loss, as in CRAMP and PICO. The receiver
    aggregates the messages from its neighbours in `G^A_t` in
    `eq:readout`.
  - Because a learned message depends on `theta`, not only on the state,
    messages move out of the observation. `o_i(t)` now has three pieces
    (field of view, direction, crowding), and messages are a communication
    step inside the decentralised policy. The nesting of the observation
    functions in `sec:pf:game` now holds with no exception.
  - Messages travel one hop of `G^A_t` per timestep. More rounds would
    relay what agents beyond the field of view send and widen the
    decentralised window past `d_obs`.
  - Communication has its own switch (drop the message term), so `L = 0`
    now only removes structural aggregation. This settles the old open
    refinement that one `L = 0` removed both.
  - The forward pass takes all agents of a timestep together. Execution
    stays decentralised.
  - PICO (`li2022pico`) is added to the bibliography and to
    `3.Background.tex`, next to CRAMP. The thesis takes from both the
    learned message content, and keeps who may talk to whom and conflict
    priority fixed, so the only learned element of communication is what
    is sent.
- **Why.** Decided by the author, reasoning in `message_design.md`. The
  network rather than the designer decides what is worth sending, it
  matches CRAMP and PICO, and a failure of communication to help cannot be
  put down to a poorly chosen message. The hand-picked payload also could
  not say which way the sender is heading, which is what RQ5 is about.
- **Reverses.** The [A12] sentence that messages keep `O_i` deterministic
  because they are read from the state.
- **Not yet done.** `slap-mapd-coupling` still builds the hand-picked
  two-number message and batches agents separately. Its message builder
  and the decentralised forward pass need to follow `eq:message`.

### [A15] Per-agent action space as numbered moves (Gap)

- **Where.** `sec:pf:game`, the action-space paragraph, and `tab:posg`'s
  `U_i` row. `2.Notation.tex` gains `d_max`.
- **Change.** `U_i` was the union of every vertex's action set, so it held
  a move toward every vertex in the graph. It is now
  `{wait, move_1, ..., move_{d_max}}`, where `move_k` is the k-th outgoing
  edge of the current vertex in a fixed order and `d_max` is the largest
  out-degree. Moves beyond the current vertex's out-degree are masked,
  leaving exactly `U(v)`. The paragraph explains this in words with an
  example before the equation.
- **Why.** Easier to read, and it is what `eq:mask` in the Method chapter
  already implements (`d_max + 1` logits), so the two chapters now agree.
  The union form did not match the slot-based mask.
- **Order of the moves.** `move_k` needs each vertex's outgoing edges in
  a fixed order, which neither chapter stated. `sec:pf:env` now numbers
  the vertices once, `V = {v_1, ..., v_|V|}`, and the action-space
  paragraph lists each vertex's outgoing neighbours in increasing vertex
  number. The code currently uses the order in which edges were added
  when the graph was built (`graph.py` `legal_actions`, and the
  `spaces.py` docstring says the thesis gave no rule), so it should sort
  by vertex number to match.

### [A17] Per-edge policy head (Design change)

- **Where.** `sec:method:rl` ("Action space and masking"),
  `sec:method:model` (new "Per-edge policy head" paragraph, `eq:edgescore`,
  `fig:edgescore`), `tab:modelparams`, `2.Notation.tex`, `references.bib`.
  New figure source `thesis-progress/scripts/images/edgescore.tex`.
- **Change.** Each move's logit is now computed from the vertex it leads
  to, `logit(move to w) = SCORE_theta(z_i || h_w^(L) || xibar_w(t))`, with
  one small network shared by every edge, and `logit(wait) =
  SCORE^wait_theta(z_i)`. `xibar_w(t)` is the message of the agent
  standing on `w`, zero if `w` is free, and is dropped with communication
  off. The scores go into the move slots by vertex number and are masked
  by `eq:mask`, so the action space `U_i` is unchanged.
- **Why.** On a graph a move has no name of its own. A head reading all
  move logits from `z_i` cannot tell which neighbour is which slot,
  because `eq:msgpass` combines neighbours as an unordered set. Checked:
  van Knippenberg et al. (2021) use a fixed output vector and have the same
  gap, and CRAMP avoids it only because its grid gives fixed directions
  (N, E, S, W). Scoring each candidate and taking a softmax over the
  candidates is the pointer mechanism of Vinyals, Fortunato and Jaitly
  (2015), cited for that idea only. Kool et al. (2019) was considered and
  not cited, since it would suggest a Transformer encoder, which the
  thesis does not use. Placing messages on the sender's vertex ties a
  message to a direction, which the averaged messages in `z_i` could not.
- **Supersedes.** The [A16] decision to keep the fixed-vector head, and
  its caveat about node IDs.
- **Not yet done.** `slap-mapd-coupling`: the policy head, and placing
  messages on the sender's vertex.

### [A18] Future work: attention-based controller parts (Design note)

- **Where.** `6.Conclusion.tex`, new subsection `sec:future`.
- **Change.** One paragraph noting that the encoder, the communication
  step and the per-edge head could each become an attention version
  without changing the formulation, cheapest first (head, then
  communication, then encoder), and that any such change must be made for
  all three learned controllers at once. Cites SePar only. The full plan
  is in `transformer_extension_guide.tex` at the workspace root.

### [A19] The reference planner leaves the formulation, stays as a baseline (Design change)

- **Where.** `2.Introduction.tex`: the opening paragraph, Aim and scope
  item 2, the [A2] paragraph in `sec:pf:controllers`, `tab:information`,
  the objective paragraph of `sec:pf:game`, the paragraph after
  `eq:rqformal`. `4.Implementation.tex`: the section intro,
  `sec:method:overview`, `sec:method:controllers`. Also
  `learning_problem_guide.tex`.
- **Change.** The prioritised planner is no longer part of the problem
  formulation. It is removed from `tab:information` (row and the
  now-redundant "Routing rule" column), from `Pi`, from the factor list
  and from `eq:rqformal`. It stays in the Method chapter as a "Reference
  baseline", reported next to the learned routers under a few main
  conditions (fixed storage, main loads), not across the full factorial
  design. The Introduction's opening paragraph says it is reported as a
  classical reference point outside the main comparison.
- **Why.** Decided by the author. No research question is about the
  planner, and as a fourth member of `Pi` it broke the "three
  architectures that differ only in their window" story and added a fourth
  arm to every factorial condition. It is kept, not removed, because it is
  the only check that the learned controllers are competitive with a
  classical method, and its code already exists.
- **Partly reverses.** [A2] (reference row, routing-rule column, planner in
  `Pi`) and the planner part of [A4].
- **Still to decide.** Exactly which conditions the baseline is reported
  under, once the experiment chapter is written.

### [A7] Section-based assignment in `tab:information` (Error)

- **Where.** `tab:information`, Section-based row, and the zone sentence
  before `eq:partition`.
- **Change.** Assignment for the section-based arm now reads "global state
  (held fixed across arms)", like the decentralised row. The zone sentence
  no longer says tasks are handed across the boundary.
- **Why.** The table said section-based assignment conditions on
  zone-local state, but the Method chapter realises assignment as one
  global greedy rule shared by all controllers, and the text says only
  routing differs. The table was the inconsistent side. This error
  existed before the GCN change.

---

## Method (`4.Implementation.tex`)

### [A5] Controller realisations and overview (Design change)

- **Where.** Section intro, `sec:method:overview`,
  `sec:method:controllers`, and the opening of `sec:method:rl`.
- **Change.**
  - Overview counts four controllers (three learned, one reference).
  - "Stages 2--3" becomes "stage 3". Stage 2 (assignment) is shared, so it
    never changes with the controller. This also matches the caption of
    `fig:methodloop`.
  - The space-time A\* text moves unchanged to a **Reference** router.
  - **Centralised** is now `π^cen_θ`, the encoder of `sec:method:model` run
    once per timestep on all of `G`, with agent `a_i`'s head read out at
    `ℓ_i(t)`.
  - A new paragraph states that the three learned routers share the
    encoder family, action mask, reward, training procedure and budget,
    and differ only in the graph the encoder runs on and which agents it
    has heads for.
  - `sec:method:rl` says the four RL components are reused on the larger
    graph (`V`, or `Y_q ∪ H_q`).
- **Why.** Realises [A2] and [A3].

### [A6] Section-based boundary rule: ownership plus halo (Design change)

- **Where.** `sec:method:controllers`, Section-based paragraph. New label
  `eq:halo`.
- **Change.**
  - **Ownership.** Zone `Y_q` owns the agents with `ℓ_i(t) ∈ Y_q` and has
    action heads for them only.
  - **Halo.** Its network runs on `Y_q ∪ H_q`, where
    `H_q = { v ∉ Y_q : d_G(w,v) ≤ d_obs for some w ∈ Y_q }`. Halo vertices
    carry role and occupancy features, but no heads and no loss. The halo
    *is* the boundary protocol of `tab:information`.
  - **Handover.** Ownership passes to the next zone on the timestep an
    agent enters it. Weights are shared across zones, so handover changes
    context, not policy.
  - **Cross-boundary conflicts.** Removed by the existing
    conflict-resolution operator, as everywhere else.
  - **Nesting.** With `p = 1` the halo is empty and `π^sec_θ = π^cen_θ`.
- **Why.** The old rule ("yield at the boundary to whichever zone has
  fewer active agents") compared planned routes. A learned policy acts one
  step at a time and produces no route to compare. The halo is the
  standard way to run a GNN on a partitioned graph.
  - Tying its depth to `d_obs` adds no new parameter.
  - It matches the formulation's statement that a section-based field of
    view is not cut off at the zone boundary, so `δ_i(t)` means the same
    thing under every architecture.
  - The conflict-resolution operator is part of the environment, not a
    controller's information (`sec:pf:agents`), so using it at boundaries
    does not widen the section-based window.
  - The `p = 1` property makes centralised, section-based and
    decentralised a continuum in how much each controller sees.
  - η_i is computed from `d_G` on the whole graph, so a boundary agent
    still knows which way a goal in another zone lies. That is the agent's
    own task information, as for the decentralised arm.
- **Rejected alternatives.** Zones exchanging embeddings (that is
  communication and would blur into RQ5). Overlapping zones with both
  proposing actions (needs an arbiter and duplicate heads).
- **Noted variant, not adopted (2026-09-30).** Halo plus learned messages
  from the agents standing in the halo, the [A14] message head applied
  across the zone edge. It would keep the halo, so the boundary protocol
  and the meaning of `delta_i(t)` at the boundary are unchanged, and add a
  learned channel on top. Not adopted because it makes the section-based
  window depend on `theta`, moves it toward the centralised one, and mixes
  a communication effect into the section-based results that RQ5 is meant
  to isolate. Replacing the halo by messages alone was ruled out, since
  boundary crowding counts need the halo's occupancy.

### [A8] Model: two open points for full-graph and zone passes (Gap)

- **Where.** `sec:method:model`, new paragraph after the `Q = 0` ablation,
  and two new rows in `tab:modelparams`.
- **Change.** The centralised and section-based routers reuse `φ_q`,
  `ψ_q`, and their readout drops the message term (communication is a
  decentralised ablation only). Two points are recorded as TBD rather
  than decided silently.
  1. **η_i encoding.** `f(v,t)` contains the per-agent potential
     `η_i(v,t)`, which cannot be one node feature in a pass shared by all
     agents. The options are one pass per agent, or a single pass with each
     agent's task encoded at the vertex it occupies (Knippenberg's
     approach).
  2. **Global pooling.** After `Q` rounds a vertex embedding only reflects
     vertices within `Q` hops. Without a pooled graph or zone embedding in
     the readout, the centralised arm does not in practice condition on
     the global state that `tab:information` grants it.
- **Why.** Both decide whether the centralised arm really is "global". If
  they were left implicit, a weak centralised result could come from the
  architecture rather than from the information regime.

### [A9] Training: equal budget and the credit signal (Design change + Gap)

- **Where.** `sec:method:training`, and two new rows in `tab:trainparams`.
- **Change.** Each learned router is trained separately under the same
  PPO procedure with the same environment-step budget, and both training
  regimes (under `F_fix` only, and matched) apply to each. Left open, as
  TBD: whether the centralised and section-based networks are updated on
  the team-mean reward of the agents they control, or on per-agent `R_i`.
- **Why.** An equal budget keeps the comparison about information, not
  training effort. The credit signal decides how much of the congestion
  externality each arm internalises, so it is the lever behind the commons
  contrast. It must be stated, not left to an RLlib default.

### [A10] Computational cost reporting (Design change)

- **Where.** `sec:impl:cost`.
- **Change.** Training and inference time are reported for each of the
  three learned controllers. The planner has no training cost, and its
  planning time per decision is the comparison point for inference time.

### [A11] Model figure (Gap)

- **Where.** `fig:architecture` in `sec:method:model`. Applied to **both**
  `4.Implementation.tex` and `4.Implementation_gcn.tex`, because the
  decentralised model is unchanged by the GCN decision.
- **Change.** Replaced the `\fbox` placeholder with
  `Images/architecture.pdf`. It is adapted from Knippenberg's Figure 3,
  with the message-passing block expanded (local subgraph, `Q` rounds,
  readout `z_i`, FC + ReLU, masked softmax and value head), agents
  `1..m` with shared θ, observations `o_i(t)` and rewards `R_i(t-1)`, and
  conflict resolution before the environment.
- **Source.** `thesis-progress/scripts/images/architecture.tex`.

---

## Figures redrawn in TikZ (same session, not tagged)

These replace matplotlib output with vector PDFs in the thesis fonts. The
sources are in `thesis-progress/scripts/images/`, and the PDFs are in
`thesis-progress/scripts/Images/` and `thesis/Images/`.

| Figure | Source | Used in | Status |
| --- | --- | --- | --- |
| `fig:loop` | `loop.tex` | both Introduction chapters | switched to `loop.pdf` |
| `fig:methodloop` | `methodloop.tex` | `4.Implementation.tex` | placeholder replaced |
| `fig:architecture` | `architecture.tex` | both Method chapters | placeholder replaced, see [A11] |

`loop.py` and `methodloop_simple.py` still exist, and `figure.py` still
regenerates `loop.png`.

---

## Still open

- [x] Read the `_gcn` chapters through and rename them over
      `2.Introduction.tex` and `4.Implementation.tex` (done 2026-09-29).
- [ ] `2.Introduction*.tex` (well-formedness paragraph) still calls Token
      Passing and Ma et al.'s centralised baseline "two of the baselines
      this thesis compares against". The Method chapter uses neither. This
      was already true before the GCN change, and needs a decision.
- [ ] `3.Background.tex`, "Congestion and emergence", still frames the
      commons for the system as a whole. It could now state the predicted
      order (centralised least exposed, then section-based, then
      decentralised) as a hypothesis.
- [ ] Decide the TBD rows added in [A8] and [A9]. The credit signal is
      now cited from `sec:pf:game` ([A12]), so deciding it also fixes what
      that sentence commits to.
- [x] **Tie-break in `eq:assignmentrule`** ([A12] follow-up, done
      2026-09-30). Two ties were unbroken: tasks released in the same
      timestep, and free agents at equal `d_G` to `s_j`. Now tasks go in
      task index order, and equal agents are ranked by the conflict-resolution
      priority order of `sec:method:resolution`. Chosen because that order
      is already in the state ([A12]), adds no parameter, and is redrawn
      each episode, so no agent is systematically favoured (lowest agent
      index would be). Rejected: settling ties by communication within
      range. Assignment must be identical across controllers and is part of
      `P`, while communication exists only for the decentralised arm and
      only if RQ5 is reached. PICO (`2202.03634`) was checked as a model
      and does not fit. Its learned priorities decide who yields on
      conflicting paths, with fixed goals, not who gets a task. A learned,
      PICO-style priority would belong to the conflict-resolution
      operator, and would put a learned component inside `P`, so it is a
      separate question.
- [x] **Which critic each arm uses** ([A12] follow-up, done 2026-09-30,
      see [A13]). Critic sees the same window as the policy in every arm,
      no centralised training with decentralised execution. The credit
      signal for the centralised and section-based arms is still open
      ([A9]), and the critic's target follows it.
- [x] **Message content for RQ5** (done 2026-09-30, see [A14]). The hand-picked payload
      `(d_G, eta_j)` cannot tell the receiver which way the sender is
      heading. Leaning towards learned message embeddings as in CRAMP and
      PICO, which would move messages from the observation into the
      decentralised policy. Options, reasons, costs and the list of edits
      are in `message_design.md` at the workspace root. Only needed if
      RQ5 is reached.
- [x] **Per-edge policy head** (first decided 2026-09-30 as [A16], not adopted, then adopted as [A17], see there). History of the [A16] decision:
      Checked against van Knippenberg et al. (2021), sec. 4.1: their
      action space is "local movement options", one move per adjacent
      outgoing edge plus wait, shared by all agents and instances, and
      their head is GCN embedding, then fully connected ReLU layers, then a
      softmax over that fixed vector. That is the thesis's slot head, so
      the author chose to keep it. `sec:method:rl` now cites them for the
      action space and states the one difference, masking instead of
      their penalised wait (the [K8] deviation, now also in the text).
      **Remaining caveat.** They give every node a node ID as an
      attribute, which is the only thing in their input that can tell two
      outgoing edges apart, and they never say how move k is matched to an
      edge. The thesis fixes the order (increasing vertex number, [A15])
      but `f(v,t)` carries no vertex number, so the network still cannot
      see which neighbour is which slot. Adding the vertex number as a
      feature would copy them more closely but would not carry over to a
      different warehouse. Worth a sentence in the limitations, or a
      decision, once results show whether it matters.
- [ ] **Code for [A17].** Per-edge policy head in `slap-mapd-coupling`,
      with the message of the agent on each neighbour vertex as an input.
- [ ] **Code for [A15].** Sort each vertex's outgoing neighbours by vertex
      number in `slap-mapd-coupling` (`graph.py` `legal_actions`), so
      `move_k` means the same as in the thesis.
- [ ] **Code for [A14].** `slap-mapd-coupling` message builder and the
      decentralised forward pass (all agents of a timestep together) must
      follow `eq:message`.
- [x] **Guide item 4** in `learning_problem_guide.tex`: the task example
      uses `a_2` and the observation figure uses `a_1`. Cosmetic.
- [ ] Confirm the delivery date (about 12 January 2027) and that the new
      arms match the thesis contract wording.
