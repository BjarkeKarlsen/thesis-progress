# Draft `[A47]`. Robots carry the put-away

**Status 2026-10-19. Draft for the author, nothing applied.** Each block names its place in
`thesis/Chapters/`, the text now, and the proposed text. On approval each changed line gets
`% [A47]` and `thesis-progress/decisions/GAPS.md` gets the entry at the end.

Decisions this draft follows (agreed 2026-10-19).
- A put-away is a task, from a receiving vertex to a shelf, served like a pick.
- Receiving vertices are a role of their own, on one side of the warehouse. Storage, delivery
  and parking vertices stay random.
- Shelf space is taken when the put-away is created. A unit is on the shelf, and can be
  picked, only once its put-away is delivered.
- Stock arrives every Δ = 100 steps, in bursts. One queue for both kinds, oldest first.
- The result is total service time over all tasks. Put-aways count in the keep-up check, and
  nothing at the horizon is excluded.
- The storage rules count the whole trip of a unit, receiving to shelf to delivery, with no
  new weight.

Two choices this draft makes that were not discussed. Check them.
1. **Stock counts on the shelf only once it is delivered** (author, 2026-10-19). $x_t(k,v)$
   keeps its meaning, the units on shelf $v$. A new $x^{\mathrm{in}}_t(k,v)$ counts the units on
   their way to $v$. The capacity constraint counts both, so the room is reserved, and the
   storage rule places into $x^{\mathrm{in}}_t$. The stock condition and the pickup rule do not
   change.
2. **Total service time counts unfinished work up to the horizon.** A task still open at $T$,
   and an order line still waiting for stock at $T$, add the time spent so far. When no line
   waits for stock this is the area under the backlog, $\sum_t B_t$. Counting only finished
   tasks would reward a rule that leaves more work unfinished.

---

## 1. Introduction (`sec:introduction`)

### 1a. The coupling paragraph, line 13, first sentence

Now:
> The storage and transport layers are coupled because storage assignments determine the
> spatial distribution of pickup tasks, while routing performance influences the effective
> cost of accessing each storage location.

Proposed:
> The storage and transport layers are coupled because storage assignments determine where
> the agents pick stock up and where they carry arriving stock to, while routing performance
> influences the effective cost of accessing each storage location.

### 1b. The study paragraph, line 16, last sentence

Now:
> The comparison focuses on task service time, on whether the fleet keeps up with the arriving
> tasks, on congestion, and on computational cost.

Proposed:
> The comparison focuses on the total service time of every task the fleet serves, picks and
> put-aways alike, on whether the fleet keeps up with the arriving tasks, on congestion, and on
> computational cost.

---

## 2. Project description (`sec:pd-aim-and-scope`, `sec:pd-rq`)

### 2a. Aim and scope, line 27, third sentence

Now:
> Orders generate pickup-delivery tasks whose pickup locations depend on the current storage
> configuration.

Proposed:
> Orders generate pick tasks whose pickup locations depend on the current storage
> configuration. Arriving stock generates put-away tasks whose shelves the storage rule
> chooses.

### 2b. Dependent variables, line 42

Now:
> The dependent variables are whether the fleet keeps up (tasks finished against tasks
> released, and whether the backlog keeps growing), throughput, mean service time and its
> three parts (waiting for an agent, travel, and blocked time), order completion time,
> crowding, the put-away distance per storage update, and controller runtime.

Proposed:
> The dependent variables are whether the fleet keeps up (tasks finished against tasks
> released, and whether the backlog keeps growing), throughput, total service time and its
> three parts (waiting for an agent, travel, and blocked time), the mean service time of
> picks, order completion time, crowding, the put-away distance per storage update, and
> controller runtime.

### 2c. The main question, line 47

Now:
> How much does adaptive storage shorten service time in a graph-based warehouse, ...

Proposed:
> How much does adaptive storage shorten the total service time of the fleet's tasks in a
> graph-based warehouse, ...

(The rest of the sentence stays.)

### 2d. RQ1, line 55

