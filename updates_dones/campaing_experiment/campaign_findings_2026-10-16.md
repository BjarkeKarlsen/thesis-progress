# Campaign findings and open decisions, 2026-10-16

Local note at the workspace root, not in a repo. It explains the problems the first campaign
(`~/thesis_runs/campaign_2026-10-14`) showed, what was measured and what is only a guess, and what
is decided and what is still open. The full numbers are in
`~/thesis_runs/campaign_2026-10-14/analysis/ANALYSIS.md`.

Sample sizes everywhere: one trained checkpoint per condition and load, 6 evaluation seeds (5 to 10),
one instance, 3 agents, horizon 630. Nothing below says how a retrained policy would behave.

## 1. The problem in one paragraph

Token Passing keeps up at every load tried (up to 0.3 tasks per step). The three learned arms keep up at
0.15, are borderline at 0.25 and fail at 0.3. Their throughput stops at about 0.21 tasks per step
however fast tasks arrive, and the three arms stop at the same place. So whatever limits them is
shared by all three, and it is not the window. The fleet is the bottleneck. Tasks wait for a free agent,
and waiting for an agent is most of the extra service time at 0.25 and 0.3.

## 2. What was measured

Throughput at each load (tasks per step, mean over 6 seeds):

| condition | 0.15 | 0.25 | 0.3 |
|---|---|---|---|
| token_passing | 0.145 | 0.234 | 0.267 |
| centralised | 0.145 | 0.206 | 0.214 |
| section | 0.146 | 0.208 | 0.212 |
| decentralised | 0.146 | 0.207 | 0.217 |

How long one agent is tied up per task. With 3 agents, one task takes about 3 divided by the
throughput of agent time. At 0.3 that is 14.0 steps for the learned arms and 11.2 for Token Passing.
Travel plus blocked time per task is 13.6 and 10.2. So the learned agents are about 97% busy. They are not
idle. Each task simply costs them about 3 to 4 steps more than it costs Token Passing.

Where those extra steps go, from the evaluation traces (60 episodes, about 14 400 legs, a leg being one
walk to a pickup or to a delivery). Means per leg:

| run | shortest hops | steps taken | steps that got closer | moves that did not | overridden | waited |
|---|---|---|---|---|---|---|
| centralised, 0.3 | 4.7 | 6.8 | 5.5 | 0.73 | 0.58 | 0.00 |
| section, 0.3 | 4.7 | 6.8 | 5.4 | 0.68 | 0.74 | 0.00 |
| decentralised, 0.3 | 4.7 | 6.6 | 5.3 | 0.59 | 0.76 | 0.00 |
| decentralised+comm, 0.25 | 4.8 | 7.3 | 5.3 | 0.54 | 0.42 | 1.10 |

Reading it. A task has two legs, so the shortest route is about 9.4 steps, and Token Passing's travel time
is 9.5 to 10. So Token Passing walks the shortest route and the learned arms do not. Of the 4 extra steps per
task, about 1.2 to 1.5 are overridden moves (conflict resolution said no) and about 3 are detours. A detour
is a move that does not get closer to the goal, plus the move needed to recover it. This is measured from
the traces, with hop counts and ignoring edge costs. The cause of the detours is not measured.

Training also showed that the return was still rising for three runs at the end (centralised and
section at 0.25, centralised at 0.3), about 110 per 20 iterations on a return near 2000.

## 3. Why the evaluation might be part of the cause

Evaluation samples a move from the policy. It does not take the most likely move. Training used an entropy
bonus of 0.02, which keeps the policy spread out on purpose. The code says in two places that whether
evaluation should be greedy is still open (`training/policy.py`, `evaluation/evaluator.py`).

A sampled policy that is spread out makes occasional wrong-way moves. That looks exactly like the detours
above. It is the strongest cheap suspect, but it is a guess until the same checkpoints are evaluated greedily.
This needs no new training.

### Should evaluation be greedy?

It is a choice and not a rule. Both are used in practice. What matters is to decide before looking at results
and to say which one was used.

For greedy as the main evaluation:
- The thesis scores controllers by their window, not by their exploration noise. The entropy bonus is a
  training device, so it should not be part of the score.
- Token Passing is deterministic, so a greedy policy is the fairer opponent.
- A greedy run is fully repeatable and has less spread over seeds.

Against, or for also reporting sampled:
- PPO optimises the sampled policy. The greedy version of it is a different policy and can be worse, or
  can get stuck. Two decentralised agents in the same situation choose the same move every time, so a
  head-on pair can repeat a refusal forever. Sampling breaks that tie by luck.
- If greedy gets stuck, that is a result about the arm and must be reported, not hidden.

Suggested rule for the author to accept or change: evaluate every checkpoint both ways on the same seeds,
name greedy as the primary result before looking, and report sampled as a robustness row. This is a thesis
decision (`tab:evalparams`, evaluation of a checkpoint), so the wording is proposed in chat first.

## 4. Decentralised with communication

