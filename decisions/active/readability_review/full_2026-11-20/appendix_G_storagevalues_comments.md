# Comments on Appendix G, "Storage rule values"

Scope: `thesis/Appendices/G.StorageValues.tex`, read as its own short paper
(PDF `thesis/Appendices/G.StorageValues.pdf`, rebuilt 2026-11-20 after the
fixes below, pages 2 to 8). Checked against `slap-mapd-coupling` on `main`
(`8ba3048`): `storage/arrival.py` (`_put_away`, `_refill_scores`,
`putaway_congestion`, `refill_amounts`), `training/spec.py`
(`refill_starting_stock`, `section_top_quantile`, the derived
`vertex_capacity`), `configs/step12/fleet_<m>.yaml`, `configs/fleet_8/*.yaml`.
Results recomputed from `thesis-progress/results/G_storage/fleet_<m>/` (all
three sweeps), the first sweep at `524ef5a`, the unmerged rerun
`~/thesis_runs/tp_a93_2026-11-13/`, `done/arrival_probe_2026-10-18.md` (the
pilot), GAPS [A75], [A76], [A77], [A85], [A93], [A103], Appendix F (the drift
period).

The annotated pages are next to this file:
`appendix_G_storagevalues_comments.pdf`.

How to answer: tick one box per point and add a note if you want. Points
marked **Fixed ([A108]).** are already changed in the `.tex`.

---

## A. Is it true (checked against the code and the result files)

### A1. Fleets 32 and 64 of the congestion rerun are finished, not merged
**Where:** p. 4 (PDF), Table G.2 and "Congestion-aware storage, rerun with
the new congestion signal, keeps up at every period". The TODO comments say
"when tp-a93 finishes".

**Rows:** the queue in `~/thesis_runs/tp_a93_2026-11-13/queue.log` finished
on 2026-11-14. The rows in `results/G_storage/fleet_32` and `fleet_64` are
still the old edge rule (the congestion rows at period 100 equal the old
weight sweep at beta 1 on all 20 seeds). Recomputed from the run folder, same
way as Table G.2 (mean of paired per-seed change, 1.96 sd / sqrt 20):

| agents | standing still per pick, demand | standing still | pick travel | pick service | order service |
|---|---|---|---|---|---|
| 32 | 2.1 | -5.1 ± 2.8 | +1.3 ± 0.9 | +0.2 ± 2.4 | +0.5 ± 2.3 |
| 64 | 2.4 | -5.3 ± 2.6 | +1.0 ± 0.6 | +0.1 ± 1.6 | +1.5 ± 1.7 |

Every seed keeps up at every period. Two sentences then stop holding as
written. "A pick stands still less than 2 steps under both rules" (2.1 and
2.4 at 32 and 64). "Its small cut in standing still is largest at short
periods, about 5 percent at 50 steps" holds at 8 and 16 agents only. At 32
it is -3.0, -5.1, -4.0, -2.1 over 50 to 400, at 64 -4.9, -5.3, -5.8, -3.3.
The conclusion "no faster than demand storage" still holds at every fleet.

Run `merge_a93_period_rows.py` for 32 and 64, add the two rows, and say the
period sentence for "8 and 16 agents" or rewrite it.

- [ ] Agree, merge and add the rows
- [ ] Wait
- Note:

### A2. Demand storage does not take "the shelves with the shortest trip distance"
**Where:** p. 2, "Demand storage puts the most popular SKUs on the shelves
with the shortest trip distance. Congestion-aware storage adds to each
shelf's score β times the time picks from that shelf stood still".

This is the trip legs mistake. The code weights the two legs, and adds
βω̂ to the pick leg only, weighted by ρ̂ (`_refill_scores`, `pick_extra`).
Even by eq. (39) "adds to each shelf's score β times ω̂" is not right, since
the score adds ρ̂ β ω̂. Not fixed here. It waits for `review_trip_legs.pdf`.
Note for that proposal: its Part 5 does not list Appendix G. Three places
here touch it, this sentence, "Both terms of the congestion-aware score (39)
count steps ... a step standing still counts the same as a step of travel"
(p. 4, true only for the pick leg in the code), and the overflow of fixed
storage in "Shelf capacity" (its question 1).

- [ ] Agree, add Appendix G to the trip legs change
- Note:

### A3. The pilot ran on a much older model
**Where:** p. 3, G.4.1, "In a pilot with Token Passing, the demand rule cut
mean service time at load 0.3 by about 43% ... against 25%".

