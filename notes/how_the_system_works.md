# How the system works

A plain description of the system the thesis studies, written 2026-10-20. It
replaces `thoughts.md` as the short version. `thoughts.md` stays as the raw
notes, and some ideas in it are out of date. The thesis chapters are the
source of truth. `../decisions/GAPS.md` gives the reason for each choice.

## The warehouse

The warehouse is a graph. Vertices are places a robot can stand, and edges are
the moves between them. Some vertices are shelves, some are delivery points
where orders leave, some are receiving points where new stock comes in, and
some are parking spots.

A fleet of robots moves on the graph. At most one robot stands on a vertex at
a time, so robots can block each other in narrow aisles.

## Orders and stock

Orders arrive over time. An order has several lines, each a product (SKU) and
a number of units. A robot fetches the units from the shelf nearest the
delivery point and carries them there. If no shelf holds the product, the
order waits until new stock arrives.

Demand is skewed and drifts. A few products are popular, and which ones are
popular changes over time.

Picking uses stock up. Every so often new stock arrives at the receiving
points. A robot carries each batch to a shelf, which is a put-away trip that
is served just like a pick. Stock already on a shelf never moves.

## The two decisions

The system makes two kinds of decision, and the thesis is about how they
affect each other.

**Where to store.** The storage rule decides which shelf new stock goes to.
There are three rules.
- *Fixed.* Every product has a home shelf, and its stock always goes there.
- *Demand.* Popular products go to shelves with short trips to the delivery
  points.
- *Congestion-aware.* Like demand, but it also avoids shelves where traffic
  is already heavy.

**How the robots move.** The router assigns tasks and chooses each robot's
next move. There are three learned routers, all graph neural networks trained
with PPO. They differ in how many robots one decision covers.
- *Centralised.* One decision covers the whole fleet. The robots choose one
  at a time, and each sees what the earlier ones chose, so they never clash.
- *Section-based.* The warehouse is split into zones. Inside a zone the robots
  choose the same way as the centralised router, and clashes between zones
  are resolved afterwards.
- *Decentralised.* Each robot chooses alone. It can optionally send learned
  messages to robots nearby.

Token Passing is a classic planner that is not learned. It runs next to the
three routers as a reference.

## Is the storage rule a SLAP?

Yes. The storage rule solves a dynamic storage location assignment problem
(DSLAP). Waubert de Puiseau et al. (2022) define DSLAP as choosing where
arriving goods are stored, and the arrival model does exactly that. Fixed
storage is classic static SLAP (dedicated storage). The demand rule is the
ABC-style rule that Waubert de Puiseau use as their baseline. What the thesis
adds is a live multi-agent router whose traffic feeds back into storage. Silva
et al. (2020) couple storage with picker routes, but they solve both once per
batch.

Three wording points follow (open, not yet in the thesis).
- `3.Background.tex` says the rule "updates storage as demand shifts". Since
  `[A38]` nothing is moved, so it should say the rule places arriving stock.
- The storage rules are hand-written formulas, not learned. The thesis should
  say so in one clause, because Waubert de Puiseau learn theirs with deep RL.
- "Assignment" means two things, storage assignment and task assignment. Say
  "storage rule" for the first and never "storage controller".

### Should storage be a PPO policy too?

Open, raised 2026-10-20, and kept as an extra to look into after the long run.
For now storage stays as rules. The case for and against, and a middle path
that adds a learned policy to RQ3 only, are in
`../decisions/ideas/learned_storage_policy.md`.

## The loop

Storage shapes the work, because where stock sits sets how far robots travel.
Traffic can shape storage, because the congestion-aware rule reads where
robots get stuck. Only the congestion-aware rule closes that loop. The demand
rule reads only the orders.

## How a run is judged

**First, does the fleet keep up?** A fleet keeps up when it finishes tasks
about as fast as they arrive. If the backlog keeps growing the fleet has
fallen behind, and the run is reported as such rather than compared.

**Then, how long does an order take?** The main measure is service time, from
when a task is released until it is delivered. It splits into three parts,
which are waiting for a robot, travelling, and being blocked by other robots.

## What the thesis compares

The main result is one comparison. How much shorter is service time with
demand storage than with fixed storage, and does that gain differ between the
centralised, section-based and decentralised routers? The gain is read as a
share of route time, so a router that routes badly is not rewarded for having
more to save.

The research questions build on that.
- **RQ1 and RQ2.** The main result above.
- **RQ3.** Does the congestion-aware rule add anything over the demand rule,
  that is, does closing the loop help?
- **RQ4.** How do the effects change with more robots (8, 16, 32 and 64) and
  more orders?
- **RQ5.** Do messages help the decentralised router? This one is optional.

## Choices worth remembering

- Costs and step values follow van Knippenberg et al. (2021), so the thesis
  does not pick its own numbers.
- The order load is set from a Token Passing sweep and scales with the fleet.
  The exact share is still open.
- Every router gets the same training budget.
- Storage costs robot time, because put-aways are real trips. That cost is
  part of total service time, not a separate number.

## Where to read more

- `../decisions/active/thesis_plan.md`, the full plan with figures and open
  questions.
- `../decisions/GAPS.md`, one entry per decision tag.
- `../decisions/decision_log.md`, decisions still waiting on the author.