Measured, at 0.25 and one checkpoint:
- It completes 0.05 less than the same arm without communication (interval over seeds, minus 0.07 to minus 0.03).
- It keeps up on 1 of 6 seeds, against 5 of 6.
- In the traces it chooses to wait on 17% of agent steps. The other arms wait on about 0%. It is overridden
  less (6% against 11%) and has fewer head-on attempts (6 against 45 steps per episode).
- In training it stands still on 29% of steps against 12%, its return is noisier and the evaluated last
  iterate sits in a dip.

So it learned a cautious policy that waits. Why is not known. Candidates are too little training, the
checkpoint sitting in a dip, the extra cost of waiting being too small in the reward, or a real effect of
communication. One run cannot tell these apart.

It is also the only arm that failed on memory in the pilot. That failure came before the chunked value
pass (PR 145, now on `main`). The campaign run completed on the first attempt.

## 5. Memory, and the difference between the two model files

The two files do different jobs.

`models/local_subgraph_encoding.py` is the data side, with numpy arrays and no learning. For one agent
at one timestep it cuts out the window around the agent, pads it to a fixed size so every row of a batch
has the same shape, and writes masks for the padding. With communication it also copies the padded window of
every sender into the same row. RLlib stores these rows in its batch.

`models/gnn_encoder.py` is the network side, with torch. It takes the padded rows and runs the
message-passing rounds over them. It has a slow single-observation version (the oracle the tests
compare against) and the batched version that training uses.

In numbers for the campaign instance (51 vertices, window cap 33 vertices, 4 outgoing edges at most,
2 senders at most). Measured on the GPU, 5 824 parameters in both cases:

| | no communication | communication |
|---|---|---|
| observation per row, stored | 3.6 KB | 10.8 KB |
| peak memory, value pass of 512 rows | 93 MiB | 283 MiB |
| peak memory, one training minibatch of 128 rows with gradients | 51 MiB | 97 MiB |
| one whole iteration in one pass (13 230 rows) | 2.4 GB | out of memory |

What this says.
- Parameters and gradients are tiny, so changing the number format of weights or of gradient clipping saves
  nothing. The model is already float32. No gradient clipping is configured at all.
- The memory is in activations, which grow with the number of rows. Communication triples it, because
  each row carries its senders' windows and the same window is embedded again for every receiver that hears it.
- The chunked value pass already keeps the peak small. Training minibatches are small.

If more room is wanted, in order of how safe it is:
1. Lower `VALUE_CHUNK_ROWS` (now 512). It only bounds memory and does not change a result.
2. Store the edge list in a smaller integer type. The edge list is 2.1 KB of the 3.6 KB per row, and
   it is stored as 64 bit integers. It is cast back when the network runs. This is a storage change only.
3. Stop storing the parts that depend only on which vertex the agent stands on (edge list, masks). Look
   them up on the GPU from the agent's vertex instead. This shrinks the rows the most but changes the
   observation and the tests, so it needs its own plan.

Embedding each agent's window once and sharing it between receivers would also cut the communication cost, but
it changes how the loss reaches the sender (issue 91), so it is a model decision, not a memory tweak.

## 6. Longer episodes and a longer budget

Proposal from the author: episodes of about 2000 steps. Consequences:
- Fewer noisy releases. At 0.15 a 630 step episode releases about 94 tasks (spread of about 10%). At
  2000 steps it releases about 300 (about 6%). The keep-up ratio divides by the nominal rate, so this
  noise is what made f_up = 0.9 fail healthy Token Passing runs in the pilot.
- More storage epochs inside one episode, which adaptive storage needs.
- One iteration is 7 runners times 2000 steps, 14 000 steps. A 500 000 step budget is then 36 iterations
  instead of 114, which is too few updates. A budget near 2 000 000 steps gives about 143 iterations. At the
  measured rate of about 18 to 21 minutes per 500 000 steps that is roughly 75 to 85 minutes per run.
- Evaluation at 2000 steps takes about 3 times longer, still a few minutes per load.
- Training horizon and evaluation horizon should stay equal. The thesis leaves both open (`tab:evalparams`).

## 7. Arrival rates

At 0.4 no condition keeps up with 3 agents. Token Passing finishes at most about 0.3, and the threshold
is 0.8 times 0.4 = 0.32. Under `eq:throughput` nothing is then compared on service time. Two options:
- report completion share, throughput and backlog at 0.4 as an overload point, with service time marked
  as falling behind, which fits the thesis as written
- raise the fleet so 0.4 becomes a keep-up load, which changes the instance

A level around 0.2 to 0.22 is still wanted. The learned arms keep up there with a heavy queue, which is
where a service-time gain can be tested. That window is inferred from the 0.21 ceiling and is not run.

## 8. Plan, in order, nothing done yet

1. Evaluate the 10 existing checkpoints greedily (small evaluator flag, no training). Needs the greedy
   decision above.
2. Turn the leg measure into a tool in the repo, and extend the trace so it also lists the waiting tasks and
   which agent holds each active task at every step. The trace today has the task, phase and goal per agent,
   and only the count of waiting tasks.
3. Train with 2000 step episodes and a larger budget. Decentralised with and without communication first,
   on 3 or more training seeds.
4. Add 0.2 to 0.22 and the 0.4 overload point to the load levels.

## 9. Open decisions

