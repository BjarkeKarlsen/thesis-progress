# B3. Pooling in the readout [review]

Branch `fix/l4-pooling`, started from the branch of B2 (`fix/l4-window`), because both edit
`models/local_subgraph_encoding.py`. Read `00_rules.md` first.

## Goal

Add the pooled embedding the thesis leaves TBD, as decided by the author on 2026-10-13. Without it a robot's embedding
reflects only the vertices within `L` rounds, so a window larger than that adds nothing. Each arm pools over its
own space.
- Centralised pools over the whole graph.
- Section-based pools over its zone only, not the halo.
- Decentralised does not pool.
Pooling is the masked mean of the final-layer embeddings, over real vertices only, never over padding.

## Thesis to read

`sec:method:model` (the readout, and the paragraph on the two open points), `tab:modelparams` (row "global pooling",
TBD). The thesis edit to the readout and the table is the author's. Do not edit `thesis/`.

## Changes

1. `models/gnn_encoder.py`. `GNNEncoderConfig` gets `pooling: Literal["none", "mean"]` with no default. When `"mean"`,
   the readout is the robot's own embedding, then the message aggregate if communication is on, then the pooled
   mean, then the congestion value last. Update `output_dim`. Apply the same change to the unbatched path used as the
   test oracle (`forward`).
2. `models/local_subgraph_encoding.py`. A fixed-shape `pool_mask [N]` float32 key in `encoded_observation_space`,
   `EncodedObservation`, `as_rllib_dict` and `encode_all_observations`, present only when pooling is on (the same
   pattern as the sender keys). 1.0 for vertices to pool over, 0.0 for halo and padding. A new optional argument to
   `encode_all_observations` gives each robot's pool vertices. The default is the robot's whole window.
   `encoded_observation_space` gains a `pooling` argument.
3. `models/base_model.py` and `models/rl_module.py`. The head input width follows `encoder.output_dim`. Confirm that the
   RLlib module passes `pool_mask` through to the encoder, and that `DecentralisedController._batch` stacks the new key
   with no change. Add a test that proves the second.
4. A pooled term is for the receiver's own view only. Sender blocks need no pooled term.
5. Docstrings name the readout by name, not by label.

## Tests

- The mean ignores padding and zero-mask vertices, checked with a hand-computed value.
- `pooling="none"` gives today's readout and no `pool_mask` key.
- A loss on the logits reaches the encoder through the pooled term.
- The padded logits equal the unbatched oracle with pooling on and off, with communication on and off, at `L = 0` and
  `L > 0`.
- The observation space matches the arrays with pooling on and off.
- One PPO iteration through `build_ppo_config` with pooling on. Write the test, do not run it.

## Flag in the hand back

The place of the pooled term in the readout (the thesis does not fix it), and that the merged move score head input
widens.
