# Step 12, thesis drafts (D21 to D27)

Drafted 2026-10-27 for the author to approve. Nothing here is in `thesis/` yet. Each block names where it
goes and what it replaces. The chapters still say delivery vertex and receiving vertex, so the drafts do
too. The rename to workstation and dock is step 03 (`[A63]`), not written yet. Tags `[A63]` to `[A67]` are
reserved by steps 03 to 06, so step 12 uses `[A68]` to `[A73]`. Values the sweep will set are marked TBD.

## Two choices first

Both agreed by the author, 2026-10-27. The blocks are then approved one at a time.

**1. The result measure (D21).** Today the result is the mean service time of picks, `eq:meanservice`, and
order completion is only reported (`app:measures`: "Service time stays the result, because it is defined
per task and compares with Ma"). D21 says the order is done when it leaves at the dock and that crowding at
the docks counts in the main result. Picks never reach a dock, so the result has to become the order
service time. The drafts below do that: $\bar\zeta_T$ keeps its symbol and its place in the gain test
`eq:rqformal`, and is redefined as the mean order service time. The per-task $\zeta_j$ stays, for the split
of `eq:split` and the reproduction of Ma et al. Rejected: keep picks as the result, which leaves the docks
out of it.

**2. Fixed storage's home shelves (D22).** `sec:impl:instances` says today "A random start would make
fixed storage a weak baseline, since $F_{\mathrm{fix}}$ always sends stock back to where it started." That
is still true in the code, where a SKU's home is the shelf it starts on. With the random start of D22, fixed
storage becomes random dedicated storage, and the gain of demand storage would be measured against a weak
baseline. Proposed: the home shelves of $F_{\mathrm{fix}}$ are chosen once from the popularity at $t = 0$,
the most popular SKUs on the shelves nearest the delivery vertices (today's `demand_blocks` placement), and
are no longer the shelves of $x_0$. The start stays random for every rule. Needs a small code change
(`_home_shelves` from the class-based placement instead of the initial counts). The drafts assume this.

## [A68] D21, shipping

**`sec:pf:tasks`, replaces "Each pair is an order line ... and nothing happens at either end."
(`2.Introduction.tex` 461 to 470).**

> Each pair is an \emph{order line}. A line is served by trips, each fetching some of its units of the SKU
> from one shelf and bringing them to the order's delivery vertex, the goods-to-person setting of
> \citet{krnjaic2022warehouse_marl}. All lines of an order share its release time and its delivery vertex.
> The delivery vertex holds the units until the last line is there. Then one robot carries the whole order
> to a receiving vertex, where it leaves the warehouse. The receiving vertices are the docks, where stock
> comes in and finished orders go out. An order is complete when it leaves.
>
> Each trip is a transport task, and there are three kinds. A \emph{pick} takes units from a shelf to the
> order's delivery vertex. A \emph{put-away} takes arriving units from a receiving vertex to the shelf the
> storage rule chose (Section~\ref{sec:pf:storage}). A \emph{shipment} takes a finished order from its
> delivery vertex to a receiving vertex, and it is released at the timestep the order's last pick is
> delivered. All three are served the same way, by one agent that goes to the pickup vertex and then to the
> delivery vertex, and nothing happens at either end.

**After `eq:task`, replaces "For a pick, $s_j$ is a shelf and $g_j$ a delivery vertex. For a put-away,
$s_j$ is a receiving vertex and $g_j$ a shelf." (480 to 481).**

> For a pick, $s_j$ is a shelf and $g_j$ a delivery vertex. For a put-away, $s_j$ is a receiving vertex and
> $g_j$ a shelf. For a shipment, $s_j$ is a delivery vertex and $g_j$ a receiving vertex, and $q_j$ counts
> every unit of the order. A shipment carries several SKUs, so its $k_j$ plays no part.

**Replaces "A put-away has no stock condition, because its units are the ones that arrived." (514).**

> A put-away has no stock condition, because its units are the ones that arrived, and neither has a
> shipment, because its units are already at the delivery vertex.

**Which dock.** One sentence after the shipment is introduced, and the same reason in `sec:pf:storage`
where put-aways start.

> The receiving vertex of a shipment, and of every put-away, is drawn at random. Which dock a truck uses
> does not depend on where the stock goes, and a fixed choice would send all the traffic to the dock
> nearest the shelves.

**`sec:pf:env`, roles paragraph, replaces "Orders leave at the delivery vertices $V_{\mathrm{del}}$, and
new stock comes in at the receiving vertices $V_{\mathrm{rcv}}$." (140 to 141).**

> The lines of an order are gathered at the delivery vertices $V_{\mathrm{del}}$. New stock comes in and
> finished orders leave at the receiving vertices $V_{\mathrm{rcv}}$.

**Scope list, replaces the item "Nothing after the delivery vertex" (1359 to 1363), D13 replaced.**

> \item[No packing] An order is ready to ship the moment its last line reaches the delivery vertex.
> Packing is done by people and is not modelled, and a delivery vertex has room for every order gathered
> there.

**`sec:pf:measures`, paragraph "Service time", replaces 1171 to 1182.**

> \paragraph{Service time.} The result is the mean \emph{order service time}, how long an order takes from
> its release until it leaves at a dock. It includes every wait the order meets, for stock, for an agent,
> for its last line and for its shipment, because the customer waits through all of them. The order is
> used rather than a single task because the order is what the customer waits for, and because the
> shipment ends at the docks, so crowding there counts in the result. The service time of one task,
> \nref{eq:servicetime}, is the measure of \citet{ma2017lifelong_mapf}. It still explains the result, and it
> is the measure their results are reproduced on (Appendix~\ref{app:repro:ma}).
>
> Formally, an order $z$ is released at $t_z^{\mathrm{released}}$, the release time all its lines share,
> and leaves when its shipment is delivered, at $t_z^{\mathrm{finish}}$. Its service time is
> \begin{equation}
>   \zeta^{\mathrm{ord}}_z = t_z^{\mathrm{finish}} - t_z^{\mathrm{released}} ,
>   \label{eq:ordercompletion}
> \end{equation}
> and with $\mathcal{Z}^{\mathrm{done}}_T$ the orders that left by $T$, the result is
> \begin{equation}
>   \bar{\zeta}_T = \frac{1}{|\mathcal{Z}^{\mathrm{done}}_T|} \sum_{z \in \mathcal{Z}^{\mathrm{done}}_T} \zeta^{\mathrm{ord}}_z .
>   \label{eq:meanservice}
> \end{equation}

**Follows from it.**

- `sec:pf:measures` 1202 to 1203, "averaging each part over the picks ... gives three means that add up to
  $\bar\zeta_T$": the three parts now add up to the mean service time of picks, which explains the pick
  part of the result. One sentence changes.
- `tab:measures` (1262 to 1280): $\bar\zeta_T$ stays "result", with source "after
  \citet{krnjaic2022warehouse_marl}". The row for $\bar\zeta^{\mathrm{ord}}_T$ goes. A row for the mean
  service time of picks, "explains the result", source Ma et al.
- `app:measures` (`C.ModelDetails.tex` 330 to 343): the "Order completion" paragraph goes, since its
  equation moved to the chapter.
- Keep-up check `eq:throughput`: shipments count with the picks, as outbound work. One clause:
  "Shipments count with the picks, since both serve orders."
- Notation (`A.Notation.tex`): $V_{\mathrm{del}}$ "where an order's lines are gathered",
  $V_{\mathrm{rcv}}$ "where stock enters and orders leave", $\bar\zeta_T$ "mean order service time over the
  orders that left, the result of a run", $\zeta^{\mathrm{ord}}_z$ "time from an order's release until it
  leaves at a dock", new $t_z^{\mathrm{released}}, t_z^{\mathrm{finish}}$ and $\mathcal{Z}^{\mathrm{done}}_T$.
  Check the letters against the table before writing.
- Code: the summary of `evaluate_run` leads with the gain in pick service time. It must lead with the
  order service time.

GAPS entry: the order is what the customer waits for, and the trip out loads the docks that inbound stock
also uses, so leaving it out (D13) hid crowding the storage rule causes. Rejected: keep picks as the result,
which leaves the docks out of it.

## [A69] D22, one start for every rule, a warm-up for evaluation

**`sec:impl:instances`, replaces "Every storage rule starts from the same stock $x_0$ ... in
Appendix~\ref{app:storage:stock}." (`4.Implementation.tex` 714 to 720).**

> Every storage rule starts from the same stock $x_0$, with each SKU alone on a shelf drawn at random for
> the seed. Each SKU starts with one refill plus the safety stock of its service level
> (Appendix~\ref{app:storage:stock}). There are twice as many shelves as SKUs, so half start empty and
> every rule has room for its first refills. A random start gives no rule a head start. A start that
> follows demand would hand every rule the same good layout, and early in a run it would decide most of
> where the stock is, whatever the rule does.
>
> The home shelves of $F_{\mathrm{fix}}$ are not the shelves of $x_0$. They are chosen once from the
> popularity at $t = 0$, with the most popular SKUs on the shelves nearest the delivery vertices, the
> class-based placement of dedicated storage. Homes that follow the random start would make fixed storage
> a weak baseline.
>
> Training and evaluation start the same way, so the router learns on the kind of warehouse it is judged
> on. An evaluation run then has a warm-up of TBD steps before anything is measured, so the stock the
> storage rule placed has replaced the random start (Appendix~\ref{app:horizon}).

**`sec:pf:storage`, the home shelf sentence (`2.Introduction.tex` 386 to 389), replaces "Every SKU has a
home shelf, the vertex that holds it in $x_0$,".**

> Every SKU has a home shelf, chosen once at the start with the most popular SKUs nearest the delivery
> vertices,

**Appendix H, `app:horizon:setting`, replaces "A run starts with no tasks and with the starting stock, so
its first steps are not typical." (`H.Horizon.tex` 34 to 35).**

> A run starts with no tasks and with every SKU on a shelf drawn at random, so its first steps are not
> typical. The warm-up lasts until the refills the storage rule placed have replaced that start.

GAPS entry: the old start put the popular SKUs nearest the delivery vertices for every rule, so the start
decided most of where stock was, and the rules made few decisions of their own. Replaces D19's start fill.
The fixed baseline keeps class-based homes, so it stays the strong baseline the main result needs.

## [A70] D24, where the delivery and receiving vertices go

**`sec:impl:instances`, replaces the U-flow paragraph "Stock enters and leaves at the same end of the
building ... At 8 agents it runs from 6 to 37 steps." (665 to 674).**

> The delivery vertices take rack faces drawn at random for each seed, anywhere in the rack area. Fixed
> delivery vertices would make the traffic of every run meet at the same vertices, so a result could hold
> for that one layout only. The receiving vertices are spread evenly along the left wall, from the front to
> the back. Stock comes in there and finished orders leave there, so a robot's work runs from the left
> wall to a shelf, on to a delivery vertex and back to the left wall. Docks along the whole wall let this
> traffic enter the rack area at every row, through the middle as well as at the front. The best shelves
> are then those near a delivery vertex and near the left wall, and demand storage finds them, because it
> measures the trip to both. The trip distance $d^{\mathrm{trip}}(v)$ of the storage vertices is reported
> for every warehouse size, because its spread is what adaptive storage can gain from. At 8 agents it runs
> from about 8 to 31 steps, averaged over 50 seeds.

(From `results/D_warehouses/step12/summary.md`, provisional until the sizing fixes the number of shelves.
Every seed at 8, 16 and 32 agents is well-formed at the first layout drawn.)

The TODO on a source for the U-shaped flow goes, since the flow is no longer a U.

## [A71] D25, two shelves per SKU

**`sec:impl:instances`, replaces "The shelves are the rack faces on both sides of every aisle and a row
along the front lane, and a shelf may hold several SKUs \nref{eq:feasiblestorage}." (660 to 662).**

> The rack faces on both sides of every aisle, and a row along the front lane, are where shelves and
> delivery vertices can go. After the delivery vertices are drawn, $2|\mathcal{K}|$ shelves are spread
> evenly over the rack faces left, two for each SKU, and the remaining faces become parking vertices. A
> shelf may hold several SKUs \nref{eq:feasiblestorage}. With a shelf on every rack face, every rule finds a
> free shelf next to a delivery vertex and the rules hardly differ. Two shelves per SKU keep storage scarce
> enough that a rule has to choose.

**Replaces "Each agent has one parking vertex ... from 58 at 8 agents to 1356 at 64 agents." (682 to 684).**

> The parking vertices are wall cells no receiving vertex takes, one per agent, and the rack faces that
> are neither shelf nor delivery vertex, so $|V_{\mathrm{ep}}| \ge m$ and an idle robot finds one nearby.
> The number of SKUs is TBD per fleet, set so that a SKU of middle popularity is refilled about four times
> per demand cycle (Appendix~\ref{app:storagecal}), and the shelves are twice that.

GAPS entry: on every rack face there were 58 shelves for 60 SKUs at 8 agents, and about 30 shelves near
each delivery vertex, so every rule placed stock next to one. Van Knippenberg et al. have no storage, so
the count had no value of its own (Appendix D). Two per SKU is the fewest that leaves room for a second
place while a refill is under way.

## [A72] D26, idle robots in the way

**`sec:pf:env`, roles paragraph, replaces "An idle robot waits at an endpoint in $V_{\mathrm{ep}}$, where
it blocks no one." (141 to 142).**

> A robot without a task may stay where it is. When it stands in the way, it goes to an endpoint in
> $V_{\mathrm{ep}}$, where it blocks no one.

**`sec:pf:observations`, after the current target is introduced (around 844), new paragraph.**

> A robot without a task has no pickup or delivery vertex, so its target is the vertex it stands on, and it
> may stay there. That changes when it is in the way. A robot is in the way when it stands on the pickup or
> delivery vertex of a task not yet finished, or when another robot tried to move onto its vertex and was
> stopped. Its target is then the nearest endpoint that no other robot stands on or is heading for and no
> unfinished task needs, until it gets there or receives a task. Token Passing parks a robot only for the
> delivery vertex of a task not yet assigned, which is the case its guarantee needs
> \citep{ma2017lifelong_mapf}. The learned controllers also need the other two cases, because they assign
> tasks without Token Passing's check that both ends of a task are clear. A robot in nobody's way is left
> alone, since a trip to an endpoint costs travel and adds to the crowding for nothing.

**Appendix C, `eq:currenttarget`, one more case.**

> $q_i(t) = e_i(t)$ when agent $i$ is free and was sent to the endpoint $e_i(t)$, and $q_i(t) = \ell_i(t)$
> when it is free otherwise.

(Check $e$ against the notation table first. If it is taken, pick another letter.)

**`sec:method:rl` (`4.Implementation.tex` 338 to 340), after "so an idle agent resting at its vertex pays
nothing."**

> An idle agent sent to an endpoint is rewarded for getting closer to it by the same shaping term as a
> task, and pays no wait cost.

GAPS entry: before, a learned robot's target with no task was its own vertex, so it stayed wherever its
last task ended, often on a delivery or receiving vertex, and the thesis's claim that an idle robot blocks
no one held for Token Passing only. Rejected: send every idle robot to an endpoint at once, which adds trips
and differs from Token Passing.

## [A73] D27, a warehouse per episode

**`sec:impl:instances`, replaces "Each seed always gives the same instance, which the split into training
and evaluation seeds relies on." (637 to 638).**

> Each seed always gives the same instance, and every episode plays the warehouse of its own seed. Training
> sees a new warehouse in every episode, one per episode of the budget, 250 at the current budget of 500 000
> steps in episodes of 2000. The validation and test seeds play warehouses no run trained on. One warehouse
> per episode is the most layouts a fixed budget can show, and with no layout repeated the router cannot
> learn one map by heart, so a result holds for the warehouses the generator draws rather than for one
> layout. Fewer warehouses seen several times would give more practice per layout and less variety, and they
> are the fallback if training does not settle (Appendix~\ref{app:training}). Every controller and storage
> rule plays the same warehouse on the same seed, so the comparison stays paired.

**Appendix J, the training setup, one sentence where the seeds are described.**

> Each training seed is its own warehouse, so the number of training seeds is the number of training
> episodes, and the window tables of every warehouse are built before training starts.

GAPS entry: the code fixed one warehouse per fleet (seed 42) while Appendix D's seed split read as one per
seed. The generator exists to give a family of irregular warehouses, so the claim is about that family, and
a test on unseen layouts shows whether the router has learned to route rather than one map.

## [A74] D28, stacked blocks of four rack rows, irregular aisles in every block

**`sec:impl:instances`, replaces "The aisles run from a front lane to a back lane, and some stop short of the
back lane. Two one-way rows cross the middle ... and a few links join neighbouring aisles."**

> The rack area is split into blocks of four rack rows. A two-way cross lane runs between neighbouring
> blocks, and at the centre two one-way rows take its place, one in each direction, like the two one-way
> central lanes of \citet{vanKnippenberg2021}. Joined at both ends they form a loop. No leaf hangs off a
> lane, so traffic across the warehouse never waits behind a robot at a shelf. A larger warehouse gets more
> blocks and more aisles rather than deeper ones, so a shelf is within four steps of a lane at every fleet
> size. With deeper blocks around one central loop, the aisles at 64 agents would be six times as deep as
> at 8 and all traffic across the warehouse would share one loop, so a difference between fleets would
> partly come from the building rather than the fleet. In each block the two outer aisles run from lane to
> lane. Every inner aisle hangs from the lane on the side of the central loop, at a length drawn from the
> seed, so some stop short in a dead end, in every block. Every other edge is two-way, and a few links join
> neighbouring aisles.

**Same section, the growth paragraph, after "...get 128, 256, 512 and 1024 vertices a robot can drive
through."**

> The shape is the most nearly square that holds them, 6 aisles and 2 blocks at 8 agents, 7 aisles and 4
> blocks at 16, 10 and 6 at 32, and 15 and 8 at 64.

**Appendix D.** The setting and method describe one pair of blocks with full lower aisles, and
`tab:instances` holds the counts of the first graph v2. Both follow the instance report on the stacked
layout (`results/D_warehouses/step12/`), drafted once its numbers are in.

GAPS entry: today's growth deepened the two blocks around one loop (4 rack rows at 8 agents, 24 at 64), so
congestion grew with the fleet partly because of the layout, which muddies any comparison across fleet
sizes. Blocks of a fixed depth keep the building around each robot the same. The lower block was full in
every seed, so the bottom half looked the same everywhere (the author, watching the layout, 2026-10-27).
Rejected: deeper blocks around one loop, more one-way pairs (several loops complicate routing for little
gain), and shelves along the central pair (it would block the loop, D3). Code `e1f6c2c` (irregular lower
block) and `9bc3bc4` (`num_blocks`, `v2_stacked_shape`). Revises `[A62]`.
