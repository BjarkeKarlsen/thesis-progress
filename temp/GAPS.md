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
- [ ] Decide the TBD rows added in [A8] and [A9].
- [ ] Confirm the delivery date (about 12 January 2027) and that the new
      arms match the thesis contract wording.
