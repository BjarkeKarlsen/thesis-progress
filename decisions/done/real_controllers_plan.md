# Plan: real centralised and section-based controllers ([A32])

**Status 2026-10-16. Done.** Every step is merged into `main`, as #161 (step 1), #162 (2), #163 (3), #164 (4), #165
(5), #166 (6) and #167 (7). Left for the author, closing #83, #81, #82, #86 and #23, and updating `THESIS_MAP.md`.
The local branch `diag/greedy-evaluation` changes `training/policy.py`, which step 6 also changed, so rebase it on
`main` before opening it.

One spec per step, ready for an implementing session (Sonnet 5.5). Work
through the steps **in order**, **one per session**, and stop after each one.
The session makes the change in a git worktree and reports the worktree's
path. The author runs the checks, commits, pushes and opens the PR.

Written 2026-10-16 against `slap-mapd-coupling` `main` at `62aa533`, Ray
2.57.0. The design was decided with the author on 2026-10-16. The record is
in `thesis-progress/decisions/done/real_centralised_design.md` (Part 3) and the
`[A32]` entry of `thesis-progress/decisions/GAPS.md`.

---

## Prompt for each run

Paste this, with the step number filled in:

> Read `real_controllers_plan.md` at the workspace root, the section "Rules
> for every run", then implement step N only. When it is done, reply with the
> worktree's path and nothing else.

---

## Rules for every run (read first)

### Setup

1. Read `AGENTS.md` and `CLAUDE.md` at the workspace root, then
   `slap-mapd-coupling/AGENTS.md` and `slap-mapd-coupling/CLAUDE.md`.
2. Read the thesis sections the step names with
   `python3 thesis_section.py <label> ...`, run from the workspace root. The
   `[A32]` text may sit uncommitted in the local working copy of `thesis/`,
   so **don't pull `thesis/`**. Read it as it is. The thesis is the source of
   truth. If the step and the thesis disagree, stop and report it.
3. Work in a new git worktree, never in the author's checkout of
   `slap-mapd-coupling`, which may hold uncommitted work. Don't run
   `git checkout`, `git stash`, `git reset` or `git pull` there. Run:

   ```
   git -C slap-mapd-coupling fetch origin
   git -C slap-mapd-coupling worktree add <scratchpad>/<branch> -b <branch> origin/main
   ```

   Work only inside the worktree, with
   `PYTHONPATH=<worktree>/src PYTHONDONTWRITEBYTECODE=1`.

### Hand-off

- **Leave the changes uncommitted in the worktree.** Don't commit, don't
  push, and don't run pytest, black, flake8 or mypy. The author runs the
  checks, commits, pushes and opens the PR.
- **Don't touch GitHub.** No issues, comments or PRs. The author opens the
  tracking issue (its text is at the end of this file).
- **The final reply is the worktree's path.** Leave the worktree in place. If
  the step stopped early (see Hard limits), add one line saying why.

### Hard limits

- Never edit anything in `thesis/`.
- **Keep the step small.** Stop and report, without coding around it, if
  - the thesis and this plan disagree,
  - step 0's findings contradict what a later step assumes,
  - a step needs a file this plan does not list, or a new design choice,
  - a stored checkpoint or fixture would have to be regenerated.
- **Don't invent values.** A value the thesis leaves open or marks TBD
  becomes a config field with no default and a comment saying so. Don't
  pick a number.

### Writing in code

- **Cite equations by name, never by label.** Write "the claim mask", not
  `eq:claimmask`. The names are in `thesis/styles/eqnames.tex`. Section and
  table labels (`sec:...`, `tab:...`) stay.
- **Symbols follow `thesis/Chapters/2.Notation.tex`.**
- **Shorten docstrings you touch.** Cut long or historical explanation in the
  code a step touches. Don't rewrite files the step doesn't list.
- **UK spelling** (behaviour, organise, colour).
- Write a test that fails without the change, next to the code it tests.

### RLlib: the new API stack only

