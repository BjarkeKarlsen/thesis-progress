# Comments on "What an agent is rewarded for"

Scope: `4.Implementation.tex`, `sec:method:rl`, eq. (48) (`eq:reward`), PDF
pages 43 and 44 of `main.pdf` (built 2026-11-20 15:33, printed pages 42 and
43). Checked against the Problem Formulation (`eq:potential`, the idle
target, `eq:split`, `eq:posg`, `eq:objective`), `sec:method:controllers` and
`sec:method:resolution`, Appendix C (`eq:onestepcost`), Appendix B and
Appendix I (`app:cal:reward`), `GAPS.md` ([A24], [A30], [A43], [A79], [A80],
[A81], [A93], [A107]), van Knippenberg et al. 2021
(`papers/knippenberg21a.pdf`, Section 4.1 and Table 1),
`results/training/rl_review_2026-11-10/README.md`, and `slap-mapd-coupling`
on `main` (`8ba3048`): `environment/reward_function.py`,
`environment/multi_agent_env.py::_compute_rewards`, `configs/step12/*.yaml`,
`configs/fleet_16/*.yaml`. Ng et al. 1999 and Devlin and Kudenko 2012 are not
in `papers/`, so the shaping claims were checked against the code and the
rl_review README only.

Points already raised in `method_controllers_comments.md` (B4, override at
zone borders) and `method_resolution_comments.md` (A2, A3, the lock) are not
repeated. They are answered here where this section settles them.

The annotated pages are next to this file: `method_reward_comments.pdf`
(the two pages of this section).

How to answer: tick one box per point and add a note if you want. Nothing in
the thesis has been changed.

---

## A. Is it true (checked against the code and the paper)

### A4. A detour is cheaper than a wait of the same length
**Fixed ([A109]).**
**Where:** p. 42 and 43, "So moving on is best, and yielding is cheaper than
a detour", "a policy weighs one step of waiting against one step away from
the target. This is how c_wait decides whether an agent yields or takes a
detour".

Be critical. The +0.9, -0.2 and -1.1 are one-step values. Over a whole route
the discounted shaping adds up to the end potential minus the start one, so
what is left per step is c_move = 0.1 for a move and c_wait = 0.2 for a
standing still step. A step away and back costs about 0.2 over two steps,
two waits cost 0.4. [A80] measured exactly this ("stepping away and back
costs 0.2 over two steps against 0.4 for two waits", and the fleet 32 runs
did it). So for the same delay a detour is cheaper than yielding, the
opposite of the sentence. I think the hunch holds. What c_wait really does is
make standing still dearer than moving, and the delivery bonus coming later
is what makes a long detour costly.

[A80] rejected raising c_move. So this is not a fix to the reward, only to
what the text claims. It also belongs in the Discussion, next to the back
and forth seen at fleet 32.

- [ ] Agree, say what the step costs do over a route
- [ ] Disagree
- Note:

### A5. The crowding term reads delta_i(t) before the move
**Where:** p. 43, "The last term, the crowding term ... gives the policy a
direct signal to avoid crowds".

**Code:** `_compute_rewards` gets "delta_i(t) at the step the action was
chosen in". So the action at t cannot change the term at t, only the term at
t+1. That is fine for a discounted return, but the signal is one step late
and partly charges an agent for others walking into its field of view. Be
critical, it is small. One clause would do.

- [ ] Agree, one clause
- [ ] Leave it
- Note:

---

## B. Reasons and sources

### B1. Why shaping at all?
**Where:** p. 42, the first term.

Knippenberg has no shaping, and we take his step costs. Why do we add it?
I think the reason is that the delivery bonus is many steps away and the
target is usually outside the field of view, so without it the agent hears
about progress only at the end. One sentence.

- [ ] Agree
- Note:

### B2. The delivery bonus is borrowed, but changed
**Where:** p. 43, "The delivery bonus ... set in Appendix I.4.2".

10 is Knippenberg's "Complete episode", paid once per episode when all
agents reach their goals. We pay it per task. The appendix TODO says so, the
section does not. Say where it comes from and that we pay it per task.

- [ ] Agree
- Note:

### B3. Why an override penalty on top of c_wait?
**Where:** p. 42, "pays extra when conflict resolution stops it".

[A43] did not take Knippenberg's collision penalty (-2), but kept n_blocked
= 0.5, which has no source (appendix TODO). The rl_review runs with 0.1 and
0 had no effect on the fleet 32 collapse. What does it buy? I think it is
that a refused move teaches the agent that the vertex is taken, which a wait
cost alone does not. One clause, and say it is ours.

