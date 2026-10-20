# Step-by-Step Guide to the Thesis (Coupled Storage–Routing in an Automated Warehouse)

This guide is meant as a **teaching and sketching aid** for your thesis. It:
- Walks through the system step by step.
- Uses simple examples that you (or another agent) can later turn into figures.
- Follows the structure of the updated Introduction and Problem Formulation.

Each section below has:
- A **plain-language description**.
- A **small concrete example**.
- A **"figure brief"**: what to draw.

---

## 1. Big Picture: Two Coupled Layers

### 1.1 Informal description

The warehouse has two decision layers:

- **Storage layer**: Decides **where items (SKUs) are stored** on shelves.
- **Transport layer**: Decides **which tasks robots execute and how they move** through the warehouse.

These layers are **coupled**:

- If you move a popular SKU closer to the delivery station, you change **where pickups happen** and thus change robot traffic.
- If robot traffic gets congested in some aisle, you change the **effective cost** of accessing storage in that aisle.

So optimising one layer while freezing the other can look good locally but be bad for the whole system.

**Thesis idea:** Treat this interaction as a **closed-loop system**. Storage responds to observed demand and traffic. Robots then run under that storage, generating new traffic that feeds back into storage decisions.

### 1.2 Example

Imagine a small warehouse:

- Storage shelves along two aisles: **Left aisle** and **Right aisle**.
- One delivery station at the bottom.

Case A (no feedback):
- Tea is stored far up the **Right aisle**.
- Robots always go up Right aisle to pick up tea, causing heavy congestion there.

Case B (with feedback):
- Storage sees that tea is requested often and that the Right aisle is congested.
- It moves some tea closer to the delivery station but on the **Left aisle**.
- Robots now use **both** aisles more evenly.

### 1.3 Figure brief

Draw two diagrams of the same warehouse:

1. **No feedback case**:
   - Tea storage far on the Right aisle.
   - Many arrows along the Right aisle showing heavy traffic.

2. **Feedback case**:
   - Tea storage moved closer via Left aisle.
   - Arrows showing more balanced traffic across Left and Right aisles.

Label: "Closed-loop coupling: storage changes routing, routing feeds storage."

---

## 2. The Warehouse as a Graph

### 2.1 Informal description

The warehouse is modelled as a **directed graph** \(G=(V,E)\):

- Vertices \(V\): discrete positions a robot can stand on.
  - Aisle cells.
  - Cross-aisle junctions.
  - Storage vertices \(V_{\mathrm{str}}\).
  - Delivery vertices \(V_{\mathrm{del}}\).
  - Endpoints \(V_{\mathrm{ep}}\) where robots can safely wait.

- Directed edges \(E\): allowed movements between positions.
  - One-way aisles: \((v,w) \in E\) does **not** imply \((w,v) \in E\).

Each edge has a **traversal cost** \(c(v,w) > 0\), e.g. the time or distance to move from vertex \(v\) to vertex \(w\).

Shortest-path distance \(d_G(v,w)\) is defined on the subgraph containing only occupiable vertices \(V_{\mathrm{mov}}\).

### 2.2 Example

Consider a tiny 4-vertex warehouse:

- Vertices: \(A, B, C, D\).
- Roles:
  - \(A\): delivery vertex.
  - \(B, C\): storage vertices.
  - \(D\): transit vertex.

Edges:

- \(A \rightarrow B\), \(B \rightarrow C\), \(C \rightarrow D\).
- Also \(D \rightarrow A\) to complete a loop.

One-way segment:

- There is an edge \(B \rightarrow C\) but **no** \(C \rightarrow B\), so robots can go forward along the aisle but not backwards.

### 2.3 Figure brief

Draw a small graph with labeled vertices:

- Shapes encode roles: squares for storage, circles for delivery, triangles for endpoints.
- Arrows show directed edges.
- Highlight a one-way edge with a single arrow.

Annotate one pair \(v,w\) with \(d_G(v,w)\): e.g. distance from A to C via B.

