# Why `warehouse_grid.py` and `warehouse_visuals.py` stay outside `base.py`

`base.py` (introduced when `figure.py` was split into `base.py` +
`fig_*.py` modules) defines one specific, hand-tuned warehouse instance for
the Problem Formulation chapter figures:

- a `networkx.DiGraph` with string node ids (`"r_c"`)
- continuous, hand-set `(x, y)` positions (`dx=1.35, dy=1.15`)
- one genuine one-way edge (`ONE_WAY`), not just a drawing convention
- fixed `STORAGE` / `DELIVERY` / `ENDPOINTS` node-role lists

`warehouse_grid.py` and `warehouse_visuals.py` were considered for the same
treatment, but neither fits:

- **`warehouse_grid.py`** draws a notation *dependency* graph
  (`NOTATION_RELATIONS`: symbol → symbols it depends on), not a warehouse
  layout at all. It has no overlap with `base.py`'s graph.
- **`warehouse_visuals.py`** models a *generic* grid warehouse
  (`WarehouseGridConfig`: integer `(row, col)` cells, arbitrary
  `node_types`/`demand`/`flows` dicts) meant to be reused with any config.
  Its own `__main__` demo builds an unrelated 3x4 example, not the
  thesis's instance.

Forcing either onto `base.py`'s graph would mean one of:

- downgrading `base.py`'s continuous, aisle-based layout to a plain integer
  grid to match `WarehouseGridConfig`, losing the one-way-aisle structure
  the Problem Formulation figures depend on, or
- writing an adapter from `base.py`'s `G`/`POS` into
  `WarehouseGridConfig`'s shape, adding coupling for a case that doesn't
  exist yet — nothing today renders the thesis's actual warehouse instance
  through `warehouse_visuals.py`.

**Decision: leave both as standalone scripts.** Don't degrade or reshape
`base.py` to accommodate them. If `warehouse_visuals.py` is later meant to
plot the *same* instance as `figure.py` (not illustrative demo data), that
is a real use case worth revisiting — at that point, add a converter from
`base.py`'s `G`/`POS` into a `WarehouseGridConfig`, rather than changing
`base.py` itself.
