# Recurrent policy plan (option 3), 2026-10-16

**Status, later on 2026-10-16. On hold, decentralised arm only.** After `[A32]` a centralised agent is never
overridden and sees the earlier agents' choices, so the stand-off this plan answers is a decentralised matter (and the
full-view setting and zone edges). It waits for the greedy diagnostic on the retrained arms. Not tested in the step 0
spike: a stateful RLModule with the turn-based adapter. Each agent acts once per timestep, so its state should step once
per timestep, but this needs checking before any build.

Local note at the workspace root. It describes how to give the learned policies a memory with a GRU or LSTM,
why it is the second step and not the first, and what it would touch. Nothing here is implemented. The first
step, option 2 (two extra signals in the observation), is described in `campaign_findings_2026-10-16.md`
section 11 and is handed to a separate branch.

## The problem it answers

The campaign's greedy evaluation showed that the learned fleets deadlock in head-on stand-offs and only get out by
chance when they sample (`campaign_findings_2026-10-16.md`, section 11). The policy is a function of the current
observation only. Two agents in a stand-off see the same thing every step, and conflict resolution only blocks
them both. A policy with no memory can only randomise.

## What a memory adds over option 2

Option 2 gives the policy "I was overridden last step" and "my priority rank". That is enough to break a
symmetric stand-off if one step of history is enough.

A memory is needed only if the right move depends on more than the last step. Examples.
- Backing out of an aisle takes several steps, and after the first step back the "overridden" flag is gone.
- Telling "blocked for 1 step" from "blocked for 8 steps".
- Not entering a corridor that blocked the agent a moment ago.

A recurrent cell does not break the symmetry by itself. Two agents with the same weights and the same inputs still
behave the same. So it needs the option 2 signals as inputs, and option 3 builds on option 2.

## Two ways to get memory

### 3a. A recurrent cell after the readout (the GRU)

Where it goes. The encoder produces the readout z_i. A GRU takes z_i and the previous hidden state and returns
z_i'. The policy head and the value head read z_i' where they read z_i now. The width of z_i' equals the width of
z_i, so the per-edge move score (`eq:edgescore`) keeps its input size. Messages stay the senders' own final-layer
embeddings and are not recurrent, which keeps the communication part as it is.

Why a GRU and not an LSTM. It has one state tensor instead of two and fewer parameters. At width 32 either is
tiny. The choice is open and should be one sentence in the thesis.

What RLlib needs. The module becomes stateful.
- `get_initial_state()` returns the starting hidden state (a dict of tensors) and `is_stateful()` follows from it.
- The forward passes read `Columns.STATE_IN` and return `Columns.STATE_OUT`.
- For training, RLlib's `AddStatesFromEpisodesToBatch` learner connector cuts each episode into chunks of at most
  `max_seq_len` steps, zero-pads them, and sets the state at the start of each chunk from the episode. So the
  module receives batches shaped (B, T, ...) and must handle the time axis. `max_seq_len` is a model setting
  (for example 20 to 32 steps, TBD).
- The module classes to change are `GNNPPOTorchRLModule` and the shared encoder wrapper in `models/rl_module.py`,
  and the forward of `ActionMaskingTorchRLModule` in `environment/action_masking.py`, which wraps them.

Parts of this repo that assume no state.
- `ModulePolicy` (`training/policy.py`) builds a batch per step and calls the module once for all robots. It would
  keep a hidden state per robot, reset it from `get_initial_state()` in `reset()`, pass it in, and store the
  output. Sampling and greedy both stay as they are.
- `compute_values` in `action_masking.py` chunks by rows (`VALUE_CHUNK_ROWS`). A recurrent value pass has to chunk
  by whole sequences, since a row depends on the rows before it.
- The encoder runs the graph network over every row, then the cell over time. The graph part stays parallel. Only
  the cell runs along the time axis, so the cost is small.
- Whether `minibatch_size` counts rows or sequences once the module is stateful has to be checked in RLlib before
  the settings (minibatch 128, 5 epochs) are reused.
- The thesis requires that the critic sees the same window as its policy. The critic's z_i' comes from the same
  recurrent state, so that holds.

Memory cost. Rows are unchanged in number. The extra is the hidden state per row (width 32) and the gradients through
`max_seq_len` steps. It is small next to the observation rows (`memory_reduction_plan.md`).

### 3b. A short history as input (no recurrence)

A cheaper middle step. Add to each robot's own information the last k steps of a few small numbers, such as whether
it moved, whether it was overridden and which slot it chose. The policy stays feedforward. No RLlib sequence
machinery, no state handling in the policy runner, no change to the value pass.

- It gives "blocked for several steps" and "what I just tried".
- It does not give a learned summary of a long past.
- k would be small (3 to 8, TBD), set by what the stand-offs need.

Recommended order if option 2 is not enough: try 3b first, since it costs a fraction of 3a.

## What it changes in the thesis

- The encoder family gets a recurrent block (3a) or a longer own-information vector (3b), in all three arms alike.
  `tab:modelparams` gets a row for the cell width and `max_seq_len`, or for k.
- The observation function `O_i` or the model section says the policy has a state. The statement that a policy is a
  function of the current observation would change.
- The three arms still differ only in their window, as long as the block is the same in all three.
- A log entry `[Axx]` in `thesis-progress/decisions/GAPS.md` with the reason, as for the other model changes. Wording is
  proposed in chat first. The thesis is not edited from here.

## Tests and the measure of success

- The stepwise forward of one robot and the sequence forward over the same steps give the same outputs (the
  recurrent version of the existing test that compares the oracle with the batched path).
- Replay under a fixed seed is bit for bit, with the hidden state reset at every episode start.
- The hidden state of one robot does not leak into another, and does not carry from one episode to the next.
- Success is the greedy evaluation. The greedy fleet should keep up about as well as the sampled fleet and should
  show no episode with a long stalled stretch. This is the same test that exposed the problem.

## When to do it

A staged comparison on the same seeds and loads, with at least 3 training seeds each.
- A, today's policy.
- B, option 2 (the two signals).
- C, B plus 3b or 3a.

Do C only if B still deadlocks under greedy evaluation or still loses to sampled evaluation by a wide margin.
Doing B and C together would not show which one helped.

## Effort, roughly

3b is about the size of option 2 plus a history buffer in the environment adapter. 3a is several times larger. It
touches the module, the masking wrapper, the policy runner, the value pass and the tests, and it needs the RLlib
sequence settings checked. These are guesses and not measured.