---

## 3. Actions: Wait or Move

### 3.1 Informal description

At each timestep, a robot at vertex \(v\) has a **local action set**:

\[
\mathcal{U}(v) = \{\mathrm{wait}\} \cup \{\mathrm{move}(w) : w \in N^{+}(v)\}.
\]

- \(N^{+}(v)\): the set of reachable successor vertices from \(v\):

  \[
  N^{+}(v) = \{w \in V_{\mathrm{mov}} : (v,w) \in E\}.
  \]

So each step, the agent chooses **either**:

- \(\mathrm{wait}\): stay at \(v\).
- \(\mathrm{move}(w)\): move along an outgoing edge to \(w\).

The one-step cost is:

\[
\hat{c}(v,w) =
  \begin{cases}
    c_{\mathrm{wait}}, & v = w, \\
    c(v,w), & (v,w) \in E.
  \end{cases}
\]

### 3.2 Example

Take vertex \(A\) with edges to \(B\) and \(C\):

- \(N^{+}(A) = \{B, C\}\).
- \(\mathcal{U}(A) = \{\mathrm{wait}, \mathrm{move}(B), \mathrm{move}(C)\}\).

If the agent chooses:

- \(u(t) = \mathrm{wait}\): \(\ell(t+1) = \ell(t) = A\) and cost \(\hat{c}(A,A) = c_{\mathrm{wait}}\).
- \(u(t) = \mathrm{move}(B)\): \(\ell(t+1) = B\) and cost \(\hat{c}(A,B) = c(A,B)\).

A legal transition is exactly one of:

- \(\ell_i(t+1) = \ell_i(t)\) (wait), or
- \((\ell_i(t),\ell_i(t+1)) \in E\) (move along an edge).

### 3.3 Figure brief

Draw a vertex \(A\) with outgoing arrows to \(B\) and \(C\):

- Show \(N^{+}(A) = \{B,C\}\).
- Draw two example sequences:
  - Route with a wait: \(A \rightarrow A\).
  - Route with a move: \(A \rightarrow B\).

Annotate each step with \(\hat{c}(v,w)\).

---

## 4. Collisions: Vertex and Swap Conflicts

### 4.1 Informal description

Individual moves can be legal, but robots share infrastructure. There are two kinds of **collision**:

1. **Vertex conflict**: two robots end a timestep on the **same vertex**.

   \[
   \ell_i(t+1) \neq \ell_j(t+1) \quad \forall i \neq j.
   \]

2. **Swap conflict**: two robots **exchange positions** across a single edge in one timestep.

   \[
   \neg(\ell_i(t) = \ell_j(t+1) \wedge \ell_j(t) = \ell_i(t+1)) \quad \forall i \neq j.
   \]

A joint move is **collision-free** only if **both** conditions hold.

### 4.2 Example

Consider two robots \(R_1\) and \(R_2\) and two vertices \(U\) and \(V\).

- At time \(t\):
  - \(\ell_1(t) = U\).
  - \(\ell_2(t) = V\).

**Vertex conflict example**:

- Both decide to move onto a shared vertex \(W\):
  - \(\ell_1(t+1) = W\), \(\ell_2(t+1) = W\).
- This violates the vertex-conflict condition.

**Swap conflict example**:

- \(R_1\): moves from \(U\) to \(V\).
- \(R_2\): moves from \(V\) to \(U\).
- Then \(\ell_1(t+1) = V\), \(\ell_2(t+1) = U\).
- Individually both moves are legal edges, but together they form a swap conflict.

**Feasible alternative**:

- \(R_1\) moves from \(U\) to \(V\).
- \(R_2\) waits at \(V\) or at some endpoint.
- One robot yields; the joint move is collision-free.

### 4.3 Figure brief

Draw three panels:

1. Vertex conflict:
   - Two robots moving into the same cell \(W\).
2. Swap conflict:
   - One robot at \(U\), one at \(V\); arrows crossing to exchange positions.
3. Resolution:
   - One robot waits, the other moves.