Now:
> Does adaptive storage that follows demand shorten service time relative to fixed storage
> under otherwise matched conditions, at a load where the fleet keeps up, and which part of
> service time changes?

Proposed:
> Does adaptive storage that follows demand shorten total service time relative to fixed
> storage under otherwise matched conditions, at a load where the fleet keeps up, and which
> part of service time changes?

### 2e. The main-result paragraph, line 79

Now:
> The main result answers RQ1 and RQ2 together. It is the gain in mean service time that
> demand-only storage gives over fixed storage under each controller, ...

Proposed:
> The main result answers RQ1 and RQ2 together. It is the gain in total service time that
> demand-only storage gives over fixed storage under each controller, ...

(The rest of the paragraph stays. "a share of route time" now means total route time.)

---

## 3. Storage (`sec:pf:storage`)

### 3a. Receiving vertices, lines 466 to 468

Now:
> In this thesis the receiving vertices are the delivery vertices, one side of the warehouse
> where goods come in and go out.

Proposed:
> In this thesis the receiving vertices lie on one side of the warehouse, where goods come in.
> Orders leave at the delivery vertices, which are spread through the warehouse.

### 3b. The storage update, `eq:storageupdate`, and a new paragraph after the tea example

The rule now places the arriving units on their way, not on the shelf. Replace the sentence
before the equation and the equation.

Now:
> The rule adds the arriving units to the shelves that have room and touches nothing else.
> Formally, the \emph{storage update} is
> \[ x_t = F(x_t^{-}, y_t, \hat\rho_t, \hat\mu_t, \hat w_t) \in \mathcal{X}, \quad
>     x_t \ge x_t^{-}, \quad \sum_v (x_t(k,v) - x_t^{-}(k,v)) \le y_t(k) \]

Proposed:
> The rule chooses a shelf with room for each arriving unit and touches nothing else. The unit
> is then on its way to that shelf. Formally, with $x^{\mathrm{in}}_t(k,v)$ the units of $k$ on
> their way to $v$, the \emph{storage update} is
> \begin{equation}
>   \begin{gathered}
>   x^{\mathrm{in}}_t = F\bigl(x_t^{-},\, x^{\mathrm{in},-}_t,\, y_t,\, \hat{\rho}_t,\, \hat{\mu}_t,\, \hat{w}_t\bigr), \qquad
>   x_t^{-} + x^{\mathrm{in}}_t \in \mathcal{X}, \\
>   x^{\mathrm{in}}_t \ge x^{\mathrm{in},-}_t,
>   \qquad \sum_{v \in V_{\mathrm{str}}} \bigl(x^{\mathrm{in}}_t(k,v) - x^{\mathrm{in},-}_t(k,v)\bigr) \le y_t(k)
>   \quad \forall k \in \mathcal{K},
>   \end{gathered}
>   \label{eq:storageupdate}
> \end{equation}

The sentence after it, "The first condition says that nothing on a shelf moves, and the second
that only arriving units are added", becomes:
> The first condition keeps the shelves within capacity, counting the units on their way. The
> second says that nothing already placed moves, and the third that only arriving units are
> added.

New paragraph after "...so `eq:storageupdate` is causal.":
> The robots carry the arriving stock to its shelves. Every shelf a SKU's units are put on
> gives one put-away task. It is released at the epoch, picks the units up at the receiving
> vertex nearest the shelf, and delivers them there. A unit is on the shelf only once it is
> delivered. Until then it takes up room on the shelf, so a second put-away cannot overfill it,
> but no order can take it. When the put-away of $q_j$ units of $k_j$ to $v$ is delivered,
> $x_t(k_j,v)$ rises by $q_j$ and $x^{\mathrm{in}}_t(k_j,v)$ falls by $q_j$. If 20 units of tea
> go to shelf $B$ at $t = 100$ and the put-away is delivered at $t = 112$, then from $t = 100$
> the 20 units take up room at $B$, and from $t = 112$ an order can take them.

