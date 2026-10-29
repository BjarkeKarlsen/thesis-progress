# 12. Shipping, an empty start, random workstations, two slots per SKU

**Decisions** D21 to D26 of `README.md`. Agreed with the author on 2026-10-26, evening, in a discussion
that started from watching a Token Passing run in the new viewer (step 09). The open questions were settled
on 2026-10-27 (section "Settled") and implementation started that day (section "Implementation").

## Why

Watching one run (8 agents, demand storage, rate 0.12, 2000 steps, `~/thesis_runs/watch/`) showed:

- Only 8 refills in 2000 steps, against 262 picks. A refill of Q = 30 units comes only once a SKU has
  sold 30 units since its last one, and 779 units over 60 SKUs is about 13 per SKU. So storage makes very
  few decisions (risk 3).
- Shelves start 40 % full (D19) with the popular SKUs nearest the workstations, so the starting layout,
  the same under every rule, decides most of where the stock is. The back half of the warehouse stays
  empty and the robots shuttle between the front slots and the front wall. So maybe we should only start with 10% full or nothing at all?
- Every refill came in at dock 132, the dock nearest the slots that demand storage chose. This should be a random dock. 
- Nothing ever goes back to a dock. An order leaves at its workstation, so the flow is only a U because the
  workstations happen to sit at the same end as the docks.
- The workstations are always on the front wall, so the traffic always meets at the same vertices. Workstation should be random places where storage nodes also are placed. 
- Most leaves are slots: 58 of 202 vertices at 8 agents, 1356 of 2508 at 64. Van Knippenberg et al. (2021)
  have no storage at all (their start and goal nodes are every node with one or two neighbours outside the
  central lanes). What we took from them is the size, 16 walkable vertices per agent. Appendix D says the
  shelf count "follows from the rack faces, so it has no value of its own". Here think if we have this much storage, does it not become that all nodes need to a workstation has 30 vertexes of storage and then the idea is not helping. So we have to degress the amount of storage in total. 

## Settled 2026-10-27

The questions of 2026-10-26 were discussed over four rounds. What was agreed:

- **D21, shipping.** When the last line of an order reaches its workstation, one shipping task carries the
  order to a dock drawn at random. The order is done when it leaves at the dock. The workstation holds
  whatever arrives, with no capacity and no processing time (both stay outside, D13 is otherwise replaced).
  Shipping is an ordinary task, assigned oldest first like the others (D11), and under Token Passing taken
  by its own task rule. Orders keep several lines. Refills also come in at a dock drawn at random, so the
  inbound traffic spreads over the docks. The docks are spread evenly along the whole left wall, front to
  back, so the traffic to them also enters through the middle (author, 2026-10-27, replacing "the docks stay
  grouped at one front corner" of the same day).
- **D22, one start.** Every SKU starts on one slot drawn at random, with its S_k units (step 05's service
  level). With slots = 2 x SKUs half the slots start empty, and the start carries no demand information, so
  no rule gets a head start. Training and evaluation start the same way, so the router learns on the kind of
  warehouse it is judged on. Evaluation adds a warm-up of about 5000 steps before scoring, so the storage
  rule's refills replace the random start. Training has no warm-up. The stall (D18) counts from the end of
  the warm-up, which `longest_completion_gap` already does. Replaces D19, the empty start and D23.
- **D24, random workstations.** Drawn at random among the rack faces, per seed. Docks along the left wall, see D21.
- **D25, slots and SKUs.** Measure throughput under Token Passing at the main load first. Then choose the
  SKU count and Q so a middle-ranked SKU is refilled about 4 times per demand cycle (4000 steps). Slots =
  2 x SKUs, spread evenly over the rack faces left after the workstations. Slot capacity holds S_k of the
  most popular SKU. One SKU per slot only at the start, later a slot holds several (D5). The rack faces that
  are neither workstation nor slot become parking leaves, so parking sits all over the warehouse. The
  walkable graph does not change.
- **Orders** stay drawn over every SKU. Every SKU is stocked from step 0 and the service level keeps it in
  stock, so a line seldom waits. Test B reports the share of lines that waited (`lines_waited`), and a share
  well above 1 % means S_k or Q is wrong, not the order stream.
- **D26, idle robots.** Every controller follows Token Passing's parking rule: when a waiting task needs the
  vertex an idle robot stands on, the nearest free parking leaf becomes its target, reserved for it.
- **Well-formedness.** Only leaves change, so it holds as long as there are m parking leaves. Checked per
  seed by the generator.

Token Passing's trigger, checked 2026-10-27 (`planners/token_passing.py`, rule 2 of the module docstring,
`_stay_or_park`): it parks only when an **unassigned** task has its **delivery** vertex where the robot
stands. Pickups need no rule there because rule 1 never hands out a task whose pickup or delivery is the
end of another robot's path. The learned controllers assign oldest first without that availability rule,
so copied word for word the trigger misses an idle robot standing on the pickup of an assigned task. See
"Implementation", part E.

