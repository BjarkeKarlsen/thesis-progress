# Comments on Appendix C, "Model details"

Scope: `thesis/Appendices/C.ModelDetails.tex` (its own PDF, pages 1 to 5
after the front page, rebuilt 2026-11-20 after the fixes below). Checked
against the Problem Formulation (`sec:pf:game`, `sec:pf:observations`,
`sec:pf:measures`), the Method (`sec:method:storage`, `sec:method:model`,
`sec:method:controllers`, `sec:method:rl`), `GAPS.md` ([A6], [A11], [A55],
[A86], [A97], [A106], [A107]), the papers in `thesis-progress/papers`
(van Knippenberg et al. 2021 `knippenberg21a.pdf`, CRAMP
`2309.10275v3.pdf`, PRIMAL `1809.03531v3.pdf`) and `slap-mapd-coupling` on
`main` (`8ba3048`): `environment/zones.py`, `environment/observation.py`,
`models/local_subgraph_encoding.py`, `models/gnn_encoder.py`,
`environment/spaces.py`, `resolution/conflict_resolution.py`,
`environment/reward_function.py`, `environment/multi_agent_env.py`,
`instances/generator.py`, the fleet configs.

The annotated pages are next to this file:
`appendix_C_modeldetails_comments.pdf` (PDF pages 2 to 6).

How to answer: tick one box per point and add a note if you want. Points
marked "Fixed" are already applied, tagged `% [A108]`, and need no answer.

---

## A. Is it true (checked against the code and the papers)

### A1. No controller reads another agent's crowding
**Where:** p. 1, C.2.2, "A section-based controller conditions on zone-local
state, so it has δ_j(t) for every agent j in its own zone". The heading says
"reads".

