# Evaluation, fleet 8, section, trained under fixed storage

## What was trained

section controller, 8 agents,
trained under fixed storage at load 0.09 on Kaggle,
`slap-mapd-coupling` commit `16acdaf63b6a2460b6055c1b806c6861c28fda16`. Budget 500000 env steps,
84 iterations, a checkpoint every 3. Run folder `/home/bjarkek/thesis_runs/training/fleet_8/section/fixed`.

## Which policy was tested, and why

Validation goes with training and the test is kept apart. Each of the 28
checkpoints played the validation seeds [100000, 100001, 100002, 100003, 100004] (2000
steps, warm-up 0, fixed storage, the rule it
trained under). The rule [A60]: of the checkpoints that keep up on every validation seed, the one with the shortest mean pick service time. If none keeps up, the highest throughput.

- Chosen: `checkpoint_000027`, after training iteration 84.
  On validation: all keep up False, throughput
  0.122 [0.096, 0.149], pick service time
  103.871 [37.651, 170.091].
- Training's own best by `episode_tasks_completed_mean` was `checkpoint_000013` (iteration 42), a different one.
- The last checkpoint, `checkpoint_000027`, is tested as a check.

The validation and test seeds are different warehouses, and neither is a training warehouse, so the
result is not measured on the seeds that chose the policy.

## How it was tested

This is the main setup ([A84]): the policy trained under fixed storage, played under every storage rule. Test seeds 200000 to 200019
(20 warehouses), 10000 steps with a
5000-step warm-up as the Token Passing runs, at load 0.09, under
fixed and demand storage. Policy on cpu, episodes on the CPU.
Evaluate commit `d204dbd24b854894b8a25ed1d1596b6239423b3c` (https://github.com/BjarkeKarlsen/slap-mapd-coupling), finished 2026-11-15T17:22.

    cd <slap-mapd-coupling at d204dbd24b854894b8a25ed1d1596b6239423b3c>
    PYTHONPATH=src python -m slap_mapd_coupling.main evaluate /home/bjarkek/thesis_runs/training/fleet_8/section/fixed --test-seeds 20 --horizon 10000 --warmup 5000 --storage-modes fixed --storage-modes demand

Queue that ran it: `/home/bjarkek/thesis_runs/cloud_2026-11-15_fleet8`. Documented with `thesis-progress/scripts/collect_evaluation.py`.

Lock measure ([A91]): longest_two_agent_hold per episode ([A91]). Seeds at or above 500, 1250 steps are listed. The threshold the thesis uses is chosen from how the numbers spread.

## Files

- `summary.md`: the test results, mean and 95 % interval over the test seeds.
- `evaluate_summary.md`: evaluate's own summary, the paired gain when played under two rules.
- `evaluation.json`: everything above in a form scripts read, evaluate's own record under "evaluate".
- `validation.jsonl`, `test.jsonl`: one row per episode.
