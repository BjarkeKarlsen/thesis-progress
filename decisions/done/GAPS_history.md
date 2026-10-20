# GAPS history

Superseded `[Axx]` entries, the untagged figure redraw and the closed
checklist items, moved out of `../GAPS.md` on 2026-10-20. Kept for the
reasoning behind the current model. The tags still appear in the chapters
as `% [Axx]` comments next to the entry that replaced them.

### [A21] Field of view counts hops (Design change, superseded by [A25])

- **Where.** `sec:pf:env` (the field-of-view sentence and
  `eq:localsubgraph`, the paragraph after it), `sec:pf:observations` (the
  "anything past" sentence, `eq:commgraph`, `tab:observationexample`),
  `eq:halo` in the Method, and `tab:notation` (new row for
  `d^hop_G`, rows for `H_q`, `d_obs`, `V_i^(d_obs)`).
- **Change.** The field of view, the halo and the communication graph are
  bounded by a new hop distance `d^hop_G(v,w)`, the fewest edges on a
  directed path, instead of the travel cost `d_G`. `d_G` keeps every other
  use (the direction label `eta`, storage distances, assignment). The
  sentence about "earlier drafts" of the model is replaced by the reason
  one depth suffices.
- **Why.** The prose said "hops" while the formulas bounded the cost
  `d_G`, and edge costs are general (the `eta` example uses `c=2`). The
  author chose hops. The field of view describes what an agent can see,
  not what a trip costs, it is read by a GCN whose layers each reach one
  hop further, and the observation figure (`observation.py`) already draws
  it with unweighted hop counts. Under the unit edge costs of the
  generated instances the two give the same sets.

### [A8] Model: two open points for full-graph and zone passes (Gap, resolved by [A29] on 2026-10-13)

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
- **Resolution, as it now stands (2026-10-16, [A32]).** Point 1, one pass
  per agent, now run in priority order with the earlier choices in the
  features. The single pass with each agent's task marked at its vertex is
  rejected because no agent would see another's choice. Before [A32] the
  reason given was that it replaces the vertex features. Point 2, the
  pooled readout stays, and it is also how an agent learns of earlier
  choices further away than `L` hops.

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

### [A40] Put-away distance replaces relocations per update (Design change, thesis text edited 2026-10-18, uncommitted)

- **Where.** `2.Introduction.tex`, the dependent variables, the opening of
  `sec:pf:measures`, "Reported costs" (`eq:relocation` is now `eq:putaway`),
  `tab:measures`, the scope list (two items) and its closing paragraph.
  `4.Implementation.tex`, `sec:impl:logging`. `5.Experiments.tex`, "Scoring a
  condition". Tagged `% [A40]`.
- **What the edit says.** The cost of storage is the put-away distance,
  each placed unit counted with the distance from the nearest receiving
  vertex to its shelf, averaged over updates. Fixed storage pays it too. The
  scope says put-away is not carried by the robots, and stored stock never
  moves, so cold stock can hold the best shelves.
- **Why.** Nothing is relocated any more, and measuring put-away for every
  rule shows what adaptive storage adds or saves.
- **Code.** PR I and J.

## Closed checklist items

- [x] **Figures for [A38].** Done 2026-10-18. `fig:storageexample` is
      `arrival_storage.png`, `fig:dkr` shows D and K only.
- [x] Read the `_gcn` chapters through and rename them over
      `2.Introduction.tex` and `4.Implementation.tex` (done 2026-09-29).
- [x] `2.Introduction*.tex` (well-formedness paragraph) called Token
      Passing and Ma et al.'s centralised baseline "two of the baselines
      this thesis compares against". Done 2026-10-13, see [A28]: Token
      Passing is the one baseline and the centralised mention is gone.
- [x] **Thesis edit for [A28].** Done 2026-10-13. The "Reference baseline"
      paragraph of the Method is rewritten for Token Passing, and the
      well-formedness paragraph says the no-deadlock guarantee belongs to
      its planning and task rule, not to the instance property alone.
- [x] The two TBD rows of [A8] (the η_i encoding and global pooling) were
      decided on 2026-10-13, see [A29].
- [x] Decide the TBD row of [A9], the credit signal. Decided 2026-10-16 by
      [A32]: the mean reward of the agents that choose together
      (`eq:credit`). The row is gone and the code (#163) follows it.
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
- [x] **Guide item 4** in `learning_problem_guide.tex`: the task example
      uses `a_2` and the observation figure uses `a_1`. Cosmetic.
- [ ] **Stock as a placement template** (proposed 2026-10-17, wording waits
      for the author, see `thesis-progress/decisions/done/stock_template_2026-10-17.md`).
      Picks never lower `x_t` and nothing is replenished. The model already
      says so (`2.Introduction.tex:444-447`, `x_t` stays fixed between
      updates) and the code does it (`multi_agent_env.py:276, 394`). But
      `2.Introduction.tex:601-604` and `:1634-1636` still read "if not
      simulated" and "modelled only if stated". Proposal: state the template
      reading where `x_t` is defined. The storage update stands in for
      replenishment and re-slotting, as a warehouse decides where incoming
      stock is put away. Say that the switch is instant and free, which favours
      adaptive storage, and that relocations are therefore reported as a cost.
      Replace both "if" sentences. Cite `WaubertdePuiseau2022DynamicSL`
      (already in `references.bib`), which defines the dynamic SLAP as where to
      store goods "upon entry or reentry into the system".