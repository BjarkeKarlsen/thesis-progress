# 09. Figures that show the structure

**Decision** D15 of `README.md`.

## Why

The graph v1 finding (spreading stock helps, distance does not) was only visible in numbers, and a reader
would not follow it. The new model has to be shown, and what the storage rules do with the stock too.

## Figure 1. The instance

The four warehouses, drawn in van Knippenberg et al.'s style (their Figures 1 and 4): roles coloured, leaves
visible, one-way edges as arrows. Next to it, or in the appendix, the grid drawing we already have. Goes in
`thesis/Appendices/D.Warehouses.tex` and, for one fleet, in the chapter.

## Figure 2. The stock per slot at a few moments

One fleet (8 agents is easiest to read), one seed, at a few steps (for example after the warm-up and a quarter
and a half demand cycle later), under fixed, demand and random storage. Per slot, the stock split by SKU
popularity rank (a colour scale), its fill against the slot capacity, and how many tasks wait for it. It
shows where each rule puts popular stock and where robots queue.

Needs a trace extension. The trace logs agents and the backlog per step but not the stock. Log the stock per
slot every Δ steps (it only changes at put-away deliveries and picks), and the tasks waiting per slot.
`src/slap_mapd_coupling/evaluation/trace.py`, and `../trace_extension_plan.md`, which already plans the
waiting tasks.

## For exploring, not for the thesis

An interactive view with a step slider over the same trace would help find what Figure 2 should show. Optional.

## Graph v1

Both figures drawn once for graph v1 too, so the thesis can show in one picture why the design changed.
