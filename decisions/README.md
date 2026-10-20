# Decisions overview

Where every design decision and plan for the thesis lives. The thesis
chapters are the source of truth for the model. These files record why it
looks the way it does. Updated 2026-10-20.

## How the folder works

- A change to the model gets an `% [Axx]` tag in the chapters and an entry
  in `GAPS.md`.
- A decision still waiting on the author goes in `decision_log.md`.
- A plan or proposal starts in `active/`. Once it is adopted, merged or
  dropped, move it to `done/` and put its status on the first line.
- An idea that is parked, not planned, goes in `ideas/`.

## Logs

| File | What it holds |
|---|---|
| `GAPS.md` | Index of every `[Axx]` tag with its status, the rationale for each tag still in force, and the open items ("every controller arm as a GCN" and later changes). The REVISION 2 `[Gxx]`/`[Kxx]`/`[Mxx]` fixes are in `../archive/temp/GAPS.tex`. |
| `done/GAPS_history.md` | Superseded tags ([A8], [A16], [A21], [A40]) and closed checklist items, moved out of `GAPS.md`. |
| `decision_log.md` | Open thesis decisions from issue #103 and the training budget gap, with options for each. |

## Active

| File | Topic | Status |
|---|---|---|
| `active/appendix_plan.md` | Which sections moved to the separate appendix document | Structure built, D and the warehouse figures to add |
| `active/thesis_plan.md` | Main planning document, built from `../notes/thoughts.md` | Live, 2026-10-19 |
| `active/embed_once_design.md` | Embed each agent's window once, to cut communication cost | Do now (Track B of `thesis-progress/archive/workspace/ROADMAP.md`) |
| `active/memory_reduction_plan.md` | Where training memory goes and what to change | Not implemented |
| `active/trace_extension_plan.md` | Extend the episode trace to find where a task goes wrong | Not implemented |
| `active/simplification_plan.md`, `active/simplification_proposal.tex` | Simplification changes that stay (version 3) | Plan |
| `active/recurrent_policy_plan.md` | Recurrent policy (option 3) | On hold, decentralised arm only |
| `active/storage_mode_prompt.md`, `active/storage_mode_wip.patch` | Make the storage rule a switch in training, evaluation and the campaign | Prompt plus unapplied work in progress |

## Done

| File | Topic | Outcome |
|---|---|---|
| `done/message_design.md` | What a message contains | Option 4, learned embeddings, `[A14]` |
| `done/real_centralised_design.md`, `done/real_controllers_plan.md` | Real centralised and section-based controllers | `[A32]`, merged #161 to #167 |
| `done/adaptive_storage_plan.md`, `done/adaptive_storage_impl_plan.md` | Adaptive storage through the learned controllers | Done |
| `done/scoring_proposal/` (v1 to v3) | A simpler way to score a run | Adopted (v3) |
| `done/stock_template_2026-10-17.md` | Stock as a placement template | Superseded by the arrival model |
| `done/arrival_storage_plan.md` | Storage decided when stock arrives | Adopted 2026-10-18, `[A38]` to `[A40]` |
| `done/order_lines_proposal.md` | Orders with several lines and amounts | `[A46]` |
| `done/code_changes_plan_2026-10-19.md` | Code for `[A43]` to `[A46]` | Merged #178 to #186, step G2 left |
| `done/A47_putaway_draft.md`, `done/putaway_code_plan_2026-10-19.md` | Robots carry the put-away | `[A47]` |

### Measurements behind the decisions

| File | What was measured |
|---|---|
| `done/demand_probe_2026-10-17.md` | Demand model, starting stock and storage rules |
| `done/short_run_2026-10-17.md`, `done/short_run_2026-10-18.md` | Short validation run, partial and finished |
| `done/arrival_probe_2026-10-18.md` | Picks empty the shelves and storage decides at arrival |
| `done/arrival_short_2026-10-18.md` | Short run policies under the arrival stock model |

## Ideas

| File | Topic |
|---|---|
| `ideas/transformer_extension/` | Adding attention (Transformer) components to the learned controllers |
| `ideas/learned_storage_policy.md` | A PPO storage policy coupled with the router, case for and against. Look into after the long run |

## Related folders

- `../notes/how_the_system_works.md` is the plain description of the system.
- `../notes/` has the research goals, status notes, the conflict signals note and `thoughts.md`, plus `updates_done/` (L4 plans, campaign findings, fix PR log).
- `../guides/` has explanatory guides (halo protocol, learning problem, move score head).
- `../archive/temp/` has the early formal drafts and reviews. These are history, not spec.
