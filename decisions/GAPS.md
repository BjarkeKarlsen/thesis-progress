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

**Revised 2026-10-16, [A32].** The arms no longer differ only in their
window. The centralised arm lets the agents choose one at a time, each
seeing the earlier choices, the section-based arm does the same per zone,
and the decentralised arm is unchanged. They differ in how many agents one
decision covers. The commons question is no longer part of the study, so
the internalisation argument above is history. Entries [A1] to [A6],
[A8], [A9], [A12], [A13] and [A29] are rewritten to match the chapters as
they now stand, each with a short History line for what it said before.

**Where the edits live.** The changes were drafted in `_gcn` copies and
adopted on 2026-09-29 by renaming them over
`thesis/Chapters/2.Introduction.tex` and
`thesis/Chapters/4.Implementation.tex` (commit `f1a3027`). Each change is
tagged inline as `% [Axx]`. Those chapters, as `thesis/main.tex` includes
them, are the source of truth for the model (see the workspace
`AGENTS.md`).

The older drafts in `thesis-progress/archive/temp/` (`problem_formulation_fixed.tex`,
`method_implementation_skeleton.tex`) are history and are not updated.

Severity key, same as `GAPS.tex`, plus one new kind.
**Design change** means a considered change of what the study does.
**Gap** means underspecified where the text otherwise commits to full formality.
**Error** means wrong as stated.

---

## Index

Status of every tag. *In force* entries are below. *History* entries are in
`done/GAPS_history.md`.

| Tag | Title | Status |
|---|---|---|
| [A1] | Framing: learned arms plus a reference baseline | In force |
| [A2] | Who decides: one learned family and the table of architectures | In force |
| [A3] | Policy forms for the centralised and section-based arms | In force |
| [A4] | Objective, loop and research formula | In force |
| [A5] | Controller realisations and overview | In force |
| [A6] | Section-based boundary rule: ownership plus halo | In force |
| [A7] | Section-based assignment in `tab:information` | In force |
| [A8] | Model: two open points for full-graph and zone passes | History, resolved by [A29] |
| [A9] | Training: equal budget and credit | In force |
| [A10] | Computational cost reporting | In force, hardware per method in [A95] |
| [A11] | Model figure | In force |
| [A12] | The learning problem still described one learned arm | In force |
| [A13] | The critic sees the same window as the policy | In force |
| [A14] | Messages are learned embeddings, part of the policy | In force |
| [A15] | Per-agent action space as numbered moves | In force |
| [A16] | Fixed-vector policy head | History, not adopted, replaced by [A17] (see closed items) |
| [A17] | Per-edge policy head | In force |
| [A18] | Future work: attention-based controller parts | In force |
| [A19] | The reference planner leaves the formulation, stays as a baseline | In force |
| [A20] | A simple score for a run, following lifelong MAPD | In force |
| [A21] | Field of view counts hops | History, superseded by [A25] |
| [A22] | Hearing is one way in the communication graph | In force |
| [A23] | The learning problem explained in words first | In force |
| [A24] | One definition of the blocked indicator | In force |
| [A25] | Field of view is measured by travel cost, not hops | In force |
| [A26] | Storage estimates cover one storage period, per step | In force |
| [A27] | The message is the sender's embedding, with no message head | In force |
| [A28] | Deadlock in dead-end corridors, Token Passing as the baseline | In force |
| [A29] | The wider routers: one pass per agent, a pooled readout, and a window that is never truncated | In force |
| [A30] | A standing-still step costs `c_wait` in the reward | In force |
| [A31] | Keep-up threshold, horizon and load levels | In force |
| [A32] | Real centralised and section-based controllers | In force |
| [A33] | The commons question folded into RQ4 | In force |
| [A34] | Skewed demand that drifts | In force |
| [A35] | Starting stock from expected demand, in blocks | In force |
| [A36] | How a wait is attributed to an edge | Replaced by [A93] (the edge estimates are gone) |
| [A37] | Storage rule wording fixes | In force |
| [A38] | Storage decided when stock arrives | In force |
| [A39] | Orders take a unit from the nearest shelf, or wait for stock | In force |
| [A40] | Put-away distance replaces relocations per update | History, revised by [A47] |
| [A41] | Research questions built around the main result | In force |
| [A42] | RQ3 asks about congestion-aware storage only | In force |
| [A43] | Edge cost and step costs from van Knippenberg et al. | In force |
| [A44] | The main result is adaptive storage, and the loop is closed in RQ3 | In force, measure revised by [A50] and [A51] |
| [A45] | Keep-up against released tasks, a backlog slope, and stalls | Revised by [A49], slope dropped |
| [A46] | Orders with several lines and amounts | In force |
| [A47] | Robots carry the put-away | In force, result measure revised by [A50] |
| [A48] | The storage rule is a dynamic SLAP, solved with rules | In force |
| [A49] | Keep-up is throughput against the release rate | In force, the measure is the served share since [A96] |
| [A50] | The result is the mean service time of picks | In force |
| [A51] | The gain between controllers is a percentage of fixed-storage service time | In force |
| [A52] | Borrowed concepts and fewer equations | In force |

## Problem Formulation (`2.Introduction.tex`)

### [A1] Framing: learned arms plus a reference baseline (Design change, revised 2026-10-16 by [A32])

- **Where.** Introduction paragraph "This thesis investigates", Aim and
  scope item "controller architecture", RQ2.
- **Change.** All three controllers are graph-neural policies trained by
  one RL procedure. They differ in how many agents one decision covers, the
  whole fleet, one zone or a single agent, and what each sees follows from
  that. Token Passing is named as the reference baseline ([A28]). The
  controller factor reads "each a learned policy that decides for the whole
  fleet, one zone, or one agent". RQ2 asks about controllers "that share
  one learning method and differ in how many agents one decision covers".
- **Why.** States the experimental contrast where a reader meets the
  research questions.
- **History.** Until [A32] the text said the controllers "differ only in
  the information they condition on", with a prioritised planner as
  reference.

### [A2] Who decides: one learned family and the table of architectures (Design change, revised 2026-10-16 by [A32])

- **Where.** `sec:pf:controllers`, after "heuristics, optimisation methods,
  or learned policies", and `tab:information`.
- **Change.** A paragraph states that every architecture's routing rule is
  a learned policy from one family, trained by one procedure, and that the
  architectures differ in how many agents one decision covers.
  `tab:information` has the columns Architecture, One decision covers,
  Assignment conditions on, and Routing conditions on. The centralised row
  routes on the global state and the earlier agents' actions, the
  section-based row on the zone-local state, the boundary protocol and the
  earlier agents' actions in the zone, and the decentralised row on
  `o_i(t)` plus messages. There is no reference row.
- **Why.** `Π` holds only the learned controllers, so RQ2 compares one
  learning family. The new column names what separates the architectures.
- **History.** The first version added a "Routing rule" column (learned or
  planner) and a "Reference" row. [A19] took the planner out of the
  formulation, and [A32] added the "One decision covers" column and the
  earlier actions.

### [A3] Policy forms for the centralised and section-based arms (Design change, revised 2026-10-16 by [A32])

- **Where.** `sec:pf:controllers`, the block after the critic paragraph.
  Labels `eq:centralisedpolicy`, `eq:sectionpolicy`.
- **Change.**
  - Centralised. The agents choose one at a time in the episode priority
    order, each from the global state and the earlier choices,
    `u_t ~ ∏_i π^cen_θ(u_i(t) | s_t, u_{≺i}(t), i)`, drawn in priority order.
    This is the chain rule, so any joint distribution can be written this
    way, at `m` evaluations per decision.
  - A collision rule. An agent may not move onto a vertex an earlier agent
    has chosen, may not swap with an earlier agent, and may not move onto a
    vertex whose agent has not chosen yet. Waiting is always allowed, so a
    centralised decision never needs conflict resolution.
  - Section-based. The same per zone, for `ℓ_i(t) ∈ Y_q`,
    `u_i(t) ~ π^sec_θ(· | s_t^(q), u^(q)_{≺i}(t), i)`. Zones choose in
    parallel and do not see each other's choices, so cross-zone clashes go
    to conflict resolution. With one zone it is the centralised arm.
  - Decentralised. Unchanged, each agent chooses independently.
- **Why.** With independent factors the centralised arm was the
  decentralised arm with a large view, since no agent saw another's choice.
  The chain rule keeps the joint action tractable and gives the arm real
  coordination. It is prioritised planning one timestep ahead with a
  learned policy in place of the path search. Knippenberg's single pass
  over the complete graph was rejected because no agent sees another's
  choice. A distribution over all joint actions was rejected because it is
  exponential in `m`. The scaling cost now shows as runtime, `m` network
  runs per timestep. Two `% TODO cite` comments mark where prioritised
  planning and turn-by-turn policies are to be cited.
- **History.** The first version sampled the factors independently,
  `∏_i π^cen_θ(u_i(t) | s_t, i)`, called it Knippenberg's single-agent
  setup, and left all clashes to conflict resolution. It quoted only the
  graph-size half of Knippenberg's Table 4. The table shows that a larger
  fleet degrades the single-agent setup too.

### [A4] Objective, loop and research formula (Design change, revised 2026-10-16 by [A32])

- **Where.** Paragraph after `eq:objective`, the loop sentence in
  `sec:pf:coupling`, and the paragraph after `eq:rqformal`.
- **Change.** `eq:objective` applies to each of the three learned
  controllers, with θ ranging over that controller's own parameters. Token
  Passing has no θ, is not trained against it, and stays outside the
  factorial design ([A19]). The loop sentence says every learned
  controller's `π(· | s_t)` is a product of per-agent distributions, and
  that under the centralised and section-based controllers each factor also
  reads the choices of the earlier agents in the same decision. The
  paragraph after `eq:rqformal` names the first factor as "the controller,
  how many agents one decision of π covers".
- **Why.** The old text allowed any one regime to be learned. Now all
  three are.
- **History.** Until 2026-10-16 the loop sentence said each agent chooses
  "from its own window", and the first factor was "the window of π".

### [A12] The learning problem still described one learned arm (Error + Gap, revised 2026-10-16 by [A32])

- **Where.** `sec:pf:game` throughout, one sentence in
  `sec:method:resolution`. New label `eq:obsfunction`.
- **Change.**
  - **Observation function per architecture.** New `eq:obsfunction`:
    `O_i(s_t) = (s_t, i)` centralised, `(s_t^(q), i)` with `ℓ_i(t) ∈ Y_q`
    section-based, `o_i(t)` decentralised. Every other element of `M` is
    shared. The controllers differ in what each agent observes and in
    which agents choose together ([A32]). The earlier agents' choices are
    made inside the policy within the timestep, so they are not part of
    the state or of any observation, and `eq:posg` and `eq:obsfunction`
    stay as they are. The centralised version is fully observed. Apart
    from messages, each narrower observation can be computed from the next
    wider one. `tab:posg`'s `𝒪_i` and `O_i` rows point to
    `eq:obsfunction` instead of `o_i(t)`.
  - **Opening paragraph.** No longer says every agent acts "from
    `o_i(t)`". Since [A32] it says that, except under the centralised
    controller, an agent neither sees the whole warehouse nor knows what
    every other agent will do.
  - **Policy paragraph.** Since [A32], under the centralised controller the
    agents draw their actions one after another, each seeing the earlier
    draws, and the section-based controller does the same inside each zone.
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
  - **Objective vs. credit.** Paragraph after the [A4] paragraph.
    `eq:objective` is the shared target. Since [A32] each update credits
    an agent's action with the mean reward of the agents that chose
    together with it (`eq:credit`), the whole fleet, one zone or the agent
    alone, because agents that choose together act as one decision-maker.
    This is why one shared objective still gives controllers that differ
    in how much congestion they cause. Before [A32] the credit was an open
    [A9] choice tied to a predicted commons ordering.
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

### [A13] The critic sees the same window as the policy (Design change, revised 2026-10-16 by [A32])

- **Where.** `sec:pf:controllers`, the sentence after "Parameter sharing
  is appropriate". `sec:method:model`, the critic paragraph, and the
  "critic input" row in `tab:modelparams`.
- **Change.** The conditional definition of centralised training with
  decentralised execution is replaced by a commitment. This thesis does
  not use it. Every router's value head reads the same embedding `z_i` as
  its policy head. The critic therefore conditions on
  `(s_t, u_{≺i}(t), i)` for the centralised router,
  `(s_t^(q), u^(q)_{≺i}(t), i)` for the section-based router, and `o_i(t)`
  plus messages for the decentralised router, the same window as that
  router's policy. The critic's target is the return under the credit
  `eq:credit` ([A32]), the mean reward of the whole fleet, of the agent's
  zone, or of the agent alone.
- **Why.** Chosen by the author over a global critic for every router
  (MAPPO style). Two reasons. A decentralised learner with a local critic
  and its own `R_i` gets no training signal that prices the congestion it
  causes outside its window, which is the congestion contrast the
  comparison is meant to show. A global critic would partly teach it that
  cost and blur the contrast. And what a controller sees is set by the
  agents it decides for, so it should limit how the controller learns as
  well as how it acts. The accepted cost is that a weaker decentralised
  result combines seeing less when acting with learning from a noisier
  critic. The text states the global critic as the standard alternative
  that is not used.
- **History.** The second reason used to read "the architecture is its
  window", and the first was framed as the commons contrast, which is no
  longer a research question.
- **Code.** `rl_module.py` feeds one `z_i` to both actor and critic, so
  the critic follows the claim feature of [A32] once that is built.

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

### [A20] A simple score for a run, following lifelong MAPD (Design change)

- **Where.** `2.Introduction.tex`: `sec:pf:measures` rewritten, the
  opening paragraph, contribution (iii), the dependent variables, the main
  RQ, RQ1, RQ3 and RQ4, and the [K2] deadline paragraph of `sec:pf:scope`.
  `4.Implementation.tex`: the section intro, `sec:impl:logging` and the new
  `tab:evalparams`. `2.Notation.tex`: the cost group and the scoring group.
  New figure `fig:timeline` (`thesis-progress/scripts/images/timeline.py`).
- **Change.** The weighted criterion `J(F,pi)` (`eq:functional`) and its
  five weights `q` are removed, and so are traffic concentration (`H_T`,
  `C_T`, `E^+_T`, `p_T`, `mu_T`, `eq:entropy`, `eq:concentration`, the [G8]
  convention, `fig:concentration`), movement cost `c_T` (`eq:movementcost`)
  and robustness as a term of the main RQ. The score now has six parts.
  1. Keeping up, `Lambda_T >= f_up * lambda_task` (`eq:throughput`), with
     the backlog `B_t` logged every timestep. A check, applied first.
  2. Mean service time (`eq:meanservice`), the result.
  3. Its split into waiting for an agent, travel and blocked time
     (`eq:split`), which add up to it. `W_T` (`eq:waiting`) is the blocked
     part.
  4. Crowding, the mean of `delta_i(t)` (`eq:crowding`), the congestion
     measure.
  5. Units relocated per storage update (`eq:relocation`), the slow-loop
     cost.
  6. Runtime per timestep (`eq:runtime`).
  The decision problem minimises expected service time subject to keeping
  up. `eq:rqformal` is a paired t-test over seeds, the 95% confidence
  interval of the mean per-seed gain lying above zero.
- **Why.** Decided by the author after the proposals in
  `scoring_proposal/` at the workspace root (versions 2 to 4). The weights
  `q` were never set anywhere, so `eq:rqformal` could not be computed, and
  any choice of weights would have set exchange rates between timesteps,
  cost units, task counts and a fraction. Ma et al. (2017), who define
  lifelong MAPD, judge an algorithm by service time and accept a run only
  if service time stays bounded, which the keep-up check states. Each
  measure is a count or an average, and each source is named. Service
  time, the keep-up condition and runtime come from Ma et al., throughput
  from the pick rate of Krnjaic et al. (2022), and the crowding density
  follows CRAMP, which uses it only in its reward. The split of service
  time, the averaging of crowding and the relocation count are the
  thesis's own. Concentration was dropped because it costs nothing unless
  it causes crowding and blocking, which are measured, and the storage
  rule already guards against it through `K`. Movement cost was dropped
  because the travel part shows the storage effect in the unit of the
  result. Robustness was dropped as a term because none of the papers in
  `thesis-progress/papers/` measures it as a quantity. They report means
  over many runs and vary the load, which `eq:rqformal` and RQ4 do. The
  paired test is possible because the order stream is seeded apart from
  the policy and the environment (`sec:impl:instances`).
- **Supersedes.** [G7] in part (`W_T` stays, as the blocked part of
  service time), [G8], and the objective part of [A4].
- **Still to decide.** `f_up`, the evaluation horizon `T` and the number
  of evaluation seeds (`tab:evalparams`).

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

### [A22] Hearing is one way in the communication graph (Error)

- **Where.** `sec:pf:observations`, the paragraph before `eq:commgraph`
  and the sentence after it. `tab:notation`, the `G^A_t` row.
- **Change.** The text now says an agent hears every agent inside its own
  field of view, and that on the directed graph hearing is one way. An
  edge `(a_i,a_j)` means `a_i` hears `a_j`.
- **Why.** The text said "each lies inside the other's field of view",
  but `eq:commgraph` tests one direction only, `eq:readout` aggregates over
  exactly those edges, and `communication_neighbours` in
  `slap-mapd-coupling` does the same. Three places agreed, so the
  sentence changed. (The code still takes a separate `communication_radius`
  instead of `d_obs`. Open item below.)

### [A23] The learning problem explained in words first (Clarity)

- **Where.** `sec:pf:game`, the opening up to `tab:posg`, the caption of
  `tab:posg`, and the paragraph on the assignment rule and conflict
  resolution.
- **Change.** The eight elements of the game are named in words before
  `eq:posg`. Two new paragraphs separate the policy (what each agent
  tries to do, a probability over its legal actions) from the transition
  kernel (the rule that turns state and joint action into the next state).
  The reward's domain now reads `U_1 x ... x U_m` instead of the undefined
  `U^m`.
- **Why.** The validation report flagged `U^m` as undefined and the
  section as equation-led. A citation for the POSG definition is still
  missing (`% TODO` in the text).

---

## Method (`4.Implementation.tex`)

### [A5] Controller realisations and overview (Design change, revised 2026-10-16 by [A32])

- **Where.** Section intro, `sec:method:overview`,
  `sec:method:controllers`, and the opening of `sec:method:rl`.
- **Change.**
  - Overview counts four controllers (three learned, one reference).
  - "Stages 2--3" becomes "stage 3". Stage 2 (assignment) is shared, so it
    never changes with the controller. This also matches the caption of
    `fig:methodloop`.
  - The reference router is Token Passing ([A28]).
  - **Centralised** is `π^cen_θ`, one network over all movable vertices,
    run once for each agent in priority order. Each run sees the agent's
    own `η_i` and the vertices the earlier agents have chosen, and its
    drawn move becomes part of what the next agent sees. A timestep takes
    `m` runs, so runtime grows with the fleet. Conflict resolution never
    overrides a centralised agent, so the override term of `eq:reward` is
    always zero for it. The text no longer calls this Knippenberg's
    centralised setup.
  - **Full-view setting** ([A32]). The decentralised router with every
    movable vertex in view and the pooled readout, each agent choosing
    alone on its own reward. It separates seeing more from choosing
    together with a shared reward. It runs under a few main conditions
    only and is not in `Π`.
  - The closing paragraph says the three learned routers share the encoder
    family, the masks, the reward, the training procedure and the budget,
    and differ in which agents choose together, so a difference in results
    is a difference in how many agents one decision covers.
  - `sec:method:rl` says the four RL components are reused on the larger
    graph (`V_mov`, or `Y_q ∪ H_q`), with two additions, the claim feature
    in `eq:features` and the claim mask `eq:claimmask`.
- **Why.** Realises [A2] and [A3].
- **History.** The centralised encoder ran once per timestep on all of `G`
  (first version), then once per agent ([A29]), and now once per agent in
  priority order with the earlier choices ([A32]). The closing paragraph
  said the routers "differ only in the graph the encoder runs on".

### [A6] Section-based boundary rule: ownership plus halo (Design change, revised 2026-10-16 by [A32])

- **Where.** `sec:method:controllers`, Section-based paragraph. New label
  `eq:halo`.
- **Change.**
  - **Ownership.** Zone `Y_q` owns the agents with `ℓ_i(t) ∈ Y_q` and runs
    the network once for each of them in priority order, as the
    centralised router does over the whole graph ([A32]).
  - **Halo.** Its network runs on `Y_q ∪ H_q`, where
    `H_q = { v ∉ Y_q : d_G(w,v) ≤ d_obs for some w ∈ Y_q }`. Halo vertices
    carry role and occupancy features, but no heads and no loss. The halo
    *is* the boundary protocol of `tab:information`.
  - **Other zones' agents.** A zone does not know their choices, so an
    agent treats every occupied halo vertex as a vertex whose agent has not
    chosen yet and does not move onto it ([A32]).
  - **Handover.** Ownership passes to the next zone on the timestep an
    agent enters it. Weights are shared across zones, so handover changes
    context, not policy.
  - **Cross-boundary conflicts.** Zones run in parallel. Two zones may
    still send agents onto the same empty vertex at the boundary, and the
    existing conflict-resolution operator removes these, as everywhere
    else.
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
    decentralised a continuum in how many agents one decision covers. It
    used to read "in how much each controller sees", before [A32].
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

### [A9] Training: equal budget and credit (Design change, credit decided 2026-10-16 by [A32])

- **Where.** `sec:method:training`, `eq:credit`, and `tab:trainparams`.
- **Change.**
  - Each learned router is trained separately under the same PPO procedure
    with the same environment-step budget, and both training regimes
    (under `F_fix` only, and matched) apply to each.
  - One environment step is one timestep of the warehouse, however many
    agents choose within it.
  - Each agent's choice is one training sample with its own value
    estimate, credited with `eq:credit`, the mean reward of the agents that
    chose together with it at that timestep. These are the whole fleet for
    the centralised router, the agents in the same zone at `t` for the
    section-based router, and the agent alone for the decentralised router
    and the full-view setting.
  - The credit row of `tab:trainparams` is gone. The budget row says "one
    per timestep".
- **Why.** An equal budget keeps the comparison about the controller, not
  training effort. Counting a timestep as one step means the centralised
  arm's `m` network runs per timestep show as runtime and training time,
  not as extra experience. Knippenberg's 24-hour wall-clock budget mixes
  compute speed with learning, and the step budget keeps the two apart.
  Credit follows the agents that choose together, because they act as one
  decision-maker.
- **History.** The credit choice was left TBD as the lever behind the
  commons contrast. The commons question is no longer part of the study.
- **Open.** Each agent's choice is its own PPO sample with its own ratio.
  Updating on the whole joint action of one decision is the alternative.
  To be settled in the code, not stated in the thesis yet.

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

### [A24] One definition of the blocked indicator (Error)

- **Where.** `sec:method:rl` (the override-flag sentences after
  `eq:reward`), `sec:method:resolution` (the paragraph on the override
  flag), `sec:impl:logging`.
- **Change.** The Method now follows `eq:split` in the Introduction.
  `omega_j(t)` is 1 when the serving agent stands still, either by a chosen
  wait or by an override. The override flag is one of the two inputs to
  it, and alone it is the reward's override indicator.
- **Why.** The Method said the override flag "defines" `omega_j(t)`,
  which would leave chosen waits out of blocked time and break the
  three-part split of service time. The author confirmed the Introduction
  is the intended definition.

---

### [A25] Field of view is measured by travel cost, not hops (Error)

- **Where.** `sec:pf:env` (the field-of-view paragraph and
  `eq:localsubgraph`), `eq:congestion` (one sentence before it),
  `sec:pf:observations` (the field-of-view subsection, the "anything past"
  sentence, `eq:commgraph`, `tab:observationexample`), `eq:halo` and the
  `d_obs` row of the parameter table in the Method, and `tab:notation`
  (the `d^hop_G` row is removed, rows for `H_q`, `d_obs`, `V_i^(d_obs)` and
  `G^A_t` reworded).
- **Change.** The field of view, the halo, the congestion feature and the
  communication graph are bounded by the travel cost `d_G`. `d^hop_G` is
  gone. `d_obs` is a positive real in the unit of edge cost, not an
  integer hop count. Hearing stays one way, with the distance taken from
  the listener's position to the sender's. The value of `d_obs` stays TBD.
  Replaces the hop count of [A21].
- **Why.** An edge's cost is its length. With every cost equal to 1 the
  world behaves like a lattice, and an edge of cost 5 behaves like five
  cells, so how far an agent sees or hears must depend on edge cost. The
  hop count of [A21] came from a misunderstanding of one word. The code
  already uses the cost distance.

### [A26] Storage estimates cover one storage period, per step (Design change)

- **Where.** `sec:pf:storage` (new paragraph and `eq:estimates` after the
  causality sentence of `eq:storageupdate`), the "steady pattern" paragraph
  in `sec:pf:coupling` (two-timescale consequence), the `W_T` versus
  `\hat w_t(e)` paragraph in the service-time section, the storage ladder
  in the Method (new paragraph after `eq:storagegreedy`), and the
  `\hat\rho`, `\hat\mu`, `\hat w` rows of `tab:notation`.
- **Change.** The three estimates are computed over a tumbling window equal
  to the storage period. At an update an estimate covers only the steps
  since the previous update, and the next window starts fresh. They are
  per step (a count divided by the number of steps), so their size does not
  depend on `Delta`. If no order was released in the window, for example
  before the first update, the update is skipped and the placement stays.
  `\hat w_t(e)` is described as a forecast from past data only, not as
  looking ahead.
- **Why.** A short fixed window matches what the thesis already says about
  traffic settling between updates and adds no new parameter. Per step
  units keep `beta` comparable across the sweep of `Delta`. Skipping an
  empty first update avoids relocating stock on no evidence.
- **Open.** Which edge a wait is charged to is not decided. The thesis
  still says "attributed to an edge or its downstream contention point"
  (`sec:pf:storage`, the sentence after `eq:storageupdate`) and
  `eq:estimates` says "waits attributed to `e`".

### [A27] The message is the sender's embedding, with no message head (Design change)

- **Where.** `sec:method:model` (`eq:message` and the paragraph after
  `eq:readout`), `tab:modelparams` (the message-width row is gone) and the
  `\xi_j(t)` row of `2.Notation.tex`.
- **Change.** `xi_j(t) = h^(L)_{l_j(t)}` replaces
  `MSG_theta(h^(L)_{l_j(t)})`. A message is the sender's own final-layer
  embedding, sent as it is, with the width of that embedding (the hidden
  width, or the raw vertex features at `L = 0`). Messages are still trained
  end to end, because the receiver's loss reaches the sender's embedding
  through the shared weights.
- **Why.** The readout takes a mean of the messages and feeds it to a
  linear layer. A plain linear message head in front of that adds only a
  narrowing step and an undecided width, so it is dropped. Sharing the
  embedding follows CRAMP (check its Figure 2, "Local broadcasting"). Chosen
  with the L2 design in `fix_prs_plan.md` ("L2a and L2b design"), which also
  rejected storing the sender's embedding in the sample (it needs RLlib
  connectors) in favour of carrying the senders' views in the receiver's
  sample.
- **Code.** L2b (`fix/learned-messages`).
- **Open.** Both citations after "as in" in the new paragraph should be
  checked against the sources. PICO uses a message head, and CRAMP may
  share the encoder vector directly.

### [A28] Deadlock in dead-end corridors, Token Passing as the baseline (Design change, thesis text edited 2026-10-13)

- **Where.** `4.Implementation.tex`, the "Reference baseline" paragraph and
  the sentence on the shared assignment above it, and `2.Introduction.tex`,
  the well-formedness paragraphs in `sec:pf:agents` (`fig:wellformed`). All
  four places carry a `% [A28]` tag.
