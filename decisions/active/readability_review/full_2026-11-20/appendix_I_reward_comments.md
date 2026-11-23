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

### A1. Section references
**Fixed ([A108]).** The summary and the Setting pointed to V-A (`sec:pf:env`)
for the field of view, and "the weight is the same for every controller"
pointed to V-F (`sec:pf:controllers`). The field of view (eq. 18) and the
sentence on the weight are both in V-G (`sec:pf:observations`), so all three
now point there.

### A2. What d_obs does for the centralised and section-based controllers
**Fixed ([A108]).** The text said the range "only sets the area over which
crowding is measured" for them. In the code it also caps the distance label
difference at plus or minus d_obs for every controller
(`observation.py:93`, `:170`) and sets the halo of each zone
(`training/env.py:212`). The text now says it does not limit what they see,
and names the three things it does set.

### A3. |V| in Table I.1
**Fixed ([A108]).** The column read 128, 256, 512, 1024, which is the
walkable count. The field of view also takes in shelves, workstations, docks
and parking leaves, so the share must be of the full |V|. Now 184, 348, 676,
1352, as in `tab:instances`.

### A4. "Unlike the shaping term it can change which behaviour is best"
**Fixed ([A108]).** Since [A90] the shaping restarts with every task and a
free agent gets none (`reward_function.py:130-141`). The RL review notes say
the guarantee of Ng et al. then no longer holds exactly. "Unlike the shaping
term" is cut, so the sentence now says only that the crowding term can
change the best behaviour. The Method still claims the guarantee
(`sec:method:rl`). That is for the method_reward review.

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

### A6. What the shaping term pays
**Fixed ([A109]).**
**Where:** p. 2, "A shaping term pays progress towards the agent's target".

Code ([A89], [A90]): the potential is minus the distance left in the whole
task (to the shelf plus the trip on before pickup), counted within one task,
and an agent with no task gets no shaping. The +0.9, -0.2 and -1.1 still
hold while it serves a task. Say "progress through its task, and nothing
while it has none" once the Method text is settled, so the two say the same.

- [ ] Agree, after the Method
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

### A8. Checked and matching
- The six terms and their signs (`reward_function.py:89-101`). Delivery per
  completed task, override per override, c_move per move with or without a
  task, c_wait per standing-still step of a serving agent, crowding every
  step for every agent.
- The +0.9, -0.2, -1.1. With gamma 0.99 and distance d left, a step towards
  gives 0.99 + 0.01d - 0.1, a wait 0.01d - 0.2, a step away -0.99 + 0.01d - 0.1.
- An override costs c_wait + n_blocked and a chosen wait c_wait ([A30]), so
  any n_blocked > 0 makes the override dearer.
- One range for observation, crowding (`occupancy_fraction` on the field of
  view, always) and communication (`communication_neighbours`, `d <= d_obs`).
- Every edge costs 1 (`default_edge_cost: 1.0`, `random_edge_costs: false`).
- Van Knippenberg Table 1: move -0.1, wait (off goal) -0.2, collision -2 and
  the episode ends, +10 for completing the episode, "empirically
  established, based on common practices".
- Van Knippenberg Table 5: 1024 nodes, depth 5 best for 32, 64, 128 agents,
  depth 4 (12.62) just above 5 (12.56) at 16, still rising at 5 for 32 and up.
- PPO uses gamma 0.99 in Tables 3, 4 and 5.
- Equation numbers (18), (21), (48) and sections V-G, VI-F against
  `main.pdf` of 2026-11-20.
- Every trained config holds d_obs 5, gamma 0.99, n_deliver 10, n_blocked
  0.5 and n_crowd 0.1, while Appendix B still says TBD (sweep) for all but
  gamma. Not changed, because no GAPS entry settles them.

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

### C3. "Crowding" and "window"
**Fixed ([A108]).** "The crowding δ_i(t)" is now "the crowding feature
δ_i(t)" ([A93]). Table I.1 said "window", which in the Method means what one
decision sees (zone plus halo for the section-based controller). It counts
the field of view, so caption and header now say so.

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
