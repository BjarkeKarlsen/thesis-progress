# SLAP–MAPD Embedding Feedback: Research and Implementation Handoff

## Purpose and status

This document transfers the substance of a research-design conversation to another LLM. It is a structured synthesis, not a verbatim transcript. It includes the user's thesis context, the proposed architecture, training schedules, deadline extensions, literature leads, and corrections to errors in earlier assistant suggestions.

Treat all proposed extensions as unimplemented unless the user confirms otherwise. Do not describe illustrative equations, dimensions, schedules, or hoped-for benefits as experimentally validated. The most recent discussion concerns whether storage-model weights can be updated only once every 100 episodes.

## 1. User and research context

The user is a technically advanced computer-science master's student researching graph neural networks (GNNs), reinforcement learning (RL), and multi-agent warehouse robotics. They prefer direct, technically detailed, implementation-oriented explanations and challenge ambiguous designs.

The thesis concerns coupling:

- **SLAP/DSLAP:** storage location assignment, including placement of arriving stock over time.
- **MAPD:** lifelong multi-agent pickup and delivery, including task assignment and routing.
- **GNN routing policies:** controllers operating centrally, by zone, or per robot.

An uploaded thesis draft was available as `main.pdf` (62 pages), titled *Coupled Storage Routing Problem with SLAP and MAPD*. Another LLM may not have that attachment. Ask for the current draft or code before making implementation-specific claims beyond this handoff.

The conversation occurred on November 23–24, 2026. Draft results and implementation details may change.

## 2. Existing warehouse model

### 2.1 Physical environment

The warehouse is a static directed graph G = (V, E). Vertices represent robot positions; edges represent legal moves. Special vertices include shelves, workstations, docks, and idle endpoints.

The model allows weighted travel costs, but the generated instances described in the draft use unit edge costs. Distinguish graph hops from weighted travel distance when discussing receptive fields.

Agents move or wait at each simulation step. Vertex conflicts and opposing edge swaps are prohibited. A common conflict-resolution module prevents illegal joint execution.

### 2.2 Stock and task flow

- Stock is represented by SKU quantities at shelves.
- Shelves have finite capacity.
- Incoming stock arrives on pallets at periodic storage epochs.
- Choosing a shelf reserves capacity immediately.
- A put-away task transports the pallet from a dock to that shelf.
- Incoming stock does not become pickable merely because a shelf was assigned; it becomes available after put-away delivery.
- Existing stored stock is not relocated by the baseline model.
- Customer orders consist of multiple lines.
- Pick tasks transport units from shelves to an order's workstation.
- A line may split into multiple pick tasks if stock is distributed across shelves.
- Once all order lines reach the workstation, a shipment task takes the order to a dock.
- The customer-facing order completion time is arrival at the dock, not completion of one pick.
- Put-away tasks generally replenish shared inventory and do not belong to exactly one customer order.

### 2.3 Controller variants

The learned controllers share much of their architecture and infrastructure:

1. **Centralised:** sees the full warehouse and chooses moves sequentially in a priority order.
2. **Section-based:** sees a zone plus a border halo; chooses moves for agents currently in that zone.
3. **Decentralised:** acts for one agent using its local graph observation, optionally with learned local agent communication.

Task assignment in the described baseline is shared across learned controllers: oldest waiting task first, assigned to the nearest free agent. It is not a learned assignment policy in that baseline. Token Passing is a separate classical reference and uses its own assignment/planning machinery.

Agents crossing zone boundaries change controlling zone but retain their tasks. Zones operate concurrently; border conflicts still require resolution.

### 2.4 Existing observations and network

The draft describes local graph observations, distances to the agent's target, a crowding feature, and optional learned messages for decentralised agents. The architecture includes a graph encoder, optional communication, and a per-move policy head.

Do not assume an exported embedding is automatically a congestion embedding. An existing routing representation was trained to help movement decisions, not necessarily to predict storage consequences.

### 2.5 Existing storage rules

The draft compares:

- **Fixed storage:** SKU home shelves, with a fallback when needed.
- **Demand storage:** place more popular SKUs on shelves with lower demand-weighted travel cost.
- **Congestion-aware storage:** augment travel cost with measured blocked time associated with picks from a shelf.

The congestion-aware rule also adjusts pickup-shelf ranking, so its effects are not limited to placement of new stock.