`eq:feasiblestorage` itself does not change. The capacity check moves into
`eq:storageupdate`, applied to $x_t^{-} + x^{\mathrm{in}}_t$.

### 3c. Fixed storage, line 548

Now:
> Only units that do not fit at home go on, to the shelf nearest a delivery vertex that has
> room.

Proposed:
> Only units that do not fit at home go on, to the shelf with room on the shortest trip from
> the receiving side to the delivery vertices.

### 3d. Access cost in the description list, after `eq:storageobjective`, line 578

Now:
> \item[Access cost] $D(x;\hat\rho_t)$: how far popular SKUs sit from where they are needed. A
> configuration that places a high-demand SKU far from every delivery point scores badly here,
> however feasible it is otherwise.

Proposed:
> \item[Access cost] $D(x;\hat\rho_t)$: how far popular SKUs travel, from the receiving side to
> their shelf and from the shelf to where they are needed. A configuration that places a
> high-demand SKU far from every delivery point, or far from the receiving side, scores badly
> here, however feasible it is otherwise.

### 3e. Line 595, the `fig:dkr` sentence

Now:
> Putting the arriving tea near the delivery vertex lowers $D$, and also lowers $K$ when that
> shelf sits on the quieter aisle.

Proposed:
> Putting the arriving tea near the delivery vertex lowers $D$ unless the shelf is far from
> the receiving side, and also lowers $K$ when that shelf sits on the quieter aisle.

(`fig:storageexample` and `fig:dkr` need the receiving side drawn in. Listed under figures at
the end.)

### 3f. Line 609, last sentence of the section

Now:
> The robots do not carry arriving stock to its shelves, which Section~\ref{sec:pf:scope}
> records as a limitation.

Proposed: delete. The new paragraph 3b says the robots carry it.

---

## 4. Tasks (`sec:pf:tasks`)

### 4a. Task definition, `eq:task` and the sentence before it, lines 627 to 640

Now:
> Each trip is a transport task, and the \emph{task definition} makes it a tuple
> \[ \tau_j = (t_j^{\mathrm{released}}, s_j, g_j, k_j, q_j), \quad ... s_j \in V_{\mathrm{str}},
> \; g_j \in V_{\mathrm{del}}, ... \]

Proposed text before the equation:
> Each trip is a transport task. A \emph{pick} takes units from a shelf to the order's delivery
> vertex. A \emph{put-away} takes arriving units from a receiving vertex to the shelf the
> storage rule chose (Section~\ref{sec:pf:storage}). Both are served the same way, by one agent
> that goes to the pickup vertex and then to the delivery vertex, and nothing happens at either
> end. The \emph{task definition} makes a task a tuple

Proposed equation, the domains only:
> \[ s_j \in V_{\mathrm{str}} \cup V_{\mathrm{rcv}}, \quad g_j \in V_{\mathrm{del}} \cup V_{\mathrm{str}}, \]
> with $(s_j, g_j) \in V_{\mathrm{str}} \times V_{\mathrm{del}}$ for a pick and
> $(s_j, g_j) \in V_{\mathrm{rcv}} \times V_{\mathrm{str}}$ for a put-away.

### 4b. The stock condition and the pickup rule

`eq:coupling` and `eq:pickuprule` do not change, because $x_t$ still counts only the units on
the shelf. Two sentences are added.

After `eq:coupling`:
> A put-away has no stock condition, because its units are the ones that arrived. Units on
> their way to a shelf are not on it, so no pick can take them.

After "Each $x_t(k, v_i)$ falls by $q^{(i)}$.":
> A line whose units are on their way waits for the put-away to be delivered.

## 5. Measures (`sec:pf:measures`)

### 5a. Opening, lines 1444 to 1450

Now:
> One check comes first, whether the fleet keeps up with the arriving tasks. Mean service time
> is then the result. ... Two costs are reported next to it, how far arriving stock travels to
> its shelves and the time the controller needs to decide.

