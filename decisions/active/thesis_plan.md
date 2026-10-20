# Thesis plan

The main planning document. Written 2026-10-19 from `thoughts.md` (the raw notes, kept as
they are) and checked against the notes it points to. Where `thoughts.md` and a later
decision disagree, this file follows the decision and says so.

Status words used below. **Decided** means the author agreed. **Proposed** means written up but
not agreed. **Open** means a decision is still needed. **Stale** means an idea in `thoughts.md`
that a later decision replaced.

Sources: `short_run_2026-10-18.md`, `arrival_short_2026-10-18.md`, `arrival_storage_plan.md`,
`research_goals_2026-10-18.md`, `thesis-progress/archive/workspace/ROADMAP.md`, `SESSION_CONTEXT.md`, and the chapters
`thesis/Chapters/2.Introduction.tex` and `4.Implementation.tex`.

## 1. The main result (decided 2026-10-18)

The thesis stands on one comparison.

> How much adaptive storage shortens service time, and how that gain depends on how many
> agents one decision covers.

- One comparison. Demand storage against fixed storage, on paired seeds.
- One measure. The paired gain in mean service time with its 95% interval, split into wait
  for an agent, travel and blocked time.
- One factor. The controller. Centralised (8 agents per decision), section-based (about 3),
  decentralised (1). Token Passing is reported next to them as a reference.
- One load, where every arm keeps up on every seed.

This is RQ1 and RQ2 read together. Everything else in the thesis either supports it or marks
where it stops holding.

**Reworded 2026-10-19 (`[A44]`, applied in the thesis). Why.** The RQ1 half does. It is paired,
uses a measure from the literature (Ma et al. 2017), and it held on every seed for every arm
that did not jam. Two parts should be reformulated.
- **The demand rule is not a closed loop.** It reads only the order stream. Under the arrival
  model its placement and put-away are identical for every router, because nothing from the
  routing reaches it. Storage shapes the tasks, but traffic never shapes storage. So demand
  against fixed measures adaptive storage, not closed-loop coupling. The loop is closed only
  by the congestion-aware rule, and at β 1 that rule placed stock as the demand rule did.
  "Closed-loop" in the main question and in RQ1 claims more than the main result shows.
- **"Depends on how many agents one decision covers" is not yet what the data shows.** The
  arms that gained most had the longest and most blocked routes under fixed storage, so they
  had more to save. Each arm saved about a quarter of its route time. Comparing arms on the
  gain in steps rewards the arm that routes worst. The gain as a share of fixed route time
  (travel plus blocked) compares them fairly.

The main result now reads as follows. The Introduction uses "demand-only" to match the
name of $F_{\mathrm{dem}}$ in the Method.

> How much demand-only storage shortens service time, and whether that gain, as a share of
> route time, differs between controllers that decide for one agent, one zone or the whole
> fleet.

The closed loop then becomes the question of RQ3, whether feeding traffic back into storage
adds to the gain. That is honest in either outcome. If the heatmap and the congestion rule
show nothing, the thesis can say that closing the loop adds little here and why (demand
storage did not create congestion to steer around). That answers the question in `thoughts.md` on whether RQ2 should be
folded into RQ1. They stay two questions, answered by one table and one figure. The
`research_goals_2026-10-18.md` proposal adds a "main result" paragraph to the Introduction to
make this visible (proposed, change 1 there).

## 2. How a run is judged

### 2.1 Does the fleet keep up?

This is the first check, and it is already in the thesis (`eq:throughput`,
`sec:pf:measures`). A fleet keeps up when it finishes tasks about as fast as they arrive.

Formally, with $\mathcal{C}_T$ the tasks completed within the horizon $T$,

$$\Lambda_T = \frac{|\mathcal{C}_T|}{T} \ge f_{\mathrm{up}}\,\lambda_{\mathrm{task}}$$

- $\lambda_{\mathrm{task}}$ is the **load**, the expected number of tasks released per
  timestep. "Load 0.2" means 0.2 tasks per timestep, so about 400 tasks over a horizon of
  2000.
- $f_{\mathrm{up}}$ is the threshold. The runs so far use 0.8.
- The backlog $B_t$ (tasks released and not finished) is logged every step. A backlog that
  keeps growing means the fleet has fallen behind.

**Correction to `thoughts.md`.** "Every arm must keep up, else there are no findings" is too
strong. A run that does not keep up is not compared on service time, but it can still be
compared on throughput and backlog. Load 0.6 does exactly that. Every arm should keep up at
the **main** load, because the main result is a service time result.