Measured blocked time is associated with the shelf from which a pick originated, but can occur anywhere along that pick's service trajectory. This is a service-cost attribution, not necessarily a physical localisation of congestion.

### 2.6 Existing coupling

The current physical forward coupling is:

    storage placement -> available pickup locations -> tasks -> robot traffic

The congestion-aware backward coupling is:

    robot outcomes -> shelf-associated blocked-time statistics -> storage/pickup ranking

The proposed extension replaces or supplements that low-dimensional backward signal with learned representations, and optionally adds a learned information channel in the reverse direction.

## 3. User's original halo literature request

The user first requested 3–5 peer-reviewed papers supporting GNN/message passing on partitioned graphs with owned vertices and read-only halo/ghost neighbours. Their controller partitions aisles into zones, with a halo defined by a fixed travel distance.

Preferred topics:

- Halo/ghost nodes or cells.
- Boundary nodes.
- Overlapping graph partitioning.
- Distributed GNN training: DistDGL, PipeGCN, BNS-GCN.
- Overlapping domain decomposition.
- Explanation of halo width versus message-passing depth or receptive field.

### 3.1 Literature leads mentioned

These are leads from the conversation, not a fully verified bibliography. Verify publisher metadata, authors, pages, peer-review status, and exact supporting passages before providing thesis-ready citations.

**DistDGL**

Da Zheng, Chao Ma, Minjie Wang, Jinjing Zhou, Qidong Su, Xiang Song, Quan Gan, Zheng Zhang, and George Karypis. 2020. *DistDGL: Distributed Graph Neural Network Training for Billion-Scale Graphs*. IEEE/ACM Workshop on Irregular Applications: Architectures and Algorithms (IA3).

- Preprint: https://arxiv.org/abs/2010.05337
- Relevant lead: partition ownership, cached one-hop halo/ghost structure, remote feature access.
- Important: one-hop topology caching is not equivalent to independently computing an arbitrary-depth GNN on an unchanging one-hop feature halo.

**PipeGCN**

Cheng Wan, Youjie Li, Cameron R. Wolfe, Anastasios Kyrillidis, Nam Sung Kim, and Yingyan Lin. 2022. *PipeGCN: Efficient Full-Graph Training of Graph Convolutional Networks with Pipelined Feature Communication*. ICLR 2022.

- https://arxiv.org/abs/2203.10428
- https://openreview.net/pdf?id=kSwqMH0zn1F
- Relevant lead: partition-parallel full-graph GCN computation and cross-partition feature/gradient communication, including pipelining/staleness.

**BNS-GCN**

Cheng Wan, Youjie Li, Ang Li, Nam Sung Kim, and Yingyan Lin. 2022. *BNS-GCN: Efficient Full-Graph Training of Graph Convolutional Networks with Partition-Parallelism and Random Boundary Node Sampling*. MLSys 2022.

- https://proceedings.mlsys.org/paper_files/paper/2022/hash/676638b91bc90529e09b22e58abb01d6-Abstract.html
- Relevant lead: remote boundary-node overhead and sampling to reduce communication/memory.

**DistGNN**

*DistGNN: Scalable Distributed Training for Large-Scale Graph Neural Networks* (2021).

- https://arxiv.org/abs/2104.06700
- Earlier response supplied only the preprint citation and did not verify the complete publication record. Resolve this before including it as a peer-reviewed recommendation.

**RapidGNN**

*RapidGNN: Energy and Communication-Efficient Distributed Graph Neural Network Training* (2025).

- https://arxiv.org/html/2509.05207v1
- Earlier response listed this despite not establishing peer review or a complete author list. Do not treat it as satisfying the original peer-reviewed-source requirement without verification.

### 3.2 Halo qualifications for future answers

For a standard local, one-hop-per-layer message-passing network, an L-layer output has an L-hop input dependency. A zone computing independently needs the dependency closure for the outputs it controls, not simply an arbitrary geometric border.

Important qualifications:

- Weighted travel radius and hop radius are not interchangeable without assumptions on edge costs.
- Global pooling, graph-wide normalisation, nonlocal attention, or positional features can add dependencies beyond the simple L-hop picture.
- Exact equivalence may require original global normalisation/degrees, not degrees recomputed on a truncated subgraph.
- Halo vertices can be read-only with respect to robot control/state ownership while their temporary neural representations are recomputed during a forward pass.
- Freezing halo hidden states at every layer is not generally the same as evaluating the original full-graph GNN.
- Layerwise communication is an alternative to preloading a complete multi-hop dependency halo.
- Distributed-training precedents justify computational/data ownership mechanisms, not warehouse-routing effectiveness.