The repo uses RLlib's new API stack (Ray 2.57), and every step stays on it.
Use `RLModule` and `RLModuleSpec`, the `Learner`, `ConnectorV2` pipelines,
`EnvRunner` and `MultiAgentEpisode`. Size batches with
`train_batch_size_per_learner`. Never use the old stack: no `Policy`,
`ModelV2`/`TorchModelV2`, `SampleBatch` postprocessing,
`postprocess_trajectory`, `RolloutWorker`, or
`.api_stack(enable_rl_module_and_learner=False, ...)`. When RLlib's docs or an
example show both, follow the new-stack version. Step 0's findings
(`scratch/FINDINGS.md` of the spike) describe how the new stack behaves with
turns, with source line references.

Thesis sections for this work (print the ones a step names):

```
python3 thesis_section.py sec:pf:controllers sec:pf:game sec:method:controllers \
    sec:method:rl sec:method:model sec:method:resolution sec:method:training
```

Equation names (`thesis/styles/eqnames.tex`) used below: the centralised
policy, the section-based policy, the vertex features, the action mask, the
claim mask, the credit, the pooled readout, the halo, the reward. Cite them
by name in code, never by label.

---

## What the thesis now says (summary, the chapters win)

- **Centralised.** The agents choose one at a time in the episode priority
  order, the same order conflict resolution uses. Agent `a_i` chooses from
  the global state and the moves of the agents before it (the centralised
  policy, chain rule over agents). One network over all movable vertices, run
  once per agent. A timestep takes `m` runs.
- **Collision rule inside a decision.** An agent may not move onto a vertex an
  earlier agent has chosen, may not swap with an earlier agent, and may not
  move onto a vertex whose agent has not chosen yet. It may follow an earlier
  agent onto the vertex that agent leaves. Waiting is always allowed. So
  conflict resolution never overrides a centralised agent, and the override
  term of the reward is always zero for it.
- **Section-based.** The same inside each zone, on the zone plus halo, for the
  agents standing in the zone. Zones run in parallel and do not see each
  other's choices. An agent treats every occupied halo vertex as an agent
  that has not chosen, so it does not enter it. Two zones may still send
  agents onto the same empty boundary vertex, and conflict resolution removes
  that. With one zone it is the centralised arm.
- **Decentralised.** Unchanged. Every agent chooses independently.
- **Full-view setting.** The decentralised router with every movable vertex
  in view and the pooled readout, each agent choosing alone on its own
  reward. Not a controller in `Π`, run under a few conditions only.
- **Vertex features** gain a fourth entry, whether `v` is in
  `V_{≺i}(t)`, the vertices the earlier agents in the same decision have
  chosen to end the timestep on (including an earlier agent that waits). It
  is always 0 for the decentralised router and the full-view setting.
- **Claim mask** `M^≺_i(t, ·)`, added to the action mask. It switches off a
  move to `w` when `w ∈ V_{≺i}(t)`, when `w` holds an agent that has not
  chosen yet (agents in other zones count as not chosen), or when the earlier
  agent on `w` has chosen to move onto the agent's own vertex. Wait is never
  switched off. Zero for the decentralised router.
- **Pooled readout** stays for the wider routers and the full-view setting.
- **Critic** reads the same `z_i` as the policy, so it sees the claims too.
- **Credit** (the credit). Each agent's choice is one training sample with its
  own value estimate, credited with the mean reward of the agents that chose
  together with it at that timestep: the whole fleet (centralised), the agents
  in the same zone at `t` (section-based), the agent alone (decentralised and
  full-view). The open credit choice of #83 is gone.
- **Budget.** Equal across arms in environment steps, **one step per
  timestep**, however many agents choose within it. Runtime `κ(t)` covers all
  `m` runs of a timestep.

---

## Design in the code

### Turns

`training/env.py`'s adapter becomes turn-based. A timestep is split into
**turns**. In one turn, the adapter returns observations only for the agents
that choose in that turn. RLlib asks the module only for those agents, and
batches them in one forward pass.