The numbers are right (22.8 of 52.8 steps and 13.0 of 52.2,
`done/arrival_probe_2026-10-18.md`). But the pilot had 6 seeds, 100 SKUs, 10
shelves, a horizon of 2000, stock arriving at the workstations by the top-up
rule, and one line per order. None of that is the model of this appendix.
A reader takes "43%" next to the 10 to 14 percent of the updated run and
wonders why the gain fell. One clause: "on an early version of the model, 6
seeds". Is that enough, or should the pilot only be named and not
quantified?

- [ ] Agree, say it was an early model on 6 seeds
- [ ] Drop the numbers
- Note:

### A4. "The only size that keeps the service level over the whole turn"
**Where:** p. 6, "so this is the only size that keeps the service level over
the whole turn."

Two pages on, the updated run shows 0.1 to 0.3 percent of lines waiting
against an aim of 1 percent, "the safety stock does a little more than it
needs to". The README of the check says the same ("A rank between would hit
it more closely"). So it is the simplest size that keeps it, not the only
one. Say "the simplest size".

- [ ] Agree
- Note:

### A5. "The safety stock of the most popular SKU of a section"
**Where:** p. 7, "With sections the safety stock is that of the most popular
SKU of a section, 16 to 18 units".

The code (`section_top_quantile`) takes the worst section, the top SKU
together with the least popular other SKUs, at the 99 percent quantile of one
period. "The most popular SKU of a section" sounds like any section. Say
"of a section whose other SKUs are the least popular, the largest share any
SKU can reach". And where does 99 percent come from? It is
`service_level: 0.99` and never named in this appendix.

- [ ] Agree
- Note:

### A6. Checked and matching
- Arrivals: one pallet of Q for every Q units ordered since the last one,
  the rest carries over (`refill_amounts`). Placed at the next update.
- Each pallet goes whole to the first shelf in the rule's order with room
  (`_put_away`, `whole`). Fixed storage tries the home shelf first and
  counts the rest as overflow.
- Shelf capacity is derived as the most room the starting stock of one shelf
  takes, 2 x (10 + safety stock) for the largest SKUs (`spec.py`, unit sizes
  0.5, 1, 2). Every SKU starts alone on a random shelf (`random_slots`), and
  fixed storage gets class-based homes, so a home shelf can hold another
  SKU's starting stock. Overflow 146 to 1740 units per run at the thesis
  values.
- Table G.1 mean fill 25, 26, 26, 27 percent (24.7, 26.0, 26.2, 27.2).
- Table G.2 matches the rows to the decimal (z interval).
- Table G.3: R = 3 λ 4000 / (|K| Q) gives 5.4, 5.4, 4.5, 4.5. Measured
  pallets per SKU per 4000 steps over the whole episode 5.0, 5.2, 4.3, 4.3.
- Put-aways 19.1 to 19.3 percent of finished tasks ("20 percent").
- Period sweep: gain 6.9 to 17.6 (8 agents), 9.6 to 17.7 (16), 11.8 to 15.7
  (32), 8.2 to 10.2 then 3.3 (64). At most 21 lines waited in a run.
- Pallet sweep: 18 to 28 percent at 15 and 30, 17.8 and 8.5 at 60 for 32 and
  64, fixed slows to 201 and 282 steps. Every seed kept up.
- First sweep stock waits 0.6 to 5.1 at 8 agents and 3.3 to 15.6 at 64 (mean
  over the three rules). The text's 5.3 and 3.6 are close, probably another
  mean. Gain 4 to 15 percent matches the README.
- Safety check numbers (5.7 to 0.0 percent, 14 percent faster, fill 24
  against 17) match the README. The rows are lost, as the README says.
- Learned first look: 21.0 to 17.3 (18 percent) and 32.5 to 29.1 (10
  percent), GAPS [A93].

### A7. Small fixes already made
- **Fixed ([A108]).** p. 2, "Each fleet runs on its own warehouse". Every
  seed generates its own warehouse (`warehouse_per_seed: true`). Now "Each
  seed generates its own warehouse and orders, and every rule compared at a
  point sees the same warehouse and orders under a seed".
- **Fixed ([A108]).** p. 4, "Both terms of the score the congestion-aware
  score (39)", a doubled name from `\nref`. Now "Both terms of the
  congestion-aware score (39)".
- **Fixed ([A108]).** p. 4, "did no better on 10 seeds". The test was at 8
  agents (GAPS [A93]). Now "did no better at 8 agents on 10 seeds".
- **Fixed ([A108]).** p. 4, "about 21 steps per pick at 8 agents and 32 at
  16 agents with the section controller". The 8-agent number is the
  decentralised controller, and the name is "section-based controller". Now
  names both.