## What it touches, once agreed

- Thesis, model: `sec:pf:tasks` (a third task kind, when an order is complete), `sec:pf:measures`
  (`eq:servicetime` ends at the dock), `sec:pf:storage` (the start), `sec:pf:env` (roles). Implementation
  and appendices: `sec:impl:instances` and Appendix D (placement, slot count, `tab:instances`), Appendix G,
  Appendix H (the warm-up), `tab:evalparams`. New `[Axx]` tags and entries in `../../GAPS.md`.
- Code: `instances/generator.py` (roles), `environment/multi_agent_env.py` (shipping tasks, empty and random
  starts), `core/tasks.py` (the task kind), `evaluation/evaluator.py` (service time), `planners/token_passing.py`
  (the third task kind), the trace and the viewer (a shipping colour), configs.
- Redo after it: tests A to D, the Ma et al. check only if the planner changes, figures 1 and 2 of step 09.

## Implementation

Branch `feat/flow-and-start` from `main` (`f52b6c5`), committed as `e0090d0` and pushed on 2026-10-27, checked out
in the main checkout (the worktree `~/worktrees/flow-start` was removed). Not merged. One part at a time, targeted tests per part.

- **A, layout (D24, D25).** `instances/generator.py`, `_build_v2`: the rack faces are drawn as today, the
  workstations at random among them (seeded), then `num_storage_vertices` slots spread evenly over the rest,
  the remaining faces parking. `dock_placement: left_wall` spreads the docks along the left wall. The
  defaults keep today's layout, so old configs still build. The fleet defaults switch in part D.
- **B, start (D22).** `training/spec.py`: `initial_placement: random_slots`, each SKU on one slot drawn at
  random with S_k units, at most one SKU per slot, the capacity derived from the largest S_k * b_k.
