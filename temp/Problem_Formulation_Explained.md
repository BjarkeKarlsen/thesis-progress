# Understanding the Problem Formulation — A Study Guide

This is **not** thesis text. `problem_formulation_fixed.tex` is written for a
committee that already knows the field; it is terse on purpose, and every
sentence in it earns its place against a page-count budget. This document has
no such budget. Its only job is to get *you* to the point where you can read
that file and immediately know why every symbol is there, what would break if
it were removed, and how it connects to the symbol before and after it.

Read this once alongside the six figures in `../Images/` (`instance.png`,
`conflicts.png`, `lifecycle.png`, `observation.png`, `loop.png`,
`concentration.png`) — they were built from the exact same example used
throughout this guide, so every abstract symbol below has a picture you can
point at.

---

## 0. The one-sentence version

A warehouse is a graph; robots move on it to fulfil tasks; where stock is
*stored* changes which tasks look easy, and how the robots *move* changes what
the storage layer knows about congestion — so the two decisions feed each
other, and this thesis is about what happens when you let them.

Everything below is one of two things: an object needed to state that
sentence precisely, or a quantity needed to check afterwards whether letting
them feed each other actually helped.

---

## 1. The running example

Fix one concrete picture in your head before any formalism — it's the exact
instance `../Images/instance.png` draws.

- The warehouse is a 5-row grid: row 0 and row 4 are **cross-aisles** running
  the full width; rows 1–3 are **storage racks** at every even column
  (0, 2, 4, 6, 8), each rack a short vertical corridor connecting the top
  cross-aisle to the bottom one.
- Roles: the blue circles are storage faces ($V_{\mathrm{str}}$), the orange
  squares are delivery points ($V_{\mathrm{del}}$, at `0_0` and `4_8`), the
  green diamonds are endpoints ($V_{\mathrm{ep}}$, where an idle robot may
  park), and the white circles are plain transit vertices.
- Three robots are shown: $a_1$ at `4_0`, $a_2$ at `2_4`, $a_3$ at `0_6`.
- One task is drawn: $\tau_j$ with pickup $s_j = $ `2_6` and delivery
  $g_j = $ `0_0`, shown as the dashed red route.
- **One rack segment is one-way**: the top-right rack (column 8) can only be
  traversed downward, `1_8 → 2_8`, not the reverse — every other edge in the
  picture works both ways. This is the one deliberately irregular thing in an
  otherwise regular-looking layout, and it exists specifically so that
  "directed graph" isn't just a word in the text.

Keep this picture open. Every section below refers back to it.

---

## 2. The environment (`sec:pf:env`)

**Plain picture.** The warehouse is a map: places a robot can be, and moves
it can make between them. That's it — everything else in this subsection is
making that map precise enough to compute with.

**The graph.** $G = (V, E)$ is **directed**. This is the single most
easily-missed fact in the whole formulation, so it's worth over-explaining:
directed does *not* just mean "you can draw an arrow on it." It means the
edge set is a set of *ordered* pairs, so $(v,w) \in E$ tells you nothing
about whether $(w,v) \in E$. In the running example, `1_8 → 2_8` exists but
`2_8 → 1_8` does not — an agent standing at `2_8` cannot use that segment to
get back up to `1_8` at all; it has to go the long way round through a
cross-aisle. Every *other* pair of adjacent vertices in the picture has edges
in both directions, but that's a fact about *this instance*, not something
the model assumes. Nothing downstream — cost, shortest paths, observations —
is allowed to secretly assume symmetry.

**The four roles.** $V_{\mathrm{mov}} \subseteq V$ is "occupiable at all."
$V_{\mathrm{str}}, V_{\mathrm{del}} \subseteq V_{\mathrm{mov}}$ (storage,
delivery) are occupiable *because* a pickup or dropoff literally means "an
agent is standing here." $V_{\mathrm{ep}} \subseteq V_{\mathrm{mov}}$ is
"legal to idle at, without blocking anyone passing through." These four sets
are allowed to overlap — nothing forces a storage face to *not* also be an
endpoint — a generated instance will typically keep them separate for
realism, but the formulation doesn't lean on that.

