# Plan for the simplification changes that stay, 2026-10-16

Local note. The controller redesign (real centralised and section-based) is not in this file. It is in
`real_centralised_design.md`, and its plan is written once that decision is taken. Two items stay here.

## Rules that apply to every step

- The thesis is the source of truth. A model change is agreed first, then written into the chapters with an inline
  `% [Axx]` tag and an entry in `thesis-progress/decisions/GAPS.md`, then implemented.
- Thesis prose follows the style rules of the workspace `CLAUDE.md`, and is only edited once the author agrees.
- Code goes in small branches from `main`. I push the branch and draft the PR text, the author opens the PR.

## 1. Embed each window once (issue 160)

Status, later on 2026-10-16: do now, Track B of `ROADMAP.md`.

Design in `embed_once_design.md`. It applies to the decentralised arm with communication, the only arm with senders.
Under the real centralised and section-based design, robots in one decision unit already share the decision, so no other
arm has messages.

1. The probe. A `Learner` subclass through `config.learners(learner_class=...)`, and `row_key` surviving the learner
   connectors. No commit.
2. One branch. Keys and adapter, the two part encoder with the equality test against the old path, the two pass value,
   the block iterator and its learner, and last the removal of the sender windows.
3. The open question of the issue is whether the decentralised arm without communication also uses the block iterator.
   Recommended yes, so the comparison with and without messages differs only in messages.
4. The cap `max_messages` (98 mentions in 16 files) can become the fleet size minus one, or go.

Retraining. Nothing needs it for correctness. The minibatch rule changes training dynamics slightly, so runs before and
after are not bit for bit comparable.

Size. Large. It touches the adapter, encoder, module, value pass and learner.

## 2. The factor grid (gate D4)

Run the main comparison of storage rule against architecture at one congestion setting and one load. Treat congestion
sensitivity and load as separate one-factor sweeps. The author agreed this lever.

- The main grid is 3 by 3, 9 conditions.
- Fully crossed with load at 3 levels (an assumption, the thesis says several), 3 storage rules by 4 routing variants by
  2 congestion settings is 72 conditions. With sweeps it is about 18 to 24.
- The limit from RQ4. The load sweep must repeat adaptive against fixed storage for every architecture, and the
  congestion sweep needs the routing toggle for every architecture. Neither can run at one storage rule. One-factor sweeps
  lose interactions.

A design change with no code beyond new sweep configs for the `sweep` verb. In `2.Introduction.tex` it changes the aim
and scope list and the experiment text. In `4.Implementation.tex` the sentence about checking the learned routers under a
few conditions (about line 177) is the nearest hook. Tag it A35 if it is logged, since A32 to A34 may be taken by the
controller redesign.

## Not yet checked

- The probe of item 1.
- How many conditions the thesis plans to run, and whether congestion sensitivity applies to every storage rule.
