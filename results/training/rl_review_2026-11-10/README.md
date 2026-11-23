# Why the decentralised arm collapses at fleet 32 (RL review, 4 to 10 November 2026)

Every run of the review, kept so the story can be shown later: the collapse, the fixes that were
tried, which ones held, and the trace that found the cause. Decentralised arm, fixed_only regime,
fixed storage, delivery reward 10 throughout. Rationale entries are `[A79]` to `[A89]` in
`decisions/GAPS.md`.

## The problem

At fleet 32 the decentralised arm learned to deliver and then unlearned it. Tasks done per episode
rose to 113 at iteration 4 and fell to 13 by iteration 12 (`progress/f32_main_8681819_fixed_only`,
the matched run is the same). Fleet 8 on the same code trained well, about 190 tasks from
iteration 11 on (`progress/f8_main_514624c`).

## What was tried

Short runs, one seed each, on the author's PC (RTX 2070 Super, 3 env runners). Tasks done per
episode.

| Run | Fleet | Iterations | What changed | Tasks, iterations 21 to 25 or the last 3 | Standing still | Kept? |
|---|---|---|---|---|---|---|
| `f8_main_514624c` | 8 | 84 | nothing, `main` | 182 | 37 % | baseline |
| `f8_all5fixes` | 8 | 21 | all five fixes of 2026-11-04 | about 55 | 70 % | no |
| `f8_ablation_A` | 8 | 25 | reward order `[A79]` + logging | 155 | 33 % | yes |
| `f8_ablation_B` | 8 | 25 | A + move cost 0.25 `[A80]` | 4 | 79 % | no, it froze the robots |
| `f8_ablation_C` | 8 | 25 | A + following rule `[A81]` | 175 | 41 % | yes |
| `f8_ablation_D` | 8 | 25 | A + scaled distance feature `[A82]` | 171 | 37 % | yes |
| `f8_ablation_E` | 8 | 25 | `[A79]`, `[A81]`, `[A82]` together | 199 | 32 % | yes |
| `f32_fixes1to4` | 32 | 12 | as E | 10 at iteration 12 | 9 % | still collapses |
| `f32_override_0.1` | 32 | 12 | E + override penalty 0.1 | 5 at iteration 12 | 8 % | no effect |
| `f32_override_0.0` | 32 | 7 (stopped) | E + override penalty 0 | 8 at iteration 7 | 23 % | no effect |
| `f32_minibatch_512` | 32 | 10 (stopped) | E + minibatch 512 | 9 at iteration 10 | 15 % | no effect |

The learner logs (`progress.csv` of each run) ruled out the PPO step size. At fleet 32 the policy
changed as little per update as at fleet 8 (mean KL 0.003 to 0.013), and the value net predicted the
returns better (explained variance 0.86 to 0.99 against 0.5 to 0.86). So the policy learned what the
reward asked for.

## The cause, from a trace

The last checkpoint of `f32_fixes1to4` (iteration 12) played one episode on test seed 200000.
Trace: `~/thesis_runs/training_fixes_test/fleet32_short/decentralised_fixed_only/traces/checkpoint_000003_fixed_seed200000.jsonl`
(13 MB, not in git). Read with `analyse_trace.py` and `trip_lengths.py` in this folder.

- 4 of 569 tasks finished. Every robot held its first task all episode and never picked up
  (31746 robot-steps heading to the pickup, 222 to the delivery, in steps 1000 to 2000).
- Robots stayed about 5 steps from the shelf (median 5, 90 % under 8), 48 % of steps towards it and
  47 % away, 45 % of moves back and forth (A, B, A).

The progress reward measured the distance to the current target, which switches from the shelf to
the workstation at pickup. So at the shelf the robot paid the whole delivery trip in one step. The
trip is about 12 steps at fleet 8 and a median of 29 (90 % under 44) at fleet 32. The refund comes
one step at a time afterwards, and PPO learned to avoid the shelf before the value net learned the
refund. Once no robot picked up, it never learned it.

## First fix: no jump at pickup (`[A89]`), not enough

`[A89]`: the potential is the distance left in the whole task, to the shelf plus the trip to the
workstation before pickup, and to the workstation after. It does not jump at pickup. Run
`progress/f32_task_potential`, 12 iterations, otherwise as `f32_fixes1to4`.

| Iteration | Tasks, old potential | Tasks, `[A89]` | Standing still, old | Standing still, `[A89]` |
|---|---|---|---|---|
| 3 | 76 | 79 | 36 % | 39 % |
| 5 | 49 | 59 | 26 % | 44 % |
| 9 | 14 | 6 | 15 % | 28 % |
| 12 | 10 | 1 | 9 % | 20 % |

