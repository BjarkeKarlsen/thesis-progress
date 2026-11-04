# Brief for an advisor: sizing the warehouse model

Written 2026-10-30. Self-contained: read this first, then the files listed at the end if you need detail.
Please check the reasoning and the numbers, say where they are wrong or weak, and propose better values
where you see them. Do not assume the proposal below is right.

## 1. The thesis in one paragraph

A Master's thesis on closed-loop coupling between storage assignment and multi-robot routing in a
warehouse. Robots pick goods from shelves and bring them to workstations, carry finished orders to docks,
and carry new stock from docks to shelves (put-aways). A storage rule decides which shelf new stock goes
to. The main result is how much shorter a pick is under **demand storage** (popular SKUs near where they
are needed) than under **fixed storage** (every SKU has a fixed home shelf), for several robot controllers.
The baseline controller is Token Passing (Ma et al. 2017). Learned controllers (PPO) are trained later and
should come close to Token Passing or beat it. Experiments run at 8, 16, 32 and 64 robots.

## 2. How the model works (what matters for sizing)

- **Warehouse.** A generated graph per seed, growing with the fleet (16 walkable vertices per robot).
  Rack faces along the aisles become workstations, shelves or parking spots. Docks are along the left wall.
- **Orders.** Poisson arrivals, `load` = order lines per step. An order has on average 5 lines (shifted
  Poisson, cited from Krnjaic et al. 2022), each a different SKU, 1 to 5 units per line (mean 3).
- **Demand.** SKUs ranked by popularity, Zipf with exponent 1. Every 200 steps the ranking shifts by 5 %
  of the SKUs, so it goes round once in 4000 steps (one "demand cycle") when the SKU count is a multiple
  of 20.
- **Tasks.** One pick per line (more if a line takes from two shelves), one shipment per order (from its
  workstation to a random dock), and put-aways for new stock.
- **Refills.** Every 100 steps (the storage period) each SKU is refilled with what was ordered since its
  last refill, in lots of Q units. Each lot is one put-away trip. So put-away trips per step = units
  ordered per step / Q = 3 x load / Q.
- **Safety stock.** Each SKU starts with Q plus a safety stock: the 99 % quantile of the units it is
  ordered in one storage period. Decided: sized at the most popular rank for every SKU, because the drift
  takes every SKU to the top once per cycle.
- **Token Passing rule that matters here.** A robot may not be given a task whose delivery vertex is the
  end of another robot's planned path. So each workstation can have only one pick "on its way" at a time.
- **Measured window.** 10000-step episodes, the first 5000 steps are warm-up and are not measured.

## 3. Decided by the author (treat as fixed unless you find a real problem)

- 8 robots get **4 workstations**. Workstations are m/2 in the old model (4, 8, 16, 32).
- **Each SKU belongs to one workstation's section.** Each seed splits the SKUs at random over the
  sections, equal sizes, fixed for the episode, no swaps. An order goes to a workstation of one section
  and draws all its lines from that section's SKUs by popularity. Fixed storage places homes near each
  SKU's workstation. Demand storage estimates a SKU's workstation from its recent lines.
- **Start.** Each SKU starts whole on one random shelf. Several SKUs may share a shelf. A SKU is not
  split over shelves at the start.
- 5 lines per order, Zipf 1, drift 5 % every 200 steps, storage period 100, safety stock at the top rank.

## 4. What the last experiment measured (Token Passing, 20 seeds, old settings)

Old settings: one line per order, 20/30/50/100 SKUs at 8/16/32/64 robots, Q = 30, m/2 workstations,
orders to a random workstation, 2 shelves per SKU.

- **Main loads** (0.6 of capacity, fixed storage): 0.105, 0.15, 0.18, 0.24 lines per step at 8, 16, 32,
  64 robots. Load per robot falls as the fleet grows, because the warehouse and the trips grow.
- **Gain** of demand over fixed storage: 9, 9, 5, 10 % shorter picks. Random storage is 12 to 22 % worse
  than fixed.
- **Refill formula verified:** refills per SKU per 4000 steps = 12000 x load / (SKUs x Q), within 0.2 of
  the measured counts.
- **Stock waits:** with safety stock at each SKU's starting rank, 6 to 14 % of orders waited for stock at
  Q = 15. With safety stock at the top rank (fleet 8, Q = 15) it fell to 0.0 %, picks 14 % faster.