Proposed:
> One check comes first, whether the fleet keeps up with the arriving tasks. Total service
> time is then the result, the service time of \citet{ma2017lifelong_mapf} summed over every
> task. ... Two measures are reported next to it, how far arriving stock travels to its shelves
> and the time the controller needs to decide.

### 5b. Keeping up, new last paragraph before "Throughput is ..."

> The check counts put-aways as tasks, because they are work the fleet must keep up with. Stock
> arrives every $\Delta$ timesteps, so the backlog jumps at every epoch and falls between them.
> The put-aways of an arrival close to the horizon cannot all be delivered by $T$, so they lower
> the share finished. They are kept in the check, and the share they cost is reported.

### 5c. Service time, replace the paragraph and `eq:meanservice` (lines 1502 to 1514)

> \paragraph{Service time.} The result is the \emph{total service time}, the time every task
> spends from its release to its delivery, added up over the run. A sum is used instead of a
> mean because the two storage rules do not make the same tasks. The orders are the same on a
> seed, but how many put-aways an arrival needs depends on how many shelves the rule spreads it
> over. A mean over different tasks could fall because a rule makes more short trips, while the
> orders wait longer. A task still open at the horizon counts with the time it has spent so far,
> and so does an order line still waiting for stock, so a rule cannot gain by leaving work
> unfinished. Formally, with $\zeta_j$ from \nref{eq:servicetime} and
> $\mathcal{Z}^{\mathrm{wait}}_T$ the order lines still waiting for stock at $T$,
> \begin{equation}
>   \zeta^{\mathrm{tot}}_T = \sum_{\tau_j \text{ released by } T}
>     \bigl(\min(t_j^{\mathrm{finish}}, T) - t_j^{\mathrm{released}}\bigr)
>     \;+ \sum_{\text{lines in } \mathcal{Z}^{\mathrm{wait}}_T} \bigl(T - t^{\mathrm{released}}\bigr) .
>   \label{eq:totalservice}
> \end{equation}
> When no line waits for stock, this is the area under the backlog, $\sum_{t<T} B_t$.
> In Figure~\ref{fig:timeline}, $\tau_1$, $\tau_2$ and $\tau_3$ take $9$, $8$ and $8$
> timesteps and the stuck $\tau_4$, released at $t = 11$, has spent $9$ by $T = 20$, so
> $\zeta^{\mathrm{tot}}_T = 34$.
> The mean service time of picks, $\bar\zeta_T$, the measure of
> \citet{ma2017lifelong_mapf} used unchanged, is reported next to it, because it is what an
> order line waits.
> \begin{equation}
>   \bar{\zeta}_T = \frac{1}{|\mathcal{C}^{\mathrm{pick}}_T|} \sum_{\tau_j \in \mathcal{C}^{\mathrm{pick}}_T} \zeta_j .
>   \label{eq:meanservice}
> \end{equation}

(Checked against `thesis-progress/scripts/images/timeline.py`. $\tau_4$ is released at 11,
so the backlog over $t = 0$ to $19$ also sums to 34.)

### 5d. Where the time goes, line 1533

Now:
> and averaging each part over $\mathcal{C}_T$, as in \nref{eq:meanservice}, gives three means
> that add up to $\bar\zeta_T$.

Proposed:
> and adding each part up over the tasks of \nref{eq:totalservice} gives three totals that add
> up to $\zeta^{\mathrm{tot}}_T$.

And in the "Each part points to one cause" paragraph, after "Travel shrinks when the storage
rule puts popular items close to where they are needed":
> and grows when it puts them far from the receiving side

### 5e. Reported costs, the put-away paragraph, lines 1605 to 1629

Now:
> \paragraph{Reported costs.} Two costs are reported next to the result and never combined
> with it, because neither is a time a task spends in the system.
>
> The first is how far arriving stock travels to its shelves. Service time shows what adaptive
> storage gains, but not what the gain costs, since the robots do not carry stock to the shelves
> (Section~\ref{sec:pf:scope}). Fixed storage pays this cost too, ...