Highlight the corresponding constraints in each panel.

---

## 5. Storage State: Where Items Live

### 5.1 Informal description

Storage lives at vertices \(V_{\mathrm{str}}\). The storage state is:

\[
x_t : \mathcal{K} \times V_{\mathrm{str}} \to \mathbb{N}_0,
\]

where \(x_t(k,v)\) is the **number of units of SKU \(k\) stored at vertex \(v\) at time \(t\)**.

The model supports:

- Multiple units of one SKU at a vertex.
- Split inventory (same SKU at several vertices).
- Shared shelves (different SKUs at the same vertex).

Each unit has a capacity footprint \(b_k\). Each storage vertex \(v\) has capacity \(\mathrm{cap}(v)\). Feasible configurations obey:

\[
\sum_{k \in \mathcal{K}} b_k x(k,v) \le \mathrm{cap}(v) \quad \forall v \in V_{\mathrm{str}}.
\]

### 5.2 Example

Three SKUs: tea, coffee, mugs.

Three storage vertices: A, B, C.

Storage matrix example:

|       | A  | B  | C  |
|-------|----|----|----|
| tea   | 12 | 0  | 5  |
| coffee| 4  | 3  | 0  |
| mugs  | 0  | 6  | 2  |

Suppose per-unit capacities:

- \(b_{\mathrm{tea}} = 1\), \(b_{\mathrm{coffee}} = 2\), \(b_{\mathrm{mugs}} = 1\).

Vertex capacities:

- \(\mathrm{cap}(A) = 20\), \(\mathrm{cap}(B) = 15\), \(\mathrm{cap}(C) = 10\).

Compute capacity use per vertex:

- At A: \(1\cdot 12 + 2\cdot 4 + 1\cdot 0 = 12 + 8 + 0 = 20\) \(\Rightarrow\) exactly full.
- At B: \(1\cdot 0 + 2\cdot 3 + 1\cdot 6 = 0 + 6 + 6 = 12 \le 15\).
- At C: \(1\cdot 5 + 2\cdot 0 + 1\cdot 2 = 5 + 0 + 2 = 7 \le 10\).

So the configuration is feasible.

### 5.3 Figure brief

Draw a table (matrix) of SKUs vs storage vertices:

- Show counts \(x_t(k,v)\).
- Next to it, draw bars showing capacity used vs capacity at A, B, C.

Label: "Feasible storage configuration under per-vertex knapsack constraints".

---

## 6. Storage Updates: Slow Feedback Loop

### 6.1 Informal description

Storage is updated periodically, every \(\Delta\) timesteps:

\[
x_t = F\bigl(x_{t-\Delta},\, \hat{\rho}_t,\, \hat{\mu}_t,\, \hat{w}_t\bigr) \in \mathcal{X}.
\]

Inputs to \(F\):

- \(x_{t-\Delta}\): previous configuration.
- \(\hat{\rho}_t\): demand estimate per SKU.
- \(\hat{\mu}_t(e)\): edge traversal counts (traffic intensity).
- \(\hat{w}_t(e)\): waiting attributed to edges (contention).

The rule \(F\) chooses a new configuration by minimising a tradeoff:

\[
x_t \in \arg\min_{x \in \mathcal{X}} \left[ \alpha D(x; \hat{\rho}_t)
+ \beta K(x; \hat{\mu}_t, \hat{w}_t)
+ \chi R(x, x_{t-\Delta}) \right].
\]

- \(D\): access distance for popular items.
- \(K\): predicted congestion exposure.
- \(R\): reassignment cost (how much you move stuff).

### 6.2 Example

Suppose tea demand increases, and traffic statistics show that the aisle near vertex A is heavily congested.

- \(\hat{\rho}_t(\mathrm{tea})\): high.
- \(\hat{\mu}_t\), \(\hat{w}_t\): indicate high traffic and waiting near A.

Storage rule \(F\) may react by:

