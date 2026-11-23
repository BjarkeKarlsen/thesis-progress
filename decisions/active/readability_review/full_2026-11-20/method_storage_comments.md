# Comments on the Method opening and "Where arriving stock goes"

Scope: `4.Implementation.tex`, the Method opening, Fig. 12 and `sec:method:storage`
(PDF pages 35 to 37 of `main.pdf`, built 2026-11-18). Checked against the
Problem Formulation (`sec:pf:storage`, `sec:pf:tasks`), the Introduction and
`slap-mapd-coupling` (`storage/arrival.py`, `environment/multi_agent_env.py`,
`configs/fleet_8/decentralised.yaml`).

The annotated pages are next to this file:
`method_storage_comments.pdf`.

How to answer: tick one box per point and add a note if you want. Nothing in
the thesis has been changed.

---

## A. Is it true (checked against the code)

### A1. The shelf order in the code is not the one in the text
**Where:** p. 37, eq. (39) and "Both legs carry the same ρ̂". Also p. 36,
fixed storage "nearest shelf by d^trip_0", and p. 37, demand storage "gives
each the nearest shelves by d^trip".

**What the text says:** a shelf is ranked by ρ̂(k) · (d^trip + β ω̂(v)).
Both trips get the same weight, "because a SKU is put away about as often as
it is picked".

**What the code does:** our runs use pallets (`refill_units: 10`) and agents
carry the put-away. In that setup all three rules rank each SKU's shelves in
`_refill_scores`:

    ρ̂(k) · (pick trip + β ω̂(v))  +  (units of k ordered per step / Q) · (put-away trip)

So the put-away trip gets its own weight, which is how often a pallet comes.
Standing still is added to the pick trip only. A line asks for 1 to 5 units
(3 on average) and a pallet holds 10, so a SKU is put away about 0.3 times
per pick. The text's "about as often" does not hold. This is also why demand
storage gives each SKU its own shelf order, not one shared "nearest" order.
Fixed storage sends pallets that do not fit at home on by this order too.

**Question:** should the text follow the code (code decides, from
2026-11-18), or was the plain d^trip meant? If the text changes, the slotting
cost D in eq. (38) changes with it.

- [ ] Agree, change the text to the code
- [ ] Change the code to the text
- [ ] Disagree
- Note:

### A2. The guessed section differs a little from the code
**Where:** p. 36, "the section most of the SKU's order lines went to in the
last storage period".

**Code:** a SKU with no line in the period keeps the last section it had. A
SKU with no line yet uses the mean over all workstations. Both are small
points. Should they go in the text, or in Appendix C?

- [ ] Agree, add to the text
- [ ] Add to the appendix only
- [ ] Leave it
- Note:

### A3. Token Passing does not run quite the same loop
**Where:** p. 35, "All controllers, and the Token Passing reference, run in
the same loop" and step 2 "by the same rule for every controller".

"A reference point" says Token Passing chooses its own tasks and does not use
the assignment rule. So step 2 is not the same for Token Passing. Say "every
learned controller" in step 2, or say Token Passing differs in steps 2 and 3.

- [ ] Agree
- [ ] Disagree
- Note:

### A4. What happens to a pallet that fits nowhere?
**Where:** p. 36, "A pallet that fits nowhere is not placed." (The Problem
Formulation says the same.)

**Code:** it is counted as not placed and the SKU's count of ordered units
still resets. So those units are gone, and the next pallet only comes after
another Q units are ordered. Do we say this, and does it belong in the
Discussion? It may never happen at the main load. Appendix E measures it.

- [ ] Agree, say it
- [ ] Leave it, it does not happen in practice
- Note:

---

## B. Repetition of the Problem Formulation

Most of this section was written before the Problem Formulation got its
readable version ([A103], [A105]). The Problem Formulation now tells much of
the same, so the Method could keep only what is new: each rule's order, the
score, the five-reading formula, the tie rules and the reason for counting
per step.

### B1. The ladder paragraph repeats the list of rules
**Where:** p. 35, "The three storage rules form a ladder…"

The Problem Formulation lists the three rules in "The storage rule" with the
same words. "The gap between the last two shows what reading … adds" is said
in the Problem Formulation too, under "Under congestion-aware storage".
"Ladder" is a nice picture, but we tell the rules a third time (Intro, PF,
here). Also, what is "the storage half of RQ2"? What is the other half, the
pickup rule? If so, say it, or drop "half".

