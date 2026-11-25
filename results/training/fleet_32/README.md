# Fleet 32 trained runs (old, left out of the thesis)

Kept as a record. The thesis does not use or mention these runs (author, 2026-11-25,
answer to question 4 of `review_locks_fleet_reward.pdf`).

## Why they are left out

They were trained on commit `0c5427b`, before the shelf blocking signal [A93], the
served counts [A96], the keep-up threshold 0.9 [A111] and #212. There is no
congestion-aware storage run and no run with messages. All results at 32 and 64
agents in the thesis come from the 16-agent policies played at the larger fleet
(the scale test).

## What is here

One folder per run, each with `spec.json` (the run settings), `commit.txt` and
`progress.jsonl` (one line per training iteration).

| Run                    | Iterations | Finished |
|------------------------|-----------:|----------|
| `decentralised_fixed`  | 84         | yes      |
| `decentralised_demand` | 84         | yes      |
| `section_fixed`        | 84         | yes      |
| `section_demand`       | 8          | no       |

The checkpoints and training logs (106 MB) stay off git, in
`~/thesis_runs/training/fleet_32/` on the PC (see `project_large_traces`: over
5 MB goes on NordLocker).
