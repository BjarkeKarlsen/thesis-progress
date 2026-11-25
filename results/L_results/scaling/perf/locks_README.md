# Why every controller locks at 64 agents (investigation, 2026-11-25)

Prompt: `thesis-progress/decisions/active/lock_warehouse_prompt.md`. Investigation only, nothing in the
thesis changed. Rows: `rows/` (perf test, 16-agent congestion-aware policies, 20 test seeds 200000 to
200019, 10000 steps, 5000 warm-up). 16-agent column from the long runs' test rows in
`~/thesis_runs/evaluation/fleet_16/<arm>/<run>/evaluation_served_horizon10000_warmup5000/test.jsonl`.

## Step 1. The measure

Code: `longest_two_agent_hold` in `slap-mapd-coupling/src/slap_mapd_coupling/evaluation/evaluator.py`
(main 8ba3048, same function on bdfda94).

- Each agent's hold = steps since its CURRENT task was assigned (trip to pickup + wait + trip to
  delivery + any queue). A task not finished by T counts to T.
- At each step in [warmup, T] it takes the SECOND longest hold among all held tasks. The value is the
  maximum of that over the window.
- It does not check that the two agents are near each other, block each other or share a task. Any
  two slow tasks anywhere in the warehouse count. The thesis text (5.Experiments, before
  `tab:exp:locks`) says "two agents hold the same task", which the code does not measure.
- Only the maximum is stored in the rows. The distribution of holds per seed is not saved anywhere,
  so it needs a replay.

Second longest hold per seed, median [min, max] over 20 seeds, and seeds at >= 500 / >= 1000 steps.
Busy = `robot_busy_share` mean.

| controller | 8 | 16 | 32 | 64 |
|---|---|---|---|---|
| centralised | 108 [79, 162] 0/0 | 182 [135, 306] 0/0 | 336 [264, 622] 3/0 | 508 [444, 6952] 12/1 |
| section-based | 113 [68, 195] 0/0 | 219 [150, 1281] 3/2 | 912 [407, 9641] 18/9 | 1279 [776, 9523] 20/14 |
| decentralised | 154 [84, 317] 0/0 | 298 [172, 837] 3/0 | 797 [442, 9087] 17/8 | 2422 [584, 9938] 20/16 |
| with messages | 102 [75, 783] 1/0 | 215 [119, 5161] 6/4 | 5088 [286, 9920] 19/18 | 4271 [1275, 9938] 20/20 |

Busy share: about 0.7 to 0.83 at 8, 0.96 to 0.99 at 16, 1.0 at 32 and 64 for every controller.

With messages at 16: the long run (checkpoint 3, and checkpoint 2 at f_up 0.9) locks on 6/20, not
18/20. The 18 in `tab:exp:locks` is a first-run count (the `% TODO [A110]` above the table says so).

Reading: the typical (median) second longest hold grows with the fleet for every controller,
also where nothing jams (centralised 108, 182, 336, 508). Its whole spread at 64 (444 to 508 on most
seeds) sits on the 500 line. So most of centralised's 12 "locks" at 64 are the measure's normal value
at that size, not a jam. Only one seed (6952) stands out. Decentralised and with messages have
medians of thousands of steps at 32 and 64, far above the normal level, so for them the long holds
are real.

## Step 1b. A new lock measure (author, 2026-11-25)

A lock needs the two agents side by side. New measure `longest_pair_stand_still` (slap-mapd-coupling
PR #216): the longest time two agents on neighbouring vertices both stood still in a row, each
holding its task, in the measured window. Lock = 200 steps or more (Token Passing's longest single
stand-still is 23, 30, 55, 64 steps at 8, 16, 32, 64 agents).

Replays on the Lenovo (`~/thesis_runs/locks_replay/`, `/root/thesis_runs/locks_replay/` there) of
every episode that can lock: old hold >= 200 and longest single stand-still >= 200. 29 at 16 agents
(long runs, all three storage rules) and 41 in the perf test. Every other episode cannot reach 200
and counts as not locked. Perf episodes play main bdfda94 + #216, 16-agent episodes 131b6b1 + the
served counts patch + #216. Both test replays gave the original row back exactly (served share,
backlog, hold, stand-still). First results: with messages 32 agents seed 200006, pair 853 (a lock);
decentralised 16 agents seed 200012, pair 39 (old rule said locked, hold 648).

## Step 2. The layout

Script `locks_layout.py` (run from `~/worktrees/main-bdfda94`, the perf test code), output
`locks_layout.json`. Warehouses from the store `~/thesis_runs/warehouses`, configs
`configs/fleet_<m>/decentralised.yaml`, the 20 test seeds. Rule as in [A91]: a category has the
layout when every one of its workstations hangs off an aisle vertex with at most 3 neighbours.

