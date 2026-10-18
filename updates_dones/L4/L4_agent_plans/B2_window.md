# B2. The window in the observation builder [review]

Branch `fix/l4-window`, from `origin/main`. Independent of B1 (use hand-built vertex sets in the tests). Read
`00_rules.md` first.

## Goal

A robot's observation is built over a window, the set of vertices the encoder runs on. For the decentralised arm it is
the field of view. For the centralised arm it is all movable vertices. For the section arm it is the robot's zone plus
its halo. This package adds the window as an input and the checks that go with it. It does not decide which window
a robot gets. The adapter (package A4) does that.

## Thesis to read

`sec:pf:observations` (the field of view, the observation, the congestion feature), `sec:method:controllers` (windows
and the halo), `sec:method:rl` (vertex features). Congestion stays defined on the `d_obs` field of view for every arm,
not on the window.

## Changes

1. `environment/observation.py`.
   - `build_observation(..., window: Sequence[VertexId] | None = None)`. `None` keeps today's behaviour, the field of
     view. Otherwise `Observation.visible_vertices` is the window.
   - The congestion feature is always computed over the `d_obs` field of view (`local_subgraph`), never over the window.
   - Features per window vertex are unchanged, including the per-robot distance label.
2. `models/local_subgraph_encoding.py`.
   - `encode_all_observations(..., windows: Mapping[AgentId, Sequence[VertexId]] | None = None)`. `None` means the field
     of view for every robot. The function stays pure and does not know which arm it serves.
   - A window larger than `max_local_nodes` raises `ValueError` in `encode_view` instead of truncating by distance label.
     Remove the truncating branch of `_select_nodes`. The author decided on 2026-10-13 that the cap never binds and
     that this applies to every arm. List every existing test that relied on truncation and rewrite it.
   - New `check_windows(graph, windows, encoding_config)` for use when an env is built. `windows` maps each vertex a
     robot can stand on to its window. It raises `ValueError` if a window omits its own vertex, omits an outgoing
     neighbour of that vertex, or is larger than `max_local_nodes`. Keep `check_slot_targets` working for the field
     of view, or implement it on top of the new check.
3. Docstrings. Update the two module docstrings that still describe truncation.

## Tests

- Three windows given as explicit vertex sets (a ball, all movable vertices, a hand-built zone plus halo). The padded
  arrays match the window, and the move slot arrays point at the right local indices.
- Congestion does not change when the window changes.
- A window above the cap raises. The old truncation tests are replaced.
- `check_windows` rejects a window missing its own vertex, a window missing an outgoing neighbour, and an oversized
  window, and accepts valid ones.
- `windows=None` gives exactly today's output (compare arrays against the previous behaviour on a fixture whose
  field of view fits the cap).

## Done when

Tests written, existing behaviour for `windows=None` unchanged on fixtures that fit the cap, and a list of every test
changed because truncation became an error.

## Flag in the hand back

That the cap rule now raises for every arm, which touches decision 15, and that example 04's cap of 12 will raise (package
A6 raises it).
