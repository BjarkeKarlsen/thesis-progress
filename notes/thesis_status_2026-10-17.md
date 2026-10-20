# Thesis status, 17 October 2026

A reading version of the status deck. It says where the thesis stands, what the last three
weeks added, what has been measured, and what comes next. Measured results and inferences are
kept apart, as in the run notes.

## 1. Summary

The model and the code are in place, and the first results are in. Adaptive storage helps the
reference planner on every test seed, and the learned arms are training with it now.

- **Model.** The thesis chapters fix the model. Three learned controllers differ in how many
  agents one decision covers, and storage adapts to demand that drifts over time. One question
  about stock came up on 17 October and has a proposed fix (section 5).
- **Code.** Everything is on `main` at `9b6be93`, after about 80 merged pull requests in three
  weeks. One run trains every arm and measures it under fixed, demand and congestion storage.
- **First results.** Under Token Passing, demand storage raises throughput by 14% at load 0.6
  and cuts service time by 25% at load 0.3, on all 6 test seeds. The learned arms started
  training at 15:16. The decentralised arm finished in 15 minutes, and the rest should be done
  around 18:30.
- **Next.** Decide the pickup rule and the long-run settings this week. The long run then
  answers RQ1 to RQ3, with a proposed target of 21 November.

## 2. The goal

The thesis asks how closed-loop coupling between storage assignment and robot routing affects
service time and congestion in a graph-based warehouse. It splits into five questions.

| question | in plain words |
|---|---|
| RQ1 | Does adaptive storage shorten service time against fixed storage, and which part of it changes? |
| RQ2 | Does that effect differ between controllers that decide for 8, about 3 or 1 agent at a time? |
| RQ3 | Does congestion-aware storage save more blocking and crowding than the travel it adds? |
| RQ4 | How do the effects change with more agents and more orders, and when does the fleet fall behind? |
| RQ5 | Conditional. Does local communication help the decentralised controller? |

A commons question is proposed as RQ6. As the fleet grows, does each agent finish fewer tasks,
and does the loss grow faster when one decision covers fewer agents? It is in `ROADMAP.md`, not
yet in the thesis.

**The loop.** Two layers feed each other. Every Δ steps a storage rule decides which shelves
hold each SKU. Each order is then picked at a shelf that holds its SKU, a controller moves the
robots, and the demand, traffic and waits it produces are counted for the next storage update.
Where stock sits changes the routing problem, and what the fleet does changes where stock goes
next.

**The main instance.** 8 robots on a 94-vertex warehouse with 10 storage and 4 delivery
vertices, 100 SKUs. Demand is skewed (Zipf, skew 1) and its ranking moves 5 places every 200
steps. The starting stock puts the most popular SKUs nearest the delivery vertices.

**The controllers.**

| controller | one decision covers | it sees | role |
|---|---|---|---|
| Centralised | 8 agents, in turn | the graph and earlier agents' claims | learned arm |
| Section-based | about 3 (3 zones) | its zone plus a halo | learned arm |
| Decentralised | 1 agent | its own field of view | learned arm |
| Full view | 1 agent | the whole graph | diagnostic |
| Token Passing | the whole fleet, planned | everything | reference planner |

The three learned arms share one method. They use PPO with one graph encoder family and one
reward, and credit is the mean reward of the agents that choose together. Full view separates
seeing more from choosing together. Token Passing is the reference, not a fourth arm, partly
because it picks its own tasks.

## 3. The last three weeks

About 80 pull requests were merged and the model changes `[A12]` to `[A37]` were logged in
`GAPS.md`.

| dates | what changed | where |
|---|---|---|
| 16 to 17 Oct | Real centralised and section arms. Night run on 8 agents. Demand probe, drifting demand, starting stock in blocks, wait rule. Adaptive storage merged. Short run. | `[A32]`, `[A34]` to `[A37]`, #161 to #174 |
| 12 to 15 Oct | Token Passing as the reference. Wait cost in the reward and keep-up threshold 0.8. First campaign with 3 agents. | `[A28]` to `[A31]`, #117 to #158 |
| 5 to 11 Oct | Runs scored the lifelong MAPD way. Experiments chapter mocked up. Implementation stack merged and checked against the thesis. | `[A20]` to `[A24]`, #51 to #116, #103 |
| 28 Sep to 4 Oct | All three controllers become learned GCN arms. Notation table and figures aligned with the chapters. | `[A12]` to `[A19]` |

The 3-agent campaign is what led to the real centralised arm. The learned fleets stopped at
about 0.21 tasks per step, against 0.267 for Token Passing, and they deadlocked under greedy
play.

## 4. Results so far

### 4.1 Night run, 16 October (measured)

The real arms under fixed storage, 8 agents, load 0.6, 20 SKUs, uniform demand, 500 000
timesteps. Chosen checkpoints, mean of 2 training seeds (1 for centralised, whose second seed
failed), 6 test seeds each.