- **What the edit says (2026-10-13).**
  - The reference baseline is Token Passing. It chooses its own tasks and
    does not use the assignment rule, so the sentence saying the reference
    planner shares the assignment is removed. Prioritised A\* is not
    described in the thesis. It stays in the code as a second reference.
  - Agents ask for the token in order of agent index. "Closest" is the
    number of moves. A planned path treats a vertex as taken from one step
    before another agent arrives on it until one step after it leaves, so
    conflict resolution never has to change a plan. Ma et al. allow agents
    to follow each other and conflict resolution here does not.
  - The well-formedness paragraph names Token Passing as the one baseline
    (the mention of the centralised MAPD baseline is gone), defines a
    non-task endpoint as a vertex of $V_{\mathrm{ep}}$ in neither
    $V_{\mathrm{str}}$ nor $V_{\mathrm{del}}$, and says the guarantee
    depends on the baseline's task rule and planning, that it means no
    deadlock, and that it says nothing about how the backlog develops.
  - Condition a) of Ma et al.'s Definition 1, a finite number of tasks, is
    left out on purpose. It is a property of the order stream, not of the
    instance. Well-formedness is required of every instance as an
    assumption. In the paper it is a sufficient condition, so the text does
    not call it necessary for solvability.
  - Open in the code, not in the text. `check_well_formedness` counts
    $V_{\mathrm{ep}} \cup V_{\mathrm{str}} \cup V_{\mathrm{del}}$ against
    $m$, and the environment needs $m$ vertices in $V_{\mathrm{ep}}$ to
    place the agents. The text now says non-task endpoints, so the
    validator should count those.
- **What was found (2026-10-13).** On the example 04 instance (seed 42,
  `slap-mapd-coupling` at `0c7b08b`) delivery vertex 22 has one exit,
  vertex 21, at the end of a one-lane corridor (19, 20, 21, 22). An agent
  rests at 22 after delivering and needs 21 to leave, while another agent
  arrives at 21 to deliver to 22. Swapping places is forbidden by the swap
  rule, and conflict resolution only turns a conflicting move into a wait,
  so neither ever moves again.
  - Reference planner: 12 tasks complete by t = 84 of 2000, none after,
    and every agent stands still for about 1,980 steps.
  - Learned policy after only 7 PPO iterations: 166, 25 and 26 tasks in
    three evaluation episodes. In the two low episodes all agents ended in
    the corridor.
  - The instance passes the well-formedness check, because a dead end is
    never on the route between two other endpoints.
- **Cause in the planner.** Prioritised A\* plans the earliest-assigned
  agent first and treats a lower-priority agent's resting vertex as free.
  The lower-priority agent then finds every way out crossing the reserved
  route, waits, and the whole thing is replanned from scratch every tick
  with the same result. Nothing makes an agent back off.
- **Decision (author, 2026-10-13).** The reference baseline is Token Passing
  (Ma et al.), not prioritised A\*. The well-formedness assumption exists
  for its guarantee, and `2.Introduction.tex` already calls it a baseline.
  The Method paragraph must be rewritten to match. For now the thesis text
  names one baseline, Token Passing, and does not describe prioritised A\*.
- **Proposed for the three learned arms (not yet confirmed).** No change to
  the arms, the shared assignment rule or conflict resolution for now.
  The thesis already says a run that does not keep up is reported as such
  (`eq:throughput`). First measure how often a trained policy ends in a
  jam, as a stall rate per arm over the evaluation seeds, from the episode
  trace. The 7-iteration result says little about a trained policy, and the
  reward already charges `n_blocked` every step. If trained policies still
  jam often, choose between two fixes, trying the first:
  1. Tighten the instance assumption so that no storage or delivery vertex
     sits in a dead-end corridor (a generator check and a sentence in the
     well-formedness paragraph). It applies equally to every arm and
     touches no decision logic, but it only reduces the problem, since
     head-on agents in any one-lane corridor can still jam.
  2. Add Token Passing's task rule to the shared assignment, so a task is
     handed out only if its pickup and delivery vertices are not another
     agent's goal. Fair to every arm, but it changes `eq:assignmentrule`.
  Undecided: ending a training episode early on a stall, since a jammed
  episode wastes the rest of its 2000 steps on stuck agents. It is a
  training rule the thesis does not have, and it needs a threshold for how
  many steps count as a stall (the study value is TBD, no default). The
  trace command uses 50 as a display setting (`DEFAULT_DEAD_AFTER`), about
  3.5 times the longest healthy still run measured so far, 14 steps, which is
  one episode of a barely trained policy. The stall is defined as
  the whole fleet standing still (no agent changing vertex, overridden or
  chosen wait alike) for N steps in a row while a task is active. The
  per-agent version, an agent holding a task that has not moved for N
  steps, fires earlier and may be better. N must exceed the longest still
  run in healthy trained episodes, measured in B20. Measured so far, the
  planner jams for good (about 1900 steps) while a sampled policy recovers
  from stretches of 94 and 223 steps, so a small N would cut runs that
  recover. In evaluation it is only a flag in the trace, never a stop.
  It could also make a jam
  cheaper, because the override penalty stops being charged once the
  episode is cut. If chosen, it should truncate and bootstrap, not
  terminate, apply to training only, and get a sentence in
  `sec:method:training`. Measure the stall rate in training first.
- **Why.** The study compares learned arms that differ only in their
  window. Giving a controller Token Passing logic would make it a planner
  and remove that contrast. The guarantee of Token Passing comes from how it
  plans and assigns, not from the instance property alone, which the
  well-formedness paragraph already says.
- **Open.**
  - Whether Token Passing runs on its own task selection or on the shared
    assignment. Its guarantee needs its own rule, so the planner would have
    to take over stage 2 of the loop for that run.
  - Whether prioritised A\* stays in the code as a second reference. The
    thesis text names one baseline for now, so this does not hold up the
    thesis edit.
  - Noticed while reading, not part of this change: the proof in
    `sec:method:resolution` that a wait is always feasible does not hold
    for a higher-priority agent moving into a lower-priority agent's vertex.
    The code works around it with a current-vertex reservation and says so
    in the `conflict_resolution.py` docstring.
- **Code.** Specs B15 to B20 and D2 in `fix_prs_plan.md` (workspace root).

### [A29] The wider routers: one pass per agent, a pooled readout, and a window that is never truncated (Design change, thesis text edited 2026-10-13, revised 2026-10-16 by [A32])

**Revision note ([A32]).** The per-agent pass, the pooled readout and the
padding cap all stay. Three things changed. The passes now run in priority
order, and each sees the vertices the earlier agents have chosen. The
single shared pass is rejected because no agent would see another's
choice, not because it replaces the vertex features. The credit is no
longer open (`eq:credit`). The arm this entry describes, a per-agent pass
over the whole graph with independent choices, is kept as the full-view
setting. The text below is the 2026-10-13 entry, and the points it gets
wrong under [A32] are marked.

- **Where.** `4.Implementation.tex`, the [A8] paragraph in `sec:method:model`
  (replaced), `tab:modelparams` (the two [A8] rows replaced and two rows
  added), the centralised paragraph in `sec:method:controllers`, and the
  visible vertex set in `sec:method:rl`. `2.Notation.tex` gets one row and
  `styles/eqnames.tex` gets `eq:pooledreadout`. The places carry a `% [A29]`
  tag.
- **What the edit says.**
  - Each agent runs the network on its own copy of the window, with its own
    η_i in the vertex features and shared weights. This is the first option
    of [A8]. A single pass with each agent's task marked at the vertex it
    occupies is named and not used, because it replaces the vertex features.
  - The centralised and section-based readouts add the mean of the
    final-layer embeddings over the vertices the router owns, all movable
    vertices for the centralised router and the zone for the section-based
    router.
    The halo is left out. The decentralised readout has no such term. The
    pooled term sits between the own embedding and δ_i(t), a placement the
    code makes and the text now states (`eq:pooledreadout`).
  - The centralised window is all movable vertices, not all of V, so the
    sentence in `sec:method:rl` now says V_mov.
  - The sentence that said the encoder runs once per timestep on G now says it
    runs on G for each agent, and the sentence that said agents share one
    graph pass is gone.
  - New `tab:modelparams` rows: the padding cap (set to the largest window so
    that none is truncated) and the number of zones p (TBD, sweep). The
    pooling row says "none" is an ablation.
- **Why.** The study compares learned arms that differ only in their window
  (no longer true under [A32]).
  Without pooling a window larger than L hops adds nothing, so the
  centralised arm would carry the same information as a decentralised arm with
  no messages. One pass per agent keeps `eq:features` as written. The cost
  was measured in the code (spike 0B in `L4_design.md`): the whole-graph
  window costs about 1.1 to 2.5 times the example 04 field of view per
  rollout step and 3.3 to 4.7 times per training minibatch, and about 1.5
  times an untruncated field of view. Each arm pools over its own space so
  that the pooled term follows the window and adds no other difference.
- **Open.**
  - The zone rule. The thesis defines the zone partition (`eq:partition`)
    and not how zones are drawn. The code draws blocks of consecutive aisles
    as equal as possible (design choice, no citation), and the thesis has no
    sentence for it yet.
  - Mean pooling is a plausible choice and has not been tested for
    learning. A sum or a max would behave differently, and a mean dilutes a
    local signal in a large graph. The `none` setting is kept as an ablation.
  - The credit signal of [A9] stays TBD. The code supports both options and
    has no default. Decided by [A32], `eq:credit`. The code default is to be
    set when the controllers are rebuilt.
  - Example 04 truncated its field of view at 12 nodes while most were
    larger. The code now raises when a window exceeds the cap (decision 15
    of `thesis-progress/decisions/decision_log.md`), and the examples are being changed to set the
    cap from the graph.
- **Code.** `L4_design.md` and `L4_agent_plans/` (workspace root). Packages
  B1 (zones by aisle), B2 (the window), B3 (pooling).

### [A30] A standing-still step costs `c_wait` in the reward (Design change, thesis text edited 2026-10-14)

- **Where.** `4.Implementation.tex`, `eq:reward` and the paragraph after it in
  the Reward paragraph, one row in `tab:rlparams`, and the sentence at the end
  of `sec:method:training`. `2.Notation.tex`, the `c_wait` row. The places
  carry a `% [A30]` tag.
- **What the edit says.**
  - `eq:reward` gets a fifth term, `- c_wait * omega_i(t)`. `omega_i(t)` is
    the blocked indicator of `eq:split` for the task agent i serves, and 0
    for an idle agent, so a parked free agent pays nothing.
  - A chosen wait and an override both cost `c_wait`, and an override also
    costs `n_blocked`. Yielding is therefore never dearer than being
    overridden.
  - The shaping term and `c_wait` are in the units of an edge cost, so the
    policy weighs a step of waiting against a step away from the target. The
    wait term is not shaping, as the congestion term is not.
  - `tab:rlparams` gets `c_wait` = 0.1, below the cheapest edge (0.5 in the
    example instance). The sentence at the end of `sec:method:training`
    now says `c_wait` is a reward weight reported with the training
    configuration, where it used to point at a footnote.
  - The `% [A24]` sentence that said an override is one of two ways to stand
    still moved into this paragraph, where the same fact is now stated through
    `omega_i(t)`. The `[A24]` tags in the logging text are unchanged.