| Controller | Turns of one timestep |
|---|---|
| decentralised, full_view | one turn with every agent (today's behaviour) |
| centralised | `m` turns, one agent each, in `core.priority` order |
| section | turn `k` holds the `k`-th agent (in priority order) of every zone that has at least `k` agents. The zones are fixed at the start of the timestep, by the zone of each agent's vertex |

The section form runs the zones in parallel, as the thesis says. A zone with
fewer agents simply has none in the later turns.

Per timestep the adapter keeps `chosen: dict[AgentId, VertexId]`, each
decided agent's successor vertex (its own vertex for a wait), and
`slots: dict[AgentId, int]`. The **unit's earlier choices** for agent `i` are
`chosen` restricted to the agents of `i`'s unit (all of them for centralised,
`i`'s zone for section). That restriction gives `V_{≺i}(t)` (its values) and
the input to the claim mask.

`step(action_dict)`:

1. Check that the keys are exactly the current turn's agents. Otherwise raise.
2. Store each slot, and its successor via `environment/spaces.py::action_for_slot`.
3. If turns remain, return observations for the next turn's agents, an empty
   reward dict, and `{"__all__": False}` for both flags (step 0, Q2). RLlib
   holds each acted agent's action until its next observation and adds the
   rewards that arrive in between to it.
4. After the last turn, call `core.step(slots)` once, apply the credit, set
   `timestep_completed = True`, rebuild the turns for `t+1`, and return
   observations for the first turn of `t+1` with the rewards of **every**
   agent. RLlib raises if an agent acts and gets an observation in the same
   sub-step without a reward (step 0, Q2).
5. If that timestep ends the episode, return an observation for **every**
   agent instead, with `truncateds={"__all__": True}`. RLlib raises for an
   agent that acted and is truncated without a final observation, and marking
   the end as terminated would drop the value bootstrap (step 0, Q5). These
   observations are never sent through the module. They only feed the
   bootstrap. They carry **no claims** (decided 2026-10-16): at the cut-off
   nobody has chosen yet, so the view without claims is the true state at the
   start of timestep `T`, and the value estimates the return before the
   earlier agents choose. Build them with `claimed=()` and the plain
   `legality_mask`, the same for every controller.

On every other sub-step `timestep_completed` is `False`. Callbacks and
evaluation read it.

### Claim mask

`resolution/conflict_resolution.py::_blocked` already is the collision rule,
with `finalised` as the earlier agents and `before_loc` as every agent's
current vertex. An agent missing from `finalised` counts as not having chosen.
So the claim mask is `_blocked` evaluated for each legal move slot, with
`finalised` set to the unit's earlier choices. Making `_blocked` public and
reusing it guarantees that conflict resolution never overrides a centralised
agent, because both apply the same check in the same order.

### Credit

The credit follows the controller. It is no longer a config field. The
existing `team_mean` function and `_groups` stay. The groups are the whole
fleet for centralised and the zone at the start of the step for section.
Decentralised and full_view keep each agent's own reward.

### Not changed

The simulator core's `step(slots)`, conflict resolution itself, the reward,
assignment, storage, the encoder's message passing, the per-edge head, the
pooled readout, communication (decentralised only), Token Passing.

### Interplay with open issues

- #160 (embed each window once per timestep) is decentralised with
  communication only. If it lands first, the turn-based adapter must keep its
  row keys. Communication with more than one turn is rejected anyway.
- #104 (one MultiAgentEnv class) stays independent. This plan keeps the
  adapter and core split.
- Closed or superseded once the steps are merged (the author closes them):
  #83 (credit), #81 (η_i in a shared pass, settled by one pass per agent),
  #82 (pooling, settled), #86 (learned wider arms), #23 (boundary yield,
  superseded).

---

## Steps

**[simple]** means mechanical. **[review]** means behaviour change, checked
against the thesis by an Opus session or the author before the PR is opened.

### Step 0. Spike, RLlib with turns [review]