- **Fixed ([A108]).** p. 3 and p. 8, "half the rotation period". Appendix F
  calls the 200 steps the drift period. Now "drift period".
  `B.Parameters.tex` still says "half the rotation period" (another scope).

---

## B. Reasons and sources

### B1. Why Δ = 100, when the updated run gains more at 200 and 400?
**Where:** p. 3 to 4, G.4.2.

The paragraph opens with the old reason, "half the drift period ... sees
every change in the ranking within one period", and "The first sweep ...
agrees. The gain ... fell at 400". The updated run says the opposite at 8 and
16 agents, the gain grows to 18 percent at 400. The reason left is "the value
that keeps a clear gain at every fleet size". Fig. G.1 (b) shows a second
reason that the text never uses, put-aways get slower with the period, 1.09
to 1.14 times fixed at 100 against 1.18 to 1.33 at 400. So a long period buys pick
gain with put-away time. I would lead with the updated run and these two
reasons, and keep the drift period as one clause.

- [ ] Agree
- [ ] Keep the order
- Note:

### B2. Is β = 1 checked where it matters?
**Where:** p. 4, "The congestion weight is β = 1. Both terms ... count
steps".

The reason (a step for a step) is clear and good. But under Token Passing ω̂
is 1 to 2.5 steps against trips of 15 to 49, so β barely acts. Under the
learned controllers ω̂ is 21 to 32 steps, as long as a whole trip, so there
β = 1 decides almost everything. The weight is then checked only where it
has nothing to do. Be critical. I think the hunch holds, and the
`configs/fleet_8` comment says the weight "is read again under the learned
arms". Say in one sentence that β is not tuned for the learned controllers
and why (a step for a step, no tuning on the test rule), and put it in the
Discussion.

- [ ] Agree, one sentence here and in the Discussion
- [ ] Run a small β check with a learned policy
- Note:

### B3. Why does fixed storage slow down at Q = 60?
**Where:** p. 6, "At 60 the gain falls again at 32 and 64 agents ...
because fixed storage itself slows down there."

Fixed storage goes from 143 to 201 steps at 32 agents and 180 to 282 at 64.
Why? My guess is overflow, a pallet of 60 no longer fits next to the
starting stock on the home shelf. If so, say it, because it is the reason
the curve bends.

- [ ] Agree, give the reason
- Note:

### B4. "Cheaper against fixed storage, because there are fewer of them"
**Where:** p. 6, "A larger pallet also makes the put-aways of demand storage
cheaper against fixed storage, because there are fewer of them."

Fig. G.2 (b) is put-away time per put-away, demand over fixed, 1.09 to 1.14
at Q = 10 down to 1.00 to 1.02 at 60. Fixed storage has just as few
put-aways, so "fewer of them" does not explain the ratio. What does? Maybe
with large pallets demand storage, too, has to go further out to find room.
I cannot tell from the rows. Either give the right reason or only state the
fact.

- [ ] Give the reason (which?)
- [ ] State only the fact
- Note:

### B5. The safety stock target of 1 percent
**Where:** p. 6, "against an aim of about 1 percent".

Where does the 1 percent come from? The code sizes at the 99 percent quantile
(`service_level: 0.99`, D25). Say once that the aim is the 99 percent service
level of one storage period, and that it is our choice.

- [ ] Agree
- Note:

---

## C. Names, plain words and symbols

### C1. Many names for the runs
**Where:** throughout. "the first sweep, on the first version of the
warehouse graph", "the initial Token Passing run", "an initial validation
run", "the updated Token Passing run", "the updated run", "the sweep" (G.4.5,
meaning the initial run), "the sweep" (G.4.4, the updated run), "a pilot".

That is four runs with seven names. A short list in Method, one name each
(the pilot, the first sweep, the initial run, the updated run), would let
the reader place every number. G.4.5 "In the sweep it did not work" is the
initial run. Say so.

- [ ] Agree
- Note:

### C2. Drift, turn, rotation
**Where:** p. 4, "The ranking turns once every 4000 steps and takes every
SKU through every rank". p. 3 "drift period" (now), "drift of demand" (p. 2).

The 200 steps are the drift period and the 4000 steps a "turn". The code says
rotation. Appendix F has the names. Keep "drift period" and "turn", and
say once that a turn is 20 drift periods.

- [ ] Agree
- Note:

### C3. λ_task and "the gain" are not introduced here
**Where:** p. 5, "the fleet orders three times λ_task units per step". The
gain throughout.