- Moving some tea units from A to a less congested vertex B or C.
- Doing so only if capacity \(\mathrm{cap}(B), \mathrm{cap}(C)\) allows it.
- Trading off the improvement in access and congestion vs the cost of relocation \(R\).

### 6.3 Figure brief

Draw two maps of the same warehouse:

1. **Before update**: heavy traffic arrows near A; tea mostly stored at A.
2. **After update**: tea partially moved to B or C; traffic arrows more spread out.

Overlay an inset showing the three terms \(D, K, R\) as bars to illustrate their tradeoff.

---

## 7. Tasks: What Robots Actually Do

### 7.1 Informal description

Customer orders are drawn from a distribution \(P_{\mathrm{ord}}\) and converted into one or more **transport tasks**.

A task is:

\[
\tau_j = (t_j^{\mathrm{released}}, s_j, g_j, k_j)
\]

- \(t_j^{\mathrm{released}}\): release time.
- \(s_j\): pickup vertex (must be in \(V_{\mathrm{str}}\)).
- \(g_j\): delivery vertex (in \(V_{\mathrm{del}}\)).
- \(k_j\): requested SKU.

The pickup vertex is **constrained by storage**:

\[
x_{t_j^{\mathrm{released}}}(k_j, s_j) > 0.
\]

This is the formal coupling: you can only create a task that picks up SKU \(k_j\) at \(s_j\) if there is stock there at release time. Changing \(x_t\) changes where tasks can pick up items.

Tasks go through three lifecycle sets:

- Waiting \(\mathcal{Q}_t\): released but not yet assigned.
- Active \(\mathcal{B}_t\): assigned to a robot, not yet finished.
- Completed \(\mathcal{C}_t\): finished.

Service time:

\[
\zeta_j = t_j^{\mathrm{finish}} - t_j^{\mathrm{released}}.
\]

### 7.2 Example

Given storage matrix above, consider task:

- \(\tau_1 = (5, A, g_1, \mathrm{tea})\).

Check coupling:

- \(x_5(\mathrm{tea}, A) = 12 > 0\) \(\Rightarrow\) task is legal.

Lifecycle example:

- Released at \(t_j^{\mathrm{released}} = 5\).
- Assigned at \(t_j^{\mathrm{assigned}} = 9\).
- Pickup at \(t_j^{\mathrm{pickup}} = 11\).
- Finish at \(t_j^{\mathrm{finish}} = 14\).

Sets:

- \(\tau_1 \in \mathcal{Q}_t\) for \(t = 5,6,7,8\).
- \(\tau_1 \in \mathcal{B}_t\) for \(t = 9,10,11,12,13\).
- \(\tau_1 \in \mathcal{C}_t\) for \(t \ge 14\).

Service time: \(\zeta_1 = 14 - 5 = 9\) timesteps.

### 7.3 Figure brief

Draw a timeline for one task:

- Mark four times: release, assignment, pickup, finish.
- Colour the segment \([t^{\mathrm{released}},t^{\mathrm{assigned}})\) as "waiting".
- Colour \([t^{\mathrm{assigned}}, t^{\mathrm{finish}})\) as "active".
- Show \(\zeta_j\) spanning both segments.

Label: "Service time includes both waiting and active phases".

---

## 8. Controllers: Who Decides What

### 8.1 Informal description

A controller \(\pi\) does two things:

1. **Task assignment** \(\pi^{\mathrm{assign}}\): which free agent gets which waiting task.
2. **Routing** \(\pi^{\mathrm{route}}\): given agent targets and information, choose actions \(u_i(t) \in \mathcal{U}(\ell_i(t))\).

Three architectures differ in **what information** they can condition on:

- **Centralised**:
  - Assignment: global state.
  - Routing: global state.

- **Section-based**:
  - Assignment: zone-local state + boundary protocol.
  - Routing: zone-local state.

- **Decentralised**:
  - Assignment: global state (held fixed across arms, for fairness in comparison).
  - Routing: **local observations \(o_i(t)\) only**.

Assignment is kept identical across architectures so that differences in performance are due to routing.