## 4. Main proposed research extension

The user asked whether embeddings from RL agents could be sent into SLAP and embeddings sent back again.

The proposed answer was yes, with two learned interfaces:

1. **MAPD -> SLAP:** routing conditions represented by spatially indexed agent-message summaries.
2. **SLAP -> MAPD:** stock, expected workload, and placement context represented by spatially indexed storage messages.

This is in addition to the physical coupling through stock and tasks.

The extension is not automatically hierarchical control in the strong sense: storage chooses locations, rather than necessarily issuing goals or commands to movement policies. Hierarchical RL is an architectural analogy for different decision timescales.

## 5. Concrete architecture

### 5.1 Routing computation

At timestep t, agent i receives its permitted graph observation plus cached storage context.

    allowed graph observation + assigned-task features + storage context
        -> routing GNN encoder
        -> agent representation z_i(t)
            -> movement policy head
            -> feedback projection head

An illustrative exported message is:

    m_i(t) = f_up(z_i(t), q_i(t)) in R^d_m

where q_i can include:

- Task phase: approaching pickup, carrying, idle.
- Time remaining to a task deadline, if deadlines are enabled.
- Estimated slack.
- Last-action override or blocked indicator.
- Relevant explicit outcome features.

Dimensions such as 16 or 32 were suggested only as prototype choices.

### 5.2 Message metadata

Store metadata separately from the latent vector:

    agent_id
    timestep
    current_vertex
    task_id / order_id, when applicable
    pickup_shelf, when applicable
    task_phase
    message_vector

Without a spatial or task key, a vector cannot tell the receiver where it belongs.

### 5.3 Spatial aggregation: keep two channels separate

**Current-location channel**

Pool messages for agents physically inside zone q:

    e_q^traffic(t) = mean{m_i(t): p_i(t) in Y_q}

Meaning: conditions currently experienced in that zone.

**Pickup-associated channel**

Pool messages for agents serving picks from shelf v:

    e_v^service(t) = mean{m_i(t): pickup(j_i) = v}

Meaning: conditions experienced while serving that shelf, potentially far from the shelf itself.

Do not merge these interpretations. Otherwise, a workstation queue can be mistaken for physical congestion at its source shelf.

Add explicit statistics to each summary:

- Sample/agent count.
- Presence mask.
- Blocking counts.
- Traversal counts.
- Optional age/staleness indicator.

A mean embedding alone discards multiplicity. Empty observations should not silently mean zero congestion.

### 5.4 Temporal aggregation

Let storage interval n be I_n = [t_n, t_(n+1)). Aggregate messages observed in that interval:

    e_bar_q[n] = TemporalAggregate({e_q(t): t in I_n})

Start with a mean and sample count. Exponential smoothing is optional. Explicitly specify whether averaging is over agent-time samples or over per-timestep means; these weight traffic differently.

### 5.5 Storage encoder

For candidate shelf v, combine:

    current stock
    available and reserved capacity
    observed demand estimates
    pending work / urgency summaries
    zone routing summary
    shelf-associated service summary

into:

    h_v[n] = f_storage(explicit_features_v[n], e_bar_zone(v)[n], e_bar_v^service[n])

This can be an MLP initially or a storage-side GNN later. Do not introduce a second GNN merely because the input is spatial; validate the need.

### 5.6 Two possible decision heads

**A. Hybrid storage rule, proposed first implementation**

Predict additional pick-service delay:

    w_hat_(k,v)[n] = g_phi(h_v[n], u_k[n])

where u_k represents SKU demand and destination/category context.

An illustrative ranking cost is:

    C(k,v) = lambda_hat_k * [d_work(k,v) + alpha*w_hat_(k,v)]
             + mu_hat_k * d_dock(v)

Definitions:

- lambda_hat_k: estimated picks per timestep.
- mu_hat_k: estimated pallet arrivals per timestep.
- d_work: shelf-to-workstation travel cost.
- d_dock: dock-to-shelf travel cost.
- w_hat: predicted extra time per pick.

