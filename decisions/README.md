# Decisions overview

Where every design decision and plan for the thesis lives. The thesis
chapters are the source of truth for the model. These files record why it
looks the way it does. Updated 2026-10-30.

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
| `active/thesis_plan.md` | Main planning document, built from `../archive/notes/thoughts.md` | Live |
| `active/model_revision/` | Model revision of 2026-10-26, steps 01 to 12 (`README.md` has the decisions) | Step 12 on `feat/flow-and-start`, not merged |
| `active/appendix_papers_handoff.md` | Write the appendices as short papers | C and D done, E, G, H and J have placeholders |
| `active/appendix_values_overview.md` | Which run fills each appendix placeholder | In use |
| `active/measures_plan.md` | The measures of a run, grouped | M1 to M4 done, M5 (`[A60]` checkpoint choice) and M6 open |
| `active/scaling_to_1024_agents.md` | Fleet sweep up to 1024 agents | Not started, fleet 128 does not generate |
| `active/cloud/` | Training arms on Kaggle and Colab, with the order of work in `README.md` | Guides written, Kaggle smoke test not run |

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
| `done/embed_once_design.md` | Embed each agent's window once | Done |
| `done/memory_reduction_plan.md` | Where training memory goes | R1 to R4 done |
| `done/simplification_plan.md`, `done/simplification_proposal.tex` | Simplification changes that stay | Embed once done, block iterator question moved to `thesis_plan.md` |
| `done/storage_mode_prompt.md`, `done/storage_mode_wip.patch` | Storage rule as a switch | Done, storage mode is a config switch |
| `done/fix_metric_values.md`, `done/fix_values_from_measures.md` | Keep-up and throughput metrics after `[A49]` to `[A51]` | Done, keep-up split into picks and put-aways (`[A59]`) |
| `done/Appendixes.md`, `done/Appendixes_safe.md`, `done/split_up_appendix_for_better_structure.md` | A test for every number no paper gives, grouped by topic | Agreed and built, `[A57]` |
| `done/appendix_plan.md`, `done/appendix_split_handoff.md` | Appendices as separate documents | Built, appendices A to L |
| `done/graph_appendix_handoff.md`, `done/graph_appenndix.md` | Warehouse graph appendix | Written (D) |
| `done/sweep.md` | Finish the load sweep | Done, main loads in `../notes/queue_findings_2026-10-26.md` |
| `done/handover_queue_analysis.md` | Analyse the queue of 2026-10-23 | Done, in `../notes/queue_findings_2026-10-26.md` |
| `done/run_in_cloud.md` | Cloud training run by an n8n server | Dropped, replaced by `active/cloud/` |

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
| `ideas/learned_storage_policy.md`, `ideas/learned_storage_pilot_plan.md`, `ideas/learned_storage_intro.tex`, `ideas/learned_storage_gcn_size.py` | A PPO storage policy. Pilot stage 1 built, uncommitted in `~/worktrees/pilot-learned-storage` |
| `ideas/recurrent_policy_plan.md` | Recurrent policy (option 3). On hold, decentralised arm only |
| `ideas/trace_extension_plan.md` | Per-task trace (release, assign, finish). Partly built, the trace has `pickup_at` |

## Related folders

- `../notes/how_the_system_works.md` is the plain description of the system.
- `../notes/` has the current notes (measures catalogue, queue findings, parameter sweep, thesis review, how to show a run, windows and embedding), plus `updates_done/` (L4 plans, campaign findings, fix PR log).
- `../archive/notes/` has the out-of-date notes: research goals, status of 2026-10-17, conflict signals and `thoughts.md`.
- `../guides/` has explanatory guides (halo protocol, learning problem, move score head).
- `../archive/temp/` has the early formal drafts and reviews. These are history, not spec.