**Decided 2026-10-19. Compare against the orders actually released on the seed (fix a).**
The old test compared throughput with the nominal rate, but the number of orders released
varies by seed (348 to 442 at load 0.2), so a jammed run could pass. Fix (a) removes that
seed-to-seed noise, and it is better than a fixed backlog bound, because a healthy fleet at a
heavier load always has more tasks in the queue at the horizon.

**Open. Fix (a) alone does not catch the jam at a threshold of 0.8.** Recomputed from the
arrival run's raw rows, finished over released (released = finished + backlog).

| load | router | finished / released, lowest seed | highest |
|---|---|---|---|
| 0.2 | centralised | 0.950 | 0.997 |
| 0.2 | section-based | 0.969 | 0.997 |
| 0.2 | Token Passing | 0.945 | 0.997 |
| 0.2 | decentralised | 0.889 (the jammed seed, service time 273) | 0.998 |
| 0.3 | centralised | 0.879 | 0.995 |
| 0.3 | Token Passing | 0.880 | 0.969 |

The jammed run sits at 0.889, so it still passes at 0.8.

**Replayed 2026-10-19 to see the backlog over time.** Nine episodes were replayed from the
arrival run's checkpoints, with $B_t$ saved every timestep (scratch script, nothing trained;
every replay reproduced its logged row exactly). Mean backlog per quarter of the run, and the
slope of $B_t$ over the second half.

| run | quarters 1 to 4 | slope per 100 steps | finished / released |
|---|---|---|---|
| decentralised, 0.2, demand, the jam | 2, 11, 90, 91 | 0.3 | 0.889 |
| decentralised, 0.2, fixed | 2, 6, 3, 8 | 0.6 | 0.99 |
| centralised, 0.2, fixed | 4, 5, 6, 12 | 1.0 | 0.99 |
| Token Passing, 0.2, fixed | 3, 7, 8, 14 | 1.0 | 0.96 |
| centralised, 0.3, demand | 7, 7, 13, 8 | −0.5 | 0.99 |
| Token Passing, 0.3, fixed | 11, 32, 52, 69 | 3.4 | 0.88 |
| centralised, 0.3, fixed | 7, 11, 32, 62 | 6.0 | 0.879 |
| Token Passing, 0.6, fixed | 47, 147, 256, 383 | 24.8 | overload |
| centralised, 0.6, fixed | 65, 206, 345, 515 | 33.6 | overload |

What this shows.
- **The jam is not falling behind.** The backlog jumped to about 90 around step 1000, peaked at
  124 and then stayed flat. The fleet jammed once and then kept pace again. A growth check
  would pass it, and so would any keep-up test, because after the jam the fleet does keep up.
- **Some runs that passed at load 0.3 were falling behind.** Centralised and Token Passing on
  seed 200 003 under fixed storage have a backlog that grows all run long. The 0.8 test passed
  them. A growth check would not.
- So these are two problems with two tools.

**Agreed 2026-10-19 and applied as `[A45]`. Three parts** (each from existing practice).
1. **Keep-up, against released orders (fix a), plus a growth check.** A run keeps up when the
   backlog does not keep growing, the bounded service time of Ma et al. (2017) and the usual
   stability condition of a queue. Read the slope of $B_t$ over the second half. Healthy runs
   sit at 1 or below, runs falling behind at 3.4 and above. Set the bound from the Token
   Passing load sweep, where the loads below capacity give the healthy slopes.
2. **A jam is reported as a stall, not hidden.** Count the episodes in which an agent holding
   a task stands still for a long stretch, per arm. This is the stall count already open
   under `[A28]` in `GAPS.md`. A router that jams is a finding about that router.
3. **The gain is read with the number of seeds that agree** (already reported, "6/6"), so one
   jammed seed shows as one seed against, not only as a shifted mean.

The main load at 0.6 of capacity also helps. At 0.3 (about 0.8 of capacity) two of the
"healthy" runs were already falling behind.

### 2.2 What is read after the check, in order

1. Throughput $\Lambda_T$ and backlog, for runs that do not keep up.
2. Mean service time, for runs that keep up. This is the result.
3. Its three parts (wait for an agent, travel, blocked). They explain the result.
4. Crowding. Shows congestion.
5. Two costs, put-away distance per storage update and controller runtime per decision.

All on the same evaluation seeds for every arm. Each measure is defined in `sec:pf:measures`
(`tab:measures`), so no new measure is needed for the comparison.

