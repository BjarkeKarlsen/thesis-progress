# B1. Zones by aisle [simple]

Branch `fix/l4-zones`, from `origin/main`. Independent of every other package. No Ray anywhere in this package.
Read `00_rules.md` first.

## Goal

Give the section-based arm its zones. The author decided on 2026-10-13 that zones follow the aisles. A zone is a block
of consecutive aisles and a vertex belongs to the zone of its aisle. The thesis defines only the partition itself
(the zone partition, a disjoint cover of the movable vertices) and the halo, not how zones are drawn, so this is a
design choice and gets no citation.

## Thesis to read

`sec:pf:controllers` (the zone partition), `sec:method:controllers` (the halo), `app:notation` (symbols for zone,
halo and `d_obs`). Print them with `thesis_section.py`.

## Changes

1. `instances/generator.py`. Add `aisle_index: dict[VertexId, int]` to `GeneratedInstance`, the aisle number of every
   vertex, left to right from 0. Derive it where the lattice is built, from the lattice column of each vertex. Do not
   read the display `positions` afterwards, since the generator calls them visualisation metadata only. Add a
   validator beside `_metadata_must_match_graph` that the keys equal the graph's vertices. Confirm with a printout
   on the example 04 instance (seed 42) that there are 7 aisles and that cross-aisle vertices carry the column of
   their aisle. At origin/main the instance has aisle columns at x = 0, 1.5, ..., 9.0 and 51 movable vertices.
2. New `environment/zones.py`. Pure functions, no Ray and no torch.
   - `zones_by_aisle(graph, aisle_index, num_zones) -> tuple[frozenset[VertexId], ...]`. Sort the distinct aisle
     numbers of the movable vertices and split them into `num_zones` blocks of consecutive aisles, as equal as
     possible, with the earlier blocks taking the extra aisle. A movable vertex joins the block of its aisle.
     Raise `ValueError` if `num_zones` is below 1 or above the number of aisles.
   - `halo(graph, zone, d_obs) -> frozenset[VertexId]`. The movable vertices outside the zone within travel cost
     `d_obs` of some vertex of the zone (the halo definition in `sec:method:controllers`). Use `graph.distance`.
   - `check_partition(graph, zones) -> None`. Raise `ValueError` if two zones overlap or the union is not the
     movable vertices.
   - `zone_of(zones) -> dict[VertexId, int]`, the index of the zone owning each vertex.
   `num_zones` is a sweep parameter. Do not give it a default anywhere.
3. Docstrings name the thesis objects by name, not by label, and use the notation table's symbols.

## Tests (`tests/unit/test_zones.py`, plus the generator test file for `aisle_index`)

- `aisle_index` keys equal the vertices, and values are consecutive from 0.
- `num_zones = 1` gives one zone equal to the movable vertices and an empty halo.
- `num_zones` equal to the number of aisles gives one zone per aisle.
- 7 aisles into 3 zones gives 3, 2 and 2 aisles, and 7 into 2 gives 4 and 3.
- `check_partition` passes on every generated instance for several seeds, and raises on an overlap and on a gap.
- Cross-aisle vertices belong to the zone of their aisle.
- A halo across a zone boundary contains the neighbour on the other side when the edge cost is at most `d_obs`, and
  not when it is larger and no shorter path exists.
- `num_zones` above the number of aisles raises. Results are deterministic for a fixed seed.

## Done when

The new tests are written, `GeneratedInstance` gains `aisle_index` without changing any existing field, and the golden
comparison is unaffected (the generator output for existing seeds must not change graph, roles or costs).

## Do not

Do not touch the examples. `generate_and_validate` drops the instance, and fixing the examples belongs to package A6.
