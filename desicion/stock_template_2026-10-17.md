# Stock as a placement template, 2026-10-17

Discussion paper. **Status: superseded on 2026-10-18 by the arrival model
(`arrival_storage_plan.md`, thesis tags `[A38]` to `[A40]`).** Picks now use stock up and the
storage update puts arriving stock away, so the template reading, the unit-proportional pickup
and the one-epoch lag are no longer needed. The tags `[A38]` to `[A40]` proposed below were
never applied and are now used by the arrival model. Original status: proposal. Nothing in the
thesis or the code is changed yet. The pending items are in `thesis-progress/temp/GAPS.md`,
"Still open". Two GitHub issues are drafted but not opened.

## The question

The author asked how stock gets into the warehouse. Tea is picked at a storage vertex and
delivered to a delivery vertex. What happens when the tea runs out, and does the thesis
cover it?

## What the model and the code do now

Checked in the code and the thesis.

- **Stock never runs out and is never refilled.** `x_t` changes only when an episode starts
  (`environment/multi_agent_env.py:276`) and at a storage update (`:394`). A pickup removes
  no unit and a delivery adds none.
- **The model already says this.** Between storage updates, "routing proceeds as normal
  while `x_t` simply stays fixed at its last updated value" (`2.Introduction.tex:444-447`).
  If a pick lowered the count, `x_t` would change at every pick.
- **The delivery vertex is the outbound station.** Delivered stock leaves the warehouse and
  never comes back into storage.
- **Every SKU can always be ordered.** The storage rules keep each SKU's total when the cap
  binds (`storage/relocation.py:28-30`). On the 8-agent instance the greedy target always
  fits (about 928 of 2000 units of capacity), so no unit is ever lost.
- **An order's pickup vertex is drawn uniformly** among the vertices that hold its SKU
  (`multi_agent_env.py:520`, `4.Implementation.tex:732`). The unit counts play no part.

So `x_t` is a **placement template**, not an inventory level. It says where each SKU can be
picked and how much shelf space it takes.

## Reading the template as put-away

The storage update stands in for replenishment and re-slotting together. It decides which
shelves hold each SKU from the next epoch on, as a warehouse decides where incoming stock is
put away. This is the classical meaning of the storage decision. Waubert de Puiseau et al.
(2022, `WaubertdePuiseau2022DynamicSL`, already in `references.bib`) define the dynamic SLAP
as "determining where to optimally store goods in a warehouse upon entry or reentry into the
system".

The reading needs no new vertices, no inbound tasks and no replenishment policy, and the
storage layer supplies what a refill would. It keeps the study on its question, which is
where stock is kept and how that couples with routing.

## Problems found

1. **The thesis contradicts itself.** `2.Introduction.tex:601-604` says "if inventory
   depletion and replenishment are not simulated", and `:1634-1636` says they "are modelled
   only if stated". Both treat the question as open, but `:444` already settles it. Wording
   such as "a valid starting inventory" (`:440`) and "stock that is not physically there"
   (`:595`) reads like physical stock that runs out.
2. **The pickup draw ignores units.** A vertex holding 1 unit of tea gets as many tea orders
   as one holding 12. Under the template reading a unit is shelf space, so more space near
   the delivery vertices should serve more orders. This matters because the cap ν binds at
   every update (48.0 units per update in every adaptive row of the short run). A capped
   update applies part of a move and can leave a SKU split between its old and new shelves.
   One leftover unit then keeps half of the SKU's orders at the old shelf. **Not measured:**
   how often SKUs are split after an update.
3. **Keeping each SKU's units is unstated.** The set of storage rules
   (`2.Introduction.tex:504-511`) admits a rule that drops a SKU, which could then never be
   ordered again. The code keeps totals only when the cap binds. When it does not, the greedy
   target is used as it is (`relocation.py:71`), and that target may leave units unplaced
   (`storage/demand.py:17`). This is harmless today and not guaranteed in general.
4. **The instant switch favours adaptive storage.** At an epoch the new placement holds at
   once and no robot carries anything. A real move through put-away takes effect slowly, as
   old shelves empty, and the put-away trips use the same aisles as picking. Fixed storage
   also gets free refills, so that part of the comparison is fair. The moves are the only
   extra gift to the adaptive rules.
5. **The coupling sits in the pickup choice, not in the stock condition.** With every SKU
   always in stock, `eq:coupling` never filters an order. Storage enters routing through
   which vertex an order is picked from.

## Options

