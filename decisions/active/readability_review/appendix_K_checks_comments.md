# Comments on Appendix K, "Simulator checks"

Scope: `thesis/Appendices/K.Checks.tex` (its own PDF, `K.Checks.pdf`, rebuilt
2026-11-20 after the fixes below, pages 2 to 4). Checked against
`slap-mapd-coupling` on `main` (`8ba3048`): `tests/unit/test_correctness_invariants.py`,
`tests/unit/test_ma2017.py`, `tests/unit/test_training_env.py`,
`tests/unit/test_policy.py`, `tests/unit/test_putaway_tasks.py`,
`tests/unit/test_arrival_rules.py`, `training/callbacks.py`,
`training/trainer.py`, `environment/multi_agent_env.py` (`EpisodeLog`),
`evaluation/evaluator.py`, `core/storage_state.py`, `core/tasks.py`,
`core/agents.py`, `benchmarks/ma2017.py`, `.github/workflows/ci.yml`. Also
`results/K_checks/ma2017/ma2017.md` and Ma et al. 2017, Table 1
(`papers/3091125.3091243.pdf`).

Tests run (only these): `test_correctness_invariants.py`, `test_ma2017.py`,
`test_training_env.py::test_replay_under_a_fixed_seed_gives_an_identical_log`.
54 passed (the coverage gate fails, as it must on a partial run).

The annotated pages are next to this file: `appendix_K_checks_comments.pdf`.

How to answer: tick one box per point and add a note if you want.

---

## A. Is it true (checked against the code and the tests)

### A3. What the tests cover
**Where:** p. 2, the list of four checks.

**Tests:** `test_correctness_invariants.py` checks all four, but only with
the two planners (prioritised A\*, Token Passing), fixed storage, the old
small generator, 4 to 6 agents and 30 to 60 steps. Other tests cover the
rest: collisions and capacity under a learned policy (`test_policy.py:393`),
replay per learned controller (`test_training_env.py:824`), replay and
capacity with stock on its way under demand storage
(`test_putaway_tasks.py:206`), replay under congestion-aware and random
storage (`test_arrival_rules.py:383,394`). Say in one sentence which
settings the tests run, so the reader does not think they ran on the
thesis warehouses.

- [ ] Agree
- Note:

### A4. Table K.2 cannot be filled as framed
**Where:** p. 3, "The four correctness checks on the runs of the thesis".

The test runs log no check, and replay needs a second run of the same
seed. Training runs did check 1 and 2 at every step (no raise means no
failure), so those rows could be filled from the training runs. Rows 3 and 4
cannot. Choices:

- [ ] Fill rows 1 and 2 from training, say 3 holds by construction and 4 is a test
- [ ] Add the checks to the evaluation and rerun
- [ ] Replace the table with the list of tests
- Note:

### A5. Check 3 cannot fail as written
**Where:** p. 2, "makes this a checkable invariant rather than merely an
assumed one".

Be critical. `Task.status()` returns one value, so a task is always in
exactly one set. The test does cross-check against the timestamps
(`test_correctness_invariants.py:145`), which catches a wrong order of
times, and `Task` refuses out-of-order times on construction. I think the
hunch holds: say it holds by construction of the task times, and that the
test checks the times are in order.

- [ ] Agree
- Note:

### A6. "Where they go"
**Where:** p. 2, "each storage update logs the units that arrive and where
they go".

The log keeps counts per arrival (`arrived_units_by_update`,
`unplaced_units_by_update`, `overflow_units_by_update`,
`split_skus_by_update`). Where the units sit is only in the trace, as a
stock line every 10 steps (`evaluation/trace.py`, `DEFAULT_STOCK_EVERY`).
Small, but say "how many arrive, and how many fit nowhere or land off their
home shelf".

- [ ] Agree
- Note:

---

## B. Reasons and sources

### B1. Why these four checks?
**Where:** p. 2, the list.

Why these four and not others, for example that a task is never handed to
two agents, or that a put-away never puts stock on a full shelf? I think
the answer is that they are the hard constraints of the PF. Say so in one
sentence, then the list reads as "each hard rule of the model has a check".

- [ ] Agree
- Note:

### B2. Why Ma et al. and why the small warehouse?
**Where:** p. 2, "The check runs the setting of Ma et al. (2017)".

Fine as is, but one clause on why: it is the paper Token Passing comes
from, and the only one with a table to compare against.

- [ ] Agree
- Note:

---

## C. Names, plain words, symbols

### C1. The appendix must read alone
**Where:** p. 2, K.1 and K.2.

`t_j^released`, `W_T`, `B_t`, `delta_i(t)`, `Q_t`, `B_t`, `C_t` and "the vertex
rule and the swap rule" all appear with no word of what they are. An
appendix is its own paper. Name each in words once ("the backlog B_t, the
tasks released but not finished") or point to Appendix A once.

- [ ] Agree
- Note:

### C2. Coding words
"accumulated online", "bitwise replay determinism", "implementation drift",
"invariant", "assertions", "per-task record", "conflict-resolution operator".
Plain words: "added up while the run goes", "the same seed gives the same
run, step for step", "a mistake in the code".

- [ ] Agree
- Note:

### C3. "Metric" and "measure"
p. 2 uses "quantity a measure needs" and then "Every metric". One name.

- [ ] Agree
- Note:

---

## D. Reading order and repetition

### D1. Text about the text
**Where:** p. 2, "These four checks are cheap, and they are also the answer
to 'how do you know the simulator implements the model of Section V.'
Section VIII reports ..."

Meta-commentary and a quoted question. The point is one sentence: the
checks show the code follows the model. Section VII-D already says it.
Cut or keep one sentence.

- [ ] Agree
- Note:

### D2. Long item 3
Item 3 holds the check and a two-clause argument. Put the check in the
list and the reason after it, in short sentences.

- [ ] Agree
- Note:

### D3. The TODO at the top
The five-part layout of `D.Warehouses.tex` is not used yet (the file says
so). K.3 already reads like a short paper. K.1 and K.2 do not.

- [ ] Agree
- Note:

---

## E. Figures

### E1. The timing figure is a placeholder
**Where:** p. 4, Fig. K.1.

The PNG says "placeholder, waits for results/timing/...". The log now has
seconds per part of the step (`EpisodeLog.stage_seconds`, written as
`seconds_<stage>` by `episode_metrics`), so it can be drawn. Or drop it,
since it is engineering only and no text refers to it.

- [ ] Draw it
- [ ] Drop it
- Note:

---

## F. What reads well
- K.3 opens with its result ("to within about 10%"), then tells how.
- The grid-to-graph conversion in one sentence, with its source.
- The paper gives neither the task sequence nor the start cells, said
  plainly, and what we did instead.
- The gap at low load is explained honestly, and what cannot be settled is
  named.

## The three changes that would help the reader most
1. Decide what the stall is (A2), then make PF, B.5 and K say the same.
2. Decide what Table K.2 reports (A4), and say which settings the tests
   run (A3).
3. Name the symbols in words so the appendix reads alone, and cut the
   closing meta paragraph (C1, D1).