**Done 2026-10-16.** Questions 1 and 2 hold, so the turn design works. The
results are written into "Design in the code", steps 4 and 5 and the RLlib
rule above. The findings file is `scratch/FINDINGS.md` on the spike worktree
(branch `spike/rllib-turns`), for the author to post on the tracking issue.

No PR. A throwaway script and a findings file in the worktree's `scratch/`
folder (`scratch/turns_spike.py`, `scratch/FINDINGS.md`). The author posts the
findings on the tracking issue.

1. Branch `spike/rllib-turns`.
2. Write a toy `MultiAgentEnv` with 3 agents and `Discrete(2)` actions. One
   "timestep" is 3 sub-steps with one agent each. The env gives a reward only
   on the third sub-step, a known value per agent, for example agent id × t.
   Train PPO on the new API stack for 2 iterations with `num_env_runners=0`,
   then read the sampled episodes.
3. Answer each of these with evidence (printed values, not reasoning):
   1. Does the runner ask the module only for the agents in the returned
      observation dict?
   2. A reward for an agent that has no observation in that step's dict.
      Does RLlib add it to that agent's last action? Compare each agent's
      per-step rewards in the `MultiAgentEpisode` with what the env emitted.
   3. What do `num_env_steps_sampled_lifetime` and
      `num_agent_steps_sampled_lifetime` count with sub-steps?
   4. How do you make one sampling call exactly one episode when the number
      of sub-steps per episode varies (section arm)? Try
      `batch_mode="complete_episodes"`. Report what RLlib requires of
      `rollout_fragment_length`, `train_batch_size_per_learner` and
      `minibatch_size` with it.
   5. At truncation (`"__all__": True`), must every agent receive a final
      observation, or only some?
   6. Does GAE bootstrap each agent from its own next observation?
4. Write the answers to `scratch/FINDINGS.md`, each with the printed evidence
   and the minimal working env. This step may run the spike script itself,
   since it is not one of the repo's checks. If 1 or 2 fails, say so at the
   top of the file. The turn design then does not work, and the author
   decides what next.

### Step 1. The claim mask [simple]

- **Branch** `feat/claim-mask`.
- **Thesis** `sec:pf:controllers` (the collision rule), `sec:method:rl` (the
  claim mask, the action mask), `sec:method:resolution`.
- **Files**
  - `resolution/conflict_resolution.py`. Rename `_blocked` to `move_blocked`,
    public, same logic. Shorten its docstring and say it is also the claim
    mask's rule.
  - `environment/spaces.py`. New
    `claim_mask(graph, agent_id, before_locations, chosen, d_max) -> Mask`,
    with `chosen` the unit's earlier choices. Start from `legality_mask` of
    the agent's vertex. Set every legal move slot whose target
    `move_blocked(...)` rejects to `-inf`. Never touch slot 0 (wait). Raise if
    the wait itself is blocked, since that is a correctness bug.
  - `tests/unit/test_spaces.py` (or a new `test_claim_mask.py`) and
    `tests/unit/test_conflict_resolution.py`.
- **Tests**
  - Each case on a small hand-built graph. A vertex an earlier agent chose is
    blocked. A vertex holding an agent that has not chosen is blocked. A swap
    with an earlier agent is blocked. Following an earlier agent that leaves
    `w` for another vertex is allowed. Wait is always legal.
  - Property test over about 200 seeded random fleets on a generated
    instance. Take the agents in a random priority order, give each one a
    random slot legal under its claim mask, with `chosen` = all earlier
    agents. Then `resolve_conflicts` overrides nobody.
- **Done when** the old conflict-resolution tests pass unchanged.

### Step 2. The claim feature [simple]

- **Branch** `feat/claim-feature`.
- **Thesis** `sec:method:rl` (the vertex features).
- **Files**
  - `environment/observation.py`. `VertexFeatures.claimed: bool`.
    `build_observation(..., claimed: Collection[VertexId] = ())` sets it on
    the visible vertices in `claimed`.
  - `models/gnn_encoder.py`. `NODE_FEATURE_DIM = 7`, the comment, and
    `_node_feature_vector`.
  - `models/local_subgraph_encoding.py`. `encode_view` writes the new column.
  - The tests of these three modules, and any test that hard-codes 6.
