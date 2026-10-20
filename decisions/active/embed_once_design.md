# Embed each agent's window once, design, 2026-10-16

**Status, later on 2026-10-16. Do now** (author's decision), as Track B of `ROADMAP.md`, in parallel with reading the
first result. With 8 agents a robot hears up to 7 senders, so a communication row is about 8 times a plain row. The
row keys must live with the turn-based adapter of #164. Communication runs with one turn only, so the decentralised arm
is the only one touched.

Local note, written before any code. It promotes the "Embed each agent's window once" option of
`memory_reduction_plan.md` from a later option to the main item, and works out the one hard part, how
training batches it. Nothing here is implemented. Issue 91 (closed) asked for exactly this ("all agents of a
timestep share one forward pass"). The implementation took a shortcut, and this note replaces the shortcut.

## Why

With communication on, each robot's row carries a full copy of the window of every sender it hears (the
`sender_*` keys, `local_subgraph_encoding.py:178`). The encoder then embeds the receivers and the B times M
sender copies in one pass (`gnn_encoder.py:373`). A message is the sender's own embedding, so the copy of a
window that a receiver embeds is a window that the sender's own row has already embedded. The same vector is
computed 1 + M times.

CRAMP embeds each agent's field of view once and lets the ego agent gather its neighbours' vectors. The thesis
text already says the message is the sender's embedding sent as it is (`[A27]`). Inference already makes one
module call per step for all robots (`training/policy.py:29`). Only training and storage still copy.

## What it saves

| | now | after embed-once | after embed-once, b1 and b2 of the plan |
|---|---|---|---|
| stored bytes per row, communication | 10 808 | 3 632 | 1 261 |
| one 2000 step iteration, 42 000 rows | 454 MB | 153 MB | 53 MB |
| encoder peak per row | 0.55 MiB | about 0.18 MiB | about 0.18 MiB, smaller after b |

The 3 632 is the 3 608 of a row without communication plus 24 bytes of keys (one row key, two sender keys, int64
each, at most 2 senders). The encoder figure is the measured no-communication figure, because the sender
passes disappear. The multiplier today is 1 + `max_messages`, so it grows with that cap too. These are
estimates from the plan's numbers and must be confirmed with the probe.

## The design

### 1. What a row holds

The `sender_*` window keys leave the observation. Two keys are added.

- `row_key`, int64 [1]. It identifies the row by timestep and robot, and is unique across runners and episodes.
- `sender_row_key`, int64 [M]. The `row_key` of each sender the robot hears, -1 for a padded slot.

A packing that fits int64 with room to spare is runner (10 bits), episode count of that env (20 bits), step
(20 bits) and robot id (8 bits). The exact packing is an implementation detail. `move_sender_index` and
`move_sender_mask` stay as they are, since they index the M sender slots, and the slots keep their meaning.

Who may talk to whom is decided in the adapter exactly as now (`max_messages` closest senders by d_G, ties by
id). Only what is stored about a sender changes, from its window to its key.

### 2. The encoder

`encode_padded` splits into two parts.

- Part one embeds the rows' own windows, `h^(L)` at each row's own vertex. This is the expensive part and runs
  once per row. The result is the row's own embedding, [B, D].
- Part two is the readout. It looks up each row's senders by `sender_row_key` among the rows' keys, takes their
  own embeddings as the messages [B, M, D], masks the padded slots, averages, and builds `z`. The output keeps
  today's shape, so `PolicyValueHead`, the move score and `move_sender_index` do not change.

The lookup is a sort of the batch's `row_key` and a `torch.searchsorted` of the sender keys. A sender key that is
not found is an error, not a zero message. That check is what makes a broken minibatch fail loudly instead of
silently training on a wrong message.

The gradient is the same as today. The receiver's loss reaches the sender's embedding, and so the weights,
through the sender's row. It is summed once per row instead of once per copy.

### 3. The value pass (GAE)

RLlib's GAE connector calls `compute_values` once on the whole train batch, with the rows ordered by episode
(one episode per robot), so a sender's row is far from its receiver's. The chunking of `compute_values`
(`action_masking.py:171`) cannot cut by position any more.

Because the value reads only `z`, it can run in two passes without gradients.

- Pass one, in chunks of any size, computes each row's own embedding. Only the [rows, D] result is kept. At
  D = 32 and 42 000 rows that is about 5 MB.
- Pass two gathers each row's senders from that table by key and applies the value head.

So the value pass stays chunked and no longer needs sender windows. The result must equal the unchunked value
of the same rows.

### 4. Minibatches of whole timesteps (the hard part)

The loss needs a robot's senders in the same minibatch. PPO's minibatches are row slices of the batch,
reshuffled by row after the first epoch (`ppo.py:133`, `shuffle_batch_per_epoch=True`), so they cut timesteps.

The fix is a minibatch iterator that works on timestep blocks.

- A block is all the rows of one timestep. Every robot is in every timestep, because no robot terminates before
  the others and all are truncated together at the horizon (`multi_agent_env.py:359`). So a block always has all
  A rows, and every sender of a row is in its block.
- Each epoch the blocks are shuffled and cut into minibatches of `minibatch_size // A` blocks.
- Where to hook it. `Learner._create_iterator_if_necessary` builds the iterator. A small `PPOTorchLearner`
  subclass overrides it to return the block iterator, and `config.learners(learner_class=...)` selects it. This
  is one method, not a copy of the update loop.

Consequences to accept.

- A minibatch holds `A * (minibatch_size // A)` rows. With 3 robots and 128 that is 126, not 128.
- Rows in a minibatch come in groups of A from the same timestep, so they are more correlated than 128 random
  rows. With 3 robots that is small. With a large fleet and a small `minibatch_size` it is not, and the setting
  is then really a number of timesteps. This couples the setting to the fleet size, which is worth a line in the
  chapter's training table if it is adopted.
- The shuffle is by block and seeded, so a training run stays reproducible. It is not part of the replay
  invariant, which is about the simulator.

### 5. Evaluation

`ModulePolicy` already builds one batch for all robots of the step, so every sender is in the batch. It needs
the two keys and nothing else. The batch of a step holds only A rows, so the lookup is trivial there.

## Which arms

Only the decentralised arm with communication has senders. The centralised and section arms have no sender keys
and keep RLlib's default minibatching.

Open for the author (see the end): whether the decentralised arm without communication also uses the block
iterator. The comparison that RQ5 needs clean is decentralised with against without communication. If only one of
them uses blocks, the difference between them is partly a difference in training, not only in communication.
My recommendation is that both use it.

## Considered and rejected

| Option | Why not |
|---|---|
| One RLlib agent for the whole fleet (a row per timestep) | The action probability ratio and the advantage become joint. The decentralised arm learns from each robot's own reward (`credit_signal` `per_agent`), so this changes the objective. |
| Store the sender's embedding in the sample | It is out of date after the first update of an iteration, and needs RLlib connectors. The L2 design rejected it for the same reason. |
| Detach the sender embedding, embed it from a lookup | The receiver's loss would no longer reach the sender, which breaks "trained end to end" in `[A27]`. |
| Make `minibatch_size` a multiple of A and keep RLlib's iterator | RLlib reshuffles rows after the first epoch, so it still cuts timesteps. |

## What has to stay true, and the tests

- **Same numbers as today.** On the same rows, the new encoder must give the same `z` and messages as the old
  one with sender windows. Exact on CPU, to float tolerance on GPU, since `index_add_` order can differ with the
  batch. Keep the old path in one test until the new one matches, then remove it. The tests that touch it are
  in `test_gnn_encoder.py`, `test_base_model.py`, `test_local_subgraph_encoding.py` and `test_rl_module.py`. The
  one-observation oracle (`forward` with `senders`) is unchanged and stays the reference.
- **Chunking changes nothing.** The two-pass value of the whole batch equals the single-pass value, for several
  chunk sizes, including one that cuts a timestep.
- **Blocks are whole.** In every minibatch the iterator yields, every non-padded `sender_row_key` is found, and
  each epoch covers each row once.
- **Gradient matches.** The gradient of a loss through the new path equals the gradient through the old path for
  a minibatch of whole timesteps.
- **Replay and the four invariants** are untouched, because the simulator does not change. Only what the
  adapter writes into the observation changes.
- **Probe.** The same memory probe as in the plan, before and after, with the rows of the plan's table.

## Not yet checked

- That a `Learner` subclass given through `config.learners(learner_class=...)` works with the one local learner
  this project uses, and that `row_key` survives the learner connector pipeline as an untouched int64 column.
  A short probe settles both, and it comes first.
- That nothing else reads the `sender_*` window keys, for example `viz/` or an evaluation script. A search of
  `src` found them only in the model files and the encoding, but `viz/` and `evaluation/` were not read.
- Whether CRAMP computes the neighbours' vectors once per step or once per ego agent. The paper says the ego's
  node matrix is built from "encoded feature vectors" of agents in its field of view, which is the shared
  structure, but it does not say how its code batches them. The thesis claim should be "as in CRAMP's structure",
  not "as in CRAMP's implementation".

## Decisions for the author

1. Does the decentralised arm without communication also use the block iterator? Recommended yes, so RQ5's
   comparison differs only in communication. Tracked as issue 160. Under the real centralised and section-based design
   (`real_centralised_design.md`), only the decentralised arm has senders.
2. Is it acceptable that `minibatch_size` becomes a number of timesteps times the fleet size (126 instead of 128
   with 3 robots)? The alternative is to leave RLlib's iterator and give up embed-once.
3. Does this need a thesis edit? The chapters already say the message is the sender's embedding, so the model is
   unchanged. If the minibatch rule goes into the training table of `4.Implementation.tex`, it is an `[Axx]`
   entry in `thesis-progress/decisions/GAPS.md`.

## Order of work

1. The probe of the section "Not yet checked", no commit.
2. One branch from `main`, in this order. The keys and the adapter. The two part encoder and the equality test
   against the old path. The two pass value. The block iterator and its learner. Remove the old sender windows
   last. A PR text with the probe numbers.
3. Steps a and b of the memory plan after that, on top. They are independent and stack.
