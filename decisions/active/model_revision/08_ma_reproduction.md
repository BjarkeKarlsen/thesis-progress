# 08. Reproduce Ma et al. (2017) on their grid warehouse

**Decision** D14 of `README.md`.

## Why

A check of the simulator and of our Token Passing against a published result. A grid world is a special case
of our graph: every open cell is a vertex, with two-way edges to its open neighbours, which is how van
Knippenberg et al. (2021, Figure 5) convert benchmark grids. It is a check, not a new result, and goes in
`thesis/Appendices/K.Checks.tex`.

## Their setup (Ma et al., 2017, `thesis-progress/papers/3091125.3091243.pdf`)

- A 21 × 35 four-neighbour grid, 50 agents (Figure 4). Black cells are blocked, gray cells are task
  endpoints, and the agents' starting cells are the only non-task endpoints.
- 500 tasks with pickup and delivery drawn at random among the task endpoints.
- Task frequencies 0.2, 0.5, 1, 2, 5 and 10 tasks per step.
- Reported per frequency: makespan, service time and runtime, for TP, TPTS and CENTRAL.
- A large warehouse, 81 × 81 with 500 agents (Figure 6), for TP only.

## Steps

1. Rebuild the 21 × 35 map from Figure 4, or find a published map file. Check the cell count against the paper.
2. A grid loader in `slap-mapd-coupling` that turns the map into a `WarehouseGraph`, with the gray cells as
   task endpoints and the starting cells as parking.
3. A task mode with their task model, a fixed list of 500 tasks with random endpoints, no storage and no orders.
4. Run Token Passing at their frequencies, with their measures (makespan, service time), several seeds.
5. Compare with their table. Report the difference, and explain any gap (their tie-breaking, their task order).

## Later, if time allows

The same grid as a second instance family for the whole problem at one fleet size, as a robustness check.
Not the benchmark maps of van Knippenberg et al. (one-shot path finding, a different problem), which are only
cited.