- **Note for the author.** Every stored checkpoint stops loading, because the
  input width changes. If a committed fixture or checkpoint test
  (`test_checkpoint_layout.py`) needs regenerating, stop and report (Rules,
  stop conditions).
- **Done when** every caller passes no claims and the observations are
  otherwise identical to `main`.

### Step 3. Credit follows the decision, and the full-view setting [review]

- **Branch** `feat/credit-follows-unit`.
- **Thesis** `sec:method:training` (the credit), `sec:method:controllers`
  (Full-view setting).
- **Files**
  - `core/experiment_config.py`. Add `"full_view"` to `ControllerArchitecture`,
    with a comment that it is the full-view setting, not a controller in `Π`.
    Reject communication with it, as with the wider arms.
  - `training/env.py`. Remove the `credit_signal` argument and the
    `CreditSignal` type. Credit by controller, team mean for centralised and
    section, own reward for decentralised and full_view. `arm_windows` for
    full_view is the centralised windows and pool. `check_arm` follows.
  - `training/arm.py`. `POOLING["full_view"] = "mean"`, `largest_window` for
    full_view is every movable vertex.
  - `training/config.py`. Remove `credit_signal` from `PPOHyperparameters` and
    from the docstrings.
  - `training/spec.py`, `configs/*.yaml`, `evaluation/evaluator.py` (drop
    `credit_signal="per_agent"`), and every example that sets it.
  - `training/callbacks.py`, wording only where it names the credit signal.
  - Tests of each.
- **Done when** a centralised and a section run give each agent its unit's
  mean reward, and decentralised and full_view give each agent its own.

### Step 4. The turn-based adapter [review]

Needs step 0's answers and steps 1 to 3.

- **Branch** `feat/turn-based-adapter`.
- **Thesis** `sec:pf:controllers`, `sec:method:controllers`, `sec:method:rl`,
  `sec:method:model` (per-agent copy paragraph).
- **Files**
  - `environment/multi_agent_env.py`. A read-only `priority` property
    returning `self._priority`. Nothing else.
  - `models/local_subgraph_encoding.py`. `encode_all_observations` gains
    `acting: Optional[Sequence[AgentId]] = None` and
    `chosen: Optional[Mapping[AgentId, Mapping[AgentId, VertexId]]] = None`
    (each acting agent's unit's earlier choices). It encodes only the acting
    agents, passes `claimed=set(chosen[i].values())` to `build_observation`,
    and combines `legality_mask` with `claim_mask` into the action mask.
    Raise if communication is on and `acting` is not every agent.
  - `training/env.py`. The turn logic of "Design in the code". Expose
    `timestep_completed`. Shorten the module docstring and say what a turn is.
  - `training/callbacks.py`. The correctness check and
    `StandingStillCounter.update` run only when `timestep_completed` is true,
    so a sub-step does not count as standing still.
  - `tests/unit/test_training_env.py`, `test_local_subgraph_encoding.py`,
    `test_training_progress.py`.
- **Tests**
  - Decentralised regression. Before changing anything, record on `main` a
    trajectory under a fixed seed with a deterministic slot rule (the first
    legal move, else wait): locations, rewards and the log per timestep.
    After the change the same run must match exactly.
  - Centralised with `m = 3`. Each sub-step returns exactly one agent, in
    `core.priority` order. `core.t` advances every third sub-step. Agent 2's
    observation marks agent 1's chosen vertex as claimed, and its action mask
    equals `claim_mask`. With random legal slots for 100 timesteps,
    `core.last_overridden` is always empty.
  - Section. Turn `k` holds the `k`-th agent of every zone. No observation
    marks a vertex chosen in another zone. An occupied halo vertex is masked.
  - Full view. One turn, no claims, pooled.
  - A step with the wrong agent ids raises.
  - Replay under a fixed seed gives an identical log (correctness invariant 4).
  - The last sub-step of an episode returns an observation for every agent,
    with `truncateds["__all__"]` true, the claim column all zero and the
    action mask equal to `legality_mask`, for centralised and section.