### 2.3 The columns of the comparison table

The table sketched in `thoughts.md` is the "which part moved" table. Each cell is the paired
change under demand storage relative to fixed storage, so negative is better.

| router | wait for agent | travel | blocked | crowding |
|---|---|---|---|---|
| centralised | | | | |
| section-based | | | | |
| decentralised | | | | |
| Token Passing (reference) | | | | |

- **Wait for an agent.** Steps from release until an agent takes the task.
- **Travel.** Steps the assigned agent spends moving.
- **Blocked.** Steps the assigned agent stands still because of traffic.
- **Crowding.** How packed the agents are around the task's route (`eq:crowding`).

The first three add up to service time.

Token Passing belongs in the table as a reference row. It is a non-learned planner that both
assigns and routes, and it is not used inside the learned arms. It is not a fourth arm because
it also picks its own tasks, while the three learned arms share one assignment rule.

## 3. What is compared

| factor | levels | status |
|---|---|---|
| storage rule | fixed, demand, congestion-aware | decided. Three rules on the same warehouse, not three warehouses |
| stock model | arrival model (new stock is placed on arrival, nothing is moved) | decided 2026-10-18, code on branches G to J, not on `main` yet |
| router | centralised, section-based, decentralised, Token Passing as reference | decided |
| full view | decentralised router seeing the whole graph | decided as a diagnostic at one condition only |
| main load | a share of capacity, set by the Token Passing sweep (section 4.3) | decided 2026-10-19 that load must scale with the fleet and 0.2 may be too light. The share is open |
| fleet size | 8, 16, 32, 64 for RQ4 | decided 2026-10-19 |
| communication | on or off, decentralised only | conditional (RQ5) |

## 4. Research questions, their experiments and their figures

### 4.1 RQ1 and RQ2, the main result

- **RQ1.** Does adaptive storage shorten service time against fixed storage, and which part
  of service time changes?
- **RQ2.** How does that gain differ between controllers that differ in how many agents one
  decision covers?

Experiment. Every arm, fixed and demand storage, main load, paired test seeds.

Shown by
- the main table, service time gain per arm with 95% interval, and
- the "which part moved" table of section 2.3.

What the short runs say, and what to be critical of.
- RQ1 looks like a yes for every arm that does not jam. At load 0.2 the gain is 10.1
  [6.2, 14.1] for centralised, 6.8 [5.7, 8.0] for section-based and 14.7 [8.8, 20.6] for Token
  Passing. These are 10-iteration policies, so none of it goes into the thesis as a result.
- RQ2 is not answered yet. The arms that gain most are the ones with the longest and most
  blocked routes under fixed storage, so they simply have more to save. That reflects how far
  each arm has learned, not how many agents one decision covers. Report the gain both in steps
  and as a share of route time (travel plus blocked), so the comparison is fair if the arms
  still differ after the long run.
- At load 0.3 the queue multiplies a small route saving by 4 to 7. That is why 0.2 is the
  candidate main load. At 0.2 most of the gain is the route saving itself.

### 4.2 RQ3, congestion-aware storage against demand storage

Experiment. Evaluation only, no extra training. Congestion rule against demand rule, paired.

**Decided 2026-10-19. Heatmap check first.**

Shown by one figure and a small table, possibly in an appendix later. Do not think about the
60-page limit before the thesis is complete.

Be critical here. The data so far does not support the story in `thoughts.md`, where demand
storage creates congestion and the congestion rule fixes it.
- Under the arrival model at β 1, the congestion rule places stock almost exactly where the
  demand rule does. No measure separates them.
- Under the old relocation model at β 3, the congestion rule added travel and blocked time for
  the learned arms.
- Crowding rose only slightly under demand storage.

