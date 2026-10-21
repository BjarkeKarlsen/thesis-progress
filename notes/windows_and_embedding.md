# Windows, embeddings and how a training row is stored

A plain description of what a robot sees, how the network turns that into a
decision, and how a training sample is stored. Written 2026-10-20, after the
memory work R1 to R4 of `../decisions/active/memory_reduction_plan.md`. The code
is in `slap-mapd-coupling` on the branch `feat/row-lookup` (worktree
`~/worktrees/feat-row-lookup`), stacked on `feat/putaway` (#188). Nothing here
changes the model in the thesis. Every change is in how the same numbers are
stored and computed.

## What a robot sees, its window

Every robot decides from a window, a set of vertices around it. The window
depends on the arm.
- *Decentralised.* The field of view, every vertex within distance `d_obs` of
  the robot.
- *Centralised* and the *full-view setting.* Every vertex a robot can stand on.
- *Section-based.* The zone the robot stands in, plus a halo of `d_obs` around
  it.

So the window is fixed by the vertex the robot stands on. Two robots on the
same vertex in the same arm always see the same set of vertices, in the same
order.

Each vertex in the window carries eight numbers.
- Five say what the vertex is. Shelf, delivery point, parking spot, plain aisle,
  receiving point. These never change.
- Three change with time. `eta`, the distance from that vertex to the robot's
  target. `occupied`, whether another robot stands there. `claimed`, whether an
  earlier agent of the same decision has already chosen it (centralised and
  section arms only).

The network needs fixed sizes, so every window is padded to the largest window
of the arm (`max_local_nodes`) and comes with masks that say which entries are
real.

## How the network embeds a window

The encoder is a small graph network. Each vertex starts from its eight
numbers. In each round, every vertex averages what it hears from its
neighbours in the window and updates its own vector. After the last round every
vertex has an embedding that also reflects its surroundings.

The robot's own embedding is the vector at the vertex it stands on. The
readout `z` puts together the own embedding, the mean of the messages it hears
(with communication on), a pooled mean over the window (centralised and section
arms), and the congestion feature. The value comes from `z`. A move is scored
from `z`, the embedding of the vertex the move leads to and, with
communication on, the message of the robot standing there.

A message is the sender's own embedding, sent as it is. A robot hears every
robot within `d_obs`, closest first, up to `max_messages` (by default the fleet
size minus one, so nobody is dropped).

## Why memory ran out

PPO stores one row per robot per timestep. One iteration at horizon 2000 with
7 runners is 14 000 times the fleet size rows, 448 000 rows at 32 agents.
RLlib turns that whole batch into tensors on the GPU before it cuts minibatches,
so the batch has to fit in 8 GB.

Before this work a row held the whole padded window. The edge list, the masks,
the move targets and the five fixed flags were copied into every row, although
they depend only on the vertex. For the centralised arm the window is the whole
warehouse, so every row carried the whole warehouse again. With communication
a row also carried a full copy of each sender's window, one per sender slot,
and the slots are padded to the fleet size.

The network then embedded every one of those sender copies again, once per
receiver that hears it.

## What changed

### R1, the window tables

Everything that depends only on the vertex is built once per run in tables
(`models/window_tables.py`).
- Per window. The vertex mask, the edge list, the edge mask, the pool mask and
  the five fixed flags of its vertices. The centralised arm has one window, the
  section arm one per zone, the decentralised arm one per vertex.
- Per vertex. Which window it uses, its own position in that window, and the
  window position of the vertex each move leads to.

A row now stores only the vertex the robot stands on (as a table position), the
three changing features, the congestion feature and the action mask. The module
rebuilds the full padded window from the tables on the GPU before the encoder
runs, so the encoder sees exactly what it saw before. The tables travel in the
module's model config, so a checkpoint carries them. They are not part of the
weights.

### R2, smaller number types

`occupied` and `claimed` are 0 or 1 and are stored as one byte each. `eta`
stays a 32-bit float, so nothing is rounded.

### R4, embed each window once (communication)

A message is the sender's own embedding, and the sender's own row already
holds everything that embedding needs. So a row no longer copies its senders'
windows. It holds its own key and the keys of its senders' rows. A key packs
the runner, the episode, the timestep and the robot, so it is unique in a batch.
A padded sender slot has key -1.

The encoder embeds each row once and finds each sender's embedding by key
(`GNNEncoder.encode_keyed`). Where the sender rows come from depends on when the
network runs.
- *Choosing actions.* All robots of a timestep are in the same call, so every
  sender is there.
- *The value pass.* It runs on the whole iteration. The module first embeds
  every row once into a table of keys and embeddings, then computes the values
  chunk by chunk, reading messages from that table.
- *A training minibatch.* PPO cuts the batch by row, so a sender can be in
  another minibatch. The learner (`training/learner.py`) looks up the rows of
  those senders in the whole batch and adds them to the minibatch as context
  rows. They are embedded with the current weights, so the receiver's loss
  still reaches the sender's window through the shared weights, but they carry
  no loss of their own.

So the minibatches, the loss and the gradients are what they were. Only the
repeated copies and the repeated embedding of the same window are gone. The
timestep-block minibatches of `../decisions/active/embed_once_design.md` were
not needed, so none of its three author decisions came up.

### R3, the batch in host memory

With `slap-mapd train --batch-on-cpu` the batch is built in RAM instead of on
the GPU. The value pass moves one chunk at a time to the GPU, and each
minibatch is moved to the GPU before its update. It is off by default.
`--value-chunk-rows` sets the rows per encoder pass of the value pass (512 by
default). Neither changes a result.

## The numbers

Stored data per iteration, measured from the observation spaces of the fleet
configs (7 runners, horizon 2000).

| fleet | arm | before | after R1 and R2 | after R4 |
|---|---|---|---|---|
| 8 | decentralised | 0.77 GB | 0.04 GB | |
| 8 | decentralised, communication | 6.15 GB | 0.34 GB | 0.06 GB |
| 8 | centralised | 1.32 GB | 0.07 GB | |
| 16 | decentralised, communication | 24.6 GB | 1.33 GB | 0.13 GB |
| 16 | centralised | 6.09 GB | 0.31 GB | |
| 32 | decentralised | 3.20 GB | 0.18 GB | |
| 32 | decentralised, communication | 101.7 GB | 5.45 GB | 0.31 GB |
| 32 | section | 19.4 GB | 0.98 GB | |
| 32 | centralised | 25.4 GB | 1.28 GB | |

The tables themselves are at most 3 MB.

GPU memory of the network with communication at 32 agents. A training
minibatch of 128 rows used about 2 GB before (16 MiB a row). After R4 it is
83 MiB, and 326 MiB with 512 context rows. A 512-row chunk of the value pass ran
out of memory before and takes 168 MiB now.

## How it was checked

- For every arm, with and without communication, the rows rebuilt from the
  tables equal the old padded rows bit for bit, over whole episodes.
- The module gives the same logits and values on the new rows as on the old
  ones (`tests/unit/test_window_tables.py`).
- A minibatch that cuts a timestep, with its context rows, gives the same
  readout and the same gradients as the old path. The chunked value pass gives
  the same values for chunk sizes that cut a timestep. A missing sender row
  raises instead of training on a zero message (`tests/unit/test_learner.py`).
- Short GPU training runs, with and without communication and with the batch in
  host memory, and a checkpoint that loads and plays through
  `slap-mapd evaluate`.

## What is left

- Old checkpoints do not load, since the rows changed. Every run is retrained
  anyway.
- Fixed on the same branch. The adapter now builds only what the compact row
  needs (`encode_all_observations(..., padded=False)`), and skips the window
  arrays, the pool mask and the senders' views. An episode on the small test
  instances is now faster than before this work, not slower. The full build
  stays as the reference the tests compare against.
- Fixed on the same branch. Two adapter tests read the claimed flag at column
  -1, which #188 made the receiving column. They now read column 6.
- Fixed on `fix/fleet64-instance` (`~/worktrees/fix-fleet64-instance`, from
  `feat/fleet-load-sweeps`). The 64-agent configs generate a warehouse with
  `max_num_cross_aisles` 28 instead of 20 (883 vertices, 34 topology attempts).
  Random role placement had to keep the aisles strongly connected with 160 role
  vertices, which almost never held with fewer cross-aisles. With 28
  cross-aisles on aisles of length 28 the warehouse is closer to an open grid
  than the 8 to 32-agent ones.