Mask infeasible shelves. Place pallets sequentially and update reserved capacity after each placement.

This is a supervised estimator inside a hand-designed decision rule. It is not an RL SLAP policy.

**B. Learned storage policy**

Produce candidate-shelf logits or action values, enforce capacity with an action mask, and train on storage-level outcomes. This is a larger research extension with delayed credit assignment.

### 5.7 Downward storage context

Generate:

    b_v[n+1] = f_down(h_v[n], planned_inbound_v[n], reserved_capacity_v[n])

Candidate content includes:

- Available stock.
- Incoming but not yet available stock.
- Expected workload based on past demand and current pending tasks.
- Capacity reservations and latest placement commitments.
- Recent routing context.

Append this to routing-visible vertex features:

    x_tilde_(i,v)(t) = concatenate(x_(i,v)(t), b_v[n+1])

Use zone context or a typed empty/masked vector for vertices without shelf-specific features.

The receiving routing policy must be trained/fine-tuned to interpret the new channels. A frozen policy cannot simply understand previously unseen input dimensions.

### 5.8 Observation-boundary concern

Restricting a globally computed embedding to visible vertices does not by itself make its information local: each vector may encode global data.

For centralised/zone/decentralised comparisons:

- Either generate downward messages from information each controller is permitted to access.
- Or declare the storage broadcast an extra communication capability and evaluate it separately.

The latest proposed prototype omits a global storage embedding to limit this issue. Even per-zone or per-shelf messages require an information-provenance check.

## 6. Causal execution order

Initialise cached storage context b[0] and empty routing accumulators.

During interval n:

1. Build each controller's permitted observation.
2. Attach cached storage context b[n].
3. Run routing encoder and movement policy.
4. Resolve conflicts and execute moves.
5. Update warehouse state, task lifecycle, and rewards.
6. Accumulate routing messages and realised outcomes.

At the storage epoch ending interval n:

1. Finalise routing summaries e[n].
2. Read current stock, demand, capacity, and pending work.
3. Encode storage state using e[n].
4. Assign shelves to arriving pallets with sequential capacity updates.
5. Create put-away tasks and reserve destinations.
6. Build storage context b[n+1].
7. Clear interval accumulators.

During interval n+1, agents use b[n+1].

The information cycle is:

    b[n] -> routing during interval n -> e[n]
         -> storage decisions and b[n+1]

This prevents a circular same-instant definition of messages.

Physical inventory changes still follow task execution. Shelf selection does not teleport stock.

## 7. Deadline extension

The user asked whether this also adds time constraints per order and task.

Important clarification: embeddings do not require deadlines. These are separate experimental factors that can be combined.

The proposed deadline-aware design is:

- One customer-facing order deadline d_z.
- Derived pick-task deadlines allowing time for downstream shipment.
- Shipment deadline equal to the order deadline.
- Put-away tasks either have separate replenishment targets or no individual deadline; they generally cannot inherit exactly one order deadline.

Order deadline:

    d_z = release_z + allowed_lead_time_z

Simple pick target:

    d_j = d_z - estimated_shipment_allowance - safety_buffer

Parallel picks are prerequisites to a common shipment. Do not add the durations of all other picks as if they must execute sequentially. All picks must be delivered before shipment can start; meeting derived targets does not guarantee the shipment will actually receive an agent on time.

### 7.1 Agent-dependent slack

    slack_(i,j)(t) = d_j - t - T_hat_(i,j)(t)

Before pickup, remaining time includes approach to pickup plus pickup-to-delivery travel and estimated delay. After pickup, include only remaining delivery travel and delay.

For an unassigned task, estimate completion separately for candidate agents or specify the selection rule used to turn those estimates into a task-level priority. Do not use an undefined agent position for an unassigned task.

### 7.2 Observation and assignment changes

Possible extra routing features:

- Normalised remaining time.
- Slack.
- Task phase.
- Order progress.
- Remaining distance.

An initial assignment extension is smallest estimated slack first, then nearest feasible free agent, but agent-dependent slack makes joint matching a more principled later option.

Deadlines should be assigned from common exogenous rules across experimental conditions. Do not give an order a more generous deadline because one storage rule places its stock farther away.

### 7.3 Soft versus hard deadlines

The suggested initial extension uses soft lateness costs rather than declaring an entire run invalid after a missed deadline.

