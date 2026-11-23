# Comments on "Implementation"

Scope: `4.Implementation.tex`, `sec:implementation` with `sec:impl:simulator`,
`sec:impl:logging`, `sec:impl:cost` and `sec:impl:validation` (PDF pages 45
and 46 of `main.pdf`, built 2026-11-20 15:33). Checked against the Problem
Formulation (`eq:runtime`, the task stages, `eq:throughput`), the Experiments
(`sec:exp:setup`, "Compute environment"), Appendix B (`tab:evalparams`),
Appendix E (`app:cal:load`, `app:load:first`), Appendix K (`app:repro`),
`GAPS.md` ([A10], [A20], [A24], [A31], [A93], [A95], [A96]), van Knippenberg
et al. 2021 (`papers/knippenberg21a.pdf`, Section 6.2, Table 4) and
`slap-mapd-coupling` on `main` (`8ba3048`): `environment/multi_agent_env.py`
(`EpisodeLog`), `core/tasks.py`, `core/graph.py`, `evaluation/evaluator.py`,
`training/env.py`, `training/policy.py`, `training/callbacks.py`,
`training/evaluate_run.py`, `planners/driver.py`,
`tests/unit/test_correctness_invariants.py` (run today, 42 passed),
`.github/workflows/ci.yml`, and the workspace `bedtime.bash`.

The annotated pages are next to this file: `implementation_comments.pdf`
(pages 45 and 46 of the thesis, before the fixes below).

How to answer: tick one box per point and add a note if you want. Only the
points marked **Fixed** were changed in the thesis, tagged `% [A108]`.

---

## A. Is it true (checked against the code and the paper)

### A1. Where the four checks run
**Fixed ([A108]).** The text said "Four checks run on every experiment, not
only during development". The code runs them like this:
- `tests/unit/test_correctness_invariants.py` runs all four, on small
  warehouses (4 to 6 agents, at most 60 steps, fixed storage), with the two
  planners only. CI is commented out in `.github/workflows/ci.yml`, so the
  suite runs only when someone runs it.
- `training/callbacks.py` checks no vertex or swap conflict and capacity at
  every timestep of every training episode, and raises if one fails.
- The task stage is computed from the task's times (`core/tasks.py`
  `Task.status`), so a task can only be in one stage. Not checked at run
  time, it cannot fail.
- The test runs (`evaluate`) check nothing.

New text: "Four checks test the simulator. [the four]. A test suite runs all
four on small warehouses. The first two also run at every timestep of every
training episode, and a run stops if one fails. A task's stage is read from
its times, so it can only have one."

Still open, outside this section: Appendix K (`app:repro`,
`app:repro:checks`) still says "on every experiment", and `tab:app:checks`
wants counts over "the runs of the thesis", which the code does not log.

- [ ] Keep the fix, and let Appendix K say the same
- [ ] Add the two checks to the test runs, then say "every run"
- Note:

### A2. "Every measure is added up while the run goes"
**Where:** p. 46, "Every measure is added up while the run goes, not
computed again at the end".

**Code:** the log adds up what the measures need (backlog every timestep,
blocked timesteps per task, crowding sums, times). The measures themselves
(service time, throughput, the runtime) are computed at the end from the log
and the task times (`evaluator.py:662`). Proposal: "What each measure needs
is logged while the run goes, so nothing is worked out again from the
replay."

- [ ] Agree
- Note:

### A3. Blocked is a count per task, not a record per timestep
**Where:** p. 46, "The backlog and whether each active task is blocked are
logged every timestep".

**Code:** the backlog is a list with one entry per timestep. Blocked is
checked every timestep but kept as a count per task, plus the longest run of
blocked timesteps in a row for the stall count (`EpisodeLog`
`blocked_ticks_by_task`, `longest_blocked_run_by_task`). Appendix K says
"one bit per timestep". Proposal: "Each task counts the timesteps it is
blocked." Also, "trace" is not defined anywhere before (see C2).

- [ ] Agree
- Note:

### A4. Where the load levels and f_up come from
**Where:** p. 46, "The load levels and f_up come from a pilot of Token
Passing (Appendix E.4.4)".

E.4.4 sets f_up = 0.8 and says it is not varied. The Token Passing run is
E.4.5 (`app:load:first`). Its main loads are 0.105, 0.15, 0.18 and 0.24 (one
per fleet), but `tab:evalparams` gives 0.15, 0.25, 0.3 and 0.4, the values of
the older three-agent pilot of [A31]. I did not fix this, because which
values hold is the author's call.

- [ ] Load levels from E.4.5, update `tab:evalparams`, point there
- [ ] Other
- Note:

### A5. What the runtime numbers really are
**Where:** p. 46, "The time per decision is logged separately for assignment
... The learned controllers run their policy on its GPU".

**Code:**
- The log keeps assignment and routing apart, but the reported measure
  kappa_T adds them (`evaluator.py:662`), as the PF defines it. Say that the
  reported number is the sum, and the split is only in the log.
- Routing time for a learned controller also holds building the
  observations (`training/env.py:538`), not only the network. I think that
  is right, but say it, since Token Passing has no such step.
- The usual test runs (`bedtime.bash`, `EVAL_ARGS` without `--gpu`) run the
  policy on the CPU, one core per run. The GPU numbers come from the
  separate run of [A95] with 3 test seeds. Say runtime comes from that run.
- [A95] still lists Token Passing's time on the same PC as open.

- [ ] Agree, say the three things
- Note:

### A6. Agents choose in turns under two controllers
**Where:** p. 45, "All agents act at the same time. Observations, rewards
and actions are passed as one entry per agent".

Be critical. Under the centralised and section-based controllers a timestep
is split into turns, and each turn passes only the agents that choose in it
(`training/env.py`, docstring lines 9 to 18). Only the moves happen
together. The sentence is true for the moves, but the reader just learnt
about turns in "Choosing together" and will wonder. PettingZoo is not used
in the code, it is only cited for the shape of the interface. I think the
hunch holds. Say "All agents move at the same time" and drop PettingZoo, or
say it is cited only for the shape.

- [ ] Agree
- Note:

### A7. "To within about 10%"
**Where:** p. 46, "reproduces the published results of H. Ma et al. (2017)
to within about 10%".

K.3 gives 8% shorter on average, ranging from 34% shorter to 3% longer over
30 settings. "To within about 10%" reads as every setting. Say "8% shorter
on average".

- [ ] Agree
- Note:

### A8. "These checks show that the simulator implements the model"
**Where:** p. 46.

Be critical. The four checks show that the hard rules hold (no clash,
capacity, task stages, replay). They say nothing about whether the storage
rules, the observations or the reward match the text. I think the hunch
holds. Say "These checks show that the hard rules of the model hold".

- [ ] Agree
- Note:

### A9. Fixed small mistakes
- **Fixed ([A108]).** "Section VIII-A0c" (p. 45). `sec:impl:instances` is a
  label on a `\paragraph` in the Experiments, so it prints a broken number.
  Now points to `sec:exp:setup` (VIII-A). The same broken number appears
  wherever else `sec:impl:instances` is cited (`4.Implementation.tex:99`,
  Appendix K), so the root fix is in `5.Experiments.tex`.
- **Fixed ([A108]).** "the storage score the congestion-aware score (39)"
  and "for assignment the assignment rule (41)". `\nref` already prints the
  name, so the word before it doubled it.
- **Fixed ([A108]).** "whether it is a pick or a put-away". Tasks are also
  shipments (`core/tasks.py:50`, `kind` is pick, putaway or ship).

### A10. Checked and matching the code
- All shortest distances are computed once per warehouse
  (`core/graph.py:188`, `_all_pairs_shortest_paths`).
- The parts named (tasks, assignment, routing, conflict resolution, storage
  update, logging) are the parts of the step, and a controller is the
  routing part only (`planners/driver.py`, `training/env.py`).