### 8.2 Example

Small graph partitioned into zones:

- \(V_{\mathrm{mov}} = \{A,B,C,D,E,F\}\).
- Zones: \(Y_1 = \{A,B,C\}\), \(Y_2 = \{D,E,F\}\).

Section-based controller:

- A robot in \(Y_1\) sees only state and congestion in \(Y_1\) plus boundary rules.
- A robot in \(Y_2\) sees only its zone.

Decentralised controller:

- Each robot sees only a neighbourhood within depth \(d_{\mathrm{obs}}\) and uses \(o_i(t)\) to decide.

### 8.3 Figure brief

Draw three panels over the same warehouse graph:

1. Centralised: entire graph highlighted.
2. Section-based: two zones shaded; each controller sees only its zone.
3. Decentralised: one agent’s local neighbourhood circle; only vertices and agents inside are highlighted.

---

## 9. What a Decentralised Agent Sees

### 9.1 Informal description

A decentralised agent doesn’t see the whole warehouse. It builds a local observation \(o_i(t)\) from four components:

1. **Local map**: vertices and edges within observation depth \(d_{\mathrm{obs}}\).

   \[
   V^{(d_{\mathrm{obs}})}_i(t) = \{ v \in V_{\mathrm{mov}} : d_G(\ell_i(t), v) \le d_{\mathrm{obs}} \},
   \]
   \[
   \mathcal{G}^{(d_{\mathrm{obs}})}_i(t) = G\bigl[V^{(d_{\mathrm{obs}})}_i(t)\bigr].
   \]

2. **Direction to target**: for each visible vertex \(v\), the distance to the current target \(q_i(t)\):

   \[
   q_i(t) =\begin{cases}s_j, & t < t_j^{\mathrm{pickup}}, \\
   g_j, & t \ge t_j^{\mathrm{pickup}},\end{cases}
   \]
   \[
   \eta_i(v,t) = d_G\bigl(v, q_i(t)\bigr).
   \]

3. **Local congestion**: fraction of nearby vertices within radius \(r_{\mathrm{cng}}\) that are occupied by other agents:

   \[
   \delta_i(t) = \delta\bigl(V^{(r_{\mathrm{cng}})}_i(t), t; \{a_i\}\bigr).
   \]

4. **Messages from nearby agents**: from agents within communication radius \(r_{\mathrm{com}}\), via communication graph \(G^{\mathcal{A}}_t\).

These are packaged as:

\[
o_i(t) = \bigl( \mathcal{G}^{(d_{\mathrm{obs}})}_i(t),\; \eta_i(\cdot, t),\; \delta_i(t),\; \text{messages from neighbours}\bigr).
\]

### 9.2 Example

Consider an agent at vertex \(A\), with observation depth \(d_{\mathrm{obs}} = 2\).

Local map:

- Visible vertices: all vertices at graph distance \(\le 2\) from \(A\).
- Subgraph includes all edges between those visible vertices.

Target distance:

- Suppose current target \(q_i(t) = C\).
- For visible vertices \(B\) and \(C\):
  - \(\eta_i(B,t) = d_G(B,C) = 2\).
  - \(\eta_i(C,t) = d_G(C,C) = 0\).

Congestion:

- Within radius \(r_{\mathrm{cng}}\), count how many vertices have other agents.
- Compute fraction of occupied vertices in that neighbourhood.

Communication:

- Another agent at vertex \(D\) is within \(r_{\mathrm{com}}\) hops of \(A\).
- They can exchange a message (e.g. "I intend to move to B"), which becomes part of \(o_i(t)\).

### 9.3 Figure brief

Draw one agent’s local observation:

- Warehouse graph faded except within a shaded circle corresponding to \(d_{\mathrm{obs}}\).
- Numbers at visible vertices showing \(\eta_i(v,t)\) (distance to target).
- A shaded inner region showing congestion radius \(r_{\mathrm{cng}}\); annotate \(\delta_i(t)\).
- Dashed circle showing communication radius \(r_{\mathrm{com}}\); draw arrows indicating messages from nearby agents.