- **Done when** the four correctness invariants hold for every controller.

### Step 5. Budget and batching per timestep [review]

Needs step 0's answers 3 and 4.

- **Branch** `feat/timestep-budget`.
- **Thesis** `sec:method:training`, `tab:trainparams` (the budget row).
- **What step 0 found.**
  - Today's `batch_mode="truncate_episodes"` with
    `rollout_fragment_length = horizon` cuts episodes in the middle once a
    timestep has more than one sub-step.
  - `batch_mode="complete_episodes"` makes one `EnvRunner.sample()` call
    return exactly one complete episode per env, whatever the fragment length.
    The algorithm samples every runner again until the summed env steps reach
    the train batch. Every timestep has at least one sub-step, so
    `train_batch_size_per_learner = max(num_env_runners, 1) * horizon` (today's
    value) gives exactly one episode per runner per iteration.
  - Neither `num_env_steps_sampled_lifetime` (sub-steps) nor
    `num_agent_steps_sampled_lifetime` (observations returned per agent,
    final ones included) counts timesteps.
  - Under `complete_episodes` RLlib resets the env at every sampling call with
    the explicit seed `config.seed + worker_index`. The adapter honours an
    explicit seed, so every training episode of a runner would get the same
    scenario.
- **Seed rule (decided 2026-10-16, option (a)).** The point of the seeds is
  that every controller trains on the same sequence of training seeds and is
  evaluated on the same evaluation seeds. A seed fixes the instance and the
  order stream (`sec:impl:instances`), so the comparisons are paired. Training
  on one seed over and over is not the aim. The adapter gains a
  constructor flag, `seed_from_cycle: bool = False`. When it is true, `reset`
  ignores the `seed` RLlib passes and always draws the next seed from the
  training cycle. `build_ppo_config`'s `env_creator` sets it to true. The
  evaluator, the examples and the tests build the adapter without it and keep
  passing explicit seeds, unchanged. `.debugging(seed=...)` stays, so RLlib's
  torch and numpy seeding and bit-for-bit replay are kept. This also fixes a
  bug on `main`: the first training episode of each runner gets
  `base_seed + worker_index` instead of a seed from the cycle, which is an
  evaluation seed once `worker_index >= train_seed_count`.
- **Files**
  - `training/config.py`. `batch_mode="complete_episodes"`,
    `rollout_fragment_length="auto"`, and `train_batch_size_per_learner`
    instead of `train_batch_size` (the new-stack key), at the value above.
    Rewrite the `PPOHyperparameters` docstring paragraph about the rollout
    length to match. The `env_creator` passes `seed_from_cycle=True`. Keep the
    field `training_budget_env_steps` and change its meaning and comment to
    timesteps (one per timestep, equal across arms).
  - `training/env.py`. The `seed_from_cycle` flag and the `reset` comment
    (RLlib does not always pass `seed=None`).
  - `training/trainer.py`. Stop on timesteps, not on RLlib's env-step
    counter. Log a timestep count from the callbacks (for example the sum of
    `core.t` over finished episodes) and stop on it.
  - `training/callbacks.py` for that metric.
  - `tests/unit/test_training_config.py`, `test_trainer.py`,
    `test_training_env.py`.
- **Tests.**
  - A tiny centralised run (`m = 3`, a short horizon, 2 iterations) reports
    exactly iterations × runners × horizon timesteps and stops at the budget.
  - With one seed split, the adapters that `build_ppo_config` makes for
    decentralised, centralised, section and full_view draw the same sequence
    of training seeds over a few episodes, in cycle order, whatever seed RLlib
    passes to `reset` (`last_seed`).
  - Evaluating each controller under one evaluation seed gives the same
    instance and the same order stream.
  - Without the flag, `reset(seed=s)` uses `s`, as today. The evaluator and
    the existing tests rely on it.

### Step 6. Evaluation through turns [review]

