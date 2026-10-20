# Real centralised and section-based controllers, finding and decision, 2026-10-16 - DONE!

Local note, written before any edit to the chapters or the code. Part 1 records what was found. Part 2 is the decision
still to take, with options and a recommendation. Nothing here is applied.

## Part 1. Finding, the arms as built are not centralised or section-based

### What the thesis as written requires

- Centralised. One controller decides for every agent from the global state, including all agent positions and tasks
  (`2.Introduction.tex`, `sec:pf:controllers`, the sentence "A centralised controller may condition on the global state").
  `sec:pf:game` says that under the centralised controller one network draws all the actions at once.
- Section-based. One network is run per zone on the zone plus a halo, with action heads for the agents the zone owns,
  and ownership passes on entering the next zone (`[A6]`, `eq:sectionpolicy`, `eq:halo`).
- Decentralised. Each agent decides from its own observation with shared weights.
- One learning family, one training budget and one shared task assignment for all.

### What is built

- One RLlib agent per robot in every arm (`training/env.py`, module docstring). All robots map to one shared policy
  (`DEFAULT_POLICY_ID` in `training/config.py`). `ModulePolicy` makes one module call per step for all robots in every arm.
- The centralised policy is a product of per-agent factors that are sampled independently (`eq:centralisedpolicy`,
  `[A3]`). Conflicts are fixed afterwards by conflict resolution.
- `[A29]` runs the network on each robot's own copy of the window, with that robot's own potential `eta_i` in the
  vertex features. The shared pass is "named and not used". The centralised copy covers all movable vertices, the
  section copy covers the zone plus halo, and `arm_windows` (`training/env.py`) builds them.
- So the centralised robot sees every position and only its own target, not the global state including tasks. The
  Introduction still says agents in a window share one graph pass (about lines 1032 to 1038), which `[A29]` removed from
  the Implementation chapter. `4.Implementation.tex` line 186 says "This is the centralised setup of
  `vanKnippenberg2021`", which it is not.
- In effect the centralised arm is the decentralised arm with a very large view. It is a wider window, not a different
  decision-maker. The section-based arm is the same with a zone window.

### Knippenberg (`thesis-progress/papers/knippenberg21a.pdf`)

- Two setups. The multi-agent setup gives each agent a local observation graph that a GCN embeds, with one model re-used
  for all agents (Section 4). This matches the thesis's decentralised arm. Their Table 5 sweeps the observation depth.
- The single-agent setup (Section 6.2) takes the complete graph including all agents as the input to one model, which
  outputs a decision vector for each agent. That is the real centralised setup.
- Table 4. Single against multi at 2048 nodes, 32 agents 13.9% against 63.3%, 64 agents 7.6% against 58.2%. The text
  says both more agents and larger graphs degrade the single-agent setup, and that it is harder to train for different
  numbers of agents. `[A3]` quoted only the graph-size half.

### History

- `e6287ae` created `controllers/` with a centralised planner, a section-based stub and a decentralised wrapper.
  `369bdbf` made the centralised controller prioritised planning with space-time A*.
- Thesis text before commit `f1a3027`. Centralised was prioritised planning over the full graph, agents planned in a
  fixed order, each around the cells reserved by higher-priority agents. Section-based was the same planner run per zone
  with a boundary rule, where a robot whose route crosses a zone edge yields to the zone with fewer agents. Only the
  decentralised arm was learned (`git show f1a3027^:Chapters/4.Implementation.tex`, lines 139 to 152).
- `01143a9` moved the planner out of the controllers. `[A19]` made it a reference baseline. `[A1]` to `[A4]` made all
  three arms learned and the arms "differ only in their window". `[A8]` named both options, one pass per agent or
  Knippenberg's single pass, and `[A29]` chose one pass per agent so the arms would differ only in the window.
- `a32e930` deleted `controllers/base.py`, `decentralised.py`, `registry.py` and `section_based.py`. The old centralised
  planner survives as `planners/prioritised_astar.py`. The section-based file was a one-line docstring and was never built.

## Part 2. Decision, how to build the real centralised and section-based arms

The author wants real centralised and section-based controllers, and the planner idea made learned. The formal design may
break. The adapters and training may be rebuilt where they do not reflect the thesis.