---

## 10. The Learning Problem (POSG View)

### 10.1 Informal description

Because each agent acts based on \(o_i(t)\) and the environment evolves under the joint actions of all agents, the setting is a **partially observable stochastic game (POSG)**:

\[
\mathcal{M} = \bigl( \mathcal{A},\, \mathcal{S},\, \{\mathcal{U}_i\},\, P,\, \{\mathcal{O}_i\},\, \{O_i\},\, \{R_i\},\, \gamma \bigr).
\]

You already define each component in Problem Formulation, so here the POSG packaging is just a clean way to view the multi-agent RL problem.

Agents are homogeneous and cooperative, sharing parameters \(\theta\). The objective is:

\[
\max_{\theta} J(\theta) = \max_{\theta} \mathbb{E}_{\pi_\theta} \Bigl[ \sum_{t=0}^{T-1} \gamma^{t}\, \frac{1}{m} \sum_{i=1}^{m} R_i(t) \Bigr].
\]

### 10.2 Example

Consider one decentralised controller:

- Observation \(o_i(t)\) as defined above.
- Policy \(\pi_\theta\) that maps \(o_i(t)\) to a distribution over actions \(\mathcal{U}(\ell_i(t))\).
- Rewards \(R_i(t)\) shaped to encourage low service time and low congestion.

The learning loop trains \(\theta\) so that the resulting policy performs well under the closed-loop storage–routing system.

### 10.3 Figure brief

Draw a schematic diagram:

- POSG block labeled \(\mathcal{M}\).
- Arrows from state \(s_t\) to observations \(o_i(t)\) for each agent.
- Arrows from \(o_i(t)\) to actions via \(\pi_\theta\).
- Environment dynamics block labeled \(P\) updating \(s_{t+1}\).

---

## 11. Closing the Loop: Two Timescales

### 11.1 Informal description

State \(s_t\) includes robot positions, task sets \(\mathcal{Q}_t,\mathcal{B}_t,\mathcal{C}_t\), and storage \(x_t\).

The system has **two clocks**:

1. **Fast clock** (every timestep):

   \[
   s_{t+1} \sim P(\cdot \mid s_t, u_t), \quad u_t \sim \pi(\cdot \mid s_t).
   \]

2. **Slow clock** (every \(\Delta\) timesteps):

   Apply storage update \(F\) using \(x_{t-\Delta}\), \(\hat{\rho}_t\), \(\hat{\mu}_t\), \(\hat{w}_t\).

Forward direction:

- Changing \(x_t\) changes pickup vertices via \(x_{t_j^{\mathrm{released}}}(k_j,s_j) > 0\), so it changes the routing problem.

Backward direction:

- Realised routing traffic and waiting feed \(\hat{\mu}_t\), \(\hat{w}_t\), influencing the next storage decision.

### 11.2 Example

Consider a simulation run:

- Timesteps 0–99: robots move, tasks are assigned and completed, traffic and waiting are logged.

At timestep 100 (storage epoch):

- Compute \(\hat{\rho}_{100}\), \(\hat{\mu}_{100}\), \(\hat{w}_{100}\).
- Apply storage rule \(F\) to obtain \(x_{100}\).

Next 100 timesteps:

- Robots operate under new \(x_{100}\), generating a new pattern of traffic.

### 11.3 Figure brief

Draw a two-layer diagram:

- Top layer: fast loop (tasks and routing) with arrows from state \(s_t\) through \(\pi\) to \(s_{t+1}\).
- Bottom layer: slow loop (storage update) applied every \(\Delta\) steps.
- Arrows from storage to tasks (via \(x_t\Rightarrow s_j\)), and from routing statistics back to storage estimates \(\hat{\mu}_t, \hat{w}_t\).

---

## 12. Scoring a Run

### 12.1 Informal description

Key quantities:

- **Throughput**:

  \[
  \Lambda_T = \frac{|\mathcal{C}_T|}{T}.
  \]