- **Why.** `c_wait` was defined (`eq:onestepcost`) and nothing read it, so the
  sentence that it decides whether an agent yields or detours was not true
  of any result (issue #147). With a flat penalty on chosen waits alone, a
  forced stop would have been cheaper than yielding, because an override
  costs `n_blocked` = 0.5. Counting every standing-still step of a serving agent
  fixes that order. The trained arms stand still in about 4 to 15% of their
  steps (waited plus overridden), so at 0.1 the term is of the order of the
  override term and well below shaping and delivery. That is measured on the
  fixed-storage runs of 2026-10-14 and inferred for the new reward.
- **Open.**
  - 0.1 is a starting value. Whether the wait term changes behaviour, or
    only adds noise, is not known until the retrained arms are compared with
    the old ones.
  - Token Passing still minimises timesteps and does not price a wait at
    `c_wait`. The thesis says so in the Reference baseline paragraph, and
    that choice is not changed here.
- **Code.** `environment/reward_function.py` needs the term, a
  `wait_cost` argument and a fifth key in the logged reward terms, and
  example 04 sets `WAIT_COST` to 0.1. Not done yet.

### [A31] Keep-up threshold, horizon and load levels (Thesis values set 2026-10-14)

- **Where.** `4.Implementation.tex`, `tab:evalparams` (values, one new row)
  and the paragraph after it. `2.Introduction.tex`, the "Keeping up"
  paragraph after `eq:throughput`. The places carry a `% [A31]` tag.
- **What the edit says.** `f_up` = 0.8, `T` = 630 and the load levels
  `lambda_task` = 0.15, 0.25, 0.3 and 0.4 tasks per step. The paragraph says
  where they come from, a Token Passing pilot on the example instance with
  three agents, and that they are set again when the fleet or the instance
  changes. The Keeping up paragraph says arrivals are random and tasks under
  way at the horizon do not count as finished, so `f_up` is below 1.
- **Why (measured, `slap-mapd-coupling` sweep of 2026-10-14, 6 seeds).**
  Token Passing finishes about 0.3 tasks per step at most. `eq:throughput` divides by
  the nominal `lambda_task`, but the tasks released vary by run (85 to 108
  against a nominal 94 at 0.15). At `f_up` = 0.9 Token Passing failed 2 of 6
  healthy seeds at 0.15 and 3 of 6 at 0.25. At 0.8 it passes 6 of 6 at 0.15,
  0.25 and 0.3 and 0 of 6 at 0.4, so the threshold sits where the fleet
  stops keeping up. The learned arms, trained at 0.15, pass 6 of 6 at 0.15
  and mostly fail at 0.25, so one policy per load level is needed (issue
  #146).
- **Open.**
  - The alternative, dividing by the tasks actually released, would remove
    the arrival noise from the check. It changes `eq:throughput` and is not
    adopted.
  - The values rest on one instance, three agents and 6 seeds. The training
    regime (one policy per load level or one policy at every load) and the
    rollout length, which now equals `T`, are still open in
    `tab:trainparams`.
- **Code.** `keep_up_threshold` is still unset in the examples. Setting it
  to 0.8 in examples 04 and 05 is not done yet.

### [A32] Real centralised and section-based controllers (Design change, thesis text edited from 2026-10-16, in progress)

- **Where.** So far `2.Introduction.tex`, the overview paragraph, the
  controller factor in `sec:pd-aim-and-scope` and RQ2. `5.Experiments.tex`,
  the RQ2 results placeholder and the "What deciding together changes"
  discussion placeholder. `sec:pf:controllers`, the joint action sentence,
  `tab:information` (new column "One decision covers"),
  `eq:centralisedpolicy`, `eq:sectionpolicy`, the collision rule and the
  critic reason. `2.Notation.tex`, the `u_{\prec i}(t)` row. The places
  carry a `% [A32]` tag. `sec:pf:game`, the cycle paragraph, the policy
  paragraph, the paragraph after `eq:obsfunction` (the controllers differ
  in what an agent observes and in which agents choose together), the
  nested observations paragraph and the credit paragraph (credit follows
  the agents that choose together). `eq:posg` and `eq:obsfunction` are
  unchanged, since earlier agents' choices are made inside the policy and
  are not part of the state. `4.Implementation.tex`,
  `sec:method:controllers`, the centralised and section-based paragraphs
  (one run per agent in priority order, occupied halo vertices are not
  entered, zones in parallel), a new "Full-view setting" paragraph and the
  closing paragraph. The false claim that the centralised router is
  Knippenberg's centralised setup is gone. The override term of
  `eq:reward` is always zero for a centralised agent. `sec:method:rl`, the
  opening paragraph, a fourth entry in `eq:features` (vertex chosen by an
  earlier agent, set `V_{\prec i}(t)`, empty for the decentralised router),
  the claim mask `eq:claimmask` added to `eq:mask`. `sec:method:model`, the
  per-agent copy paragraph (runs follow the priority order), one sentence
  on why the pooled readout stays, the critic paragraph, two rows of
  `tab:modelparams`. `2.Notation.tex`, rows for `V_{\prec i}(t)` and
  `M^{\prec}_i`. `styles/eqnames.tex`, `eq:claimmask`.
  `sec:method:training`, one environment step is one timestep, and the
  open credit choice is replaced by the credit `eq:credit`, the mean reward
  of the agents that choose together. The credit row of `tab:trainparams`
  is gone. `2.Notation.tex`, the `A_i(t)`, `bar R_i(t)` row.
  `styles/eqnames.tex`, `eq:credit`. Chapter text done 2026-10-16.
  - The full-view comparison separates seeing more from choosing together
    with a shared reward, since a full-view agent is credited with its own
    reward. A fourth setting to split choosing together from the shared
    reward is not added.
- **What the edit says.**
  - The controllers differ in how many agents one decision covers, the whole
    fleet, one zone or a single agent, and what each sees follows from that.
    They no longer "differ only in the information they condition on".
  - RQ2 asks how the coupling effect differs between controllers that differ
    in how many agents one decision covers. Its results placeholder reports
    mean runtime `kappa_T` next to the gain.
  - The discussion uses the full-view setting (the decentralised controller
    with the whole graph in view) to tell seeing more apart from deciding
    together.
  - The overview paragraph names Token Passing as the reference baseline. It
    still said "prioritised planner", which `[A28]` had replaced.
- **Why.** The arms as built after `[A3]` and `[A29]` are one per-robot policy
  with a wider window, sampled independently, so the centralised arm is the
  decentralised arm with a large view (Knippenberg's multi-agent setup, not
  his single-agent one). The design decided with the author is in
  `thesis-progress/decisions/done/real_centralised_design.md`, Part 3.
  - Centralised. Agents decide one at a time in the episode priority order,
    each seeing the vertices earlier agents have claimed this timestep. The
    policy is the chain rule over agents, so it can represent any joint
    distribution at a cost linear in `m`.
  - Section-based. The same per zone on the zone plus halo, zones in
    parallel, cross-zone clashes to conflict resolution.
  - An agent may enter an occupied vertex only if its agent has already
    decided to leave it, so a unit never produces a clash.
  - Credit is the unit's mean reward. The credit row of `tab:trainparams`
    goes.
  - The training budget stays in environment steps. Runtime `kappa_T` is
    where the cost of deciding for more agents shows.
  - The original "which architecture degrades slowest" question and the
    commons question are not used.
- **Open.**
  - Citations for policies that choose agents' actions one after another
    (Wen et al. 2022, Fu et al. 2022), not yet verified.
  - The chain-rule sentence after `eq:centralisedpolicy` says any joint
    distribution can be written as the product. The network sees only
    occupancy and an unlabelled set of chosen vertices, within L hops plus
    the pooled readout, and only its own target. A sentence saying so was
    added on 2026-10-16.
  - First in the priority order means choosing first, not right of way. An
    earlier agent may not enter the vertex of a later agent that has not
    chosen, so in a corridor the later agent is the one that steps aside.
    A sentence after "prioritised planning one timestep ahead" was added on
    2026-10-16.
  - The fleet size RQ2 is run at. Decided by the author later on
    2026-10-16, not yet in the thesis: the first result uses a generated
    warehouse with 8 agents and 94 vertices (9 aisles, 3 zones), at load
    0.3, which is an overload there (Token Passing finishes 0.26 to 0.27).
    `sec:impl:instances` and `tab:evalparams` still need the wording
    (`thesis-progress/archive/workspace/ROADMAP.md`, Milestone 1).
  - Resolved. RLlib's turn-based multi-agent environment supports the
    sub-steps (step 0 spike of `real_controllers_plan.md`, 2026-10-16).
  - `[A1]`, `[A2]`, `[A3]`, `[A4]`, `[A5]`, `[A6]`, `[A8]`, `[A9]`, `[A12]`,
    `[A13]` and `[A29]` rewritten to match on 2026-10-16. The two `[A4]`
    sentences (the loop sentence and the first factor after
    `eq:rqformal`) and `3.Background.tex` ("the same three controllers of
    `tab:information`") were brought into line the same day.
- **Code.** Plan in `real_controllers_plan.md` at the workspace root.
  Every step merged into `main` on 2026-10-16 (#161 claim mask, #162 claim
  feature, #163 credit and full-view setting, #164 turn-based adapter, #165
  budget per timestep and the seed fix), then #166 (evaluation through
  turns) and #167 (configs and docs). Checkpoints from before #162 no longer load,
  since the vertex features grew from 6 to 7 entries.

### [A34] Skewed demand that drifts (Design change, thesis text edited 2026-10-17)

- **Where.** `2.Introduction.tex`, `sec:pf:tasks`, after `P_ord` is named.
  `4.Implementation.tex`, `sec:impl:instances` (three paragraphs) and two
  rows of `tab:evalparams`. The places carry a `% [A34]` tag.
- **What the edit says.** Popularity is skewed and changes over time, and
  the storage layer only sees the orders. In the realisation each order asks
  for one SKU, the SKU in rank r is asked for in proportion to 1/(r+1) (Zipf,
  skew 1), and the ranking moves five places every 200 steps. Pickup and
  delivery are drawn as before. The draw uses the same random numbers
  whatever is in stock, so the orders are identical under every controller
  and storage rule. No new symbols, since the values are fixed.
- **Why (measured, demand probe of 2026-10-17,
  `thesis-progress/decisions/done/demand_probe_2026-10-17.md`).** Uniform demand
  gives adaptive storage nothing to gain, so RQ1 was empty
  (`thesis-progress/decisions/decision_log.md` #1). With a fixed skew the demand rule gained almost
  nothing over a good starting stock. With the drift, Token Passing under
  fixed storage lost about 15% throughput and the demand rule won most of it
  back, and at load 0.3 service time fell by 27% (Token Passing) and 44% to
  59% (the night's decentralised policies).
- **Open.** The values come from one instance, one planner and two policies
  trained under uniform demand. A sweep of the skew and the drift is not
  planned yet.
- **Code.** PR A of `adaptive_storage_impl_plan.md` (workspace root), in
  progress.

### [A35] Starting stock from expected demand, in blocks (Design change, thesis text edited 2026-10-17)

- **Where.** `4.Implementation.tex`, `sec:impl:instances`, after the [A34]
  paragraphs. Tagged `% [A35]`.
- **What the edit says.** Every storage rule starts from the same `x_0`,
  computed once from the popularity at t = 0. Storage vertices are ordered by
  mean distance to the delivery vertices, and the most popular SKUs fill the
  nearest vertex, ceil(|K| / |V_str|) SKUs per vertex, then the next.
- **Why.** A random start makes fixed storage a weak baseline (#95). In the
  probe the block placement beat one popular SKU per vertex under fixed
  storage (0.443 against 0.391 throughput with 100 SKUs). The mean distance
  is used because an order picks its delivery vertex uniformly.
- **Open.** `F_dem` and `F_cng` still rank storage vertices by the nearest
  delivery vertex (`thesis-progress/decisions/decision_log.md` #9, decided to stay until the
  congestion rule is settled).
- **Code.** PR B of `adaptive_storage_impl_plan.md`.

### [A36] How a wait is attributed to an edge (Gap, thesis text edited 2026-10-17)

- **Where.** `4.Implementation.tex`, `sec:method:storage`, after the [A26]
  paragraph. Tagged `% [A36]`.
- **What the edit says.** Whenever the agent serving a task stands still,
  one wait is counted on the next edge of its shortest route to its current
  goal, whether it chose to wait or was overridden. No wait for an agent
  without a task or at its goal.
- **Why.** `eq:estimates` only said "waits attributed to e"
  (`thesis-progress/decisions/decision_log.md` #21). The code counted only overridden moves, so
  for Token Passing and the centralised arm, which never collide, `w_hat`
  was always 0 and `F_cng` equalled `F_dem`. The rule was decided in
  `adaptive_storage_plan.md` section 2, and on 2026-10-17 the author agreed
  it also replaces how overridden moves are charged.
- **Code.** PR C of `adaptive_storage_impl_plan.md`.

### [A37] Storage rule wording fixes (Error, thesis text edited 2026-10-17)

- **Where.** `4.Implementation.tex`, `sec:method:storage`, the opening
  paragraph and `eq:storagegreedy` with the sentence after it. Tagged
  `% [A37]`.
- **What the edit says.** The ladder sentence no longer calls the
  `F_dem` to `F_cng` gap "exactly this thesis's contribution". It is the
  storage half of RQ3 (`thesis-progress/decisions/decision_log.md` #20). The access term reads
  `min_{g in V_del} d_G(v, g)` (#10, was the typo `d_G(v, min_g)`). SKUs are
  placed in descending order of demand, each to the free vertex with the
  lowest score (#8, read literally the old text gave rarely ordered SKUs the
  best vertices first).
- **Code.** None, the code already did this.

### [A38] Storage decided when stock arrives (Design change, thesis text edited 2026-10-18, uncommitted)

- **Where.** `2.Introduction.tex`, `sec:pf:storage`: the paragraphs from "Stock
  changes in two ways" to the storage objective, the estimates paragraph,
  the new `eq:arrivals`, the fixed-storage paragraph, the definition of F, and
  `eq:storageobjective` with the paragraphs after it; `sec:pf:coupling`, two
  sentences of the loop paragraph. `4.Implementation.tex`,
  `sec:method:storage` (the three rules, the [A26] sentence, the paragraph
  that replaces the hard cap, the pilot result, `tab:storageparams`) and
  `sec:impl:instances` (starting stock). `2.Notation.tex` and
  `styles/eqnames.tex`. All tagged `% [A38]`.
- **What the edit says.** Picking uses stock up. Every Delta timesteps new
  stock arrives at the receiving vertices V_rcv (the delivery vertices), and
  the storage rule decides which shelves it goes to. Stock already on a shelf
  never moves. The storage update becomes `x_t = F(x_t^-, y_t, estimates)`
  with `x_t >= x_t^-` and at most `y_t(k)` units added per SKU. The arrivals
  `eq:arrivals` fill each SKU up to `max(x_min, ceil((1 + epsilon) Delta
  rho_hat))` plus its waiting orders, the same under every rule. F_fix is
  dedicated storage (arrivals to the home shelf), F_dem and F_cng place
  arrivals by access distance and by the congestion-aware score. The
  reassignment term R, its weight chi and the cap nu are gone. New symbols:
  `V_rcv`, `x_t^-`, `y_t(k)`, `x^up_t(k)`, `epsilon`, `x_min`. Removed:
  `R`, `chi`, `nu` (the cap).
- **Why (measured, arrival probe of 2026-10-18,
  `thesis-progress/decisions/done/arrival_probe_2026-10-18.md`).** Relocation under
  a cap moved stock for free and left split SKUs with leftover units. Deciding
  at arrival cut service time at load 0.3 by 43% against fixed storage (25%
  with relocation), with the same fixed baseline, and its put-away is shorter
  than fixed storage's. Matches the dynamic SLAP as Waubert de Puiseau et al.
  (2022) define it. Adopted by the author on 2026-10-18
  (`thesis-progress/decisions/done/arrival_storage_plan.md`).
- **Open.** The values of epsilon, x_min and Delta (`tab:storageparams`, TBD).
  `fig:dkr` was redrawn on 2026-10-18 with D and K only, the bars labelled
  fixed storage and adaptive rule (`storage_update_example.py`).
  `fig:storageexample` was redrawn on 2026-10-18 as `arrival_storage.png`
  (`arrival_storage.py`): fixed storage sends arriving tea to its far home
  shelf, an adaptive rule to the nearest shelf with room, the old tea stays,
  and an order walks 3 edges against 1. The sentences before the figure and
  before `fig:dkr` were reworded to match. Replaces the proposals
  `[A38]` to `[A40]` of `stock_template_2026-10-17.md`, which were never
  applied.
- **Code.** PR G to J of `arrival_storage_plan.md`, uncommitted, acceptance
  passed.

### [A39] Orders take a unit from the nearest shelf, or wait for stock (Design change, thesis text edited 2026-10-18, uncommitted)

- **Where.** `2.Introduction.tex`, `sec:pf:tasks` (the stock condition and
  the new `eq:pickuprule` paragraph, replacing the "placement template"
  sentence), `sec:pf:measures` (the backlog and one sentence in the
  service-time split). `4.Implementation.tex`, `sec:impl:instances` (how an
  order is drawn). Tagged `% [A39]`.
- **What the edit says.** An order takes one unit from the vertex holding its
  SKU that is nearest its delivery vertex, ties by vertex index. With no unit
  anywhere it waits and becomes a task once stock arrives, keeping its release
  time, so the wait for stock counts in its service time and in the wait
  before assignment. The stock condition holds at the step the unit is taken.
  The backlog counts waiting orders, `B_t = |Q_t| + |B_t| + |Z^wait_t|`. The SKU
  is drawn without looking at stock. New symbol: `Z^wait_t(k)`.
- **Why.** Units must run out for the nearest-shelf pickup to make sense, or
  one unit near each delivery vertex would serve every order. The arrival
  probe attributes about 2 timesteps of the 8 extra gain at load 0.3 to the
  pickup rule.
- **Code.** PR H and J.

### [A33] The commons question folded into RQ4 (Design change, thesis text edited 2026-10-19, uncommitted)

- **Where.** `2.Introduction.tex`, the factors paragraph after `eq:rqformal`.
  `5.Experiments.tex`, "Mapping questions to comparisons". Tagged `% [A33]`.
- **What the edit says.** On the fleet sweep of RQ4, throughput per agent,
  `Lambda_T / m`, shows whether each agent finishes fewer tasks as the fleet
  grows, and whether that loss is faster when one decision covers fewer
  agents.
- **Why.** The author reinstated the commons question on 2026-10-16
  (proposed as RQ6 in `thesis-progress/archive/workspace/ROADMAP.md`). It uses the same runs and the same
  measure as RQ4, so a sixth question would only split the reader's
  attention. Agreed 2026-10-19 (`research_goals_2026-10-18.md`, change 7).
- **Code.** None. `Lambda_T` and `m` are already logged.

### [A41] Research questions built around the main result (Design change, thesis text edited 2026-10-19, uncommitted)

- **Where.** `2.Introduction.tex`, the factor list and the sentence after it,
  RQ1, RQ2, RQ4, a new paragraph after the RQ list, and one sentence in the
  factors paragraph after `eq:rqformal`. Tagged `% [A41]`.
- **What the edit says.** The first factor is the storage rule (fixed,
  demand-only or congestion-aware). Storage rule and controller carry the
  main result, and the other factors bound it. RQ1 asks for the gain at a
  load where the fleet keeps up. RQ2 asks how the gain of RQ1 differs between
  controllers. RQ4 asks at what load the gain stops holding and at what load
  each controller stops keeping up. A new paragraph names the main result,
  the paired service time gain per controller with its interval and its
  split, answered by RQ1 and RQ2 together. The gain is read with its split,
  because a fleet near its limit turns the same travel saving into a larger
  cut in the wait for an agent.
- **Why.** The author agreed one main result on 2026-10-18
  (`short_run_2026-10-18.md`) and applied changes 1, 3, 4, 6 and 9 of
  `research_goals_2026-10-18.md` on 2026-10-19.
- **Not applied.** Change 2 (the main question), change 5 (RQ3 for storage
  only), change 10 (the formal factors) and change 11 (made obsolete by the
  arrival model of [A38]). The third item of the factor list stays as it is
  until change 5 is decided.
- **Code.** None.

### [A42] RQ3 asks about congestion-aware storage only (Design change, thesis text edited 2026-10-19, uncommitted)

- **Where.** `2.Introduction.tex`, the factor list (item 3 removed), the
  sentence after it and the one after that, RQ3, the main-result paragraph,
  the sentence on `d_obs` after `eq:localsubgraph`, the paragraph before
  `eq:congestion` and the one closing that subsection, and the second factor
  after `eq:rqformal`. `5.Experiments.tex`, "Factors", `tab:expfactors` (row
  removed), "Mapping questions to comparisons", the RQ3 results paragraph,
  `fig:exp:rq3` and "The price of avoiding congestion". Tagged `% [A42]`.
- **What the edit says.** RQ3 asks whether congestion-aware storage reduces
  crowding and blocked time beyond demand-only storage, and whether the
  travel it adds costs more service time than it saves. Congestion
  sensitivity is no longer a factor of its own. It is a level of the storage
  rule. Every controller still receives the crowding signal, and its weight
  `n_cng` in the reward is the same for every controller and not varied
  between runs.
- **Why.** Varying the routing half would mean training every arm twice, and
  it is a question about the controller, not about the coupling. The
  storage half needs evaluation only (`research_goals_2026-10-18.md`, change
  5, agreed 2026-10-19).
- **Open.** The value of `n_cng` is still TBD (`tab:rlparams`).
- **Code.** None. The routing toggle can stay in the code unused.

### [A43] Edge cost and step costs from van Knippenberg et al. (2021) (Design change, thesis text edited 2026-10-19, uncommitted)

- **Where.** `4.Implementation.tex`, `sec:impl:instances` (one sentence on edge
  cost), `eq:reward` (a move term), a new paragraph after the `[A30]`
  paragraph, and `tab:rlparams` (two rows). `2.Notation.tex`, the `c` header
  and a `c_move` row. Tagged `% [A43]`.
- **What the edit says.** Every edge of a generated instance costs 1, as on
  the benchmark maps of van Knippenberg et al. A move takes one timestep, so
  distance and time share a unit. The reward charges `c_move` = 0.1 for every
  move and `c_wait` = 0.2 for a standing-still step, the move and wait values
  of their Table 1. With the shaping term a step towards the target is worth
  about +0.9, a wait −0.2 and a step away −1.1, so moving on is best and
  yielding stays cheaper than a detour (`[A30]` still holds).
- **Why.** The author asked on 2026-10-19 that cost values come from an
  existing source rather than be chosen. Unit edges also make put-away
  (edge cost) and travel (timesteps) directly comparable, and make Token
  Passing's timestep minimisation the same as cost minimisation.
- **Not taken.** Their collision penalty (−2). The override penalty stays.
- **Code.** `random_edge_costs: false` in every config, `wait_cost: 0.2`, a
  `move_cost` argument and a sixth logged term in
  `environment/reward_function.py`. Not done yet. Needs retraining, which the
  long run does anyway.

### [A44] The main result is adaptive storage, and the loop is closed in RQ3 (Design change, thesis text edited 2026-10-19, uncommitted)

- **Where.** `2.Introduction.tex`, the opening paragraph of the project
  description, the main question, RQ1, RQ2, RQ3, the main-result paragraph,
  and a new paragraph with `eq:relgain` after `eq:rqformal`. `2.Notation.tex`,
  the travel row. `styles/eqnames.tex`, `eq:relgain`. `5.Experiments.tex`, the
  mapping paragraph. Tagged `% [A44]`.
- **What the edit says.** The demand-only rule reads only the order stream,
  so the main result is the gain of adaptive storage, not of a closed loop.
  The loop is closed only when storage also reads the traffic, which RQ3
  asks about. Between controllers the gain is compared as a share of route
  time (travel plus blocked under fixed storage), `eq:relgain`.
- **Why.** Under the arrival model the demand rule's placement and put-away
  were identical for every router, so no traffic reached storage. The arms
  that gained most in timesteps had the longest routes under fixed storage,
  and each arm saved about the same share
  (`arrival_short_2026-10-18.md`). Agreed 2026-10-19. This also settles
  change 2 of `research_goals_2026-10-18.md`.
- **Code.** The evaluation summary should report the relative gain. Small.

### [A45] Keep-up against released tasks, a backlog slope, and stalls (Design change, thesis text edited 2026-10-19, uncommitted)

- **Where.** `2.Introduction.tex`, the dependent variables, the "Keeping up"
  paragraph (`eq:throughput` rewritten) and `tab:measures`.
  `4.Implementation.tex`, `sec:impl:logging` and `tab:evalparams` (two rows).
  `2.Notation.tex`, the `f_up`, `chi` and `Lambda_T` rows. Tagged `% [A45]`.
- **What the edit says.** A run keeps up if it finishes at least `f_up` of
  the tasks released in that run and the least-squares slope `chi_T` of
  `B_t` over the second half is at most `chi_max`. A jam that the fleet
  recovers from passes, and is counted as a stall per controller. Throughput
  `Lambda_T` is the result for a run that does not keep up.
- **Why.** The old check compared throughput with the nominal rate. A
  decentralised run that jammed (336 of 378 orders, service time 273) passed
  it, and centralised and Token Passing runs at load 0.3 whose backlog grew
  all run also passed. Replaying nine episodes (2026-10-19, `thesis_plan.md`
  section 2.1) showed the two problems need two tools. Agreed 2026-10-19.
- **Open.** `chi_max` (from the Token Passing load sweep) and the stall
  length. `[A28]`'s stall item is now this one.
- **Code.** `evaluation/evaluator.py` reads `env.log.backlog_by_t` for the
  slope and the released count, and logs stalls. Not done yet.

### [A46] Orders with several lines and amounts (Design change, thesis text edited 2026-10-19, uncommitted)

- **Where.** `2.Introduction.tex`, the dependent variables, `sec:pf:tasks` (the
  task-generation rule, `eq:task` gains `q_j`, the stock condition, the pickup
  rule rewritten), `eq:estimates` (lines), the arrivals paragraph and
  `eq:arrivals` (units), a new "Order completion" paragraph with
  `eq:ordercompletion`, `tab:measures`, and two scope items.
  `4.Implementation.tex`, the demand model, the starting stock, `tab:evalparams`
  (two rows) and `sec:impl:logging`. `2.Notation.tex` and `styles/eqnames.tex`.
  Tagged `% [A46]`.
- **What the edit says.** An order is several order lines, each a SKU and a
  quantity (the problem formulation already allowed this). A line is served
  by trips, one per shelf it takes units from, nearest the delivery vertex
  first, the goods-to-person setting of Krnjaic et al. (2022). Every line of
  an order shares its release time and delivery vertex. Units no shelf holds
  wait for stock. `rho_hat` counts lines (placement), a new
  `rho_hat^unit` counts units (arrivals), and waiting lines add their units.
  Order completion time, the longest service time among an order's tasks, is
  reported. 5 lines per order on average (Krnjaic et al.), 1 to 5 units per
  line, uniform. `lambda_task` is order lines per timestep.
- **Why.** The author asked for it on 2026-10-19, before the long run. A line
  may take from several shelves, at the author's request, because a SKU can
  sit on several shelves under the arrival model.
- **Consequence.** A split line makes more tasks, so the number of tasks can
  differ between storage rules under the same seed. The order stream, and so
  the orders and lines, stay identical, and the gain test pairs per seed, not
  per task, so it still holds. A rule that splits stock pays for it in extra
  trips. The number of tasks per line is logged.
- **Open.** The distribution of lines per order (mean 5). The letter `q` is
  also the current target `q_i(t)`, a clash that predates this change.
- **Code.** Order generator, task model (quantity, order and line id), pickup
  rule, arrivals in units, waiting lines, the starting stock, and the metrics
  (order completion, tasks per line). Gated step G1 of
  `code_changes_plan_2026-10-19.md`, to be written out.

### [A47] Robots carry the put-away (Design change, thesis text draft 2026-10-19)

- **Where.** `2.Introduction.tex`, `sec:introduction` (coupling paragraph),
  `sec:pd-aim-and-scope` (aim and scope, dependent variables, main question,
  RQ1, main-result paragraph). `sec:pf:storage` (receiving vertices,
  `eq:storageupdate` and paragraph after tea example, fixed storage, access
  cost description, fig:dkr sentence, last sentence). `sec:pf:tasks`
  (task definition, stock condition and pickup rule). `sec:pf:measures`
  (opening, keeping up paragraph, service time paragraph with `eq:totalservice`,
  where the time goes, reported measures and `eq:putaway`, `tab:measures`,
  decision problem, gain, relative gain). `sec:pf:scope` (abstract put-away
  item, closing paragraph). `4.Implementation.tex`, `sec:method:storage`
  (storage rules and `eq:tripdistance`, instances receiving vertices).
  `sec:impl:logging` (per-task record). `2.Notation.tex` (notation table
  additions). `styles/eqnames.tex` (equation names for new equations).
  Figures `fig:storageexample`, `fig:dkr`, `fig:taskroute` need redrawing
  to show receiving side and put-away leg.
- **What the edit says.** Arriving stock is no longer placed on its shelf
  instantly and free. Instead, every placement is a put-away task, from a
  receiving vertex on one side of the warehouse to the shelf, served like a
  pick. Receiving vertices are a distinct role; storage, delivery and
  parking vertices stay random. Shelf space is reserved when the put-away is
  created, but units count as on the shelf only once the put-away is
  delivered, using a new variable `x^in_t` for units in transit. The
  storage rules judge a shelf by the whole trip of a unit (receiving to
  shelf to delivery), with no new weight. The result becomes total service
  time over all tasks (including tasks still open at the horizon), reported
  as `zeta^tot_T`, because the two storage rules make different put-aways
  and a mean over different tasks is not a paired comparison. Mean pick
  service time is reported alongside it. Stock arrives every Δ = 100 steps
  in bursts, and one queue serves both picks and put-aways, oldest first.
- **Why.** The change answers an open question: what does adaptive storage
  cost in robot time (the same unit as the result)? It gives RQ3 a
  mechanism, since storage now creates traffic directly. It also removes the
  "abstract put-away" limitation. Revises [A40] (put-away distance is no
  longer reported as a cost) and [A44] (the result measure changes from mean
  to total service time). The design decisions 1 and 2 that the draft
  identifies (stock only counts on shelf once delivered, and total service
  time counts unfinished work) were agreed 2026-10-19.
- **Open.** Two design choices that were not discussed in detail, marked in
  the draft. Confirm them before applying.
  1. Stock counts on the shelf only once it is delivered. The capacity
     constraint counts both `x_t` and `x^in_t`, so room is reserved.
  2. Total service time counts unfinished work up to the horizon. A task
     still open at T adds the time spent so far. When no line waits for
     stock this is the area under the backlog.
- **Arrivals count stock on its way (2026-10-19).** `eq:arrivals` subtracts
  `x_t^- + x^{in,-}_t`, not the shelf stock alone. Without it, units whose
  put-away is still open at the next epoch are ordered again, and so are the
  units lines wait for while those units are on their way, so an overloaded
  run fills its shelves with reserved room. Counting them also keeps the
  arrivals the same under every rule, since shelf stock plus stock on its way,
  less the units lines wait for, is arrived minus ordered. Under instant
  put-away nothing is on its way, so the template and instant runs are
  unchanged.
- **Code.** About four PRs before the Token Passing load sweep and retrain.
  Storage rules, task creation and completion, shelf capacity tracking,
  metrics (total service time, mean pick service time), and the arrival
  model (Δ = 100, one queue). Not yet started.

---

### [A48] The storage rule is a dynamic SLAP, solved with rules (Design change, thesis text edited 2026-10-20, uncommitted)

- **Where.** `3.Background.tex`, `sec:bg:storage` and the opening of
  `sec:rw:storage`. `6.Conclusion.tex`, `sec:future`.
- **What the edit says.** The Background defines DSLAP as deciding where
  goods are stored as they arrive (Waubert de Puiseau et al. 2022) and says
  the storage rule solves it for arriving stock, with fixed rules rather than
  a learned policy. The description of the three storage papers is left to
  Related Work only, so they are no longer introduced twice. The sentence
  that the rule "updates storage dynamically as demand shifts" is gone,
  since stock on a shelf never moves after [A38]. Future work gains a
  paragraph on a learned storage policy trained in turns with one router,
  and the Transformer subsection of Related Work becomes two sentences there.
- **Why.** The old wording described relocation, which the arrival model
  replaced. Saying the rules are fixed answers the obvious question of why
  the storage side does not learn, and the idea itself is kept in
  `decisions/ideas/learned_storage_policy.md`. Removing the doubled papers
  and the Transformer subsection also saves about a page.

### [A49] Keep-up is throughput against the release rate (Design change, thesis text edited 2026-10-20, uncommitted)

- **Where.** `sec:pf:measures` (`eq:throughput`), `sec:pd-aim-and-scope`, `tab:measures`,
  `tab:evalparams` (Appendix H), the notation table.
- **What the edit says.** A run keeps up when its throughput is at least
  `f_up` times the rate tasks were actually released, `Lambda_T >= f_up (|C_T| + B_T) / T`.
  The backlog slope `chi_T` and its threshold `chi_max` are gone. The stall count stays.
- **Why.** The author asked for fewer new concepts. Throughput against arrivals
  is the lifelong MAPD measure (Li et al. 2021) and the stability condition of a
  queue, so it needs a citation, not an argument, and drops a TBD threshold.
- **Revises.** [A45] (the two-part check).

### [A50] The result is the mean service time of picks (Design change, thesis text edited 2026-10-20, uncommitted)

- **Where.** `sec:introduction`, `sec:pd-aim-and-scope`, `sec:pd-rq`, `sec:pf:measures`
  (`eq:meanservice`, `eq:split`), Appendix F, `5.Experiments.tex`, `tab:measures`.
- **What the edit says.** The result is Ma et al.'s mean service time, over the
  completed picks. Put-aways count in the keep-up check and their mean service
  time is reported next to the result. Total service time (`eq:totalservice`)
  and the put-away distance (`eq:putaway`, `nu_T`) are removed.
- **Why.** The measure of the literature, used unchanged, is easier to compare
  and to validate. The risk [A47] named, that a rule could gain by leaving
  work unfinished, is covered by the keep-up check, which a run must pass
  before it is compared.
- **Open.** A line split over two shelves gives two picks, so the number of
  picks can differ between rules on one seed. Worth one sentence in the
  threats to validity once the results are in.
- **Revises.** [A47] (total service time as the result) and [A40] (put-away distance).

### [A51] The gain between controllers is a percentage of fixed-storage service time (Design change, thesis text edited 2026-10-20, uncommitted)

- **Where.** `sec:pd-rq` (RQ2 and the main result), `eq:relgain`, `5.Experiments.tex`.
- **What the edit says.** RQ2 compares `100 * gain_n / zeta_bar(F_fix, pi)` between
  controllers instead of the gain as a share of route time.
- **Why.** Storage studies report gains as a percentage over the baseline
  (Waubert de Puiseau et al. 2022), so the number reads the same way as theirs.
- **Revises.** [A44] (share of route time).

### [A52] Borrowed concepts and fewer equations (Clarity, thesis text edited 2026-10-20, uncommitted)

- **What the edit says.** Concepts the thesis defined itself are named and
  cited as the known versions. The move, vertex and swap rules are the MAPF
  definitions of Stern et al. (2019). The arrivals are an order-up-to policy
  (Axsater 2015). The demand rule and the starting stock are class-based
  storage by the cube-per-order index (Heskett 1963, de Koster et al. 2007).
  The claim mask is a one-step reservation table of prioritised planning
  (Silver 2005). Choosing in turn is a sequential policy (Wen et al. 2022,
  Fu et al. 2022). The distance label is van Knippenberg's distance feature,
  and its bound moves to Appendix K. The split is the queue split between
  waiting and being served. 25 definitions move to Appendix M, "Definitions
  in full", each kept in words in the main text, and 4 small displays become
  inline. The move, vertex and swap rules follow, written in words with
  `fig:conflicts`. The main text goes from 51 displayed equations to 20.
- **Why.** The author found the maths heavier than in comparable papers, and
  a system with fewer new ideas is easier to validate. What stays new is the
  coupling of storage to live traffic and the comparison of controllers by how
  many agents one decision covers.
- **Check.** The seven new references in `references.bib` were added from
  memory and must be checked against the sources before submission.

### [A53] Conflict resolution also protects the vertex of an agent still to be processed (Correctness, thesis text edited 2026-10-20, uncommitted)

- **Where.** `sec:method:resolution`, step 2 and the feasibility argument.
- **What the edit says.** A proposed move is also refused when it enters the
  current vertex of an agent not yet processed, the claim mask rule applied
  after the fact. The feasibility argument is replaced by the short
  induction, with the two-agent counterexample. The rule is cautious, so
  some safe follow moves become waits.
- **Why.** An external review (2026-10-20) showed the old argument fails: a
  higher-priority agent accepted onto the vertex of a lower one that then
  waits gives a vertex conflict. The code already had the fix since issue #7
  (`resolution/conflict_resolution.py`, `move_blocked`), and
  `test_swap_conflict_forces_both_agents_to_wait` covers the case. Only the
  text lagged.
- **Code.** No change.

### [A54] Pick units are reserved at release and leave the shelf at pickup (Design change, thesis text edited 2026-10-20, uncommitted)

- **Where.** `sec:pf:tasks` (`eq:coupling`, the pickup rule paragraph), `eq:pickuprule`
  (Appendix M), `eq:arrivals` (Appendix G), the arrivals paragraph, the notation table.
- **What the edit says.** New quantity `r_t(k,v)`, the units promised to picks not yet
  picked up. The stock condition is checked at release against `x_t - r_t`. The units
  stay in `x_t` and take up room until pickup. The pickup rule and the arrivals read
  `x_t - r_t`.
- **Why.** The external review (2026-10-20) found the text inconsistent. Stock fell at
  release but the stock condition was stated at the step the units are taken. The code
  also freed shelf room at release, so a put-away could be sent into room still holding
  units. Option (b) of the review chosen by the author, since capacity is one of the
  four correctness checks.
- **Code.** `feat/stock-reservation` (worktree `~/worktrees/feat-stock-reservation`),
  stacked on #190, commits `13e858e` and `98d70a1`. Changes `_release_orders`,
  `_arrive` and `_advance_task_lifecycle`. The age of a picked unit is now measured at
  pickup. Results can change only through room on shelves, because the pickup rule and
  the arrival amounts read the same numbers as before.
- **Open.** `r_t` belongs in the state tuple (review point on the state, step 3).

### [A55] Claims narrowed after the external review (Clarity, thesis text edited 2026-10-20, uncommitted)

- **What the edit says.**
  - Paired seeds give the same customer orders, not the same tasks. Where a line
    is picked and how it splits depend on storage, and that is part of the gain.
  - The first part of the service-time split is "the wait before assignment",
    since it also holds the wait for stock (`eq:split`, `5.Experiments.tex`).
  - `W_T` (`eq:waiting`) averages over completed picks, like `eq:meanservice`.
  - Edge cost is distance, not travel time. Every edge takes one step, and
    every instance has unit costs (all 28 configs, `default_edge_cost: 1.0`).
  - The controllers are compared as configurations. They differ in what a
    decision sees, knowledge of earlier moves and reward credit, not only in
    how many agents one decision covers.
  - Pham et al. (2024) does not isolate communication. The sentence now says
    what their experiment shows.
    **Revised by [A101] (2026-11-18).** This was wrong. Their ablation (Table II)
    switches messages off. See [A101].
  - Appendix K. The distance-label bound limits how much one step shortens
    `eta_i`, not how much it lengthens it. The "worst case is bounded" claim
    is removed.
  - The keep-up check is a finite-horizon check, so the backlog over the run is
    shown for the main-result conditions.
  - The trip distance's delivery leg (`eq:tripdistance`) is named a stand-in,
    since delivery vertices are drawn at random.
  - `fig:loop` redrawn (`thesis-progress/scripts/images/loop.tex`). Arrivals,
    put-aways, reservations and the five-part task. Fixed storage sends
    arrivals home rather than holding `x_t` fixed.
- **Why.** External review, 2026-10-20.
- **Code.** None. The backlog per step is already logged (`log.backlog_by_t`).

### [A56] The two training regimes answer different questions, and order throughput is reported (Design change, thesis text edited 2026-10-20, uncommitted)

- **Where.** `sec:method:training`, the training paragraph of `5.Experiments.tex`,
  the order completion paragraph of `sec:pf:measures`.
- **What the edit says.** Training on `F_fix` only is the main result, because one
  frozen policy meets every storage rule, so the gain is the storage rule's.
  Matched training compares whole systems, and part of its gain can come from
  training. Training and evaluation seeds are counted apart. Orders completed
  per timestep are reported next to task throughput.
- **Why.** External review, 2026-10-20. Split lines and put-aways change the task
  count without changing the customers served.
- **Open.** Closed by [A114] (2026-11-23): the author chose matched training only, F_fix-only training is dropped.
  The seed counts are still the open mockup.
- **Code.** None. `num_completed_orders` is already in `RunMetrics`.

### [A57] Warehouse size and role counts follow the fleet, and the generator checks only well-formedness (Design change, thesis text edited 2026-10-21, uncommitted)

- **Where.** `sec:impl:instances`, `app:wellformed` (the endpoint set),
  `app:instances` (the four warehouses and the generator check).
- **What the edit says.** |V| = 16 m, so 128, 256, 512 and 1024 vertices for
  8, 16, 32 and 64 agents. |V_ep| = m, |V_str| = m/2, |V_del| = |V_rcv| =
  m/2, two agents per dock at every size. Every edge is two-way in the experiments, and one-way edges stay
  a feature of the model. The receiving vertices are endpoints of the
  well-formedness check, as the code already had it. The sentence crediting
  random role placement to Ma et al. is dropped, because they draw tasks at
  random from fixed endpoints.
- **Why.** The graph size was drawn at random per seed (86 to 131 vertices at
  m = 8) and the role counts had been tuned until generation passed (64 agents
  had fewer shelves than 32). The 16 m sizes match van Knippenberg et al.
  (2021), Tables 4 and 5. m/2 shelves make agents share shelves (author,
  2026-10-21). The generator's extra condition, that the plain vertices stay
  strongly connected, rejected well-formed placements. The fleet warehouses drop it
  (`role_backbone: false`), and older configs keep it, so they give the same instances.
  The fleet size alone sets the warehouse (`fleet_defaults`). A config with an `instance`
  section builds that warehouse as written.
- **Open.** The reason given for two-way edges is a proposal, for the author to
  confirm. vertex_capacity of the 8-agent configs is raised from 200 to 300,
  since 4 shelves hold up to 240 units at the start.
- **Code.** Worktree `~/worktrees/fix-warehouse-scaling` (branch
  `fix/warehouse-scaling`, uncommitted). `generator.py` (`fleet_defaults`,
  `role_backbone`), `spec.py` (`instance_params`), the `validation.py` docstrings,
  `configs/fleet_*` (no instance section), and
  `scripts/instance_report.py`. Earlier fleet runs do not reproduce. Every other
  config is unchanged.
- **Appendix.** Handoff for writing `app:instances`:
  `decisions/done/graph_appendix_handoff.md`.

## Still open

- [ ] **Gap: an order's workstation is random, so the storage rules have no
      target.** Decided 2026-10-29, option (a), D29 in `model_revision/README.md`.
      Code and thesis text still to do. Found 2026-10-29 in the step 12 sweep, raised by the author.
      Since `[A70]` the delivery vertices are random rack faces, and every
      order still draws one at random, while the second leg of
      `eq:tripdistance` (Appendix C, line 637) is the distance to the
      nearest delivery vertex. `4.Implementation.tex`, line 65 (`[A55]`),
      justifies that leg as ranking a shelf by how close it sits to "the
      delivery side", which no longer exists. On 5 step 12 warehouses per
      fleet the rule's best fifth of shelves is about 3 steps from its
      nearest delivery vertex but 11, 16, 24 and 34 steps from the one an
      order uses (an average shelf 12.5, 17, 25 and 35). `[A70]` took the
      mean over the docks for the same reason. Proposed, not agreed: each
      delivery vertex keeps needing the same SKUs, fixed or changing
      slowly. The options and the open points are in
      `model_revision/README.md`, "Still open". It changes the demand model
      and the second leg of the trip, so it gets its own `[Axx]` entry once
      agreed, and it comes before the SKU count and Q (D25).
- [x] **Code for [A75] and [A76].** Done 2026-10-31 with `[A77]`, slap-mapd-coupling `18fefda`.
- [ ] **Token Passing checks the values, it does not settle them for the other systems** (author,
      2026-11-02). The updated Token Passing run (2026-10-31, `results/E_load`, `F_demand`,
      `G_storage`, `app:load:runs` in Appendix E) found two things that hold for Token Passing only.
      Look at both again under the learned arms (centralised, section-based, decentralised) once
      they are trained.
      - *Congestion weight.* Weights 0 to 4 change the pick service time by at most 2 %, because
        Token Passing's waiting happens before a robot takes the task, on no edge the weight sees.
        The learned arms may block each other more, so the storage half of RQ3 is read there.
      - *Stock waits.* 0.1 to 0.3 % of lines wait for stock, against an aim of about 1 %. A slower
        arm finishes put-aways later, so stock reaches the shelf later and more lines may wait.
        Report the share per arm. The safety stock stays as it is until then.
      - *Main load.* The main load is 0.6 of Token Passing's capacity, and every arm and both
        storage rules run at it, so the comparison stays paired. Kept as it is (author,
        2026-11-02). An arm that beats Token Passing runs further below its own limit, so its waits
        are shorter and its gain may look a little smaller. Say this in one sentence in the threats
        to validity when the results are written. RQ4, which varies the load, shows the rest.
- [x] **Text and code for the step 12 sizing.** Replaced by `[A77]` (2026-10-31): the SKU count is
      2.5 per agent, not 250 x main load, and Q = 10. Text done as [A75] (2026-10-30). Decided 2026-10-29 ("D25,
      sized" and "D25, safety stock" in `model_revision/README.md`): Q = 12
      at every fleet, n = 250 x main load rounded to a multiple of 20, 5
      lines per order, and every SKU's safety stock sized at rank 0. The
      starting stock text (`4.Implementation.tex`, the refill rule and
      `tab:evalparams`) and `refill_starting_stock` still say the SKU's
      rank at t = 0. One `[Axx]` entry when the text is written.
- [ ] **Code for [A49] to [A51].** Four drift points posted to #103 on
      2026-10-20 (group "measures"): the two-part keep-up check, the mean
      service time over all tasks instead of picks, the put-away distance
      still computed, and the relative gain over route time. One fix PR from
      `main` (https://github.com/BjarkeKarlsen/slap-mapd-coupling/issues/103#issuecomment-6291490025).
- [ ] **Open point of [A50].** A line split over two shelves gives two picks,
      so the number of picks can differ between rules on one seed. Decide
      whether that needs handling, or one sentence in the threats to validity.
- [ ] **References for [A52].** Check the eight entries added from memory
      (Li 2021, Silver 2005, Wen 2022, Fu 2022, Heskett 1963, de Koster 2007,
      Axsater 2015, Stern 2019) against the sources.

- [ ] **Values for [A38].** epsilon (probe value 1), x_min (8 in the
      configs), Delta (100), the receiving vertices, and beta under the
      arrival model (1 in `configs/medium_arrival`).

- [ ] **Validator for [A28].** `check_well_formedness` in
      `slap-mapd-coupling` counts non-task endpoints against $m$, as the
      text now says. Today it counts all endpoints, and an instance with
      fewer than $m$ vertices in $V_{\mathrm{ep}}$ passes it and then
      fails when the environment places the agents.
- [ ] **Stall rate for [A28].** After a realistic training run, also take
      the longest whole-fleet still run over the healthy episodes, which
      sets N for the training truncation. Then count the
      evaluation episodes in which an agent holding a task stops moving for
      a quarter of the episode, per arm. Then pick between the instance rule
      and the assignment rule. The real centralised and section-based arms
      are built ([A32]), so measure all three arms after the first retrain.
- [ ] **Code for [A28].** Episode trace, training progress metrics and the
      Token Passing baseline in `slap-mapd-coupling`. Specs B15 to B20 in
      `fix_prs_plan.md`.
- [ ] `3.Background.tex`, "Congestion and emergence", still frames the
      commons for the system as a whole. [A32] dropped the commons
      question, and the author reinstated it later on 2026-10-16 (proposed
      RQ6 in `thesis-progress/archive/workspace/ROADMAP.md` at the workspace root, not yet in the thesis).
      Align this paragraph with the RQ once its wording is approved.
      The question is now part of RQ4 ([A33], 2026-10-19), so this paragraph
      can be aligned.
- [ ] Write the sentence in `sec:pf:controllers` that says how the zones of
      the zone partition are drawn (blocks of consecutive aisles, [A29]), and
      decide the number of zones `p`. Higher priority since [A32], because
      the section-based arm only differs from the centralised arm when
      `p > 1`.
- [ ] **Code for [A17].** Per-edge policy head in `slap-mapd-coupling`,
      with the message of the agent on each neighbour vertex as an input.
- [ ] **Code for [A15].** Sort each vertex's outgoing neighbours by vertex
      number in `slap-mapd-coupling` (`graph.py` `legal_actions`), so
      `move_k` means the same as in the thesis.
- [ ] **Code for [A14].** `slap-mapd-coupling` message builder and the
      decentralised forward pass (all agents of a timestep together) must
      follow `eq:message`.
- [ ] **Code for [A20].** `slap-mapd-coupling` `evaluation/metrics.py` and
      `evaluator.py` still compute entropy, concentration and movement
      cost. They should compute the keep-up check, the three parts of
      service time, crowding and relocations per update, and the paired
      per-seed gain of `eq:rqformal`.
- [ ] **Values for [A20].** `f_up` (0.8), the evaluation horizon (630) and
      the load levels are set, see [A31]. The number of evaluation seeds in
      `tab:evalparams` is still TBD.
- [ ] **Code for [A30] and [A31].** The `c_wait` reward term (0.1) and
      `keep_up_threshold` = 0.8 in `slap-mapd-coupling`, then retrain. Code
      done on `main` (`reward_function.py`, `wait_cost: 0.1` and
      `keep_up_threshold: 0.8` in every `configs/*.yaml`), checked
      2026-10-16. The retrain is still to do.
- [ ] Confirm the delivery date (about 12 January 2027) and that the new
      arms match the thesis contract wording.
- [ ] **Code for [A22].** `slap-mapd-coupling` `communication_neighbours`
      takes `communication_radius`; the thesis uses `d_obs` for it.
- [ ] **Citation for [A23].** A source for the POSG definition.
- [ ] **Code for [A21].** `slap-mapd-coupling` bounds the field of view and
      communication with the cost distance `graph.distance`. It should use
      a hop distance (breadth-first search) for those, as `eq:localsubgraph`,
      `eq:commgraph` and `eq:halo` now say.
- [ ] **Gap: pickup vertex in proportion to units.** The pickup vertex is
      drawn uniformly among the vertices holding the SKU
      (`4.Implementation.tex:732`, `multi_agent_env.py:520`), so a leftover
      unit at an old vertex keeps half of the SKU's orders there. That matters
      because ν binds at every update. Proposal: draw in proportion to
      `x_t(k,v)`, mapping the same `u_pickup` through cumulative units so the
      order stream stays paired. Also name the pickup choice next to
      `eq:coupling` as where storage enters routing. Changes every
      adaptive-storage result, so it is to be decided before the long run.
      Issue drafted, not yet opened.
- [ ] **Gap: a storage update keeps each SKU's units.** The set of storage
      rules (`2.Introduction.tex:504-511`) allows a rule that drops a SKU, which
      could then never be ordered again. The code keeps totals only when the
      cap binds (`storage/relocation.py:28-30, 71`), and the greedy target can
      leave units unplaced (`storage/demand.py:17`). This never happens on the
      8-agent instance (928 of 2000 capacity). Proposal: say so in the thesis,
      and check totals after every update in the code. Issue drafted, not yet
      opened.
- [ ] **Check: the instant switch.** Optional. Evaluate the adaptive rules
      with every update applied one epoch late, with no retraining, to see
      how much of the gain the instant switch carries.

### [A58] The main load comes from fixed storage, and capacity is the highest rate that keeps up (Design change, thesis text edited 2026-10-21, uncommitted)

- **Where.** `app:load:method` (Appendix D).
- **What the edit says.** The Token Passing load sweep runs fixed storage only. The
  capacity of a warehouse is the highest arrival rate at which fixed storage, and every
  lower rate, keeps up on every seed (`eq:throughput`). The main load is 0.6 of it, and
  every storage rule and controller of that fleet runs at this one rate. Each fleet size is
  swept on its own warehouse, on a grid of 0.0125 m to 0.1 m in eight steps, refined
  between the last passing and the first failing rate.
- **Why.** The gain test pairs fixed and adaptive storage on one order stream, so they need
  one rate. Fixed storage is the baseline, and the other systems' results are read from
  their own runs. The earlier reading, the highest mean throughput over the rates, kept
  rising past the point the fleet fell behind, because throughput counts put-aways, which
  grow with the rate. It also drops `chi_max`, which `[A49]` removed.
- **Revises.** The capacity reading of `thesis_plan.md` section 4.3 ("the most tasks per
  timestep Token Passing sustains").
- **Code.** Worktree `~/worktrees/fix-measures` (branch `fix/measures-a49-a51`,
  uncommitted), `scripts/load_sweep.py`, `scripts/run_fleet_sweeps.sh`,
  `scripts/extract_sweep_parameters.py`. The sweeps in `slap-mapd-coupling/DIR/` predate
  the graph fix of `[A57]` and are run again.

### [A59] The keep-up check is applied to picks and put-aways separately (Design change, thesis text edited 2026-10-23, uncommitted)

- **Where.** `sec:pf:measures` (`eq:throughput`), the notation table (`f_up`, and a new row for
  `C^put_T`, `B^pick_T`, `B^put_T`).
- **What the edit says.** A run keeps up only if its picks and its put-aways each pass the check,
  each against its own release rate, with the same `f_up`. The orders still waiting for stock
  count in the pick backlog. Throughput as the result of a run that does not keep up stays the
  total over both kinds.
- **Why.** The Token Passing parameter sweep of 2026-10-22 showed that the combined check misses
  put-aways falling behind. At 32 agents demand storage passed on 20 of 20 seeds while it
  finished 301 of 450 put-aways (67 %), because the picks carried the combined share above 0.8.
  A rule that leaves put-aways waiting can shorten the picks and still pass. See
  `notes/parameter_sweep_2026-10-23.md` and `notes/measures_catalogue.md`.
- **Revises.** [A50], whose "Why" said the keep-up check covers a rule that gains by leaving work
  unfinished. With one combined check it did not. [A47] (put-aways count as tasks in the check).
- **Code.** `evaluation/metrics.py` (`keeps_up`, and the per-kind backlog), the load sweep's
  capacity reading. Planned in `active/measures_plan.md`. The capacities and main loads of
  `[A58]` are read again with the new check.

### [A60] A checkpoint is chosen on validation seeds by pick service time among those that keep up (Design change, thesis text edited 2026-10-23, uncommitted)

- **Where.** `app:cal:checkpoint` (Appendix G), which was a TODO.
- **What the edit says.** Every saved checkpoint plays the validation seeds. Among those that pass
  the keep-up check on every validation seed, the one with the shortest mean pick service time is
  evaluated on the test seeds. If none passes, the one with the highest throughput is taken and
  the arm is reported by its throughput. The training return is not used.
- **Why.** It is the rule of `eq:decisionproblem` applied to checkpoints, so checkpoint choice and
  the result use one measure. The training return is dominated by the shaping term and does not
  track service time (`thesis_plan.md` section 5).
- **Open.** The number of validation seeds and the checkpoint frequency. The configs have 2 seeds
  and every 3 iterations.
- **Code.** `choose_checkpoint` in `training/evaluate_run.py`, branch `feat/evaluate-horizon`
  (2026-11-02). It replaced the most completed tasks, which follows how many orders arrived. The
  configs' `score_attribute: episode_return_mean` only names Tune's best checkpoint, which
  `evaluate` does not use.

### [A61] The horizon is 2000 or more, and the load sweep states its seeds and covers the largest fleet (Design change, thesis text edited 2026-10-23, uncommitted)

- **Where.** `tab:evalparams` (Appendix B, `T`), the TODO of `app:cal:horizon` (Appendix H),
  `app:load:method` (Appendix D).
- **What the edit says.** `T` is 2000 or more, still open for the calibration of
  `app:cal:horizon`, which may raise it but not lower it. The load sweep runs 20 seeds per
  rate, as many as the compute allowed, to show how much the numbers vary between order
  streams on each generated warehouse, and it gives an overview of the settings that work per
  fleet, not a tuned optimum. Where the lowest grid rate already fails, rates below it are
  added the same way as between the last passing and the first failing rate.
- **Why.** The author set the floor of the horizon: long enough for the demand estimate to
  settle, for several demand drifts (period 200) and storage periods (Δ = 100), and for a
  learned storage rule to make enough choices (about 200 per episode at 8 agents). 630 was a
  value from the three-agent pilot of `[A31]`, and every config already uses 2000. The author
  does not argue for the number of seeds, only states it and what it is for. At 64 agents the
  lowest grid rate (0.8) failed on the rerun of 2026-10-23, so "one grid covers every fleet"
  no longer held.
- **Revises.** `[A31]` (`T` = 630), `[A58]` (the grid).

### [A62] Graph v2, every endpoint a leaf off the aisles, a one-way loop and a U-shaped flow (Design change, thesis text edited 2026-10-26, uncommitted)

- **Where.** `sec:impl:instances` (Chapter 4), `app:instances` (Appendix D: summary, setting,
  `app:instances:method`, results, `tab:instances`, conclusion and `app:cal:roles`).
- **What the edit says.** Every storage, delivery, receiving and parking vertex is a leaf with
  one edge to the aisle beside it, so every warehouse is well-formed by construction and none
  is discarded. Aisles run from a front lane to a back lane, and two one-way rows in opposite
  directions cross the rack area and form a loop with no leaf on it. Every other edge is
  two-way. Some aisles stop short of the back lane, and one link per pair of neighbouring
  aisles in each block joins them at a row drawn from the seed. Delivery vertices on the
  front wall, receiving vertices from one front corner, parking from the opposite back corner,
  a U-shaped flow. 16 m walkable vertices with the leaves on top. The shelf count follows from
  the rack faces (58, 230, 575 and 1356), and a shelf may hold several SKUs.
- **Why.** The queue of 2026-10-23 showed that storage could hardly change trip length, and
  that a robot serving a shelf blocked the aisle (`notes/queue_findings_2026-10-26.md`,
  sections 2 and 3). Model revision decisions D1 to D6
  (`active/model_revision/README.md`, `02_graph.md`). Van Knippenberg et al. (2021),
  Section 4 and Figure 4, checked in the paper: start and goal nodes have one or two
  neighbours, and the two uni-directional central lanes carry none except at their ends.
- **Result.** Test A (`results/tests/A_graph_v2/`): 50 of 50 seeds well-formed at every fleet,
  each from the first layout. Trip distance 6 to 37 at 8 agents, 5 to 131 at 64. At 8 agents
  and load 0.12, demand storage beats fixed by 14 % on pick service time, random beats fixed
  by 18 %, and demand is 4.5 % behind random. Travel per pick drops by under one step.
- **Open.** A source for the U-shaped flow (Bartholdi and Hackman, to check, TODO in both
  places). Closed for the chapter by `[A70]`, which ends the U-shaped flow (Appendix D still says U). `warehouses.png` still shows the old layout (step 09). The text mentions no earlier
  layout (author, 2026-10-26). The thesis is not committed.
- **Code.** PR #193 (`feat/graph-v2`), with the random put-away rule of test A in PR #194.
- **Revises.** `[A57]` (roles drawn at random on the aisles, m/2 storage vertices, every edge
  two-way, layouts discarded until well-formed).

### [A68] Shipping to a dock, and the order service time as the result (Design change, thesis text edited 2026-10-27)

- **Where.** `sec:pf:tasks` (order lines, the three task kinds, the task definition, the stock
  condition), the roles paragraph of `sec:pf:env`, the scope list (D13's item "Nothing after the
  delivery vertex" replaced by "No packing"), `sec:pf:measures` (the result, the service time
  paragraph with `eq:ordercompletion` and `eq:meanservice`, the split, the keep-up check,
  `tab:measures`), `app:measures` (Appendix C, the old order completion paragraph removed) and the
  notation table.
- **What the edit says.** The delivery vertex holds an order's units until its last line is
  there, then a shipment carries the whole order to a receiving vertex, where it leaves. A
  shipment is a third kind of task, released when the order's last pick is delivered, served
  like a pick or a put-away. The receiving vertex of every shipment and put-away is drawn at
  random. The result $\bar\zeta_T$ keeps its symbol and its place in `eq:rqformal`, and is now the
  mean order service time, from an order's release until it leaves at a dock. The per-task
  service time stays, to explain the result and for the reproduction of Ma et al. Shipments count
  with the picks in the keep-up check.
- **Why.** The order is what the customer waits for, and the trip out loads the docks that inbound
  stock also uses, so leaving it out (D13) hid crowding the storage rule causes. Model revision
  D21 (`active/model_revision/12_flow_and_start.md`), and choice 1 of `12_thesis_drafts.md`,
  agreed by the author 2026-10-27. A random dock because which dock a truck uses does not depend on
  where the stock goes.
- **Rejected.** Keep the mean service time of picks as the result, which leaves the docks out of it.
- **Code.** Branch `feat/flow-and-start` (`e0090d0`): `shipping` and `dock_choice` in the arrival
  settings, ship tasks in `environment/multi_agent_env.py`, `order_metrics` ending at the dock.
  Still to change: the summary of `training/evaluate_run.py` leads with the gain in pick service
  time, it must lead with the order service time.
- **Revises.** D13 and `[A50]` (the mean service time of picks as the result), and `[A46]` (order
  completion as the longest service time among an order's tasks, reported only).

### [A69] One random start for every rule, class-based homes for fixed storage (Design change, thesis text edited 2026-10-27)

- **Where.** `sec:impl:instances` (the start paragraph), `sec:pf:storage` (the home shelf of
  $F_{\mathrm{fix}}$), `app:horizon:setting` (Appendix H, the warm-up).
- **What the edit says.** Every rule starts from the same $x_0$, each SKU alone on a shelf drawn at
  random for the seed with one refill plus its safety stock. Half the shelves start empty. The home
  shelves of $F_{\mathrm{fix}}$ are chosen once from the popularity at $t = 0$, the most popular SKUs
  nearest the delivery vertices, and are not the shelves of $x_0$. Training and evaluation start the
  same way, and evaluation measures after a warm-up (length TBD) in which the storage rule's refills
  replace the start.
- **Why.** The old start put the popular SKUs nearest the delivery vertices for every rule, so the
  start decided most of where stock was and the rules made few decisions of their own (watching a
  run, 2026-10-26). Model revision D22, and choice 2 of `12_thesis_drafts.md`, agreed 2026-10-27.
  Homes that followed a random start would make fixed storage random dedicated storage, a weak
  baseline for the main result.
- **Rejected.** An empty start (every slot placed by the rule, but the first thousands of steps are
  filling), and homes that follow the random start.
- **Code.** `initial_placement: random_slots` on `feat/flow-and-start`. Fixed storage's homes from the
  class-based placement: commit `b44db09` (`fixed_homes`). The step 12 sweep started 2026-10-27
  12:12 ran before that change, so its fixed storage had random homes.
- **Revises.** D19 (start fill 0.4, the SKU count derived from it) and `[A35]`/`[A38]` (the start
  as the class-based placement applied once, homes as the shelves of $x_0$).

### [A70] Delivery vertices on random rack faces, receiving vertices along the left wall, the put-away leg over every dock (Design change, thesis text edited 2026-10-27)

- **Where.** `sec:impl:instances` (the paragraph that was the U-shaped flow, its TODO removed),
  `sec:method:storage` (the trip distance in words, twice), `eq:tripdistance` (Appendix C).
- **What the edit says.** The delivery vertices take rack faces drawn at random for each seed. The
  receiving vertices are spread evenly along the whole left wall. Stock comes in and orders leave
  there, so work runs from the left wall to a shelf, to a delivery vertex and back. The first leg of
  $d^{\mathrm{trip}}(v)$ is the mean distance over the receiving vertices, since a refill's dock is
  drawn at random. At 8 agents $d^{\mathrm{trip}}$ runs from about 11 to 34 steps, the means over 50
  seeds of the smallest and largest (`results/D_warehouses/step12/summary.md`).
- **Why.** Fixed delivery vertices on the front wall made every run's traffic meet at the same
  vertices, and the docks in one corner sent every refill to the same dock (dock 132, watching a run on
  2026-10-26). With random docks, the nearest dock is not where a refill comes from, so the mean is the
  trip the rules should weigh. Model revision D24, the author's note on the docks (2026-10-27).
- **Rejected.** Random places along the front wall only, which keeps "near the front is good" true in
  every layout. The nearest dock in `eq:tripdistance`, which favours shelves near one dock that only
  some refills use.
- **Check.** Every seed at 8, 16, 32 and 64 agents is well-formed at the first layout drawn (instance
  report, 50 seeds per fleet).
- **Code.** `station_placement: rack_faces` and `dock_placement: left_wall` in graph v2 (`e0090d0`),
  `DrawnDocks` for the mean over the docks (`2817ca7`). The step 12 sweep started 2026-10-27 12:12 ran
  before `2817ca7`, so its rules weighed the nearest dock.
- **Revises.** `[A62]` (delivery vertices on the front wall, receiving vertices at one front corner, a
  U-shaped flow) and `[A47]` (the first leg from the nearest receiving vertex).

### [A71] Two shelves per SKU, the other rack faces parking (Design change, thesis text edited 2026-10-27)

- **Where.** `sec:impl:instances` (the shelves, and the counts of parking vertices and SKUs).
- **What the edit says.** After the delivery vertices are drawn, $2|\mathcal{K}|$ shelves are spread
  evenly over the rack faces left, and the remaining faces become parking vertices, so
  $|V_{\mathrm{ep}}| \ge m$. The number of SKUs per fleet is TBD, set so that a SKU of middle popularity
  is refilled about four times per demand cycle.
- **Why.** With a shelf on every rack face there were 58 shelves for 60 SKUs at 8 agents and about 30
  shelves near each delivery vertex, so every rule placed stock next to one and the rules hardly
  differed. Van Knippenberg et al. have no storage, so the count had no value of its own (Appendix D).
  Two per SKU is the fewest that leaves a second place while a refill is under way. Spread evenly rather
  than at random, so a seed does not cluster its shelves. Model revision D25.
- **Rejected.** A shelf on every rack face.
- **Provisional counts** (instance report, 50 seeds, `results/D_warehouses/step12/`): 40 shelves and 21
  parking vertices at 8 agents, 640 and 742 at 64, with 20 and 320 SKUs. Final counts after the sizing.
- **Code.** `num_storage_vertices` for graph v2 (`e0090d0`).
- **Revises.** `[A62]` (the shelves follow from the rack faces, 58 to 1356, $|V_{\mathrm{ep}}| = m$).

### [A72] An idle robot moves to an endpoint only when it is in the way (Design change, thesis text edited 2026-10-27)

- **Where.** The roles paragraph of `sec:pf:env`, `sec:pf:observations` (a paragraph after the
  distance label), `eq:currenttarget` (Appendix C, two more cases), `sec:method:rl` (the reward of an
  idle agent), the notation table ($q_i(t)$, new $y_i(t)$).
- **What the edit says.** A robot without a task keeps its own vertex as its target. When it stands on
  the pickup or delivery vertex of an unfinished task, or another robot was stopped from moving onto its
  vertex, its target becomes the nearest free endpoint $y_i(t)$ until it arrives or gets a task. The
  shaping term rewards it for getting closer, with no wait cost.
- **Why.** A learned robot with no task targeted its own vertex, so it stayed where its last task ended,
  often on a delivery or receiving vertex, and "an idle robot waits at an endpoint, where it blocks no
  one" held for Token Passing only (README "Still open", 2026-10-26). Token Passing's own rule covers
  only the delivery vertex of an unassigned task, because its task rule never hands out a task whose
  ends are taken. Model revision D26, refined by the author 2026-10-27.
- **Rejected.** Sending every idle robot to an endpoint at once, which adds trips and differs from Token
  Passing. Copying Token Passing's trigger word for word, which leaves a pickup blocked.
- **Code.** `idle_parking` in the experiment section (`e0090d0`), on in `configs/step12/`.

### [A73] A new warehouse every episode (Design change, thesis text edited 2026-10-27)

- **Where.** `sec:impl:instances` (the seed sentence), Appendix J (the seed split).
- **What the edit says.** Every episode plays the warehouse of its own seed. Training sees one warehouse
  per episode of the budget, 250 at 500 000 steps of 2000-step episodes, and the validation and test seeds
  play warehouses no run trained on. Every controller and storage rule plays the same warehouse on the same
  seed, so the comparison stays paired. Each training seed is its own warehouse, and the window tables of
  every warehouse are built before training.
- **Why.** The code fixed one warehouse per fleet (seed 42), while Appendix D's seed split read as one per
  seed. The generator exists to give a family of irregular warehouses, so the claim is about that family,
  and a test on unseen layouts shows whether the router learned to route rather than one map. One per
  episode is the most layouts a fixed budget shows. Model revision D27, agreed 2026-10-27.
- **Rejected.** One warehouse per fleet. A smaller pool seen several times, kept as the fallback if
  training does not settle.
- **Code.** `warehouse_per_seed`, `training/warehouses.py`, `StoredWindowLookup` (`e0090d0`),
  `prepare-warehouses` (later on the same branch).
- **Revises.** The fixed instance seed of `[A57]`/`[A62]`.

### [A74] Stacked rack blocks of four rows, irregular aisles in every block (Design change, thesis text edited 2026-10-27)

- **Where.** `sec:impl:instances` (the layout paragraph, the shapes per fleet). Appendix D still to follow.
- **What the edit says.** The rack area is blocks of four rack rows, a two-way cross lane between
  neighbouring blocks and the one-way loop at the centre. A larger warehouse gets more blocks and aisles,
  not deeper ones, so a shelf is within four steps of a lane at every fleet size. In each block the outer
  aisles run lane to lane and every inner aisle hangs from the lane on the side of the loop at a length
  drawn from the seed. 6 aisles and 2 blocks at 8 agents, 7 and 4 at 16, 10 and 6 at 32, 15 and 8 at 64.
- **Why.** The old growth deepened two blocks around one loop (4 rack rows at 8 agents, 24 at 64), so
  congestion grew with the fleet partly because of the layout, which muddies any comparison across fleet
  sizes. The lower block was full in every seed, so the bottom half looked the same everywhere (the author,
  watching the layout, 2026-10-27). Model revision D28.
- **Rejected.** Deeper blocks around one loop. More one-way pairs, which complicate routing for little
  gain. Shelves along the central pair, which would block the loop (D3).
- **Code.** `e1f6c2c` (irregular lower block), `9bc3bc4` (`num_blocks`, `v2_stacked_shape`). The old layouts
  build bit for bit as before (27 instances compared).
- **Revises.** `[A62]` (two blocks around one pair, the lower block full).

### [A75] The SKU count, the refill size and the safety stock (Design change, thesis text edited 2026-10-30)

- **Where.** `sec:impl:instances` (the SKU count, the drift as a share, the start stock),
  `tab:evalparams` (Appendix B), `tab:notation` (Q), Appendices E, F and G (the step 12 sweep).
- **What the edit says.** Q = 12 units at every fleet. The SKU count is 250 x the main load, rounded to a
  multiple of 20, so every SKU is refilled about four times per demand cycle and the 5 % drift is a whole
  number of SKUs (the ranking goes round in exactly 4000 steps). Every SKU starts with one refill plus the
  safety stock of the most popular rank.
- **Why.** The step 12 sweep (`results/G_storage/README.md`). The refills follow from the orders,
  12000 x load / (n Q) per cycle, matched by the sweep within 0.2. One Q keeps put-aways the same share of
  trips at every fleet. With 30 and 50 SKUs the ranking went round in 3000 and 5000 steps. The safety stock
  sized at each SKU's starting rank left 6 to 14 % of orders waiting at Q = 15, and sizing it at the top rank
  brought fleet 8 to 0.0 % with picks 14 % faster. Model revision "D25, sized" and "D25, safety stock".
- **Rejected.** A Q per fleet (put-away share 9 to 17 % by fleet). Large Q to hide the waits, which leaves
  under one refill per cycle.
- **Code.** Not yet: `refill_starting_stock` (top rank), the configs.

### [A76] Each SKU belongs to one delivery vertex (Design change, thesis text edited 2026-10-30)

- **Where.** `sec:method:storage` (the trip distance and its reason, replacing the stand-in of `[A55]`),
  `sec:impl:instances` (the delivery vertex count, how an order picks its delivery vertex, the
  fixed homes), the scope item "SKUs ordered independently" in `2.Introduction.tex`, `eq:tripdistance`
  (Appendix C, now $d^{\mathrm{trip}}_t(k,v)$ with $\hat h_t(k)$), Appendix D (the shelf-only trip relabelled
  `eq:shelftrip`), `tab:notation` ($h(k)$), `tab:evalparams`, Appendix F.
- **What the edit says.** Each seed splits the SKUs at random over the delivery vertices, 10 each, so there
  are |K| / 10 delivery vertices, each with its own section, fixed for the run. An order picks its delivery
  vertex at random and draws its lines from that vertex's SKUs by popularity. The demand rules read the
  SKU's delivery vertex from the last storage period's lines. Fixed storage places its homes near h(k)
  and never moves them. Kept simple by the author (2026-10-30), no swaps, model revision "D29, simplified".
- **Why.** With a random delivery vertex per order the rule's best shelves were only 3 to 10 % closer in
  practice than an average shelf, so storage had no place to aim for (step 12 sweep). Model revision D29.
- **Rejected.** The mean over the delivery vertices, as `[A70]` does for the docks, which leaves storage
  little to gain. A soft link, or fewer lines per order, which with m/2 delivery vertices leave 2 to 5 SKUs
  per vertex.
- **Code.** Not yet.
- **Revises.** `[A55]` (the second leg as a stand-in), `[A70]` (m/2 delivery vertices, the nearest one).

### [A77] The warehouse scales with the fleet, and each section has four workstations (Design change, thesis text edited 2026-10-31)

- **Where.** `sec:impl:instances` (shelves and workstations, the SKU count, the sections, Q in the
  starting stock, the homes of F_fix), `sec:method:storage` and `eq:tripdistance` in Appendix C (the
  second leg), the Token Passing paragraph of `sec:method:controllers`, the orders text and a new
  scope item in `2.Introduction.tex`, `tab:notation` (h(k)), `tab:evalparams` (Appendix B).
- **What the edit says.** Everything grows with the fleet. Per agent 16 walkable vertices, 5 shelves,
  2.5 SKUs, half a workstation, half a dock and one parking vertex, so 20, 40, 80, 160 SKUs and 40,
  80, 160, 320 shelves at 8, 16, 32, 64 agents, two shelves per SKU. Each SKU belongs to a section of
  20 SKUs, a random split per seed, and each section is served by 4 workstations on neighbouring
  rack faces. An order picks one workstation at random, draws its lines from that workstation's
  section, and every line goes there. h(k) is now the section's workstations, and the second leg
  of the trip is the mean distance to them. Q = 10, so put-aways are a fifth of the trips. Token
  Passing's rule lets one agent head for a workstation at a time, so an order's lines queue there.
  This is kept and stated as a limitation, since the router is not what the thesis tests.
- **Why.** With 10 SKUs per section and 5 lines per order, demand was nearly flat: the top fifth of
  SKUs took 33 % of the lines, against 46 % with sections of 20 and 64 % for one-line orders over
  every SKU (a simulation of the order drawing, 2026-10-30). One rule, everything per agent, keeps
  every warehouse equally full and is easy to state. On the queue: a scratch run at fleet 8 (6
  seeds, load 0.1, Token Passing) gave picks of 212 steps, 187 of them waiting for the workstation,
  with one vertex per workstation, against 36 steps with four entry points per workstation.
- **Rejected.** The SKU count from the load (250 x load in `[A75]`), which keeps the refills per SKU
  equal across fleets but not how full the warehouse is. A shelf on every rack face, which makes a
  large warehouse nearly empty (about 5 shelves per SKU at 64 agents). Several entry points per
  workstation, which removes the queue but changes the warehouse for one router.
- **Cost.** A SKU is refilled less often in a large warehouse, since the load grows more slowly than
  the fleet. The step 12 sweep of 2026-10-31 measures by how much.
- **Code.** slap-mapd-coupling `18fefda` on main (`workstations_per_section`, `Vertex.section`,
  configs/step12).
- **Revises.** `[A75]` (the SKU count from the load, Q = 12), `[A76]` (10 SKUs per workstation, one
  workstation per section, the second leg to one vertex), `[A71]` (two shelves per SKU, now 5 per
  agent over 2.5 SKUs per agent).

### [A78] The network reads distance as a difference from the robot's own vertex (Design change, thesis text edited 2026-11-02)

- **Where.** `sec:method:model` ("What the network reads" and a new paragraph "Distance as a
  difference", new `eq:relativeeta`), `eq:features` in Appendix C, `tab:notation`. Same day, from the
  same review of the network: a "No memory" paragraph at the end of `sec:method:model`, one line on
  the pooled mean in `sec:method:controllers`, "close to the target" in `sec:method:rl` with the
  1 - gamma note, and L = 0 to 5 in Appendix J (`app:training:method`, `tab:app:rounds`).
- **What the edit says.** Each vertex gets its distance to the target minus the robot's own
  distance, capped at plus or minus d_obs. The reward's potential still uses the distance itself.
- **Why.** The distance is to the target, not to the robot, so it is large on every vertex in view
  (about 30 in fleet 8, over 50 in fleet 64), next to features that are 0 or 1. The move only
  depends on the difference, which was hidden in two large numbers. Small numbers centred on zero
  train better with PPO. The cap gives the feature the same range under every controller, as the
  crowding number has, since the centralised window is the whole warehouse.
- **Rejected.** Dividing the distance by d_obs, which shrinks the numbers but still hides the
  difference. No cap, which leaves values as large as the warehouse in the centralised window.
- **Cost.** The robot sees which way is closer but no longer how far it is from its target in
  total, so the value head cannot tell 2 steps left from 40. The author keeps it so (2026-11-02):
  the move only needs the direction. Rejected with it: the robot's own distance as one extra scaled
  number next to the crowding number. Memory and speed are unchanged. The policy can still take a
  step back for a bigger gain later.
- **Code.** Not written yet. `environment/observation.py` (the feature) and the tests that check its
  values. Do it before the step 5 training runs.

### [A79] The shaping potential at t+1 is read after assignment and parking (Correction, thesis text edited 2026-11-04)

- **Where.** `sec:method:rl`, the paragraph after `eq:reward`, and one new paragraph after it.
- **What the edit says.** Phi_i(t+1) is the potential the robot sees at t+1, after new tasks and
  parking vertices are handed out. A free robot's target is its own vertex, or its parking vertex
  when it stands in another robot's way (D26).
- **Why.** The code computed the reward before assignment and parking, so the jump in the
  potential when a robot got a new target was never charged. The shaping then no longer cancelled,
  which Devlin and Kudenko's guarantee needs. Each task carried a free bonus of about its distance
  to the shelf. With D26 an idle robot could earn it again and again by standing in the way, a loop
  the policy can learn. A fleet 8 check with a robot that always steps towards its goal (2000 steps)
  found 12 jumps the reward never charged, adding up to -95.
- **Rejected.** Leaving free robots out of the shaping, which removes the parking loop but not the
  free bonus of every task.
- **Cost.** A robot pays a one-off amount when it gets a task. It does not choose its tasks, so no
  best behaviour changes, but the value head has to learn the drop.
- **Code.** `environment/multi_agent_env.py::step`: the rewards move after `_release_and_assign`
  and `_update_parking`, and the parking target is read before and after the step, not once. A test
  checks that the potentials match from one step to the next.

### [A80] Raising the move cost above the wait cost (Rejected 2026-11-10, thesis text removed)

- **What was tried.** c_move = 0.25 against c_wait = 0.2 (edited 2026-11-04), so that a blocked
  robot waits instead of stepping away and back. With c_move = 0.1 stepping away and back costs 0.2
  over two steps against 0.4 for two waits, and the fleet 32 decentralised runs of 2026-11-04 did
  that before they collapsed (tasks done 113 at iteration 4, 1 at 16).
- **Why rejected.** It froze the robots instead. Fleet 8 decentralised fixed_only, 25 iterations
  each, one seed (`~/thesis_runs/training_fixes_test/ablation/`): with the reward order of `[A79]`
  alone the run reached 155 tasks done per episode at iterations 21 to 25 and 33 % standing still.
  Adding c_move = 0.25 gave 4 tasks and 79 % standing still. The run without any fix (main
  `514624c`) gave 182 tasks and 37 %.
- **Now.** c_move stays 0.1 and `[A43]` stands. The stepping back and forth is left to the
  following rule of `[A81]`, which removes many of the blocks behind it. To check again on fleet
  32, where the collapse happened.

### [A81] Conflict resolution lets a robot follow a robot that leaves (Design change, thesis text edited 2026-11-04)

- **Where.** `sec:method:resolution`, the rule and the two paragraphs after it.
- **What the edit says.** A robot that moves onto another robot's vertex is handled after that
  robot. Of the robots that are ready, the priority order decides. Robots whose chain of wants
  closes into a circle (a swap is the shortest) wait. The claim mask is unchanged and stricter, so
  the centralised and section-based joint actions are accepted whole.
- **Why.** Under `[A53]` a robot could not move onto the vertex of a robot later in the order even
  when that robot left, so following another robot in an aisle cost a wait and the override
  penalty. The robot cannot see its priority, so the penalty looked random to the policy. The
  decentralised arm had a 10 to 20 % override rate against about 0 % for the others, and blocked
  moves towards the target fed the stepping back and forth seen in the fleet 32 runs (`[A80]`).
- **Rejected.** Leaving it and naming it as a limitation.
- **Cost.** A robot ahead in a chain is handled before robots earlier in the order, so it can win
  an empty vertex against them. Circles of three or more robots still wait.
- **Code.** `resolution/conflict_resolution.py::resolve_conflicts` (`move_blocked` stays the claim
  mask), tests in `tests/unit/test_conflict_resolution.py`.
- **Revises.** `[A53]` (the rule, the claim-mask wording).

### [A82] The network also reads the distance to the target, scaled (Design change, thesis text edited 2026-11-04)

- **Where.** `sec:method:model` (a paragraph "How far the target is" and the scaled label after
  `eq:relativeeta`), `eq:features` in Appendix C.
- **What the edit says.** Each vertex also gets eta_i(v,t) / 50, as in van Knippenberg et al.
  (2021), next to the relative label of `[A78]`. The same 50 in every warehouse.
- **Why.** With the relative label alone the robot cannot tell 2 steps from 40, so the value head
  cannot see a value that grows with the distance (the cost noted in `[A78]`). Dividing by one
  fixed number keeps the feature near 0 to 1 next to the 0/1 features, which `[A78]` was about.
- **Rejected.** Raw distances (the scale problem of `[A78]` again). Dropping the relative label.
- **Cost.** One more feature (9 per vertex). Old checkpoints no longer load.
- **Code.** `environment/observation.py` (`DISTANCE_SCALE`), `models/gnn_encoder.py`
  (`NODE_FEATURE_DIM` 9), `models/local_subgraph_encoding.py`, `models/window_tables.py` (the
  compact "eta" holds both labels).
- **Revises.** `[A78]` (its rejected option).

### [A83] Readability pass on the introduction, and the research questions on hold (Design change, thesis text edited 2026-11-10, uncommitted)

- **Where.** `2.Introduction.tex`, the whole introduction and project description. Tagged `% [A83]`.
- **What the edit says.** One name per idea: "demand storage" (not adaptive or demand-only),
  "congestion-aware storage" closes the loop. The link between the layers is told with a concrete
  example. Orders are told first, then the pick task they create. Each measure is tied to the
  question it answers. Decision time, put-away service time and orders finished leave the
  introduction. The contribution paragraph is cut, and its one sentence opens the expected outcome,
  which now lists the three deliverables (model, simulator, measured gain). The main-result
  paragraph keeps the percentage gain and drops the 95% interval (already in the Experiments
  chapter and `eq:rqformal`), the reference sentence and random storage. Nothing is added to the
  Experiments chapter (author, 2026-11-10).
- **Load.** Appendix E builds the warehouse. It uses Token Passing to choose the main load and does
  not answer a research question. The load question is answered by evaluating each trained
  controller at several arrival rates, with no new training. Fleet size stays in the load, for the
  fleet sizes that are trained. The load is given as a share of what the fleet can serve.
- **Research questions, on hold.** New list in the chapter, old list commented out next to it:
  old RQ1 and RQ2 merged into RQ1, old RQ3 and RQ4 become RQ2 and RQ3, old RQ5 becomes RQ4 and is
  no longer conditional. To be revisited once the results are in. Until then the other chapters
  and Appendix E keep the old numbering.
- **Why.** The author's review (`Thesis _comments.pdf`, 2026-11-09). The section used several names
  for the same thing and did not say clearly what the main result is. RQ2 read as a repeat of RQ1.
- **Open, settled in `[A84]`.** The author asks whether a main result on demand storage, which does not close the loop,
  carries the thesis idea of coupling MAPD and SLAP. See `[A44]`.
- **Code.** None.

### [A84] Coupling is tested two ways, and the loop also at a higher load (Design change, thesis text edited 2026-11-10, uncommitted)

- **Where.** `2.Introduction.tex`, the two coupling paragraphs and the new RQ2. `3.ProblemFormulation.tex`,
  `sec:pf:coupling`. `5.Experiments.tex`, the mapping paragraph and `tab:expfactors` (new row).
  Tagged `% [A84]`.
- **What the edit says.** Coupling is tested two ways. One way: demand storage changes where the
  robots drive, and the main result asks whether its gain depends on the controller. Both ways:
  congestion-aware storage reads the traffic and closes the loop. The loop is tested at the main
  load and at a higher load where every controller still keeps up but the aisles are crowded.
  `sec:pf:coupling` no longer says adaptive storage adds the backward path. Only congestion-aware
  storage does.
- **Why.** The thesis idea is the coupling of MAPD and SLAP, but demand storage only works one way,
  and in the step 12 sweep the congestion weight changed nothing (within 2 %) at the main load.
  Avoiding crowded aisles can only help where the aisles are crowded, which the main load may not
  give. A little-effect answer is still a result, and fits the expected outcome.
- **Rejected.** Making the closed loop the main result, given the 2 % finding.
- **Gap.** The higher load is TBD. Choose it from the load test (old RQ4, new RQ3) as the highest
  load where every trained controller still keeps up, not from the Token Passing sweep.
  **Settled by [A131] (2026-11-24):** this rule has no answer, since the learned controllers fall
  behind at the main load. The higher load is 0.9 of Token Passing's capacity.
- **Cost.** Evaluation only. The main setup runs one frozen policy, trained under fixed storage,
  under every storage rule, so no new training.
- **Revises.** `[A44]` (adds the one-way reading and the higher load). Settles the open point of `[A83]`.
- **Code.** The evaluation scripts need the higher load as one more condition for demand and
  congestion-aware storage. Small.

### [A85] Random storage is dropped (Design change, thesis text edited 2026-11-10, uncommitted)

- **Where.** `G.StorageValues.tex`: the subsection `app:cal:random` with its figure
  `fig:app:stockmoments` removed, the refill-size sweep sentence and the conclusion no longer mention
  random storage. `2.Introduction.tex` already dropped it (`[A83]`). Tagged `% [A85]`.
- **What the edit says.** Random storage is not part of the thesis. Fixed storage is the only
  reference the gain is measured against.
- **Why.** The author does not want it, and the thesis should stay as short as it can. Its one job
  was to check that the gain of demand storage comes from knowing demand, not from spreading stock.
  The step 12 sweep answered that clearly (random 48 to 210 % slower than fixed, on every seed), so
  it adds length without supporting a research question.
- **Rejected.** Keeping the stock moments figure with only fixed and demand storage. Its text was
  built around random storage.
- **Code.** `scripts/sweep/parameter_sweep.bash` no longer runs the refill-size sweep under
  `random` (the only run that used it, uncommitted on `main`). The evaluation in `bedtime.bash`
  never ran it. The mode itself and `scripts/images/stock_moments.py` stay, unused by the thesis.
- **Revises.** `[A83]` (random storage was to move to the Experiments chapter).

### [A86] Readability pass on the environment, docks, no V_mov, agent from the Problem Formulation on (Design change, thesis text edited 2026-11-10, uncommitted)

- **Where.** `3.ProblemFormulation.tex`: the chapter opening and `sec:pf:env`, the uses of V_mov and
  "receiving vertex" further on. `4.Implementation.tex`, `5.Experiments.tex`: "robot" becomes "agent"
  in the text (comments untouched), V_mov and "receiving vertex" removed. `A.Notation.tex`: the V_mov
  row removed, V_rcv renamed V_dock ("docks"), the role sets, N+(v), d_G, the zones, the location
  and the end vertex now over V. `C.ModelDetails.tex`: V_dock in the trip distance, `eq:onestepcost`
  moved from the `sec:pf:env` group to a new `sec:method:rl` group. `G.StorageValues.tex`: docks.
  Figures `instance_simple`, `instance`, `observation` (legend V_dock, plain vertices "aisle") and
  `conflicts` (agents a_1 and a_2, no formulas, "a_2 waits"), redrawn from
  `scripts/images/m8.py` and `conflicts.py`. Tagged `% [A86]`.
- **What the edit says.** The chapter opens with one sentence and says once that a robot is called an
  agent. The environment is told in words first, then as a graph. Every edge costs 1, so the two
  directions never cost differently and that sentence is gone. The wait-or-move action model is
  only in `sec:pf:agents`. The wait cost is left to the reward. The receiving vertices are called
  docks everywhere, V_dock. V_mov is dropped, because every vertex is a place an agent can stand,
  so the role sets are subsets of V. The Figure 1 caption names the two middle aisles as one-way,
  as the picture shows.
- **Why.** The author's review, 2026-11-10. The opening repeated the introduction, the environment
  had the action model twice, introduced the wait cost before its use and used two names for the
  docks. Figure 2 repeated equations 3 and 4 just above it. "Robot" and "agent" were the same word.
- **Rejected.** Keeping V_mov for a later warehouse with positions agents cannot enter. It can come
  back when such a warehouse exists.
- **Not changed.** The introduction and project description keep "robot". `2.Notation.tex`,
  `tmp1.tex` and `C.ModelDetailsV1.tex` (old versions) keep the old symbols.
- **Code.** None. The code may keep its own names for these sets.

### [A87] Readability pass on where the items are, and the storage update places at most what arrived (Correction and design change, thesis text edited 2026-11-10, uncommitted)

- **Where.** `3.ProblemFormulation.tex`: the chapter opening and `sec:pf:storage`. Figure
  `arrival_storage` (`fig:storageexample`) redrawn from `scripts/images/arrival_storage.py`.
  Tagged `% [A87]`.
- **What the edit says.** The opening is the short picture of the warehouse again, and says once that
  a robot is called an agent. The subsection is told in words first. The storage state stays a
  counting function. Room on a shelf is explained before eq:feasiblestorage. How stock changes is
  three steps (arrives at a dock, the rule picks the shelf, an agent carries it). x^in is explained
  as units on their way ("in" for inbound). The three estimates come before the storage update and
  say who uses them: demand storage the orders, congestion-aware storage also the crossings and
  waits, which come from how the agents moved. The storage update states its three conditions in
  words, then as equations, without "subject to". Each condition has a short name beside it
  (labels `eq:upd:room`, `eq:upd:keep`, `eq:upd:arrived`), and an example on the stock of
  Table I shows all three, including units left unplaced. The objective no longer names a separate x*, it
  is written on x^in. The "simpler map" paragraph, the bullet list and the separate timing paragraph
  are gone. The example follows Figure 3 and is told with demand storage. Figure 3 draws the tea on
  shelves, labels the square as the workstation only and calls panel (b) demand storage.
- **Correction.** The third condition of the storage update was "=", so every arriving unit had to
  get a shelf. The Implementation chapter leaves what fits nowhere unplaced, so it is now "<=", as
  an older draft had it.
- **Kept.** w_hat, explained in one line (the author chose to keep it over using waits or crossings
  alone, 2026-11-10). Equations 7 to 10 stay in the main text, because the storage update is the
  core of the storage side of the model.
- **Why.** The author's review (`Thesis _comments.pdf`). The subsection was abstract, gave
  symbols before their meaning and did not say who uses the estimates.
- **Code.** None for the text. Check that the code also leaves unplaced what fits nowhere.

### [A91] Agents can lock at a workstation on a one-lane aisle, kept as a limitation (Design decision 2026-11-11 and 2026-11-12, thesis text edited 2026-11-12)

- **What happens.** A workstation hangs off an aisle by a single edge ([A62]). When that aisle is one
  lane wide, agents bringing lines to the workstation queue on the aisle. The agent at the
  workstation then wants the aisle vertex the first agent in the queue stands on, and that agent
  wants the workstation. That is a swap, the shortest circle of `sec:method:resolution`, so both
  wait. The queue behind blocks the only way out, so nothing breaks the circle unless an agent
  chooses to back out. The section around that workstation stops, and the rest of the fleet keeps
  working. Seen in the traces of 2026-11-11 (`~/thesis_runs/training_fixes_test/`, fleet 8 and
  fleet 32, [A90] reward), for example test seed 200000.
- **How often the layout occurs.** Over the 258 warehouse seeds of each fleet, a section with all
  four of its workstations off a one-lane aisle vertex (degree 3 or less) occurs in 35 seeds at
  fleet 8 (14 %) and 70 at fleet 32 (27 %). Of the six test seeds, 200000 and 200005 have it at
  both fleet sizes.
- **Token Passing is not affected.** Its paths keep a vertex from one step before arrival to one
  step after leaving, and every warehouse is well-formed ([A28], `app:wellformed`), so it does not
  lock. The limitation is one of the learned controllers on this family of layouts.
- **Rejected: a cap on tasks per workstation.** A rule that gives a workstation at most k open
  tasks at a time (k = 1 and k = 4 were discussed) was coded in `~/worktrees/workstation-cap`
  and stopped before it ran in full. It changes the assignment rule that every controller shares,
  and it fights the order model, where all lines of an order go to the same workstation. van
  Knippenberg et al. (2021) have no such rule either. Not used.
- **Rejected: rebuilding the layout.** Making the aisles two lanes, or the workstations not hang
  off one-lane aisles, would remove the lock but means a new warehouse sweep with Token Passing.
- **Decision (author, 2026-11-11).** Keep the layout and the rules. Train the controllers as they
  are, so that whether they learn to back out is part of what is measured. State it as a
  limitation, and report it in the results.
- **What is reported.** The number of locked test seeds per controller and storage rule, next to
  the keep-up check. Under RQ4, whether messages make it rarer. A two-seed test at fleet 8 with
  congestion-aware storage (`fleet8_congestion` and `fleet8_congestion_comm`) is all there is so
  far, three seeds. By the rule below, two of three seeds lock without messages and none with them,
  and with messages the fleet finished more tasks (91 against 43, 155 against 107, 201 against
  143). An earlier version said messages did not prevent the lock. It used a looser test (one agent
  standing still for 50 steps) and is corrected. Numbers and commands in
  `results/limitations/workstation_lock/README.md`.
- **Decided (author, 2026-11-12).** A seed is locked when at least two agents each hold the same
  task for 500 steps or more at the same time. A locked seed counts as not keeping up. The
  evaluation uses 20 test seeds (5 of them have the layout at fleet 8), which needs an option in
  the code, since the trained runs store 6. The mechanism and the figure `workstation_lock` go in
  the Implementation chapter beside conflict resolution. Review PDF
  `active/readability_review/review_workstation_lock.pdf`, approved 2026-11-12.
- **Where.** `4.Implementation.tex`, `sec:method:resolution`: the paragraph on a lasting circle,
  figure `fig:workstationlock` (`Images/workstation_lock.png`, from
  `scripts/images/workstation_lock.py`) and the paragraph that walks through it.
  `5.Experiments.tex`: the keeping-up and communication mockups and a threat to validity. All
  tagged `% [A91]`.
- **Why the decentralised controller does not back out (added 2026-11-12, author).** It is
  credited with its own reward only, so backing out for another agent gains it nothing, while
  the section-based and centralised controllers share the reward of the agents that choose
  together. The congestion term charges crowding, the same whether an agent waits or backs out,
  and the override penalty falls on the agent that wants to leave, not on the one that blocks it.
  So messages (RQ4) are its only way to learn it. Rejected for now: a larger congestion weight
  (does not point to the move that helps) and a penalty on the blocking agent (a new reward of the
  thesis's own, and every run would restart). A shared reward for the decentralised controller
  is named as future work in the threats to validity.
- **Code.** None. The cap branch `feat/workstation-cap` is not merged.

### [A93] Congestion is measured as the time picks stand still at each shelf (Design change 2026-11-13, thesis text edited 2026-11-13)

- **Why the old signal went.** Congestion-aware storage read, for each edge, crossings times waits
  per step (`\hat\mu_t(e)\,\hat w_t(e)`). That number is about 1e-4 per edge against a trip of about
  29 steps, so it never moved a shelf. Only 18 to 34 of 782 edges see a wait in a storage period, so
  the shelf order it gives changes almost completely each period. Under Token Passing a pick stands
  still 1 to 2.5 steps, and most of its time is the wait for an agent, on no edge. Waits per
  crossing, crossings alone, workstation pressure and their mix did no better than demand storage
  with Token Passing (fleet 8, 10 seeds).
- **What replaces it.** `\hat\omega_t(v)`: each finished pick counts the steps its agent stood still
  (the blocked part of `eq:split`) and notes them on the shelf it came from. A period's reading is
  the mean over the shelf's picks, and `\hat\omega_t(v)` is the plain average of the shelf's last
  five readings (author chose this over keeping one fifth of each new reading, which works about
  the same but is harder to explain). One period alone has about eight picks per shelf at 8 agents.
- **Where it acts.** The score becomes `\hat\rho_t(k) (d^trip + \beta \hat\omega_t(v))`, `\beta = 1`,
  and `K = \sum \hat\rho_t(k) \hat\omega_t(v) x^new`. Both terms count steps. Under
  congestion-aware storage a line also picks from the shelf with the least distance plus
  `\hat\omega_t(v)`, so the loop closes on every order line and not only every `\Delta` steps.
- **Demand stays on the nearest shelf (author, 2026-11-13).** Demand storage knows only the orders.
  Picking by standing still would make it read congestion too, and the gap to congestion-aware
  storage would no longer show what reading congestion adds. The nearest shelf is the plain rule
  without traffic knowledge. This also keeps every fixed and demand run valid.
- **Not averaged: the demand estimate.** With Token Passing, averaging `\hat\rho_t` over periods
  made no difference (+0.2 against -0.2 percent, fleet 8, 20 seeds), so congestion-aware storage
  reads the same `\hat\rho_t` as demand storage.
- **Evidence.** Policies trained under demand storage, best checkpoint by training tasks, 5 seeds,
  4000 steps with 1000 left out. With the signal in storage and picking, standing still per pick
  fell on every seed: fleet 8 decentralised (ck24) 21.0 to 17.3, tasks equal, service 294 to 244;
  fleet 16 section (ck25) 32.5 to 29.1, tasks 361 to 384. Fleet 16 decentralised (ck23) and fleet 32
  decentralised (ck2) jam over long runs and cannot be read (author: fleet 16 decentralised needs
  messages). Rows and scripts in `results/G_storage/a93_first_look/`.
- **Thesis text.** `3.ProblemFormulation.tex` (what the rule knows, `eq:storageupdate`, K, the
  pickup rule under congestion-aware storage and why demand keeps the nearest shelf, the loop),
  `3.Background.tex`, `4.Implementation.tex` (`eq:storagegreedy`, the estimate paragraph, the [A36]
  paragraph removed), `C.ModelDetails.tex` (`eq:estimates`, the pick order, the measures note),
  `G.StorageValues.tex` (`app:cal:beta`), notation and parameters. Tagged `% [A93]`. Review:
  `active/readability_review/review_shelf_blocking.pdf`. Open in the text: the Token Passing and
  learned numbers of `app:cal:beta` (TODO comments).
- **The loop figure and the names (author, 2026-11-13).** `fig:loop` is now `shelf_loop.png`
  (`scripts/images/shelf_loop.py`), the tea example of `fig:storageexample` one period later: picks
  queue at shelf A, so the next line takes C and the new tea goes to the quiet aisle. It replaces
  the box diagram of `loop.tex`, which repeated the Introduction and `fig:methodloop` and never
  showed standing still. `K` is renamed the *blocking cost*, because since [A93] it charges blocking,
  not crowding (it was the crowding cost, and the congestion term in the Background). `\delta_i(t)`
  is the *crowding feature* everywhere (it was also the congestion feature and the crowding number),
  and the reward's last term, which charges it, is the *crowding term* (was the congestion term).
  Its weight is `n_{\mathrm{crowd}}` (was `n_{\mathrm{cng}}`, which looked like `F_{\mathrm{cng}}`). The
  code keeps its own name for the weight.
  Storage reads standing still and not the crowding feature, because a crowd that keeps moving costs
  no time. A storage rule on `\delta` itself was not run. Review:
  `active/readability_review/review_loop_figure.pdf` (v3).
- **RQ2 and the Introduction (author, 2026-11-13).** The goal is unchanged, but closing the loop now
  acts in two places. RQ2 reads "storage also avoids shelves where robots get blocked" (was "avoids
  crowded aisles"), and the Introduction says the rule steers both new stock and picks away from
  those shelves. RQ2 measures both parts together (option a). This is said in the RQ2 results and
  listed as a threat to validity. Splitting them (Token Passing with only the placement or only the
  pick part, Appendix G) was option b, left for when the `app:cal:beta` reruns happen.
- **Implementation check (author, 2026-11-13).** The same kinds of error fixed in
  `4.Implementation.tex`: arriving units go in whole refills of Q onto the first shelf with room
  (the code's `rule: refill`, `_put_away` with `whole`), not "as many as fit"; the loop's step 1 and
  one sentence in "Where arriving stock goes" now name the pickup rule under congestion-aware
  storage; "crowding number", "adaptive storage" and Token Passing's "delivery" renamed; Token
  Passing also runs under demand storage (was "fixed storage" only); the storage score is used at
  each storage update, the pickup rule every timestep. Open: the workstation lock figure uses runs
  trained under the old signal.
- **Refills in the Problem Formulation and the figures (author, 2026-11-13).** "How stock changes"
  says stock comes in refills of Q, each whole onto one shelf as one put-away. The storage update
  example uses three refills of 3 tea (6 of 9 placed) with `storage_update.png` beside it
  (`fig:storageupdate`). Stage 1 of `methodloop.pdf` names the pickup rule. An Overleaf tab opened
  before a push reverted `app:cal:beta` (`76033fe`); the merge kept the new text.
- **Figures and names (author, 2026-11-13).** "Adaptive storage" replaced in the main chapters by
  demand storage, both rules by name, or the rule F in the formal research question. Figures (review
  `active/readability_review/review_figures.pdf`): `controllers_window.png` merges
  `controllers_example.png` and `congestion_mini.png` (`fig:controllers-example`, `fig:congestion`
  gone); `architecture_compact.pdf` moved to Appendix C (`app:controllers:sources`); the tea example
  `arrival_storage.png` redrawn with a dock and slot-box shelves by `shelf_loop.py` (`arrival_storage.py`
  removed), and `shelf_loop.png` with the dock on the left, because with the dock on the right the
  empty shelf of the right aisle was the shortest trip and demand storage would not have chosen A.
  `observation.png`: the aisle vertices are v and w (were B and C, which name shelves).
  `instance.png`: shelves B and C carry Table I's stock, the legend says "route of a_2 while tau_1 is
  active" (was "Active set B_t", with the task missing its units).
- **Appendix check (author, 2026-11-13).** Appendix C "The arrivals" and `eq:arrivals` now follow the
  refill rule the runs use (`rule: refill`, `refill_amounts`): one refill of Q for every Q units
  ordered since the last refill, the rest carries over, the (R, nQ) policy of Axsater (2015) with the
  reorder point one refill below the starting stock (citation not checked against the book). It was
  the top-up rule (margin epsilon, floor x_min), which the code keeps but the thesis runs do not use.
  Notation: `y^ord_t(k)` added, epsilon, x_min, rho^unit and q^wait removed. Appendix G: the
  congestion-aware rule described by standing still (was the edge waiting), the weight checked at
  beta = 1 against demand storage (was a sweep 0 to 4), refills in "Shelf capacity", conclusion
  updated. "Adaptive" and "demand-only" replaced in A, C, E, F, G; "robot" is "agent" in C, E, G, H,
  J, L. Review: `active/readability_review/review_arrivals.pdf`. `C.ModelDetailsV1.tex` (unused draft
  with another outline) left for the author.
- **Code.** `slap-mapd-coupling` branch `feat/a93-shelf-standing-still`: `ShelfStandingStill` and the
  per-shelf reading in `environment/storage_estimates.py`, the reading per finished pick and the
  pick rule in `environment/multi_agent_env.py`, the score in `storage/arrival.py`
  (`putaway_congestion`). The instant put-away path still reads the edge estimates and is not part
  of the thesis model. The edge counting itself is still recorded but no longer read on the robot
  put-away paths.
- **To rerun.** Listed in SESSION_CONTEXT.md: the Token Passing `app:cal:beta` and the congestion
  rows of `app:cal:period`, the congestion-regime training at fleets 8, 16 and 32, and decentralised
  with messages at 16. Fixed and demand runs stay valid.

### [A95] Runtime is measured on one machine, the learned controllers on the GPU and Token Passing on the CPU (Design change 2026-11-15, thesis text edited 2026-11-15)

- **Where.** `4.Implementation.tex`, `sec:impl:cost`. `5.Experiments.tex`, the compute environment
  paragraph. Tagged `% [A95]`.
- **What the edit says.** The time per decision is logged on the same machine for every controller.
  The learned controllers run their policy on its GPU. Token Passing runs on the CPU, the hardware it
  is built for, so each method is timed on its own hardware. Token Passing's planning time per
  decision is still what the learned routers' decision time is compared with.
- **Why.** The learned controllers are a GPU workload and were trained and tested with the policy on
  the GPU. Token Passing cannot use a GPU. Timing each on its own hardware still shows whether the
  learned routers decide faster.
- **Rejected.** kappa_T on the CPU for every controller (the author's choice of 2026-11-13). It holds
  the learned controllers to hardware they are not built for.
- **Code.** None. `evaluate --gpu` with 3 test seeds, one policy at a time with nothing else heavy on
  the PC (unit `rt16-gpu`, `~/thesis_runs/runtime_gpu_2026-11-15_fleet16/`, into `runtime_gpu/`).
- **Open.** Token Passing's own time per decision must come from this PC too. Fill the
  "runtime measurement" row of `tab:exp:compute` (RTX 2070 SUPER) once the run is done.

### [A96] The keep-up check counts the work served in the window (Design change 2026-11-16, thesis text edited 2026-11-16)

- **Where.** `3.ProblemFormulation.tex`, "Keeping up" (a new paragraph, eq:throughput and its
  sentence, the measures table). `E.Load.tex`, the check and how a failing run is reported. Notation
  rows in `A.Notation.tex` and `2.Notation.tex`. Tagged `% [A96]`. Review:
  `decisions/active/readability_review/review_served_share.pdf`.
- **What the edit says.** The check compares the tasks finished in the measured window, whenever
  they were released, with the tasks released in it, for picks (with ship tasks) and put-aways apart
  ([A59]). Each share must be at least f_up. New sets R^pick_T, D^pick_T and the same for put-aways
  (D, since calligraphic F is the storage rule class). A failing run is reported by its served share.
  C^put_T is no longer used and left the notation table. f_up stays 0.8 (the author's yes of
  2026-11-16, read as keeping it).
- **Why.** Since [A66] the old check counted only tasks released in the window. A fleet that fell
  behind in the warm-up works through its older tasks in the window, so the old share was near 0
  however much it served. Every learned fleet 16 run read "0 of 20" and the arms could not be told
  apart, although centralised fixed never went more than about 68 steps without finishing a task.
  The served share asks what the check is for, whether the queue grows or holds.
- **Rejected.** Reporting the share next to the old check. The old check fails every run that fell
  behind early, however much it serves later.
- **Code.** Branch `feat/served-share` (worktree `~/worktrees/served-share`), uncommitted:
  `served_counts`, `served_keep_up_parts`, `RunMetrics.served_share` and its pick and put-away parts,
  `row_keeps_up` reads the shares when a row has them. Tests in `test_evaluator.py`,
  `test_horizon.py`.
- **Open.** (1) Appendix E's capacities and so every fleet's main load were found with the old check.
  Token Passing keeps up with almost no backlog at the main load, so its rows pass either way, but at
  the capacity edge the two checks can differ. Its rows hold no served counts, so checking needs the
  load sweep near the capacity played again. Queued 2026-11-16 (unit `load-served`,
  `~/thesis_runs/load_served_2026-11-16/`, rows in `results/E_load/fleet_<m>/served_check/`). One fleet
  8 seed at 0.15 reproduced the old row exactly, served share 0.99 picks, 0.97 put-aways. (2) The fleet 16 tests are replayed with the new counts
  (`~/thesis_runs/replay_served_2026-11-16/`). Until then `fleet16_results.py` draws an estimate from
  the backlog slope. (3) Fleets 8 and 32 tests have no served counts either.
- **Revised 2026-11-17 (author's yes, review `readability_review/review_served_share_lines.pdf` v4).**
  (1) An order line released in the window that still waits for stock at T counts as one released
  pick. A pick task is made only once its stock is on a shelf, so a fleet whose put-aways fail
  released almost no picks and its pick share read high (fleet 16 decentralised fixed 4.8, 835 lines
  waiting). Option chosen: one per line (a line is 1.03 to 1.18 tasks). Rejected: counting by order
  line, cleaner but new code and every run played again for no change in any verdict, and counting
  only lines released in the window, which brings back what [A96] fixed. Checked on the replay rows:
  no keep-up verdict changes, the pick share lands on the put-away share. (2) Lambda_T counts every
  task finished in the window, whenever released, per step after the warm-up (said in words, no
  warm-up symbol). It counted only tasks released in the window, centralised fixed 0.036 against
  0.143. C_T left the formula and the notation rows. Changes the Regime 1 claim in Appendix L about
  the policy with messages. Thesis: `3.ProblemFormulation.tex` "Keeping up", `A.Notation.tex`,
  `2.Notation.tex`. Code: branch `fix/served-share-lines` (worktree `~/worktrees/served-lines`),
  uncommitted. Old rows are updated from their counts (`num_finished_in_window`,
  `num_waiting_orders`), not replayed. Checkpoints already chosen stay, since validation rows are
  read back.


### [A97] The model's definitions come back from Appendix C, and the idle target is in the Problem Formulation again (Clarity and catch-up, thesis text edited 2026-11-17, uncommitted)

- **Where.** `3.ProblemFormulation.tex`, tagged `% [A97]`: the environment (graph, not grid, vertex
  numbers break ties, reachability against van Knippenberg), agents and collisions (why not a reward
  penalty), where the items are (eq:arrivals, the starting stock, eq:estimates, the rule set
  F and the three rules), orders and tasks (eq:pickuprule), who decides (eq:partition,
  eq:sectionpolicy), what a decentralised agent sees (the idle target, the two forms the policy reads,
  eq:congestion, eq:commgraph), the learning problem (tab:posg, the action list), how a run is scored
  (eq:runtime, eq:decisionproblem), scope (docks without limit, what deadlines and re-tasking would
  change). `C.ModelDetails.tex`: the arrivals, starting stock, the game table and action list, the
  reported measures, the decision problem, "What the model leaves out" and the moved "Definitions in
  full" are removed. The q_i(t) row in `A.Notation.tex` and `2.Notation.tex`. Review:
  `decisions/active/readability_review/review_pf_content.pdf`.
- **What the edit says.** Each definition is in words first, then the equation, with an example on
  numbers the chapter already has. The idle target is in words only: an agent with no task targets its
  own vertex, or the nearest free endpoint while it is in the way. The free-agent condition stays in
  words, without its display.
- **Why.** The chapter had shrunk from about 13,500 words (19 October) to 9,330, and it used symbols
  it defined only in Appendix C (kappa_T, the section-based policy, F_fix and F, the communication
  graph). The author's rule of 2026-10-23 says the model's formal definitions stay in the thesis. The
  idle target of [A72] was lost from the thesis while every config has `idle_parking: true`. The
  author asked that the text not become too complex, so the short forms of the review were taken.
- **Cost.** Against [A52], displayed equations go from 34 to 43, and the chapter to about 10,600
  words.
- **Code.** None. Checked against `origin/main`: `storage/arrival.py` (refills),
  `storage_estimates.py` (last five readings), `observation.py` (crowding denominator, the two
  distance forms), `reward_function.py::current_target`, `idle_parking: true` in every config.
- **Open.** Docks without limit was a TODO in Appendix C and is now stated. Well-formed warehouses
  stay out of the chapter.
- **Revises.** [A52] (definitions moved out), catches up [A72].

### [A98] The Problem Formulation opens with the problem, and the expected outcome names the coupling

**Where.** `3.ProblemFormulation.tex`, opening of Section `sec:problem`. `2.Introduction.tex`, Subsection "Expected outcome".

**What.** The Problem Formulation now opens by naming the three decisions it couples (storage assignment, task assignment, path finding), then states in plain words what is decided, the three limits (room, no collisions, pick only stock on the shelf) and the score (order time, among pairs that keep up). It points forward to `eq:decisionproblem` in `sec:pf:measures`. The expected outcome now says the thesis delivers a coupling of the three problems, and lists the measured answer each research question gives.

**Why.** The formal statement needs symbols built over the whole chapter, so it stays at the end. A reader still needs to know from the first lines what the chapter builds towards. Asked by the author 2026-11-17.

Later the same day the expected outcome also got the predictions per research question, written before the results are read. The centralised controller gaining most comes from `5.Experiments.tex` ("What deciding together changes"). Keeping up and coming close to Token Passing is the author's aim. The RQ2 balance comes from the introduction. The decentralised controller stopping first (RQ3) and messages helping where routes cross (RQ4) follow from the controllers' design.

**Model change.** None. Wording only.

### [A99] Results and Discussion for 8 and 16 agents, served share first

**Where.** `5.Experiments.tex`, Results and Discussion. `L.Results.tex`, 16-agent block and the new `tab:app:locks`.

**What.** Review `review_results_discussion_fleet16.pdf` v5, approved 2026-11-17. Results report 8 and 16 agents side by side, with a 32-agent column left TBD. The learned controllers are compared by served share, because even seeds that pass the keep-up check leave work behind and their orders take 300 to 3200 steps against 150 to 280 under Token Passing. Service time and its gain are reported for Token Passing only, as the order time (the result of the Problem Formulation) with the pick time beside it. New tables `tab:exp:served`, `tab:exp:locks`, `tab:exp:time`, and `tab:exp:rq1` rewritten per fleet. Discussion fills "What was expected" ([A98]) and adds "The load" and "What could have been done differently" (longer training episodes, more training, a way out of locks, imitation of Token Passing).

**Decisions by the author (2026-11-17).** f_up stays 0.8, every result uses it. The main loads stay, because every run used them, and the Discussion says they assumed every controller would keep up. Order time is the headline. Fleet 32 gets its own column. Token Passing at 8 agents is replayed on the test seeds (`~/thesis_runs/tp_testseeds8_2026-11-17`).

**Open.** Token Passing fleet 8 rows still play seeds 0 to 19 until the replay is home (TODO in `5.Experiments.tex`). Fleet 8 centralised fixed (Kaggle). The section-based Regime 1 row in `tab:app:regime1:16` (rerun20). Fleet 32 tests. `fleet16_served.png` to redraw from the revised counts.

### [A100] RQ4 drops its second part, on where routes cross

**Where.** `2.Introduction.tex`, RQ4 in Subsection "Research question". Tagged `% [A100]`.

**What.** RQ4 now asks only whether local communication makes the decentralised controller route better than what a robot sees on its own. The second part, whether that depends on robots close on the graph being the ones whose routes cross, is dropped.

**Why.** Nothing in the thesis measures whether close agents are the ones whose routes cross, and no experiment varies it, so that part could not be answered. Raised in the review `readability_review/review_project_description.pdf` v2, decided by the author 2026-11-17.

**Closed by [A102] (2026-11-18).** The prediction and the Conclusion sentence are reworded there.

**Was open.** The RQ4 prediction in the Expected outcome ("messages should help most where agents close on the graph are also the ones whose routes cross") and the Conclusion sentence in `5.Experiments.tex` ("Messages helped only under fixed storage, not where routes cross in general") still use the idea. Their wording waits for the author.

**Model change.** None. Wording only.

### [A101] Background and Related Work rewritten, Pham and Bera corrected

**Where.** `3.Background.tex`, all of it. `references.bib`, five new entries. Tagged `% [A101]`.

**What.** Review `readability_review/review_background_related_v2.pdf`, approved 2026-11-18. The Background explains ideas only. It has no sentences about this thesis and no forward references. Subsection "Multi-Agent Reinforcement Learning" is now "Reinforcement learning", with many agents in its last paragraphs. Each paper is described once, in the Related Work, with what it found and what it leaves fixed. Wang (2009) is dropped. The weak sources are replaced: Reyes et al. (2019) for the company blog, Ma (2022) for the teaching handout and for NP-hardness (both costs), Hardin (1968) for the CoMSES page. The knapsack textbook and Y. Li et al. (2023) are gone. New entries are Q. Li et al. (2020), Q. Li et al. (2021, MAGAT) and Z. Ma et al. (2021, DHC). Their text follows their arXiv abstracts. The bib data comes from Crossref.

**Pham and Bera, correcting [A55].** [A55] said they never test their policy without messages. Their ablation (Fig. 5, Table II) does. In an 80 x 80 world with 4 agents, success falls from 85% to 79% without messages and to 75% without the crowd reward. The fair criticism is one test setting and baselines copied from earlier papers. The thesis's on/off test of messages (RQ4) is still a clean comparison, but not the first one.

**Open.** Two TODOs in the chapter. Weidinger et al. and Merschformann et al. need one sentence of result each, and their abstracts must confirm that traffic is not fed back into storage. The last paragraph of the research gap was done in [A102].

**Model change.** None. Wording and sources only.

### [A102] Project Description and the end of the research gap rewritten, RQ4 no longer conditional

**Where.** `2.Introduction.tex` (Project Description, and "drive" in the Introduction), `3.Background.tex` (last paragraphs of `sec:rw:gap`), `3.ProblemFormulation.tex` (two sentences on RQ4), `5.Experiments.tex` (factors paragraph, factor table, Discussion). Tagged `% [A102]`.

**What.** Review `readability_review/review_project_description_v3.pdf`, approved 2026-11-18.
- Scope. The main load is one where every controller *should* keep up. Congestion-aware storage runs at the main load and a higher load, and a sweep of rising loads shows when the gain of demand storage disappears.
- Measures. Order times are compared only when both runs keep up. Otherwise the served share is compared, and it also answers RQ4.
- Questions. The main question drops "graph-based warehouse". RQ2 asks whether closing the loop makes orders faster than demand storage, and whether a fleet that falls behind serves more. RQ3 asks whether the gain grows, shrinks or disappears. The paragraph after the questions keeps only the reason for the percentage. The communication paragraph is cut, its reason moved to the list of factors.
- Expected outcome. Shorter, keeps "coupling" ([A98]). The RQ4 prediction is now that messages help the decentralised controller clear crowding near it and finish more tasks.
- Research gap. Names two results, the controlled comparison of fixed and demand storage first, closing the loop with congestion-aware storage (the thesis's own rule) second.
- RQ4 is no longer called conditional anywhere. The Discussion drops "not where routes cross in general".

**Decisions by the author (2026-11-18).** Keep the main question. The served share in the measures is enough for RQ1 with learned controllers. RQ3 wording fine. Order of the two results as above.

**Model change.** None. Wording only.


### [A103] Problem Formulation up to "Orders and tasks" made readable, pallets, contributions in one place

**Where.** `3.ProblemFormulation.tex` (opening, `sec:pf:env`, `sec:pf:agents`, `sec:pf:storage`, one phrase in `sec:pf:measures`, "Docks without limit"), `4.Implementation.tex` (`sec:method:storage`, `sec:method:resolution`), `2.Introduction.tex` (new `sec:pd-contributions`), `3.Background.tex` (end of `sec:rw:gap`), `5.Experiments.tex`, `A.Notation.tex`, `2.Notation.tex`, `B.Parameters.tex`, `C.ModelDetails.tex`, `E.Load.tex`, `G.StorageValues.tex`, `H.Horizon.tex`, `styles/eqnames.tex`, figures `arrival_storage.png`, `storage_update.png`, `shelf_loop.png`. Tagged `% [A103]`.

**What.** Review `readability_review/review_pf_env_storage.pdf` v4, approved 2026-11-18.
- Contributions are listed once, in a new subsection after the research questions. The expected outcome keeps only the expectations. The research gap ends by pointing to the contributions.
- The Problem Formulation names what it borrows and points back to the Background by number and name ("Section III-A, Storage assignment"). No forward references are added.
- Reachability now says what the code builds. Every warehouse (layout v2, `instances/generator.py`) is well-formed, and so strongly connected. The old sentence said the model asks for less than van Knippenberg's condition.
- The move equation `eq:transition` goes. The action model is said in words, with its name and citation. The penalty argument moves to `sec:method:resolution`.
- `sec:pf:storage` gets a new order: storage state and room, how stock changes, the storage rule and the three rules with the tea example, what the rule reads, the storage update with its example. SKU and room are explained in words. The symbols for stock on its way, `x_0`, `y^ord` and the equations `eq:upd:*` go. `eq:storageupdate` is a signature written mostly in words. `eq:estimates` keeps only the order estimate.
- `D`, `K` and `D + beta K` (`eq:storageobjective`) and the five-period formula of `omega_hat` (new `eq:standstill`) move to `sec:method:storage`.
- "Pallet" replaces "refill" as the name of a batch of new stock, in every chapter and appendix. The verb "refilled" and the labels stay. The code keeps `refill_units`.
- The three tea figures are redrawn in the look of the pygame viewer ([A104]), with short panel titles and a one-line legend.

**Decisions by the author (2026-11-18).** Keep `c(v,w)`. Keep `rho_hat` as a display, since the next equation uses it. Pallet is the only name. The two tea figures may swap numbers. The text follows the code from now on, because the results are run.

**Model change.** None. Wording, order and notation only.

### [A104] The style every thesis figure follows: the pygame viewer decides (Figure style, decided 2026-11-18)

**Where.** All figures drawn by `thesis-progress/scripts/images/`, copied to `thesis/Images/`. First applied to `arrival_storage.png`, `storage_update.png` and `shelf_loop.png` ([A103]).

**The rule.** The pygame viewer of `slap-mapd-coupling` decides how the warehouse looks. Its values are in `viz/theme.py` (`ROLE_STYLES`) and `viz/pygame_renderer.py` (`_PHASE_COLOURS`, `_RANK_STOPS`, `_draw_slots`, `_marker`). They are copied into `base.py` as `PG`, `RANK_STOPS` and `rank_colour()`, so `thesis-progress` does not import the other repo. If the viewer changes, `base.py` follows it.

**The style.**
- **Base.** Every script imports `base.py`: serif text, math in the LaTeX font (`mathtext.fontset = "cm"`).
- **Marks, as in the viewer.** An aisle position is a small white circle with a grey rim (`aisle_node`). A shelf is a square slot, white with a blue rim (`shelf_slot`). A workstation is an orange-filled square (`work_mark`). A dock is a purple triangle (`dock_mark`). A parking endpoint is a green diamond. A shelf and a workstation are both squares, and they are told apart by the fill, white with a blue rim against orange.
- **Stock on a shelf.** The slot fills from the bottom, one band per SKU, the most popular lowest, in the viewer's popularity colours (dark red, then orange, light blue, pale blue). New stock on its way is striped in the put-away colour on top. A slot a put-away reached gets a purple rim.
- **Agents and trips.** An agent has the viewer's colour for what it does: grey when idle, orange on its way to a pick, red on its way to a workstation, purple on a put-away, green when shipping. A trip is a thin line in that colour along the aisles it uses, just beside the edges. A put-away is dashed. When two trips use the same edge they run on opposite sides. No free curved arrows. Named agents are $a_1$, $a_2$, ...
- **Text.** One dark grey for all labels and notes. Panel titles are short names, "(a) Fixed storage", not sentences. The figure carries only the numbers the text uses ("6 edges", "stood still 5 steps", "20/20"). No aisle labels, and nothing the caption already says.
- **Legend.** One line under the figure, plain words (shelf, workstation, dock, aisle), then the SKUs, the fills and the lines the figure uses.

**Why.** The author decided the viewer sets the look, so a figure and a screen of the viewer show the same warehouse. Earlier figures looked machine-made (sentence titles with colons, notes in several colours, curved arrows, legends of eight to ten entries), and the shelf marks differed from figure to figure.

**Redrawn (2026-11-18).** Every thesis figure that draws a warehouse now uses these marks: `arrival_storage.png`, `storage_update.png`, `shelf_loop.png`, `instance_simple.png` (Fig. 1), `instance.png`, `observation.png`, `warehouses.png`, `warehouses_seeds.png` and `workstation_lock.png`. `base.py` `ROLE_MARK` holds the role marks for whole-warehouse drawings, which `m8.py`, `warehouses.py` and `workstation_lock.py` share. One-way edges are blue arrows, as in the viewer. A route takes the phase colour of each leg (orange to the pickup, red to the workstation), and agents in `workstation_lock.png` take their traced phase. `conflicts.png` and `wellformed.png` draw only aisle circles and parking diamonds, which already match.

**How.** Change the script, run it, look at the PNG, then copy it to `thesis/Images/`. Never edit a PNG in `thesis/Images/` directly.

### [A105] "Orders and tasks" and "A task's life" made readable, the stock condition at creation, the standing-still measure explained

**Where.** `3.ProblemFormulation.tex` (`sec:pf:storage` four paragraphs, `sec:pf:tasks` and `sec:pf:lifecycle` rewritten, sigma(j) defined in "Direction to the target", one phrase in `sec:pf:scope`), `4.Implementation.tex` (`sec:method:storage`, the tie rule), `5.Experiments.tex` (Discussion, new paragraph "What the congestion measure misses" and a threats item), `6.Conclusion.tex` (Future work, learned storage), `2.Notation.tex` and `A.Notation.tex` (rows of tau_j, s_j, q_i(t)), figures `pickup_rule.png` (new, `pickup_rule.py`) and `lifecycle.png` (redrawn in the viewer style, [A104]). Tagged `% [A105]`.

**What.** From the author's red comments on the PDF of 2026-11-18, through a review PDF approved and applied the same day and then deleted.
- `sec:pf:tasks` tells one story: orders, sections, from order to tasks, three kinds of task (new `tab:taskkinds`), the task, promised stock, the pickup rule with `fig:pickuprule`, the stock condition, congestion-aware storage (new `tab:rules`), running out.
- Reasons added for drifting popularity, sections (logic only, the step 12 sweep stays in its appendix), one workstation per order, reservation, and an agent carrying any amount.
- "Pickup vertex" is dropped. s_j is "where the task picks up", a shelf, dock or workstation by kind. The notation table says "pickup place", the word of the Background.
- Ma et al. (2017) cited for the task (s_j, g_j), and for the service time. Release time, SKU and amount are the thesis's own.
- The tie rule (lower vertex number first) moves to the Implementation chapter.
- The online shop sentence and "tally" go. "Storage layer" goes.
- `sec:pf:lifecycle`: the reason for three stages first, the description list merged into `eq:lifecycle` with names, sigma(j) moved to where it is used, the repeated service time paragraph cut.
- Discussion: congestion-aware storage cannot see detours (only stated, no claim about the learned controllers). Threats: no storage rule is learned. Future work: storage is not learned because of training cost and because two learners make the source of a result unclear.

**Model change.** None. Two places now say what the code does ([code decides], 2026-11-18): the stock condition holds when the pick is created, not at `t_j^released`, since a pick keeps its order's release time when its line waited for stock. A line short of stock takes what there is and only the rest waits. `hat omega` counts every step a pick stands still, whatever the reason.

**Follow-up the same day (author asked to check flow and the appendices).** Wording only. Two repeats cut (popularity said twice in the order paragraphs, the wait-for-an-agent reason said twice in `sec:pf:lifecycle`). `q` named before `eq:pickuprule`. The goods-to-person sentence moved before the order's path. "The same number" in the congestion-aware bullet named. "Has to stand still" became "stands still", to match "whatever the reason". Appendices: `F.Demand.tex` (a line gives one pick or more, "storage layer" gone), `D.Warehouses.tex` (the flow paragraph told in order, without "First, Second", and a short line takes the rest from the next storage vertex), both notation tables (`V_str` "shelves", `g_j` "delivery place", the release time of a pick that waited). `D.Warehouses.tex` keeps "storage vertex", since it builds the graph.

### [A106] "Who decides" made readable, the full-view setting removed, one name "controller"

**Where.** `3.ProblemFormulation.tex` (`sec:pf:controllers` rewritten, conflict resolution named in `sec:pf:agents`, `fig:crowding` new in "How crowded the neighbourhood is", the state in `sec:pf:game` points back, one sentence on `pi_theta` after `eq:objective`, `sec:pf:coupling`, `sec:pf:measures`), `4.Implementation.tex` (opening, `fig:methodloop` caption, `eq:credit` paragraph, `sec:method:reference` now "A reference point"), `5.Experiments.tex`, `6.Conclusion.tex`, `2.Notation.tex` and `A.Notation.tex`, `B.Parameters.tex`, `J.Training.tex`, `L.Results.tex`, `styles/eqnames.tex`, figures `controllers_window.png` (redrawn without delta, short titles) and `crowding.png` (new, `crowding.py`). Tagged `% [A106]`.

**What.** From the author's red comments on the PDF of 2026-11-18, through a review PDF approved and applied the same day and then deleted.
- `sec:pf:controllers` in one order: what a controller decides, what the three share (one assignment rule, conflict resolution, the kind of network, the budget), the state `s_t` defined before use, then centralised, section-based and decentralised once each, with short paragraph headings, and the table and figure last as a summary. The Assignment column of `tab:information` goes.
- Forward references to `sec:method:resolution`, `sec:method:controllers`, `sec:method:training` and "the next section" go. "Trained the same way" and "trained only on what it can see" go (method, and the reason is in `sec:method:training`).
- The centralised controller gets the sentence on why it is still central. The collision rule keeps only what differs from `sec:pf:agents`. The claim mask details stay in `sec:method:controllers`.
- The decentralised policy is `pi^dec_theta`, new `eq:decentralisedpolicy`. `pi_theta` in `eq:objective` stays generic, with one sentence naming the three policies.
- Conflict resolution is named in `sec:pf:agents`, "one of the agents waits instead". The order stays in `sec:method:resolution`.
- delta leaves `fig:controllers-example` and gets `fig:crowding` in V-G3. `sec:pf:coupling` and `sec:pf:measures` point to it.
- The full-view setting goes from the thesis, because it was not run. The code keeps `configs/full_view.yaml`.
- "controller" replaces "arm" (33 lines, Experiments and appendices B, J, L, RQ4) and "architecture" where it meant a controller. "Architecture" stays where it means the network.
- The overview before Scope is aligned: `lambda_task` counts order lines (as the code and the notation table), the storage objective and `K` are no longer named in the Problem Formulation, the seeding sentence points back to `sec:pf:tasks`.

**Model change.** None.

### [A107] Small text-to-code fixes in "Choosing together" and "When moves still clash"

**Where.** `4.Implementation.tex`, `sec:method:controllers` and `sec:method:resolution`, `fig:workstationlock` caption. Tagged `% [A107]`.

**What.** From `readability_review/method_controllers_comments.md` (A1, A3, A4, C1 in part) and `method_resolution_comments.md` (A1, A4, B1, C1), applied 2026-11-20 on the author's word to fix small known mistakes. The text now follows the code (rule of 2026-11-18).
- The centralised network runs on every vertex an agent can stand on, not "all vertices" (`arm_windows`).
- The one shared pass is named as Knippenberg's single-agent setup (his Section 6.2).
- The zones are blocks of neighbouring aisles (`zones_by_aisle`). Whether a zone and a SKU section get different names is still open (C1).
- Halo vertices carry every feature and no agent on them chooses in the zone. The old text said they show only role and occupancy and get no move scores. The halo's range keeps a border agent's whole field of view in its window. The old reason, that it keeps the crowding feature the same, did not hold, because crowding is always counted over the field of view.
- "Handled after that agent" cites Knippenberg (Section 4.2).
- "The order priority" and "successor vertex" in the conflict resolution steps become "the priority order" and "the vertex it asks for".
- Only a centralised joint action is always accepted whole. A section-based one can be changed at a zone border.
- The caption of `fig:workstationlock` names the decentralised controller without messages and an earlier run, instead of "test seed 200000".

**Model change.** None. The readability points and the open questions stay in `review_controllers.pdf` and `method_resolution_comments.md`.

### [A108] Small known mistakes fixed by the section and appendix review subagents

**Where.** `4.Implementation.tex` (`sec:method:training`, `sec:method:reference`, `sec:implementation`), Appendices A to L, `styles/eqnames.tex`. Tagged `% [A108]`.

**What.** On 2026-11-20 the author asked for the rest of the Method chapter and every appendix to be reviewed by one subagent each (`readability_review/SUBAGENT_BRIEF.md`), with small known mistakes fixed directly. Each fix makes a sentence, caption, table cell or reference agree with the code, the cited paper or the thesis. The full list, with the evidence for each fix, is under "Fixed ([A108])" in each comments file (`method_training`, `method_reference`, `implementation`, `appendix_A` to `appendix_L` in `readability_review/`). In short:
- Method: "router" becomes "controller"; the critic "sees the same window as its own policy"; a broken `\nref` sentence on the coupling; Token Passing runs under every storage rule and its vertex rule is stricter than Ma et al.'s; the correctness checks run in the test suite and, for conflicts and capacity, at every training step, not "on every experiment"; doubled equation names; a shipment is a task kind.
- A: c_wait is from van Knippenberg; two unused rows removed; the backlog counts order lines; W_T is per pick; omega_i(t) and the waiting-line rule added; `eq:relativeeta` gets a name in `eqnames.tex`.
- B: tables made to fit; gamma 0.99 and the three PPO values cited from Schulman et al.; d_obs 5 from van Knippenberg; 20 test seeds; the main loads 0.09, 0.18, 0.3, 0.6 replace the 3-agent pilot of [A31]; "drift period".
- C: eleven fixes, among them the random docks, the mean over neighbours, the CRAMP feature index, v named in the two masks, Table C.1 matched to Fig. 9.
- D: the shelf count, parking placement, Table D.1 and the Results numbers rerun on the current generator ([A77]).
- E, F, G, H, I, J, K, L: wording that contradicted the served check ([A96]), the pick gain named as pick, references to the right sections, seed and fleet details, typos, column headers that called pick service time zeta-bar.

**Model change.** None.

### [A109] The worst text-to-code mistakes fixed without the author

**Where.** `3.ProblemFormulation.tex`, `4.Implementation.tex`, `5.Experiments.tex`, Appendices A, B, C, F, H, I, J, K, `2.Notation.tex`, `styles/eqnames.tex`. Tagged `% [A109]`.

**What.** On 2026-11-20 the author asked for the worst mistakes to be fixed without them (`readability_review/FIX_BRIEF.md`). The code decides (rule of 2026-11-18). Choices stay with the author and are listed in `method_review_queue.md`.
- **Reward ([A89], [A90]).** The reward text now matches the code. [A89] and [A90] were adopted in the code (`reward_function.py`, on `main`) after the RL review of 2026-11-10, but had no GAPS entry. [A89] makes the potential minus the distance left in the whole task, before pickup the distance to the pickup plus the trip on to the delivery, after pickup the distance to the delivery (new `eq:taskpotential`), so it does not jump at pickup. The observation's distance label is unchanged. [A90] counts progress only within the task served at t. The finishing step ends at potential 0, a new task is never charged, and an idle agent gets no shaping. This replaces [A79]'s "charge once" rule, which made fleet 32 agents stop just before the workstation. Ng's guarantee now holds only within a task. Also corrected: over a route a detour of k steps costs k c_move against k c_wait for waiting, so "yielding is cheaper than a detour" was false, and the section now says who pays the override term under each controller. Places: `sec:method:rl`, one sentence in `sec:method:model`, the Phi row of `A.Notation.tex` and `2.Notation.tex`, `I.Reward.tex`. Left: the code docstring of `reward_function.py` still describes [A79], and `3.Background.tex:109` presents Devlin and Kudenko for a potential that changes over time.
- **Problem Formulation, Experiments, Appendices C and F, facts.** No model change. Every network reads only its own agent's crowding delta_i (PF V-G and C.2.2 had said a zone or the centralised controller reads all its agents' values). The transition kernel also draws the dock of each shipment and put-away at random (PF V-H and the scope item). The backlog counts order lines waiting for stock, not orders. The Zipf weight 1/(r+1) applies within the section of the drawn workstation, so a SKU's overall share is only roughly 1/(r+1) (Experiments, Appendix F). The drift rotates the ranking, so the top SKUs drop to the bottom in one step. The fleet is calligraphic A at PF line 87. `sec:impl:instances` moved from a paragraph to its subsection, so it prints VIII-A, not VIII-A0c. Appendix C cites `eq:standstill` for omega-hat.
- **The lock and Token Passing (`sec:method:resolution`, `sec:method:reference`).** The lock of Fig. 15 is told as it happens in the trace, not as a circle the rule forces. Agents in front of the workstation often choose to wait, and the rule refuses moves onto an agent that stays. When both ask at once they swap and both wait. In the trace both happen (295 of 843 steps contain a circle, 748 refused moves are onto an agent that chose to wait). Who pays, from `reward_function.py`: a refused move costs c_wait + n_blocked, a chosen wait c_wait, and in a circle every agent pays. Messages do not change the credit. The rejected rule is named as the [A91] cap on tasks per workstation, and no back-out rule is added so that learning to back out stays part of what is measured. Why Token Passing never locks (the vertex hold and well-formed warehouses, [A91]) is said once in `sec:method:reference`. The randomness of P includes the random docks. Model and code unchanged.
- **Stall and horizon.** No model change, the code decides. The thesis said a stall is one agent holding a task that stands still too long. The code (`evaluator.py`, D18) flags a run as stalled when the whole fleet goes longer than the stall length after the warm-up without finishing a task. The per-agent stand-still is only a diagnostic, because under Token Passing an agent's waits are often planned. The PF, Appendices H and K and Table B.5 now say this. The stall length stays TBD because no config sets it, so no reported run counts stalls. The evaluation horizon was "2000 or more, open". Every reported test run plays T = 10000 and leaves the first 5000 out (D22), and training episodes are 2000 steps. Appendix H, the Experiments and Table B.5 now give these values. H's figures are not redrawn, their captions say they come from the earlier graph runs of 24 October.
- **Main session.** The Experiments say that m of the rack faces left over become parking and the rest are not built (`generator.py` `_v2_stations_and_slots`, D25), not every leftover face and wall cell. The trip of a shelf at 8 agents is 17 to 38 steps (`eq:shelftrip`, rerun in `results/D_warehouses/instance_report_2026-11-20`), not 11 to 34. Shelf ties in `sec:method:storage` are broken by the plain trip and then by index (`storage/arrival.py` `_refill_scores`), not by index alone. `styles/eqnames.tex` gains names for `eq:relativeeta` and `eq:taskpotential`.
- **Training values.** Code decides. The text called the training values TBD or planned to sweep them, but every trained run uses the same ones: L = 2, hidden and head width 32, minibatch 128, 5 epochs, entropy 0.02, value-loss weight 1.0, one episode per runner, seeds 250/5/20, 500 000 steps on 2000-step episodes, reward weights 10/0.5/0.1, 3 zones. Appendices B and J give these values, "set" where ours by choice and "open, not tuned" for the model and PPO values. No sweep of L, width or PPO values was run, so J's planned sweep tables are removed. J says the loss is RLlib 2.57's PPO loss, which adds an adaptive KL penalty (0.2, target 0.01) and a value-loss clip of 10. Validation uses 5 seeds at the training episode length. Lines per order is 1 + Poisson(4). Safety stock per fleet is 16/18/17/16 from G. The further training of the 16-agent runs (warm start, 2 000 000 steps on 16 000-step episodes) is stated as a fact, not as the policies the results use. `sec:method:training` drops the unused fallback. Not a model change.

**Model change.** In the text only. [A89] and [A90] (the reward) and D18 (the fleet-level stall) and D22 (10000 steps with 5000 left out) were already in the code and are now in the thesis. The code is unchanged.

### [A110] The learned controllers compared on served share, seed by seed, and the chapter reports 16 agents (author approved 2026-11-23, review_seed_spread.pdf v4)

**Where.** `5.Experiments.tex` (Scoring a condition, the results opening, Keeping up, new "Why the count does not follow the mean", `tab:exp:served`, `tab:exp:locks`, RQ1 the controller, RQ2, RQ4, What was expected, Why the learned controllers fall behind, What could have been done differently), new `fig:exp:seeds` (`Images/fleet16_seeds.png` from `thesis-progress/scripts/images/fleet16_seeds.py`), `L.Results.tex` (8 agents opening). Tagged `% [A110]`.

**What.**
- Service time is compared only when both runs keep up on every seed (unchanged). Every other pair is compared on served share, with the paired difference over the same 20 seeds and a 95 % interval. The count of seeds that keep up is a gate and does not rank, because it follows the spread of the seeds, not the mean. Hard seeds are shared by every controller (correlation between runs 0.57 to 0.93) and locks drop single seeds far down. Under congestion-aware storage the three learned controllers cannot be told apart (centralised minus section-based 0.020 [-0.033, 0.073], minus decentralised 0.013 [-0.022, 0.048]).
- Rejected: comparing service time on the seeds where both runs pass, because it keeps only the easy seeds.
- The chapter reports 16 agents. The 8-agent learned results move to Appendix L, because those policies trained only the first budget (500 000 steps on 2000-step episodes, checkpoint chosen on 2000-step runs), while the 16-agent policies were trained again for 2 000 000 steps on 16 000-step episodes. Side by side the two fleets would mix fleet size with training length. Token Passing's 8-agent gain stays in RQ1, since it needs no training (author). The 32-agent columns leave the chapter tables for the same reason (author).
- `tab:exp:served` holds served share and seeds that keep up in two blocks, no brackets.
- The Discussion no longer says the policies trained on 2000-step episodes. It says what the long training did (decentralised congestion-aware 0.66 to 0.80, section-based fixed 0.63 to 0.76), and longer episodes are no longer offered as untried.
- Open: the cells of centralised fixed and demand, section-based demand and with messages under demand and congestion-aware storage are first-run numbers until their long runs are evaluated (`% TODO [A110]`).

**Model change.** None.

### [A111] The keep-up threshold f_up from 0.8 to 0.9 (author approved 2026-11-23, review_seed_spread.pdf v4)

**Where.** `3.ProblemFormulation.tex` after `eq:throughput`, `E.Load.tex` (`app:cal:load`, conclusion), `B.Parameters.tex`, `5.Experiments.tex` (Keeping up, The load). Tagged `% [A111]`. Code: `keep_up_threshold` in the configs (author's PR), `served_counts.py` `F_UP`.

**Why.** 0.8 came from the 630-step pilot of [A31], where the tasks under way at the end were a large part of the run. Under the [A96] count the tasks under way at the start and at the end roughly cancel, and a steady fleet serves about 1.0. Token Passing on the test seeds: lowest seed 0.947 at 8 agents, 0.954 at 16, all 120 runs pass 0.9. At 0.8 the learned seeds that pass still grow their queue by 38 to 101 tasks over the measured steps (orders 1200 to 1700 steps), so "passing means steady" was false for them. At 0.9 their passing seeds stay within -28 to +14 tasks. With the served count, 0.9 gives back Appendix E's capacities (0.15, 0.3, 0.5, 1.0, served_check rows), so the main loads stay at 0.6 of capacity, and the Discussion's "about 0.5 of capacity" goes. 0.95 is too tight (Token Passing's put-aways reach 0.954).

**No rerun.** Every row stores the pick and put-away shares, so keep-up is recounted. The checkpoint choice ([A60]) recomputed at 0.9 from the validation rows picks the same checkpoint for all seven evaluated long runs. The calculation was checked: `served_counts` matches `eq:throughput`, and arriving minus finished work matches the measured queue growth (correlation 0.986 over 140 long-run seeds).

**Open.** Capacity also needs every lower tested rate to pass at 0.9. Played again on Kaggle (`slap-load-sweep-low`, 2026-11-23), `% TODO [A111]` in Appendix E. Appendix L's keep-up columns are recounted when its tables are rebuilt with the long runs.

**Model change.** The value only.

### [A112] Shipments are created only when their order is complete, a known limit (author approved 2026-11-23)

**Where.** `5.Experiments.tex`, Threats to validity. Tagged `% [A112]`.

**What.** A ship task is created when the order's last unit reaches the workstation (`_ship`, `multi_agent_env.py`). A fleet that falls behind owes shipments that are not counted yet, so its served share reads high, the same fault [A96] fixed for lines waiting for stock. Estimated from the rows at about 0.01 for the best learned runs and 0.05 for the weakest. Measured on 2026-11-23 by a replay of the order stream alone (`~/thesis_runs/shipment_range_2026-11-23/replay.py`, merged code, one row per test seed in `runs11/rows.jsonl`, `comm_cng_ckpt2_rows.jsonl`, `token_passing_rows.jsonl`). The estimate was low. The learned runs at 16 agents lose 0.04 to 0.08 of their pick share, and a run keeps up on at most two fewer of its 20 test seeds (section fixed and congestion-aware 6 to 4, comm congestion at checkpoint_000002 6 to 6). The ranking per storage rule stays, except that centralised and section become equal under fixed storage (0.709 each). Token Passing loses under 0.01 and keeps up on 20 of 20 at both ends in every regime. Centralised demand follows once it is evaluated. Counting one shipment per arrived order is not applied to the finished runs, so all runs keep one count. It is the fix for later work.

**Model change.** None.

### [A113] No controller sees orders, and deadlines on orders as future work (author 2026-11-23)

**Where.** `5.Experiments.tex`, new paragraph "Orders are not seen" and an item in "What could have been done differently". Tagged `% [A113]`.

**What.** Checked in the code. The assignment rule hands out the oldest waiting task to the nearest free agent (`controllers/assignment.py`), the network chooses only moves and sees no order or task age (`environment/observation.py`), the reward pays every finished task alike (`reward_function.py`), and Token Passing takes the task nearest to its agent (`planners/token_passing.py`). So no controller favours finishing an order, while the result is order service time. A first step needs no deadline, an assignment rule that finishes started orders first (author). Future work after van Knippenberg et al. (2021, Section 4.1, Table 1, checked): a deadline per order, an earlier deadline per task derived from it, assignment by least time to spare, the time left as an agent feature, a cost per late step.

**Model change.** None now. The scope already excludes deadlines.

### [A114] One training setup, each storage rule with its own policy (author approved 2026-11-23, review_training_setup.pdf v3)

**Where.** `sec:method:training` (`4.Implementation.tex`), `5.Experiments.tex` (Training paragraph and its mockup, Run plan, training results mockup and `fig:exp:learning`, RQ2, the training-time row), `J.Training.tex`, `L.Results.tex` (`app:results:regime1` and `tab:app:regime1:16` removed). Tagged `% [A114]`.

**What.** Replaces [A56] on the training setups. The thesis reports only policies trained under the rule they are tested with, and does not mention the other setup. The fixed-trained test (Regime 1) is dropped. Its rows and the removed text are kept in `thesis-progress/results/dropped/regime1_fixed_trained/`. The RQ2 claim that the gain comes with training, not the rule alone, rested on that test and is cut.

**Why.** The results already used this setup. The Regime 1 rows came from the old 500 000-step policies, the research questions do not need them, and one training run per rule could not separate rule from training anyway. Rejected: rerunning Regime 1 on the long policies.

**Model change.** None.

### [A115] Names: SKU category, W_1, h(k) without hat, v*_i(t), N_t, v_(i) (author approved 2026-11-23)

**Where.** `thesis/Chapters/3.ProblemFormulation.tex`, `thesis/Chapters/4.Implementation.tex`, `thesis/Chapters/5.Experiments.tex`, `thesis/Chapters/2.Notation.tex`, `thesis/Appendices/A.Notation.tex`, `thesis/Appendices/B.Parameters.tex`, `thesis/Appendices/C.ModelDetails.tex`, `thesis/Appendices/D.Warehouses.tex`, `thesis/Appendices/E.Load.tex`, `thesis/Appendices/F.Demand.tex` (rename words only), `thesis/Appendices/G.StorageValues.tex`, `thesis/Appendices/K.Checks.tex`. Tagged `% [A115]`.

**What.** Seven naming points.
1. The group of SKUs served by four workstations is a *category*, not a section, in prose, captions, tables and the notation table. The section-based controller, $\pi^{\mathrm{sec}}$, zones $Y_q$, document sections and all labels keep their names.
2. The workstation of `fig:workstationlock` is $W_1$, as in the Problem Formulation examples. The image still prints $w$ and is redrawn later.
3. A SKU's category is $h(k)$, and the hat $\hat h_t(k)$ is dropped. An order draws its workstation first and takes lines only from that workstation's category, and a refill only follows a line, so the demand rules' estimate always equals $h(k)$ when used (`multi_agent_env.py`). The text says the demand rules learn $h(k)$ from the SKU's first order line. `eq:tripdistance` uses $h(k)$ for every rule.
4. The current target `eq:currenttarget` is $v^{\star}_i(t)$, so $\eta_i(v,t) = d_G(v, v^{\star}_i(t))$. $q$, $q_j$, $q^{(i)}$ and the zone index $q$ are unchanged.
5. The backlog is $N_t$, split at the horizon into $N^{\mathrm{pick}}_T$ and $N^{\mathrm{put}}_T$. The sets $\mathcal{Q}_t$, $\mathcal{B}_t$, $\mathcal{C}_t$ and $N^{+}(v)$ are unchanged.
6. The pickup rule lists the shelves as $v_{(1)}, v_{(2)}, \dots$, and $V = \{v_1, \dots, v_{|V|}\}$ keeps its numbering.
7. $s$ is unchanged.

**Why.** A SKU "section" was confused with zones, with the section-based controller and with document sections. $w$ was both the vertex a move leads to and the workstation of Fig. 15, a page apart. The hat warned of a guess that is never wrong in the runs. $q_i(t)$ was a place among $q$ letters meaning units. $B_t$ and $\mathcal{B}_t$ met in one formula. $v_1$ meant both the first vertex of $V$ and the nearest shelf.

**Model change.** None, names only. The code keeps its identifiers (`sku_sections` etc.).

### [A116] Appendix F rewritten: order gain beside pick gain, the three runs in order (author approved 2026-11-23, review_appendix_F.pdf v2)

**Where.** `Appendices/F.Demand.tex` (whole appendix), `Images/app_demand_sweep.png` (from `thesis-progress/scripts/images/appendix_load.py`, `demand_sweep()`). Tagged `% [A116]` at the top and in the Summary, Setting and Conclusion.

**What.** The order gain, the thesis result, is reported beside the pick gain (new `tab:app:demandgain`: 14.1, 17.5, 17.7, 14.6 percent against 10.9, 13.9, 13.2, 10.2 at 8 to 64 agents). The pilot, the initial run, what changed and the updated run are told once each, in order (new labels `app:demand:first`, `app:demand:changes`; `app:demand:sweep` now on the updated run). The Setting says what demand is with categories (1, 2, 4, 8 categories; at 8 agents one category served by every workstation), states the test length and what it means for a drift period of 400. The Zipf law, its exponent and the drift are stated as the thesis's own, with Silva et al. (2020) as an example of class-based skew. Uniform demand is "expected to gain little, not run". The keep-up of these pre-[A96] rows is argued, not rerun: the earlier count is never above the served share (apart from at most 0.35 percent waiting lines) and the lowest seed is 0.92. Numbers recomputed per seed (eq:relgain): initial run 32 agents 6 not 5 percent, put-away cost 9, 12, 13, 14. The figure shows order gain, pick gain and put-away cost in percent, no keep-up row. The 8-agent single category does not explain a smaller gain (travel cut 21.8 percent, as large as at 16 and 32), and the text says the runs do not say why. The sentence that an order gains more because its lines come one after another was dropped (not measured).

**Why.** Review of 2026-11-20 (`appendix_F_demand_comments.md`): F read the pick while the thesis result is the order, mixed the runs and repeated the pilot. Pilot rows restored from the Trash to `thesis-progress/results/F_demand/pilot_2026-10-17/`.

**Model change.** None.

### [A117] Appendix G: the 32 and 64 agent rows of the [A93] rerun merged (author approved 2026-11-23)

**Where.** `Appendices/G.StorageValues.tex` (`app:cal:period` congestion sentence, `app:cal:beta` sentence and `tab:app:beta`), `thesis-progress/results/G_storage/fleet_{32,64}/storage_rule.{congestion_weight,epoch_length}/`. Tagged `% [A117]`.

**What.** The tp-a93 rerun (finished 2026-11-14) is merged for fleets 32 and 64 the same way as 8 and 16: `congestion_weight` replaced, `epoch_length` congestion rows replaced with `merge_a93_period_rows.py`, fixed and demand rows kept. Checks: demand rows match the period-100 demand rows on all 20 seeds, period-100 congestion rows match beta 1 on all 20 seeds, the computation reproduces the 8 and 16 rows exactly. Table G.2 gains 32 (2.1, -5.1 ± 2.8, +1.3 ± 0.9, +0.2 ± 2.4, +0.5 ± 2.3) and 64 (2.4, -5.3 ± 2.6, +1.0 ± 0.6, +0.1 ± 1.6, +1.5 ± 1.7). Two sentences change: a pick stands still 1 to 2.5 steps (not under 2), and the cut in standing still by period is 3 to 6 percent up to 200 steps and 1 to 3 at 400 from 16 agents on, with no pattern at 8. The conclusion holds at every fleet: congestion-aware storage is no faster than demand storage under Token Passing.

**Model change.** None. The previous rows stay in the git history of thesis-progress.

### [A118] The stall length: 36 order lines' worth of arrivals at the main load (author approved 2026-11-23)

**Where.** `3.ProblemFormulation.tex` (stall paragraph of the measures), `B.Parameters.tex` (`tab:evalparams` stall row), `H.Horizon.tex` (Summary, Method, `app:cal:stall`, Conclusion, new `fig:app:standstill`), TODO in `L.Results.tex`. Code: branch `fix/stall-length` (worktree `~/worktrees/stall-length`, from origin/main 2cce82e, uncommitted): `stall_length` in every `configs/fleet_<m>/*.yaml`, passed through `training/spec.py` to `ExperimentConfig`, comment in `core/experiment_config.py` fixed, test in `tests/unit/test_training_spec.py`. Tagged `% [A118]`.

**What.** A stall is a stretch after the warm-up in which no agent finishes a task (model revision D18, `longest_completion_gap`) longer than the stall length. The stall length is 36 / lambda_task steps: 400, 200, 120 and 60 at 8, 16, 32 and 64 agents.

**Why.** The author kept the stall at 200 steps. Checked against Appendix H's rule (above the longest stretch of a healthy Token Passing run at the main load): Token Passing reaches 316, 114, 53 and 12 steps (F_demand demand.skew rows at skew 1, 40 runs per fleet), so 200 would call 12 of 40 healthy 8-agent runs stalled. A light load leaves longer quiet stretches, so the length is counted in arriving work. 36 lines gives 200 at 16 agents and clears every fleet. At 16 agents 33 of 220 learned test runs stall, none of which keeps up. Rejected: one length in steps for every fleet. Stalls are counted from the stored rows, no rerun.

**Model change.** A value only (was TBD). No run changes; `RunMetrics.stalled` was None in every row.

### [A119] Claim mask swap clause, the halo's source, the reading of the priority sign, Fig. claim mask (author approved 2026-11-23, review_controllers.pdf questions)

**Where.** `4.Implementation.tex` (`sec:method:controllers`, the claim mask and section-based paragraphs, new `fig:claimmask` from `thesis-progress/scripts/images/claim_mask.py`), `3.ProblemFormulation.tex` (where u_{\prec i}(t) is introduced), `references.bib` (`zheng2020distdgl`). Tagged `% [A119]`.

**What.** The claim mask keeps its three conditions, as the code does (`environment/spaces.py` `claim_mask` calls `move_blocked`), and the text adds that a swap never arises inside one decision, because the earlier agent could not move onto an agent that had not chosen yet; the swap rule works in conflict resolution. The figure shows zone Y_2 with its halo and the two cases that can fire. The halo is cited to the HALO vertices of DistDGL (Zheng et al. 2020, Section III-B, checked in the arXiv PDF, now in `papers/`), with the width as the thesis's own (the field of view). The sign of the priority order is read once as "comes before" instead of renaming it.

**Why.** Questions 1 to 6 of `review_controllers.pdf`: zones and categories settled by [A115], d_obs = 5 already cited to van Knippenberg et al. Table 5, the mean's reasons kept, the halo needed a source ([A6] called it standard with none), the figure asked for, border overrides kept as a cost of deciding in zones (Discussion list).

**Model change.** None.

### [A120] "Choosing together" reworded from review_controllers.pdf (author approved 2026-11-23)

**Where.** `4.Implementation.tex`, `sec:method:controllers`. Tagged `% [A120]` with the point of `method_controllers_comments.md` it answers.

**What.** Text about the text dropped (D4). The override sentence of the claim mask paragraph now lives only in `sec:method:rl` (D1). "Seeing the whole window" becomes "What the larger window adds": what the mean covers per controller, that it is the readout of Gilmer et al. (2017) in its simplest form, why a mean (same size for any window, no dependence on numbering), and that a centralised agent sees its neighbours in detail and the rest only as an average, so what sets it apart is the earlier choices near it, the claim mask and the shared credit (B1, B2). Zones are blocks of neighbouring aisles as equal as the aisles allow, not a SKU category (C1). The sentences on entering the next zone and on p = 1 are cut (D2). A section-based agent can be overridden at a zone border, a cost of deciding in zones that the comparison keeps (B4). The closing paragraph names the credit as a difference between the controllers (D3). "All vertices" stays, since every vertex can be stood on (author).

**Model change.** None.

### [A121] Experiments: how the tested checkpoint is chosen (author 2026-11-23)

**Where.** `5.Experiments.tex`, Training paragraph. Tagged `% [A121]`.

**What.** Two mockups ("levelled off, judged by criterion" and "which checkpoint is evaluated") replaced by the rule already in Appendix J (`app:cal:checkpoint`, [A60]): a checkpoint every three iterations, each on 5 validation seeds, the shortest mean pick service time among those that keep up on every validation seed, else the highest throughput, only that one tested. The training return is not used. From `review_evaluation_setup.pdf` 2.1, the rest of which is out of date (moved to done/).

**Model change.** None.

### [A122] The two legs of a shelf's trip are weighted by how often they are walked (author approved 2026-11-23, review_trip_legs.pdf v3)

**Where.** `4.Implementation.tex` (`sec:method:storage`: the trip paragraph with the tea example, `eq:storageobjective`, fixed, demand and congestion-aware storage, `eq:storagegreedy`), `C.ModelDetails.tex` (`eq:tripdistance` now the two legs, overflow sentence), `A.Notation.tex` (rows for the pallet rate and the two legs), `styles/eqnames.tex` (name "the two legs"). Tagged `% [A122]`.

**What.** The text follows the code (`storage/arrival.py`, `_refill_scores`, `leg_weighted_distance`). The workstation leg d^work(k,v) is weighted by the lines of the SKU per step, the dock leg d^dock(v) by its pallets per step (units ordered per step over Q), and congestion-aware storage adds beta times the standing still to the workstation leg. The unweighted trip distance d^trip(k,v) is gone; Appendix D keeps its plain trip d^trip(v), which breaks ties. Fixed storage sends a pallet that misses its home shelf by the same weighted legs; the ratio of the weights is about Q over units per line for every SKU, so fixed storage still favours no SKU. Overflow at 16 agents: about 8 percent of arriving units under Token Passing, 40 to 60 percent under the learned controllers. The sentence that a SKU is put away about as often as it is picked is removed (a SKU is picked about three times as often). The "SKU with no line yet" case is left out, since it never happens in the runs.

**Why.** Review of 2026-11-20 (`method_storage_comments.md` A1): text and code differed, and from 2026-11-18 the code decides because every run used it.

**Model change.** None, text only. Follow-up: draw the tea example on `fig:storageexample`.

### [A123] Method opening, storage and assignment reworded, lost pallets reported (author approved 2026-11-24, review_method_storage.pdf v4)

**Where.** `4.Implementation.tex` (opening of `sec:method`, `fig:methodloop` caption, `sec:method:storage`, `sec:method:assignment`, the halo sentences of `sec:method:controllers`), `3.ProblemFormulation.tex` (`sec:pf:storage`: the arrival-only reason, fixed-storage overflow, "greedy" removed, the lost pallet, `tab:rules`), both notation tables (epoch to update), `5.Experiments.tex` (Results "Keeping up", Discussion "What could have been done differently", mock-up "storage periods"), `E.Load.tex` (`app:load:validity`), `L.Results.tex` (new `app:results:lost`, `tab:app:lost:16`). Figure `scripts/images/methodloop.tex` redrawn in greys. Tagged `% [A123]`.

**What.** Two comment sets in one go (the pasted ten points and `method_assignment_comments.pdf`). The six-step list becomes prose and the figure stays; Token Passing chooses its own tasks is said in the loop. What the Problem Formulation already says is not repeated in the Method (only the controller differs, the three rules, stock stays, few picks per period, the pickup rule, arrivals the same, the K reason). "Order" of a rule becomes "ranking". beta is explained after `eq:storageobjective`, and D + beta K moves from the display into the sentence. "Greedy" is said once, in the Method. Five readings are a practical smoothing choice, not tuned. Ties in one place. The arrival-only reason and the pilot numbers move to the Problem Formulation. Assignment is held fixed on purpose and out of scope, "nearest" is to where the task picks up, an example on Table I, and the put-away priority goes to the Discussion. With p = 1 the section-based controller is the centralised one (undoes the cut of [A120] D2, at the reviewer's request). A pallet that fits on no shelf is lost, its units are not ordered again (code: `_put_away`, `refill_amounts`). A SKU's category is always known by its first pallet, since a pallet needs Q ordered units.

**Lost pallets.** Token Passing loses none at the main load (460 storage-sweep runs at 16 agents). The long 16-agent learned runs lose up to 15 percent of arriving units (decentralised, fixed). Rows and script in `thesis-progress/results/L_results/lost_units/`. Appendix E's rule (zero failed placements at the main load) was checked with Token Passing only, and now says learned losses are reported, not used to drop a setting.

**Model change.** None, text only. Open: centralised demand in `tab:app:lost:16` and the Results sentence once it is evaluated.

### [A124] "How an agent chooses its move" reworded, three figures redrawn (author approved 2026-11-24, review_method_model.pdf v3)

**Where.** `4.Implementation.tex` (`sec:method:model`, `fig:architecture`, new `fig:distancedifference`, `fig:edgescore`), `5.Experiments.tex` (two threats to validity), `6.Conclusion.tex` (future work, memory), `D.Warehouses.tex` (trip lengths at 16 agents), both notation tables (row of the vertex message removed, SCORE row reworded). Figures `scripts/images/architecture.tex`, `edgescore.tex`, new `distance_difference.py`. Tagged `% [A124]`.

**What.** Part B of `method_model_comments.md`. Message passing over graph convolution gets its reason in one clause (a vertex weighs a neighbour by what is on it, Appendix C). Messages have no layer of their own, the thesis's own choice: CRAMP needs a separate network because its agent state comes from an image network, here the agent vector already comes from message passing, so a message is one more round along the communication graph, the mean collects and the move score learns ("adds no power" removed). Vertices hear neighbours, agents send messages. AGG is written as mean, the vertex message symbol is replaced by xi_j of the agent on w (zero when empty). The relative label display moves to "Distance as a difference", with a new figure of the two numbers. The 50 is the thesis's own round number (van Knippenberg et al. give the raw distance, checked in the paper); at 16 agents the longest trip is about 48 steps (instance report 2026-11-20), the label is one leg so stays below 1. No memory: training cost and the network is not the focus; that it may favour controllers that see more goes to threats, memory (LSTM) to future work. Slot order explained. Figure 13 keeps both halves in greys with the words of the text; Figure 14 in words, agents in viewer colours; Appendix C keeps its compact figure whole.

**Model change.** None, text only. The review PDF quoted 41 and 75 steps from the older step-12 instance report; the thesis uses 48 and 86 from the 2026-11-20 report that Appendix D already follows.

### [A125] "Choosing together" trimmed to what the Problem Formulation does not say (author approved 2026-11-24, review_method_controllers.pdf)

**Where.** `4.Implementation.tex` (`sec:method:controllers`), `5.Experiments.tex` (Discussion, "What was expected"). Tagged `% [A125]`.

**What.** The rest of `method_controllers_comments.md` (B2, B3, B4, C1, E1 were done in [A119] and [A120]). D4: one run per agent is said in the PF, the Method keeps only that runtime grows with the fleet. D1: the three claim-mask cases are the PF rule, so the mask is only named and introduced. D2: the section-based paragraph splits into the zone with its halo and "At the border"; the p = 1 sentence, re-added in [A123], goes again since the PF says it. D3: the closing paragraph is dropped, the PF's "What the controllers share" says it. B1: the Discussion gives a possible reason the centralised controller did not gain the most (detail near the agent, the rest as an average, so it differs mainly by the claim mask and the shared credit). The controller table keeps "the whole warehouse", since it states what the controller may see.

**Model change.** None, text only.

### [A126] "When moves still clash" trimmed, the rule told once (author approved 2026-11-24, review_method_resolution.pdf)

**Where.** `4.Implementation.tex` (`sec:method:resolution`), `scripts/images/workstation_lock.py` (legend). Tagged `% [A126]`.

**What.** The rest of `method_resolution_comments.md` (A3, C1, C2 and the dock draw of C3 were done in [A107] and [A109]). D1: the opening names who can still clash (decentralised agents, agents of two zones at a border) instead of "the masks make each move possible". D2: the list is the rule; the prose keeps only why a fixed rule is needed and that the agent in front is handled first (van Knippenberg et al.); the priority order drawn once per episode is in the PF. D3: an agent whose chain of waiting runs into a circle is never ready (code: `conflict_resolution.py`). C3: "the warehouse is random" instead of P, and the paired-seeds sentence in plain words. C4: "counts towards the mean blocked time" (the doubled equation name). Figure 15 gets parking in its legend; nothing else in the figure changed.

**Model change.** None, text only.

### [A127] "What an agent is rewarded for": reasons and sources per term, n_override, a table of terms (author approved 2026-11-24, review_method_reward.pdf)

**Where.** `4.Implementation.tex` (`sec:method:rl`, new `tab:rewardterms`, one word in `sec:method:resolution`), both notation tables, `B.Parameters.tex`, `I.Reward.tex`. Tagged `% [A127]`.

**What.** The rest of `method_reward_comments.md` (A4 and per-task shaping were [A109]). Opening in words, the numbers +0.9, -0.2, -1.1 moved to the step-cost paragraph with gamma = 0.99 (D1). A table of the six terms with value and source (E). Why shaping: the bonus is far and the target usually out of view; van Knippenberg et al. have none (B1). Delivery bonus: their "complete episode" +10, paid per task here (B2). No collision penalty: collisions cannot happen here; the override term (the thesis's own) stops a refused move from costing the same as a chosen wait (B3). n_blocked renamed n_override (code: override_penalty), omega_i(t) replaced by an indicator in words (C1, C3). Crowding: charged by how full the field of view is, read when the move is chosen, the thesis's own, seeing a crowd does not make it costly (A5, B4). A worked example of a 12-step task (D3). Appendix I: override 0.1 and 0 at fleet 32 did not change the collapse (rl_review_2026-11-10).

**Model change.** None. Names only (n_override), values and terms unchanged.

### [A128] "How the controllers learn": two training stages told as done, the credit group, one critic reason (author approved 2026-11-24, review_method_training.pdf v3)

**Where.** `4.Implementation.tex` (`sec:method:training`, one sentence in `sec:method:resolution`), `J.Training.tex` (training budget), `5.Experiments.tex` ("What could have been done differently"), both notation tables (row `eq:credit`), `references.bib` (`{{Ray Team}}`). Tagged `% [A128]`.

**What.** The rest of `method_training_comments.md`. One shared policy cited to the Background, not RLlib (B2). Seeds split three ways, training, validation, test (C3). Runtime told once (D3). The critic explanation cut (D2). The critic keeps one reason, the window limit holds in learning too; the crowding reason was wrong there (the credit hides the cost, not the critic) and is cut, since the Problem Formulation already says it (A3, D1). The rejected critic named, centralised training with decentralised execution (Lowe et al.) (B3). The credit: "credit group" (the code's word, symbol A_i(t) kept, C2); the joint reward is borrowed from PRIMAL (agents within one field of view, their "no noticeable difference" not quoted); here the group is the agents that chose together; the group is fixed at the start of t (`_start_timestep`); a mean so the credit keeps one agent's reward scale and all controllers share the PPO values (B1). "Training ... is also harder" dropped, no result shows it (B4). "When moves still clash" and the Experiments say "credit", not "reward" (D1).

Training told as it was done, at 16 agents: a first run of 500,000 steps on 2000-step episodes, then a second run from its tested checkpoint of 2,000,000 steps on 16,000-step episodes, the same for every controller and rule. The Method gives reasons from the design only (saves time; episodes longer than the 10,000-step evaluation run). Appendix J gives the outcomes: first-stage policies fell behind; the pilot (decentralised with messages, fixed) broke down within 10k to 20k steps over 100k-step runs and kept learning in the second stage (0.079 to 0.184 tasks per step in training, iterations 1 to 18; test 0.091 to 0.156, served 0.37 to 0.56; checkpoint chosen on 2 validation seeds; budget and episode length changed together). New Discussion item: training from random weights on long episodes, since a weak first run could hold its long run back. The list count "Four more" corrected to "Six more".

**Left out on purpose (author, 2026-11-24).** Five second-stage runs (section fixed, demand, congestion-aware; centralised fixed, demand) restarted on Colab after 144,000 steps from their own checkpoint because of the `resume --gpu` bug, with fresh optimiser state (lr and entropy constant), budget 1,856,000, so 2,000,000 in all. The weights carried over, so "every run is trained the same way" holds. Some second-stage runs are evaluated on 2026-11-25; the text is written as done.

**Model change.** None, text only.

### [A129] Introduction, Project Description, Background and Related Work: each part tells the design once (author approved 2026-11-24, review_intro_background.pdf v1)

**Where.** `2.Introduction.tex` (Introduction, Aim and scope, Research question, Contributions), `3.Background.tex` (MAPF, RL, GNN sections, Related Work `sec:rw:comm-decentral`). Tagged `% [A129]`.

**What.** From `readability_review/Checklist.md`, sections 3 and 4, as corrected on 2026-11-24. Each part gets one job: the Introduction gives the problem, the coupling and what is compared; Aim and scope the factors and the scope; the RQs only the questions; Expected outcome only predictions. The two Introduction paragraphs with the same popular-SKU example merged. "Whole fleet, one zone or one robot" now told once, in the Introduction. The higher-load detail left to RQ2. New Introduction paragraph on messages, so RQ4 is motivated. Aim and scope loses the order and task explanation (Problem Formulation defines them) and the measures paragraph (Experiments sets them out), and keeps what "keeps up" means. A scope paragraph was proposed and then cut (author): `sec:pf:scope` already says homogeneous agents, no humans, no physical model and stored stock never moves. RQ4 reworded to what is tested (author, option 1): "Do learned messages between nearby robots let the decentralised controller serve more of the arriving work, and does that change with the storage rule?" It was "route better than what a robot sees on its own", but the Experiments compare served share with and without messages under each storage rule. The percentage-gain paragraph after the RQs cut, it is nearly word for word the one beside `eq:relgain`. Contributions lose the lead-in (repeats the Problem Formulation opening and `sec:rw:gap`) and item 4 ("results"). Background: CBS in one sentence (nothing later uses it), Deep Q-learning kept as one defining sentence (Related Work uses it twice), CTDE removed (the Method explains it where it is rejected, [A128]), the Tien and Lischka paragraph cut (not cited later, Tien link broken). Related Work: the 47% of MAGAT cut. Kept on purpose: the tragedy of the commons (returns in the Discussion), the 6.3%, the 1024 agents and Pham's switch-off test.

**Open.** Deep Q-learning stays uncited as before. `sec:pf:scope` still says "If RQ4 is not reached", for the Problem Formulation pass.

**Model change.** None, text only.

### [A131] Future work: embedding feedback between storage and routers (author approved 2026-11-24)

**Where.** `6.Conclusion.tex` (`sec:future`, end of the storage paragraph). Tagged `% [A131]`.

**What.** Three sentences after the learned storage policy: storage could read the agents' own embeddings ($\xi_j(t)$, `eq:message`), averaged per shelf over a storage period, as shelf features beside $\hat\omega_t(v)$, and hand the routers a short vector per shelf (stock on its way, room reserved). Modelled out in `ideas/learned_storage_policy.md`, section "Variant: embedding feedback between storage and routers", from `ideas/slap_mapd_embedding_feedback_handoff.md`. Not planned (author). Deadlines from the same conversation left out.

**Model change.** None, text only.

### [A130] Introduction and Project Description, second pass: storage told as the arrival model, Token Passing's role, one name per idea (author approved 2026-11-24, review_introduction.pdf v1)

**Where.** `2.Introduction.tex` (Introduction, Aim and scope, RQ3, Contributions, Expected outcome), `E.Load.tex` (`app:load:method`, the reason for 0.6). Tagged `% [A130]`.

**What.** From the red comments `readability_review/intro_comments.pdf`. "Move stock as demand changes" was a leftover from before [A38]; it now says "place arriving stock by demand", that stock on a shelf stays there, and one sentence each on fixed and demand storage (code: `storage/arrival.py`). The measure moves into that paragraph and is named service time. "Differ only in how much one decision covers" becomes "differ in how much one decision covers", and what each robot sees and whose reward judges it follow from that ([A128]). Token Passing gets its reason: from the paper that defines MAPD, and it needs no training, so it sets the main load. Congestion-aware storage is named in the Introduction; "blocked" is the one name for its signal. "Learned messages", not "short". Aim and scope: "the coupling" and "how fast orders are served"; the main load and why it sits below capacity (from Appendix E); the served share defined again (lost in [A129]). RQ3 "learned" for "trained". Contributions name the three problems, explain the classic score in words with Heskett, say "robots", and limit the pairing to one fleet size. Expected outcome loses its sentence about the text, says service time and robots, and gains the author's RQ4 expectation (messages help under every storage rule). SLAP cited to Reyes et al.

**Why 0.6 (author, 2026-11-24).** It comes from an early Token Passing run that found where the fleet falls behind (the pilot of [A31], 2026-10-14, 3 agents, 6 seeds). At about 0.6 of that point the fleet kept up with room to spare and its agents seldom waited for a task. Written into Appendix E.

**Open.** A sentence on why warehouses and robot fleets matter, before the first paragraph, was offered and not answered.

**Model change.** None, text only.

### [A131] The higher load of the loop test is 0.9 of Token Passing's capacity (Design change, author approved 2026-11-24, review_introduction.pdf question 3a)

**Where.** `E.Load.tex` (`app:load:method`, new display `lambda_high`), `5.Experiments.tex` (`tab:expfactors`, row "load for the loop"). Tagged `% [A131]`.

**What.** RQ2 runs congestion-aware and demand storage at the main load and at lambda_high = 0.9 lambda_capacity, for every controller. The learned controllers are judged there by served share.

**Why.** The rule of [A84], the highest load where every trained controller still keeps up, has no answer: the learned controllers already fall behind at the main load (Experiments, "Keeping up"). So Token Passing sets this rate too. 0.9 sits close to the limit, where the aisles should be fuller, and Token Passing should still keep up because every tested rate below its capacity passes.

**Rejected.** Dropping the higher load (RQ2 at the main load only), and running it for Token Passing alone.

**Revises.** [A84] (its Gap: the higher load).

**Open.** The runs at 0.9 of capacity are not done. The evaluation needs the higher load as one more condition for demand and congestion-aware storage under every controller and Token Passing. The Results then need RQ2 at this load.

### [A132] Introduction opens on why picking matters; the scope sentence on RQ4 not being reached is cut (author approved 2026-11-24)

**Where.** `2.Introduction.tex` (new first paragraph), `3.ProblemFormulation.tex` (`sec:pf:scope`). Tagged `% [A132]`.

**What.** Two sentences of motivation before the two decisions: order picking is the most labour-intensive and costly warehouse activity, up to 55% of operating cost (de Koster et al. 2007, abstract checked on Semantic Scholar 2026-11-24), and in warehouses where mobile robots fetch the goods, such as Kiva systems (Weidinger et al. 2018), how fast orders are picked depends on where the stock sits and how the robots move. The scope sentence "If RQ4 is not reached, the results say nothing about communication" is cut, since RQ4 is answered.

**Open.** The Merschformann et al. abstract could not be fetched, so it is not cited here.

**Model change.** None, text only.

### [A133] Problem Formulation: the model kept, method and evaluation detail cut or moved (author approved 2026-11-25, review_problem_formulation.pdf v1 and v2)

**Where.** `3.ProblemFormulation.tex` (all sections), `5.Experiments.tex` (new paragraph "The gain test" before "Mapping questions to comparisons", one clause in "Scoring a condition"), `2.Introduction.tex` (demand storage sentence), both notation tables (row of $\mathcal{F}$). Tagged `% [A133]`.

**What.** From `readability_review/Checklist.md` sections 5 and 6, checked against the text, plus a second list from the author. P1: the Background named in full once, later "described in the Background". P2: the DSLAP is named first, the pilot numbers (43 %, 25 %) leave the chapter and stay in Appendix G (`app:cal:arrival`), partly undoing [A123]. P3: the capacity example in words, matrix product dropped. P4 option a (checklist 6.3): a storage rule places arriving stock and ranks the shelves a line takes from; $F$ means both parts and $\mathcal{F}$ holds both ("and nothing else" cut); the congestion-aware listing now writes $v_{(i)}$ as in the pickup rule. P5: busy and free said once; what an idle agent does moved from "Direction to the target" to "A task's life", the target section keeps one sentence. P6 and P12: two sentences swallowed by mid-line `%` tags restored ("The centralised policy is", "It looks at the whole fleet and not at one"). P7: forward pointers cut where the Method already holds the content (two forms of the distance label, the crowding weight paragraph, masked moves, the scoring opening); kept only for $R_i$, $\gamma$ and "the reward is given in", which the chapter leaves open on purpose. P8 and N6: the 2/5 crowding example cut, `fig:crowding` carries it. N5: $\zeta_1 = 14-5 = 9$ cut, `fig:lifecycle` shows it. N4: the storage update example in one sentence. P9: subsection "Putting the pieces together" removed, `eq:observation` closes the crowding subsection. N7: crowding subsection titled "for every controller". P10 (checklist 6.1 and 6.2): the prose inventory, the policy/kernel explanation and the sequential-draw repeat cut; the learned policy is the routing rule of a controller, assignment sits in $P$; "only the observation changes" replaced by the three differences of Who decides. P11: the $\Delta$ paragraph trimmed to the trade-off (learning and the sweep table cut). N1: "storage epochs" to "storage updates". P13: full stop after `eq:split`. N2: "queue split" to "service-time split" in `tab:measures`. P14: the gain test, `eq:rqformal`, `eq:relgain` and the 95 % reporting line moved to the Experiments (labels unchanged); the factor paragraph cut (third copy after Aim and scope and `tab:expfactors`); the Experiments' "paired t-test" clause now points to the gain test. P15: scope keeps the boundary only (how to add deadlines or re-tasking cut). P16: about 200 lines of commented-out old text removed (in git). N3: Introduction, demand storage puts stock "on the free shelves with the shortest trips" (code ranks by the dock, shelf, workstation trip [A122]).

**Kept on purpose.** Pickup rule and controller definitions stay in the Problem Formulation ([A123], [A125]); the task-route figure stays (tea task $\tau_1$ reused); the storage-update figure stays (only place a lost pallet is shown); the count examples of the keep-up check stay.

**Model change.** None, text only.

### [A134] Problem Formulation round 2: design reasons to the Method, reporting to the Experiments and Appendix C (author approved 2026-11-25, review_problem_formulation_v3.pdf)

**Where.** `3.ProblemFormulation.tex`, `4.Implementation.tex` (`sec:method:storage`, `sec:method:model`, `sec:method:training`), `5.Experiments.tex` ("Scoring a condition", new paragraph "Stalls"), `C.ModelDetails.tex` (new `app:measures:keepup`). Tagged `% [A134]`.

**What.** R1: action numbering cut from the learning problem (the Method already has it), the four-exit example moved to "Only moves that exist". R2: why messages are learned (a hand-picked message cannot say where the sender heads) moved to the Method's "Messages"; the Problem Formulation keeps that a message is part of the policy. R3: why the field of view is small moved to the Method's model opening; the limit stays. R4: "sharing one policy suits agents that are all alike" cut (the Method's training section gives it). R5: what $\theta$ stands for per controller moved to "How the controllers learn"; the credit difference stays. R6: why every controller reads the crowding feature, the CRAMP source and the appendix pointer moved to "What the network reads"; the chapter keeps that every controller reads only the agent's own value. R7: smoothing of $\hat\omega$ (few picks per period, a shelf with no pick yet reads 0) moved to the Method beside `eq:standstill`. R8: stalls moved unchanged to the Experiments. R9: "the backlog over the run is shown" moved to "Scoring a condition"; the finite-horizon limit stays. R10: the reasons of the keep-up counting and both count examples (900/600, 800/10) moved to Appendix C, `app:measures:keepup`; the chapter keeps each rule in one sentence.

**Model change.** None, text only.

### [A135] Problem Formulation round 3: seams after the cuts, smaller figures (author approved 2026-11-25, review_problem_formulation_v4.pdf)

**Where.** `3.ProblemFormulation.tex`, `4.Implementation.tex` (`sec:method:storage`, `sec:method:model`). Tagged `% [A135]`.

**What.** S1: the storage update now says what a valid placement is, and $\mathcal{F}$ is defined once, in Orders and tasks (placement and ranking, [A133] P4a). S2: `eq:estimates` moved up beside the words on $\hat\rho$. S3: the field of view's limit joined its paragraph (the one-line paragraph under `fig:observation` removed). S4: "so $a_2$ can take its next task once $\tau_1$ is delivered" replaces a "So" that did not follow. S5: the Method's crowding sentences ([A134] R6) get their own paragraph "Crowding" after the vertex features. S6: the reason for smoothing $\hat\omega$ comes before the choice of five readings. G1 to G9: figure widths only (instance 0.6, observation 0.7, storage update 0.6, pickup rule 0.6, crowding 0.45, loop 0.8, arriving tea 0.7, lifecycle 0.85, conflicts 0.85). The chapter ends one page earlier (PDF pages 20 to 42). G10 (removing a figure) declined.

**Model change.** None, text and figure sizes only.
