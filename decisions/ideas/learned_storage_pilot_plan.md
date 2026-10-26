# Pilot plan: a learned storage rule under Token Passing

**Status 2026-10-22. Stage 1 built, in the worktree `~/worktrees/pilot-learned-storage` (branch `pilot/learned-storage`, uncommitted).** The author asked Claude to decide the three open questions and build it. Decided. Stage 1 runs under Token Passing even though a tie with the demand rule is likely. The storage policy trains with a plain PPO loop, not RLlib. Units not picked by $T$ are credited with what is known by then. Builds on
`learned_storage_policy.md` (decisions and memory check) and the draft text in
`learned_storage_intro.tex`. A pilot in `slap-mapd-coupling`, not thesis text.

## What Token Passing leaves for storage to learn

One episode per fleet at its selected main load, seed 0, Token Passing, run on
2026-10-22 with `scripts/sweep/load_sweep.py` and the uncommitted fleet configs
of the main checkout. One seed, so read the sizes, not the differences.

| agents | rate | rule | put-aways | service | wait for agent | travel | blocked |
|---|---|---|---|---|---|---|---|
| 8 | 0.12 | demand | 209 | 22.2 | 9.4 | 12.2 | 0.63 |
| 16 | 0.15 | fixed | 222 | 80.9 | 53.8 | 25.2 | 1.89 |
| 16 | 0.15 | demand | 231 | 93.2 | 66.7 | 25.1 | 1.44 |
| 32 | 0.36 | fixed | 411 | 83.4 | 62.5 | 19.5 | 1.49 |
| 32 | 0.36 | demand | 467 | 47.8 | 24.4 | 22.7 | 0.76 |
| 64 | 0.42 | fixed | 463 | 171.1 | 123.4 | 45.0 | 2.68 |
| 64 | 0.42 | demand | 511 | 175.8 | 125.9 | 47.7 | 2.13 |

Means per pick, in timesteps.

- **Under Token Passing a pick is blocked for 0.6 to 2.7 steps**, under 5 % of
  its service time. Token Passing plans paths that avoid each other, so traffic
  costs it little. The time goes to waiting for an agent.
- **So under Token Passing the loaded time is close to the trip distance.** A
  learned rule there has almost no traffic to react to. The expected outcome is
  that it learns what the demand rule already does. Where it can still differ is
  capacity (keeping near shelves for popular SKUs, as Waubert de Puiseau's agent
  learned) and how many shelves a SKU is spread over.
- This matches `thesis_plan.md` section 4.2. Demand storage has not been shown
  to create congestion. The learned routers had longer and more blocked routes,
  so traffic is where a learned router meets the storage rule.

So the pilot is two stages. Stage 1, this PR, checks that a storage policy
learns at all, under Token Passing, where it is cheap and nothing else learns.
Stage 2, a later PR, puts the trained policy against a fixed learned router,
where blocked time is larger. Only stage 2 can show coupling.

## Stage 1, this PR

### Setting

- 8 agents, rate 0.12 (the selected main load), horizon 2000, $\Delta = 100$.
  One episode takes about 7 s and gives about 200 storage choices.
- Token Passing routes and assigns, as in the load sweep. No Ray.

### Code, in a worktree from `main`

1. **The learned put-away rule** (`storage/learned.py`). SKUs in order of
   $\hat\rho_t$, then one choice per put-away among the shelves with room, as
   in `eq:storagepolicy` of the draft. Built on the shared fill loop
   `_put_away`, so capacity, unplaced units and the result type stay as for the
   other rules. It records each choice (observation, mask, shelf, log
   probability, value) with the (SKU, shelf) it gave.
2. **Config and env.** `storage_mode: learned`, with the same requirements as
   `demand` (Delta, the estimates). The env takes the rule object the way it
   takes an `assigner`, since a learned rule carries a network and a recorder
   and cannot come from the name registry alone.
3. **Where a pick's units came from.** The env already keeps lots per (SKU,
   shelf) and takes them oldest first (`_take_units`). The lot gains the id of
   the put-away that delivered it, and a pick records which put-aways its units
   came from. Starting stock has no put-away and credits nobody.
