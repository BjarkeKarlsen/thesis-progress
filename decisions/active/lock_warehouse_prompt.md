# Prompt: why does every controller lock at 64 agents, is it the warehouse?

Paste this into a new Claude Code session started at `~/Documents/thesis`.

---

Read `SESSION_CONTEXT.md` (section "2026-11-25") first. This is an investigation only. Do not change the
thesis, do not commit, do not start long runs without asking me. Report what the data shows and say plainly
what it does not show.

**The finding.** In the performance test (`thesis-progress/results/L_results/scaling/perf/rows/`, one JSON row
per fleet, controller and seed, 20 test seeds 200000 to 200019, 10000 steps, 5000 warm-up, the 16-agent
congestion-aware policies played in bigger warehouses), the thesis's lock count (two agents hold one task for
500 steps or more, `longest_two_agent_hold >= 500`) gives these seeds out of 20:

| controller | 8 | 16 | 32 | 64 |
|---|---|---|---|---|
| centralised | 0 | 0 | 3 | 12 |
| section-based | 0 | 3 | 18 | 20 |
| decentralised | 0 | 3 | 17 | 20 |
| with messages | 1 | 18 | 19 | 20 |

(16 agents from `tab:exp:locks` in `thesis/Chapters/5.Experiments.tex`.) At 64 agents the centralised and
section-based controllers still serve 0.94. Holds of 1000 steps or more at 64: 1, 14, 16, 20. Token Passing
keeps up at 32 and 64 agents at the same main load (Appendix E, `thesis-progress/results/E_load/`).

**The question.** Is the rise in locks with fleet size caused by the warehouses (their layout as the fleet
grows), by the policies (trained at 16 agents and played out of their training size), or by the lock
measure itself (a 500-step hold may mean less in a fleet of 64)?

**What to check, in this order. Stop and report after each step.**

1. **The measure.** How does `longest_two_agent_hold` get counted (`slap-mapd-coupling`, evaluator)? Is it
   the longest hold of any pair over the whole measured window? A fleet of 64 has more pairs and a longer
   queue, so a 500-step hold may be more likely by chance. Look at the distribution of holds per seed, not
   only the maximum, if the rows or traces allow it.
2. **The layout.** The thesis names one lock spot: a workstation on an aisle one lane wide
   (`sec:method:resolution` in `4.Implementation.tex`, [A115] in `thesis-progress/decisions/GAPS.md`). A
   category with all its workstations on such aisles occurs in 14 % of the warehouses at 8 agents and 27 % at
   32. Get the same share for the 16 and 64 agent warehouses of the 20 test seeds
   (`thesis-progress/results/D_warehouses/`, the warehouse store `~/thesis_runs/warehouses`, the generator in
   `slap-mapd-coupling`). Then check per seed whether seeds with such a layout lock more, per controller.
3. **Where the locks happen.** If step 2 does not settle it, replay a few locked seeds at 64 agents (start
   with the centralised controller, which locks least, and one decentralised seed) with a trace of agent
   positions, and find where the long holds sit: at workstations, on one-lane aisles, at docks, at section
   borders. Use the run scripts in `~/thesis_runs/scaling_2026-11/perf/` (job.sh) and the checkpoints listed in
   `perf/log`. Keep each replay short and run it only when the PC is not busy with training or evaluation
   (check `systemctl --user list-units` first, the fleet reward runs may be training).
4. **Token Passing as the reference.** Token Passing plays the same warehouses. Does it ever hold a task long
   in the 64-agent warehouses of these seeds? If it never does, the layout alone cannot cause a lock, and the
   question becomes why the learned policies walk into it.
5. **Training size.** The policies were trained at 16 agents. Compare the agents per aisle and per
   workstation at 16 and at 64 agents at the main load. If density per workstation is higher at 64, the
   policies meet queues they never saw in training.

**Report.** One short paragraph per step: what was checked, the numbers, and what it means. End with which of
the three causes (warehouse, policy, measure) the data supports, and what one extra check would settle it.
Write the numbers into `thesis-progress/results/L_results/scaling/perf/locks_README.md`. Talk to me in short,
plain sentences.
