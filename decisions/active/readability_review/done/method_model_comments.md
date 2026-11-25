# Comments on "Who takes which task" and "How an agent chooses its move"

Scope: `4.Implementation.tex`, `sec:method:assignment` and `sec:method:model`
(PDF pages 37 to 40 of `main.pdf`, built 2026-11-18). Checked against the
Introduction, the Problem Formulation (`sec:pf:controllers`,
`sec:pf:observations`), `GAPS.md`, the CRAMP paper (Pham and Bera 2024,
`papers/2309.10275v3.pdf`) and `slap-mapd-coupling` on `main` (`8ba3048`):
`controllers/assignment.py`, `environment/observation.py`,
`models/gnn_encoder.py`, `models/base_model.py`.

The annotated pages are next to this file:
- `method_assignment_comments.pdf`, pages 35 to 37. It also has the
  storage notes, which repeat `method_storage_comments.md`.
- `method_model_comments.pdf`, pages 38 to 40.

The storage section is in `method_storage_comments.md` (18 Nov). Its point A1
(the trip legs) has its own proposal, `review_trip_legs.pdf`.

How to answer: tick one box per point and add a note if you want. Nothing in
the thesis has been changed.

---

## A. Who takes which task

### A1. "Same rule for every controller" said three times
**Where:** p. 37, "Every learned controller uses the same assignment rule".
It is also in the PF ("What the controllers share") and in step 2 of the
Method loop.

Drop it here and start with the rule.

- [ ] Agree
- [ ] Disagree
- Note:

### A2. Where does the rule come from?
**Where:** p. 37, "Each waiting task, oldest first, goes to the nearest free
agent".

Is it borrowed, for example a greedy rule from Ma et al. (2017), or our own?
Cite it or say so. Also say "nearest" to what: where the task picks up, the
shelf or the dock.

**Code:** matches the text (`assign_tasks`). Tasks are sorted by release time
and then task index. Each one goes to the free agent nearest its pickup
vertex, and ties go by the priority order.

- [ ] Agree
- Note:

### A3. Why do put-aways get no priority?
**Where:** p. 38, "A put-away gets no priority of its own, because oldest
first is the simplest rule".

Units on their way cannot be picked, so a put-away that waits long may hold
up picks. That is a reason to think about, not only "simplest". Be critical.
I think it holds at the main load, but maybe not at high load. Discussion?

- [ ] Add a reason
- [ ] Add to the Discussion
- [ ] Leave it
- Note:

### A4. Is task assignment part of the study?
**Where:** the Introduction, Contributions: "The thesis joins three
problems ... storage assignment, task assignment and path finding".

In the Method, task assignment is one fixed greedy rule that every
controller shares. Say that it is held fixed on purpose, and name it out of
scope.

- [ ] Agree
- [ ] Disagree
- Note:

### A5. Token Passing chooses its own tasks
**Where:** p. 38, the last line of the subsection.

This is the same point as A3 in `method_storage_comments.md`. Say it in the
loop at the start.

---

## B. How an agent chooses its move

### B1. Where the message idea comes from (CRAMP)
**Where:** p. 39, "Messages." and "No separate message layer is added,
because a linear layer in front of a mean and of the next linear layer adds
no power".

**CRAMP (Pham and Bera 2024, Section III-E):** agents are the nodes of their
own graph. The message block is a GNN with L layers of learned graph filters
and an activation, and it weights neighbours by distance. Its output is
averaged and joined with the LSTM output.

**Ours (`gnn_encoder.py`):** a message is the sender's own final vector, sent
as it is, averaged, with no layer of its own, in one round.

So the message idea is CRAMP's, but leaving out the head is our own choice.
The text should say so. The "adds no power" reason only rules out a
*linear* head, not CRAMP's nonlinear one. What is the real reason? Fewer
weights, or one round so the window stays at d_obs?

- [ ] Agree, say it is our own and give the reason
- [ ] Add a message head like CRAMP (code change)
- Note:

### B2. "Message" means two things
**Where:** p. 39, "Passing information along the graph".

m_v is what vertices pass to each other in a round. ξ_j is what agents send
to each other. "The mean of the messages it receives" is then unclear. One
name per idea, for example "what a vertex hears from its neighbours" for m.

- [ ] Agree
- Note:

### B3. Too many symbols in the message passing paragraph
**Where:** p. 39, eq. (43) to (45).

m, h, φ, ψ, ξ, AGG, E^A and ‖ come at once. AGG could just be "mean". ξ_j = h
is in eq. (44) and again in words under "Messages". ξ̄_w has a bar, which
reads as a mean, as in W̄. Is it needed?

- [ ] Agree
- Note:

### B4. No memory
**Where:** p. 40, "Memory would be the same in every controller, so it would
not change the comparison".

Be critical. I do not think that holds. The decentralised agent sees least,
so it loses most without memory, because an agent that leaves its view is
forgotten. So leaving memory out may favour the controllers that see more.
Keep the training cost reason, drop the fairness one, and add this to the
Discussion. CRAMP and PRIMAL both have an LSTM, so we take CRAMP's messages
but not its memory. Say so. Drop "(an LSTM)".

- [ ] Agree
- [ ] Disagree
- Note:

### B5. Reading order in the distance paragraphs
**Where:** p. 38 and 39.

- "What the network reads" leaves out the scaled distance, which comes two
  paragraphs later.
- Eq. (42) belongs to "Distance as a difference", not "How far the target
  is". "and the scaled distance label is η/50" after the display reads
  broken.
- "Same range under every controller" leans on the centralised window,
  which comes in VI-D. Say "also when the window is the whole warehouse".
- Why 50? The code says about 30 steps at fleet 8 and over 50 at fleet 64,
  so at 64 it is not near the range of the others.

- [ ] Agree
- Note:

### B6. Why general message passing instead of Knippenberg's graph convolution?
**Where:** p. 38, "replaces their graph convolution ... with general message
passing".

The reason is only in the appendix. One clause here.

- [ ] Agree
- Note:

### B7. Plain words
"A linear layer in front of a mean ...", "one hop", "per-edge policy head",
"(an LSTM)". These are technical words. "One hop" is new, because the
reader knows the range as d_obs.

- [ ] Agree
- Note:

### B8. Figures
- Fig. 13: the right half repeats the loop of Fig. 12. "How well things are
  going, used in training" is the value, which the text never mentions. It
  also sits under the assignment text, before its own heading.
- Fig. 14: π_θ, SCORE_θ, ‖ and 0 for no message. The left half does not
  follow the viewer style (red agent, blue arrows). The caption repeats the
  text.
- "The numbering of the edges does not affect what the policy learns" is
  followed by slots numbered by vertex. One clause saying why both hold.

- [ ] Agree, redraw
- Note:

---

## C. What reads well
- Starting with the decentralised case and then adding.
- The 48 and 47 example for the distance difference.
- The grid and graph argument for scoring moves by where they lead.
- The action mask, with Knippenberg's penalised wait as the rejected option.

## The three changes that would help the reader most
1. Say that sending messages without a head is our own choice, with its
   real reason (B1), and give the two kinds of message two names (B2).
2. Rethink the "No memory" reason and add it to the Discussion (B4).
3. Hold task assignment fixed on purpose and say so (A4). Cut the third
   "same rule" (A1).