| arm | agents per decision | throughput (tasks per step) | blocked (steps per task) | runtime (ms per decision) |
|---|---|---|---|---|
| Decentralised | 1 | 0.427 | 2.1 | 7.2 |
| Full view | 1, whole graph | 0.439 | 1.8 | 11.6 |
| Section-based | about 3 | 0.415 | 0.9 | 15.9 |
| Centralised | 8 | 0.365 | 0.04 | 16.8 |

No arm keeps up at load 0.6, on any test seed. Covering more agents per decision cuts blocking
and costs runtime. The centralised arm blocks least but finishes the fewest tasks. Several
chosen checkpoints are early ones, so the arms may not have finished learning, and uniform
demand says nothing yet about adaptive storage.

### 4.2 Demand probe, 17 October (measured)

Drifting demand is what gives storage something to do. With the ranking fixed, the demand rule
gained almost nothing over a good starting stock. With the drift, fixed storage lost about 15%
of its throughput under Token Passing at load 0.6, and the demand rule won most of it back. At
load 0.3 the demand rule cut service time by 27% for Token Passing, and by 44% and 59% for the
night's two decentralised policies, played without retraining. Details in
`demand_probe_2026-10-17.md`.

### 4.3 Short run, Token Passing (measured)

The first attempt of the short run trained no learned arm because Ray's socket path was too
long. It was fixed and rerun the same afternoon. Token Passing played the 6 test seeds under
every storage rule (Δ 100, ν 48, β 3) and reproduced the probe exactly on the 24 rows they share.
Mean over seeds, gains paired seed by seed.

**RQ1.** Adaptive storage helps on every seed. At load 0.6 the fleet falls behind, so throughput
counts. Demand storage takes it from 0.375 to 0.428 tasks per step (+14%), and the backlog at the
end falls from 457 to 350 tasks. At load 0.3 the fleet keeps up, so service time counts.

| part of service time, load 0.3 | fixed | demand | congestion (β 3) |
|---|---|---|---|
| waiting for an agent | 39.16 | 27.70 | 31.10 |
| travel | 12.86 | 11.20 | 11.69 |
| blocked | 0.20 | 0.32 | 0.26 |
| **service time** | **52.22** | **39.22** | **43.05** |

The gain of demand storage is 13.0 steps per task, 95% interval 4.8 to 21.2. Congestion storage
gains 9.2, interval 4.6 to 13.8. Travel falls on every seed, but nine tenths of the gain sits in
the wait for an agent.

**RQ3.** Against demand storage, congestion storage lowers blocked time (6 of 6 seeds at load
0.6, 5 of 6 at 0.3) and raises travel (6 of 6 at both loads). Throughput is lower on every seed
(−0.008 at load 0.6, −0.003 at 0.3), and service time at load 0.3 is 3.8 steps higher. At β 3 the
net effect is slightly worse than demand storage.

**Cost.** Every update moves exactly 48 units, the cap, so the cap binds every time. One episode
moves 960 units, more than the 800 in stock. If robots carried them, the distance would be about
0.7 to 1.0 times the travel the fleet does for its tasks.

### 4.4 What we infer (not measured)

- RQ1 for Token Passing is a clear yes. Both adaptive rules beat fixed storage on every seed at
  both loads, and the intervals exclude zero.
- At load 0.3 the gain is mostly a queueing effect. Token Passing finishes 0.83 to 0.90 of the
  arriving tasks under fixed storage, close to its limit, so a small saving in travel per task
  shortens the queue for an agent by much more. At a lower load the gain would be closer to the
  travel saving alone. This matters for RQ2, because arms that finish tasks at different rates
  sit at different distances from their limit at the same load.
- β 3 is the wrong test value if β 1 is the candidate. The probe's only congestion win was at
  β 1, and only for the decentralised policies, which block more than Token Passing.
- Whether adaptive storage pays depends on the cap. With ν binding at every update, one value of
  ν is one point on a gain against cost curve.

### 4.5 Short run, learned arms (in progress)

The four learned arms train for 10 iterations each (140 000 timesteps, training seed 0) under
fixed storage, then each is measured under all three storage rules at both loads. This gives the
first reading of the gain per arm (RQ2), the arms under fixed storage with runtime, and how far
10 iterations get. It is a first look only, with one training seed and 6 test seeds. The analysis
goes into `short_run_2026-10-17.md` when the run finishes.

## 5. The stock question and the proposed solution

Stock never runs out in the model. A pick does not lower the count at a shelf and nothing is
refilled, so the storage state is a placement template, not an inventory level. The
Introduction already implies this, since the storage state stays fixed between storage updates.

**Proposed reading.** The storage update stands in for replenishment and re-slotting together.
It decides which shelves hold each SKU from the next epoch on, as a warehouse decides where
incoming stock is put away. This matches the dynamic storage assignment problem of Waubert de
Puiseau et al. (2022), already in `references.bib`, which is about where goods are stored "upon
entry or reentry into the system". No new vertices or inbound tasks are needed.

