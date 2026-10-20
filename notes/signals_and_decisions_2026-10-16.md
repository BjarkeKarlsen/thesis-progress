# Conflict signals, and the decisions that need to be made, 2026-10-16

**Status, later on 2026-10-16. Narrowed by `[A32]`.** Sections 1 to 5 measure the arms as they were before the real
centralised and section-based controllers (`real_centralised_design.md`). Those checkpoints no longer load on `main`,
since #162 grew the vertex features from 6 to 7 entries. A centralised agent is never overridden, and its rank is
implied by when it chooses, so the deadlock questions of 6B now concern the decentralised arm, the full-view setting
and clashes across zone edges only. Updates are marked "Update [A32]" below. The current decision queue is in
`SESSION_CONTEXT.md` at the workspace root.

Local note at the workspace root. It continues `updates_dones/campaign_findings_2026-10-16.md` (sections 1 to 12 there:
the 0.21 ceiling, the greedy diagnostic, the leg split). Plans in their own files at this level are
`trace_extension_plan.md`, `memory_reduction_plan.md` and `recurrent_policy_plan.md`.

Everything here is measured or labelled as a guess. All results have one trained checkpoint per condition, 6 evaluation
seeds (5 to 10), one instance, 3 agents, horizon 630.

## 1. What the findings so far say, in short

- The learned fleets stop at about 0.21 tasks per step at any load, and the three arms stop at the same place. Token
  Passing reaches 0.267 at 0.3.
- A task costs a learned agent about 4 steps more than Token Passing. About 2.4 to 2.9 are detour and 1.2 to 1.5 are
  overridden steps. The needed route (9.4 to 9.5) equals Token Passing's travel.
- Under greedy evaluation every arm deadlocks in head-on stand-offs (throughput 0.011 to 0.057, 0 of 60 runs keep up).
  Sampling is what gets the fleet out. The policies have no memory, and conflict resolution blocks both agents.
- The communication arm learned to wait (17% of steps). Under greedy it freezes with agents standing still on 91 to 97%
  of steps.

## 2. Conflict signals, what was built

Branch `feat/conflict-signals`, commit 3010147. Local only. Built by a subagent, checked by me (119 tests rerun, branch and
commit inspected). Not a pull request yet.

An optional switch, off by default, that adds two of the agent's own signals to the end of the readout in every arm.
- `overridden_last_step`. True only if conflict resolution actually overrode the agent at the step that just ended. An
  agent that chose wait is not flagged.
- `priority_rank`. The agent's own rank in the per-episode priority order, 0 the highest, encoded as rank over (m minus 1).
  The encoding is illustrative and a raw option exists.
- The switch is stored in the encoder config, so it is saved with the checkpoint. Examples 04b and 05 read it from the
  loaded module. Old checkpoints load as off.
- Reward, conflict resolution and the step are not changed. 38 new tests. A 2 iteration smoke run only. Nothing was trained
  long enough to say anything about the deadlock.

## 3. A weakness in that design

With 3 agents the agent's own rank is not enough. An agent of rank 1 should yield to rank 0 and go ahead of rank 2, and it
cannot tell which one it faces. Ranks 1 and 2 would both read "I am not the top rank" and yield, a wait-wait deadlock.

Proposed fix, not built. Make the rank a feature of each occupied vertex in the field of view, the rank of the agent
standing there, and optionally its override flag. The own vertex then gives the own rank. All arms already see occupancy,
so the arms still differ only in window. The thesis has to state that the rank of agents within the field of view is
visible.

## 4. Ideas that were considered and set aside

- **Put the signal in the communication message.** Messages exist only in the decentralised arm with communication. The
  other arms would not get it, and the RQ5 ablation would mix with the deadlock fix. A message is the sender's own
  final-layer embedding (`[A27]`, no message head), so a signal can only travel if it is already an encoder input. With the
  signals as inputs the communication arm hears them anyway.
- **An internal message for all arms.** If it means the agent's own signals as input, that is what the switch is. If it
  means a real exchange between agents in every arm, it reopens the communication scope decision.
- **A reward for not being overridden.** A bonus for not being overridden is a larger override penalty plus a constant per
  step, and with a fixed horizon a constant changes nothing. The stand-off already costs minus 1.0 per step for the pair,
  so the incentive is not missing. The policy lacks a deterministic way out. The communication arm shows the trade. It
  leaned toward waiting and froze under greedy evaluation. Reward moves a fleet from push-push to wait-wait. A higher
  penalty could still cut overrides in general (1.2 to 1.5 steps per task), but that is separate tuning, and a reward
  change needs the thesis and plan mode first.

## 5. The experiment, ready to run

```
bash ~/thesis_runs/signals_2026-10-16/run_signals_experiment.sh
```

