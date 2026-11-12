# Agents that lock at a workstation on a one-lane aisle (`[A91]`)

The numbers behind the limitation in `decisions/GAPS.md` `[A91]` and the review PDF
`decisions/active/readability_review/review_workstation_lock.pdf`. Every number comes from
`scripts/workstation_lock.py`, and the figure from `scripts/images/workstation_lock.py`.

## The rule for a locked seed (author, 2026-11-12)

A seed is locked when at least two agents each hold the same task for 500 steps or more at the same
time, a quarter of a 2000-step episode. A locked seed counts as not keeping up.

## How often the layout occurs

A section has the layout when every one of its workstations hangs off an aisle vertex with at most
3 neighbours (the aisle before, the aisle after, the workstation). Seeds are the training,
validation and 20 test seeds of `configs/fleet_<m>/decentralised.yaml`, code `main` `0c5427b`.

    cd ~/worktrees/train-0c5427b
    PYTHONPATH=src ~/.venvs/rl/bin/python ~/Documents/thesis/thesis-progress/scripts/workstation_lock.py \
        layout --fleet 8 --test-seeds 20 > layout_fleet8.txt

| Fleet | Training seeds | Test seeds (20) | All |
|---|---|---|---|
| 8 | 33 of 250 (13 %) | 5 (200000, 200005, 200012, 200017, 200018) | 38 of 272 (14 %) |
| 32 | see `layout_fleet32.txt` | | |

The fleet 32 count of 2026-11-11 (6 test seeds, 258 seeds) found 70 of 258 (27 %), with test seeds
200000 and 200005.

## Which traces lock

Traces of 2026-11-11 in `~/thesis_runs/training_fixes_test/`, decentralised, 8 agents, checkpoint 8,
`[A90]` reward. `fleet8_congestion` trained without messages, `fleet8_congestion_comm` with them,
both under congestion-aware storage.

    cd ~/thesis_runs/training_fixes_test
    python3 ~/Documents/thesis/thesis-progress/scripts/workstation_lock.py traces \
        fleet8_congestion/*/traces/*.jsonl fleet8_congestion_comm/*/traces/*.jsonl \
        fleet8_per_task/*/traces/*.jsonl --out locked_traces_2026-11-11.json

| Seed | Without messages | With messages |
|---|---|---|
| 200000 | locked from t = 1157, 43 tasks | 91 tasks |
| 200001 | locked from t = 1691, 107 tasks | 155 tasks |
| 200002 | 143 tasks | 201 tasks |

Full output in `locked_traces_2026-11-11.txt`. Three seeds only, so the full runs decide RQ4.

## The figure

Test seed 200000 without messages, at t = 900 (the queue forms), 1157 (the lock forms) and 1500
(still locked). The whole fleet finishes 2 tasks after t = 1157.

    for t in 900 1157 1500; do python3 thesis-progress/scripts/workstation_lock.py frame \
        ~/thesis_runs/training_fixes_test/fleet8_congestion/decentralised_congestion/traces/checkpoint_000008_congestion_seed200000.jsonl --t $t; done
    python3 thesis-progress/scripts/images/workstation_lock.py   # from the workspace root

Writes `scripts/images/data/workstation_lock_t<t>.json` and `scripts/Images/workstation_lock.png`.