- Each task records release, assignment, pickup and finish times, and its
  order and line (`core/tasks.py`, `EpisodeLog.order_line_by_task`).
- Backlog logged every timestep (`EpisodeLog.backlog_by_t`).
- Assignment and routing timed apart (`multi_agent_env.py:1020`,
  `planners/driver.py:42`, `training/policy.py:73`).
- Training wall time logged per iteration (`training/callbacks.py:354`).
- The four tests exist and pass (42 passed, 2026-11-20).
- Parking of idle agents is in the Method (reward section), so it is not a
  choice the simulator adds.

---

## B. Reasons and sources

### B1. Knippenberg's single-agent setup, for the cost of one run per agent
**Where:** p. 46, "Computational cost".

Carried forward from `method_controllers_comments.md` A4. The centralised and
section-based controllers run the network once per agent per timestep, m
runs. The cost section is where the reader asks whether that is affordable.
Knippenberg, Section 6.2 and Table 4: the single-agent setup takes the whole
graph and gives one output per agent. It solved far fewer instances as the
graph and the fleet grew (2048 nodes, 64 agents: 7.6% against 58.2% for the
multi-agent setup, 24 hours of training), and he names computational
efficiency as the reason. Be critical: his table counts solved instances,
not time per decision, and his multi-agent setup is itself one run per
agent. So it supports one run per agent on a local window, not that m runs
are cheap. One clause, with that care, is enough.

- [ ] Agree, add one clause here
- [ ] Keep it in "Choosing together" only
- Note:

### B2. What the runtime answers
**Where:** p. 46, "Runtime is one of the measured results".

No research question asks about runtime. The PF calls it a "reported
measure" and cites Ma et al. for it. Say here in one clause why we report
it (a learned router is only of practical use if it decides fast enough),
which the paragraph already says later. Lead with that.

- [ ] Agree
- Note:

---

## C. One name per idea, plain words

### C1. Four names for kappa_T
**Where:** p. 46, "Runtime", "time per decision", "decision time",
"planning time".

The PF calls it the mean runtime. Use "runtime" here too, and "decision" for
one timestep's joint action. "Learned routers" and "learned controllers" are
also both used in the paragraph. Use "learned controllers".

- [ ] Agree
- Note:

### C2. "Trace"
**Where:** p. 46, "so a growing queue shows in the trace", and "The trace
has no vertex or swap conflict".

Never defined. Is it the log, or the per-step file of `evaluation/trace.py`?
Say "where every agent stood at every timestep" once, or say "the log".

- [ ] Agree
- Note:

---

## D. Reading order and repetition

### D1. Evaluation values in "What is logged"
**Where:** p. 46, "Table B.5 lists the values used to score a run. The load
levels and f_up come from ...".

These two sentences are about the experiment design, not logging.
`sec:exp:setup` already has a mockup about pilot runs that fix the load
levels. Move them there.

- [ ] Agree
- Note:

### D2. Runtime hardware told twice
**Where:** p. 46, "on the same machine for every controller ... Token
Passing runs on the CPU".

The "Compute environment" paragraph of VIII-A says the same. Keep it here
and let VIII-A point back, or the other way.

- [ ] Agree
- Note:

---

## E. Figures

### E1. Point to the timing figure
Appendix K has a planned figure of where the time of a step goes
(`app:timing`). One sentence in "Computational cost" pointing to it would
show that routing, not the simulator, is what the runtime measures.

- [ ] Agree
- [ ] No
- Note:

---

## F. What reads well
- The opening line, the simulator adds no choices of its own.
- "A controller is the routing part only, so swapping it touches nothing
  else."
- The reason training time and decision time are kept apart.
- The reason each method is timed on its own hardware.

## The three changes that would help the reader most
1. Settle which checks run on which runs, and make Appendix K say the same
   (A1).
2. Runtime: one name, say that kappa_T is the sum, and say which run it is
   measured on (A5, C1).
3. Move the evaluation values to the Experiments and fix where the load
   levels come from (A4, D1).