An appendix is read alone. λ_task appears first in a formula, and the main
loads in Table G.3 are not said to be λ_task. "The gain" is never defined. Is
it the cut in mean pick service time of demand over fixed storage, as a share
of fixed? Fig. G.1 shows it as a share (0.1), the text as percent. One
sentence in Method, "the gain is the cut in mean pick service time against
fixed storage, in percent, paired by seed", and "the main load λ_task, order
lines per step".

- [ ] Agree
- Note:

### C4. "Where picks stand still least for its distance"
**Where:** p. 2, "and a line also takes from the shelf where picks stand
still least for its distance."

I cannot follow "least for its distance". The rule is the nearest shelf
after adding ω̂ to each distance. Say "a line also takes its units from the
shelf with the smallest distance plus ω̂".

- [ ] Agree
- Note:

### C5. The broken section number
**Where:** p. 2 and p. 6, "(Section VIII-A0c)".

The same fault as D4 in `method_storage_comments.md`. The label sits under a
`\paragraph` in `5.Experiments.tex`. Here it shows twice. The fix is in
Experiments, not here.

**Fixed ([A109]).** The label moved to the subsection, so it prints VIII-A.

- [ ] Agree, fix in Experiments
- Note:

### C6. "Refill" in Fig. G.2
**Where:** p. 7, the x axis "refill size Q (units)".

[A103] made "pallet" the only name. The axis still says refill. Redraw from
`appendix_storage.py`.

- [ ] Agree
- Note:

---

## D. Reading order and repetition

### D1. Shelf capacity before the safety stock it is built on
**Where:** p. 3, G.3.1 "Shelf capacity", which points forward to G.4.5.

The capacity is derived from the safety stock, which is settled two sections
later, and its table already shows a result, the mean fill of the updated
run. Is it a method at all? I would move it to the Results, after the safety
stock, as "the shelf capacity follows". Then the fill is said once.

- [ ] Agree, move after the safety stock
- [ ] Keep it in Method
- Note:

### D2. The same numbers three or four times
- The mean fill 25 to 27 percent: Table G.1, the sentence after it, the end
  of G.4.5 and the conclusion.
- The lines that wait for stock: G.4.2 ("at most 0.9 percent"), G.4.5 ("0.1
  and 0.3"), conclusion ("fewer than 0.3"). Two different numbers for what
  looks like one fact, one at every period, one at the thesis values. Say
  which.
- The pilot: Summary, G.4.1 and the conclusion. G.4.1 also repeats the
  reason given in `sec:method:storage` (see D6 there).

- [ ] Agree, say each once
- Note:

### D3. The congestion rows sit in the period section
**Where:** p. 4, last paragraph of G.4.2.

It reads as part of the β story. Should it move into G.4.3, after Table G.2,
as "across the periods it does the same"? Then G.4.2 is only about Δ.

- [ ] Agree
- [ ] Keep
- Note:

### D4. The first sweep paragraph floats
**Where:** p. 3, "The first sweep, on the first version of the warehouse
graph, agrees. The gain held up to a period of 200 steps and fell at 400".

Which warehouse, how many seeds, and why is it still here when two newer runs
follow? If the drift-period reason is kept (B1), one clause is enough.

- [ ] Agree
- Note:

---

## E. Figures

### E1. Fig. G.1 sits in the pallet section with half a page empty
**Where:** p. 5. The figure is placed `[t]` and lands after G.4.4 starts,
with white space below. Place it right after the period text, or put the two
sweeps side by side in one figure.

- [ ] Agree
- Note:

### E2. Panel (c) "seeds that keep up" is flat at 1 in both figures
Every seed kept up at every value. One sentence in the text says it. The
panel could go, and the two other panels get more room.

- [ ] Agree, drop panel (c)
- [ ] Keep
- Note:

### E3. Panel (b) is not in the text
The put-away cost over fixed is shown in both figures but used only in B4.
See B1, it is the missing reason for Δ.

- [ ] Agree
- Note:

---

## F. What reads well
- Method says plainly that the sweeps do not choose the values, and why. Good.
- The safety stock story, cause, check, decision, in three short paragraphs.
  Easy to follow.
- The pallet count formula with words first and a check against the run.
- Table G.2 with intervals over paired seeds.
- The edge rule paragraph says why it went in one short paragraph.

---

## The three changes that would help the reader most
1. Merge the finished fleet 32 and 64 congestion rows (A1), and correct the
   two sentences they change.
2. Give Δ = 100 the reason of the updated run, including the put-away cost
   of Fig. G.1 (b) (B1), and say β is not tuned for the learned controllers
   (B2).
3. Name the four runs once (C1), and move shelf capacity after the safety
   stock so each number is said once (D1, D2).
