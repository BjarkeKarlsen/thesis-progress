# Memory reduction plan, 2026-10-16

Local note at the workspace root. It says where the memory of a training run goes, what was measured, and
what to change, in order. Nothing here is implemented yet. Code is in
`slap-mapd-coupling/src/slap_mapd_coupling/models/` and `environment/action_masking.py`.

## Where it stands

Memory is not limiting today. The pilot's decentralised run with communication ran out of GPU memory once, before
the value pass was chunked (PR 145, on `main`). The campaign's communication run finished on its first attempt.
The reason to act now is the plan for longer runs, 2000 step episodes and a budget near 2 000 000 steps. That makes
one iteration 14 000 steps, so the stored batch grows about 3 times.

The GPU is an RTX 2070 Super with 8 GB. Other processes already use about 1.4 GB of it.

## What was measured

The model is small and already float32. It has 5 824 parameters at hidden width 32. So weights, their gradients
and any clipping of them take no meaningful memory. No gradient clipping is configured at all. Changing the
number format of the weights saves nothing. The memory is in the rows of observations and in the activations that
grow with the number of rows.

Peak extra GPU memory of the encoder (campaign instance, 3 agents, 2 senders at most):

| rows | no communication | communication |
|---|---|---|
| 128, with gradients (one training minibatch) | 51 MiB | 97 MiB |
| 512, no gradients (one chunk of the value pass) | 93 MiB | 283 MiB |
| 2 048, no gradients | 366 MiB | 1 120 MiB |
| 13 230, no gradients (one iteration, unchunked) | 2 367 MiB | out of memory |

It grows in a straight line with rows, about 0.18 MiB per row without communication and 0.55 MiB with it.

What one stored row holds, in bytes (computed from the observation space):

| key | shape | type | bytes |
|---|---|---|---|
| edge_index | 132 by 2 | int64 | 2 112 |
| node_features | 33 by 6 | float32 | 792 |
| edge_mask | 132 | float32 | 528 |
| node_mask | 33 | float32 | 132 |
| move_target_index | 4 | int64 | 32 |
| own_index, congestion | 1 each | int64, float32 | 12 |
| **total, no communication** | | | **3 608** |
| the same for each of 2 senders (communication) | | | adds 3 600 each |
| **total, communication** | | | **10 808** |

The edge list alone is 59% of a row.

## What to change, in order

### Step a. Lower the chunk size

`VALUE_CHUNK_ROWS = 512` in `environment/action_masking.py` bounds the rows of one encoder pass in the value
pass. It does not change any result, because the pass has no gradients and each row is independent.

- 256 rows halves the peak of that pass, to about 47 MiB without communication and 140 MiB with it.
- The cost is more, smaller passes, so a little slower. It is not on the training path (minibatches of 128 are).
- Make it a parameter next to the PPO settings, so a run can lower it without editing the module. Keep 512 as the
  default so nothing changes unless asked.

### Step b. Store the observation in smaller types

This changes only how a row is stored, not what is in it.

b1. The index arrays hold vertex numbers below 33, so they fit in int8.

| | now | after b1 | saved |
|---|---|---|---|
| no communication | 3 608 | 1 732 | 52% |
| communication | 10 808 | 5 194 | 52% |

b2. The masks are 0 or 1 and are stored as float32. As uint8 they take a quarter.

| | after b1 | after b1 and b2 | saved against now |
|---|---|---|---|
| no communication | 1 732 | 1 237 | 66% |
| communication | 5 194 | 3 691 | 66% |

Where it changes.
- `encoded_observation_space` (the dtypes of the space) and `encode_view` and the sender copies (the arrays that
  are built) in `local_subgraph_encoding.py`.
- A cast at the top of `GNNEncoder.encode_padded` back to int64 for indexing and to float32 for the masks. Torch
  indexing needs int64.
- The batch builder `_batch` in `training/policy.py` stacks whatever type it gets, so it needs no change.

What has to be checked, because it is not certain.
- That RLlib passes int8 and uint8 through to the module without turning them into float32. If it converts them,
  there is no saving in the batch, and the saving is only in the stored samples.
- The existing tests that compare the one-observation oracle with the batched path, and the replay test, must
  pass unchanged. Results must be bit for bit the same, since only types change.
- A memory probe before and after, with the same rows as the table above.

What it gives for a 2000 step iteration (7 runners, 3 agents, 42 000 rows).

| | now | after b1 | after b1 and b2 |
|---|---|---|---|
| no communication | 152 MB | 73 MB | 52 MB |
| communication | 454 MB | 218 MB | 155 MB |

## Later options, not now

- **Look up what depends only on the vertex.** The window around a vertex, its edge list, its masks and the move
  targets depend on the graph and on which vertex the agent stands on, not on the time step. They could be built
  once per vertex and looked up on the GPU from the agent's vertex. A row would then hold only the vertex features
  that change (about 800 bytes, roughly 78% less than now). It changes the observation and many tests, so it needs
  its own plan. It is the best structural saving.
- **Embed each agent's window once.** With communication each receiver carries its senders' windows, so the same
  window is embedded again for every receiver that hears it. Sharing the embedding would cut the communication cost
  from about the square of the fleet size to about linear. **Promoted to the main item, designed in
  `embed_once_design.md`.** It needs minibatches of whole timesteps, so it is a training change as well as a memory
  change. Steps a and b above stay as a second layer on top of it.
- **Mixed precision (float16).** Not recommended. The GPU is Turing, which has no bfloat16, so it would be float16
  with loss scaling. The masks hold very negative values and the benefit at width 32 is small. It would also have
  to be applied to every arm to keep the comparison fair.

## Order of work

Second of three pieces, written up before any code. The first is `trace_extension_plan.md`. The third is the leg
tool. When this is implemented it should be one small branch from `main`, with the probe numbers in the pull
request text.