4. **Credit, after the episode.** A choice gets minus the loaded time of its
   put-away plus the loaded time of each pick that took its units, split by
   units when a pick takes from two lots. Loaded time is
   $t^{\mathrm{finish}} - t^{\mathrm{pickup}}$. The sum over all choices equals
   minus the objective of `eq:storagelearning` over what was credited, and a
   test checks that.
5. **The network** (`models/storage_policy.py`). The routers' `GNNEncoder`
   (L 2, width 32) over the whole graph, with its own weights and its own
   vertex features: the role flags, occupied, free capacity share, units of
   the SKU on the shelf and on their way, traffic and waiting through the
   vertex, and trip distance. A shelf score per storage vertex from the shelf's
   embedding and the readout. The readout is the pooled mean plus the SKU
   (demand estimate, unit size, units left). A value head on the readout.
   `GNNEncoderConfig` gains an input width with today's 8 as its default, so
   the routers do not change.
6. **Training** (`training/storage_ppo.py`). Plain PPO in torch: a few
   episodes in parallel processes per iteration, rewards credited when each
   episode ends, GAE over the choices in order, clip, minibatches. Starting
   values copied from the router configs (lr 3e-4, clip 0.2, GAE 0.95,
   gamma 0.99, minibatch 128, 5 epochs, entropy 0.02), marked illustrative.
   Training seeds from the spec's seed split.
7. **Evaluation.** The load sweep runs `learned` next to `fixed`, `demand` and
   `congestion` from a checkpoint, on the same test seeds, so the comparison is
   paired. Each row also gets the mean loaded time of picks and put-aways.
8. **Tests.** The rule respects the three conditions of the storage update.
   Masked shelves are never chosen. Provenance follows the lots. Credit adds up.
   A two-iteration training smoke test. Same seed, same run.

### Why plain PPO and not RLlib for the storage policy

The routers train through RLlib with one step per timestep. The storage policy
acts on the slow clock, a varying number of times per epoch, and its reward is
known only when the units are picked, often after the episode's last choice.
In RLlib that needs a custom connector to move rewards back to their choice.
Token Passing needs no Ray at all. A short PPO loop over whole episodes is
simpler and easier to check. The cost is a second PPO implementation in the
repo. If stage 2 trains in turns with a learned router, the storage side keeps
this loop and loads the router for inference only.

### Budget

Eight episodes in parallel per iteration, about 10 s and 1600 choices. A first
run of 500 iterations (4000 episodes, 800 000 choices) takes about 1.5 hours.
Waubert de Puiseau needed about 20 million choices with three actions, but
their observation was a 500-long one-hot vector. If the curve still rises at
500 iterations, extend it.

### What counts as passing

Evaluated on 20 test seeds (cheap under Token Passing), paired.

1. The training return rises, and the learned rule beats a rule that picks a
   shelf with room at random.
2. The learned rule's mean loaded time is at most fixed storage's.
3. Learned against the demand rule is reported either way. A tie is the
   expected result under Token Passing and says that Token Passing leaves only
   distance to learn.

### Not in this PR

- Stage 2 with a learned router. It needs a router checkpoint trained under
  the put-away model, and the decision on whether to train in turns.
- Any thesis text. The `[Axx]` tags and the change to `[A48]` wait for the
  pilot.
- Larger fleets.

## Open points

- **Units still on a shelf, or a put-away still on its way, at $T$.** Default:
  credit what is known by $T$, and give a put-away that has been picked up the
  time it has been carried so far. The alternative is to bootstrap from the
  value head.
- **Reward scale.** Divide by the mean trip distance of the warehouse, so the
  scale is about one at every size.
- **The pilot branch and the thesis.** `AGENTS.md` asks the code to match the
  thesis, and the learned rule is not in it. The PR is marked as a pilot and
  only lands on `main` if the rule is adopted.
- **Configs.** The main checkout has uncommitted fleet configs with the selected
  rates (0.12 at 8 agents). A worktree from `main` does not have them, so the
  pilot config sets 0.12 itself.

