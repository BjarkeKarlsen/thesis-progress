# Earlier runs

The learned controllers' first training, kept as research into the problem
(author, 2026-11-23). Nothing here is the main result. The main result is
the long 16-agent runs, collected in `results/L_results/fleet_16/` once
their evaluations finish. In the thesis every run here is called an
earlier run.

## What these runs are

- Training: 500 000 environment steps on episodes of 2000 steps, one
  policy per controller and storage rule.
- Test: 20 test seeds, 10000 steps, the first 5000 left out.
- The served counts ([A96]) come from replays of the same policies on the
  same test seeds. Read them with `scripts/served_counts.py` (f_up 0.9,
  [A111]). Take every number from the replay rows,
  `~/thesis_runs/evaluation/fleet_<m>/<arm>/<rule>/evaluation_served_horizon10000_warmup5000/`.
- `fleet_32/`, `fleet_64/` hold only template tables. Fleets 8, 32 and 64
  come back in the thesis only through the scaling test
  (`decisions/active/scaling_plan.md`), with the long 16-agent policies.

## What they showed

- **Training was too short.** A policy that falls behind slowly hardly
  shows it in 2000 steps, so neither training nor the checkpoint choice
  punished it. This led to the long runs (2 000 000 steps on 16 000-step
  episodes, [A110]).
- **Why 16 agents is the main warehouse.** With the same short training,
  congestion-aware storage gave no gain at 8 agents and helped 3 of 4
  controllers at 16. Served share, fixed against congestion-aware:

  | controller | 8 agents | 16 agents |
  |---|---|---|
  | centralised | 0.86, 0.81 | 0.54, 0.59 |
  | section-based | 0.87, 0.91 | 0.63, 0.69 |
  | decentralised | 0.84, 0.82 | 0.12, 0.66 |
  | with messages | 0.96, 0.82 | 0.37, 0.34 |

  Agents were blocked about as long per pick at 8 (8 to 19 steps) as at 16
  (15 to 24), so the reason is not too few agents to crowd. At 8 agents the
  fleet nearly kept up, so there was little for the storage rule to win.
  The 16-agent decentralised jump is mostly its weak run under fixed
  storage.
- **The keep-up threshold.** Under the served count a steady fleet sits
  near 1.0, and seeds that passed at 0.8 still grew their queue, so f_up
  went to 0.9 ([A111]).
- **Locks.** The decentralised controller loses most of its work to locks
  in front of workstations (`results/limitations/workstation_lock/`).

## Layout

`fleet_<m>/<arm>_<rule>/` the summary and evaluation of one run,
`fleet_16/rows/` the copied test rows, `comparison.md`, `overview.md` and
`tables.tex` per fleet (from `scripts/images/appendix_results.py` and
`fleet16_results.py`, which now read from here).
