# Memory reduction plan, rewritten 2026-10-20

**Status, later on 2026-10-20. R1 to R4 are implemented**, uncommitted on `feat/row-lookup`
(`~/worktrees/feat-row-lookup`), stacked on `feat/putaway` (#188). R4 was built without the
timestep-block minibatches. The learner adds the senders' rows to each minibatch instead,
so PPO's minibatches are unchanged. How it works and the measured numbers are in
`../../notes/windows_and_embedding.md`. The sections below are the plan as written.

Local note. It says where the memory of a training run goes on current code, what was measured, and what to change,
in order. Nothing here is implemented. It replaces the plan of 2026-10-16, whose numbers came from the 3-agent
campaign instance with 6 vertex features and are out of date. `embed_once_design.md` is now step R4 of this plan.

Code is in `slap-mapd-coupling/src/slap_mapd_coupling/models/` (`local_subgraph_encoding.py`, `gnn_encoder.py`,
`rl_module.py`), `environment/action_masking.py` and `training/arm.py`.

## Where it stands

Memory limits RQ4. From 16 agents on, the centralised and section arms do not fit on the GPU, and at 32 agents they
do not fit in RAM either. Communication does not fit at any fleet size. The decentralised arm without communication
fits everywhere measured.

The GPU is an RTX 2070 Super with 8 GB, about 6.7 GB free (other processes hold about 1.4 GB). The machine has 31 GB
of RAM.

RLlib's learner connector is built with the learner's device (`learner.py:341`, Ray 2.57), so the whole train batch
of an iteration is turned into tensors on the GPU before it is cut into minibatches. The stored batch therefore has
to fit on the GPU, not only the minibatch.

## What was measured, 2026-10-20

Probe script `memprobe.py` in the session scratchpad, run on the code of `main` plus the fleet configs of
`feat/fleet-load-sweeps`. Observation spaces are built from the configs `configs/fleet_{8,16,32}/*.yaml`. One iteration
is 7 runners times horizon 2000 timesteps, one row per agent per timestep, so rows = 14 000 times the fleet size. The
centralised arm has one row per agent turn, which is the same count.

| fleet | arm | communication | movable vertices | window cap N | bytes per row | GB per iteration |
|---|---|---|---|---|---|---|
| 8 | decentralised | no | 98 | 59 | 6 908 | 0.77 |
| 8 | decentralised | yes, 7 senders | 98 | 59 | 54 948 | 6.15 |
| 8 | section | no | 98 | 98 | 11 824 | 1.32 |
| 8 | centralised | no | 98 | 98 | 11 824 | 1.32 |
| 16 | decentralised | no | 226 | 59 | 6 908 | 1.55 |
| 16 | decentralised | yes, 15 senders | 226 | 59 | 109 796 | 24.6 |
| 16 | section | no | 226 | 203 | 24 424 | 5.47 |
| 16 | centralised | no | 226 | 226 | 27 184 | 6.09 |
| 32 | decentralised | no | 472 | 61 | 7 140 | 3.20 |
| 32 | decentralised | yes, 31 senders | 472 | 61 | 226 916 | 101.7 |
| 32 | section | no | 472 | 360 | 43 264 | 19.4 |
| 32 | centralised | no | 472 | 472 | 56 704 | 25.4 |

The 64-agent configs did not build. `generate_instance` raised `InstanceGenerationError` at seed 42 ("none of 100
sampled topologies admitted a well-formed role assignment").

Why the centralised and section rows are large. Their window is every movable vertex, or a zone with its halo, and
the cap N is set to the largest window (`training/arm.py`). The whole window is stored in every row. The edge list is
53 to 55% of a row in every arm, and for the centralised arm it is the same in every row of every episode.

The GNN pass itself is not what limits. Peak extra GPU memory of the encoder, in MiB per row.

| fleet | arm | value pass, 512 rows, no gradients | training minibatch, 128 rows, with gradients |
|---|---|---|---|
| 8 | decentralised | 0.34 | 0.55 |
| 8 | centralised | 0.54 | 0.81 |
| 16 | centralised | 1.23 | 1.87 |
| 32 | decentralised | 0.33 | 0.52 |
| 32 | section | 1.95 | 3.02 |
| 32 | centralised | 2.56 | 3.94 |
| 32 | decentralised, communication | out of memory | 16.1 |

At 32 agents one chunk of the centralised value pass is about 1.3 GB, and one minibatch about 0.5 GB.

## What a row holds, and what depends on the time step

A row of every arm holds the window's vertex features, its masks, its edge list, the move targets, the agent's own
index, the congestion feature and the action mask, and the pool mask for the arms that pool. Only part of this changes
with time.

| part | depends on |
|---|---|
| edge list, edge mask, vertex mask | the window only |
| pool mask | the window only |
| move targets, own index | the agent's vertex |
| the role flags (storage, delivery, endpoint, transit, receiving), 5 of the 8 vertex features | the vertex only |
| occupied, claimed, eta, 3 of the 8 vertex features | the time step (and the turn, for claimed) |
| congestion, action mask | the time step |

The window of a row is fixed by the agent's vertex in every arm. It is the field of view of that vertex for the
decentralised arm, the zone of that vertex with its halo for the section arm, and every movable vertex for the
centralised arm. The vertex order inside a window is fixed too, since `local_subgraph` and the arm windows depend on
the graph and the vertex only. So one key per row, the agent's vertex, recovers everything in the first four lines.

## What to change, in order

### R1. Store what depends only on the vertex once, and look it up

The row keeps the agent's vertex, the 3 time-dependent vertex features, the congestion feature and the action mask.
Everything else moves into tables built once per run from the graph and the arm. The module looks the tables up on the
GPU and rebuilds the tensors `encode_padded` takes today, so the encoder does not change.

- The tables. Per window, the edge list, the edge mask, the vertex mask, the pool mask and the role flags of its
  vertices. Per vertex, its window number, its own index in that window and its move targets. The centralised arm has
  one window, the section arm one per zone, the decentralised arm one per movable vertex. At 32 agents the
  decentralised tables are about 2 MB.
- Where the tables live. Registered buffers of the RL module, built from the graph and the arm when the module is
  built, so a checkpoint carries them. How they reach the module (the model config or a rebuild from the graph) is
  decided in the branch.
- Where it changes. `encoded_observation_space` and `encode_view` in `local_subgraph_encoding.py` (what is stored),
  the start of the forward in `rl_module.py:50` to `rl_module.py:70` (the lookup), and the table builder next to
  `arm_windows`. `encode_padded` and `PolicyValueHead` keep their arguments.
- It changes no number. The rebuilt tensors are the ones stored today, so results are bit for bit the same. The model
  and the thesis do not change.

### R2. Smaller types for what is left

`occupied` and `claimed` are 0 or 1 and go to uint8. `eta` stays float32, so the results stay bit for bit the same.
The module casts back at the lookup. The action mask stays as RLlib's masking expects it.

Estimated batch per iteration after R1 and after R1 with R2, in GB.

| fleet | arm | now | after R1 | after R1 and R2 |
|---|---|---|---|---|
| 8 | decentralised | 0.77 | 0.09 | 0.05 |
| 8 | centralised | 1.32 | 0.14 | 0.07 |
| 16 | section | 5.47 | 0.56 | 0.29 |
| 16 | centralised | 6.09 | 0.62 | 0.32 |
| 32 | decentralised | 3.20 | 0.34 | 0.18 |
| 32 | section | 19.4 | 1.97 | 1.00 |
| 32 | centralised | 25.4 | 2.55 | 1.30 |

These are computed from the shapes, not measured. A row after R1 is about 12 N bytes plus 32, and about 6 N plus 32
after R2. The probe is run again on the branch.

At 64 agents the warehouse has perhaps 1 000 movable vertices and the batch twice the rows, so the centralised arm
would be about 5 to 6 GB after R1 and R2. That is near the free GPU memory, which is why R3 follows.

### R3. Keep the batch in RAM, move one minibatch at a time to the GPU

Only if R1 and R2 are not enough, which is likely for the centralised arm at 64 agents. The learner connector then
builds the batch on the CPU, and the iterator moves each minibatch and each value-pass chunk to the GPU. The hook is
the same as embed-once's (`Learner._create_iterator_if_necessary`, through `config.learners(learner_class=...)`), so R3
and R4 share one learner subclass. To be probed first. Whether the GAE connector's value pass can run on CPU tensors
moved chunk by chunk.

Lower the value-pass chunk size with it. `VALUE_CHUNK_ROWS = 512` in `environment/action_masking.py` becomes a setting
next to the PPO settings, with 512 as the default. At 64 agents one centralised chunk of 512 rows would be several GB.

### R4. Embed-once, for RQ5 only

`embed_once_design.md`. After R1 a sender needs only its own row's key, not a copy of its window, and its message is
looked up from the embedding of its own row. That is what makes the communication column fit (about 1 KB per row at
32 agents instead of 227 KB). It needs minibatches of whole timesteps, a training change, so it stays a separate branch
and waits until RQ5 is confirmed.

## Not recommended

- Mixed precision (float16). The GPU is Turing, without bfloat16, so it would be float16 with loss scaling. The masks
  hold very negative values, it changes numbers, and it would have to apply to every arm.
- Storing `eta` as float16. It halves what is left after R2 but is no longer bit for bit, and R1 with R2 is enough up
  to 32 agents.

## Another limit at 32 and 64 agents, not memory

An iteration at 32 agents is 448 000 rows. With 5 epochs and minibatches of 128 that is about 17 500 gradient steps
per iteration. Training time may limit RQ4 before memory does. `thesis_plan.md` already says to time one iteration of
each arm at 32 and 64 before committing. Whether the minibatch size or the number of runners scales with the fleet is
a training-table decision, not part of this plan.

## Tests

- The lookup rebuilds the same tensors. For every arm, the rebuilt dense observation equals the one `encode_view`
  builds today, on a few episodes of the 8-agent warehouse.
- The existing oracle tests (`test_gnn_encoder.py`, `test_base_model.py`, `test_rl_module.py`,
  `test_local_subgraph_encoding.py`, `test_policy.py`, `test_training_env.py`) pass, with only the stored layout
  changed in them.
- A short training run gives the same losses before and after, at a fixed seed on CPU.
- Replay and the four invariants are untouched, since the simulator does not change.
- The probe before and after, with the numbers in the pull request text.

## Order of work

1. R1 and R2 as one branch from `main`. Needed before any training at 16 agents or more.
2. Time one iteration of each arm at 16 and 32 with R1 and R2, which also gives the real GPU peak.
3. R3 and the chunk-size setting, if step 2 or the 64-agent warehouse needs it.
4. R4 when RQ5 is confirmed.
5. Separately, the 64-agent configs do not generate an instance at seed 42. That belongs to the warehouse generation of
   RQ4, not to this plan.