- [ ] Agree
- Note:

### B4. Why the crowding term, when delta is already seen?
**Where:** p. 43, "that is accepted because it gives the policy a direct
signal to avoid crowds".

delta_i(t) is already in the observation. So the reason must be that seeing
a crowd does not by itself make it costly. Is that the reason? And this is
the one term that changes which behaviour is best, so say it is our own.

- [ ] Agree
- Note:

---

## C. Names, plain words, symbols

### C1. One name for being overridden
**Where:** p. 42 and 43, "conflict resolution stops it", "is overridden",
"Being stopped", "the override cost", and "the override penalty" in
`sec:method:resolution`, weight n_blocked.

Seven words for one thing. Use "overridden" and "the override term", as
`sec:method:resolution` does. n_blocked looks like the blocked time of eq.
(31), which also counts chosen waits. Rename it, for example n_override, and
update the notation table.

- [ ] Agree, and rename n_blocked
- [ ] Agree, keep n_blocked
- Note:

### C3. omega, three times
**Where:** p. 42, "omega_i(t) = omega_j(t) of the service-time split (30)".

omega_j is the task's blocked indicator, omega_i the agent's, and
omega hat_t(v) the shelf's standing still since [A93]. A reader cannot tell
omega_i from omega_j when i and j are just indices. Is omega_i needed? The
term could read c_wait omega_j(t) with sigma(j) = i, or say it in words.

- [ ] Agree, drop omega_i
- [ ] Keep it
- Note:

### C4. Plain words
- "as it drives there". Say "moves there".
- "counted in edge costs". All edges cost 1 ([A43]), so say "in the same
  unit, one step".
- "The last term, the crowding term, charges for crowding." Says nothing
  new. "The crowding term charges an agent for every agent in its field of
  view."
- "c_wait of the one-step cost (C.7)" sends the reader to Appendix C for a
  number we can just name. Drop the reference.

- [ ] Agree
- Note:

---

## D. Reading order and repetition

### D1. The numbers come before what they are made of
**Where:** p. 42, "Close to the target, a step towards it is worth about
+0.9, a wait -0.2 and a step away -1.1".

Good to lead with words and numbers. But they need gamma and c_move, which
come in the fifth paragraph, and gamma is a training value the reader has
not seen (Appendix B says TBD, the configs 0.99). Either give the values
here in one sentence, or move the numbers to the c_move paragraph and keep
the opening in words.

- [ ] Give the values in the opening
- [ ] Move the numbers down
- Note:

### D2. "Yielding is cheaper" three times
**Where:** p. 42, "yielding is cheaper than a detour", "yielding is never
dearer than being stopped", and p. 43, "This is how c_wait decides whether
an agent yields or takes a detour". The +0.9, -0.2 and -1.1 also appear
twice.

Say it once, and with A4 decide what it says.

- [ ] Agree
- Note:

### D3. A worked example of one task
With [A90] the reward over one task is easy to show: a task of 12 steps
earns about 12 from shaping, plus 10 at delivery, minus 1.2 in move costs,
and each wait costs 0.2. This would replace the "charged once" paragraph and
make A2 and A4 concrete. Numbers from the fleet 8 trip in the README (about
12 steps).

- [ ] Agree
- Note:

---

## E. Figures

None in this section, and none needed if D3 is taken. A small table of the
six terms with their value and source (Knippenberg, ours, TBD) could replace
the scattered values. Optional.

- [ ] Add the table
- [ ] No
- Note:

---

## F. What reads well
- The opening says in plain words what is paid and what is charged.
- "Standing still costs time, and the reward says so." The reason sits with
  the term, and the order (yielding never dearer than being overridden) is
  argued.
- The c_move paragraph names the source, the values and that they are taken
  as they are.
- The crowding term says plainly that it can change the best behaviour, and
  why that is accepted.

## The three changes that would help the reader most
1. Rewrite the shaping part to match the code: Phi as the distance left in
   the task, progress counted within a task only, no shaping for idle
   agents, and say the guarantee holds only within a task (A1 to A3). Log
   [A89] and [A90] in GAPS.
2. Fix what the step costs claim. Over a route a detour is cheaper than a
   wait of the same length, so "yielding is cheaper than a detour" is not
   true (A4, D2).
3. Name the override once and say who pays it under each controller (C1,
   C2).
