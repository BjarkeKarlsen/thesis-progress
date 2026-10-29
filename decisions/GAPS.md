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
| [A10] | Computational cost reporting | In force |
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
| [A36] | How a wait is attributed to an edge | In force |
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
| [A49] | Keep-up is throughput against the release rate | In force |
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
- **Open.** The author should confirm `F_fix`-only training as the main result.
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
  `decisions/active/graph_appendix_handoff.md`.

## Still open

- [ ] **Gap: an order's workstation is random, so the storage rules have no
      target.** Found 2026-10-29 in the step 12 sweep, raised by the author.
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
- **Code.** The configs select by `episode_return_mean`. Planned in `active/measures_plan.md`.

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
