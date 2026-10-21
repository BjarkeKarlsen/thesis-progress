# Appendix: a test for every number no paper gives us

Agreed 2026-10-21. The structure that combines this idea with `split_up_appendix_for_better_structure.md` is in `decisions/active/appendix_split_handoff.md`.

The rule: every number that does not come from another article gets an appendix that shows
how it was found. Your questions are grouped by topic below, each with the answer indented
under it. **To figure out** marks what nobody knows yet, with a proposed way to find out.
**Status** says where it stands.

Legend for where a number comes from:
- *cited*: taken from a paper.
- *derived*: follows from other numbers by a calculation.
- *tested*: read off an experiment.
- *open*: none of these yet.

A value that is only in a config, a code comment, or "the usual default" counts as *open*.
It is the current number, not a reason for it.

---

## 1. The graph (appendix C, `app:instances`)

**Q. Generate many instances for fleet sizes 8, 16, 32, 64, explain how the proof works in
simple terms, and cite van Knippenberg as inspiration.**

> **Status.** Decided and built (`[A57]`). The writing is handed off in
> `decisions/active/graph_appendix_handoff.md`.
>
> - **Size.** |V| = 16m gives 128, 256, 512 and 1024 vertices. *Cited*: van Knippenberg et
>   al. (2021) use 128 to 2048 nodes for 32 and 64 agents, and 1024 nodes for 64 agents.
> - **Role counts.**
>   - Parking = m is *cited*: it is the fewest Ma et al. (2017) allow.
>   - Storage = m/2 is the author's choice, so that agents share shelves. That is a reason
>     but not a test. *Open* whether m/2 rather than m/4 or m.
>   - Delivery = receiving = m/2 gives two agents per dock at every fleet size, so the
>     crowding at a dock means the same at every size. It replaced max(4, m/4), whose floor
>     gave m = 8 a different ratio. *Tested* only for well-formedness (every seed passes,
>     including 32 receiving vertices on the front row at m = 64). The ratio 2 itself is
>     *open*.
> - **Shape factors** (1.1 and 0.7) are chosen by us. The 50-seed test shows that they work
>   (every instance well-formed), not that they are the best values. So they are *tested*
>   for feasibility and *open* otherwise.
> - **The "proof".** There is nothing to prove again. Ma et al. prove that Token Passing
>   never deadlocks on a well-formed instance. Our part is a check run on every instance:
>   there are m parking vertices, and every role vertex can reach every other without
>   passing through a third. The appendix explains the check in words and cites their
>   theorem.
> - **To figure out.** Why two agents per dock and two agents per shelf. Either cite a real
>   warehouse ratio, or show that the main result barely changes with another ratio (for
>   example m/4).

---

## 2. Storage (appendix G, `app:storage`)

**Q. How much should each storage vertex hold? How do we test it without running the whole
system or making many assumptions? Can we take numbers from a model online? Has someone done
this already, and what do we cite?**

> Note that β is the congestion weight of the storage rule. The room one unit takes is the
> unit size per SKU (0.5, 1 and 2 in the configs).
>
> - **Proposed test** (*derived*). A shelf must hold its starting stock plus one period's
>   arrivals at the expected demand. Both follow from the arrival equation and the starting
>   stock formula, so capacity = largest required load × a margin. Appendix G's capacity
>   check then confirms it on each fleet. This needs no simulation and explains why m=8
>   needed 300 rather than 200.
> - **To figure out.**
>   - The margin on top of the required load. Proposal: the same ε as the arrivals.
>   - Whether a published warehouse model gives shelf sizes that fit our unit sizes. Only
>     cite one if it really matches. Otherwise the calculation stands alone.

**Q. Do delivery and receiving vertices hold an unlimited amount, or do they have a capacity
too? What would each choice change?**

> **Proposed answer: unlimited.**
> - A delivery vertex is where orders leave and a receiving vertex is where stock enters.
>   Neither holds stock in the model.
> - Ma et al. (2017) put no capacity on pickup or delivery locations.
> - What limits these vertices is that only one robot stands there at a time, and the vertex
>   rule already enforces that.
> - A dock capacity would add a queue at receiving that no research question asks about.
>
> **To do.** One sentence with this reasoning in the model, and one line in the scope
> appendix (`app:scope`).

**Q. The arrival rate should come from the Token Passing load sweep, high enough that agents
keep up but low enough that they don't wait for tasks. Run it for 8, 16, 32, 64 and adjust
the rate in a reasonable way as the fleet grows.**

> - **Test** (*tested*). `scripts/load_sweep.py` already reads off the rate at 0.6 of Token
>   Passing's capacity. That is the "keeps up, but agents don't sit idle" point.
> - **Don't scale the rate linearly with m.** The warehouse grows as 16m, so trips grow
>   roughly as √m and throughput per agent falls. Sweep each fleet size and take 0.6 of
>   that fleet's own capacity. This replaces commit "scale arrival rates linearly by fleet
>   size".
> - **To figure out.** Why 0.6. Proposal: show backlog against load for one fleet and
>   argue that 0.6 sits safely below the knee. Or cite queueing practice, where
>   utilisation is kept below the point at which waiting explodes, if you find a source.