| fleet | categories | test seeds with the layout | share of workstations on one-lane aisles |
|---|---|---|---|
| 8 | 1 | 5 of 20 (200000, 200005, 200012, 200017, 200018, as in [A91]) | 0.31 |
| 16 | 2 | 6 of 20 (200000, 200006, 200008, 200009, 200012, 200017) | 0.17 |
| 32 | 4 | 8 of 20 (+200005, 200016) | 0.19 |
| 64 | 8 | 9 of 20 (+200010) | 0.15 |

The share of one-lane workstations does not grow with the fleet. More categories give more chances
that one of them is all one-lane, so more seeds have the layout.

Seeds that lock, layout seeds vs the others, congestion-aware storage. "old" = hold >= 500. "locks"
= pair stand-still >= 200 from the replays (step 1b), every other seed cannot reach 200.

| controller | fleet | old | locks | served share |
|---|---|---|---|---|
| centralised | 16 | 0/6 vs 0/14 | 0/6 vs 0/14 | 0.87 vs 0.90 |
| centralised | 32 | 3/8 vs 0/12 | 0/8 vs 0/12 | 0.85 vs 0.83 |
| centralised | 64 | 5/9 vs 7/11 | 0/9 vs 0/11 | 0.89 vs 0.98 |
| section-based | 16 | 3/6 vs 0/14 | 0/6 vs 0/14 | 0.88 vs 0.91 |
| section-based | 32 | 8/8 vs 10/12 | 1/8 vs 0/12 | 0.86 vs 0.88 |
| section-based | 64 | 9/9 vs 11/11 | 3/9 vs 0/11 | 0.82 vs 1.04 |
| decentralised | 16 | 3/6 vs 0/14 | 0/6 vs 0/14 | 0.89 vs 0.90 |
| decentralised | 32 | 8/8 vs 9/12 | 3/8 vs 0/12 | 0.70 vs 0.84 |
| decentralised | 64 | 9/9 vs 11/11 | 3/9 vs 4/11 | 0.67 vs 0.72 |
| with messages | 16 | 6/6 vs 0/14 | 1/6 vs 0/14 | 0.86 vs 0.94 |
| with messages | 32 | 8/8 vs 11/12 | 6/8 vs 1/12 | 0.21 vs 0.72 |
| with messages | 64 | 9/9 vs 11/11 | 5/9 vs 2/11 | 0.45 vs 0.89 |

At 8 agents no controller locks. Reading: centralised never locks. Section-based and decentralised up
to 32 lock only on layout seeds. At 64 decentralised also locks on 4 other seeds, and with messages
locks on other seeds from 32 on. The served share drops most on layout seeds for with messages (0.21
vs 0.72 at 32).

## Step 2b. Replayed lock counts (2026-11-25, 70 of 70 replays, all match their original rows)

Collected with `python3 ~/thesis_runs/locks_replay/collect.py`. Seeds that lock out of 20, layout
seeds vs the others.

Perf test (congestion-aware storage, 16-agent policies):

| controller | 8 | 32 | 64 |
|---|---|---|---|
| centralised | 0 | 0 | 0 |
| section-based | 0 | 1 (1/8 vs 0/12) | 3 (3/9 vs 0/11) |
| decentralised | 0 | 3 (3/8 vs 0/12) | 7 (3/9 vs 4/11) |
| with messages | 0 | 7 (6/8 vs 1/12) | 7 (5/9 vs 2/11) |

16 agents, long runs, each storage rule:

| controller | congestion-aware | demand | fixed |
|---|---|---|---|
| centralised | 0 | 0 (no candidate: longest stand-still 32 steps, test 2026-11-25 15:36) | 0 |
| section-based | 0 | 0 | 0 |
| decentralised | 0 | 1 (0/6 vs 1/14) | 9 (1/6 vs 8/14) |
| with messages | 1 (1/6 vs 0/14) | 0 | 2 (1/6 vs 1/14) |

Locked seeds: decentralised fixed 200002, 200003, 200004, 200007, 200009, 200010, 200011, 200013,
200018. Decentralised demand 200016. With messages congestion-aware 200009, fixed 200004, 200008.
Perf: section 32 200006, 64 200000, 200005, 200008. Decentralised 32 200000, 200006, 200017, 64
200000, 200001, 200002, 200007, 200008, 200010, 200018. With messages 32 200000, 200005, 200006,
200012, 200016, 200017, 200018, 64 200000, 200003, 200004, 200005, 200006, 200008, 200012.

Reading:
- Centralised never locks, at any size and under every storage rule (demand at 16: no seed stands still over 32 steps).
- Locks are far rarer than the old count said (for example section-based 64: 20 old, 3 real).
- Only the two decentralised controllers lock at 16 agents. Decentralised under fixed storage locks
  on 9 of 20 seeds, mostly not on layout seeds, so fixed storage, not the layout, drives those.
- Above 16, section-based locks only on layout seeds. Decentralised and with messages also lock
  elsewhere, at 64 and from 32 on.
