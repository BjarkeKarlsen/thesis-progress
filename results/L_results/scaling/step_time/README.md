# Step time test, 8 to 64 agents

Time per decision step of the four learned controllers as the fleet grows. Fills the scaling part of
Appendix L (`app:results:scaling`) and the decision time figure of the Experiments chapter
(`fig:exp:time`). Figure script: `thesis-progress/scripts/images/scaling_steptime.py`.

## What ran

- **Policies.** The long congestion-aware 16-agent policy of each controller, at its chosen
  checkpoint ([A111], the 0.9 rule), played without further training in the warehouse of 8, 16, 32
  and 64 agents at that fleet's main load (0.09, 0.18, 0.3, 0.6). Section-based uses 2 sections at
  8 agents and 3 x m/16 above.
- **Episode.** One seed (200000), 3000 steps, the first 2000 a warm-up. Timed over the 1000
  measured steps only (`window_decision_runtime_seconds`) and per 100 steps
  (`decision_runtime_per_100_steps`).
- **Machine.** The PC, network on the GPU (RTX 2070 SUPER), one CPU thread, nothing else running,
  23 November 2026, 20:00 to 23:27.
- **Code.** `~/worktrees/scaling-run` (`feat/scaling-run`, PR #210, `408ea93`), `timing.sh` and
  `timing_probe.py` here are the copies that ran. Token Passing was not part of this test.

## Files

- `rows.jsonl` 16 rows, one per fleet and controller.
- `rows_redo.jsonl` fleet 8 section-based and centralised again. The first two overlapped a smoke
  test at 20:04, so **these two replace the ones in `rows.jsonl`**.
- `log`, `logs/` the run log and one log per episode.
- Fleet 64 centralised was paused (SIGSTOP) in its warm-up from 20:52 to 22:40. Its window is
  clean, its all-steps mean is not.

## Result, seconds per step in the measured window

| agents | decentralised | with messages | section-based | centralised |
|---|---|---|---|---|
| 8 | 0.005 | 0.006 | 0.024 | 0.032 |
| 16 | 0.009 | 0.010 | 0.043 | 0.071 |
| 32 | 0.018 | 0.019 | 0.110 | 0.220 |
| 64 | 0.043 | 0.051 | 0.225 | 0.897 |

Section-based and centralised stay flat over the window. Decentralised, with and without messages,
climb 10 to 15 % from the first to the last 100 steps at 32 and 64 agents. Every controller stays
under 1 s per step (Ma et al. 2017).