- Greedy or sampled as the primary evaluation (section 3).
- 0.4 as an overload point, or a larger fleet (section 7).
- Episode length, budget and evaluation horizon (section 6). All three are TBD in the thesis.
- Whether communication gets the same longer budget as every other arm. The recommendation is yes, so
  that the one-budget claim holds.

## 10. Decisions made on 2026-10-16

- Evaluation of the PPO policies stays sampled, which is what PPO optimises. Only the planner is
  deterministic by nature. Greedy evaluation is a diagnostic, not a second way of scoring. It is on branch
  `diag/greedy-evaluation` (`ModulePolicy(greedy=True)`, `--greedy` in example 05, sampled stays the default).
  Run it with `bash ~/thesis_runs/campaign_2026-10-14/greedy_eval.sh`. The result goes to
  `~/thesis_runs/campaign_2026-10-14_greedy/analysis/ANALYSIS.md`. Only its evaluation tables are new. Its
  training and stall sections are copies of the sampled campaign, because the greedy sweep writes no traces.
- How to read the diagnostic. If greedy throughput at 0.3 comes close to Token Passing (about 0.27), the
  0.21 ceiling is mostly the policy's own sampling noise, and the fix lies in training (for example the
  entropy bonus). If it stays near 0.21, the policies learned the detours, and the cause is training or
  something all three arms share. A greedy policy can also deadlock. That would show as fewer completed tasks.
- Memory, first steps: lower `VALUE_CHUNK_ROWS` and store the edge list in a small integer type. The lookup
  by vertex (option 3 in section 5) stays a later option.
- Next piece of work: split the travel part of service time into the route that was needed (the shortest
  route from where a leg starts, which the storage layout sets), the detour, the overridden steps and the
  waited steps, and extend the trace with the waiting tasks and the agent holding each active task.

## 11. Result of the greedy diagnostic

Measured on all 60 greedy evaluation runs (10 checkpoints, 6 seeds each, trained load only, the campaign's seeds).

- Greedy throughput falls to 0.011 to 0.057 tasks per step, from 0.145 to 0.217 when sampled. No greedy
  run passes the keep-up check (0 of 60), against 33 of 60 when sampled.
- The fleet deadlocks. In one traced greedy episode per arm at 0.25 (seed 5), the fleet finished 2 of 140
  tasks (centralised), 11 (section), 82 (decentralised) and 8 (decentralised with communication). The rest of
  the episode, from step 37 to 630 in the centralised case, two agents on neighbouring vertices each wanted the
  other's vertex and were overridden on 96% of their steps. With communication the agents instead stood still on
  91 to 97% of their steps. This is four episodes on one seed, so it shows the mechanism and not how often it happens.
- The service times in the greedy table are shorter (for example 18 against 49 steps, centralised at 0.25), but they
  average only the few early tasks that finished. They are not comparable.
- When a greedy agent does move, it walks a shorter route. Travel time is 9 to 11 steps against 11 to 12.

What it says. My guess, given before the run, that sampling noise causes the ceiling was wrong in its direction.
The noise is what lets the fleet get out of head-on stand-offs. The policies are memoryless. The same situation
gives the same move, and conflict resolution only says no, so a pair that wants each other's vertex stays stuck
until a random draw differs. That the learned detours are partly the price of this escape is a hypothesis, not
measured. It is consistent with the share of moves that go the wrong way, about 10 to 12% (section 12).

Possible directions, none of them decided. The policy could see that it was overridden at the last step. The
resolution rule could make the lower-priority agent give way instead of only blocking. Either one is a model
change and needs the thesis first. This also means the head-on deadlock question from the campaign report has an
answer. Sampled evaluation hides it, and greedy evaluation shows it in every arm.

## 12. Result of the leg tool (`evaluation/legs.py`, branch `feat/leg-analysis`)

Sampled evaluation traces, 6 episodes per run. Per complete task, in steps (a task has two legs). The four parts add
up exactly to the total, and the total matches travel plus blocked time in the sweep.

| run | needed route | detour | overridden | waited | total | moves going farther |
|---|---|---|---|---|---|---|
| centralised, 0.3 | 9.5 | 2.9 | 1.2 | 0.0 | 13.6 | 12% |
| section, 0.3 | 9.5 | 2.7 | 1.5 | 0.0 | 13.7 | 11% |
| decentralised, 0.3 | 9.4 | 2.4 | 1.5 | 0.0 | 13.3 | 10% |
| decentralised+comm, 0.25 | 9.5 | 2.1 | 0.8 | 2.2 | 14.7 | 9% |
| centralised, 0.15 | 8.7 | 2.4 | 1.9 | 0.0 | 13.0 | 11% |

- The needed route (9.4 to 9.5) equals Token Passing's travel time at 0.3 (9.5). So the whole difference to Token
  Passing is detour (2.1 to 2.9) and overridden steps (1.2 to 1.5), about 4 steps per task.
- No move is level. A move goes closer or farther.
- The communication policy has the smallest detour and override cost but loses 2.2 steps per task to waiting.
- The tool reads existing traces. Per task release times need the trace extension (`trace_extension_plan.md`).