**A. Physical inventory with replenishment.** Picks lower `x_t`, and inbound tasks bring
stock from a receiving vertex. Not proposed. It adds a second task type, inbound vertices, a
refill policy and stockouts. Each is a new factor in the storage-against-routing comparison,
and the time left does not allow it.

**B. Template with the put-away reading (proposed).** Keep the model, state it, and fix
points 1 to 3. The cost of the free switch (point 4) is reported, not modelled.

**C. Template with a delayed switch.** As B, but each update takes effect one epoch later.
Proposed as a check on B, not as the model.

## Proposed solution

### 1. Wording in the thesis (clarity, becomes `[A38]` when applied)

After the definition of `x_t` (`2.Introduction.tex:349`):

> Picking does not empty a shelf. The storage update stands in for replenishment and
> re-slotting together. It decides which shelves hold each SKU from the next epoch on, as a
> warehouse decides where incoming stock is put away \citep{WaubertdePuiseau2022DynamicSL}.
> The change takes effect at once and moves no robot, which favours adaptive storage, so the
> stock it would move is reported as a cost.

Replacing `2.Introduction.tex:601-604`:

> Because picking does not empty a shelf and the storage update never removes a SKU, every
> SKU can be ordered at every timestep. The stock condition decides where an order is
> picked, not whether it can be placed.

In the scope list, replacing `2.Introduction.tex:1634-1636`:

> Picks do not use up stock and nothing is replenished, so $x_t$ is a placement template,
> not an inventory level.

### 2. Keeping each SKU's units (model change, `[A39]` when applied)

Thesis, with the set of storage rules (`2.Introduction.tex:505`):

> The storage update moves units and never adds or removes them, so each SKU keeps the
> amount it starts with. Formally, every $F \in \mathcal{F}$ keeps
> $\sum_{v} x(k,v)$ for every $k \in \mathcal{K}$.

Code: check after every storage update that each SKU's total equals its total in
`x_{t-Delta}`, and fail loudly if not. Decide what the greedy rule does when a SKU does not
fit. It can fail, or the instance generator can guarantee enough capacity. No result changes
on today's instance.

### 3. Pickup in proportion to units (model change, `[A40]` when applied)

Draw the pickup vertex with probability `x_t(k,v) / sum_v' x_t(k,v')`. Map the same uniform
number `u_pickup` through the cumulative unit counts, with vertices in id order. The
generator draws the same random numbers as today, so the order stream of a seed stays
identical under every storage rule and the pairing holds.

Thesis, `4.Implementation.tex:732`:

> The pickup vertex is drawn among the vertices that hold the SKU, in proportion to the
> units each holds, so more shelf space near the delivery vertices serves more of the
> SKU's orders.

And next to `eq:coupling` in `sec:pf:tasks`, one sentence saying that storage enters
routing through this choice.

Consequences:
- Every adaptive-storage result changes, including the demand probe and the short run of
  2026-10-17. The long run should use the decided rule.
- `demand_blocks` puts each SKU at one vertex, so the two draws coincide under fixed storage
  and fixed-storage results should not change. To confirm when implemented.

### 4. The instant switch (a check, no model change)

Measure the adaptive rules with every update applied one epoch late, without retraining. If
adaptive storage still beats fixed storage with the lag, the instant switch is not what
carries the result. Report it with RQ1.

## What follows for the runs

- The short run in progress uses the uniform pickup. It validates training and measurement,
  and its adaptive-storage numbers are superseded once point 3 is adopted.
- Point 3 should be decided before the long run, and implemented in a small fix PR from
  `main` with a test that the order stream is unchanged.
- Point 2 needs a check in the code but no rerun.
- The relocation cost stays reported next to the gain. Under the put-away reading it is an
  upper bound on the extra work, because a real warehouse would make most of these moves
  during put-away anyway.

## Decisions asked of the author

1. Adopt the put-away reading and the wording of section 1? (Recommended.)
2. Adopt the rule that every update keeps each SKU's units, in the thesis and checked in the
   code? (Recommended.)
3. Adopt pickup in proportion to units before the long run? (Recommended. It changes the
   adaptive-storage results.)
4. Run the one-epoch-lag check with the long run's measurement? (Optional, cheap.)

## Measured or inferred

Measured: the code paths and line references above, the 48.0 units per update in the short
run's Token Passing rows, and the 928 of 2000 capacity on the 8-agent instance. Inferred, not
measured: that SKUs are often split after a capped update, that partial moves lose much of
their effect under the uniform draw, and that the instant switch overstates the gain.