## First run, 2026-10-22, and what changed for the night run

- **First run** (8 agents, the routers' PPO values: gamma 0.99, entropy 0.02, 8 episodes per
  iteration), stopped at iteration 156. The policy learned a little up to iteration 40, then went
  back to uniform (entropy 1.386, log 4). The iteration-150 checkpoint on 20 test seeds: loaded
  time 3077, random 3065, demand 2698, fixed 3404. Service time is the same under demand,
  random and learned (24.7 to 24.8), so under Token Passing at 8 agents where an adaptive rule
  puts stock barely moves the service time. Plot and rows in
  `~/thesis_runs/storage_pilot_2026-10-22/`.
- **Why.** At 8 agents there are 4 shelves with trip distances 11 to 15, each about 77 % full,
  and demand saves under 2 steps per choice over random against tens of steps of noise. GAE
  with gamma 0.99 added the rewards of the next choices to every advantage, and the entropy
  bonus then pulled the policy back.
- **Changes.** gamma 0, entropy 0.005, 16 episodes per iteration, two torch threads for the
  update (the default made it ten times slower), and a put-away-only credit as a check with a
  known answer. The crowding measure is cached on the graph (16 times faster at 64 agents,
  identical results), also on its own branch `perf/field-of-view-cache` for `main`.
- **Night run.** `scripts/storage_pilot_night.bash`: 8 agents put-away check, 8 agents full
  reward, then 64 agents (rules first, then training for 6 hours). It waits for any load or
  parameter sweep to finish first.
- **Scaling** to 128 to 1024 agents: `../active/scaling_to_1024_agents.md`.

## Night run outcome, 2026-10-22 to 2026-10-23

All three stages ran, each evaluated on 20 paired test seeds under Token Passing. The results and the code are in
`~/thesis_runs/storage_pilot_night_2026-10-22/`. The figure is `plots/pilot.png` there, drawn by
`thesis-progress/scripts/results/plot_storage_pilot.py`. Credit is the loaded time of a put-away and of the picks
that take its units, from pickup to finish (point 4 above), so the time a task waits for a robot is not in it.

| stage | rule | loaded time (the credit) | pick | put-away | all tasks | put-aways done | keeps up |
|---|---|---|---|---|---|---|---|
| 8, put-away credit only | learned | 6.39 per put-away | 22.0 | 91.9 | 52.0 | 176 / 191 | 20 / 20 |
| 8, full credit | fixed | 3404 | 44.4 | 68.3 | 54.5 | 170 / 183 | 20 / 20 |
| 8, full credit | demand | 2698 | 24.7 | 130.5 | 67.2 | 157 / 190 | 20 / 20 |
| 8, full credit | random | 3065 | 24.8 | 34.8 | 29.1 | 174 / 183 | 20 / 20 |
| 8, full credit | learned | 2783 | 21.9 | 72.7 | 43.7 | 178 / 191 | 20 / 20 |
| 64, full credit | fixed | 29082 | 150.2 | 68.4 | 120.4 | 421 / 450 | 20 / 20 |
| 64, full credit | demand | 21767 | 167.3 | 530.7 | 266.8 | 268 / 496 | 0 / 20 |
| 64, full credit | random | 28602 | 99.2 | 56.2 | 84.1 | 427 / 450 | 20 / 20 |
| 64, full credit | learned | 20988 | 162.2 | 488.5 | 245.6 | 233 / 497 | 0 / 20 |

Service times are means in timesteps. "All tasks" weights picks and put-aways by how many were completed.

- **The training loop works.** In the put-away check the return levels off within about 25 iterations. The
  learned put-away distance (6.39) is as short as the demand rule's (6.48) and well below fixed (9.20) and random
  (8.22). There is no nearest-shelf reference in the output, so the demand rule is the closest benchmark.
- **8 agents, full credit. The pass criteria of stage 1 are met.** The return rises, the learned rule beats
  random on loaded time (282 shorter) and is below fixed. It is 85 longer than demand (95 % interval 48 to 122).
  The return levels off by about iteration 50 of 400.
