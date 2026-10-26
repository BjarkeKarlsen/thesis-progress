# 02. Warehouse graph v2 (proposed tag [A62])

**Decisions** D1 to D6 of `README.md`. This file is the brief for the session that builds it. Read
`README.md` (decisions, order, risks, rules) first, then this file to the end before writing code.

## Scope of this step

- **In:** the graph v2 generator in `slap-mapd-coupling`, its tests, a random storage rule (needed for test A),
  the instance report on graph v2, and test A.
- **Out:** the rename (step 03, so keep today's role names: `delivery` for workstations, `receiving` for docks,
  `endpoint` for parking), the arrival model (04, 05), the measures (06), training (10), and any text in
  `thesis/`. After test A, propose the thesis wording to the author and wait.

## Before starting

- `slap-mapd-coupling` `main` is at `e1abc67`, and the main checkout holds uncommitted work (M1 to M4 of
  `../measures_plan.md`: the check by kind, the new metrics, the shelf-taken waits, the timing log, the sweep
  scripts). Do not disturb it. Ask the author whether M1 to M4 are committed or put in a PR first. Test A needs
  their metrics (`keeps_up_picks`, `mean_pick_wait_pickup_taken`, `robot_busy_share` and others).
- Work in a git worktree, for example `~/worktrees/graph-v2`, branched from wherever M1 to M4 end up. Leave the
  work uncommitted and report the path. The author opens the PRs (memory "Author opens PRs").
- Where the code, the learned storage policy, the trained routers and the graph v1 instances live: `README.md`,
  "Where things live".
- Python is `~/.venvs/rl/bin/python`, never bare `python`. Run the tests with
  `~/.venvs/rl/bin/python -m pytest tests/unit -q` from the worktree.

## Why

On graph v1, storage could hardly change trip length. At 8 agents the 4 storage vertices were 11 to 15 steps
from delivery (`results/E_load/fleet_8/summary.md`, "Trip distance"), because the delivery vertices were spread
through the warehouse and each order picks one uniformly. The storage vertices sat on through-aisles, so a robot
serving one blocked the aisle, and Token Passing lets only one robot head for an endpoint at a time. Spreading
stock over shelves, which random storage does most, was what helped, not putting it near delivery.
`../../../notes/queue_findings_2026-10-26.md`, sections 2 and 3.

## The layout

Front at the bottom.

```
 back lane       ( )──( )──( )──( )──( )──( )        two-way
 racks       [s]( )[s] [s]( )[s] [s]( )[s]           aisles of different lengths, some dead ends
 main pair   ──→──→──→──→──→──→──→──→──→──→          one-way, opposite directions, no endpoints
             ←──←──←──←──←──←──←──←──←──←──
 racks       [s]( )[s] [s]( )[s] [s]( )[s]
 front lane  [s]( )──( )[s]──( )──( )[s]──( )        two-way, slots on its rack side
                 │    │    │    │    │
 front wall     [W]  [W]  [W]  [W]  [W]              workstations
 side wall   [D][D] near one front corner            docks
 walls       [P] parking
```

`( )` is walkable. `[ ]` is a leaf, a vertex with exactly one edge (two directed edges, one each way).

