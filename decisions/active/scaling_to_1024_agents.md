# Scaling the warehouse to 128, 256, 512 and 1024 agents

**Status 2026-10-22. A requirement, raised by the author. Not started.** The fleet sweep must
reach 128, 256, 512 and 1024 agents. This note lists what stands in the way today, measured on
2026-10-22 with `slap-mapd-coupling` `main` at `0c2358f` (fleet warehouses of
`instances/generator.py::fleet_defaults`, 16 vertices per agent, so 2048 to 16384 vertices).

| agents | vertices | distance pairs | instance |
|---|---|---|---|
| 64 | 1 024 | 1.0 M | generates, 44 s |
| 128 | 2 048 | 4.2 M | **does not generate** with the fleet defaults |
| 256 | 4 096 | 16.8 M | not tried |
| 512 | 8 192 | 67 M | not tried |
| 1024 | 16 384 | 268 M | not tried |

## What breaks, in order

1. **The generator.** At 128 agents `fleet_defaults` gives "none of 100 sampled topologies
   admitted a well-formed role assignment". The shape bounds or the role placement must change
   before any larger fleet exists. The saved instances in `results/instances/instances/` stop
   at fleet 64.
2. **All-pairs distances.** `WarehouseGraph` keeps d_G for every pair of movable vertices in a
   Python dict, built at construction (3.2 s and 1 M entries at 64 agents). The number of pairs
   grows with the square of the warehouse, so 1024 agents needs 268 M entries, roughly 30 GB as a
   dict, more than the 31 GB machine has free. Options: a numpy matrix of small integers (edge
   costs are 1, so int16 holds every distance, 0.5 GB at 1024 agents), or distances computed on
   demand to the few targets in use.
3. **The crowding measure.** Fixed on 2026-10-22: it worked out every robot's field of view from
   scratch every timestep, agents times vertices distance look-ups, 92 % of a 64-agent episode.
   `WarehouseGraph.within` now keeps each vertex's field of view, so a 300-step 64-agent episode
   went from 36.9 s to 2.3 s with identical results. Branch `perf/field-of-view-cache`.
4. **Token Passing.** 11 ms per step at 64 agents. How it grows past 64 is not measured.
5. **The learned storage policy (pilot).** Its parameters do not depend on the size, but a
   minibatch of 128 over the whole graph needs about 0.6 GB at 1024 vertices and grows with the
   vertices, so about 10 GB at 1024 agents. The minibatch would have to shrink, or the policy
   look at a window around each shelf instead of the whole graph. Its traffic feature is a count
   per step, so it grows with the fleet and needs normalising before a policy trained small is
   tested large.

## Next step when this is taken up

Measure one episode per size once the generator builds the warehouse, with the distance table
replaced first, since it is the first hard memory limit.