It only delayed the collapse. The trace of its last checkpoint
(`~/thesis_runs/training_fixes_test/fleet32_task_potential/decentralised_fixed_only/traces/checkpoint_000003_fixed_seed200000.jsonl`,
read with `analyse_trace.py`, `queue_check.py` and `exit_check.py`):

- The robots now pick up. In steps 1000 to 2000, 25414 robot-steps carry a load and 6554 head to a
  shelf. 14 of 569 tasks finished.
- They stop 3 to 8 steps before the workstation (56 % of loaded robot-steps) and step back and
  forth (39 % of moves A, B, A). Loaded robots go to 6 of the 16 workstations, 4.2 per workstation on
  average.
- It is not a jam at the workstation. A loaded robot stood on its own workstation for only 9
  robot-steps in 1000 steps. The 2392 robot-steps on a workstation are robots whose goal is
  elsewhere, stepping into a free dead end for one step (median stay 1) as part of the back and
  forth. The way out was taken in 401 of them.

## The cause behind both collapses

`[A79]` charges a robot for its new task's distance on the step it gets the task. With orders
waiting, which at fleet 32 is always, the robot gets its next task in the same step it finishes the
current one. So delivering pays +10 and at once costs the new task's whole distance, about 30 to 60,
and the robots learned to stop just before the workstation. `[A79]` said the robot cannot avoid that
charge, which was wrong: it avoids it by never finishing.

The rule behind both collapses: whenever reaching a goal brings a large penalty at once, the robots
stop just before that goal. Before `[A89]` it was the shelf (the pickup jump), after it the
workstation (the hand-out charge). Fleet 8 escapes because its trips are short (shelf to workstation
about 12 steps, against a median of 29 at fleet 32), so the penalties are small.

Rejected on the way: a deadline penalty as in van Knippenberg et al. (2021), weak -0.1 per step
late. A hovering robot saves 30 to 60 by not finishing, far more than such a penalty, and the
model has no deadlines (lifelong tasks, service time is the measure). Raising the delivery reward
(the author keeps 10, from van Knippenberg) and raising gamma, which do not remove the penalty.

## The fix to test next (`[A90]`), coded, not run

Progress is counted within the task the robot serves only. Each step closer to finishing it pays
about +1 and each step away about -1 (the distance left, `[A89]`). The step that finishes a task ends
at potential 0. A task handed out starts counting on the next step from its own start, so no step
pays for a new task's distance. A free robot gets no shaping, which also closes the parking loop
`[A79]` was meant to stop. Over a task the robot earns about its length plus 10, so finishing is
never penalised. The cost is that the formal guarantee of Ng et al. (1999) no longer holds exactly,
because the count resets between tasks. `[A79]`'s thesis text needs rewriting with it.

Code: `environment/reward_function.py::reward_terms` (the shaping term), tests
`tests/unit/test_reward_order.py`, `test_idle_parking.py`, `test_reward_function.py` (24 pass). The
patch of everything uncommitted on the branch is `configs/per_task_uncommitted_2026-11-10.patch`.

To run, from `~/worktrees/rl-review-tests`: the script
`~/thesis_runs/training_fixes_test/fleet32_per_task/run.sh` (12 fleet 32 iterations, about 28
minutes on the PC, then a trace of the last checkpoint). Start it under
`systemd-inhibit --what=sleep:idle:handle-lid-switch`. It was started once on 2026-11-10 18:12 and
stopped by the author after a minute, so delete `fleet32_per_task/run.log` and
`decentralised_fixed_only/` there first.

Success looks like tasks done still climbing past iteration 4 and robots reaching their
workstations in the trace. If they still step back and forth, the next step is a move cost equal to
the wait cost (0.2), one change at a time. Then several seeds, and fleet 8 again.

## Code

`slap-mapd-coupling` branch `fix/rl-review-tests` (`600a614`, fixes `[A79]`, `[A81]`, `[A82]` and the
move cost kept at 0.1, pushed, no PR, the classifier blocked `gh pr create`). `[A89]` and `[A90]` are
uncommitted on top in `~/worktrees/rl-review-tests`. The ablation worktrees are
`~/worktrees/ablation-A` to `-D`. The variant configs are in `configs/` here. The five-fix patch of
2026-11-04 is `configs/all_fixes_2026-11-04.patch`.