For completion time C_z:

    tardiness_z = max(0, C_z - d_z)

Evaluate on-time rate, tardiness, throughput, backlog, and unfinished overdue orders. Reporting only completed orders can hide the worst failures.

Task-level penalties are optional shaping/surrogates. Applying both task and order penalties can double-count delay or alter incentives; specify the intended objective.

Deadline awareness does not guarantee feasibility or prevent deadlocks.

### 7.4 Corrected urgency weight

An earlier assistant formula was wrong:

    1 + rho*max(0, d_j - finish_j)

It upweights early completions, not urgent tasks.

A proposed bounded online alternative is:

    w_j(t) = 1 + rho*clip((s_crit - slack_(i,j)(t))/s_scale, 0, 1)

where s_scale > 0. This increases weight when slack is tight/negative. Thresholds are design parameters.

Keep explicit urgency statistics alongside latent summaries so urgency cannot be accidentally lost in pooling.

## 8. Training: what actually learns?

### 8.1 Three distinct mechanisms

- A forward data connection passes vectors at inference time.
- A supervised objective trains a predictor from labels.
- An RL objective trains a policy from returns.

Do not assume a forward connection automatically trains both ends. Do not assume PPO propagates gradients through discrete warehouse actions or simulator transitions.

### 8.2 Stage A: upward interface only

1. Freeze routing policy and its encoder.
2. Collect messages/embeddings, metadata, and realised delay outcomes.
3. Train spatial/temporal aggregation projections and a delay predictor.
4. Use predictions inside a fixed storage ranking rule.

Illustrative objective:

    L_delay = mean_j (w_hat_j - observed_extra_delay_j)^2

Define the label and forecast horizon precisely. A current interval's summary used at an epoch should predict future relevant outcomes, not accidentally use the answer from the future as an input.

Pitfalls:

- Never-finished tasks are censored; dropping them biases against severe congestion.
- Delays are observed only for selected shelves/actions, not all alternatives.
- Rarely used candidate shelves are out-of-distribution.
- A model predicting per-task service delay may not identify the causal marginal effect of placing one more pallet at a shelf.
- Freeze/detach routing embeddings during this stage.

### 8.3 Stage B: downward interface

Freeze the storage estimator/rule and train or fine-tune routing with storage-context inputs.

If the context producer is trainable, explain whether gradients reach it. Serialising/detaching cached messages prevents that unless the graph is deliberately reconstructed or retained. Alternatively, train the context encoder with an explicit auxiliary objective.

Do not retain a huge graph across hundreds of simulation steps merely by accident. Choose an intentional training boundary.

### 8.4 Stage C: alternating adaptation

Only after individual directions help:

    freeze routing -> train storage-side components
    freeze storage side -> train routing
    evaluate with both frozen

A changing routing encoder changes the coordinate system and semantics of exported embeddings. Stored latent vectors from old encoder versions may become incompatible.

Options to investigate:

- Version data by encoder checkpoint.
- Recompute embeddings from stored raw observations where possible.
- Keep a stable/frozen export encoder.
- Refit the receiving predictor after routing updates.

These are options, not established implemented solutions.

## 9. Most recent question: update storage only every 100 episodes?

The user asked whether updating the storage component only every 100 episodes would be enough.

The key answer was to distinguish three clocks:

| Clock | Typical trigger | What changes |
|---|---|---|
| Routing action | Every simulation step | Intended robot moves |
| Storage inference / feedback refresh | Each storage epoch within an episode | Placement decisions and cached storage messages |
| Parameter learning | After a collected batch, potentially 100 episodes | Network weights |

A network with frozen weights can produce different decisions every storage epoch because its inputs change.

### 9.1 Illustrative 100-episode batch schedule

    Freeze routing policy and export encoder.

    repeat:
        keep storage-model weights fixed for 100 episodes

        within every episode:
            every timestep:
                compute agent observations/messages/actions
                execute actions and collect outcomes

            every storage epoch:
                aggregate recent messages
                run storage model with unchanged weights
                assign arriving pallets
                refresh storage context

        train storage model on the batch
        evaluate without learning

The number 100 is not theoretically justified. It is an initial hyperparameter to test.

### 9.2 Better basis than episode count

Choose updates using:

- Number of storage epochs or placement transitions collected.
- Number of completed/censored labelled outcomes.
- Coverage of shelves, zones, loads, and demand patterns.
- Validation error or held-out policy performance.
- Runtime and sample-efficiency tradeoffs.

Example from the discussion: 100 episodes with 10 storage epochs each yield 1,000 storage-epoch observations; this is not necessarily 1,000 independent placement outcomes because each epoch can contain multiple pallets and observations are correlated.

### 9.3 Supervised versus PPO interpretation

If storage is a supervised delay predictor:

- Train it on labelled, versioned data.
- Replay can be useful with distribution/encoder-version controls.
- The batch need not correspond to exactly one policy update.

If storage is an RL policy trained with PPO:

- Collect fresh rollouts under the current storage policy.
- Perform the algorithm's limited optimisation passes on that batch.
- Then collect a new batch.
- Do not indefinitely replay arbitrarily old policy trajectories as if they were on-policy.
- Define the storage-level transition, action, reward, and next decision point, including variable intervals if relevant.

If the routing policy keeps learning within the 100 episodes, storage inputs and the effective environment move during collection. The recommended first prototype freezes routing rather than assuming a 100-episode lag solves this problem.

## 10. Evaluation and ablations

Proposed variants:

1. Existing scalar blocked-time feedback baseline.
2. Upward embedding only.
3. Downward storage context only.
4. Bidirectional embedding feedback.
5. Zeroed/shuffled message controls.
6. Explicit-feature interface with comparable model capacity.

Separate deadline-aware and deadline-free experiments. Otherwise, gains cannot be attributed to embeddings rather than urgency-aware assignment/rewards.

Keep constant where possible:

- Warehouse seeds.
- Exogenous customer orders and deadline rules.
- Stock arrivals.
- Capacity constraints.
- Conflict resolution.
- Training/evaluation budgets.

Possible metrics:

- Order service time, when fleet stability permits comparison.
- Served share/throughput and backlog.
- Blocking and detours.
- Deadlock incidence.
- Put-away cost.
- On-time rate and overdue unfinished orders if deadlines are enabled.
- Predictor calibration and coverage.
- Computation and communication cost.

Do not claim observed blocked-time prediction accuracy necessarily yields better placement. Evaluate downstream outcomes.

## 11. Corrections and cautions from earlier assistant responses

The following points supersede loose or incorrect statements earlier in the conversation:

1. **Deadline urgency sign:** the early-completion weighting was backwards; use a clearly defined slack/urgency measure instead.
2. **Embedding feedback does not imply deadlines.** Treat these as separable extensions.
3. **Do not add undefined shelf-indexed factors to the dock cost.** Earlier messages garbled the draft's notation into a term resembling `t_v * p_alt(k) * d_dock(v)`. The intended illustrative cost is pick frequency times pick cost plus pallet frequency times put-away cost. Check the PDF/LaTeX for original notation.
4. **Do not call the current encoder frozen if downward inputs change its input dimension without adaptation.** Preserve the old policy only during upward-only training; downward context requires an adapter or fine-tuning/training.
5. **Correct slack depends on agent and task phase.** Do not send an already-loaded agent back through its pickup in the estimate.
6. **An earlier candidate-agent assignment expression added a task-only urgency term to distance.** If the term is identical for all candidate agents, it cannot change which agent minimises the expression. Use urgency for task ordering or define candidate-specific estimated completion costs.
7. **Parallel order lines are not a sequential chain.** Reserve shipment time but do not blindly sum all other picks.
8. **Prediction is not causal optimisation.** Delays observed at a chosen shelf are not labels for all unchosen shelves.
9. **Latent coordinates are not inherently interpretable.** Avoid naming dimensions as queue/deadlock/urgency without supervision or probing.
10. **Global context can violate observation restrictions.** A local recipient does not make the source local.
11. **Placement does not immediately update available inventory.** Reserve capacity and create a put-away; actual delivery enables picks.
12. **Read-only halo means ownership, not necessarily frozen neural hidden states.** Differentiate simulator control permissions from temporary message-passing computation.
13. **A 100-episode update interval is an example, not a validated recommendation.** Choose from storage-level data and validation.
14. **The thesis's future-work wording:** alternating training is proposed to reduce the risk of two learners chasing one another; it was not evidence that alternating training itself necessarily causes that problem.
15. **Potential-based shaping needs conditions.** If proposed, specify state, discount, terminal treatment, and changing task identities. A generic slack potential with task switches is not automatically safe in every implementation.
16. **Peer review was not verified for every halo paper initially listed.** Do not repeat incomplete preprint references as a finished peer-reviewed shortlist.