- **Branch** `feat/turn-based-evaluation`.
- **Thesis** `sec:impl:cost` (runtime), `sec:method:controllers`.
- **Files**
  - `evaluation/evaluator.py`. `_controller_run`'s `step()` loops sub-steps
    until `adapter.timestep_completed`, so one call is still one timestep.
  - `training/policy.py`. The call already takes any subset of agents.
    Update the docstring ("one module call per turn"). The sampling stream
    stays `(episode_seed + offset, t, agent_id)`, since each agent chooses
    once per timestep.
  - `tests/unit/test_evaluator.py`, `test_policy.py`.
- **Tests.** An evaluation of each controller, including full_view, runs `T`
  timesteps. A centralised evaluation never overrides. The summed routing
  runtime covers every turn (one record per turn, summed over the episode).
  Replay is bit for bit.

### Step 7. Examples, configs and docs [simple]

- **Branch** `docs/real-controllers`.
- **Files.** `configs/centralised.yaml`, `configs/section.yaml`, a new
  `configs/full_view.yaml`, the centralised and section examples
  (`examples/02_centralised_fixed.py`, `examples/03_section_based.py`), the
  comparison example `examples/05_full_comparison.py` if it lists the arms,
  `docs/controller_integration.md`, `docs/TRAINING.md`, `docs/MODELS.md`,
  `CHANGELOG.md`. Keep the example numbering.
- **New API stack.** Add one convention line to `AGENTS.md`: RLlib's new API
  stack only, no old-stack classes (the list in "RLlib: the new API stack
  only" above). `docs/model_integration.md` still says to inherit from
  `TorchModelV2`, which is the old stack. Change it to the `RLModule` the repo
  uses (`GNNActionMaskingRLModule`).
- **Done when** `slap-mapd train` starts with each config (the author runs
  it).

After step 7, the author closes #83, #81, #82, #86 and #23, and updates
`THESIS_MAP.md` at the workspace root. It still names the deleted
`controllers/centralised.py` and `section_based.py`.

---

## Open, not for the implementing session

- PPO treats each agent's choice as its own sample with its own ratio. Updating
  on the whole joint action of a decision is the alternative. Decide after the
  first training runs, not now.
- Whether the chain-rule centralised arm trains stably with a fleet-mean reward
  at larger fleets. The campaign instance has 3 agents, so this shows only
  once the fleet grows.

---

## Tracking issue text (the author opens it)

Title: `Real centralised and section-based controllers [A32]`

Body:

> The thesis now describes real centralised and section-based controllers
> (`[A32]`, `sec:pf:controllers`, `sec:method:controllers`, `sec:method:rl`,
> `sec:method:training`). The arms as built are one per-robot policy with a
> wider window, sampled independently, so the centralised arm is the
> decentralised arm with a large view.
>
> **What changes**
> - Centralised. Agents choose one at a time in the episode priority order,
>   each seeing the earlier choices (the centralised policy). A collision rule
>   inside the decision (the claim mask) means conflict resolution never
>   overrides a centralised agent.
> - Section-based. The same per zone on the zone plus halo, zones in parallel
>   (the section-based policy).
> - The vertex features gain a claimed flag. The action mask gains the claim
>   mask.
> - Credit follows the agents that choose together (the credit), so the
>   credit signal of #83 is no longer a setting.
> - A full-view setting (decentralised router with the whole graph in view
>   and the pooled readout) is added for a few conditions.
> - The budget counts one environment step per timestep.
>
> **Steps** (one PR each, from `main`, in order)
> - [ ] 0. RLlib spike with turns (findings posted as a comment here)
> - [ ] 1. The claim mask
> - [ ] 2. The claim feature
> - [ ] 3. Credit follows the decision, and the full-view setting
> - [ ] 4. The turn-based adapter
> - [ ] 5. Budget and batching per timestep
> - [ ] 6. Evaluation through turns
> - [ ] 7. Examples, configs and docs
>
> Resolves #83, #81, #82 and #86, and supersedes #23, once merged.
