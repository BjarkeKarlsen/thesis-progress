# Comments on "How the controllers learn"

Scope: `4.Implementation.tex`, `sec:method:training` (PDF pages 44 and 45 of
`main.pdf`, built 2026-11-20 15:33, printed pages 43 and 44). Checked against
the Background (PPO, the critic, one shared policy, centralised training with
decentralised execution), the Problem Formulation (`sec:pf:controllers`, the
objective and the paragraph after it, `sec:pf:coupling`), "Choosing together"
and "When moves still clash", Appendices B, J and L, the Experiments
(`sec:exp:setup`, "What could have been done differently"), `GAPS.md` ([A9],
[A13], [A32], [A56], [A62], [A73], [A106]), van Knippenberg et al. 2021
(`papers/knippenberg21a.pdf`, Section 2.2 and Figure 3) and
`slap-mapd-coupling` on `main` (`8ba3048`): `training/env.py` (`team_mean`,
`_groups_at_start`, `_groups`, `arm_windows`), `training/config.py`,
`training/trainer.py`, `models/base_model.py`, `configs/fleet_8` and
`configs/fleet_16`.

The annotated pages are next to this file: `method_training_comments.pdf`.

How to answer: tick one box per point and add a note if you want. Three small
text-to-code fixes are applied and tagged `% [A108]`. Everything else is
unchanged.

---

## A. Is it true (checked against the code and the Results)

### A3. The critic argument leans on a credit we no longer have
**Where:** p. 44, "A decentralised learner gets no signal about the
crowding it causes for agents it cannot see ... A critic that sees the whole
warehouse during training only would partly teach that cost".

Be critical. A critic only predicts the return of the agent's own credit.
The decentralised credit is its own reward (eq. 49, `env.py` step, no
`team_mean` for `decentralised`). The delay it causes others is not in that
reward, so a critic that sees the whole warehouse could not teach it either.
The credit hides the cost, not the critic. GAPS [A13] keeps this reason from
when the credit was still open. I think the hunch holds. The first reason
(what a controller sees should limit how it learns) stands alone. The second
belongs to the credit paragraph, where it is true.

- [ ] Agree, move the second reason to the credit
- [ ] Disagree
- Note:

---

## B. Reasons and sources

### B1. Where is the credit from, and why the mean?
**Where:** p. 44, eq. (49).

Is the group mean ours? Knippenberg (Section 2.2) points to agents that
train on "a combined reward/value function" (Foerster et al. 2016, Gupta et
al. 2017), but his own agents get their own reward (his Figure 3). Neither
source is in `references.bib`. Cite one, or say the zone mean is ours. And
why the mean and not the sum? I guess so the reward keeps the same scale
whatever the size of the group, which matters because zones differ in size.
One clause.

- [ ] Cite (which?)
- [ ] Say it is ours, give the reason for the mean
- Note:

### B2. One shared policy is cited to RLlib
**Where:** p. 44, "with one policy shared by all agents, as RLlib supports
(Team, 2024)".

The Background gives the idea, with Knippenberg ("sharing one network this
way made training faster"). RLlib is the tool, so it belongs in the
Implementation, where RLlib is already named. Also the citation prints as
"Team, 2024", because the bib author `Ray Team` (`references.bib:127`) needs
braces.

- [ ] Agree
- Note:

### B3. Name the critic we did not use
**Where:** p. 44, "A critic that sees the whole warehouse during training
only".

This is centralised training with decentralised execution, which the
Background introduces with Lowe et al. Use the name and the citation, in one
clause. [A13] says the text states it as the standard alternative.

- [ ] Agree
- Note:

### B4. "Harder to learn"
**Where:** p. 45, "This setup is also harder to learn".

Is it shown? In Appendix L the policies trained under congestion-aware
storage served more than the ones trained under fixed storage (decentralised
0.186 against 0.028 tasks per step). That does not prove it easier, but it
does not support "harder" either. Say it as a risk ("can be harder"), or
drop it.

- [ ] Say it as a risk
- [ ] Drop it
- Note:

---

## C. One name per idea

### C2. A_i(t)
**Where:** p. 44, "with A_i(t) the agents that choose together".

The fleet is A. With a subscript it reads as "the fleet of agent i". The
notation table has both, so it is not wrong. Is a word like "group" with its
own letter clearer? The code calls it the credit group.

- [ ] Keep
- [ ] New letter
- Note:

### C3. Training and evaluation seeds
**Where:** p. 44, "Seeds are split between training and evaluation".

The code splits three ways (`train_seed_count`, `validation_seed_count`,
`test_seed_count`), and the checkpoint is chosen on validation seeds. The
Results say "test seeds". Use the three names.

- [ ] Agree
- Note:

### C4. Setups or regimes
**Where:** p. 45, "Two training setups are reported".

The Experiments, GAPS [A9]/[A56] and the configs (`regime:`) say "training
regimes". Pick one.

- [ ] Setups
- [ ] Regimes
- Note:

---

## D. Reading order and repetition

### D1. The credit is told three times
**Where:** p. 44, "It is credited with the mean reward of the agents that
chose together with it".

The PF says it ("An action is judged by the average reward of the agents
that chose together with it"), and "When moves still clash" uses "credited
with its own reward" two pages before the credit is defined here. Tell it in
full once, here, and point back from the others.

Carry-forward check: this section agrees with the credit. The closing
paragraph of "Choosing together" says the three controllers "share the
network, the masks, the reward and the training". They share the reward
function (eq. 48), not the credit. Write "the reward function" there and
name the credit as what differs, which is the PF's third consequence ("whose
reward an action is judged by"). The Experiments' "A shared reward for the
decentralised controller" means a shared credit too.

- [ ] Agree
- Note:

### D2. The critic explained again
**Where:** p. 44, "the critic, the part of the learner that estimates how
good a situation is".

The Background says this in the PPO paragraph. Cut the clause.

- [ ] Agree
- Note:

### D3. The first paragraph holds five ideas
**Where:** p. 44, the opening paragraph.

PPO, one shared policy, the seed split, the equal budget, and one step per
timestep. The seed split belongs with the warehouses (each seed is a
warehouse). "Its extra cost shows in runtime" is also in "Choosing together"
("runtime grows with the size of the fleet"). Split it, and say runtime once.

- [ ] Agree
- Note:

### D4. The two setups are told twice
**Where:** p. 45, the last paragraph.

`sec:exp:setup` repeats it ("Both training regimes ... are run. In the first
... In the second ... The main result uses the first."). It is a choice of
the experiment, so it could live there only, with one sentence here. Settle
after A1.

- [ ] Keep here, cut in the Experiments
- [ ] Move to the Experiments
- Note:

---

## E. Figures

No figure here, and none is needed. If A1 keeps both setups, a two-row table
(trained under, played under, what the gain measures) may be easier than
the paragraph.

- [ ] Table
- [ ] No
- Note:

---

## F. What reads well
- "One environment step is one timestep of the warehouse, however many
  agents choose within it", and the reason that follows. Clear.
- "It cannot learn one map by heart." Plain and concrete.
- The credit listed as the whole fleet, the zone, the agent alone.
- "The gain then compares two whole systems, storage rule and policy
  together."

## The three changes that would help the reader most
1. Settle which training setup is the main result, since the Results already
   use the second (A1).
2. Put the second critic reason where it is true, in the credit, and say
   where the credit comes from (A3, B1).
3. Bring the training numbers up to the runs that are tested, and drop the
   plan sentence (A2).