It trains the decentralised arm with the signals at load 0.25 with the campaign's settings (500 000 steps, 7 runners,
horizon 630, GPU, about 20 minutes). It then compares that checkpoint with the campaign's checkpoint without the signals on
seeds 5 to 10, sampled and greedy. The table goes to `~/thesis_runs/signals_2026-10-16/check/signals_check.md`. Columns are
throughput, keep-up, stalled episodes, swap steps per episode, service time of completed tasks and the leg split.

It runs on a local branch `exp/signals-greedy` in `slap-mapd-coupling/.claude/worktrees/exp-signals-greedy`. That branch
merges the signals, greedy and leg-tool branches with no conflict (82 tests passed). It is not for a pull request. The
comparison step was smoke tested on the old checkpoint and an untrained signals checkpoint. The training step has not been
run.

How to read it. The control row (no signals) has sampled throughput 0.207 with 5 of 6 seeds keeping up, and greedy
throughput 0.057 with 0 of 6. The signals help if greedy comes close to sampled and the stalled count drops, while sampled
does not get worse. No numeric threshold has been set.

Limits. One checkpoint per row, one load, one arm. It tests the own rank scalar as built, which is probably too weak with 3
agents, so a negative result would not rule out the per vertex version. A positive result from one training seed would still
need confirming on more seeds.

## 6. Decisions that need to be made

Items marked "thesis" change the model or the evaluation. Wording is proposed in chat first and logged as `[Axx]` in
`thesis-progress/decisions/GAPS.md`. Nothing here has been edited in the thesis.

### A. Already decided
- PPO policies are evaluated sampled. Greedy is a diagnostic only. Only the planner is deterministic by nature.
- Memory work starts with the chunk size and the smaller integer types. The lookup by vertex stays a later option.
- Option 3 (memory) is written up in `recurrent_policy_plan.md` and comes after the signals.

### B. About the deadlock (the main open question)

Update [A32]. First run the greedy diagnostic on the new arms after the first retrain. Inside a centralised decision a
stand-off can only be wait-wait, not an override, and the later agent sees the earlier agent's choice, so it has what it
needs to step aside. Items 1 to 6 then apply to the decentralised arm, the full-view setting and zone edges.

1. Which route. Change the resolution rule (the higher priority agent passes, the lower yields), add the signals (option 2),
   or add memory (option 3, with the cheaper history input 3b first). Proposed order, each on at least 3 training seeds:
   A today, B the signals, C B plus a history or a recurrent cell. Thesis.
2. If the signals. The agent's own scalar, or the rank per vertex in the field of view (recommended). Whether the
   occupant's override flag is also shown. Thesis.
3. The rank encoding (illustrative rank over m minus 1, or raw) and whether the previous proposed move is a third signal.
4. Whether the signals are a permanent part of the model or a diagnostic ablation. This sets whether it goes into
   `eq:obsfunction` or into the experiments chapter. Thesis.
5. Whether the thesis says that greedy evaluation deadlocks and that the reported results are sampled. One sentence. Thesis.
6. Update [A32]: do not run the experiment as it stands, since its control row is a pre-`[A32]` checkpoint. Rebase
   `feat/conflict-signals` on `main`, then train the control and the signals run together. Original item: whether to
   run the experiment above before or after the per vertex change. Running it now costs about 20 minutes and
   tests a design that is probably too weak. Waiting delays the answer by the time to build the change.

### C. Loads and training length

Update, later on 2026-10-16. The first result moves to an 8-agent warehouse with 94 vertices at load 0.3, an overload
there (Token Passing finishes 0.26 to 0.27). Training is 500 000 timesteps, horizon 630, 2 training seeds (0 and 1000),
run overnight (`~/thesis_runs/night_2026-10-16/`). The checkpoint is chosen by completed tasks on validation seeds 20 and
21 and tested on seeds 5 to 10. Items 7 to 11 below are about the 3-agent instance and stay as history, except where
marked. The order of work is in `thesis-progress/archive/workspace/ROADMAP.md` at the workspace root.
7. Load 0.4. An overload point where nothing keeps up with 3 agents (Token Passing finishes at most about 0.3), reported as
   completion share, throughput and backlog, or a larger fleet so 0.4 keeps up. Thesis (`eq:throughput`, fleet size).