**Code:** every network reads only the agent's own δ_i. The readout is the
own vector, the mean (or the messages) and δ_i, in that order
(`gnn_encoder.py`, the readout). δ is not a vertex feature
(`local_subgraph_encoding.py:362`). The window holds the other agents, so
their crowding could be worked out, but nothing reads it. The PF says the
same thing in V-G ("Each controller reads the values of the agents it
decides for", `3.ProblemFormulation.tex:1074`).

**Proposal:** "Every controller reads only the agent's own crowding
feature. A wider window holds more agents, so a zone or the whole fleet
could work out the others' values, but the network does not read them."
Fix the PF sentence the same way. Or cut the first paragraph of C.2.2.

- [ ] Agree, say it as the code does (here and in V-G)
- [ ] Cut the paragraph
- Note:

**Fixed ([A109]).** C.2.2 and V-G now say every controller reads only the
agent's own δ_i. The wider window of a zone or the centralised controller
could give the others' values, but the network does not read them.

### A2. Knippenberg's convolution is not plain Kipf, and "special case"
**Where:** p. 3, "This is a special case of the message-passing step (43)".

Be critical. Their Section 2.3 says the GCN embeds node *and edge*
attributes, so their layer is not Kipf's without edges. And in the code
the message is the mean of φ(h_v, h_w), so Kipf's weights
1/√(deg v · deg w) cannot be reached exactly, since φ does not see the
degrees. I think "special case" holds for (43) as written (φ takes the
whole set), but not for the network we run. "Has the same shape" is safer,
and one clause that their layer also reads the edge costs.

- [ ] Agree
- [ ] Leave it
- Note:

### A3. The one-step cost is used nowhere
**Where:** p. 5, eq. (C.7).

ĉ(v,w) appears only here and in the notation tables. VI-F takes only
c_wait from it. The reward charges c_move = 0.1 for a move
(`reward_function.py:146`), not c(v,w) = 1. A reader will think a move
costs c(v,w). The graph carries `wait_cost` but only the reward uses it.

**Proposal:** define c_wait and c_move in words in VI-F and drop (C.7) and
its rows in A and in `2.Notation.tex`.

- [ ] Agree
- [ ] Keep (C.7)
- Note:

### A4. Trip distance
Known. The code weights the two legs, eq. (C.2) adds them. Open in
`review_trip_legs.pdf` (Part 4 rewrites this equation). Not touched here.

### A5. Checked and matching
- **Halo (C.3):** `zones.halo` takes the movable vertices outside the zone
  with d_G(w,v) ≤ d_obs from some zone vertex w. Non-movable vertices have
  no edges, so leaving them out of the equation changes nothing.
- **Vertex features (C.4):** the nine numbers of `encode_view` are the
  multi-hot role (five flags), η̃ capped at ±d_obs, occupied by another
  agent, in V_{≺i}(t), and η/50. Onehot against multi-hot is already in
  `method_model_comments.md` B9.
- **Action mask (C.5):** `legality_mask`, 0 on wait and the real moves,
  −∞ on the empty slots.
- **Claim mask (C.6):** `claim_mask` and `move_blocked`. The vertex rule,
  the swap, and a move onto an agent that has not chosen yet (agents of
  other zones count as not chosen). Wait is never switched off.
- **Edge costs:** every config has `default_edge_cost: 1.0` and
  `random_edge_costs: false`, as C.2.5 says.
- **Crowding:** always counted over the field of view
  (`build_observation`), and `congestion_weight: 1.0` for every
  controller, as C.2.1 says.
- **Table C.1:** δ_1 = 2/5 matches Fig. 9 (five other vertices, a_2 and a_3
  on two of them).
- **Bound (C.1):** true by the triangle inequality. Equality on a shortest
  path, as written.
- **Gilmer et al.:** the message and update functions as in their paper.
  Messages along edges in both directions in the code
  (`window_structure`, `_local_undirected_neighbours`).
- **Kipf and Welling:** the normalisation with self-loops is right.
- **Van Knippenberg et al.:** DQN, an invalid move becomes a penalised wait,
  a collision ends the episode with −2, move −0.1 and wait −0.2 (their
  Table 1), the output layer gives all action values at once, Figure 3.
- **CRAMP:** agents in the field of view as nodes, distance weights in A,
  node features from the CNN, the GNN outputs averaged and joined with the
  LSTM output. The crowd density counts agents over free space, in a region
  smaller than the observation (w = 5), only in the reward, with a
  threshold ζ.

### Fixed ([A108])
**Fixed ([A108]).** P is not random only through orders. The code also draws
a dock at random for each put-away and each finished order
(`multi_agent_env.py:899`, `:919`, `dock_choice: random` in every config).
C.2.1 now says so. V-H says "Its only randomness is the arrival of orders"
too (`3.ProblemFormulation.tex:1209`), so the PF needs the same fix.
**Fixed ([A109]).** V-H and the "Deterministic execution" item of the scope
now name the dock draw too.

**Fixed ([A109]).** `app:measures:blocked` cited `eq:storageupdate` for
ω̂_t(v). It now cites `eq:standstill`, where ω̂ is defined.

**Fixed ([A108]).** Table C.1 gave η_1(B,t)=4 and η_1(C,t)=6. Since [A93]
Fig. 9 and V-G use the aisle vertices v and w, with 3 and 5.

**Fixed ([A108]).** "It differs in two ways" from Gilmer et al. There are
three. The code takes the mean over the neighbours (`gnn_encoder.py:186`),
they take the sum. The doubled name "The message passing step the
message-passing step (43)" is fixed in the same sentence.

**Fixed ([A108]).** "The move score, the value head and conflict resolution
are what this model adds." Van Knippenberg et al. already apply the actions
in an order that avoids collisions where it can (their Section 4.2), and
VI-E cites them for it. Now only the move score and the value head are
new, and conflict resolution goes further by turning every remaining clash
into a wait.

**Fixed ([A108]).** The CRAMP equation had no f on the left, so g read as
the agents. In their Section III-E, f and g number the features of a layer.

**Fixed ([A108]).** In both masks v was not named. It is ℓ_i(t), the agent's
own vertex, so the last case of the claim mask is the swap.

**Fixed ([A108]).** "The reading follows the crowd density" and "W_T is not
the shelf estimate" named nothing a reader of this appendix has. They now
open with the mean crowding (32) and the mean blocked time W_T (31).
"Scored by the vertex it leads to the move score (46)" now reads "leads to,
by the move score (46)". The halo and the vertex features end with a full
stop instead of a dangling comma.

---

## B. Reasons and sources

### B1. PRIMAL is missing from the side by side
**Where:** p. 2, C.2.5, "takes its parts from three sources", and p. 3,
"They turn an invalid move into a penalised wait, and here the mask
removes it".

The Method says the network follows van Knippenberg et al., "who built on
PRIMAL". PRIMAL is not set beside the model here. It matters for the mask:
PRIMAL already samples only valid actions in training and reports that this
trains more stably than penalties (their III-B), and an invalid move
becomes a wait only at test time. So our mask is PRIMAL's idea on a graph,
not only the opposite of van Knippenberg's penalised wait. PRIMAL is also
actor-critic (A3C), closer to our PPO than a DQN, and its agents act one
after another in a random order and can still collide (−2).

**Proposal:** a short paragraph "PRIMAL" (mask, actor-critic, sequential
order), and cite PRIMAL in the mask sentence of VI-C.

- [ ] Agree, add a paragraph
- [ ] Only cite it in the mask sentences
- Note:

### B2. Crowding is used in more ways than CRAMP's
**Where:** p. 4, "Here it covers the field of view d_obs, has no threshold,
and is averaged into a reported outcome. That averaging is this thesis's
own."

Here the crowding feature is also an input of every controller and a term
of the reward (C.2.1 says so). CRAMP uses its density only in the reward.
That is the bigger difference.

- [ ] Agree
- Note:

### B3. Why the distance-label bound, and on whose numbers?
**Where:** p. 2, C.2.4.

The first sentence repeats V-G ("a small step back for a bigger gain
later"). Nothing in the thesis refers to (C.1) or to C.2.4. [A55] already
narrowed its claim. The example uses an edge of cost 2, which never happens
in our warehouses. "A policy could claim to make huge progress for free"
sounds as if the policy reports the label, but the label is computed.
What does the reader need it for? I think it can go, or shrink to one
sentence in V-G. If it stays, use cost 1 and point to it from V-G.

- [ ] Cut
- [ ] Keep, use cost 1 and point to it
- Note:

---

## C. Names, plain words, symbols

### C1. Old words in C.2.2
**Where:** p. 2, "One detail needs stating explicitly ... Section-based
routing's own window already includes 'boundary protocol'".

"Needs stating explicitly" is text about the text. "Routing" (we say
controller), "conditions on", "zone-local state" and "boundary protocol" in
quotes. The chapters no longer use "boundary protocol", only the notation
tables do (`A.Notation.tex`, rows H_q and s_t^(q)). VI-D now says the halo
keeps a border agent's whole field of view in its window ([A107]). So the
paragraph repeats VI-D in old words. Cut it and point to VI-D, as the PF
does.

- [ ] Agree
- Note:

### C2. One name for shelf and stock
**Where:** p. 1, "on every storage vertex", "the storage state", and
"the storage configuration x_9".

Shelf, and "the stock x_t" as in Table V (the learning problem).

- [ ] Agree
- Note:

### C3. F and the distance label
- C.1.1, "F breaks such ties": F is not introduced in this appendix. Say
  "the storage rule".
- C.2.4, "The direction to target η_i is a distance". V-G calls η the
  distance label. Use one name.
- C.2.4, "= 3; it cannot" and "closer / further": a semicolon joins two
  clauses, and the slash reads as code.

- [ ] Agree
- Note:

---

## D. Reading order and repetition

### D1. Three parts that nothing points to
C.2.1 (the example state and the remarks), Table C.1 and C.2.4 (the bound)
are never referenced from the thesis. Only `app:controllers` is, from V-G,
for the zone edge. C.2.1 repeats V-H ("the same for every controller, so
they are part of P", the priority order is in the state) and calls it "a
second reason" without the first. Table C.1 repeats the V-G example and
Fig. 9. Either the thesis points to each of them, or they go.

- [ ] Cut C.2.1, Table C.1 and C.2.4
- [ ] Keep and point to them (from where?)
- Note:

### D2. C.2.1 says it has two remarks on the kernel
**Where:** p. 1, "This subsection gives an example state and two remarks on
the transition kernel."

Text about the text. Only one remark is about the kernel. The paragraph on
crowding is about what a controller sees, so it belongs in C.2.2 (and A1
changes it).

- [ ] Agree
- Note:

### D3. Ties go round in a circle
**Where:** p. 1, C.1.1.

VI-A says ties go by index "so each rule gives exactly one placement
(Appendix C.1.1)". C.1.1 says the tie-breaking rule is in VI-A. The reader
goes back and forth and learns nothing new. "The rules do not search for
the smallest value" is also said twice in VI-A. Cut C.1.1, or put the real
tie order here once `review_trip_legs.pdf` is settled (the code breaks
equal scores by the plain trip first, then the vertex id).

- [ ] Cut
- [ ] Keep with the tie order
- Note:

### D4. The opening sentence
**Where:** p. 1, "The worked examples, derivations and formal statements
behind the design of the thesis, in the order of the thesis. Each keeps its
number, ..."

The first sentence has no verb. "Each keeps its number" is not true, the
equations here are numbered C.1 to C.7. The same sentence comes again word
for word at the start of C.4. Say what the appendix holds in one sentence
and drop the rest.

- [ ] Agree
- Note:

### D5. Order of C.4
C.4 goes VI-A, VI-D, VI-C, VI-F. Put the halo (VI-D) after the features and
masks (VI-C), in the order of the Method.

- [ ] Agree
- Note:

### D6. C.3 retells V-J
**Where:** p. 4, "The result of the thesis is the service time gain ...".

Nothing below uses it. One sentence on what C.3 holds is enough.

- [ ] Agree
- Note:

---

## E. Figures

### E1. Fig. C.1
"(ibid.)" in a caption reads odd. Write the names, or "as in Figure 3 of
the same paper". And what does it show that Fig. 13 in the Method does
not? If the point is only "drawn as van Knippenberg drew it", one figure
may be enough.

- [ ] Agree, fix the caption
- [ ] Also drop the figure
- Note:

---

## F. What reads well
- Gilmer and Kipf each written in their own form and then in ours. Easy to
  check.
- "Other differences from van Knippenberg et al.", one difference per
  sentence.
- W_T against the shelf estimate. "A forecast" against "looks back" says it
  in two words.
- "The bound limits gains only" is honest about what the bound does not
  give.

## The three changes that would help the reader most
1. Say what the networks really read of the crowding feature (A1), here and
   in V-G.
2. Cut or point to the parts nothing refers to: C.1.1, C.2.1, Table C.1 and
   C.2.4 (D1, D3, B3), and drop the unused one-step cost (A3).
3. Add PRIMAL to the side by side, and credit it for the action mask (B1).
