# Roadmap to the first result

Written 2026-10-16, after the real centralised and section-based controllers were merged (#161 to #167).
The state and the open decisions are in `SESSION_CONTEXT.md`. This file is the order of work.

The first result means the four learned arms compared on one warehouse under fixed storage. Throughput,
backlog, service time and its parts, crowding, and runtime `kappa_T`, each on paired evaluation seeds. It
answers the controller half of RQ2. The coupling half (RQ1, and RQ2's "effect of coupling") needs adaptive
storage and the demand model, which is Milestone 2.

## Decisions taken on 2026-10-16

| decision | choice | consequence |
|---|---|---|
| centralised arm | keep C-B as built | it sees occupancy and earlier claims, not other agents' targets. One `[A32]` sentence says so |
| messages (RQ5) | embed-once now (#160) | a code track next to the training, see Track B |
| instance for the first result | 8 agents, 94 vertices, 9 aisles | one decision covers 8, about 3 (3 zones) or 1 agent |
| load | 0.3 | an overload. Token Passing finishes 0.26 to 0.27 there, so results are throughput and backlog, not keep-up |
| overnight run | 4 arms x 2 training seeds (0 and 1000), 500 000 timesteps | about 9 to 10 hours, see Milestone 0 |
| evaluation tool | local script in `~/thesis_runs/night_2026-10-16/` | a repo version follows in Milestone 1 |
| Token Passing | not run | the arms are compared with each other only |
| commons question | reinstate as an explicit research question | thesis wording below, needs approval |

## Milestone 0. Tonight

```
nohup systemd-inhibit --what=sleep:idle bash ~/thesis_runs/night_2026-10-16/run_night.sh > ~/thesis_runs/night_2026-10-16/night.log 2>&1 &
```

- Trains decentralised, centralised, section and full_view on seed 0, then again on seed 1000.
- Each run is evaluated right after it trains. Every checkpoint (one per 10 iterations) plays validation
  seeds 20 and 21, the one with the most completed tasks is chosen, and the chosen and the last checkpoint
  play test seeds 5 to 10. Actions are sampled.
- Code is a detached worktree of `main` at 97b6c39 in `~/thesis_runs/night_2026-10-16/code`, so edits to the
  normal checkout do not affect the night.
- Progress in `STATUS.md`, results in `eval/summary.md`, raw rows in `eval/test.jsonl` and
  `eval/validation.jsonl`. Started again, finished runs are skipped.
- Do not start other training while it runs. It uses the GPU and 7 runners.

## Milestone 1. Read the night, then fix what it shows (about one week)

1. **Read the results.** Per arm, mean and spread over the 2 seeds and 6 test seeds. Check that a centralised
   agent is never overridden (`return_override` is 0 in its training log) and that runtime grows with the
   number of agents one decision covers.
2. **Greedy diagnostic.** Evaluate the chosen checkpoints greedily too (rebase `diag/greedy-evaluation` on
   `main` first). It shows whether the centralised arm still stalls, now as wait-wait.
3. **Decide whether 0.3 stays.** If every arm saturates at the same throughput, the load hides the differences.
   Then add 0.2, where Token Passing still keeps up.
4. **Repo work, small PRs from `main`.**
   - Evaluation reads the instance from the run's spec, so 04b and 05 work on any warehouse (replaces the
     local script).
   - Checkpoint selection by completed tasks on validation seeds, with the validation seeds in the seed
     split. Today `--seed` moves the training seeds and the evaluation seeds together, so two training seeds
     are evaluated on different seeds unless the evaluation seeds are given explicitly.
   - The 8-agent warehouse as a shipped config set (`configs/medium/*.yaml`).
   - `run_campaign.py` learns the full-view arm and the config files.
   - Close #83, #81, #82, #86 and #23, and update `THESIS_MAP.md`.
5. **Thesis, each edit approved first.**
   - `sec:impl:instances` and `tab:evalparams`. The 8-agent warehouse as the main instance, load 0.3.
   - `tab:trainparams`. Budget 500 000 timesteps, seed counts, checkpoint selection on validation seeds.
   - The sentence that reported results are sampled and greedy is a diagnostic.
   - The commons research question, see below.
   - Each as a `% [Axx]` tag and a `GAPS.md` entry.

## Milestone 2. The coupling result (RQ1 and RQ2)

1. **Demand model** (`thesis-progress/decisions/decision_log.md` #1). Uniform demand gives adaptive storage nothing to follow, so
   this decides whether RQ1 has an answer. Options are a fixed skew (Zipf) or a skew that drifts.
2. **Adaptive storage** through the learned arms, `thesis-progress/decisions/done/adaptive_storage_plan.md`. Fill
   the storage TBDs (`Delta`, `nu`, `beta`).
3. **Matched training regime**, then the gain of adaptive over fixed storage per arm on paired seeds
   (`eq:rqformal`). That is the first full RQ1 and RQ2 result.
4. Training seeds, at least 3 per condition.

## Milestone 3. Scale, commons and communication (RQ4, the commons question, RQ5)

- Fleet sweep, for example 4, 8, 12 and 16 agents (the 12- and 16-agent warehouses were generated on
  2026-10-16, 178 and 221 vertices). This answers RQ4 and the commons question together.
- Decentralised arm with communication, once Track B has landed.
- Conflict signals and memory for the decentralised arm, only if the greedy diagnostic still shows stalls.

## Track B. Embed-once (#160), in parallel with Milestone 1

Design in `thesis-progress/decisions/active/embed_once_design.md`, steps in `simplification_plan.md` section 1.
It matters now because with 8 agents a robot hears up to 7 senders, and every sender's window is copied into
the receiver's row, so a communication row is about 8 times a plain row.

1. The probe. A `Learner` subclass through `config.learners(learner_class=...)`, and `row_key` surviving
   the learner connectors. No commit.
2. One branch. Row keys in the adapter (keep the turn logic of #164), the two part encoder with an equality
   test against the old path, the two pass value, the block iterator and its learner, then removing the
   sender windows.
3. Open in the issue. Whether the decentralised arm without communication also uses the block iterator.
   Recommended yes, so the comparison with and without messages differs only in the messages.

Communication does not run with more than one turn, so this touches the decentralised arm only.

## Proposed commons research question (not in the thesis yet)

Wording for approval, as an `[A33]` change:

> RQ6: As the fleet grows, does each agent complete fewer tasks, and does this loss grow faster when one
> decision covers fewer agents?

Measured by throughput per agent, `Lambda_T / m`, against `m`, per controller, on the fleet sweep of
Milestone 3. Crowding and blocked time show where the loss comes from. It reuses RQ4's runs, so it adds no
training.

## Questions from `thoughts.md`, answered

- **Must every arm keep up?** Keep-up is reported per arm. At 0.3 on the 8-agent warehouse even Token
  Passing builds a backlog, so the first result compares throughput and backlog. A load where every arm keeps
  up (about 0.2) is the follow-up in Milestone 1, step 3.
- **Which numbers decide which run is best?** Fixed goals, in order. Throughput `Lambda_T` first, then service
  time and its parts (wait for an agent, travel, blocked), then crowding, then runtime `kappa_T`. Always on
  the same evaluation seeds for every arm.
- **Is `episode_return_mean` the right measure?** No. It is RLlib's moving average of the reward return over
  recent training episodes (default window 100), not tasks completed. In the timing run the shaping term was
  468 of a return of 477, against 179 for deliveries. So the night evaluation chooses checkpoints by completed
  tasks on validation seeds, and Milestone 1 moves that rule into the repo and the thesis.
- **Should the arms pick their own tasks, as Token Passing does?** Today all learned arms share one assignment
  rule (`eq:assignmentrule`), so RQ2 compares routing only. Recommended to keep. Token Passing's own task
  choice is one reason it is a reference and not a fourth arm.
- **Action mask against the override penalty.** The action mask removes moves that are illegal for one agent
  alone, such as a slot with no edge. Two agents can still choose legal moves that clash (same vertex or a
  swap) because they choose at the same time. Conflict resolution then overrides one of them, and the override
  penalty is what the policy learns from. The centralised arm's claim mask removes those clashes before they
  are chosen, so its override penalty is always 0.
- **Is the GNN encoder the graph?** No. `local_subgraph_encoding.py` cuts each agent's window out of the graph
  and turns it into tensors. `gnn_encoder.py` is the network that embeds those tensors. One builds the input,
  the other learns from it.
- **The two heads.** `base_model.py` has a policy head (scores for each move and wait) and a value head (how
  good the situation is, for PPO's advantage). There is no graph head.
- **How the planners are built.** `planners/` holds the non-learned routers (Token Passing, prioritised A*).
  They drive the same simulator core through `planners/driver.py`, while the learned arms go through the
  RLlib adapter.
