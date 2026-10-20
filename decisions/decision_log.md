# Open thesis decisions from #103

These are the "Waiting for a thesis decision" points in `slap-mapd-coupling`
issue #103, plus the training-budget gap. Each entry lists the options, where
in the thesis the decision goes, and what it changes in the code. The code
follows only once the thesis says it. Line numbers are from `thesis/` as of
2026-10-07.

The order runs from most to least blocking. Decisions 1 to 4 decide whether
any result can be reported at all.

**Status 2026-10-16.** Decided or overtaken: 2 (unit only, the first
result uses 500 000 timesteps), 5 (lower priority), 14 and 17, each marked
in its entry. Still the most blocking: 1, the demand model, for RQ1 and
the coupling half of RQ2. The others are still open
and were not rechecked against the chapters, so the line numbers below may
have moved. The ordered list of what to decide next is in
`SESSION_CONTEXT.md`.

**Added 2026-10-17.** Entries 19 to 21, from comparing the storage rules of
the Method with the Introduction. The Introduction is the source of truth, so
each one is a Method sentence (or code) that does not match it.

---

## 1. Demand model (#94)

- **Today:** Poisson arrivals at rate lambda_task. Each order's SKU and pickup
  vertex are drawn uniformly among the pairs that are in stock.
- **Options**
  - (a) Keep it uniform.
  - (b) Skewed SKU popularity, such as Zipf with exponent s, fixed per run.
  - (c) Skewed popularity that drifts over the run, so adaptive storage has
    something to follow.
- **Where to decide:** `sec:pf:tasks` (the order process P_ord), with its
  values in `tab:evalparams` (`4.Implementation.tex`).
- **Effect on the code:** `environment/multi_agent_env.py` order generation,
  and new config fields such as `popularity_skew` and `drift_rate` with no
  default. Under (a), F_dem has nothing to adapt to, so the adaptive-storage
  research question becomes empty. This also blocks #95, the starting stock
  placed from expected demand.

- **Test values agreed 2026-10-17** (from the Token Passing probe in
  `~/thesis_runs/demand_probe/`, runs `quick/` and `quick2/`): Zipf skew
  s = 1, the ranking rotates 5 places every P = 200 steps, 100 SKUs of 8
  units, vertex capacity 200, starting stock in blocks (most popular SKUs at
  the vertices nearest the delivery vertices), Delta = 100, nu = 48, beta 3
  and 10, load 0.3 for service time and 0.6 for throughput. Illustrative, not
  thesis values yet. Measured: at load 0.3 the demand rule cuts service time
  from 54.1 to 39.4 (rotation every 200) and from 44.4 to 36.5 (every 500).
  Without rotation the gain is near zero.

## 2. Training budget (gap under "Fix PR: training")