Proposed:
> \paragraph{Reported measures.} Two measures are reported next to the result.
>
> The first is how far arriving stock travels to its shelves. Its time is already in the
> result, because the put-aways are tasks. The distance shows how much of a change in travel
> comes from the put-aways, since a rule that puts stock near the delivery vertices can lengthen
> them. Fixed storage pays it too, ...

(`eq:putaway` itself stays.)

### 5f. `tab:measures`

- $\bar\zeta_T$ row: role "reported, picks only".
- New row: $\zeta^{\mathrm{tot}}_T$ \eqref{eq:totalservice} & result & after
  \citet{ma2017lifelong_mapf}.
- $\bar\nu_T$ row: role "explains the result".
- Caption unchanged.

### 5g. The decision problem, `eq:decisionproblem`, line 1671

"the shortest expected service time" becomes "the shortest expected total service time", and
$\mathbb{E}[\bar\zeta_T(F,\pi)]$ becomes $\mathbb{E}[\zeta^{\mathrm{tot}}_T(F,\pi)]$.

### 5h. The gain, line 1702

Now:
> \mathrm{gain}_n = \bar\zeta_T^{(n)}(F_{\mathrm{fix}}, \pi) - \bar\zeta_T^{(n)}(F, \pi) .

Proposed:
> \mathrm{gain}_n = \zeta^{\mathrm{tot},(n)}_T(F_{\mathrm{fix}}, \pi) - \zeta^{\mathrm{tot},(n)}_T(F, \pi) .

And "the difference in their service times comes from the storage rule alone" becomes "the
difference in their total service times comes from the storage rule alone, the put-aways it
makes included".

### 5i. The relative gain, `eq:relgain`

The denominator becomes the total travel and total blocked time of the fixed-storage run,
$\zeta^{\mathrm{travel,tot},(n)}_T(F_{\mathrm{fix}},\pi) + W^{\mathrm{tot},(n)}_T(F_{\mathrm{fix}},\pi)$,
and "with $\bar\zeta^{\mathrm{travel}}_T$ the mean of ..." becomes "with the totals of
\nref{eq:split}".

---

## 6. Scope (`sec:pf:scope`)

### 6a. Replace the "Abstract put-away" item

Now:
> \item[Abstract put-away] Stock arrives in batches every $\Delta$ timesteps and is on its shelf
> at once. The robots do not carry it, so put-away takes no fleet time and adds no traffic. Its
> distance is reported as a cost, \nref{eq:putaway}.

Proposed:
> \item[No handling time] A task ends when its units reach the vertex. Unloading at a shelf or
> at a delivery vertex takes no time, and nothing is packed or built there.

### 6b. The closing paragraph

Now:
> In particular, results about the value of congestion feedback are conditional on put-away
> being free, results about decentralised control ...

Proposed:
> In particular, results about decentralised control ...

---

## 7. Method (`4.Implementation.tex`)

### 7a. `sec:method:storage`, the three rules (lines 70 to 95)

A new distance, the trip of a unit through shelf $v$, is introduced once before the rules:
> Every rule judges a shelf by the trip a unit makes through it, from the nearest receiving
> vertex to the shelf and on to the nearest delivery vertex. Formally,
> \begin{equation}
>   d^{\mathrm{trip}}(v) = \min_{g \in V_{\mathrm{rcv}}} d_G(g, v) + \min_{g \in V_{\mathrm{del}}} d_G(v, g) .
>   \label{eq:tripdistance}
> \end{equation}
> Both legs are counted in timesteps, so they add without a weight.

- $F_{\mathrm{fix}}$: "to the other shelves in order of $\min_{g\in V_{\mathrm{del}}} d_G(v,g)$"
  becomes "in order of $d^{\mathrm{trip}}(v)$".
- $F_{\mathrm{dem}}$: the same change.
- `eq:storagegreedy`:
  > \mathrm{score}(k,v) = \hat\rho_t(k)\cdot d^{\mathrm{trip}}(v)
  > \;+\; \beta \sum_{e \in \mathrm{path}(v)} \hat\mu_t(e)\,\hat w_t(e) ,

  and "where $\mathrm{path}(v)$ is the shortest path used to reach $v$ from the nearest
  delivery point" becomes "where $\mathrm{path}(v)$ is the trip of
  \nref{eq:tripdistance}, the shortest path from the nearest receiving vertex to $v$ and on to
  the nearest delivery vertex".
