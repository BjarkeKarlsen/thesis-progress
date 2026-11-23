# Scaling test: step time and performance as the fleet and warehouse grow (draft 2026-11-23)

Status: agreed with the author on 2026-11-23. Code PR #210, script ~/thesis_runs/scaling_2026-11/run.sh,
started by hand once the evaluations are done (the PC must be quiet for timing).

## Question

1. **Step time.** How the decision time per step, and per step per agent, grows with the fleet.
   It argues for the scalability of the decentralised controller.
2. **Performance.** Whether the warehouse still works as it grows (served share, queue growth,
   locks), next to Token Passing on the same seeds.

The main results (16 agents, all three storage rules) answer whether coupling helps. This test only
shows scalability, so it runs under **congestion-aware storage only** (author).

## Design, one run per warehouse size gives both answers

- Fleets 8, 16, 32 and 64, each in its own warehouse (2.5 SKUs and 5 shelves per agent, Appendix D)
  at its own main load (0.09, 0.18, 0.3, 0.6).
- The long-trained 16-agent policies under congestion-aware storage, played without further
  training. The network does not depend on the size of the warehouse. Section-based uses
  3 x m/16 sections (6 at 32, 12 at 64), as in the probe of 2026-11-16.
- Controllers: centralised, section-based, decentralised, with messages, and Token Passing.
- Each run records the decision time kappa_T ([eq:runtime]) and the served share, queue growth and
  locks in the same episode, so no separate timing run is needed.
- All runs on the PC, one at a time, nothing else running (author: same machine for all, so the
  times compare). Learned controllers on the GPU, Token Passing on the CPU, as in Appendix L.
- 16 agents is not played again (author 2026-11-23). Its step time comes from the clean GPU timing runs of Appendix L (same PC, alone, the network does not change with training), its performance from the 20 test seeds of the long runs (a 5000-step window against 4000 here, the served share is a rate).
- Fewer runs than the main test, stated as a limit of computing power (author).

## Length and seeds (to confirm)

3 test seeds (200000 to 200002), 6000 steps with a 2000-step warm-up. Fewer seeds and shorter runs
do not change how well a policy plays. They only make the estimate less precise. The large gain
came from training on longer episodes, not from testing longer.

Rough time per episode at 6000 steps, from the 16-agent timings and the busy-machine probe at 64
(32 is interpolated):

| controller | 8 | 16 | 32 | 64 |
|---|---|---|---|---|
| centralised | ~2 min | ~11 min | ~1 h | ~5.8 h |
| section-based | ~1 min | ~7 min | ~30 min | ~1.9 h |
| decentralised, with messages | <1 min | ~1.5 min | ~6 min | ~20 min |
| Token Passing (CPU) | <1 min | <1 min | ~2 min | ~10 min |

Total about 19 h on the PC with 3 seeds each (16 agents skipped), except the centralised controller at 64 with 1 seed
(5.8 h). Real numbers come from the first runs.

## Reading the time

kappa_T is the computer time per simulated step. A step is one move of one aisle position. Ma et
al. (2017) count runtimes below one second per timestep as allowing real-time lifelong operation
(checked in the paper, Section "Runtimes per Timestep"). The chart shows kappa_T and kappa_T / m
against m, with the 1 s line.

## Outputs

- Figure: decision time per step against fleet size, one line per controller, log scale, 1 s line.
- Table: served share, queue growth, locks per fleet and controller.
- Thesis: Appendix L (a new "Scaling" part) and one paragraph plus the figure in the Experiments
  (RQ3 or Discussion, to agree).

## Open

- 16 agents in the 32 and 64 warehouses (the warehouse grows, the fleet does not) separates the two
  effects. The probe of 2026-11-16 showed the warehouse alone does most of the harm. Optional, about
  +3 h with the decentralised controllers only.
