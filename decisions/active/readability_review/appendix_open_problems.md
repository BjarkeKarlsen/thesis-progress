# Open problems in the appendices

Written 2026-11-25, after [A143] (Appendix C). Each point says what is wrong,
where it is, and what is needed. Tick a box or add a note.

---

## 1. Left open from the Appendix C review

### 1.1 The learned overflow share has no source
**Where:** was in Appendix C under the trip legs, now removed ([A143]).

The text said that at 16 agents a pallet misses its home shelf for about
8 percent of the arriving units under Token Passing, and 40 to 60 percent
under the learned controllers. The 8 percent fits Appendix E (6 to 10
percent, `app:load:validity`). I found no rows for the 40 to 60 percent.
It came in with [A122] on 2026-11-23, likely from the first runs, not the
long ones.

The number is not in the thesis now. The question is whether it should be.
It would show that the learned fleets fall behind and fill the shelves.

- [ ] Leave it out
- [ ] Recount from the long 16-agent runs and add it to Appendix L, "Stock in the test runs"
- Note:

### 1.2 Blocked time against the shelf estimate was cut
**Where:** was Appendix C, `app:measures:blocked`, now removed ([A143]).

It said that W_T looks back over a run and the shelf estimate is a forecast
that steers storage. Nothing pointed to it. If you want the difference
stated, one sentence fits where W_T is defined in `sec:pf:measures`.

- [ ] Fine as cut
- [ ] Add one sentence in the Problem Formulation
- Note:

### 1.3 Files that nothing includes
**Where:** `thesis/Chapters/`.

`main.tex` does not include these, and no other file does:
`2.Notation.tex` (an older copy of `A.Notation.tex`), `tmp1.tex`,
`5.Experiments.before.*`, `Project.tex`, `Thesis_idea.tex`, `Timeplan.tex`,
`Helper.tex`. `2.Notation.tex` is the risky one. Review comments keep
asking to edit it, and an edit there changes nothing in the PDF. Deleting
them changes the Overleaf project, and they stay in its history.

- [ ] Delete them
- [ ] Keep them
- Note:

---

## 2. Numbers that disagree or are not counted

These change what a reader sees in the results. They come first.

### 2.1 Decision time at 16 agents disagrees with itself
**Where:** `L.Results.tex:456`, "Decision time as the fleet grows".

The step time test gives 42 ms for centralised and 24 ms for section-based
at 16 agents. The test runs earlier in the same appendix give 110 and 73 ms.
Both cannot stand as they are. One guess, not checked, is that the step time test
times one decision alone, while the test runs also time the environment, or
run on a busier machine. This needs checking in the code and the run
setup, then one sentence saying what each number measures.

- [ ] Find out why, then decide
- Note:

### 2.2 The stalled-runs column was never counted
**Where:** `L.Results.tex:186`, `tab:app:check:16`.

`stall_length` was unset when the table was made. The TODO says to count it
with 36 / arrival_rate when the table is rebuilt on the long runs.

### 2.3 The stall count waits for every long run
**Where:** `H.Horizon.tex:157` ([A118]).

"33 of the 220 test runs stall" counts the 11 long runs that were home on
2026-11-23. Recount when every long run is evaluated.

### 2.4 Centralised demand at 16 agents is still TBD
**Where:** `L.Results.tex:233` (red cell), also `tab:exp:locks`.

This is item 2 of the to-do list in `SESSION_CONTEXT.md`, and waits for eval-pc.

### 2.5 The served figure uses the old counts
**Where:** `L.Results.tex:134`. `fleet16_served.png` should be redrawn from
the counts of `served_counts.py` ([A96]).

---

## 3. Decisions only you can make

### 3.1 Appendix J, Model and training
- **Line 29.** The Summary has no answer yet. The training runs are done,
  so the answer can be written now.
- **Line 91.** Were the epochs, minibatch size and entropy coefficient
  tuned in a small pilot? Or is it "not tuned, the same for every
  controller"?
- **Lines 191 and 199.** The reason for L = 2 message-passing rounds and
  for width 32. One reason each is enough.
- **Line 214.** "500 000 environment steps, open". The long runs were
  2 000 000 more steps on top (line 232). Say which budget the thesis
  reports.
- **Line 217.** One or two sentences on the training curves.
- **Line 234.** Should the four PPO values be marked "cited" in
  Appendix B?

### 3.2 Appendix F, Demand drift
**Line 333.** Should Appendix B list the Zipf exponent, drift period and
drift step as "tested"?

---

## 4. Structure

### 4.1 Appendix K does not follow the five-part form
**Where:** `K.Checks.tex:8`.

Every experiment appendix uses Summary, Setting, Method, Results,
Conclusion. K is still a list of checks. Its question would be "does the
simulator implement the model?". Either rewrite it in the five parts, or
call it reference material in `overview.tex` and `LATEX.md`, next to A, B
and C.

- [ ] Rewrite in five parts
- [ ] Call it reference material
- Note:

### 4.2 Appendix L has no plan in the text
**Where:** `L.Results.tex:13`.

The TODO says every measure, in the order of `measures_catalogue.md`. Check
that the tables follow that order before submission. Line 361 still needs a
sentence only where a result needs explaining.

### 4.3 Appendix C is now only a reference
After [A143], C holds the sources side by side, the keep-up count and the
formal statements. That is fine as reference material. It has no question
of its own, so it should not grow back into a place for worked examples. A
new example belongs in the chapter that needs it.

---

## Suggested order
1. 2.1 decision time (a wrong number is worse than a missing one)
2. 2.4, 2.2, 2.3, 2.5 once the evaluations are in
3. 3.1 Appendix J decisions
4. 1.1 to 1.3, 3.2, 4.1