- **8 agents, pick service time.** The learned rule is the fastest on picks (21.9 against 24.7 for demand,
  interval of the difference 2.1 to 3.7). The put-away-only policy reaches the same 22.0, so this comes from
  where put-aways go, not from the pick credit.
- **64 agents. The policy learns its credit, and the credit points the wrong way.** The return rose from −790 to
  −306, and the learned rule has the shortest loaded time of any rule. Meanwhile pick service time rose from 95
  to 160 during training, and the rule keeps up on no seed, like demand and congestion. It stopped at the 6 hour
  cap after 120 iterations.
- **Random storage is the fastest rule once put-aways count, at both fleet sizes.** At 64 agents only about half
  the put-aways under demand or learned storage are completed, against over 90 % under random or fixed.
- **Likely cause.** Token Passing hands out a task only if no other robot's path already ends at that task's
  pickup or delivery vertex (`planners/token_passing.py`, rule 1). So tasks aimed at the same shelf queue one at
  a time. Shortening the loaded time sends many put-aways to the few shelves nearest the receiving side, where
  they queue. The credit does not count that wait. This follows from the code rule and has not been measured
  directly.
- **The same holds for the demand rule in the parameter sweep.** See
  `../../notes/parameter_sweep_2026-10-23.md`.

Open, for discussion. Nothing is decided yet.

1. Whether the credit should count the whole service time, from release to finish, instead of the loaded time.
2. Whether to measure the queueing at shelves directly first, to confirm the cause.
3. Whether the pilot continues at all, given `how_the_system_works.md` recommends keeping the rules and naming a
   learned storage policy as future work.

## Rerun of 2026-10-23, with the check of [A59] and the endpoint diagnostics

`~/thesis_runs/storage_pilot_night_2026-10-23/`. Same credit as the night before (loaded time).

- **8 agents.** The learned rule keeps up on 20 of 20 seeds, demand on 19 (one seed's put-aways fall behind). Learned minus demand on pick service time is −2.9 (95 % interval −3.7 to −2.1), minus fixed −22.5, minus random −3.0. Its put-away service time is about fixed's (+3.0, −6.1 to +12.2), well below demand's (−59.8) and above random's (+36.5).
- **64 agents, the rules.** Demand storage keeps up on picks on 20 of 20 seeds and on put-aways on 0 of 20. A demand put-away waits 510 timesteps for a shelf another robot's path ends at, of a put-away service time of 531. Under random storage that wait is 16. Robots are busy 33 % of the time under demand, 42 % under random. The wait for a taken receiving vertex is 0 at every fleet size and under every rule.
- **So the 64-agent failure is Token Passing's endpoint rule meeting a rule that sends many put-aways to the same few shelves.** The loaded-time credit does not see that wait, so the learned rule learns the same concentration.
- **Open.** What the credit should weigh, put-aways or picks. See the discussion of 2026-10-23.

**Decided 2026-10-23: option A, each task's whole service time.** A choice is credited with the service time of its put-away, release to finish (or to T), and its share of the service time of the picks that took its units. The evaluation rows of the night runs, scored with each candidate credit, show why (`total_service_time` is A summed over an episode).

| credit | where it ranks the rules that fail the check (demand, congestion) |
|---|---|
| loaded time (the first credit) | best, at 8 and at 64 agents |
| A, whole service time | last, at 8 and at 64 agents |
| C, pick service time only | 2nd of 5 at 8 agents, above two rules that keep up |

B, pick service time with a penalty for put-aways falling behind, would match the thesis rule exactly but needs a penalty weight nothing in the thesis gives. It is the fallback if A gives up too much pick time. A's one lean is that at 8 agents it ranks random storage just above the learned rule of the loaded credit, trading about 3 steps of pick time for about 36 of put-away time. Code: `credit=service` in `training/storage_ppo.py`, `measure="service"` in `storage/learned.py`, the default of `scripts/storage_pilot_night.bash`.
