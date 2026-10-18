# What a message should contain

Status: **decided and applied, option 4 (learned embeddings)**, tag `[A14]`
in the chapters and `thesis-progress/temp/GAPS.md`. The analysis below is
kept as the record of why. Still to do: `slap-mapd-coupling` code.

## Where things stand

`4.Implementation.tex` (`sec:method:rl`) fixes the message from `a_j` to
`a_i` as a hand-picked pair,

    (d_G(l_i(t), l_j(t)),  eta_j(l_j(t), t))

that is, how far away the sender is and how close it is to its own
target. The receiver aggregates the incoming messages (`AGG` in
`eq:readout`) and concatenates them into `z_i`.

**What it cannot tell the receiver:** which direction the sender is
heading. So the receiver cannot tell whether their routes will cross,
which is exactly what RQ5 asks about (does communication help more when
hop-adjacency does not predict route overlap).

## The options

| Option | Content | Chosen by | Keeps `O_i` a function of the state? |
|---|---|---|---|
| 1. Current | distance to sender, sender's distance to its target | designer | yes |
| 2. Richer hand-picked | option 1 plus the sender's target `q_j(t)` and/or its preferred next vertex (next step on its shortest path) | designer | yes, but needs a tie-break for the next vertex |
| 3. Actual intent | the move the sender has chosen this timestep | sender's policy | no, needs a propose-then-act round, and actions are chosen simultaneously |
| 4. **Learned embedding** | a vector the sender computes from its own observation, trained end to end | network | no, see the formulation change below |

What the two closest papers do (both in `thesis-progress/papers/`):

- **CRAMP** (`2309.10275`, Pham and Bera). Each agent's CNN encodes its
  observation into a feature vector. A GNN over the agents, with edge
  weights from inter-agent distances, mixes those vectors between agents
  within the field of view. The message *is* the learned embedding.
- **PICO** (`2202.03634`). The agent network has a separate "message"
  output head, `e_m = I^e_theta(o_m)`, computed from the agent's own
  observation. Messages are gathered by a cluster's central agent (chosen
  by learned priority) and broadcast back. Trained through the policy
  loss. The paper visualises messages with t-SNE because they are not
  directly readable.

## Why learned embeddings (option 4) look better

1. **The network decides what is worth sharing.** With options 1 and 2
   the designer guesses what matters (distance? target? next step?
   crowding?). An embedding computed from the sender's own observation
   already contains its direction to its target (`eta_j` over its field of
   view), its local crowding (`delta_j`) and its surroundings. The receiver
   can learn to use whichever part helps.
2. **It matches the literature this thesis compares against.** CRAMP,
   which `3.Background.tex` cites, learns its messages, and so does PICO
   (in `thesis-progress/papers/`, not yet cited, and not yet in
   `references.bib`). The attention-based SEPAR that `3.Background.tex`
   also discusses shares information implicitly through learned weights.
   A hand-picked payload would make this thesis's communication arm weaker
   than the methods it positions itself against, for reasons unrelated to
   the research question. Adopting option 4 would be a natural point to
   add PICO to the bibliography.
3. **A weak channel gives a weak answer to RQ5.** If communication shows
   no benefit with a two-number message, that says little about
   communication. It may only mean the message was too poor. With a
   learned channel, a null result means something.
4. **It avoids encoding a vertex identity.** Options 2 and 3 have to send
   a target or next vertex, which on a general graph needs a relative
   encoding to generalise across warehouses. An embedding is a fixed-size
   vector by construction.

## What it costs

- **Interpretability.** What a learned message carries cannot be read
  off directly. PICO uses t-SNE plots for this. The thesis would need a
  similar probe, or accept that the channel is a black box.
- **A formulation change.** A learned message depends on `theta`, not
  only on the state. It can no longer be part of the observation `o_i(t)`
  and the observation function `O_i`, which `[A12]` says are
  deterministic functions of `s_t`. The clean way is to say that messages
  are part of the decentralised *policy*, a communication step inside
  `pi_theta` that runs over the communication graph `G^A_t`, rather than
  the fourth piece of the observation. `o_i(t)` would then have three
  pieces (field of view, direction, crowding), and `G^A_t` stays as the
  definition of who can talk to whom.
- **Implementation.** Messages must flow between agents inside one
  forward pass (a GNN over the agents, as in CRAMP). RLlib's multi-agent
  API batches per agent by default, so the decentralised forward pass
  needs all agents of a timestep together, similar to the centralised
  router's pass over the whole graph.
- **The existing ablation note.** `sec:method:model` already says a single
  `L=0` removes structural aggregation and communication together, and
  that two separate round counts would isolate them. With learned
  messages that split becomes more important, so it should be adopted,
  not left as an open refinement.

## The reason to give in the thesis for the chosen model

If option 4 is adopted, the justification is points 1 to 3 above, in one
or two sentences in `sec:method:rl`, roughly: the message is a learned
embedding of the sender's own observation, as in CRAMP and PICO, so the
network rather than the designer decides what is worth sharing, and a
failure of communication to help cannot be put down to a poorly chosen
message.

## What would change if option 4 is adopted

- `2.Introduction.tex`, "What a decentralised agent sees". `o_i(t)`
  loses messages as its fourth piece (`eq:observation`,
  `tab:observationexample`, the intro list of four things). "Messages
  from nearby agents" becomes a description of the communication step
  that the decentralised policy uses, still bounded by `G^A_t`.
- `2.Introduction.tex`, "The learning problem". The sentence "This holds
  for messages too, because a message only carries positions and targets
  that are already part of `s_t`" is no longer true and goes.
  `eq:obsfunction`'s decentralised case stays `o_i(t)`, now without
  messages.
- `4.Implementation.tex`. The message payload sentence becomes a learned
  message head, `eq:readout` aggregates learned messages, and the two
  round counts (structure, communication) replace the single `L`.
- `2.Notation.tex`. A symbol for the message (for example `e_j(t)`, which
  is free) and the communication round count.
- `slap-mapd-coupling`. The message builder and the decentralised
  forward pass.
- `learning_problem_guide.tex`. Its fixed item 3 (messages keep `O_i`
  deterministic) is reversed, messages now live in the policy instead.

## Noted variant: messages across zone boundaries

Not adopted, kept as an option. The centralised and section-based networks
already exchange learned information between all agents inside their
window, because those agents share one graph pass, so messages inside a
zone would add nothing. Across a zone edge, the section-based network sees
only the halo (`eq:halo`), the role and occupancy of vertices within
`d_obs` hops outside the zone. The variant would keep the halo and add
learned messages from the agents standing in it. It would not remove the
boundary protocol, it would widen it. Messages instead of the halo are
ruled out, because a boundary agent's `delta_i(t)` needs the halo's
occupancy. Reasons for not adopting it: the section-based window would then
depend on `theta`, move toward the centralised one, and mix a communication
effect into the section-based results, which RQ5 is meant to keep
separate. Recorded under [A6] in `thesis-progress/temp/GAPS.md`.