- [ ] Agree, cut to what is new
- [ ] Keep the ladder as a short reminder
- Note:

### B2. Stock stays put, and a pallet can go unplaced
**Where:** p. 36, "Stock already on a shelf stays where it is" and "A pallet
that fits nowhere is not placed."

Both are in "The storage update" of the Problem Formulation, with an
example. The "one SKU at a time, each pallet whole onto the first shelf with
room" part is new and should stay.

- [ ] Agree
- [ ] Disagree
- Note:

### B3. "The thesis's own, because the classic problem has no traffic"
**Where:** p. 36, the blocking cost K.

Almost the same sentence is in the Problem Formulation (congestion-aware
bullet) and in the Introduction (contribution 2). Here it is the third time.
Keep it in one place. I would keep it where the rule is first named, in the
Problem Formulation.

- [ ] Agree
- [ ] Disagree
- Note:

### B4. "Greedy, not the best placement" is said four times
**Where:** p. 36, "Neither rule searches for the smallest value". p. 37,
"greedily and not exactly", twice. Problem Formulation: "The rules are
greedy … none of them claims to find the best possible placement."

Once is enough. Keeping "this is a score, not the objective" here is fine,
because that is new.

- [ ] Agree
- [ ] Disagree
- Note:

### B5. The demand estimate paragraph
**Where:** p. 37, "The demand estimate is the rate per step of the order
estimate (7)…"

Eq. (7) is already per step, so the first sentence repeats it. The new part
is the reason: per step keeps β comparable when Δ changes. "If no order was
released in a period, nothing was picked and nothing arrives" floats on its
own. What do we want to tell the reader with it?

- [ ] Agree
- [ ] Disagree
- Note:

### B6. The standing-still paragraph
**Where:** p. 37, "The time standing still comes from the picks…"

The Problem Formulation already says a shelf has few picks, that one period
jumps up and down by chance, that we look back over several periods, and
that a shelf with no pick reads 0. New here are the five readings, that a
shelf with no pick keeps its average, and eq. (40). Point back and keep the
new part. Why five? [A93] says a plain average was chosen over a fading one
because it is easier to explain. That reason could go in one clause.

Be critical: W̄_s(v) may be read as the workstation W_1 of the pickup
example. I think the risk is small, because the bar and the (v) set it apart.
Still, another letter is cheap.

- [ ] Agree
- [ ] Disagree
- Note:

### B7. The pickup rule under congestion-aware storage
**Where:** p. 37, "Under congestion-aware storage the pickup rule also
adds…"

"Under congestion-aware storage" in the Problem Formulation says this, with
the example and the reason why demand keeps the nearest shelf. Only the tie
rule ("the lower vertex number goes first") is new. It could join the ties
paragraph below, which then says ties once. Code: matches, ω̂ is added to the
distance to the line's workstation, with no β.

- [ ] Agree, keep only the tie rule
- [ ] Disagree
- Note:

---

## C. Repetition of the Introduction

### C1. "Only the controller differs"
**Where:** p. 35, "All controllers share the same parts, and only the step
where agents choose their moves differs."

The Introduction says the controllers are "trained the same way … so they
differ only in how much one decision covers". Contribution 3 says "between
two runs only the storage rule or only the controller changes". Be critical:
I think the Method may say it again, because here it is the reason for the
shared loop. One short sentence would be enough.

- [ ] Keep it, it is the reason for the loop
- [ ] Shorten
- Note:

### C2. Congestion-aware storage told three times
**Where:** p. 35, "Congestion-aware storage does the same, but it avoids
shelves where picks often stand still, and it also picks from them less."

The Introduction says "steer both new stock and picks away from those
shelves". The Problem Formulation says it again. See B1.

- [ ] Agree
- [ ] Disagree
- Note:

No other repeats of the Introduction found in this part.

---

## D. Reading order, names and symbols

### D1. β and x^new in eq. (38)
**Where:** p. 36, eq. (38).

β is used in D + βK two paragraphs before it is explained (eq. 39). x^new is
used only in eq. (38). Would the cost paragraph read better after the three
rules, as their summary? Then β is known, and the two "greedily and not
exactly" sentences (B4) go away.

- [ ] Agree, move it after the rules
- [ ] Keep it, define β in it
- Note:

### D2. The list and Fig. 12 tell the same six steps
**Where:** p. 35 and 36.