**Q. `storage_rule.epoch_length: 100`, the Δ that decides when the storage rule updates.
There is no reason for this number.**

> **Status: open.** The thesis has Δ = TBD (sweep), and the configs use 100.
> **To figure out.** The constraints on Δ are:
> - several storage updates per demand drift (the drift period is 200 steps),
> - Δ long enough that a put-away finishes before the next update,
> - several updates per episode.
>
> Proposal: sweep Δ ∈ {50, 100, 200, 400} with Token Passing under demand storage and keep
> the value where the gain levels off. The constraints above give a short argument even
> before the sweep.

**Q. `congestion_weight: 1.0`, why?**

> **Status: open.** This is β of the congestion-aware storage rule, TBD (sweep) in the
> thesis. 1.0 is a placeholder.
> **To figure out.** β trades distance against crowding. Put both terms in the same unit
> first, then sweep β ∈ {0, 0.5, 1, 2, 4} with Token Passing and report the gain and the
> crowding. β = 0 is demand storage, which gives a built-in check.

---

## 3. Episode length (appendix D or J)

**Q. Why 2000? It lets demand and congestion evolve over time, but we need a reason and a
test. Does the learned-storage question need deciding first? Storage only changes every 100
steps. Does that suit a learned policy, or is it what lets us tell storage gains from
controller gains?**

> - **No need to wait for learned storage.** The horizon follows from timescales:
>   - **Warm-up.** It must pass the point where the backlog settles. Measure this with
>     Token Passing on each fleet.
>   - **Drift.** It must then cover several demand drifts. The ranking moves every 200
>     steps, so 2000 gives 10 moves.
>   - **Storage periods.** It must cover several storage periods Δ.
>
>   Test: plot throughput and backlog over time and set the horizon = warm-up + k drift
>   periods.
> - **Your last point is right.** A fixed storage period that is slower than routing is what
>   separates the gain of storage from the gain of the controller. That is a reason to keep
>   the storage rules and leave a learned storage policy as future work, as
>   `notes/how_the_system_works.md` recommends.
> - **Mismatch found.** The thesis gives the evaluation horizon as T = 630 (Appendix H,
>   `[A31]`), but the configs use `horizon: 2000`. One of them has to change.
> - **To figure out.** k, the number of drift periods. Proposal: the smallest k for which
>   the gain estimate stops moving, with k = 5 as a starting point.

---

## 4. Agents

**Q. The step costs come straight from van Knippenberg, so we don't study them. But why is the
observation depth 5? They studied depth too, so why 5, and should we test other depths?**

> - **Step costs.** Move 0.1 and wait 0.2 are *cited* from van Knippenberg et al. (2021),
>   Table 1, and are already in the thesis (`[A43]`). They say the values follow common
>   practice, so the thesis can only say "taken from them", not why they are right. The
>   same table has a wait at the goal of +0.1, which we don't use, since an idle agent pays
>   nothing in our reward.
> - **Depth 5** (`observation_depth: 5`, d_obs, TBD (sweep) in the thesis). *Open* today:
>   5 is only the config value. A possible source is van Knippenberg et al.'s Table 5,
>   where depth 5 scores best or close to best for 16 to 128 agents on 1024 nodes. That
>   becomes a reason only once checked to transfer to our graphs (below).
> - **To figure out.**
>   - Their depth counts edges on a train-yard graph, so check that 5 covers a similar share
>     of our graph. Report the mean window size at d_obs = 5 per fleet.
>   - Whether to sweep at all. The thesis says the range is never varied (`[A42]`), so
>     citing their table is enough unless you want one small check, for example 3 and 5 on
>     the 8-agent warehouse.
>   - H.Parameters should then change from "TBD (sweep)" to "5, after van Knippenberg".

---

## 5. Congestion reward

**Q. How did we arrive at this function, is it good, and does it work like CRAMP's
penalty?**

> - **What it is.** The term is −n_cng · δ_i(t). Here δ_i is the share of the agent's
>   field of view occupied by other agents. The thesis says its reading follows the crowd
>   density of CRAMP (Pham et al. 2024).
> - **To figure out.**
>   - Whether CRAMP uses crowd density as a reward penalty, and with what weight and form.
>     Read the paper and quote it. I don't know this for certain. If they penalise it in the
>     reward, cite their form and weight. If they only use it for planning, say ours is an
>     adaptation.
>   - Whether the term is good. It is not shaping, so it can change which behaviour is
>     best, and the thesis already states that trade-off.

**Q. The weight 0.1 barely contributes, and initial tests suggest the reward does nothing. We
need a reason for the number, or a test.**