| part | rule | source |
|---|---|---|
| endpoints | every slot, workstation, dock and parking vertex is a leaf. A path cannot pass through a vertex with one edge, so no path between two endpoints crosses a third, which is the well-formedness of Ma et al. (2017). It holds by construction once the walkable part is strongly connected | van Knippenberg et al. (2021), Section 5 (start and goal nodes have one or two neighbours), Ma et al. (2017), Figure 4 (task endpoints beside the shelf blocks) |
| main pair | two one-way rows across the centre of the rack area, in opposite directions, joined at both ends so they form a loop. No leaf attaches to them | van Knippenberg et al. (2021), Figure 4 and Section 5 |
| front lane | a two-way row along the front wall. Workstation leaves on its wall side, slot leaves on its rack side, so the nearest slot is 2 steps from a workstation | U-flow layout. Source to find (Bartholdi and Hackman's textbook, to check) |
| docks | grouped at one front corner, on the side wall, and if needed round the corner onto the end of the front lane. Inbound and outbound are at the same end of the building | as above |
| racks | aisles run from the front lane to the back lane, crossing the main pair. Rack faces on both sides of every aisle vertex in the rack rows. Aisles of different lengths, some dead ends, and a few extra links between neighbouring aisles, the role van Knippenberg's diagonal edges play | `[A57]` (non-lattice shape), van Knippenberg et al. (2021) |
| parking | m leaves on the walls the docks leave free (side walls, then the back lane), out of the front traffic. Well-formedness needs at least m non-task endpoints | Ma et al. (2017) put the non-task endpoints on the border |
| size | 16 m walkable vertices (the lanes, the main pair and the aisles), the graph sizes van Knippenberg et al. use for 32 and 64 agents. Leaves come on top, so the floor space per robot is the same at every fleet size | `[A57]` |
| counts | m/2 workstations and m/2 docks, two robots per station as in `[A57]` | `[A57]` |
| slots | several SKUs per slot (`eq:feasiblestorage` unchanged). The slot count follows from the rack faces, with no parameter of its own | |
| edge costs | every edge costs 1 | `[A43]` |

Not taken from van Knippenberg et al.: their "can wait" node attribute. Agents may wait anywhere, and Token
Passing relies on that.

## What exists today (graph v1)

`src/slap_mapd_coupling/instances/generator.py`:

- `GeneratorParams`: `max_num_aisles`, `max_aisle_length`, `max_num_cross_aisles`, `num_transit_vertices`,
  `one_way_fraction`, edge cost settings, `wait_cost`, `num_storage_vertices`, `num_delivery_vertices`,
  `num_endpoints` (parking), `num_receiving_vertices`, `min_internal_role_vertices`, `role_backbone`, `seed`.
- `fleet_defaults(num_agents)`, line 276. `VERTICES_PER_AGENT = 16`, `FLEET_INSTANCE_SEED = 42`. Builds the
  warehouse of each fleet. Every edge two-way, m/2 storage, m/2 delivery, m/2 receiving, m parking.
- `_build` and `_try_build`, from line 376. Stages: `_sample_shape` (aisle lengths, cross-aisle rows),
  `_create_plain_topology`, `_create_transit_segments`, `_orient_transit_segments` (one-way segments, keeps the
  graph strongly connected), `_sample_well_formed_role_vertices` (puts roles on existing vertices and rejects
  until well-formed, receiving drawn from row 0), `_assign_roles`, `_create_graph`. A topology that admits no
  well-formed placement is discarded and the next attempt is drawn from `(seed, attempt)`.
- `GeneratedInstance`: `graph`, `positions` (display only), `aisle_index`, `aisle_lengths`, `cross_aisle_rows`,
  `num_transit_vertices`, `topology_attempts`.

`src/slap_mapd_coupling/core/graph.py`: `VertexRole` has the flags `movable`, `storage`, `delivery`,
`endpoint` (parking) and `receiving`, not an enum. `Edge` has `one_way`. `WarehouseGraph` precomputes all-pairs
distances at construction, so a bigger graph costs memory there (1024 walkable plus leaves at 64 agents).

`src/slap_mapd_coupling/instances/validation.py`: `check_connectivity` and `check_well_formedness(graph,
fleet_size)`. The latter needs at least m non-task endpoints, and every ordered pair of endpoints joined both
ways by a path avoiding every other endpoint.

Who uses an instance:

- `training/spec.py`, `instance_settings()` (line 268) and `build_instance()` (line 383). An empty `instance:`
  section in a config builds `fleet_defaults(num_agents)`. `build_instance` rejects an instance that fails
  either check. Every run (training, evaluation, the sweeps) goes through here.
- `environment/zones.py` and `training/arm.py`, line 71. The section-based arm draws zones as blocks of
  consecutive aisles from `aisle_index`. Every vertex of graph v2 needs an `aisle_index`, leaves included (a
  rack face takes its aisle's index, a lane vertex its column).
- `storage/arrival.py`, `trip_distance` (line 161): from the nearest receiving vertex to v, then to the nearest
  delivery vertex. It works unchanged, and its spread over the slots is what this step should widen.
- `scripts/instance/instance_report.py` (and an older `scripts/instance_report.py`): generates every fleet over
  many seeds, checks both conditions and reports sizes, roles, degree, discards and the trip distance of the
  storage vertices. Earlier output is in `thesis-progress/results/D_warehouses/`.

## What to build

1. **A layout switch.** Add `layout: Literal["v1", "v2"]` to `GeneratorParams`, default `"v1"`, so every older
   config and the graph v1 archive still build the same instance. `fleet_defaults()` returns `"v2"`. Add a
   `fleet_defaults_v1()` or a flag so graph v1 can still be rebuilt for the archive figures.
2. **The v2 backbone.** Columns are aisles. Rows from the front: the front lane, the lower racks, the main pair
   (two rows), the upper racks, the back lane. Reuse `_sample_aisle_lengths` for uneven aisles, so some aisles
   stop short of the back lane (dead ends). Exactly `VERTICES_PER_AGENT * m` walkable vertices.
3. **The main pair.** Edges on the lower main row point one way and on the upper row the other way. Join the
   two rows at both ends so they form a loop. Aisle edges crossing them stay two-way. Mark the one-way edges
   with `one_way=True`.
4. **Extra links** between neighbouring aisles at a few random rows, the role of van Knippenberg's diagonals.
   Default: one per pair of neighbouring aisles in each rack block, at a random row. Expose the count.
5. **Leaves.** Add, each with one two-way edge to its walkable vertex:
   - rack faces on both sides of every aisle vertex in the rack rows (role `storage`),
   - slots on the rack side of the front lane between aisles (role `storage`),
   - m/2 workstations on the wall side of the front lane, spread evenly (role `delivery`),
   - m/2 docks at one front corner, on the side wall from the front up, then round onto the front lane end if
     needed (role `receiving`),
   - m parking leaves on the walls left free (role `endpoint`).
6. **Display positions.** Leaves sit next to their vertex. Space the aisle columns (for example every third
   column) so the rack faces of neighbouring aisles do not overlap in a drawing. Positions are display only.
7. **Validation.** `check_connectivity` and `check_well_formedness` must pass for every seed and fleet, with no
   rejection loop needed. Keep `topology_attempts`, which should be 1.

## Tests (`tests/unit/test_generator.py`, `test_validation.py`)

- every endpoint has exactly one neighbour, and every walkable vertex is no endpoint;
- the walkable part is strongly connected, and the whole graph passes both checks, for fleets 8, 16, 32, 64 and
  50 seeds each;
- the main pair is one-way, forms a loop, and carries no leaf;
- the counts: 16 m walkable, m/2 workstations, m/2 docks, m parking, and the number of slots;
- docks are within a few steps of one front corner, and every workstation is a leaf of the front lane;
- every vertex has an `aisle_index`, and the section arm's zones still cover the graph (`environment/zones.py`);
- the same seed gives the same instance, and `layout="v1"` gives exactly the graph v1 instance (compare with a
  stored v1 instance, for example from `thesis-progress/results/D_warehouses/instances/`).

## Fit at 64 agents, check and report

32 workstations need a front lane of at least 32 vertices. 32 docks and 64 parking leaves need wall space.
Work out the front and wall lengths for each fleet from the shape before coding. If they do not fit, report the
numbers and the options to the author (two leaves on one wall vertex, a wider shape, parking also on the back
lane) rather than choosing silently.

## Random storage, needed for test A

`main` has no random rule. Under the arrival model a storage rule is a **put-away rule**, registered with
`@register_putaway_rule(...)` in `src/slap_mapd_coupling/storage/arrival.py` (next to `putaway_fixed`,
`putaway_demand` and `putaway_congestion`, lines 251 to 345), and called from `_arrive` in
`environment/multi_agent_env.py` (line 618). `storage/registry.py` holds the rules of the older template model
and is not the place. The pilot's random rule lives in `~/worktrees/pilot-learned-storage`,
`training/storage_ppo.py` (line 456), through the learned rule's hook, not as a rule.

- Add `putaway_random`, registered as `"random"`: each arriving SKU's units go to slots drawn uniformly among the
  slots with room, through the shared fill loop `_put_away`. Draw from a stream seeded by the run seed, so a seed
  always gives the same run and the four invariants of `slap-mapd-coupling/AGENTS.md` hold.
- Add `"random"` to `StorageMode` (`core/experiment_config.py`, line 19), and check that `scripts/sweep/load_sweep.py
  --storage-modes` accepts it.
- A unit test, and an `examples/` script if the repo convention asks for one (`AGENTS.md`, "Conventions").
- Check with the author that this small rule may go in the same PR or its own.

## Test A, after the generator works

**Question.** On graph v2 with today's arrival model, does demand storage beat random on picks, and does travel
per pick now drop under demand storage? (risk 2 of `README.md`)

1. **Instance report** for all four fleets:
   `~/.venvs/rl/bin/python scripts/instance/instance_report.py --configs configs/fleet_{8,16,32,64}/centralised.yaml --seeds 50 --out <dir>`.
   Report the walkable and leaf counts, the degree, and the trip distance of the slots (smallest, largest,
   ratio) against graph v1 (11 to 15 at 8 agents, ratio 1.36).
2. **A main load for 8 agents on graph v2.** The graph v1 loads do not carry over. A short fixed-storage load
   sweep: `scripts/sweep/load_sweep.py --config configs/fleet_8/decentralised.yaml --seeds 20
   --stop-when-overloaded --rates-per-agent 0.0125 0.025 0.0375 0.05 0.0625 0.075 0.0875 0.1 --out <dir>`,
   then the main load from its `capacity.json` (0.6 of capacity).
3. **The comparison** at that load:
   `scripts/sweep/load_sweep.py --config configs/fleet_8/decentralised.yaml --rates <main load> --seeds 20
   --storage-modes fixed demand random --out <dir>`.
4. **Report.** Per rule: picks and put-aways keeping up, pick service time, its split (wait for a robot, travel,
   blocked), the shelf-taken waits, robot busy share, put-away service time. The gain of demand over fixed and
   over random, paired by seed, with the 95 % interval. The graph v1 numbers to compare with are in
   `../../../notes/queue_findings_2026-10-26.md`.

Write the rows to `thesis-progress/results/tests/A_graph_v2/` with a `README.md` in the style of the other
results folders (what it answers, commands, code state). Read the result with the author before step 04.

## Thesis text, after test A and the author's approval

- `thesis/Chapters/4.Implementation.tex`, `sec:impl:instances`, lines 616 to 660. The `[A57]` sentences to
  replace: "The storage, delivery and parking vertices are drawn at random from the rest, so the delivery
  vertices are spread through the warehouse", "There are m/2 storage vertices, so agents often need the same
  shelf", and "every edge of the generated warehouses is two-way". The rejection paragraph ("A sampled topology
  that no placement ... can make well-formed is discarded") becomes well-formedness by construction. Graph v1
  in one clause, as the reason for the change.
- `thesis/Appendices/D.Warehouses.tex`: the generation, the four warehouses, the checks, and the trip distance
  spread per fleet.
- `thesis/Chapters/2.Introduction.tex`, `sec:pf:env`: check that nothing says roles may sit anywhere. The
  Problem Formulation should not change.
- The `[A62]` entry in `thesis-progress/decisions/GAPS.md`.

## Done when

- the tests above pass, and the whole unit suite still passes;
- the instance report shows every fleet well-formed on 50 seeds, with the counts and trip distances;
- test A is run and reported, with its folder and README;
- the worktree path, the changed files and anything decided along the way are reported to the author, with
  nothing committed.