So the first step is to check whether demand storage causes congestion at all. A heatmap of
traffic per vertex, demand against fixed, shows it. If it does not, RQ3 becomes a limit of the
main result ("congestion-aware storage adds nothing here, because demand storage did not create
congestion to avoid"). That is a valid finding, not a failure. See question Q3.

The routing half of RQ3 (a congestion-sensitive reward for the controllers) needs every arm
trained a second time. `research_goals_2026-10-18.md` proposes dropping it (proposed, change 5).

### 4.3 RQ4, more agents and more orders

Experiment. A sweep over fleet size, each with matching arrival rate, every arm, fixed and
demand storage. The idea from CRAMP is to show the effect as a line over fleet size.

The commons question ("does each agent finish fewer tasks as the fleet grows, and faster when
one decision covers fewer agents") uses the same runs and the same measure, throughput per
agent $\Lambda_T / m$. Proposed to fold it into RQ4 rather than add RQ6.

Shown by a figure with fleet size on the x axis, service time gain (and throughput per agent)
on the y axis, one line per arm.

Fleet sizes 8, 16, 32 and 64 (decided 2026-10-19).

**The load scales with the fleet (decided 2026-10-19). The main load is 0.6 of capacity.** A load of 0.2 tasks per timestep is
light for 8 agents and nothing for 64, so load is defined relative to capacity.
- Capacity is the most tasks per timestep Token Passing sustains on that warehouse under fixed
  storage. On the 8-agent warehouse it is near 0.375.
- The arrival rate is a fixed share of that capacity, the same share for every fleet size. On
  8 agents, today's 0.2 is about 0.53 of capacity and 0.3 is about 0.8.
- Token Passing is the yardstick because it needs no training, so capacity does not move when
  the learned arms improve. The share must still be one where every trained arm keeps up,
  because the main result is a service time result. The learned arms finished fewer tasks than
  Token Passing after 10 iterations (centralised 0.30 against 0.375 at load 0.6), so the share
  is checked again after the long run.
- The sweep is the appendix experiment `thoughts.md` asks for. It lets the thesis argue for
  the number instead of choosing it.

The share is 0.6 (decided 2026-10-19), about 0.22 tasks per timestep on 8 agents, to be
confirmed by the sweep. It is heavier than 0.2, which the author found too light. It stays well
below 0.3 (about 0.8 of capacity), where the queue multiplied the route saving by 4 to 7 and
RQ2 became partly a measure of how close each arm runs to its limit.

**Larger fleets, transferred and trained (decided 2026-10-19).** Two sets of policies play
the 16, 32 and 64-agent warehouses.
- *Transferred.* The policies trained on 8 agents, without retraining. This works because
  every arm shares its network weights across agents and reads a local window of the graph,
  so the same network runs on any fleet size. It answers candidate question 8 ("does
  performance stay stable when agents are added").
- *Trained.* Policies trained on each fleet size, as far as the hardware allows.
- The difference between the two separates "more traffic" from "never trained on this many
  agents".

**What training at 32 and 64 agents costs.** This is the riskiest part of the plan.
- New warehouses. Instances exist for 8, 12 and 16 agents (94, 178 and 221 vertices). 32 and
  64 need the generator to scale up, probably to several hundred vertices.
- Memory. The GPU has 8 GB, and the training batch grows with the number of agents. Memory
  reduction becomes needed here.
- The centralised arm. Its agents choose one at a time, so at 64 agents one timestep is 64
  turns. At 8 agents it already took about 4 times longer to train than the decentralised arm
  (64 against 15 minutes for 10 iterations).
- Plan. Train at 16 first. Time one training iteration of each arm at 32 and 64 before
  committing. Where training does not fit, the transferred policies still give the point, and
  the thesis says why that size was not trained.

### 4.4 RQ5, communication (conditional)

Does local communication help the decentralised controller? The message content is decided
(learned embeddings, `[A14]`, `Done/message_design.md`). Embed-once (#160) is the code that
makes it affordable. RQ5 runs only if RQ1 to RQ4 are done.

### 4.5 The candidate questions removed earlier

Recommendation. None of them comes back as its own research question. Each is already covered
or was dropped for a reason.

| # | question | where it lives now |
|---|---|---|
| 1 | travel per task against a decoupled baseline | RQ1. Fixed storage is the decoupled baseline and travel is one of the three parts |
| 2 | edge congestion against a decoupled baseline | RQ3 and the crowding measure |
| 3 | which architecture has the highest throughput at fixed size | context table under fixed storage. Not the thesis question, and after short training it shows learning speed |
| 4 | which architecture degrades slowest with size | RQ4 |
| 5 | commons-like overuse under individual rewards | commons question, folded into RQ4 (proposed) |
| 6 | congestion-sensitive rewards reduce the concentration | routing half of RQ3, proposed to drop |
| 7 | local communication in distributed controllers | RQ5 |
| 8 | stable performance when agents are added | RQ4, by evaluating the 8-agent policies on larger fleets without retraining (decided 2026-10-19) |

## 5. Figures and tables to produce

| what | content | answers |
|---|---|---|
| training curve | tasks completed per training episode against iteration, one colour per arm | that every arm learned |
| validation curve | tasks completed on validation seeds per checkpoint, one colour per arm | checkpoint choice |
| override rate | share of moves overridden by conflict resolution per iteration | that the centralised arm is never overridden (always 0) |
| main table | service time gain per arm, 95% interval, seeds with the same sign | RQ1, RQ2 |
| split table | section 2.3 | RQ1, RQ2 |
| warehouse graph, storage | where demand storage puts stock against fixed storage | RQ1, why travel falls |
| warehouse graph, traffic | traffic or blocked time per vertex, demand against fixed | RQ3, whether congestion appears |
| cost graph | put-away distance against service time gain, over a sweep of the stock margin | what the gain costs |
| scaling graph | gain and throughput per agent against fleet size | RQ4, commons |
| load sweep | Token Passing throughput against arrival rate per warehouse | appendix, justifies the load |

On training plots. Service time is not part of the reward (the reward is potential shaping, a
delivery bonus, an override penalty, a wait cost and a crowding cost, `eq:reward`), so a service time curve over training would
come from the validation runs, not from training. RLlib's `episode_return_mean` is not a good
training curve, because the shaping term dominates it.

## 6. Cost of adaptive storage

**Stale in `thoughts.md`.** The list of relocation measures (relocation distance per update,
distance per relocated unit, relocation distance against travel saved, and so on) belongs to
the old relocation model, where stock already on a shelf was moved for free. The arrival model
replaced it on 2026-10-18. Under the arrival model nothing is moved. New stock arrives at the
receiving point every period and the storage rule decides which shelf it goes to.

The cost is now the **put-away distance per update**, how far arriving stock travels to its
shelves (`eq:putaway`). Adaptive storage is cheaper than fixed here, because it places stock
nearer to where it is needed (at load 0.2, 31.7 against 73.0 per update).

Where it goes in the thesis.
- The definition goes in the problem formulation or method.
- The measured values go in the results chapter, next to the gain they buy.
- The cost graph of section 5 shows both together.

This also closes item 3 of "other work" in `thoughts.md`. A relocation cost for newly arriving
items does not make sense, and under the arrival model there is none, because placing arriving
stock is what dynamic SLAP does "upon entry or reentry into the system" (Waubert de Puiseau et
al. 2022). Letting a controller learn when to move stock that is already stored is a different
problem and is out of scope. However this changes the introduction and does it not also change the result?

## 7. Parameter values

Do not pick values freely, so the thesis does not turn into a study of cost settings.
- Routing and reward values. Take them from van Knippenberg et al. (2021) where the model
  matches theirs, and say so where it does not.

**Decided 2026-10-19. Take the movement cost of an agent and the edge cost from van
Knippenberg et al. (2021).** What they use, against what the thesis and code use now.

| value | van Knippenberg (Table 1) | thesis and code now |
|---|---|---|
| edge cost | 1 per edge on their benchmark lattices | random per edge in [0.5, 2.0] (`random_edge_costs: true`) |
| moving one step | reward −0.1 | no per-move term. Moving is paid through the shaping term |
| waiting, not at the goal | reward −0.2 | $c_{\mathrm{wait}}$ = 0.1, "below the cheapest edge" (`[A30]`) |
| collision | −2, and the episode ends | override penalty 0.5, no collision possible after resolution |
| reaching the goal | +10 | delivery reward 10 (already the same) |

**Correction to the earlier note.** Taking their values does *not* reverse `[A30]`. Their
reward has no shaping term, the thesis reward does. Shaping pays about one edge cost per step
towards the target and charges about one per step away. With unit edges and their two values,
one step of each kind is worth roughly
- a step towards the target, +1 − 0.1 = +0.9,
- waiting, −0.2,
- a step away (a detour), −1 − 0.1 = −1.1.

So waiting stays cheaper than a detour, as `[A30]` wants, and moving on stays best, as van
Knippenberg wants. Both orders hold.

**Does it strengthen the thesis? Yes, for three reasons.**
1. Every cost value then has a published source instead of being chosen by the author.
2. Time and distance get the same unit. Today an edge costs 0.5 to 2.0 but every move takes
   one timestep, so put-away (edge cost) and travel (timesteps) cannot be compared directly.
   The short run notes had to call those ratios rough. With unit edges they are exact.
3. Token Passing minimises timesteps. With unit edges that is the same as minimising cost, so
   the reference and the learned arms optimise the same thing.

One limit to state honestly. Van Knippenberg et al. say their values "were empirically
established, based on common practices". The thesis borrows them and says so. It does not
claim they are optimal.

**Agreed 2026-10-19 and applied in the thesis as `[A43]`.** Code still to do, and the
policies must be retrained, which the long run does anyway.
- Thesis. `sec:impl:instances`, every edge cost 1, after van Knippenberg et al. and the MAPF
  benchmarks they use. `eq:reward` gains a move term $-c_{\mathrm{move}}$ for every step an
  agent moves, with $c_{\mathrm{move}} = 0.1$, and $c_{\mathrm{wait}}$ becomes 0.2.
  `tab:rlparams` and the notation table get both values with the citation. `[A30]`'s wording
  "below the cheapest edge" still holds. Worked examples with an edge of cost 2 (for example
  `2.Introduction.tex`, near line 1058) need checking.
- Code. `random_edge_costs: false` in the configs, a `move_cost` argument and a sixth logged
  term in `environment/reward_function.py`, `wait_cost: 0.2`.
- The graph stays non-lattice in shape (one-way aisles, dead ends), so RQ5's point about a
  non-lattice graph still holds. Only the costs become uniform.
- Not included unless asked. Their collision penalty (−2) against the override penalty (0.5).
- Storage values (period Δ, stock margin, β). Look for values in the SLAP and dynamic SLAP
  literature first. Where none fits, choose by the Token Passing sweep and say so.
- Values still marked TBD in `4.Implementation.tex` are genuinely undecided. Each needs a
  source or a sweep.

## 8. The lattice comparison after van Knippenberg (open)

What van Knippenberg et al. (2021) did. They took classic MAPF benchmark maps (grid worlds),
turned each open cell into a node with unit cost edges, and compared their GCN router with A*,
ICBS, ICTS and PRIMAL on the number of solved instances. The point was to place a graph-based
method among grid-based ones.

The idea in `thoughts.md` is to do the same, putting the warehouse graph in a lattice with cost
1 per edge. **Decided 2026-10-19. The small version below.**
- Those benchmarks are one-shot MAPF. This thesis is lifelong pickup and delivery with storage,
  so a direct replication needs a one-shot mode and baselines that do not exist in the code.
- A smaller version fits the thesis. Run the arms and Token Passing on a lattice version of the
  warehouse with unit edge costs and check that the ranking holds. That shows the results do
  not depend on the non-lattice graph.

## 9. Engineering work

| item | what | status | needed for |
|---|---|---|---|
| land the arrival model | review and merge branches G to J, commit `[A38]` to `[A40]` in `thesis/`, redraw `fig:storageexample` and `fig:dkr` | code merged into `main` (#175 to #177). Thesis text uncommitted | everything after this |
| keep-up test | the three-part check of `[A45]`, in the thesis and in evaluation | done 2026-10-19, code merged (#180, #181). `chi_max` and the stall length wait for the Token Passing load sweep | the main result |
| checkpoint choice | choose on validation at the measurement load, or say it is the training load | open | the main result |
| seeds | 3 training seeds, 10 to 12 test seeds | proposed | the main result |
| embed-once (#160) | embed the graph once per step instead of once per agent window | active, Track B | RQ5 |
| memory reduction | `memory_reduction_plan.md`. Saves memory, not time (see below) | not started | training at 32 and 64 agents |
| larger warehouses | generate the 32 and 64-agent instances, time one evaluation episode per arm on each | not started | RQ4 |
| RLlib new API stack | done 2026-10-19, uncommitted in the worktree `chore/rllib-new-api` (scratchpad). Was already on the new stack. Old callback base class, the Catalog warning, the DreamerV3 import warnings and the implicit API stack fixed. Open for the author: the Ray version floor, `restart_failed_env_runners`, two RLlib-internal warnings | review and commit | cleaner runs |
| code for `[A43]` to `[A46]` | `code_changes_plan_2026-10-19.md` at the workspace root, eight steps | done 2026-10-19, all eight merged into `main` (#178 to #186, with SKU names as #183). Only the gated step G2 is left | the long run |
| research goals | changes 1, 3, 4, 6, 7 and 9 of `research_goals_2026-10-18.md` | applied 2026-10-19 as `[A41]` and `[A33]`, uncommitted. Changes 2, 5 and 10 open | the Introduction |

**Should memory reduction come first, since it would cut training time?** Not by itself.
`memory_reduction_plan.md` stores the same rows in smaller number types and splits one pass
into smaller pieces. It saves memory, and step a makes that pass a little slower. Memory is
also not what limits a run today, since the 8-agent runs fit on the GPU. It becomes needed when
training at 32 and 64 agents. Training time goes into running
the simulator and, for the centralised arm, into its one-agent-at-a-time turns. What would
cut time is a separate change, such as looking up the per-vertex window once instead of
rebuilding it every step (listed under "Later options" in that plan), or embed-once for the
communication runs. Memory reduction moves up only if a long run runs out of memory.

## 10. Order of work

1. **Land the arrival model** (code and thesis text). Every adaptive number depends on it. 
    DONE `order_lines_proposal.md`
2. **Settle the decisions that change what the long run measures.** The keep-up check (Q9, CHECK THE 
   `[A45]`) and the Knippenberg costs (Q11, `[A43]`) are settled, and the research-goal changes
   are applied (`[A41]`, `[A33]`). Checkpoint choice and seeds are still open.
      `/home/bjarkek/Documents/thesis/slap-mapd-coupling/DIR/`  if result is complete
3. **Write the agreed changes into the thesis.** `[A43]` to `[A46]` are written, uncommitted, THINK IS DONE 
   and their code is merged (`code_changes_plan_2026-10-19.md`, steps 1 to 8). Load as a share
   of capacity and the transfer evaluation for RQ4 are still to be tagged.
    DNE

   **Next is step 4.** The order lines of `[A46]` make arrivals burstier, so the sweep runs
   on the put-away model of `[A47]` (robots carry arriving stock, decided 2026-10-19). Text
   drafted in `A47_putaway_draft.md`, code planned in `putaway_code_plan_2026-10-19.md`
   (P1 to P6, the Token Passing runner last). Then one arm is trained as a pilot.
4. **Token Passing load sweep** on every warehouse (8, 16, 32, 64). Cheap, no training. It
   gives capacity per warehouse, so 0.6 of capacity becomes an arrival rate per fleet size. DONE `/home/bjarkek/Documents/thesis/slap-mapd-coupling/DIR/` location 
    Running right now. 
5. **Long run.** Three arms plus Token Passing, fixed and demand storage, main load, 3 training
   seeds, arrival model.
6. **Main result figures and tables** (section 5).
7. **RQ3 check.** Traffic heatmap, then decide whether RQ3 is a result or a limit.
8. **RQ4 sweep.** Generate the 32 and 64-agent warehouses. Evaluate the 8-agent policies on
   every size. Train at 16, then time 32 and 64, with memory reduction first.
9. **RQ5** if time allows, after embed-once.
10. **Lattice comparison**, depending on Q4.

## 11. Questions for the author

Answered ones move into the sections above.

Answered 2026-10-19.
- Q1. Load scales with the fleet, as a share of Token Passing capacity. 0.2 tasks per
  timestep may be too light. The share is still open (section 4.3).
- Q2. Fleet sizes 8, 16, 32, 64.
- Q3. Heatmap check first.
- Q4. Small lattice check on the warehouse.

Answered 2026-10-19, second round.
- Q1b. The main load is 0.6 of capacity.
- Q5. Larger fleets are evaluated with the 8-agent policies, without retraining. This answers
  candidate question 8.
- Q6. Keep-up is judged against the orders released on the seed.
- Q7. Changes 1, 3, 4, 6, 7 and 9 applied.
- Q8. The movement cost of an agent and the edge cost come from van Knippenberg.

Answered 2026-10-19, third round.
- Q10. Train at the larger sizes too, as far as the hardware allows, next to the transferred
  policies.
- Q12. Change 5 applied as `[A42]`. Change 2 is on hold until Q13 is settled, since it would
  write "closed-loop" into the main question.

Answered 2026-10-19, fourth round.
- Q9. Three-part keep-up fix, applied as `[A45]`. Still open are `chi_max` and the stall
  length.
- Q11. Knippenberg costs, applied as `[A43]`.
- Q13. Main result reworded, applied as `[A44]`. Change 2 of the research goals is settled
  by it.

Still open.
- **Q14. FIFO.** What should be first in, first out? See section 12.
- Q15. Orders with several lines and amounts, applied as `[A46]` (2026-10-19), code merged
  (#182, #184, #185). A line may take from several shelves. Still open is the distribution of
  lines per order (mean 5).
- **G2, cold stock on prime shelves.** Definitions agreed 2026-10-19 (top 10 SKUs, prime
  shelves the nearest ones the top 10 fill). Built uncommitted in the worktree
  `feat/cold-stock`. Needs a sentence in `sec:pf:measures`.
- Q16. Delivery vertices. Answered 2026-10-19, they stay at random, as in Ma et al. (2017).
  The thesis drops "one side of the warehouse" (`[A47]`, drafted). The spread of shelf
  distances is reported per warehouse size (`code_changes_plan_2026-10-19.md`, W1).

## 12. Ideas raised on 2026-10-19

### FIFO

Two things in the model already have an order.
- **Tasks** are already first in, first out. Free agents take the oldest waiting task first
  (`eq:assignmentrule`).
- **Stock** is picked from the shelf nearest the order's delivery vertex (`[A39]`), whatever
  its age.

So FIFO would most likely mean picking stock oldest first, as warehouses rotate stock. Two
cautions.
- It does not close the loop. Which unit is oldest depends on when stock arrived and on the
  orders, not on the traffic. The loop is closed only when storage reads the traffic.
- It sends agents past nearer stock to reach older stock, so travel rises. Old stock sits
  where demand was when it arrived, which after a drift can be far from where it is wanted
  now. The gain of RQ1 would likely shrink.

The phrase "take the task at the last point and finish that first" could also mean last in,
first out. That needs the author's meaning before anything changes (Q14).

### How the old placement empties (asked 2026-10-19)

Stored stock never moves, so an old placement empties only when its units are picked.
- **A SKU that cooled down.** Its old shelf is near the delivery vertices, so it is also the
  nearest holder, and picks already take from it first. It drains at the SKU's own order rate,
  which is now low. The arrivals rule also counts those units, so few new units arrive. FIFO
  picking would not drain it any faster. This is the "cold stock on prime shelves" of the
  arrival probe (73% to 79% of the prime shelves' used capacity held SKUs ranked 20 or lower).
- **A SKU that got hotter.** New units go nearer, old units sit further away. The old ones are
  picked once the near shelf runs out, and since arrivals top up the total, that happens.
  FIFO would use the old ones first, at the cost of longer trips.

So FIFO does not solve it. Three levers do, each from existing practice.
1. **The margin ε.** How much stock is left behind when demand moves. A smaller margin leaves
   less behind. It is already in the planned margin sweep, evaluation only.
2. **Measure whether it matters.** Shelf capacity is about half used, so cold stock blocks no
   placement today. A measure of cold stock on prime shelves shows it (gated step G2 of
   `code_changes_plan_2026-10-19.md`).
3. **Healing moves.** Moving cold stock off prime shelves in small steps is the "healing" of
   Kofler et al. (2011, re-warehousing against healing), and the relocation agent in the
   dynamic SLAP review of Waubert de Puiseau et al. (2022). It brings back a relocation cost,
   and with unit edges that cost is now a time. It stays a stated limitation, already in the
   scope ("Stored stock never moves"). Kofler et al. is not in the bibliography yet.

### Orders with several items and amounts

Today an order is one unit of one SKU, and it becomes one task (one shelf, one delivery
vertex). Two ways to allow more.
- **Split the order into lines.** Each unit becomes its own task, possibly for different
  agents, and the order is done when its last task is delivered. Small change, mostly the
  order generator and one more measure (order service time, the time until the last line is
  delivered). Storage and controllers are unchanged. It adds little to the research
  questions unless SKUs are ordered together, and then the natural next step is a storage rule
  that places SKUs ordered together near each other (correlated storage in the SLAP
  literature), which is a new rule.
- **One agent picks the whole order.** A task becomes a tour of several shelves. That changes
  the task model, the agent's current target and its observation, the assignment rule, Token
  Passing (which assumes one pickup per task) and the service time split. It is a different
  problem (order batching and picker routing), weeks of work, and it would delay the long run.

**Update 2026-10-19. The split version is an existing model.** Krnjaic et al. (2022), already
cited, define an order as several order lines, each an item and a quantity. In their
goods-to-person setting each robot fetches one storage location to the delivery station, and
the order is complete when all its lines are picked. Their pick rate counts order lines per
hour. That is the split version, and the thesis' task is one such line with quantity 1. Their
picker-to-goods setting, where one vehicle collects a whole order, is the tour version.

So the split version is faster than it looked. Controllers, observations and Token Passing do
not change, and no retraining is needed for the task model itself. What changes is the order
generator, the pickup rule (a line takes its quantity from one shelf), the arrivals counting
units, and one more measure (order completion time). About two to three small PRs, plus a
thesis change. Adopted as `[A46]` and built as steps 6 to 8 of
`code_changes_plan_2026-10-19.md`, merged 2026-10-19.

Recommendation. Implement the split version before the long run if the author wants it, since
every result changes with the order stream. Keep the tour version as a stated limitation.