- **Unit decided 2026-10-16 ([A32]): (a), environment steps, one per
  timestep however many agents choose in it, equal across arms.** The code
  follows (#165). The value is still TBD in `tab:trainparams`. The rest of
  this entry is the state before the decision.

- **Today:** there is no setting. The caller picks how many times to call
  `algo.train()`.
- **Options**
  - (a) A config field `training_budget_steps`, counted in environment steps,
    with no default, added to #85.
  - (b) The same field, counted in episodes.
- **Where to decide:** `tab:trainparams` (`4.Implementation.tex:514`), next
  to "equal across arms" (`4.Implementation.tex:498-501`).
- **Effect on the code:** `training/config.py`, and the trainer stops after
  the budget. The fair-comparison claim between the arms depends on this.

## 3. Where agents start, l_i(0) (#105)

- **Today:** random distinct endpoints, drawn from the episode seed.
- **Options**
  - (a) Keep random distinct endpoints.
  - (b) Fixed endpoints by agent index.
  - (c) Random distinct vertices anywhere in V_mov.
- **Where to decide:** `sec:pf:agents` (the initial state), one sentence.
- **Effect on the code:** `environment/multi_agent_env.py:202`, plus the
  replay test. Under (b), training episodes vary less.

## 4. A free agent's target q_i(t) (#102)

- **Today:** a free agent's target is its own vertex, so its distance label
  is 0 and the reward gives it no shaping signal while it is idle.
- **Options**
  - (a) Keep its own vertex.
  - (b) The nearest endpoint, so idle agents learn to clear transit vertices.
  - (c) The pickup vertex of the task the assignment rule would give it next.
- **Where to decide:** the current target (`eq:currenttarget`,
  `2.Introduction.tex:900-907`).
- **Effect on the code:** `environment/reward_function.py`
  (`current_target`), plus the distance labels in `environment/observation.py`.
  Option (b) changes the learned behaviour directly. Option (c) couples the
  reward to the assignment rule.

## 5. The reference planner's horizon (#99, including `stationary_window`)

- **Lower priority since [A28].** Token Passing is the reference baseline,
  and prioritised A* is kept only as a reference planner, so this affects
  only its numbers.

- **Today:** a reservation horizon of |V| steps is hard-coded.
- **Options**
  - (a) A config field with no default, added to #85.
  - (b) Keep |V| and state it in the thesis.
  - (c) The evaluation horizon T.
- **Where to decide:** the reference planner paragraph
  (`4.Implementation.tex:148-156`).
- **Effect on the code:** `controllers/centralised.py:79-89, 217-238`, and
  `experiment_config.py` under (a). This only affects the baseline numbers.

## 6. The "marginal value" of a relocation under the cap (F_dem and F_cng)

- **Today:** a relocation is one gaining (SKU, vertex) cell. Cells are ranked
  by the storage rule's own placement order, and the budget is spent in
  units, so a cell can be applied in part.
- **Options**
  - (a) Keep the placement order and say so.
  - (b) The drop in the congestion-aware score D + beta K per relocated
    unit, which needs a score for F_dem too (beta = 0).
  - (c) Drop the words "marginal value" and write "the first nu units in the
    rule's priority order".
- **Where to decide:** the relocation cap in `sec:method:storage`
  (`4.Implementation.tex:91-98`), and the nu row in `2.Notation.tex:83`.
- **Effect on the code:** `storage/relocation.py`, `storage/demand.py:89-94`
  and `storage/congestion.py:186-187`. Option (c) needs no code change.
  Option (b) changes which items move when the cap binds. This entry covers
  three #103 points (from #58, #59 and #61).

## 7. Which units leave when the cap binds

- **Today:** units are taken from source cells in ascending vertex id.
- **Options**
  - (a) Keep ascending vertex id, as a deterministic tie-break.
  - (b) The worst-scoring source cell first, farthest from delivery.
- **Where to decide:** same paragraph as decision 6
  (`4.Implementation.tex:96-99`).
- **Effect on the code:** one sort key in `storage/relocation.py:85`. Under
  (b), more relocations pay off.

## 8. "SKUs are placed in ascending score order"

- **Today:** SKUs go in descending demand, and each takes its lowest-score
  free vertex. Read literally, the thesis would give low-demand SKUs the best
  vertices first.
- **Proposed wording:** "SKUs are placed in descending order of estimated
  demand, each to the free vertex with the lowest score."
- **Where to decide:** `4.Implementation.tex:86-87`.
- **Effect on the code:** none, since the code already does this.

## 9. Which way "nearest delivery point" is measured

- **Today:** the nearest point is chosen by d_G(v, g), but path(v) runs from
  that point to v. With one-way edges the two can differ.
- **Options**
  - (a) d_G(v, g), the storage vertex to the delivery point, the leg a loaded
    agent drives.
  - (b) d_G(g, v), matching how path(v) is written.
  - (c) Define path(v) from v to g, so both directions agree with (a).
- **Where to decide:** the congestion-aware score (`eq:storagegreedy`,
  `4.Implementation.tex:80-85`).
- **Effect on the code:** `storage/congestion.py:16-25, 44-49, 96`, with a
  one-line change in direction. The rankings only differ on layouts with
  one-way aisles.

## 10. Typo in the congestion-aware score

- `eq:storagegreedy` writes `d_G(v, \min_g)`. The code reads it as
  `\min_{g \in V_{\mathrm{del}}} d_G(v, g)`.
- **Proposed fix:** write `\min_{g \in V_{\mathrm{del}}} d_G(v, g)` at
  `4.Implementation.tex:80`. Combine it with decision 9.
- **Effect on the code:** none.

## 11. Role feature: one-hot or multi-hot

- **Today:** multi-hot (storage, delivery, endpoint, transit), with transit
  meaning none of the other three.
- **Options**
  - (a) Multi-hot, with the thesis saying so and defining "transit".
  - (b) One-hot with a fixed priority between overlapping roles.
- **Where to decide:** the vertex features (`eq:features`,
  `4.Implementation.tex:220-225`) against `2.Introduction.tex:133-134`.
- **Effect on the code:** none under (a). Under (b), `environment/observation.py`
  (`role_flags`) changes and the vertex features lose one bit of information.

## 12. How congestion sensitivity is switched off for a learned policy

- **Today:** delta_i(t) always enters z_i. The switch only decides whether
  the observation computes it.
- **Options**
  - (a) Zero delta_i(t) in the input.
  - (b) Set n_cng = 0 in the reward, but keep the input.
  - (c) Both.
- **Where to decide:** `2.Introduction.tex:849-850, 1178-1180` (the
  congestion-sensitivity toggle).
- **Effect on the code:** `models/gnn_encoder.py:172-179`, plus config
  validation of `congestion_reward_weight`. This sets what the "insensitive"
  arm means in the congestion research question. It also interacts with the
  fix PR that always puts delta_i(t) in the observation.

## 13. Depth of phi_r and psi_r

- **Today:** each is one Linear+ReLU layer, with one hidden width.
- **Options**
  - (a) One layer, stated in the thesis.
  - (b) A depth parameter in `tab:modelparams`, TBD.
- **Where to decide:** `tab:modelparams` (`4.Implementation.tex:426-437`).
- **Effect on the code:** `models/gnn_encoder.py:122-129`. Under (b), one
  extra config field.

## 14. The extra trunk in the head

- **Decided 2026-10-13: (a), remove it.** The code follows in L3 (#92). The text
  already says the value head reads z_i, so the one thesis edit left is the
  figure `fig:architecture`, which still draws the trunk as a "fully connected +
  ReLU" box. The rest of this entry is the state before the decision.
- **Today:** a shared FC+ReLU trunk sits between z_i and both the policy head
  and the value head.
- **Options**
  - (a) Remove it, so the value network reads z_i directly as the thesis
    says.
  - (b) Keep it and add it to the thesis.
- **Where to decide:** `4.Implementation.tex:373-375, 432`.
- **Effect on the code:** `models/base_model.py:43, 57-59`. It will change
  again with the per-edge head (#92), so deciding before #92 avoids doing the
  work twice.

## 15. Padding caps for the field of view and messages

- **Today:** `max_local_nodes` and `max_messages` cut the input, keeping
  vertices by ascending distance label and messages by sender distance.
- **Options**
  - (a) No caps, padding to the largest size in the batch, as the thesis
    implies.
  - (b) Keep the caps as config, with values set large enough never to bind,
    and say so in the thesis.
- **Where to decide:** `4.Implementation.tex:313-325`, `tab:modelparams`.
- **Effect on the code:** `models/local_subgraph_encoding.py:9-24, 68-87`.
  Under (a), memory use follows d_obs. This interacts with #91.

## 16. PPO settings the thesis doesn't name

- **Today:** RLlib's defaults are used, which means an adaptive KL penalty
  (`use_kl_loss=True`, `kl_coeff=0.2`) on top of the clip,
  `vf_clip_param=10.0` and `grad_clip=None`.
- **Options**
  - (a) Pure clipped PPO (`use_kl_loss=False`), with the remaining settings
    listed in `tab:trainparams`.
  - (b) Keep RLlib's defaults and list them in `tab:trainparams`.
- **Where to decide:** `tab:trainparams` (`4.Implementation.tex:487, 514-521`).
- **Effect on the code:** `training/config.py:181-191`, a few explicit
  arguments. Option (a) matches "clipped PPO" as written.

## 17. Actions during evaluation

- **Decided 2026-10-16: (b), sampled.** Greedy evaluation is a diagnostic
  only (`thesis-progress/notes/signals_and_decisions_2026-10-16.md`,
  6A). `controllers/decentralised.py` no longer exists, and evaluation goes
  through `training/policy.py`. The thesis sentence saying that the
  reported results are sampled is still to write (6B.5 there).

- **Today:** example 04 picks the most likely action, while
  `DecentralisedController` samples from the policy.
- **Options**
  - (a) Most likely action, which is deterministic but can deadlock
    symmetric agents.
  - (b) Sampled, using a stream seeded from the episode seed.
- **Where to decide:** `4.Implementation.tex:190-193`.
- **Effect on the code:** `controllers/decentralised.py:117-118` and
  `examples/04_decentralised_training.py:201`. Both must use the same choice.

## 18. Placing storage vertices (#76)

- **Today:** a seeded random sample of aisle cells.
- **Options**
  - (a) Keep the seeded random sample and add it to `sec:impl:instances`.
  - (b) A deterministic pattern, such as every k-th aisle cell.
  - (c) Every aisle cell is a storage vertex.
- **Where to decide:** `sec:impl:instances` (`4.Implementation.tex:559-561`).
- **Effect on the code:** `instances/generator.py:150-160`. Under (a),
  instances vary with the seed, which adds variance to paired runs unless the
  instance seed is held fixed.

## 19. The congestion score is not the Introduction's congestion exposure K

- **Today:** the Introduction defines K as "how much predicted traffic a
  configuration concentrates onto one corridor", with the example of two
  high-demand SKUs on the same busy aisle (`2.Introduction.tex:528-531`).
  The Method's congestion-aware score adds `beta * sum mu_hat(e) w_hat(e)`
  along path(v) (`eq:storagegreedy`, `4.Implementation.tex:76-87`). That is
  a fixed price per vertex from past traffic. It is the same for every SKU,
  so relative to the distance term it weighs most for rarely ordered SKUs
  and least for popular ones, and it does not grow when a second popular
  SKU is placed on the same corridor.
- **Options**
  - (a) Keep the score and reword K in the Introduction as exposure to past
    congestion.
  - (b) Weight the congestion term by the SKU's demand,
    `rho_hat(k) * (d(v) + beta * exposure(v))`, so every SKU trades distance
    against congestion the same way.
  - (c) (b), and also raise a corridor's predicted load as SKUs are placed on
    it during the update, so concentration itself is penalised as K says.
- **Where to decide:** `eq:storagegreedy` and the sentence after it
  (`4.Implementation.tex:76-87`), against `eq:storageobjective`.
- **Effect on the code:** `storage/congestion.py` (`score`). Under (b) a
  one-line change. Under (c) the greedy fill keeps a running load per edge.
  `beta`'s scale changes under (b) and (c), so its sweep values follow the
  choice.
- **Measured 2026-10-17** (`thesis-progress/decisions/done/demand_probe_2026-10-17.md`):
  (b) equals the demand rule at beta 1 to 10, a variant of (c) did worse than
  the demand rule, and today's score at beta = 1 lowered blocked time for the
  decentralised policies with throughput level. This points to (a), with beta
  around 1, unless the retrained arms show otherwise.

## 20. "Exactly this thesis's contribution" overstates the storage ladder

- **Today:** the Method says the gap between `F_dem` and `F_cng` "isolates
  exactly this thesis's contribution: the value of traffic information over
  demand information alone" (`4.Implementation.tex:59-63`). The
  Introduction names the contribution as the model, the implementation and
  the analysis of when feedback shortens service time and when it adds
  congestion (`2.Introduction.tex:20`). The `F_dem` to `F_cng` gap answers
  the storage half of RQ3, one question of four.
- **Proposed wording:** "The rules form a ladder. The gap between the second
  and the third shows what traffic information adds to demand information
  alone, the storage half of RQ3."
- **Where to decide:** `4.Implementation.tex:59-63`.
- **Effect on the code:** none.

## 21. How waits are attributed to an edge (w_hat)

- **Today:** the Introduction defines `w_hat_t(e)` as "waiting attributed to
  an edge or its downstream contention point" (`2.Introduction.tex:455-457`,
  `eq:estimates`). The Method never says how a wait is attributed. The code
  counts a wait only when conflict resolution overrides a move, charged to
  that move's edge (`environment/multi_agent_env.py:310-319`,
  `environment/storage_estimates.py:72-74`). Token Passing and the
  centralised arm are never overridden, so for them `w_hat` is always 0 and
  `F_cng` behaves exactly like `F_dem`. Only the decentralised arms ever feed
  it waits.
- **Decided earlier (`adaptive_storage_plan.md`, section 2):** a step where an
  agent serving a task stands still is charged to the next edge on its route
  to its goal, whatever kept it there. This matches the Introduction.
- **Still open:** the Method sentence, and which "route" (the shortest path
  to the goal is proposed).
- **Where to decide:** a sentence after `eq:estimates`, or in
  `sec:method:storage` next to the `[A26]` paragraph.
- **Effect on the code:** `environment/multi_agent_env.py` (charge the wait
  where `record_blocked_tick` is called) and a test that `w_hat` is not
  always 0 under Token Passing (task T8 of `adaptive_storage_plan.md`). The
  demand probe runs this rule as `--wait-rule standing`. In its smoke test
  Token Passing then had 0.18 to 0.27 waits charged per step, and `F_cng`
  differed from `F_dem`.

