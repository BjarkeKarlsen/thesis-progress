# Fix PRs already merged

Moved out of `fix_prs_plan.md` on 2026-10-13, word for word. The plan keeps
only what a later agent still needs and points here for the rest.

| Section below | Merged as | What is still open |
|---|---|---|
| B11, `fix/comparison` | #124 | Its three #103 points are not ticked yet (listed in the plan). |
| L2a and L2b design | #126 and #127 | Nothing. The plan carries forward the points L3 and L4 use. |
| L2a, `fix/sparse-encoder` | #126 | Nothing. |
| L2b, `fix/learned-messages` | #127 | Nothing. The Hand back reports below are the state before the merge. |

Statuses written inside the sections are as of the time they were written.
The merge numbers above are the current state.

---

### B11. `fix/comparison`: "evaluation: interval for every quantity, pair on d_obs, show an undecided keep-up" [review]

- **Thesis to read:** `sec:pf:measures` (every quantity as a mean with a
  95% interval), the gain test, and the window factor in the research
  questions.
- **#103 items closed:** three points (from #80).
- **Files:** `evaluation/comparison.py`, `evaluation/metrics.py`, tests.
- **Changes:**
  1. Add `observation_depth` to `RunMetrics` and to `_MATCHED_FIELDS`.
  2. Report mean and 95% t-interval over seeds for every scored quantity of
     each arm, not only the gain.
  3. `all_keep_up: bool | None`, which is None when any run's `keeps_up` is
     None.
- **Tests:**
  - pairing runs with different d_obs raises an error
  - the interval on a known sample matches scipy
  - an unset f_up gives None

---

### L2a and L2b design (2026-10-12, both merged as #126 and #127)

L2 is split in two. The split and the choices below were agreed in chat on
2026-10-12. Nothing is built yet.

**Decisions taken**

- **Learned messages are the sender's own embedding.** `xi_j = h_{l_j}^(L)`,
  the final-layer embedding at the sender's own vertex, from the sender's own
  field of view with the shared weights. There is no `MSG_theta`. A plain
  linear layer before a mean and another linear layer adds nothing, and
  dropping it removes the "message width" parameter. CRAMP also shares the
  encoder vector as it is (its Figure 2, "Local broadcasting").
- **Option A, not D.** A receiver's training sample carries the padded views of
  its senders, and the network recomputes their embeddings with the current
  weights. This keeps the gradient reaching the sender's embedding, as the
  thesis says, and needs only env-side code. Option D (storing the sender's
  embedding) was rejected. RLlib stores only the env's observation and the
  module's own outputs, so D would need a connector that runs the encoder, a
  way to save the embeddings and a learner connector that looks up the senders
  of the same step. The connector API is alpha.
- **The encoder goes sparse first (L2a).** A multiplies the encoder's work by
  `1 + M`, and today the encoder evaluates `phi` on all `N^2` vertex pairs.
  Edge lists make the cost proportional to the number of edges. L4 needs this
  anyway, for a pass over a whole graph.
- **Fallbacks.** If the cost is still too high, the options are a message with
  its own ReLU layer (small thesis change) or implicit communication, where
  neighbours' intent enters the observation (changes what RQ5 asks, so a thesis
  decision).

**Before either PR starts** (the author, or a session the author asks)

- Reopen #91 (closed on 2026-10-07 with nothing built). Close #89 (the thesis
  now uses cost distance, `[A25]`) and tick its four #103 items.
- Open the L2a issue, linking #91 and #86.
- Thesis edit, applied by the author, logged as `[A27]` in `GAPS.md`:
  `eq:message` becomes `xi_j(t) = h_{l_j(t)}^(L)`. Remove the message-width row
  of `tab:modelparams`. Update the readout and move-score text that mention
  `MSG_theta`, and the sentence "a fully connected layer over the sender's own
  final-layer embedding". The "trained end to end" sentence stays true.
- Drift to fix on the way: `observation.py` still says the thesis uses hop
  distance. It no longer does.

### L2a. `fix/sparse-encoder`: "models: message passing over edge lists, not a dense pair tensor" [review]

- **Thesis to read:** `sec:method:model` (the message-passing step) and
  `sec:pf:env` (the field of view). The maths do not change, so no thesis
  edit is needed.
- **#103 items closed:** none. Groundwork for L2b and L4.
- **Files:** `models/gnn_encoder.py`, `models/local_subgraph_encoding.py`,
  `models/base_model.py`, `models/rl_module.py`, `training/env.py`,
  `controllers/decentralised.py`, the examples that build an encoding config,
  tests.
- **Changes:**
  1. Replace `adjacency [N, N]` with an undirected edge list
     `edge_index [E_max, 2]` (int64, one row per undirected pair among the
     selected vertices) and `edge_mask [E_max]`. `E_max = N * d_max`, derived
     from `max_out_degree(graph)`, so it is not a new cap.
  2. `forward_padded` flattens the batch, builds both directions of every edge,
     computes `phi_r(h_v, h_w)` per directed edge, adds up per vertex with
     `index_add_` and divides by the masked degree (minimum 1). Padded edges
     contribute nothing. No new dependency.
  3. `encoded_observation_space` takes `d_max` as well, since the edge list's
     size depends on it.
  4. Keep the unbatched `forward` as the oracle.
  5. Shorten the docstrings these files carry.
- **Tests:**
  - the sparse path equals the old dense path to float tolerance on random
    graphs (keep the dense formula in the test as the reference)
  - padding vertices and padding edges do not change `z_i`
  - a vertex with no neighbours, and `L = 0`, behave as before
  - the padded path equals the unbatched `forward`
  - an edge present in only one direction still counts for both endpoints
  - the observation space matches the arrays
- **Depends on:** nothing.
- **Hand back:** the commands in "Checks before pushing", plus the command that
  shows the equivalence test failing if the degree division is removed.