### Centralised, the options

| | How it decides | For | Against |
|---|---|---|---|
| C-A. Knippenberg single-agent | One network, one pass over the complete graph with every agent's target marked, one output vector for all robots, drawn independently | Closest to the cited source. One call per step | No coordination inside the decision, so conflicts are still fixed afterwards. Targets must be marked at the occupied vertex or given one channel per agent, which ties the network to a fleet size. Not the planner idea |
| C-B. Learned prioritised planner | Robots one at a time in priority order. Each sees the graph, its own target and the vertices earlier robots have claimed this step. One network, one team reward | Matches the old text and the planner baseline. Inside the decision there are no vertex or swap clashes, so conflict resolution is not needed. Keeps `eq:features` as written, since one robot is handled at a time. Decision time grows with the number of robots, which is the scaling limit | Sampling needs one sub-step per robot in the adapter. A new feature (claimed vertices) and a dynamic mask. Not exactly Knippenberg. No citation yet for autoregressive multi-agent policies |
| C-C. One joint distribution | A distribution over every joint action | Truly one decision | Exponential in the number of robots, so it fails for any real fleet (`[A3]`) |

C-B reuses most of what exists. Today's per-robot network with a whole-graph window is the per-robot step of C-B. New in
C-B are the claimed-vertex feature, the sequential sampling, the group credit and the dynamic mask. The `team_mean`
code already forms the groups.

### Section-based, the options

| | Rule | Notes |
|---|---|---|
| S-A. Centralised procedure per zone | The same procedure as the centralised arm, run once per zone on the zone plus halo, for the robots in the zone. Zones in parallel. Halo vertices are context only. Cross-zone clashes go to conflict resolution (`[A6]`) | With one zone it equals the centralised arm. Credit is the zone's mean reward. The group changes as robots cross zone edges |
| S-B. Restore the old yield rule | Compare planned routes and yield at the boundary | Needs routes. A one-step policy produces none (the reason `[A6]` dropped it). Not workable under C-A or C-B |

So the section arm follows from the centralised choice. S-A is the only workable form.

### Recommendation

- Centralised, C-B. It follows the author's own planner text, gives the arm a genuine scaling limit, and costs the least
  new code. Use C-A only as a fallback if the sub-step adapter proves too slow, and if so cite Knippenberg's single-agent
  setup directly.
- Section-based, S-A.
- Decentralised unchanged, with learned messages as an option. Messages are a decentralised matter again, since robots in
  one decision unit already share the decision.
- Credit is one team reward per decision unit, the mean over its robots, and the decentralised unit is one robot. This
  follows from the unit and needs no separate setting.

### What changes formally

- `eq:posg` and `eq:obsfunction`. The decision unit is the fleet, a zone or a robot. The claim "three versions of one game
  that differ only in `O_i`" goes. RQ2 becomes how the result changes with the size of the group one decision-maker
  decides for, which also sets what it sees.
- The critic window (`[A13]`) becomes the decision unit's window. The `[A29]` per-robot copy and pooled readout need
  review. The pooled readout may stay or go once the step network sees the claimed vertices.
- The mask of `eq:mask` gains a dynamic part, the vertices claimed by earlier robots in the unit.

### What survives

`eq:objective`, the reward, the shared assignment rule, conflict resolution (now needed only between units), the
decentralised arm and its messages, PPO, the Token Passing and prioritised A* references, and the factor design.

### `[Axx]` entries to rewrite, first pass from the titles

Rewrite or replace. A1, A2, A3, A4, A5, A6, A8, A9, A12, A13, A29. Light update. A10, A11, A14, A17, A19, A27. Only some
of these were read in full, so the list is provisional. The chapters change first, then the entries are rewritten to match.

### Open questions

Status 2026-10-16. 1 to 5 are answered in Part 3 and by the step 0 spike (C-B, the episode priority order, the pooled
readout stays, the full-view setting is kept on a few conditions, the turns work). 6 and 7 are still open. See Part 4.

1. C-B or C-A.
2. The priority order inside a unit. The conflict-resolution order is redrawn each episode. The old planner used the
   earliest assignment time first.