Keep one. I would keep the figure and one sentence. "The subsections follow
it" is not quite true, because storage (step 6) comes first. Say why storage
comes first, for example because the Problem Formulation has the same order,
or drop "follow it".

- [ ] Agree
- [ ] Disagree
- Note:

### D3. Fig. 12 words
**Where:** p. 36, Fig. 12.

"Swaps with the controller", "revise joint action to satisfy vertex and swap
constraints", "apply F to update x_t" and "lifecycle" are code words or
symbols the text around it does not use. The Problem Formulation says "A
task's life", not "lifecycle". The caption says "routing", but the text says
"chooses its move". Use the same short words as the list.

- [ ] Agree, redraw
- [ ] Disagree
- Note:

### D4. Home shelves of fixed storage
**Where:** p. 36, "(Section VIII-A0c)".

The reference prints as "VIII-A0c", because the label sits under a
`\paragraph` in `5.Experiments.tex`. The paragraph it points to (the
warehouses) does not say how home shelves are chosen. In the main text
nothing says where "most popular" comes from at the start. Only Appendices E
and G talk about home shelves. Where should the reader learn it?

- [ ] Agree, explain here in one sentence
- [ ] Point to an appendix
- Note:

**Fixed ([A109]), the number only.** The label moved to the subsection, so it
prints VIII-A. Where the reader learns how home shelves are chosen is still
open.

### D5. Why the demand rules use a guessed section
**Where:** p. 36, "The demand rules do not know a SKU's section h(k)."

We give the stand-in but not the reason. Is it because a rule may only read
the orders that came in, as the Problem Formulation says? Then one clause.
Fixed storage does use h(k). Appendix C says so, the main text does not.

- [ ] Agree
- [ ] Disagree
- Note:

### D6. Arriving stock rather than moving stored stock
**Where:** p. 37, "Placing arriving stock was chosen over relocating stored
stock, because it changes the layout more…"

This is a modelling choice, so should its reason sit in the Problem
Formulation, where the choice is made ("decides where arriving stock goes,
and nothing else")? "Changes the layout more" I cannot follow. More than
what? The paragraph also mixes four things: the choice, ties, same arrivals
and where the values are set.

- [ ] Agree, move the reason to the PF
- [ ] Keep it here, reword
- Note:

### D7. Small practical faults
- `\nref` after words that already name the thing doubles them: "the
  arriving stock the storage update (8)", "arriving units the arrivals (6)",
  "D of the slotting costs (38)" (twice), "service time the service-time
  split (30)".
- "(C.2) (Appendix C.1)", two references in a row for the trip distance.
  One is enough.

- [ ] Agree
- Note:

---

## E. What reads well
- The trip-distance paragraph. Each leg has its reason right where it is set.
- Demand storage cites Heskett and de Koster where it is used.
- The two-shelf example before eq. (39).
- Words before the equation in the standing-still paragraph.

---

## Corrections to my first chat summary
These points from the first pass were wrong and are not in this file:
- "ρ̂ and ω̂ are used before they are defined." Both are defined in the
  Problem Formulation ("What the rule reads"). Only β is used early (D1).
- "No reason for pallets of Q." The Problem Formulation explains pallets and
  the (R,nQ) policy, and one agent carries a pallet in one trip.
- "Add why only congestion-aware storage changes the pickup rule." The
  Problem Formulation already has it (now B7, a repetition).
- "We never say why the storage rules are hand-made." The Problem
  Formulation says it ("The rules are made by hand and not learned").
- "The storage rule differs too, so 'only stage 3 differs' is false." The
  sentence is about the controllers, and storage is held fixed when they are
  compared. Only the Token Passing point holds (A3).
- "Does the reader still have Q_t?" It is defined in "A task's life".
- "'Four workstations' may not hold for every size." Four per section is
  fixed by the model.
- "The reader does not know the sweep yet." The Problem Formulation already
  mentions the Δ sweep.
- The code mismatch is wider than I first said (A1). It covers all three
  rules, not only congestion-aware storage.

## The three changes that would help the reader most
1. Settle A1. Either the text follows the leg weights of the code, or the
   code goes back to plain d^trip.
2. Cut the section to what the Problem Formulation does not already say
   (B1 to B7), and put the cost of eq. (38) after the rules (D1).
3. Fix the Token Passing sentence (A3), the broken reference (D4) and the
   doubled `\nref` words (D7).