**What needs fixing.**

1. **Wording.** Two sentences in the Introduction still say depletion and replenishment are
   modelled "only if stated". They should state the template reading outright. Clarity only.
2. **Pickup in proportion to units.** Today an order is picked uniformly among the shelves that
   hold its SKU, so one leftover unit at an old shelf keeps half of the SKU's orders there. The
   cap binds at every update, so partial moves are common. Proposal: pick in proportion to the
   units each shelf holds, using the same random number so the order stream stays paired. This
   changes every adaptive-storage result and should be decided before the long run.
3. **Each SKU keeps its units.** The thesis never says a storage update only moves units. It
   holds on today's instance (the stock needs 928 of 2000 units of capacity), but neither the
   thesis nor the code guarantees it. Proposal: state it, and check it in the code after every
   update.
4. **The instant switch.** The new placement holds at once and moves no robot, which favours
   adaptive storage. Report it, and optionally measure the rules with each update applied one
   epoch late.

The full argument, with draft thesis wording, is in `stock_template_2026-10-17.md`. The items
are logged under "Still open" in `GAPS.md`. Two GitHub issues are drafted but not yet opened.

## 6. Where to go from here

A proposed plan for the roughly twelve weeks to delivery. The delivery date, about 12 January
2027, is still to confirm.

| until | phase | what happens |
|---|---|---|
| 24 Oct | Read and decide | Read the short run. Decide the pickup rule and the long-run settings. Thesis wording for stock, the 8-agent instance and the commons question. |
| 21 Nov | The coupling result | Long run, four arms, fixed against adaptive storage. Answers RQ1, RQ2 and RQ3. Then the matched training regime. |
| 12 Dec | Scale | Fleets of 4, 8, 12 and 16 agents (the 12- and 16-agent warehouses exist). Answers RQ4 and the commons question. RQ5 if time allows. |
| 12 Jan | Write | Experiments and Discussion chapters, figures and tables from the runs, a full thesis check before delivery. |

## 7. Results still needed and decisions to take

**Results still needed.** Every comparison is on paired seeds with mean and spread. Service time
counts only where the fleet keeps up, otherwise throughput and backlog.

| question | result needed | have now |
|---|---|---|
| RQ1 | Adaptive against fixed storage per arm, and which part of service time moved | Token Passing only, it helps |
| RQ2 | The RQ1 gains across arms, with at least 2 training seeds | short run training now |
| RQ3 | Congestion against demand storage at β 1 and β 3, blocking against travel | Token Passing at β 3, no gain |
| RQ4 | The same at 4, 8, 12 and 16 agents and several loads | warehouses generated, not run |
| Commons | Tasks per agent as the fleet grows, per arm | reuses the RQ4 runs, wording pending |
| RQ5 | Decentralised arm with and without messages | code in progress (#160) |

**Decisions to take before the long run.**

| decision | proposal | reason |
|---|---|---|
| Pickup rule | In proportion to the units a shelf holds | One leftover unit keeps half of a SKU's orders, and the cap binds at every update |
| Seeds | At least 2 training seeds, 10 to 12 test seeds | One training seed confounds arm and seed, and 6 test seeds give ±8 on a gain of 13 |
| Loads | Add 0.2 to 0.3 and 0.6 | At 0.3 the gain is mostly queueing, and 0.2 shows the travel effect |
| Storage rule values | β 1 and 3, cap of 16 and 48 units | β 3 loses to demand storage, and two caps give a first gain against cost curve |
| Commons question | Add as RQ6, tasks per agent against fleet size | Reuses the RQ4 runs, no extra training |
| Matched training | After the long run, decentralised arm first | Only once the fixed-storage arms are shown to learn |
| Zones | Blocks of consecutive aisles, 3 zones for 8 agents | The sentence is still missing in `sec:pf:controllers` |

## 8. Limits and sources

**Limits.** Every number here comes from one instance. The learned results have one or two
training seeds and 6 test seeds, and the arms are far from fully trained. The Token Passing rows
are deterministic for a seed, so they carry no training variation. The relocation cost is free
in the simulator, and its comparison with task travel is rough because one is in edge cost and
the other in timesteps.

**Sources.**

- Short run note: `thesis-progress/decisions/done/short_run_2026-10-17.md`
- Stock discussion paper: `thesis-progress/decisions/done/stock_template_2026-10-17.md`
- Demand probe: `thesis-progress/decisions/done/demand_probe_2026-10-17.md`
- Run folders: `~/thesis_runs/short_2026-10-17/`, `~/thesis_runs/night_2026-10-16/`,
  `~/thesis_runs/demand_probe/`
- Order of work: `ROADMAP.md`, current state: `SESSION_CONTEXT.md`, model changes:
  `thesis-progress/decisions/GAPS.md`
- Status deck: https://claude.ai/artifact/SRitW5eepWasuMeqUkyF7j