3. Whether the pooled readout stays.
4. What to do with the full-view setting, which is the decentralised arm with a very large view and needs no code. It is the
   one comparison that separates the effect of what a unit sees from the effect of how it decides. Archive with a git tag
   or keep as a setting on a few conditions.
5. Whether RLlib's turn-based multi-agent environment supports the sub-steps. Not verified.
6. A citation for autoregressive multi-agent policies.
7. Training stability of a sequential policy with a team reward at larger groups.

### Risks accepted

- The rebuild strengthens RQ2 and does not help RQ1 or RQ3, the coupling questions.
- It rebuilds the adapter, training and chapters. Any existing centralised or section result is lost.
- On the campaign instance, with 33 vertices and 3 robots, the sequential cost is small. A visible trend needs a larger
  fleet or warehouse.

## Part 3. Decisions taken, 2026-10-16

Taken with the author against the original research goals (introduction, problem statement and RQs of the project
description).

- Research questions. The original "which architecture degrades slowest" question is not used. The commons question is
  removed. Current RQ1 to RQ5 stay, and RQ2 is reworded, since the arms no longer differ only in what they see but in how
  many robots one decision covers.
- Centralised, C-B. Robots decide one at a time and each sees the vertices earlier robots have claimed this timestep.
  The policy is the chain rule over robots, `pi(u_t | s_t) = prod_k pi_theta(u_(k) | s_t, claims of robots 1..k-1)`,
  which represents any joint distribution at a cost linear in m. Candidate citations, not yet verified: Wen et al. 2022
  (Multi-Agent Transformer) and Fu et al. 2022 (auto-regressive policies in cooperative MARL).
- Section-based, S-A. The same procedure per zone on the zone plus halo, zones in parallel, no claims shared between
  zones, cross-zone clashes to conflict resolution. With one zone it equals the centralised arm.
- Undecided occupant. Inside a unit a robot may enter an occupied vertex only if its robot has already decided to leave
  it, and not by a swap. Wait is always legal, so a unit never produces a clash. Conflict resolution is needed only
  between zones.
- Priority order inside a unit. The episode priority order that conflict resolution already uses. No new parameter.
- Credit. Each robot decision gets its unit's mean reward and its own value estimate. The TBD credit row of
  `tab:trainparams` goes.
- Pooled readout stays, since without it a robot sees only L hops of claims.
- Full-view setting kept on a few conditions, as the comparison that separates what a unit sees from how it decides.
- Scaling. Runtime and learning only. Decisions take no simulated time. kappa_T is reported next to throughput. The
  training budget stays equal in environment steps, one step per timestep however many robot decisions it holds. No
  real-time check. Knippenberg's 24-hour wall-clock budget mixes compute speed with learning difficulty, and the
  step budget keeps them apart.
- Open for the code. Whether RLlib's turn-based multi-agent environment supports the sub-steps.

## Part 4. Follow-ups from a review of the decisions, 2026-10-16

- The chain-rule claim. The thesis says any joint distribution can be written as the product. The network sees only
  occupancy and an unlabelled set of chosen vertices, within L hops plus the pooled readout, and only its own target.
  A sentence saying so was added to the centralised paragraph of `sec:method:controllers`.
- Priority means choosing first, not right of way. An earlier agent may not enter the vertex of a later agent that has
  not chosen, so in a corridor the later agent steps aside. A sentence was added after the collision rule in
  `sec:pf:controllers`. It is also why a memoryless centralised policy can break a stand-off.
- RQ2 needs a fleet where the decision sizes differ. With 3 agents one decision covers 3, about 1.5 or 1 agents.
  Decided later on 2026-10-16: the first result uses 8 agents on 94 vertices (8, about 3 or 1 agents per
  decision). The fleet sweep of RQ4 adds 4, 12 and 16 agents.
- Kept as built later on 2026-10-16: the centralised run does not see other agents' targets. Revisit after the
  first result.
- The full-view comparison mixes choosing together with the shared reward. Accepted in `[A32]`.

### Order

1. Take the decision above. Done, see Part 3.
2. Rewrite the chapters, with the author's approval of each section.
3. Rewrite the `[Axx]` entries to match.
4. Code, in small branches with issues. The planners stay as references.
