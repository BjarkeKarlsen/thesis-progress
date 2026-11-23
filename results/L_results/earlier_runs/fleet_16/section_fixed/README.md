# Evaluation, fleet 16, section, trained under fixed storage

## What was trained

section controller, 16 agents,
trained under fixed storage at load 0.18 on this PC,
`slap-mapd-coupling` commit `0c5427b`. Budget 500000 env steps,
84 iterations, a checkpoint every 3. Run folder `/home/bjarkek/thesis_runs/training/fleet_16/section/fixed`.

## Which policy was tested, and why

Validation goes with training and the test is kept apart. Each of the 28
checkpoints played the validation seeds [100000, 100001, 100002, 100003, 100004] (2000
steps, warm-up 0, fixed storage, the rule it
trained under). The rule [A60]: of the checkpoints that keep up on every validation seed, the one with the shortest mean pick service time. If none keeps up, the highest throughput.

- Chosen: `checkpoint_000024`, after training iteration 75.
  On validation: all keep up False, throughput
  0.225 [0.207, 0.242], pick service time
  154.363 [106.250, 202.476].
- Training's own best by `episode_tasks_completed_mean` was `checkpoint_000024` (iteration 75), the same checkpoint.
- The last checkpoint, `checkpoint_000027`, is tested as a check.

The validation and test seeds are different warehouses, and neither is a training warehouse, so the
result is not measured on the seeds that chose the policy.

## How it was tested

This is the main setup ([A84]): the policy trained under fixed storage, played under every storage rule. Test seeds 200000 to 200019
(20 warehouses), 10000 steps with a
5000-step warm-up as the Token Passing runs, at load 0.18, under
fixed and demand storage. Policy on cuda, episodes on the CPU.
Evaluate commit `ecdec4994ba49ebd49a2fb8f734267f092c62589` (https://github.com/BjarkeKarlsen/slap-mapd-coupling), finished 2026-11-14T16:03.

    cd <slap-mapd-coupling at ecdec4994ba49ebd49a2fb8f734267f092c62589>
    PYTHONPATH=src python -m slap_mapd_coupling.main evaluate /home/bjarkek/thesis_runs/training/fleet_16/section/fixed --test-seeds 20 --horizon 10000 --warmup 5000 --storage-modes fixed --storage-modes demand --gpu

Queue that ran it: `None`. Documented with `thesis-progress/scripts/collect_evaluation.py`.

Lock measure ([A91]): longest_two_agent_hold per episode ([A91]). Seeds at or above 500, 1250 steps are listed. The threshold the thesis uses is chosen from how the numbers spread.

## Files

- `summary.md`: the test results, mean and 95 % interval over the test seeds.
- `evaluate_summary.md`: evaluate's own summary, the paired gain when played under two rules.
- `evaluation.json`: everything above in a form scripts read, evaluate's own record under "evaluate".
- `validation.jsonl`, `test.jsonl`: one row per episode.
