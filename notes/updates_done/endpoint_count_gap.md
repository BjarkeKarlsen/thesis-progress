# Gap: the endpoint count differs between the thesis, the validator and the environment

Found 2026-10-13 while implementing Token Passing (B18, branch
`fix/token-passing-planner`). For the author to decide. Related to B19 (the
thesis edits) and to the well-formedness paragraph in `2.Introduction.tex`.

## What is undetermined

Three places count endpoints in three different ways.

| Where | What it requires |
|---|---|
| Thesis, `2.Introduction.tex`, well-formedness paragraph | at least m non-task endpoints, where m is the fleet size |
| `slap-mapd-coupling/src/slap_mapd_coupling/instances/validation.py`, `check_well_formedness` | at least m endpoints, counting V_ep, V_str and V_del together |
| `slap-mapd-coupling/src/slap_mapd_coupling/environment/multi_agent_env.py`, `_initial_agent_vertices` | at least m vertices with the V_ep role, otherwise `ValueError` at `reset` |

Ma et al. (2017), Definition 1, ask for no fewer non-task endpoints than agents.
Their endpoints are every initial agent location, every pickup and delivery
location and any extra parking. The non-task endpoints are the ones that are not
pickup or delivery locations.

## Why the count matters

Token Passing finds a path for the agent that asks for the token because at most
m - 1 other agents can be resting on non-task endpoints, so one is always free to
park on (their Property 2). With fewer than m, a parking agent can find none free.
It would then stay on a delivery vertex, tasks delivering there would become
unavailable, and the run would stall. The code does not throw in that case.

## What happens today

A generated instance with 6 storage vertices, 3 delivery vertices and only 2 V_ep
vertices, validated for a fleet of 3 with `require_well_formed=True`, is accepted as
well-formed. `WarehouseMAPDEnv` with 3 agents then raises at construction, "instance
has 2 endpoints (V_ep) but 3 agents".

So the validator accepts an instance the environment cannot run. The environment
check catches it, but by accident, and the validator's count is still weaker than
the thesis text.

## Why the code cannot resolve it

Which count is right is a statement about the model, so it belongs in the thesis.
Changing the validator first would make the code say something the thesis does not.
`sec:pf:env` also says the roles may overlap, so the thesis has to say whether a
V_ep vertex that is also a storage or delivery vertex counts as a non-task endpoint.

## Decision needed

Done 2026-10-13 for the thesis text, see `GAPS.md` [A28]. The well-formedness paragraph now
defines a non-task endpoint as a vertex of V_ep in neither V_str nor V_del. The validator
change below is still to do.

1. State the condition as "at least m vertices in V_ep that are in neither V_str
   nor V_del".
2. Say whether the pairwise path check keeps its endpoints as V_ep, V_str and V_del
   together (as now), with only the count taken over the non-task ones.

## After the decision

A small PR changes `check_well_formedness` to count `V_ep` minus `V_str` and `V_del`
against m, and updates its tests. The Token Passing planner already parks agents only
on V_ep vertices that are not storage or delivery vertices, so it matches this reading.
Log it in `GAPS.md` and tag the thesis text with `% [Axx]` when the wording is changed.
