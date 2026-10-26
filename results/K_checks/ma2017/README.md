# K. Token Passing on the small warehouse of Ma et al. (2017)

**Answers.** Does our simulator, with our Token Passing, reproduce the published Token Passing
results? (Step 08 of `decisions/active/model_revision/`, D14.)
**Fills.** `app:repro:ma` and `tab:app:ma2017` of Appendix K.
**Run.** 2026-10-26, `slap-mapd-coupling` branch `feat/ma-reproduction` (worktree
`~/worktrees/refill`, uncommitted), 5 seeds per cell, 7 workers. The LaTeX build ran at the same
time, so the runtimes are inflated. They are not comparable with the paper's anyway.

    cd ~/worktrees/refill
    PYTHONPATH=src ~/.venvs/rl/bin/python scripts/ma2017.py --seeds 5 --workers 7 \
        --out ~/Documents/thesis/thesis-progress/results/K_checks/ma2017

## Answer

Yes, to within about 10 %, and always on the fast side. Over the 30 cells (6 frequencies × 5
fleets) our service time is 8.1 % shorter than theirs on average, from 34 % shorter to 2.5 % longer.
Makespans at frequency 0.2 agree to within 0.3 %. All 150 runs finished all 500 tasks, and no agent
ever left its plan (`num_diverged` 0).

- **At frequency 0.2, service time is 3.7 to 5.3 steps shorter at every fleet.** Tasks hardly wait at
  that load (the delivery leg alone is 15.5 steps on average), so this is a convention or path
  difference the paper does not pin down. Candidates, not checked: when a task added at t first
  enters the token round, and whether their service time counts the step of the pickup or delivery
  differently.
- **The largest gap, 10 agents at 0.5 (87.7 against 132.8), is a fleet near its capacity**, where
  service time is most sensitive to the one task sequence they used.
- The gap is not a sign of a broken simulator, since the order of the cells (by frequency and fleet)
  matches theirs everywhere.

Full table: `ma2017.md`. Rows: `ma2017.jsonl`, one per (frequency, fleet, seed).

## Choices the paper leaves open

- The map is rebuilt from Figure 4 of the AAMAS 2017 paper (`papers/3091125.3091243.pdf`), as
  `MA2017_MAP` in `benchmarks/ma2017.py`: 21 × 35 cells, 635 open, 200 task endpoints, 152 start
  cells, 100 blocked.
- The task sequence and the start cells of fleets under 50 are drawn from the seed.
- Task k is added at the first t with k < (t + 1) f. Pickup and delivery are distinct.
- Numbers compared are Table 1 of the AAMAS 2017 version. The thesis cites the key
  `ma2017lifelong_mapf`, which is the 2020 Transportation Science version, and its tables were not
  checked. Either cite the conference version for this table or check the journal's numbers.
