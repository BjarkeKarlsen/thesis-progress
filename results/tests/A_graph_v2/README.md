# Test A. Graph v2 at 8 agents

**Answers.** On graph v2 with today's arrival model, does demand storage beat random storage on
picks, and does travel per pick drop under demand storage? (Risk 2 of
`decisions/active/model_revision/README.md`, step 02.)
**Fills.** `tab:instances` and the results of `app:instances` (Appendix D). The comparison is a
check for the model revision, not a thesis result.
**Run.** 2026-10-26, 20 seeds, T = 2000, Token Passing, `configs/fleet_8/decentralised.yaml`
as it is (stock floor 8, margin, Δ = 100, shelf capacity 300, robot put-away).

## Answer

No. Demand storage beats fixed storage on picks, but random storage beats it by more, and
travel per pick hardly drops.

| | fixed | demand | random |
|---|---|---|---|
| keeps up | 20 / 20 | 18 / 20 (put-aways fail on 2) | 20 / 20 |
| pick service time | 44.3 | 37.9 | 36.3 |
| wait for a robot | 24.2 | 19.2 | 17.0 |
| travel | 18.4 | 17.5 | 18.0 |
| shelf-taken wait (pick) | 5.7 | 10.5 | 1.5 |
| put-away service time | 41.3 | 148.1 | 39.8 |
| robot busy share | 0.62 | 0.38 | 0.60 |
| peak shelf fill | 0.11 | 0.82 | 0.12 |

Paired by seed, with the 95 % interval:

- Pick service time, demand minus fixed, −6.4 [−7.8, −5.0], 14 % shorter. Random minus fixed
  −8.0 [−9.5, −6.6], 18 % shorter. Demand minus random +1.6 [+0.2, +3.1], demand 4.5 % longer.
- Travel per pick, demand minus fixed −0.84 [−1.08, −0.60] steps, 4.6 %. The gain is mostly in
  the wait for a robot, as on graph v1.
- Demand storage piles stock on the nearest shelves (peak fill 0.82 against 0.11). Its picks wait
  twice as long for a taken shelf as under fixed storage, and its put-aways take 3.6 times as
  long.

Why travel barely moves, not checked: every rule starts from the same demand-ordered layout
(`demand_sized_blocks`), and the arrivals are small next to the starting stock (about 10 units a
period against about 790 on the shelves, the floor of 8 per SKU setting most of it). So the rules
differ only in where a few arrivals go. Steps 04 and 05 (no floor, refills of Q units) change
this, and test B repeats this comparison.

## The warehouses

`warehouses/summary.md`. Every fleet is well-formed on 50 of 50 seeds, each from the first
layout. Trip distance of the slots:

| fleet | walkable | all vertices | slots | trip min | trip mean | trip max | ratio |
|---|---|---|---|---|---|---|---|
| 8 | 128 | 202 | 58 | 6 | 20.0 | 37 | 6.1 |
| 16 | 256 | 518 | 230 | 5 | 31.1 | 63 | 12.6 |
| 32 | 512 | 1151 | 575 | 5 | 42.6 | 87 | 17.4 |
| 64 | 1024 | 2508 | 1356 | 5 | 60.0 | 131 | 26.2 |

A 64-agent warehouse takes about 24 s to build, most of it the all-pairs distances (about
850 MB per process).

## The main load

`load_sweep/capacity.json`. Fixed storage keeps up on every seed at 0.2 and fails on 6 of 20 at
0.225, so the capacity is 0.2 and the main load 0.12.

## Commands

From `~/worktrees/test-a-combined` (`main` at `0c11849` with PR #193, graph v2, and PR #194,
the random put-away rule), `PY="PYTHONPATH=src ~/.venvs/rl/bin/python"`, `R` this folder:

    $PY scripts/instance/instance_report.py --configs configs/fleet_{8,16,32,64}/centralised.yaml \
        --seeds 50 --out $R/warehouses
    $PY scripts/sweep/load_sweep.py --config configs/fleet_8/decentralised.yaml --seeds 20 \
        --stop-when-overloaded --out $R/load_sweep \
        --rates-per-agent 0.0125 0.025 0.0375 0.05 0.0625 0.075 0.0875 0.1
    $PY scripts/sweep/load_sweep.py --config configs/fleet_8/decentralised.yaml --seeds 20 \
        --rates 0.225 0.25 0.275 --out $R/load_sweep
    $PY scripts/sweep/load_sweep.py --config configs/fleet_8/decentralised.yaml --rates 0.12 \
        --seeds 20 --storage-modes fixed demand random --out $R/comparison
    ~/.venvs/rl/bin/python $R/test_a_table.py $R/comparison/load_sweep.jsonl > $R/comparison/tables.md
