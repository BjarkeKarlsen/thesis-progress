# 04. Stock without the floor, with a service level (proposed tag [A64])

**Decision** D8 of `README.md`, agreed 2026-10-26. Done in one session with step 05. **The brief for both is
`05_refill.md`.** This file keeps the reasons and what was decided for the stock alone.

## Why

Today each SKU is filled up to max(x_min, ⌈(1+ε) Δ ρ̂_unit⌉) every period (`eq:arrivals`). x_min = 8 is per
SKU over the whole warehouse, not per shelf. With 100 SKUs the floor alone is 800 units, while about 36 units
are ordered per period at 8 agents. So the floor sets nearly all stock, ε reaches only the 1 to 5 most popular
SKUs, and the sweep of ε from 0.25 to 2 changes nothing. Shelves were 78 % full at 8 agents and 16 % at 64,
because the stock stays about 950 room units while the shelves grow with the fleet.

## Decided

- x_min is removed from the model.
- ε is replaced by a service level, the textbook way (Axsäter, 2015, already in the bibliography). Each SKU
  starts with one refill plus the service-level quantile of a period's demand, and the refill rule of step 05
  keeps it there. The value is a convention (0.99 proposed), cited, not tuned.
- A stock-out stays possible but rare. A line that finds no stock waits for the next delivery (`[A39]`). The
  wait for stock is reported as a validity check that should stay near 0, like overflow.
- Arrivals stay the same under every storage rule, so the paired comparison stays fair.
- Unit sizes stay, for the room a unit takes on a slot only.
