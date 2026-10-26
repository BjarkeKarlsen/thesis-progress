# 03. Rename delivery vertex to workstation, receiving vertex to dock (proposed tag [A63])

**Decision** D7 of `README.md`. Text and code.

## Why

In Ma et al. (2017) every task has a pickup and a delivery location. Since `[A47]` a put-away's delivery
location is a slot, not a delivery vertex, yet the notation table says g_j ∈ V_del. Naming the roles by what
they are separates the two meanings, and "workstation" is the usual word in goods-to-person warehouses.

| now | new | symbol now | symbol new | what it is |
|---|---|---|---|---|
| delivery vertex | workstation | V_del | V_ws | where a pick ends and the order is packed |
| receiving vertex | dock | V_rcv | V_dock | where arriving stock enters and a put-away starts |
| pickup and delivery of a task | unchanged | s_j, g_j | unchanged | the two ends of any task |

The symbols are proposals. Check `thesis/Appendices/A.Notation.tex` and `notation_renames.md` (workspace
root) for clashes first.

## Thesis text

- `thesis/Appendices/A.Notation.tex`. Lines 38 and 39 (the role sets), line 100 (g_j ∈ V_del, which should
  become the union of the slots and the workstations, or say per task kind).
- About 12 mentions of "delivery vertex" in `2.Introduction.tex` and 10 in `4.Implementation.tex`, and the
  appendices. Read each one. Where it means the end of a task, it stays "delivery".
- `thesis/styles/eqnames.tex` if an equation name contains the word.

## Code

- `src/slap_mapd_coupling/core/graph.py`, `VertexRole`, and every use of the delivery and receiving roles
  (`core/tasks.py`, `environment/multi_agent_env.py`, `instances/generator.py`, `instances/validation.py`,
  `storage/*.py`, `planners/token_passing.py`, `evaluation/metrics.py` and `trace.py`).
- Metric field names that contain "delivery" in the role sense, for example
  `mean_pick_wait_delivery_taken`. Renaming a field breaks the readers in `thesis-progress/scripts/`. Change
  both, or keep the old name and say so in the field's docstring.
- Configs and the trace header (vertex roles).
- One PR for the rename alone, before or together with step 02, so the diff stays readable.