## 12. Public research sources used as methodological leads

These support general mechanisms, not the complete proposed warehouse architecture.

### Learned communication

Jakob N. Foerster et al. (2016), *Learning to Communicate with Deep Multi-Agent Reinforcement Learning*, NeurIPS.

https://proceedings.neurips.cc/paper/2016/file/c7635bfd99248a2cdef8249ef7bfbef4-Paper.pdf

Relevant distinction: reinforced versus differentiable communication and deliberate training of message channels.

### Different decision timescales

Alexander Sasha Vezhnevets et al. (2017), *FeUdal Networks for Hierarchical Reinforcement Learning*, ICML.

https://proceedings.mlr.press/v70/vezhnevets17a/vezhnevets17a.pdf

Relevant analogy: slow manager representations and fast worker actions. Not a SLAP–MAPD solution.

Tejas D. Kulkarni et al. (2016), *Hierarchical Deep Reinforcement Learning: Integrating Temporal Abstraction and Intrinsic Motivation*.

https://collaborate.princeton.edu/en/publications/hierarchical-deep-reinforcement-learning-integrating-temporal-abs/

Relevant analogy: high-/low-level policies operating at distinct timescales. Verify full venue metadata before formal citation.

### Hierarchical nonstationarity

*Hierarchical Reinforcement Learning with Timed Subgoals* (HiTS), NeurIPS 2021.

https://proceedings.neurips.cc/paper/2021/file/b59c21a078fde074a6750e91ed19fb21-Paper.pdf

Relevant lead: changing lower-level policies change the higher-level learning problem. Retrieve complete author metadata if citing.

### Learned dynamic storage

Constantin Waubert de Puiseau et al. (2022), *Dynamic Storage Location Assignment in Warehouses Using Deep Reinforcement Learning*, Technologies 10(6), 129.

https://www.mdpi.com/2227-7080/10/6/129

Relevant precedent: learning dynamic storage assignment. Does not establish bidirectional agent-embedding feedback.

### Time-constrained graph routing

Marijn van Knippenberg, Mike Holenderski, and Vlado Menkovski (2021), *Time-Constrained Multi-Agent Path Finding in Non-Lattice Graphs with Deep Reinforcement Learning*, ACML, PMLR 157.

https://proceedings.mlr.press/v157/knippenberg21a.html

Mentioned by the thesis and conversation. Read the original paper before claiming exact deadline/reward/observation mechanisms.

## 13. Recommended starting design

This is the latest coherent proposal, not a commitment from the user:

1. Keep the existing warehouse simulator and physical constraints.
2. Freeze the existing routing policy/export encoder.
3. Export task-tagged agent representations.
4. Aggregate by current zone and separately by pickup shelf.
5. Train a delay predictor from explicit features plus embeddings.
6. Insert the predictor into the existing storage-ranking rule.
7. Refresh summaries and make placements at storage epochs within episodes.
8. Update predictor weights after a sufficiently large batch; test 100 episodes as one candidate.
9. Validate against scalar feedback and explicit-feature controls.
10. Add downward storage context and routing fine-tuning only after upward feedback proves useful.
11. Add deadlines as a separately controlled extension, not as an implicit consequence of embeddings.
12. Consider alternating/co-learning only after stable one-direction baselines exist.

## 14. Open decisions for the next LLM to resolve with the user

- Does the user want a learned delay estimator, an RL storage policy, or both?
- What code/network tensors already exist, and where can z_i be extracted?
- What is the current storage-epoch length and episode horizon?
- How many placement decisions and completed picks occur in 100 episodes?
- Is routing frozen during storage training, or is joint learning essential?
- Is downward communication required in the first experiment?
- Are deadlines actually being adopted, or merely being explored?
- What information is legally available to each controller variant?
- How are incomplete/locked tasks represented in training labels?
- Is shelf-level prediction sufficiently supported by data, or should the first model operate by zone?
- What is the exact delay-prediction target and horizon?
- What training/evaluation seeds and budgets are available?

Answer the user's next concrete question directly. Do not overwhelm them by asking all these questions at once. Resolve the few that matter to the requested implementation step.