L2a is built and committed in the worktree, but nothing has been run against the project's tests. The subagent ran only its own scratch scripts, plus a syntax compile of the changed files.

- Worktree: /tmp/claude-1000/-home-bjarkek-Documents-thesis/ff2e2bf1-85d1-4720-bc45-059101cd9ab6/scratchpad/l2a
- Branch and commit: fix/sparse-encoder, commit e9182df, on top of origin/main at f81f487 (PR #124).
- Size: 11 files, 503 insertions and 238 deletions. Six source files and five test files. The commit message ends with the Co-Authored-By line from the plan.
- Not pushed. I confirmed the commit, the diff stat and the key code lines in the worktree myself.

What the scratch scripts showed

- The new edge-list encoder matches a copy of the old dense formula within 6e-8, for 1, 2 and 3 rounds, with padded vertices and padded edges.
- With the degree division removed, the difference grew to 1.6, so the equivalence test does catch that mistake.
- The padded path matched the unbatched forward exactly on a real encoded observation.
- Every observation from the training env stayed inside its observation space, for three vertex counts and with one-way edges. edge_index is int64, and the edge list never overflowed.
- The RLlib action-masking module built with the int64 array inside the Dict observation, and forward_inference ran on a real env observation.

What is not verified

- The new test functions. Nobody has run them yet.
- Black, flake8 and mypy. The code was formatted by hand.
- The learner path. forward_train and RLlib's batching were not exercised. The subagent's attempt failed with a KeyError because it passed a batch shape the module doesn't expect, so I'd call that a mistake in its scratch call. Your pytest run is where the int64 batching gets tested for real.

Differences from the spec

- d_max is derived inside encode_observation as len(mask) - 1, since a mask has d_max + 1 entries, so its signature and callers stay the same. encoded_observation_space does take d_max, as specified. I checked the line, and it is max_edges(config, len(mask) - 1). Do you prefer passing d_max explicitly?
- One new helper, max_edges(config, d_max), which returns N × d_max. It is not a config field.
- No self-loop code. WarehouseGraph already rejects self-loops and duplicate directed edges.
- Edges touching a padded vertex are also masked by node_mask, as the dense formula did, and a test covers it.
- Examples needed no change. The docstring clean-up in the controller and rl_module.py is partial, and the rest belongs to L2b.

### L2b. `fix/learned-messages`: "models: the learned message, all agents in one forward pass" [review]

- **Thesis to read:** `sec:pf:observations`, `sec:method:model`, `app:notation`.
  If `eq:message` still contains `MSG_theta`, stop and report. The `[A27]` edit
  has not been applied.
- **#103 items closed:**
  - the observation item "`Observation` carries `messages` as hand-picked pairs" (from #63)
  - the hand-built width-2 message (from #64)
  - the "o_i(t) carries messages" comment drift (from #64)
  - the two L=0 docstring items (from #64 and #69)
  - the padded message tensor (from #66)
  - the `base_model` naming item (from #66)
  - the one-pass-per-agent item (from #67, its per-edge half is L3)
  - the inference-per-agent item (from #69)
  - Not closed: the padding-caps gap (from #66, needs a thesis decision).
  - Closes #91.
- **Files:** `environment/observation.py`, `models/local_subgraph_encoding.py`,
  `models/gnn_encoder.py`, `models/base_model.py`, `models/rl_module.py`,
  `controllers/decentralised.py`, `training/env.py`, `training/config.py`,
  the examples, tests.
- **Changes:**
  1. Delete `Message` and `Observation.messages`. `build_observation` no longer
     reads `config.communication`. `communication_neighbours` stays, ordered
     closest first with ties by agent id. Remove the two stale hop-distance
     sentences.
  2. `EncodedObservation` drops `message_features` and `message_mask`. It gains
     `sender_node_features [M, N, F]`, `sender_node_mask [M, N]`,
     `sender_edge_index [M, E_max, 2]`, `sender_edge_mask [M, E_max]`,
     `sender_own_index [M]` and `sender_mask [M]`. With communication off these
     keys are absent from the arrays and from the observation space. The cap
     `max_messages` stays as it is (gap, from #66).
  3. One helper encodes a graph view and is used for the robot itself and for
     each sender. One function builds every robot's `EncodedObservation` for a
     timestep, with its senders. The controller and the training env both call
     it, and L4's env will too.
  4. `GNNEncoderConfig` gets `communication: bool` with no default. `z_i` is
     `h_i || mean_j(h_j) || delta_i`, or `h_i || delta_i` when communication is
     off. The mean is over the masked senders and is zero when there are none.
     `MESSAGE_FEATURE_DIM` is removed. A message has the width of the encoder's
     own embedding, so there is no new parameter.
  5. `DecentralisedController.route` builds all encoded observations, makes one
     batched module call, and samples each action with the same per
     `(seed, t, agent)` stream as now.
  6. `build_ppo_config` checks that `ExperimentConfig.communication` equals
     `GNNEncoderConfig.communication`.
  7. Fix the "o_i(t) to logits" docstring and the L=0 docstrings (communication
     has its own switch). Cite equations by name, such as "the message" and "the
     readout". Also replace the six `eq:mask` mentions already on `main` with
     "the action mask" (`training/env.py:21`, `tests/unit/test_base_model.py:67`,
     `controllers/decentralised.py:66, 69, 168, 175`), since this PR rewrites those
     docstrings anyway.
  8. L2a left the encoder with a `d_max` it derives as `len(mask) - 1` inside
     `encode_observation`. The one function of change 3 should take `d_max`
     explicitly from `max_out_degree(graph)`, which it already has.
- **Tests:**
  - `o_i(t)` is identical with communication on and off
  - a sender's block equals that robot's own encoding
  - sender order and the closest-first cap are deterministic
  - a message depends only on its sender, and padded senders and sender order
    do not change `z_i`
  - the padded path equals the unbatched path
  - a loss on `z_i` gives a gradient to the encoder through the sender path
    (the end to end claim)
  - `z_i` has the right width with communication off, and at `L = 0` with
    communication on the messages are the senders' raw features
  - `build_ppo_config` rejects a mismatch of the two `communication` settings
  - one module call per `route()`, and actions equal to per-agent calls
  - replay is bit for bit with communication on (correctness check 4)
- **Depends on:** L2a, B2 (merged) and the `[A27]` thesis edit.
- **Note for L3:** L3's move score reads the message of the robot on the vertex
  a move leads to. L3 adds the slot index it needs. The layout here leaves room
  for one more array.
- **Hand back:** the commands in "Checks before pushing", plus the command that
  shows the gradient test failing when the senders' embeddings are detached.


L2b is built and committed in the worktree, but none of the new or changed tests have been run. The subagent ran only scratch scripts. I confirmed the commit, the diff size, the missing leftovers and the function signature myself.

- Worktree: /tmp/claude-1000/-home-bjarkek-Documents-thesis/ff2e2bf1-85d1-4720-bc45-059101cd9ab6/scratchpad/l2b
- Branch and commit: fix/learned-messages, commit 737b39f, on top of origin/main at 630a927 (the L2a merge).
- Size: 18 files, 1,524 insertions and 795 deletions. The tree is clean and nothing is pushed.
- Checked by me: the commit adds no eq: labels. No message_features, message_mask, MESSAGE_FEATURE_DIM, Message( or MSG_theta remains in src, tests or examples.

What the scratch scripts showed

- Sparse path: it still matches the dense formula within 3e-8, with and without senders.
- Gradient: a loss on the message part of z alone reaches every encoder weight. With the sender embeddings detached it reaches none.
- One module call: route() makes one forward_inference call per timestep. Its actions equal per-agent calls with the same sampling seeds.
- Observation spaces: real env observations stay inside their spaces, with communication on and off.
- Replay: the realised trace replays identically with communication on.
- PPO: one small training iteration ran through build_ppo_config, with communication on and again with it off. That exercises the learner path with the new Dict keys, which L2a left untested.

Not verified

- The tests themselves. None of the new or changed tests has been run. The subagent only re-stated their properties in scratch scripts. One risk it named is the strict == between routed and per-agent actions, which could only fail on a float tie at a sampling boundary.
- Formatting and typing. Black, flake8 (including unused imports) and mypy were not run. The code was hand-formatted.

Decisions to know about

- encode_all_observations(graph, fleet, tasks, t, experiment_config, encoding_config, d_max) is in models/local_subgraph_encoding.py. d_max is required and explicit. The controller and the training env both call it, and L4 will too.
- Other helpers: encode_view (the shared graph-view encoder) and encode_observation(..., d_max, config, sender_views=None), where None means communication is off.
- max_messages == 0 with communication on raises a ValueError from check_communication_caps. It is called from four places. The cap itself keeps its meaning, so the padding-caps gap stays open.
- The controller doesn't check that the module's communication matches its experiment_config. A mismatch would raise a KeyError or silently ignore keys. build_ppo_config does check it. A one-line check in DecentralisedController.__init__ would be cheap if you want it.
- Old checkpoints break. Checkpoints saved before this PR lack communication in their encoder config and fail at load. This matters for example 04b_evaluate_checkpoint.py. It should go in the PR description, and the subagent's draft already notes it.
- Docstrings: the six eq:mask mentions I asked for are replaced, plus two more in training/config.py.

### B16. `fix/training-progress-metrics`: "training: report progress every iteration" [review]

**Merged as #129 on 2026-10-13**, built as specified. The callback, the metric
names and the print line are in `training/callbacks.py`. The spec follows.

- **Why.** Training prints `None` or `nan` on most iterations, and the two
  numbers it does print say nothing about the stall.
- **Thesis to read:** none. Do not change `train_batch_size`, the horizon or
  any hyperparameter. They are undecided and a larger batch would change
  training.
- **Files:** `training/callbacks.py`, the print loop in
  `examples/04_decentralised_training.py`, new
  `tests/unit/test_training_progress.py`.
- **Changes:**
  1. A pure function `progress_metrics(env: WarehouseMAPDEnv) -> dict[str,
     float]` giving `tasks_completed`, `tasks_released`, `backlog`,
     `steps_since_last_completion` (t minus the latest finish time, or t if
     none) and `episode_step`.
  2. A class `TrainingProgressCallbacks(CorrectnessInvariantCallbacks)`, a
     subclass so one class is passed to `.callbacks()` and no list is needed.
     It counts, in `on_episode_step`, the agent-steps where an agent did not
     change vertex. In `on_sample_end` it logs the values from change 1 for
     the episode in progress, taken from `env_runner.env`, plus
     `standing_still_fraction` over the fragment, with
     `metrics_logger.log_value(name, value, reduce="mean")`, then resets the
     counters. In `on_episode_end` it logs `episode_tasks_completed` and
     `episode_last_completion_t`. Check in a short run that the keys appear
     in `result["env_runners"]`. If `env_runner.env` does not reach the
     environment, stop and report.
  3. A function `format_iteration(i, n, result) -> str` used by the print
     loop. It prints the always-present values, and prints the episode return
     only when it is a finite number, otherwise `no episode ended`.
  4. Example 04 uses `TrainingProgressCallbacks` and `format_iteration`.
- **Tests:** `progress_metrics` on a hand-built environment after a few steps,
  `format_iteration` with `None`, `nan`, a missing key and a normal value, and
  the counter logic of the standing-still fraction without RLlib. If an
  existing test already runs one PPO iteration, assert the new keys there.
- **For L4:** the single `MultiAgentEnv` must keep these callbacks working.

### B15. `fix/episode-trace`: "evaluation: write a per-step episode trace" [simple]

**Merged as #130 on 2026-10-13**, built as specified, with the wandering measure and
the dead flags added during the build. `--dead-after` defaults to 50
(`DEFAULT_DEAD_AFTER`). The agent did not run the tests. The spec follows.

- **Why.** An episode ends in a few numbers. When one looks wrong, a per-step
  record of what every agent did is what shows why.
- **Thesis to read:** `sec:impl:logging` (what is logged, the blocked bit and
  the override flag) and `sec:method:resolution`. This adds no thesis
  parameter and changes no behaviour.
- **Files:** `environment/multi_agent_env.py`, new `evaluation/trace.py`,
  new `tests/unit/test_trace.py`, and one test in
  `tests/unit/test_multi_agent_env.py`.
- **Changes:**
  1. `WarehouseMAPDEnv` gets two read-only attributes, `last_proposed:
     dict[AgentId, Action]` and `last_overridden: frozenset[AgentId]`. Set
     them in `reset()` (empty) and in `step()` right after
     `resolve_conflicts`. Nothing in the loop reads them.
  2. `EpisodeTraceWriter(path, env)` in `evaluation/trace.py` writes JSON
     Lines. Call `record(env)` after every `env.step()`. First line is a
     header: format number, `config.model_dump(mode="json")`, vertices with
     their roles, edges with cost, and the initial positions. Then one line
     per timestep with `t`, `completed`, `released`, `backlog` and, per
     agent, `at`, `intent` (target vertex or null for wait), `moved`,
     `overridden`, `task`, `phase` (`to_pickup` or `to_delivery`) and `goal`.
     The task is the one the agent served during the step that just ended,
     which is `active_tasks_by_agent(env.tasks, t - 1)`. A pickup at time t
     counts as `to_pickup` for that step.
  3. `load_trace(path)` and `summarise_trace(header, steps, window=None)`
     returning a frozen dataclass: steps, completed, released, backlog,
     completed at 25/50/75/100% of the episode, last completion time, per
     agent (moves, moves in the window, overrides, longest stand still,
     final vertex, task and goal), the agents holding a task that did not
     move in the window ("stuck"), who waits on whom at the last step, and
     the out-neighbours of the stuck agents' vertices. Per agent it also gives
     the share of goal moves in the window that brought it closer to its goal
     (distances from the header's edges) and the distinct vertices visited in
     the window, and it lists the "wandering" agents, those holding a task
     with a share below `min_progress`. A stuck check alone misses an agent
     that moves all the time and gets nowhere (example 04 at 7 iterations:
     0 stuck, about 52% of moves closer, 22 to 24 tasks per 2000 steps).
     `window` defaults to a quarter of the episode and `min_progress` to 0.5.
     Both are display settings for a diagnostic, not study parameters.
     It also gives the longest run of steps with the whole fleet standing
     still while a task was active (a stand-still is a vertex that did not
     change, not a chosen wait, since an override is part of the jam). With
     `--dead-after N` it adds the first step the whole fleet, and the first
     agent holding a task, had stood still for N steps. The command line
     defaults N to 50 (`DEFAULT_DEAD_AFTER`, below 1 is rejected). It is a
     display setting, about 3.5 times the longest healthy stretch measured so
     far (14 steps, one episode of a barely trained policy, so a lower bound).
     3 or 5 would end a healthy sampled run. The study value for B21 stays
     open. It is a flag in the trace, never a stop.
     `format_summary` gives the text.
  4. `python -m slap_mapd_coupling.evaluation.trace FILE [FILE ...]
     [--window N] [--min-progress X]` prints the summary for each file, and
     with more than one file also prints the fraction of episodes with a
     stuck agent and with a wandering agent.
- **Tests:**
  - the header and the line count (header plus one line per step)
  - on a small hand-built instance with a dead-end vertex and two agents
    scripted head-on, `moved`, `intent` and `overridden` are as expected
  - `summarise_trace` on a hand-written trace file flags the stuck agents and
    the waiting pair, with no environment involved
  - the `--dead-after N` flags on hand-written traces, including a still
    fleet with no active task (no flag) and one agent frozen while the
    others move (only the per-agent flag)
  - the same seed gives byte-identical files
  - running with the writer gives the same `RunMetrics` as running without it
- **Not in this PR:** the visual replay. The format is meant to feed one later.


### B15. `fix/episode-trace` (merged as #130)

Merged 2026-10-13, spec in `fix_prs_done.md`. Every run can write a per-step trace
(`evaluation/trace.py`, `EpisodeTraceWriter`), and
`python -m slap_mapd_coupling.evaluation.trace FILE [FILE ...]` summarises it:
completions over time, stuck and wandering agents, the longest whole-fleet still run,
and `--dead-after N` (default 50, a display setting). Next: B17 writes traces from
`run_episode` and example 04.

### B16. `fix/training-progress-metrics` (merged as #129)

Merged 2026-10-13, spec in `fix_prs_done.md`. Every iteration now logs
`tasks_completed`, `tasks_released`, `backlog`, `steps_since_last_completion`,
`episode_step` and `standing_still_fraction` under `result["env_runners"]`, and
`episode_tasks_completed` and `episode_last_completion_t` when an episode ends.
`TrainingProgressCallbacks` replaces `CorrectnessInvariantCallbacks` in example 04.
Pushed straight to `main` on 2026-10-13 (`d159733`): an iteration with no finished
episode prints `episode_return_mean=0`, a real 0 prints `0.0`, and a numpy float32
return counts as a number. L4 must keep them working.

### B17. `fix/trace-in-evaluation`: "evaluation: runs can leave a trace" [simple] (merged as #131)

- **Files:** `evaluation/evaluator.py`, the evaluation loop in
  `examples/04_decentralised_training.py`, tests.
- **Changes:**
  1. `run_episode(..., trace_path: Path | None = None)`. With a path it
     writes the trace. Without one nothing changes.
  2. Example 04's `evaluate` writes `examples/output/traces/04_episode_<k>.jsonl`
     for each episode and prints `format_summary` for it.
- **Tests:** `run_episode` with a trace path returns the same `RunMetrics` as
  without one, and the file has one line per step plus the header.
- **Depends on:** B15 (merged). Do the example half after B14, since both edit
  example 04's evaluation loop. The evaluator half can go first.

### B14b. `fix/example-04b-sync`: "examples: 04b matches 04" [simple] (merged as #131)

- **Why.** 04b says its builders "must match 04 exactly" and no longer do.
  04b has horizon 300, observation depth 3, wait cost 0.5, deliver reward 20
  and an instance with 10 storage and 6 delivery vertices that is not checked
  for well-formedness. 04 has 2000, 5, 2.0, 10 and a different instance.
- **Files:** `examples/04b_evaluate_checkpoint.py`, new test.
- **Changes:** set 04b's `build_instance`, `build_storage` and `build_config`
  to the values in 04 as they are after B14.
- **Tests:** load both files by path and assert the instances, storage and
  configs are equal.
- **Depends on:** B14.

### B18. `fix/token-passing-planner`: "planners: Token Passing as the reference baseline" [design]

Not for hand-off until the author has answered the questions below.

- **Thesis to read:** `2.Introduction.tex` lines 289 to 320 (well-formedness)
  and the "Reference baseline" paragraph in `4.Implementation.tex` (about
  lines 155 to 165). The thesis edit is B19.
- **Algorithm** (Ma et al. 2017). A token holds every agent's committed path.
  An agent that reaches the end of its path asks for the token, one at a time
  in agent id order (a choice the paper leaves open, so flag it).
  1. Available tasks are the released, unassigned ones whose pickup and
     delivery vertices are not the last vertex of any other agent's path.
  2. If there is one, take the one with the smallest distance from the
     agent's vertex to its pickup (ties by task id). Plan a space-time A\*
     path vertex, pickup, delivery against the other agents' paths, where
     each other path is extended by standing at its last vertex for ever. The
     path ends at the delivery vertex.
  3. If there is none and no available task has its delivery vertex at the
     agent's vertex, the path is to stay.
  4. Otherwise the agent goes to the closest free non-task endpoint, planned
     the same way.
  Each tick the planner returns the next step of every committed path.
- **Questions for the author:**
  1. Does Token Passing pick its own tasks, or use the shared assignment?
     Recommendation: its own. The guarantee depends on the task rule. The
     planner then replaces stage 2 of the loop for that run, for example
     through an `assign` method on the router that the loop calls when
     present. The thesis says assignment is shared among the controllers, and
     the baseline is outside them, but it is a thesis edit.
  2. Does `PrioritisedAStarPlanner` stay in the code as a second reference?
     The thesis text names one baseline, Token Passing, for now, so this does
     not hold up the thesis edit (B19).
- **Constraint to check with a test.** Token Passing plans allow an agent to
  enter a vertex in the same step another leaves it. Conflict resolution
  blocks that when the leaving agent has lower priority, because it reserves
  every unprocessed agent's current vertex. The plan must not rely on it, so
  plan with a vertex counted as taken at both the step it is left and the
  step after. The test asserts that conflict resolution never overrides a
  Token Passing plan.
- **Other changes:** the planner is stateful, so `PlannerRouter.reset(seed)`
  must reset the token, and replay must stay bit for bit. Update the
  `Planner` docstring, which says planners are pure functions.
- **Tests:** a hand-built dead-end corridor instance where the old planner
  stalls and this one does not. The example 04 instance (seed 42, horizon
  2000) with no agent stuck by B15's summary, no override and no collision.
  A few generated well-formed instances with the same checks. Replay equality.
- **Depends on:** B15 (merged) for the stuck check.



### L1 status, and L1c to handle later

Decided 2026-10-12, thesis text logged as `[A26]` (`thesis-progress/decisions/GAPS.md`).
The estimates use a tumbling window equal to the storage period, as per step
rates. An update is skipped only when no order was released in the window.

- **L1a** `fix/online-estimator`: `storage/estimation.py` (`OnlineEstimator`)
  and its unit tests. Built, committed locally, checks and push pending.
  Part of #60 and #103, closes nothing.
- **L1b** (config fields, validators, gap issues): probably not needed, because
  the window is the existing storage period and nothing else was left as a
  free parameter. Confirm when L1c is planned.
- **L1c** (not started): wire the estimator into `environment/multi_agent_env.py`.
  - Call `observe` from stage 1 (task releases) and stage 5 (edge traversals
    and blocked edges). Replace the three `{}` in stage 6 with the snapshot.
    Skip the storage update when `snapshot.demand` is None.
  - Run the estimator only when `storage_mode != "fixed"`, so F_fix stays
    byte identical. Reset it with the episode.
  - Add the integration test: with a scripted release schedule, F_dem's
    placement changes when demand shifts and F_fix's does not, and the F_cng
    term is non-zero when an edge is blocked. Add the estimator snapshots to
    the replay trace of correctness check 4. Update the stale comments in
    `multi_agent_env.py`, `storage/base.py` and `docs/storage_rule_integration.md`.
  - Closes #60 and the three #103 points under "Fix PR: storage estimates
    (#60)". Depends on L1a and on decision 4.
  - **Blocked on decision 4**: which edge a wait is charged to. Options are
    the intended edge of an overridden move (observed, but may undercount
    queues behind a standing agent) or every blocked tick charged to the next
    edge on the shortest path to the goal (counts more, needs a goal rule).
    Prototype both on a queue scenario before writing it into the thesis. The
    thesis wording at `2.Introduction.tex` (about line 443), `eq:estimates`
    and the notation row for the waiting estimate still says "attributed to an
    edge" without saying which.
  - Also decide demand skew (#94, decision 1) before reporting any adaptive
    storage result. Under uniform demand F_dem has nothing real to adapt to.
  - B12 (warm-up) should cover the first storage period. B13 should land after
    L1c so that check 2 sees realistic relocations.

### L2a and L2b design (merged as #126 and #127, moved)

The design choices, both specs and the build reports are in `fix_prs_done.md`.
What a later agent still needs from them:

- **Learned messages are the sender's own embedding** (`xi_j = h_j`, no message
  head). A receiver's training sample carries the padded views of its senders,
  and the network recomputes their embeddings with the current weights
  (option A). The reasons, and the rejected option D, are in the archive.
- **One function builds every robot's encoded observation.**
  `encode_all_observations(graph, fleet, tasks, t, experiment_config,
  encoding_config, d_max)` in `models/local_subgraph_encoding.py`, with `d_max`
  required. The controller and the training env call it, and L4's env must too.
  The helpers are `encode_view` and `encode_observation(..., sender_views=None)`,
  where None means communication is off.
- **`max_messages == 0` with communication on** raises a `ValueError`
  (`check_communication_caps`). The cap keeps its meaning, so the padding-caps
  gap stays open (decision 15).
- **`GNNEncoderConfig.communication`** has no default and must equal
  `ExperimentConfig.communication`. `build_ppo_config` checks it.
  `DecentralisedController.__init__` does not, and a one-line check there is
  still open.
- **Old checkpoints break.** The encoder config gained `communication`, and L3
  changes the head again. Example `04b_evaluate_checkpoint.py` needs a retrained
  checkpoint.
- **L4:** the encoder runs over edge lists (L2a), so a pass over a whole graph
  or a zone is sparse.

### L3 design (2026-10-13, built, PR #128 open)

#### What is wrong today

- `PolicyValueHead` (`models/base_model.py:30-47`) is one `Linear(hidden_width,
  num_actions)` over a shared trunk of `z_i`. It cannot tell which neighbour sits
  in which slot, which is exactly what `eq:edgescore` was written to fix.
- `EncodedObservation` says nothing about which vertex a slot leads to, or
  which robot stands there.
- `GNNEncoder._embed_padded` returns only the embedding at the robot's own
  vertex. The embeddings `h_w^(L)` at its neighbours are computed and thrown away.
- `_GNNSharedEncoder` hands RLlib one tensor `z` as both ACTOR and CRITIC, so
  `self.pi` never sees anything else.

#### Decision 14 (decided by the author on 2026-10-13: (a), remove the trunk)

Recommendation: **(a), remove the trunk.** The per-edge head already splits the
policy into `SCORE_theta` (one small network shared by every edge) and
`SCORE^wait_theta(z_i)`. A trunk shared by those two and the value head has no
natural place any more, because the move score reads `z_i || h_w || xibar_w`, not
a trunk output. Three small networks, each reading its own input, match the
thesis as written ("the value head is a fully connected ReLU network over
`z_i`", `4.Implementation.tex:387-389`) and the `tab:modelparams` row "hidden
width: phi_r, psi_r, FC layers". The text needs no edit, but the figure does. `fig:architecture`
(`thesis-progress/scripts/images/architecture.tex`) draws one "fully connected +
ReLU" box between the readout and both heads, which is the trunk. Under (a)
that box goes, and the figure shows the readout feeding the move score, the
wait score and the value. The gap item "the head adds its own trunk" (from #66)
then closes by the code matching the thesis.

Under (b) the trunk would have to stay for the value head and the wait score
only, and the thesis would need a sentence plus a `tab:modelparams` row. It
would also make the policy depend on a trunk that the move score bypasses.

Depth is decision 13 and stays out of this PR. Every network is one
hidden layer of `hidden_width`, as today.

#### Thesis to read

`sec:method:model` (`eq:edgescore`, `eq:readout`, `eq:message`), `sec:pf:env`
(`eq:actions`, `[A15]` slot order, `eq:localsubgraph`), `app:notation`. If
`eq:edgescore` no longer reads `SCORE_theta(z_i || h_w || xibar_w)`, stop and
report.

#### Changes

1. **`EncodedObservation` records the slot targets.** Four new keys in
   `observations` (`models/local_subgraph_encoding.py`):
   - `move_target_index [d_max]` int64, the local index in the padded view of the
     vertex move_k leads to. Slot k is the k-th outgoing neighbour by vertex
     number, so this is `graph.out_neighbours(l_i)` mapped through the view's
     index. Padding slots hold 0.
   - `move_target_mask [d_max]`, 1.0 where the slot exists. It repeats
     `action_mask[1:]` on purpose. The RLModule strips `action_mask` from the batch
     before the network runs, and the head should not depend on it.
   - `move_sender_index [d_max]` int64 and `move_sender_mask [d_max]`. With
     communication on only, like the six sender keys. The index points into the
     `M` sender blocks, at the robot standing on that vertex. The mask is 0 when
     nobody stands there, or when that robot is not among the `max_messages` it
     hears. This is the "slot index" the L2b note reserved room for.

   `encoded_observation_space`, `as_rllib_dict`, `_assemble` and
   `encode_all_observations` follow. The occupant of a vertex comes from
   `fleet.locations()` (one robot per vertex, by the vertex rule). Position in
   the sender list comes from the `heard` list that is already built.
2. **The field of view must contain every move target.** `_select_nodes` keeps
   `l_i` and all of `N+(l_i)` first, then fills the rest by ascending `eta`.
   Two checks raise a `ValueError` and do not truncate silently:
   - `max_local_nodes < d_max + 1`, in `encoded_observation_space`.
   - an out-neighbour outside the field of view (edge cost above `d_obs`), in
     `encode_view`. `eq:localsubgraph` then has no `h_w` to give the head.
3. **The encoder exposes per-vertex embeddings.**
   - `_embed_padded` returns `h^(L)` for every vertex, `[R, N, D]`. Callers gather
     the own vertex.
   - New `GNNEncoder.encode_padded(...) -> EncoderOutput(z, node_embeddings
     [B,N,D], messages [B,M,D] or None)`. `forward_padded` stays and returns
     `.z`, so the readout tests are untouched.
   - The unbatched oracle gets a sibling that returns `h_w` and `xibar_w` for
     each slot, for the equivalence test.
4. **The head scores each move by where it leads** (`models/base_model.py`).
   - `PolicyValueHead` keeps its name and holds three networks, with no trunk
     under (a): `score` (`z_i || h_w || xibar_w` to 1), `score_wait` (`z_i` to 1)
     and `value` (`z_i` to 1). Each is `Linear`, `ReLU`, `Linear` of
     `hidden_width`.
   - Input width of `score` is `z_dim + D`, plus `D` with communication on,
     where `D = encoder.embedding_dim`. With communication off `xibar_w` is
     dropped, as the thesis says.
   - `h_w` is a gather of `node_embeddings` at `move_target_index`. `xibar_w` is
     a gather of `messages` at `move_sender_index`, times `move_sender_mask`, so
     a padded sender's embedding never leaks in.
   - Logits are `cat([wait, scores], -1)`, `[B, d_max + 1]`. Slot k already is
     the k-th neighbour by vertex number, so "placed by vertex number" costs
     nothing more. Slots with `move_target_mask` 0 get a score from padding and
     are removed by the action mask afterwards, so nothing is masked twice.
   - `PolicyValueHeadConfig` loses `num_actions`, because the head no longer has
     a fixed output. `build_ppo_config`'s check (`training/config.py:178`) moves
     to the observation space, where `d_max` is the length of the slot arrays.
5. **RLlib wiring** (`models/rl_module.py`).
   - `_GNNSharedEncoder` returns `ACTOR` as a dict `{"z", "slot_inputs"}` and
     `CRITIC` as `z`. `DefaultPPOTorchRLModule` passes ACTOR straight to `self.pi`
     in `_forward_train` and in the inference paths, and uses only CRITIC for
     the value, so a dict should work. **Spike first** (ten minutes, one PPO
     iteration), and if RLlib objects, pack the slot features into one
     flat tensor and unpack in `_PiHead`.
   - `_PiHead` and `_VfHead` call the head's `policy` and `value` methods.
   - `DecentralisedController._batch` already stacks every key of the
     observation, so the new keys need no change there. A test proves it.
6. **Docstrings.** Update `base_model.py`, `rl_module.py`, `gnn_encoder.py` and
   `local_subgraph_encoding.py` (which still say "one policy output over a
   trunk"). Cite `eq:edgescore` by name, "the move score", not by label, as in
   L2b.

#### #103 items closed

- the per-edge head item (from #66, `base_model.py:57-58, 64-65`, including
  "`EncodedObservation` doesn't record which vertex each slot leads to")
- the per-edge half of the one-pass-per-agent item (from #67)
- the trunk gap (from #66), if (a)

Closes #92. Not closed: the padding-caps gap. Change 2 adds a rule (own vertex
and neighbours are always kept) and two hard errors. That is a flagged choice
that belongs to decision 15, so it goes in the PR description and in #103 as
a note on that gap.

#### Flagged choices for the PR description

- An occupant who is not among the `max_messages` heard senders gives a zero
  `xibar_w`, the same as an empty vertex. The thesis says "if there is one", and
  the cap is decision 15.
- A move whose target is missing from the view is an error, not a zero.
- Old checkpoints break again, because the head's weights change shape.
  Example `04b_evaluate_checkpoint.py` needs a retrained checkpoint.

#### Tests

- the padded logits equal an unbatched oracle that scores each neighbour
  one at a time, with communication on and off, at `L = 0` and `L > 0`
- relabelling slots permutes the logits the same way (the thesis claim that
  vertex numbering does not affect what the policy learns): permute the slot
  arrays, and the move logits permute, the wait logit does not change
- a score depends only on `(z_i, h_w, xibar_w)`. Two slots with equal inputs get
  equal logits
- `xibar_w` is zero for an empty vertex, for a robot not heard, and for a padded
  sender. It equals the sender's own embedding otherwise
- the slot arrays match the graph: `move_target_index` follows increasing vertex
  number, and padding slots are masked
- the observation space matches the arrays, with communication on and off. The
  `move_sender_*` keys are absent with it off
- `max_local_nodes < d_max + 1` raises. A view over the cap still keeps every
  neighbour. A neighbour outside `d_obs` raises
- a loss on one move logit reaches the encoder through `h_w`, and with
  communication on also through the sender path of `xibar_w`
- the value is unchanged by the slot arrays, and its network has no shared
  trunk (under (a))
- one PPO iteration through `build_ppo_config`, communication on and off (the
  learner path with the new keys)
- `route()` makes one module call, and the actions equal per-agent calls
- replay is bit for bit with communication on (correctness check 4)

#### Files

`models/gnn_encoder.py`, `models/base_model.py`, `models/rl_module.py`,
`models/local_subgraph_encoding.py`, `training/config.py`, `training/env.py`
(only if it names the head's `num_actions`), the examples that build
`PolicyValueHeadConfig`, `tests/unit/test_base_model.py`, `test_gnn_encoder.py`,
`test_local_subgraph_encoding.py`, `test_rl_module.py`, `test_training_config.py`,
`test_decentralised_controller.py`.

#### Size and order

One PR, `fix/move-score-head`, branched from `main` after the decision. Commit
in this order, so each step passes alone: (1) slot arrays and the field of view
rule, (2) encoder per-vertex output, (3) the head and the RLlib wiring. Expect
about the size of L2a.

#### Depends on

L2b (merged), B6 (merged, slot order by vertex number), decision 14. L4 reuses
the head: the centralised and section-based arms have no `xibar`, and the head
already drops it when communication is off.

#### The env is RLlib's (the author's requirement, 2026-10-13)

The training env stays a `MultiAgentEnv`, and everything the network needs
arrives through its observation. Today `training/env.py` wraps the plain
`WarehouseMAPDEnv`. L4 is where the two become one (#104), so L3 must not depend
on how that is done.

What this means for L3:

- The slot arrays are built in `encode_all_observations` and leave the env
  inside the `observations` Dict, next to the sender blocks. No connector,
  no side channel, and no lookup of the graph inside the network.
- Every new key has a fixed shape in `encoded_observation_space` (Box or
  Discrete), because RLlib batches on the declared space. This rules out
  "variable number of neighbours" and is one more reason to prefer the fixed
  layout (own vertex at 0, neighbours at 1 to `d_max`) over four extra arrays.
- The controller at evaluation calls the same function and the same module, so
  a trained policy sees exactly what it saw in training.
- A missing neighbour or an unheard sender cannot be a Python exception in the
  middle of an RLlib rollout worker. It has to be decided in advance, as a
  check when the env is built or as a defined zero. This settles the second
  question below in favour of a check at construction, not an error per step.

Direction from the author, 2026-10-13: whatever does not depend directly on a
planner moves into the RLlib env, to cut complexity. My reading is that the
six-stage loop, task release, conflict resolution, storage updates, the
reward and the observation all live in the `MultiAgentEnv`. Only the routing
that is driven by a planner (the reference planner baseline, which does not
learn) stays outside and plugs in through the `actions` the env is given. This
is L4's design (#104) and is not designed yet. L3 does not wait for it, because
its changes sit in the observation and the model, which both layouts share.
One consequence to confirm in L4: ray becomes a hard dependency of the
simulator, where the docstring of `environment/multi_agent_env.py` keeps it out
of baseline runs on purpose.

#### Build decisions (2026-10-13, taken so the build could start)

These settle the open questions above. Each one is cheap to reverse.

- **Decision 14 is (a), decided by the author on 2026-10-13.** No trunk. Under (a) `fig:architecture` in the thesis
  needs its "fully connected + ReLU" box removed. That edit is the author's,
  in `thesis-progress`, and is not part of this PR.
- **The four slot arrays** of change 1, not the fixed layout. The fixed layout
  stays an option for later.
- **A neighbour outside the field of view** is checked when the env is built
  (`check_slot_targets`, called from `WarehouseMAPDMultiAgentEnv.__init__`), so a
  rollout worker never meets it. `encode_view` also raises as a safeguard,
  because `DecentralisedController` has no graph at construction. If the check
  rejects fixtures in many test files, the agent stops and reports. It does not
  loosen the rule.
- **An occupant that is not among the heard senders** gives a zero `xibar_w`.
  Flagged in the PR description.
- **Worktree:** `/tmp/claude-1000/-home-bjarkek-Documents-thesis/3501202a-a049-42fa-bf37-b3216b365202/scratchpad/l3`,
  branch `fix/move-score-head`, from `origin/main` at b3882e8. Committed there,
  not pushed. The author runs the checks and opens the PR.

#### Hand back

The commands in "Checks before pushing", plus the command that shows the
permutation test failing when the slot arrays are shuffled without permuting
the logits, and the one that shows the gradient test failing when `xibar_w` is
detached.

#### Questions for the author

1. Decision 14 is answered, (a).
2. Are the two hard errors in change 2 acceptable, or should an out-of-view
   neighbour be allowed with a zero embedding?


#### Build status (2026-10-13)

L3 is PR #128. The first three commits are pushed. A fourth, `fa864ba`, is local only and
needs a plain `git push`. It drops `move_target_mask` and `check_move_slots`, which gave the
thesis nothing (the head never read the mask, and the check could not fail). I checked it by
compiling and by a scratch smoke run of the env. The tests, black, flake8 and mypy
have not been run by me. I confirmed the commits, the diff size, the missing `eq:` labels and sibling
references, and that both failing-test commands match the code. The agent's scratch scripts did the
rest.

- Worktree: /tmp/claude-1000/-home-bjarkek-Documents-thesis/3501202a-a049-42fa-bf37-b3216b365202/scratchpad/l3
- Branch and commits: `fix/move-score-head` on `origin/main` at b3882e8.
  `d905c77` slot arrays and the field-of-view rule, `760dc0e` encoder per-vertex
  output, `6176ac6` the head and the RLlib wiring.
- Size: 16 files, 1158 insertions, 199 deletions with the fourth commit. About 60% is tests.
- The RLlib spike worked. A dict is accepted as the actor output in exploration,
  train and inference, with the masking module. Two PPO iterations ran in scratch,
  communication on and off.
- Not verified: the new unit tests, and whether any existing fixture fails the new
  field-of-view check. The agent read every fixture and found none, but nothing
  ran. No PPO-iteration unit test was added.
- Differences from the spec: the value network is `value_net`, the head takes
  `(input_dim, embedding_dim, communication, config)`, the sender position comes
  from the sender's own vertex, and `build_ppo_config` now also runs
  `check_slot_targets` and a new `check_move_slots`.
- Still open for the author: the figure edit in `fig:architecture` (decision 14
  was answered (a) on 2026-10-13), a note on the padding-caps gap in #103, and the PR #128 description lines that
  still name the two removed pieces.