8. Add a load around 0.2 to 0.22, where the learned arms keep up with a heavy queue.
9. Episode length (about 2000 steps), budget (about 2 000 000 steps, about 80 minutes a run) and the evaluation horizon,
   kept equal to the training horizon. All three are TBD in the thesis. Update [A32]: the budget unit is decided, one
   environment step per timestep (#165). The values are not. A centralised timestep now takes m network runs, so the
   wall-clock estimates per run grow with the fleet.
10. Partly decided: 2 seeds for the first result, at least 3 for reported results. How many training seeds (at least 3) and which loads they cover. About 20 minutes per run at 500 000 steps.
11. Checkpoint selection. Save checkpoints every N iterations and choose on validation seeds, or evaluate the last one. The
    communication run ended in a dip. TBD in the thesis. Update: the night run saves one every 10 iterations and chooses
    by completed tasks on validation seeds, because the training return is dominated by the shaping term. Thesis and
    repo still to follow.
12. Whether communication gets the longer budget together with every other arm (recommended, so the one-budget claim holds).
13. The threshold f_up (0.8 so far).

### D. Measurement and tools
14. Implement the trace extension (`trace_extension_plan.md`), one `tasks` line at the end of each trace. It gives release
    time and assignment time per task.
15. Implement the memory change (`memory_reduction_plan.md`, steps a and b). Not limiting today, useful with longer runs.
16. Whether to split travel into needed route and detour in the thesis (`eq:split`). The leg tool already does it. Thesis.
17. A scripted shortest-path controller through the same environment, to separate the policy from the shared assignment and
    resolution rules. Not built. Recommended.
18. An entropy schedule (now constant 0.02) if the deadlock fix leaves a gap between greedy and sampled.
19. Whether `scripts/run_campaign.py` gets options for the signals and for greedy evaluation.

### E. Branches and housekeeping

Update [A32]. All of these are based on `main` before #161 to #165. `feat/conflict-signals` will clash with #162 (the
vertex features went from 6 to 7 entries). `diag/greedy-evaluation` touches `training/policy.py`, which step 6 of
`real_controllers_plan.md` (#166) also changed, so rebase it before opening it.
All local and not pushed. The author opens the pull requests. Each is from `main` and independent of the others. The signals
branch and the greedy branch touch the same lines of example 05, and they merged without conflict on the experiment branch.

| branch | commit | content | state |
|---|---|---|---|
| `feat/campaign-analysis` | 3d08c02 | analysis of a finished campaign, `--analyse` in run_campaign | ready for a PR |
| `diag/greedy-evaluation` | 29f29bb | `greedy` option in `ModulePolicy`, `--greedy` in example 05 | ready for a PR |
| `feat/leg-analysis` | 9db82dc | `evaluation/legs.py`, the split of each task's steps | ready for a PR |
| `feat/conflict-signals` | 3010147 | switchable override flag and own rank | ready for a PR, the design may change |
| `exp/signals-greedy` | local | the three above merged, for the experiment | not for a PR |

20. Which of these to open as pull requests, and in what order.
21. Whether to open the GitHub issue for the thesis gap (the observation has no override flag or priority rank). The repo
    rule is to open an issue for a gap, and the author decides when. Draft text is below.

Draft issue. Title: the thesis observation has no override flag or priority rank, and the learned arms deadlock on head-on
swaps. Body: `sec:pf:observations` defines o_i(t) without any signal from conflict resolution. When two robots want each
other's vertex, both are overridden to wait and see the same observation at the next step. Sampling escapes by chance, and
greedy evaluation deadlocks for hundreds of steps. The code has an optional extension (`feat/conflict-signals`, off by
default). Open points for the thesis. Whether the observation or the readout includes the signals and how to describe them as
the robot's own information, the rank encoding, whether the previous move is exposed, and whether it is permanent or an
ablation.

Draft pull request text for the signals branch. Title: add switchable conflict signals (override flag and priority rank) to
the observation. Summary: an optional extension of o_i(t) (`sec:pf:observations`) and the readout (`sec:method:model`). With
the switch on, each robot of every arm also observes whether conflict resolution overrode its move at the step that just
ended and its own rank in the per-episode priority permutation (`sec:method:resolution`), appended after the congestion
feature. Off is the default and then everything is as before. New interface: `ConflictSignalsConfig` as
`GNNEncoderConfig.conflict_signals`, and `--conflict-signals` and `--priority-rank-encoding` in example 04. 04b and 05 read it
from the loaded module. Gap in the thesis text: no override flag and no priority rank in o_i(t), and the extension is off by
default and the thesis is not edited. Reward, conflict resolution and the step are untouched. Test plan: 17 test files, 464
passed (subagent's run), black and flake8 clean on touched files, `mypy src` shows only the known `evaluator.py` error, a 2
iteration smoke run. Not checked: that the signals remove the deadlock.

### F. Still guesses, not measured
- Update [A32]. Whether the centralised and section-based arms still deadlock under greedy evaluation, as wait-wait
  instead of an override.
- That the signals, in either form, remove the deadlock.
- That the detours are partly the price of escaping stand-offs by chance.
- That a larger budget lifts the 0.21 ceiling.
- That a load near 0.2 to 0.22 is where adaptive storage can be tested.
- Everything about retrained policies. All results have one checkpoint per condition.

## 7. Notes on how this was produced

- The subagent's report was model output. I checked the branch, the commit, the file list and reran 119 tests. I did not rerun
  its full list of 17 test files.
- The findings note was moved to `updates_dones/` while this session ran. This note was written next to the plan files so the
  open decisions stay at the top level.
