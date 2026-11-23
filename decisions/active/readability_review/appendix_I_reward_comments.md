# Comments on Appendix I, "Observation depth and reward weights"

Scope: `thesis/Appendices/I.Reward.tex` (`app:reward`), the appendix as its
own paper, `I.Reward.pdf` rebuilt 2026-11-20 after the fixes below. Checked
against `slap-mapd-coupling` on `main` (`8ba3048`):
`environment/reward_function.py`, `environment/observation.py`,
`training/env.py`, every config in `configs/` and the trained runs in
`~/thesis_runs` (all 498 run configs: d_obs 5, gamma 0.99, n_deliver 10,
n_blocked 0.5 apart from the two fleet 32 override tests, n_crowd 0.1,
c_move 0.1, c_wait 0.2). Also checked against van Knippenberg et al. 2021
(`papers/knippenberg21a.pdf`, Tables 1 and 5, Sections 6.2 and 6.3), the
PPO paper's Tables 3 to 5, `main.pdf` of 2026-11-20 (section and equation
numbers), `D.Warehouses.tex` (`tab:instances`), `GAPS.md` ([A30], [A43],
[A79], [A80], [A93]) and the RL review notes
(`results/training/rl_review_2026-11-10/README.md`, the only written record
of [A89] and [A90], which have no GAPS entry yet).

The annotated pages are next to this file: `appendix_I_reward_comments.pdf`.

How to answer: tick one box per point and add a note if you want. Points
marked **Fixed ([A108])** are already changed in `I.Reward.tex`.

---

## A. Is it true

### A5. "A decentralised agent sees nothing beyond it"
**Where:** p. 2, Setting, first paragraph.

Be critical. An agent hears every agent inside its field of view, and a
message is computed from the sender's own observation (PF, Messages from
nearby agents). So news from up to 2 d_obs away reaches it. I think the
hunch holds for the decentralised controller with messages. "Sees nothing
beyond it, and hears only the agents inside it" would be true.

- [ ] Agree
- [ ] Leave it
- Note:

### A7. "Their depth counts edges on a graph shaped like a train yard"
**Where:** p. 2, Method, first paragraph.

The train yard is right (Section 6.2 says the following experiments use the
yard graphs). "Counts edges" is not in the paper. It only says "how far away
from the agent's location other nodes can be", and their edges carry costs.
Their Figure 2 (d = 2) suggests hops. Write "appears to count edges" or drop
the clause. Their Section 6.3 also says the field of view grows fast with
node degree. Our mean degree is 2.23 to 2.24 (`tab:instances`), against
"each node tends to have a lower degree than a node in a grid world" for
theirs. Comparing degree may say more than the window count, and we already
have it.

- [ ] Agree
- Note:

---

## B. Reasons and sources

### B1. Is the delivery reward pilot already done?
**Where:** p. 2, "so a pilot compares n_deliver of 1 and 10".

The configs record it: "A 5000-iteration run showed rising training return
with zero evaluation completions", with n_deliver = 1. The author kept 10
from van Knippenberg (SESSION_CONTEXT). Then the pilot may be that run. Cite
it, or say why it must be rerun under [A90]. Also give the reason for the
size. Under [A90] the shaping already pays about the task's length, a trip
of 22 to 46 steps on average (`tab:instances`), so 10 is a bonus of a third
to a half of a task. Is that the point of it?

- [ ] Cite the old run, drop the pilot
- [ ] Keep the pilot
- Note:

### B2. Nothing sets n_blocked = 0.5
**Where:** p. 3, "so its size is open"; p. 2, Summary, "set by training
runs".

The argument that any n_blocked > 0 is enough reads well. But no run is
planned for it, while the summary says training runs set it. The fleet 32
tests at 0.1 and 0.0 changed nothing (`rl_review_2026-11-10`, rows
`f32_override_0.1` and `f32_override_0.0`). Cite them as the evidence that
the size matters little. Also say who pays it. The claim mask means the
centralised controller is never overridden, and the section-based one only
at zone borders, so the term acts mostly on the decentralised controller.

- [ ] Agree, cite the runs and say who pays it
- Note:

### B3. Why this rule for the crowding weight?
**Where:** p. 3, "The weight kept is the smallest that lowers blocked time
without lowering throughput".

Why blocked time and throughput, when the main result is service time? One
weight serves every controller (V-G), so what if the three disagree? Give
the tie rule. Four values times three controllers is twelve trainings. Is
that inside the budget, and which seeds? (The TODO says this is not yet
agreed.)

- [ ] Agree, give measure, tie rule and cost
- Note:

### B4. The discount against the task length
**Where:** p. 3, "which can be set against how long a task takes here".

Give the number. The mean trip is 22 to 46 steps (`tab:instances`), so 100
steps covers one task at every size. Van Knippenberg give no discount, so
the PPO paper is the only source. Fine.

- [ ] Agree
- Note:

---

## C. Names and plain words

### C1. Three names for d_obs
"Observation depth" (title, van Knippenberg's word), "cost range"
(summary), "field-of-view range" (notation table). Keep one, and say once that
van Knippenberg call it depth.

- [ ] Field-of-view range
- [ ] Observation depth
- Note:

### C2. Delivery reward and override penalty
The Method says "delivery bonus" and "override cost", this paper "delivery
reward" and "override penalty". One name each, the same in both.

- [ ] Use the Method's names
- [ ] Use these names
- Note:

### C4. "Keeps up" and "configs"
Table I.2 uses "keeps up" without saying where it is defined. Fig. I.2
says "the value in the configs", which is code language. "The value the
trained runs use".

- [ ] Agree
- Note:

---

## D. Reading order and repetition

### D1. The summary ends on symbols
Six ideas, then five symbols the reader meets only in the Setting. Name them
in words in the summary.

- [ ] Agree
- Note:

### D2. "These values shape how the learned controllers route"
What is the point of this paragraph? It mixes the crowding weight and the
field of view, and its last sentence repeats the paragraph on the field of
view. Keep it about the crowding weight.

- [ ] Agree
- Note:

### D3. Results in a different order from the Method
The Method goes depth, step costs, delivery, override, crowding, discount.
The reward subsection of the Results shows the crowding figures before the
delivery table. Put them in the Method's order.

- [ ] Agree
- Note:

### D4. Headings with a colon
"Calibration: the observation depth" prints as "...depth:" in the run-in
heading, and the style has no colons. "The observation depth", "The reward
weights", "The discount".

- [ ] Agree
- Note:

---

## E. Figures and tables

### E1. Fig. I.1 lands in the Method
It floats to the top of page 3, before the Results start. Place it after its
heading. The script reads the fixed-storage runs, so say "fixed storage" in
the caption.

- [ ] Agree
- Note:

### E2. "At two sizes" in Table I.2
Reads as two warehouse sizes, then says 8 agents. "At two values".

- [ ] Agree
- Note:

---

## F. What reads well
- The honest reading of van Knippenberg's Table 5: "the largest depth they
  tested rather than a shown optimum". Checked and true.
- The override argument. Any n_blocked > 0 makes being stopped dearer than
  yielding, said in one sentence.
- The horizon of the discount, 1/(1 - gamma) = 100, in plain words.
- The collision penalty set aside with its reason (conflict resolution
  turns the move into a wait).

## The three changes that would help the reader most
1. Say what sets n_deliver and n_blocked from runs that already exist (B1,
   B2), so the paper is not left with two open values.
2. Describe the shaping as the code now pays it, per task and nothing when
   idle (A6), together with the Method.
3. One name each for d_obs, the delivery reward and the override penalty
   (C1, C2).