> - **Likely reason it does nothing.** δ is a share between 0 and 1, so with few agents
>   per window it is often about 0.05. Then 0.1 × 0.05 = 0.005 per step, against a move
>   cost of 0.1 and a wait cost of 0.2. The term is about 20 times smaller than the step
>   costs. This is a back-of-envelope estimate, not measured.
> - **To figure out.**
>   1. Log the mean of each reward term per step in a short run. That shows the real size
>      of the congestion term.
>   2. Sweep n_cng ∈ {0, 0.1, 1, 2} on the 8-agent warehouse and read crowding and blocked
>      time. If 0 and 0.1 look the same, the term does nothing at 0.1.
>   3. Choose the smallest weight that lowers blocked time without lowering throughput, or
>      drop the term and say why.

---

## 6. Model

**Q. How did we arrive at this model? What do `num_rounds`, `hidden_width` and
`head_hidden_width` do, and why these values?**

> - **What they are.**
>   - `num_rounds: 2` is L, the message-passing rounds of the encoder. Each round lets a
>     vertex see one more hop, so 2 rounds mix information from vertices two edges away.
>   - `hidden_width: 32` is the size of the vertex embeddings inside the encoder.
>   - `head_hidden_width: 32` is the size of the hidden layer of the policy and value heads
>     that score the edges.
> - **Where the model comes from.** The PRIMAL line (Sartoretti et al. 2019), with the CNN
>   replaced by a graph network as van Knippenberg et al. did (Section
>   `sec:method:model`). That part is cited.
> - **Status: open.** L and hidden width are TBD in Appendix H. L is marked "sweep, incl.
>   L = 0". The values 2 and 32 are placeholders.
> - **To figure out.**
>   - L: run L ∈ {0, 1, 2, 3} on the 8-agent warehouse with one training seed. L = 0 shows
>     what message passing adds at all.
>   - Width: check whether van Knippenberg give their layer sizes (their paper, Section 4.2)
>     and cite them if so. Otherwise pick 32 or 64 by a small pilot, and say the study does
>     not tune it.

---

## 7. PPO

**Q. Why do we have these numbers and this training budget? Doesn't the thesis say checkpoint
selection depends on the task, not on `episode_return_mean`?**

> - **Core values.** lr 3e-4, clip 0.2, GAE λ 0.95, γ 0.99, entropy 0.02, 5 epochs and
>   minibatch 128 are all *open*. They are the config values, with no reason written down.
>   Some of them look like common PPO defaults, but that is not a reason until a source
>   is checked.
> - **To figure out.**
>   - Look up whether the PPO paper (Schulman et al. 2017) or the RLlib documentation for
>     your version actually uses these values. Only those that match can be *cited*.
>   - For the rest, either a small pilot, or the statement "not tuned, the same for every
>     arm". That keeps the comparison fair but is not a reason for the value itself.
>   - **Budget** (500 000 environment steps). This is *open*. Proposal: the budget at which
>     the return of the slowest arm levels off on the 8-agent warehouse, read from a
>     learning curve. Larger fleets may need more, which also has to be checked.
> - **Checkpoint selection mismatch.** The configs choose the best checkpoint by
>   `episode_return_mean`, the training return. SESSION_CONTEXT and the Experiments chapter
>   plan to choose it on validation seeds, which should mean a task measure such as
>   throughput or service time. These are not the same.
>
>   **To figure out.** Decide the selection measure. Then make the code evaluate checkpoints
>   on the validation seeds by that measure, or change the thesis to say training return.

---

## 8. Experiment values in the config

**Q. Every value in this block should say where it comes from.**

> | value | source | status |
> |---|---|---|
> | `discount: 0.99` | none, config value | *open*. **To figure out.** Check whether a source uses 0.99 for a comparable task, or tie it to the horizon (0.99 weighs about the next 100 steps, so compare with a typical task length) |
> | `deliver_reward: 10.0` (n_deliver) | van Knippenberg et al. (2021), Table 1: +10 for "complete episode". Ma et al. (2017) have no reward, since Token Passing is planning and its objective is service time | *cited*, with one difference to state: their +10 is paid once per episode, when every agent has reached its goal, and ours once per delivered task. **To figure out.** Whether that difference matters. A small pilot with n_deliver ∈ {1, 10} answers it |
> | `override_penalty: 0.5` (n_blocked) | none. The closest in van Knippenberg et al. is the collision penalty −2, which also ends their episode. We never let a collision happen, because conflict resolution overrides the move instead | *open*. The model only needs it above 0, so that an override costs more than a chosen wait. **To figure out.** Whether to take their −2 as the size (an override is the move that would have collided), or set it with the congestion sweep of section 5 |
> | `move_cost: 0.1` | van Knippenberg et al. (2021) | *cited* (they give no reason beyond common practice) |
> | `congestion_reward_weight: 0.1` (n_cng) | none | *open*, see section 5 |
> | `congestion_sensitive: false` | none | *open*. **To figure out.** Which experiments switch it on, and why the default is off |
> | `seed: 0` | none | not a model value, but the seed scheme is *open* (SESSION_CONTEXT, queue item 4) |