- **C, shipping and docks (D21).** `core/tasks.py` (kind `ship`), `environment/multi_agent_env.py` (release
  a ship task when an order's last pick is delivered, a random dock per refill and per shipment, seeded),
  `evaluation/evaluator.py` (an order is done when its ship task is), the trace and the viewer.
- **D, sizing (D25).** Measure throughput, then set the SKU count and Q in the configs. Needs A to C.
  Until then the step 12 settings stay in `configs/step12/` (author, 2026-10-27). After the sizing they go into
  all three arm configs of every `configs/fleet_<m>/`, `configs/step12/` is deleted, and the `step12` job and
  the watch command point back at `configs/fleet_<m>/`.
- **E, idle robots (D26, refined).** For the learned controllers: an idle robot gets the nearest free parking
  leaf as its target, reserved for it, when its vertex is the pickup or delivery of an unfinished task, or
  another robot tried to move onto it this step and was stopped (author, 2026-10-27).
- **F, a warehouse per episode (D27).** The episode seed draws the warehouse and the start. 250 training
  warehouses built ahead of time and stored, validation and test seeds their own.

Status 2026-10-27: A, B and C coded with their tests (`test_generator_v2.py`, `test_random_slots.py`,
`test_shipping.py`). D and E not started. Choices made while coding, to confirm:

- The random start is drawn from `storage.seed`, once per study, so every episode of a training run and
  every evaluation episode start from the same layout. Not redrawn per episode.
- With random docks the put-away rules still score a slot by its nearest dock, since the dock is drawn
  after the slot. The trip itself starts at the drawn dock.
- A ship task names the SKU of its order's first line, and carries all the order's units.
- In the keep-up split, ship tasks count on the pick side (everything that is not a put-away).
- The fleet defaults and configs are unchanged, so every existing run builds as before. Part D switches
  them once the SKU count and Q are measured.

Status later 2026-10-27: E coded (`idle_parking` in the experiment section, `test_idle_parking.py`), on in
`configs/step12/`. D is queued as the `step12` job of `bedtime.bash` on the provisional configs
`configs/step12/fleet_<m>.yaml` (20, 60, 140, 320 SKUs, Q = 30), not started. F not started, see below.

**F, what it takes.** Today the network is tied to one graph. The window tables (`models/window_tables.py`)
are built from the graph and travel in the module's model config, so a checkpoint carries them, and the
observation space size is the window count of that graph. Measured per warehouse, the decentralised arm's
tables are 0.9 MB at 8 agents, 2.1 MB at 16 and 4.2 MB at 32 (about 9 MB expected at 64). For 250
warehouses that is 0.2, 0.5, 1.0 and about 2.3 GB, held by every env runner and the learner. Proposed
design: build the pool once and store each warehouse with its tables on disk, a sample names its
warehouse as well as its vertex, and the module loads tables per warehouse as batches need them, keeping a
few in memory. The checkpoint then carries the weights and the pool's path, and evaluation on unseen
warehouses loads theirs the same way. Touches the env adapter, the module, the learner's context rows,
the evaluation loader and the section arm's zones (one set per warehouse).

Status 2026-10-27, evening: F coded as designed. `warehouse_per_seed` in the spec, the pool in
`training/warehouses.py` (tables under `~/thesis_runs/warehouses/<fleet>_<arm>_<hash>/`), vertex keys and
`StoredWindowLookup` in `models/window_tables.py`, the adapter switches warehouse at reset, evaluation and
the load sweep play each seed's warehouse, and `evaluate --trace-seeds N` writes traces that carry the
seed's own warehouse. On in `configs/step12/` with 250 training seeds. `test_warehouse_per_seed.py`: the
module gives the same logits and values on keyed samples from two warehouses as on padded samples, for the
decentralised, centralised and section arms. A 2-iteration training run with 2 env runners and its
evaluation with traces ran. Preparing a pool builds the tables of every seed of the split before training,
which is minutes at 8 agents and likely hours at 64.

## Sizing proposal (part D, 2026-10-29)

From the step 12 sweep (`results/tests/step12_sweep/README.md`, which has the arithmetic and the check).
Decided by the author on 2026-10-29, logged as "D25, sized" in the README.

- **Q = 12 at every fleet.** Put-aways are then the same share of trips at every fleet and SKU count, 17 %
  with 5 lines per order and 11 % with one.
- **n = 250 x main load, rounded to a multiple of 20.** Every SKU then gets about 4 refills per 4000-step
  demand cycle (12000 x load / (n Q)), and the 5 % rotation share is a whole number of SKUs, so the
  ranking turns in exactly 4000 steps. At today's main loads n = 20, 40, 40 and 60 (refills 5.3, 3.8, 4.5
  and 4.0), slots 40, 80, 80 and 120. The rerun's main loads will move with the extra put-aways, and the
  rule is applied once more to them.
- **Found on the way.** The sweep's 30 and 50 SKUs made the ranking turn in 3000 and 5000 steps, not
  4000. There is room for more slots than the configs used (45, 95, 174 and 368 at most). The orders
  of `configs/step12/` have one line each, since no `lines_per_order` is set, while D21 keeps several
  lines per order. The rerun switches them on, 5 lines on average as in `[A46]`
  (`lines_per_order: {distribution: shifted_poisson, mean: 5}`), decided by the author on 2026-10-29.
- **Open.** The waits for stock are far above the 1 % aim at small Q (5.7 % to 14 % of orders at
  Q = 15). The likely cause is that S_k is sized at each SKU's rank at t = 0, while the rotation takes
  every SKU to the top. Checked on fleet 8 at Q = 15 with every SKU's safety stock sized at rank 0: the orders that waited
  fell from 5.7 % to 0.0 % and picks got 14 % faster, for 24 % mean shelf fill against 17 %. Decided by
  the author on 2026-10-29: S_k = Q + the rank 0 quantile for every SKU ("D25, safety stock"). Still to
  do: `refill_starting_stock` in the code, and the starting stock in the thesis with an `[Axx]` tag.
- **Workstations (D29, 2026-10-29).** Each SKU belongs to one workstation, so `num_delivery_vertices`
  becomes n / 10, 2, 4, 4 and 6 at today's SKU counts, and follows n when the rule is re-applied.
- Configs not changed yet. They change when the step 12 settings move into `configs/fleet_<m>/`.

## Also left from 2026-10-26

- The round of `#103` for the merges since `689a80b` (#188 to #197) was started and stopped by the author.
  Nothing was posted. Areas: scoring and horizon, stock and storage, instances and the Ma check, and the
  trace and viewer (only a known catch-up there, the step 03 rename: the viewer and figures say slot,
  workstation and dock, the chapters still say storage vertex or shelf, delivery and receiving vertex).
- Offered, not done: label the SKU rows of the viewer "#43" and "44 units", with a small "rank, SKU,
  units" line over each list, since the bare rank and amount were misread.