**Cost.** Every edge $e=(v,w)$ has a cost $c(e) = c(v,w) > 0$. $d_G(v,w)$ is
the cheapest directed path cost from $v$ to $w$ — and because $G$ is
directed, $d_G(v,w) \ne d_G(w,v)$ in general (in the running example,
$d_G(\texttt{1\_8}, \texttt{2\_8})$ is one hop; $d_G(\texttt{2\_8},
\texttt{1\_8})$ has to detour through a cross-aisle, and *is a different,
larger number*). This asymmetry is exactly what a one-way aisle should
produce — if your intuition says "shouldn't distance be symmetric," that
intuition is calibrated on undirected roads, not one-way ones.

**Connectivity, weakened on purpose.** The model only requires $d_G(v,w)$ to
be finite for pairs that actually get used (every occupiable vertex can reach
every vertex it's ever sent to). This is deliberately *weaker* than "every
vertex can reach every other vertex" (full strong connectivity), which is
what Knippenberg et al.'s source paper assumes outright. The weaker version
is what lets an instance contain an unreachable maintenance spur without the
whole model breaking — whether that's ever actually exercised by generated
instances is a separate, still-open question (see `sec:impl:instances`).

**Actions and one-step cost.** At vertex $v$, an agent can wait or move to
any $w$ with $(v,w) \in E$:
$\mathcal{U}(v) = \{\mathrm{wait}\} \cup \{\mathrm{move}(w) : (v,w) \in E\}$.
The realised cost of a step is $c_{\mathrm{wait}}$ if the agent stayed put,
or $c(v,w)$ if it moved — two cases, not one, purely because $(v,v)$ (a
self-loop) is never an element of $E$, so $c$ has nothing to say about
waiting; $\hat c(v,w)$ is the function that patches that gap.

> **Common confusion.** $c(e)$, $c(v,w)$, and $\hat c(v,w)$ are the *same
> number* for a real move — $c(v,w)$ is just $c(e)$ written with the edge
> spelled out as its endpoints. $\hat c$ is the only one of the three that
> also knows what to do about waiting.

---

## 3. Agents and collisions (`sec:pf:agents`)

**Plain picture.** The environment section describes one robot's options.
This section is what happens the instant there's more than one — because
now they can crash into each other, and the graph alone says nothing about
that.

A fleet $\mathcal{A} = \{a_1, \ldots, a_m\}$ shares $G$. Agent $a_i$'s
position is $\ell_i(t)$; a move is legal solo if it stays put or follows a
real edge (`eq:transition`) — but legal solo moves can still collide as a
*joint* action. Two distinct failure modes, and `../Images/conflicts.png`
draws exactly these three panels:

- **(a) Vertex conflict** — two agents end up at the same vertex.
  `eq:vertexconflict`: $\ell_i(t{+}1) \ne \ell_j(t{+}1)$ for all $i \ne j$.
- **(b) Swap conflict** — two agents cross the *same edge in opposite
  directions* in one step, i.e. they'd have to pass through each other.
  `eq:swapconflict` catches this specifically because (a) is blind to it: a
  swap never puts two agents at the same vertex at the same time, it's only
  visible if you look at *both* $t$ and $t{+}1$ together.
- **(c) The fix that's always available** — waiting is legal everywhere, so
  one agent can always yield. *Which* agent yields is left as a decision
  (Method's job, `sec:method:resolution`) — the Problem Formulation only
  guarantees a feasible choice exists, never picks one.

These two constraints are **hard**: a trace that violates either one isn't a
worse solution, it isn't a solution.

---

## 4. Where the items are — storage (`sec:pf:storage`)

**Plain picture.** Before anything can be picked up, it has to be *somewhere*.
This section is the entire state of "what's on which shelf," plus the rule
that's allowed to rearrange it.

**The state.** $x_t : \mathcal{K} \times V_{\mathrm{str}} \to \mathbb{N}_0$
counts units: $x_t(k, v)$ is "how many units of SKU $k$ sit at storage vertex
$v$ at time $t$." A worked mini-example, two SKUs at one storage vertex `1_0`
with $\mathrm{cap}(\texttt{1\_0}) = 100$: if helmets take $b_{\mathrm{helmet}}
= 1$ unit of shelf space each and batteries take $b_{\mathrm{battery}} = 2$,
then $x_t(\mathrm{helmet}, \texttt{1\_0}) = 40$ and
$x_t(\mathrm{battery}, \texttt{1\_0}) = 20$ is feasible because
$40 \cdot 1 + 20 \cdot 2 = 80 \le 100$ — that inequality, checked at *every*
storage vertex simultaneously, is exactly `eq:feasiblestorage`. It's a system
of knapsack constraints, one per vertex, which is why two SKUs' placements
aren't independent decisions: they're fighting over the same 100 units of
shelf space.

**The update rule.** Storage moves on a *slow clock* — only at epochs
$t \in \{\Delta, 2\Delta, \ldots\}$ — via
$x_t = F(x_{t-\Delta}, \hat\rho_t, \hat\mu_t, \hat w_t)$. The three hatted
inputs are *causal estimates*, computed only from data available strictly
before the epoch: $\hat\rho_t$ guesses per-SKU demand, $\hat\mu_t(e)$ guesses
edge traffic, $\hat w_t(e)$ guesses waiting. $F_{\mathrm{fix}}(x,\cdot)=x$
(never move anything) is one specific, always-available choice of $F$ — the
baseline the whole thesis compares against.

**Why it's an optimisation, not a formula.** $x_t$ is chosen to minimise a
weighted sum of three named pressures:
$\alpha D(x;\hat\rho_t) + \beta K(x;\hat\mu_t,\hat w_t) + \chi R(x, x_{t-\Delta})$
— $D$ pulls popular SKUs close to delivery, $K$ pushes them apart so they
don't all share one corridor, $R$ resists moving things that don't need to
move. None of $D$, $K$, $R$ have a stated formula yet — on purpose; the exact
functional forms are a Method-level choice (`sec:method:storage`), because a
different thesis could pick different ones and still be studying the same
*problem*.

> **Why this matters for the thesis.** $\beta$ is literally the
> congestion-sensitivity switch for storage: $\beta = 0$ means the storage
> layer never looks at traffic at all, $\beta > 0$ means it does. RQ3 is a
> question about this one knob (plus its routing-side counterpart, §6 below).

---

## 5. Where the work comes from — tasks (`sec:pf:tasks`)

**Plain picture.** Orders arrive; each becomes a job for exactly one robot:
go get SKU $k_j$ from $s_j$, bring it to $g_j$.

$\tau_j = (r_j, s_j, g_j, k_j)$ — release time, pickup vertex, delivery
vertex, requested SKU. In `instance.png`, that's the task with
$s_j=$`2_6`$, g_j=$`0_0`.

**The coupling condition — the most important equation in the section.**
$x_{r_j}(k_j, s_j) > 0$. In words: the pickup vertex isn't just *a* storage
face, it has to actually hold stock of the requested SKU *right now*. This
one inequality is the entire bridge between the two layers: change $x_t$
(storage's decision) and you change *which vertices ever get visited as
pickups* (routing's problem). Every other equation in this document exists
either to define something this inequality needs ($x_t$, $s_j$, $k_j$), or
to measure the consequence of it changing.

**The lifecycle.** Three timestamps — release $r_j$, assignment $y_j$,
completion $d_j$, with $r_j \le y_j \le d_j$ — carve a task's life into three
sets that are disjoint *by construction*, not by a separately-checked rule:
$\mathcal{Q}_t$ (waiting, $r_j \le t < y_j$), $\mathcal{B}_t$ (active,
$y_j \le t < d_j$), $\mathcal{C}_t$ (completed, $d_j \le t$). See
`../Images/lifecycle.png` — the three intervals tile the timeline with no
gaps and no overlaps because that's what three consecutive half-open
intervals do, automatically. Service time $\zeta_j = d_j - r_j$ spans *both*
phases, which is stated explicitly so nobody mistakes "assign it fast" for
"deliver it fast" — a controller that assigns instantly but then dawdles
gets no credit.

---

## 6. Who decides — controllers (`sec:pf:controllers`)

**Plain picture.** Something has to decide (a) which free agent goes after
which waiting task, and (b) how that agent actually moves there,
collision-free. A controller $\pi = (\pi^{\mathrm{assign}}, \pi^{\mathrm{route}})$
is both jobs together, kept as two separate maps so a routing algorithm
never gets silently credited (or blamed) for assignment quality.

**Three architectures, one axis of difference.** Centralised, section-based,
decentralised — the *only* thing distinguishing them at this level is what
information $\pi^{\mathrm{route}}$ is allowed to see (Table 1: global state /
zone-local state / $o_i(t)$ only). Task assignment is held identical across
all three, on purpose, so a result difference can only be attributed to
routing, never to a lucky assignment heuristic.

**The congestion signal, unified.** This is a piece added specifically so
the three architectures can be compared *fairly* on the "congestion
sensitivity" axis, not just the "which architecture" axis. Define one
occupancy fraction over *any* vertex window $S$ and exclusion set
$\mathrm{excl}$:
$$
\delta(S,t;\mathrm{excl}) = \frac{|\{a_j \in \mathcal{A}\setminus\mathrm{excl} : \ell_j(t)\in S\}|}{\max\{1, |S|-|\mathrm{excl}|\}}
$$
— "what fraction of this window is currently occupied by someone else."
Every architecture gets the *same* instrument, just evaluated on its own
natural window: centralised gets the whole graph ($S = V_{\mathrm{mov}}$),
section-based gets its own zone ($S = Y_q$, reusing the partition
`eq:partition`), decentralised gets its own local neighbourhood ($S =
V^{(r_{\mathrm{cng}})}_i(t)$, excluding itself since it's the one asking).
`../Images/congestion.png` draws exactly these three windows on the running
example: same graph, same three agents, three different-sized answers to
"who's nearby."
Without this, "congestion-sensitive routing" would only have been a
realisable concept for the decentralised arm — and then RQ2 and RQ3 couldn't
both be asked cleanly, because one factor would only exist at one level of
the other.

---

## 7. What a decentralised agent sees (`sec:pf:observations`)

**Plain picture.** A decentralised agent can't see the warehouse — it sees a
bounded bubble around itself, plus whatever nearby agents choose to tell it.
Everything in this subsection is characterising the *shape* of that bubble.

**The bubble itself.** $V_i^{(d)}(t)$ is every vertex within $d$ hops of the
agent (directed hops — see §2); $\mathcal{G}_i^{(d)}(t)$ is the subgraph on
those vertices. Fixed size regardless of $|V|$, which is *why* one trained
policy can run on a bigger warehouse than it was trained on — and the price
is that a conflict brewing $d{+}1$ hops away is invisible until it's closer.
See `../Images/observation.png`: agent $a_2$'s blue highlighted region is its
$\mathcal{G}_i^{(2)}(t)$; agents $a_1$ and $a_3$ sit outside both the
highlighted region *and* the dashed communication circle, so $a_2$ genuinely
cannot know they exist right now.

**Restoring direction: the potential.** Inside a bubble with no sense of
"which way is the goal," $\eta_i(v,t) = d_G(v, q_i(t))$ — distance from $v$
to the agent's *current target* — is annotated onto every visible vertex
(the blue numbers in the figure). The one piece of real mathematical care
here: $\eta_i(w,t) - \eta_i(v,t) \ge -c(v,w)$, with *equality* exactly when
$(v,w)$ starts a shortest path. A negative-but-not-equal difference still
means "closer," just not provably *optimally* closer — and that gap between
"closer" and "certified shortest" is precisely the room a congestion-aware
policy needs: it can deliberately take a merely-closer step instead of the
provably-shortest one, to avoid a jam.

**The congestion feature.** $\delta_i(t)$ is exactly the decentralised
instance of $\delta(S,t;\mathrm{excl})$ from §6 — nothing new here, just
plugged in with $S$ = the agent's own local window.

**The communication graph.** $G^{\mathcal{A}}_t = (\mathcal{A}, E^{\mathcal{A}}_t)$
is a *second*, unrelated graph — its nodes are agents, not warehouse
vertices, and an edge means "close enough to talk," not "drivable." Don't
let the shared-looking notation ($G$ vs. $G^{\mathcal{A}}_t$) suggest they're
the same kind of object; they aren't.

**Putting the bubble together.** $o_i(t) = (\mathcal{G}_i^{(d)}(t),\,
\eta_i(\cdot,t),\, \delta_i(t),\, \text{messages from neighbours in } G^{\mathcal{A}}_t)$
— four pieces, each defined above, packaged into what the decentralised
policy actually receives.

---

## 8. The learning problem (`sec:pf:game`)

**Plain picture.** Once you have "an agent acts from a partial view while
the world moves under everyone's joint action," you're describing a
standard object: a partially observable stochastic game (POSG),
$\mathcal{M} = (\mathcal{A}, \mathcal{S}, \{\mathcal{U}_i\}, P, \{\mathcal{O}_i\},
\{O_i\}, \{R_i\}, \gamma)$. Nothing here is bespoke to warehouses — it's the
standard multi-agent RL container, with the warehouse-specific objects from
§2–§7 slotted into its slots.

**One subtlety worth internalising: fixed action space, masked per state.**
$\mathcal{U}(v)$ from §2 depends on *which vertex* the agent is at — but a
POSG wants one fixed action space per agent. The fix:
$\mathcal{U}_i := \bigcup_v \mathcal{U}(v)$ (union over every vertex's
options), and at any actual state only the subset for the agent's *current*
vertex is enabled — the rest are masked to zero probability. This is how "the
legal moves depend on where you are" gets embedded into a formalism that
assumes a fixed action space.

**The objective.** $J(\theta) = \mathbb{E}\big[\sum_t \gamma^t \frac{1}{m}
\sum_i R_i(t)\big]$ — team-averaged, because agents are homogeneous,
cooperative, and share one parameter vector $\theta$. The reward $R_i$ itself
is deliberately left unspecified here — it's an *instrument* for getting a
good policy, not part of what "good" means; that's `eq:functional` in §10.

---

## 9. How the two layers close the loop (`sec:pf:coupling`)

**Plain picture.** Two clocks running at once. See `../Images/loop.png` —
that picture *is* this section.

- **Fast loop, every timestep:** tasks generated → controller assigns and
  routes → environment advances.
- **Slow loop, every $\Delta$ steps:** the traffic those fast steps produced
  becomes the causal estimates $\hat\mu_t, \hat w_t$ that feed the *next*
  storage update.

**Both directions matter, and only one of them is optional.** Forward
(storage → routing) always exists: it's the coupling condition from §5,
$x_{r_j}(k_j,s_j) > 0$ — change the storage layer and you mechanically
change which vertices become pickups. Backward (routing → storage) is the
part an experiment can switch off: $F_{\mathrm{fix}}$ simply ignores
$\hat\mu_t, \hat w_t$ — same diagram, feedback arrow deleted. That's the
entire experimental contrast of this thesis, stated as literally as
possible: one diagram, with and without one arrow.

**Why $\Delta$ is a real experimental variable and not a tuning nuisance.**
Too small, and $F$ reacts to noise the fast process hasn't had time to
average out — the task distribution becomes non-stationary from the
learner's point of view. Too large, and $\hat\mu_t, \hat w_t$ are stale by
the time $F$ uses them. There's no context-free "right" $\Delta$; it has to
be swept.

---

## 10. How a run is scored (`sec:pf:measures`)

**Plain picture.** Three questions about a completed run: how much work got
done, what did it cost to do it, and how was the traffic spread out while
doing it? Everything in this subsection answers one of those three.

**Work done.** $\Lambda_T = |\mathcal{C}_T|/T$ (throughput) and
$\bar\zeta_T$ (mean service time) — the latter is reported, the former is
deliberately *excluded* from the aggregate score below because, under a
fixed arrival rate, it's largely the same information as $\bar\zeta_T$ read
backwards.

**Cost.** $\bar c_T$ = total movement cost across all agents, divided by
tasks completed.

**Spread.** $\mu_T(e)$ counts traversals of edge $e$ over the whole run;
normalising gives $p_T(e)$, and its (normalised) entropy $H_T$ is 1 when
traffic is perfectly even and → 0 when it all funnels down one edge.
Concentration $C_T = 1 - H_T$ is the complement — see
`../Images/concentration.png` for the two extremes side by side, same
graph, same width scale. *Concentration is not congestion*: a concentrated
flow at low load causes zero delay, so both are reported, never conflated.

**Runtime.** $\kappa_T$ = mean wall-clock time per decision. This one is
reported *alongside* the others, never folded into the weighted sum below —
seconds and warehouse-distance don't share a unit system, and forcing them
into one weighted sum would silently invent an exchange rate between them.

**The one number everything else feeds.**
$$
\mathcal{J}(F,\pi) = q_{\mathrm{svc}}\mathbb{E}[\bar\zeta_T] + q_{\mathrm{mov}}\mathbb{E}[\bar c_T] + q_{\mathrm{wait}}\mathbb{E}[W_T] + q_{\mathrm{conc}}\mathbb{E}[C_T] + q_{\mathrm{back}}\mathbb{E}[B_T]
$$
Five terms, all "lower is better," all in compatible units (time, distance,
counts — never seconds-of-compute). $W_T$ (time lost to blocking *after*
assignment) is kept deliberately distinct from $B_T$'s queueing term (time
lost *before* assignment) so the two never double-count the same delay.

**The actual research question, formalised.** Does an adaptive $F$ beat
$F_{\mathrm{fix}}$ by more than seed noise —
$\mathcal{J}(F,\pi) < \mathcal{J}(F_{\mathrm{fix}},\pi)$ — and does the
margin depend on architecture (Table 1), on congestion sensitivity ($\beta$
for storage, a realisation of $\delta$ for routing), or on load ($m$,
$\lambda_{\mathrm{task}}$)? That's `eq:rqformal` — everything before it in
this document exists to make every symbol in that one sentence precise.

---

## 11. Scope and assumptions (`sec:pf:scope`)

What's deliberately *not* modelled, stated once so no Method subsection has
to apologise for it individually: no battery, no kinematics, no capacity
beyond one task at a time; execution is deterministic (accepted actions
always succeed, and the conflict-resolution tie-break is itself
deterministic, so the *only* randomness in the system is order arrivals);
physical relocation of stock is free unless $\chi > 0$ says otherwise; and —
the biggest deliberate narrowing relative to the Knippenberg source paper —
**tasks carry no deadline**. Lateness only ever shows up as a nudge to the
*average* $\bar\zeta_T$; no single task can be said to have failed. If a
later version of this thesis needs service-level guarantees, that's a
Problem-Formulation-level change (a deadline field on $\tau_j$, plus either a
hard feasibility cut or a soft penalty term), not a Method-level one — it
would redefine what a *valid* or *well-scored* solution even is.

---

## 12. Cheat sheet

| Symbol | One line |
|---|---|
| $G=(V,E)$ | The directed warehouse graph. |
| $V_{\mathrm{mov}}, V_{\mathrm{str}}, V_{\mathrm{del}}, V_{\mathrm{ep}}$ | Occupiable / storage / delivery / endpoint vertices. |
| $c(e){=}c(v,w)$, $\hat c(v,w)$ | Edge cost; realised one-step cost (handles waiting too). |
| $d_G(v,w)$ | Cheapest directed path cost — **not** symmetric in general. |
| $\mathcal{A}, \ell_i(t), u_i(t)$ | Fleet; agent $i$'s position; agent $i$'s chosen action. |
| `eq:vertexconflict`, `eq:swapconflict` | The two ways two agents can collide. |
| $x_t$, $\mathcal{X}$ | Storage state (units per SKU per vertex); the feasible set. |
| $F$, $F_{\mathrm{fix}}$ | The storage update rule; the do-nothing baseline. |
| $\hat\rho_t,\hat\mu_t,\hat w_t$ | Storage's causal estimates: demand, traffic, waiting. |
| $\tau_j=(r_j,s_j,g_j,k_j)$ | A task: release, pickup, delivery, requested SKU. |
| $x_{r_j}(k_j,s_j)>0$ | **The coupling condition** — storage $\to$ routing link. |
| $\mathcal{Q}_t,\mathcal{B}_t,\mathcal{C}_t$ | Waiting / active / completed task sets. |
| $\pi=(\pi^{\mathrm{assign}},\pi^{\mathrm{route}})$ | A controller: who-does-what, then how-they-move. |
| $\delta(S,t;\mathrm{excl})$ | Shared occupancy/congestion signal, any window $S$. |
| $\eta_i(v,t)$ | Distance from $v$ to agent $i$'s current target. |
| $\delta_i(t)$ | Decentralised instance of $\delta$: local crowding. |
| $G^{\mathcal{A}}_t$ | Who-can-talk-to-whom graph — **not** the warehouse graph. |
| $o_i(t)$ | Everything a decentralised agent actually gets to see. |
| $\mathcal{M}$ (POSG) | The formal multi-agent learning problem. |
| $\Delta$ | Storage epoch length — the slow clock's period. |
| $\bar\zeta_T,\bar c_T,W_T,C_T,B_T,\kappa_T$ | Service time, movement cost, blocked-time, concentration, backlog, runtime. |
| $\mathcal{J}(F,\pi)$ | The one number a run is ultimately judged by. |

---

## 13. How it all fits together

1. §2 gives you a graph. §3 lets more than one robot stand on it safely.
2. §4 says what's on the shelves; §5's coupling condition is the only place
   that fact touches routing at all.
3. §6 says who's allowed to know what, and gives every architecture the same
   congestion instrument so the comparison across architectures is fair.
4. §7 packages "what one decentralised agent knows" into one object; §8 puts
   that object into the standard multi-agent-RL container.
5. §9 is the actual mechanism: fast loop every step, slow loop every
   $\Delta$ steps, and the entire experimental question is what happens when
   you delete one arrow in that diagram.
6. §10 is how you'd know, at the end, whether deleting that arrow was a good
   idea.

If you can redraw `../Images/loop.png` from memory and say, for each arrow,
which equation it *is*, you understand the formulation.
