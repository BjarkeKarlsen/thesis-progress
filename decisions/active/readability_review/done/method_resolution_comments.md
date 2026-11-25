# Comments on "When moves still clash"

Scope: `4.Implementation.tex`, `sec:method:resolution` and Fig. 15
(`fig:workstationlock`), PDF pages 41 to 43 of `main.pdf` (built 2026-11-18,
no newer `.tex`). Checked against the Problem Formulation (`sec:pf:agents`,
`sec:pf:tasks`, `sec:pf:controllers`, `sec:pf:game`, `sec:pf:scope`), the
Method sections before it, `GAPS.md` ([A12], [A24], [A53], [A81], [A91],
[A103]), van Knippenberg et al. 2021 (`papers/knippenberg21a.pdf`, Section
4.2), `results/limitations/workstation_lock/README.md` and
`slap-mapd-coupling` on `main` (`8ba3048`):
`resolution/conflict_resolution.py`, `environment/reward_function.py`,
`environment/multi_agent_env.py`, `environment/spaces.py`, and the trace of
Fig. 15 (`~/thesis_runs/training_fixes_test/fleet8_congestion/decentralised_congestion/traces/checkpoint_000008_congestion_seed200000.jsonl`).

Points already raised in `method_controllers_comments.md` (override at zone
borders, B4) are not repeated.

The annotated pages are next to this file:
`method_resolution_comments.pdf` (pages 41 to 43 of the thesis).

Fixed and decided points are removed (full file in `full_2026-11-20/`).

How to answer: tick one box per point and add a note if you want. Nothing in
the thesis has been changed.

---

## A. Is it true (checked against the code)

### A3. The lock in Fig. 15 is not a circle of the rule

**Fixed ([A109]).** Text only. The colours of the figure are left for the author.
**Where:** p. 42, Fig. 15 and "Agent a6 stands on the only vertex out and
waits to enter w ... Neither a8 nor a6 can move first".

**Trace** (`checkpoint_000008_congestion_seed200000.jsonl`, the run of the
figure):
- t = 1157: a8 (on w) and a6 (on the vertex in front) both chose to wait.
  Only a7 asked to move, onto a6's vertex, and was overridden.
- t = 1160: a6 asks to enter w and is overridden, because a8 waits.
- t = 1500: a3 stands in front of w and chooses to wait. a8, a6 and a2 ask
  for its vertex and are overridden.

Nobody is "never ready". The lock is agents choosing to wait in front of
each other, and the rule only refuses the moves onto a waiting agent. The
text tells it as a circle of the rule ("such a circle can last"). The
figure is right, it draws the arrows the agents asked for. The text is
what is off.

This changes the story a little: the lock is learned behaviour (waiting is
cheaper than being overridden, A2), not something the rule forces. I think
that is the more honest and more interesting version, and it belongs in
the Discussion too.

Smaller: the colours are not the viewer's ([A104]). Agents to a
workstation are red, and the green diamonds of (a) are not in the legend.

- [ ] Agree, tell the lock as agents choosing to wait
- [ ] Keep the circle story (then pick a trace where it is a circle)
- [ ] Redraw in viewer colours
- Note:

---

## C. Plain words and symbols

### C1. "The order priority", "successor vertex"
**Where:** p. 41 and 42, steps 1 and 2.

"The order priority" reads like a typo. The PF calls it the priority order
and gives it no symbol, so drop `\mathrm{priority}`. "Successor vertex" is
coding language: "the vertex it asks for".

- [ ] Agree
- Note:

### C2. w, again
**Where:** p. 42, "workstation w".

w is a neighbour vertex in eq. (46) and the claim mask, and workstations
are W_1, W_2 in the PF. Use a name from the workstation family.

- [ ] Agree
- Note:

### C3. P and paired seeds

**Fixed ([A109]).** The dock draw only. "P" and "paired seeds" are left as they are.
**Where:** p. 43, "So P is random only through the arrival of orders".

- Does the reader still know P? Say "the warehouse" in words.
- The dock of each shipment is also drawn at random (PF, Orders and tasks).
  Does that count as part of the orders? Be critical, it is small, but the
  PF scope says the same, so both should agree.
- "Paired seeds" is not defined until the Experiments.

- [ ] Agree
- Note:

### C4. "The blocked time of the mean blocked time"
**Where:** p. 43, the last line.

Reads twice. "It counts towards the mean blocked time (31)".

- [ ] Agree
- Note:

---

## D. Reading order and repetition

### D1. "The masks make each move possible on its own"
**Where:** p. 41, the first line.

Only the action mask does that. The reader already knows the claim mask
stops clashes inside one decision, so say who still clashes: decentralised
agents, and agents of two zones at a border.

- [ ] Agree
- Note:

### D2. The rule is told twice, and the priority order three times
**Where:** p. 41, the prose before the list and the list.

The prose says the rule, then the list says it again. Keep one. "Drawn once
from the episode seed" is already in the PF (Who decides) and in VI-B.

- [ ] Keep the list, cut the prose
- [ ] Keep the prose, cut the list
- Note:

### D3. Agents behind a circle
**Where:** p. 42, "An agent is never ready when the agents it waits on form
a circle".

Agents queuing behind a circle are never ready either. The code says the
chain "runs into" a circle. One clause.

- [ ] Agree
- Note:

---

## E. What reads well
- "A penalty in the reward would not be enough on its own, because a
  learned policy draws its actions at random." The reason sits where the
  choice is made.
- The swap as the shortest circle.
- The lock told as a story with t = 900 and t = 1157, and the cost in tasks.
- "Whether the learned controllers learn to back out is part of what is
  measured." It says plainly what was decided ([A91]).

## The three changes that would help the reader most
1. Tell the lock of Fig. 15 as it happened: agents choosing to wait, not a
   circle of the rule. Say which controller and run it is (A3, A4), and fix
   the override penalty sentences with it (A2).
2. Fix "accepted whole" for the section-based controller (A1).
3. Cite Knippenberg for handling the agent in front first, and name the
   rule that was rejected for breaking circles (B1, B2).