- **Random workstation per order:** the shelves demand storage ranked best were only 3 to 10 % closer to
  the workstation an order actually used than an average shelf. This is why sections were introduced.
- **Congestion:** a pick is blocked 1 to 3 steps, 2 to 3 % of its time.
- **Test with 2 workstations at 8 robots** (sections of 10, 40 SKUs, 5 lines, Q = 12): robots busy only
  30 %, a pick waits about 120 steps for a robot, pick time 135 against about 45 with 4 workstations.
  Cause: the Token Passing rule above, with only 2 workstations at most 2 picks are in flight.
- **Rack faces left** for shelves after workstations and one parking spot per robot, on the tightest of
  20 warehouses: about 45, 95, 174, 368.

## 5. The proposal to check

Rules:
1. **Q = 10 at every fleet.** With 5 lines per order, a line makes 1 pick, 0.2 shipments and 3/Q
   put-aways, so put-aways are (3/Q) / (1.2 + 3/Q) = 20 % of trips at every fleet.
2. **SKUs = 300 x main load, rounded to a multiple of 20.** Then refills per SKU per cycle =
   12000 x load / (SKUs x 10) is about 4, enough storage decisions per SKU to follow the drift.
   (Equivalently: refills per SKU = 4000 x put-away trips per step / SKUs, so with the put-away share
   fixed the SKU count alone sets the refills.)
3. **Sections of 10 SKUs**, about twice the lines of an order, so an order still chooses by popularity.
   Sections = SKUs / 10.
4. **Workstations stay m/2**, so Token Passing is not throttled. A section is served by a group of
   workstations when there are more workstations than sections.
5. **Shelves = all rack faces** left after workstations and parking, rounded down: 40, 90, 170, 360.

| robots | main load (old) | SKUs | sections | workstations | per section | shelves | refills per SKU per cycle |
|---|---|---|---|---|---|---|---|
| 8 | 0.105 | 40 | 4 | 4 | 1 | 40 | 3.2 |
| 16 | 0.15 | 40 | 4 | 8 | 2 | 90 | 4.5 |
| 32 | 0.18 | 60 | 6 | 16 | 2 to 3 | 170 | 3.6 |
| 64 | 0.24 | 80 | 8 | 32 | 4 | 360 | 3.6 |

Plan: run the load sweep first on the new settings (the main loads will move, likely up, because 5 lines
per order means fewer shipments), apply rule 2 again to the new loads, then the sensitivity sweeps.

## 6. Questions for you

1. Is the reasoning of rules 1 to 5 sound? Is any formula wrong?
2. Is "about 4 refills per SKU per demand cycle" a sensible target, and is fixing the put-away share
   (via one Q) the right thing to hold equal across fleets?
3. Are 10 SKUs per section enough for orders of 5 lines? Does a section spanning several workstations
   cause a problem for the storage rules or for the comparison of fixed and demand storage?
4. Is m/2 workstations a sound way to avoid the Token Passing bottleneck, or is there a better rule
   (for example from the load per workstation and the trip length)?
5. With shelves allowed to hold several SKUs and about one shelf per SKU, is storage still scarce enough
   that the rules must choose? Does a shelf capacity need setting?
6. The SKU count depends on the main load, and the main load depends on the settings. Is one pass of
   "load sweep, then set SKUs" enough, or does it need to iterate?
7. Anything that makes the comparison of demand and fixed storage unfair, or that would make the learned
   controllers unable to keep up with Token Passing at these loads.

## 7. Files, if you need detail

All paths are under `~/Documents/thesis/`.
- `thesis-progress/results/README.md`, and the `E_load`, `F_demand`, `G_storage` READMEs: the last
  experiment, its commands and findings, and the sizing arithmetic (in `G_storage/README.md`).
- `thesis-progress/decisions/active/model_revision/README.md`: the decision log (D21 to D29).
- `thesis-progress/decisions/GAPS.md`, entries `[A75]` and `[A76]`.
- `thesis/Chapters/4.Implementation.tex`, section `sec:impl:instances` and `sec:method:storage`.
- Code: `slap-mapd-coupling/` on branch `feat/workstation-sections`, `environment/multi_agent_env.py`
  (order drawing, sections), `storage/arrival.py` (put-away rules), `training/spec.py` (start stock,
  safety stock). Uncommitted, and it still has one section per workstation and one SKU per starting
  shelf, so it does not yet match the proposal in section 5.