- **Mean service time**:

  \[
  \bar{\zeta}_T = \frac{1}{|\mathcal{C}_T|}
  \sum_{\tau_j \in \mathcal{C}_T} (t_j^{\mathrm{finish}} - t_j^{\mathrm{released}}).
  \]

- **Movement cost per completed task**:

  \[
  \bar{c}_T = \frac{\sum_{i=1}^{m} \sum_{t=0}^{T-1}
  \hat{c}(\ell_i(t),\ell_i(t+1))}{|\mathcal{C}_T|}.
  \]

- **Traffic concentration** via entropy \(H_T\) and its complement \(C_T\).

- **Backlog** \(B_T = |\mathcal{Q}_T| + |\mathcal{B}_T|\).

- **Post-assignment waiting** \(W_T\).

The overall system-level criterion:

\[
\mathcal{J}(F,\pi) = q_{\mathrm{svc}}\, \mathbb{E}[\bar{\zeta}_T]
+ q_{\mathrm{mov}}\, \mathbb{E}[\bar{c}_T]
+ q_{\mathrm{wait}}\, \mathbb{E}[W_T]
+ q_{\mathrm{conc}}\, \mathbb{E}[C_T]
+ q_{\mathrm{back}}\, \mathbb{E}[B_T].
\]

Throughput \(\Lambda_T\) and runtime \(\kappa_T\) are reported separately.

### 12.2 Example

Suppose over horizon \(T=1000\):

- \(|\mathcal{C}_T| = 800\): 800 tasks completed.
- Sum of service times \(\sum_{j \in \mathcal{C}_T} \zeta_j = 7200\).
- Sum of movement costs \(\sum_{i,t} \hat{c}(\ell_i(t),\ell_i(t+1)) = 40000\).

Then:

- \(\Lambda_T = 800/1000 = 0.8\) tasks per timestep.
- \(\bar{\zeta}_T = 7200/800 = 9\) timesteps per task.
- \(\bar{c}_T = 40000/800 = 50\) cost units per task.

### 12.3 Figure brief

Draw:

- A histogram of service times \(\zeta_j\).
- A bar chart comparing \(\bar{\zeta}_T\), \(\bar{c}_T\), \(C_T\), \(B_T\) across different experimental conditions.

---

## 13. Formal Decision Problem and Research Question

### 13.1 Informal description

Formally, the decision problem is:

\[
(F^{\star}, \pi^{\star}) \in \arg\min_{F \in \mathcal{F},\, \pi \in \Pi} \mathcal{J}(F,\pi)
\]

subject to the feasibility constraints:

- Storage capacity: \(\mathcal{X}\).
- Legal individual transitions.
- Collision avoidance.
- Task–storage coupling.

The thesis does **not** solve this globally. Instead, it compares selected combinations of \(F\) and \(\pi\) under a factorial design and asks empirically:

> Does there exist an adaptive storage rule \(F\) such that \(\mathcal{J}(F,\pi) < \mathcal{J}(F_{\mathrm{fix}},\pi)\) by more than seed variance, and how does that effect depend on controller architecture, congestion sensitivity, and load parameters?

### 13.2 Example

Compare two settings:

- Fixed storage \(F_{\mathrm{fix}}\) + decentralised controller.
- Adaptive storage \(F\) + decentralised controller.

Run many seeds in each, estimate mean \(\mathcal{J}\), and test whether the adaptive combination significantly improves \(\mathcal{J}\) and under which loads.

### 13.3 Figure brief

Draw a high-level diagram:

- Axis: controller architectures (centralised / section-based / decentralised).
- Axis: storage mode (fixed vs adaptive).
- Each cell: a box showing key metrics and whether \(F\) improves over \(F_{\mathrm{fix}}\).

---

This markdown file is meant to be a **bridge** between your formal Problem Formulation and visual intuition. Each example is small enough to be drawn as a figure but structured enough to match the symbols and equations already used in your thesis.