- One sentence after `eq:storagegreedy`:
  > Both legs are weighted by the same $\hat\rho_t(k)$, because arrivals refill what was
  > ordered, so a SKU is put away about as often as it is picked.

### 7b. `sec:impl:instances`, after "...which the split into training and evaluation seeds
relies on."

> The receiving vertices are drawn at random from one end row of the warehouse, the inbound
> side. The storage, delivery and parking vertices are drawn at random from the rest, as the
> pickup and delivery locations of \citet{ma2017lifelong_mapf} are, so the delivery vertices
> are spread through the warehouse. The mean trip distance $d^{\mathrm{trip}}(v)$ of the
> storage vertices is reported for every warehouse size, because that spread is what adaptive
> storage can gain from.

### 7c. `sec:impl:logging`

One sentence where the per-task record is described:
> Each task also records whether it is a pick or a put-away, so the mean service time of picks
> and the split by kind can be read off.

---

## 8. Notation (`2.Notation.tex`)

| symbol | change |
|---|---|
| $V_{\mathrm{rcv}}$ | meaning becomes "Where arriving stock enters, one side of the warehouse" |
| $s_j$ | domain $V_{\mathrm{str}} \cup V_{\mathrm{rcv}}$, "pickup vertex of a pick or a put-away" |
| $g_j$ | domain $V_{\mathrm{del}} \cup V_{\mathrm{str}}$, "delivery vertex of a pick or a put-away" |
| $x^{\mathrm{in}}_t(k,v)$, $x^{\mathrm{in},-}_t$ | new, `eq:storageupdate`, "units of $k$ on their way to shelf $v$, and just before the epoch" |
| $\zeta^{\mathrm{tot}}_T$ | new, `eq:totalservice`, "total service time, the result" |
| $\bar\zeta_T$ | meaning becomes "mean service time of picks, reported" |
| $\mathcal{C}^{\mathrm{pick}}_T$ | new, "picks completed by $T$" |
| $d^{\mathrm{trip}}(v)$ | new, `eq:tripdistance`, "trip of a unit through shelf $v$" |

`thesis/styles/eqnames.tex` gains names for `eq:totalservice` ("the total service time") and `eq:tripdistance` ("the trip distance").

---

## 9. Figures that change (not drafted)

- `fig:storageexample` and `fig:dkr`. Add the receiving side and the put-away leg.
- `fig:taskroute` (`instance.png`). Add receiving vertices to the drawing.
- `fig:timeline`. Unchanged. It already shows $\tau_4$'s release.
- `fig:lifecycle`. Unchanged.

---

## 10. `GAPS.md` entry

> **[A47] Robots carry the put-away.** Arriving stock was placed on its shelf at once and free,
> so the storage rule never caused traffic and its cost was only reported. Now every placement
> is a put-away task, from a receiving vertex on one side of the warehouse to the shelf, served
> like a pick. Space is reserved when the put-away is created, and the units count as on the
> shelf only once it is delivered. The storage rules judge a shelf by the whole trip of a unit, receiving to
> shelf to delivery, in timesteps, so no new weight is needed. The result becomes total service
> time over all tasks, including the time of tasks still open at the horizon, because the two
> rules make different put-aways and a mean over different tasks is not a paired comparison.
> Mean pick service time is reported next to it. Why. It answers the open question of
> `thoughts.md` on what the storage cost is (robot time, in the same unit as the result), and
> it gives RQ3 a mechanism, since storage now creates traffic directly. Revises `[A40]` (the put-away
> distance is no longer the cost) and `[A44]` (the result measure). Removes the "Abstract
> put-away" limitation. Cost. About four code PRs before the Token Passing load sweep, and a
> retrain, which the long run needs anyway.
