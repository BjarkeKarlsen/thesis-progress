# 10. Training speed on the bigger graph

**Decision** D16 of `README.md`.

## Why

The learner update was 87 to 93 % of every training iteration (170 s at 8 agents, 540 s at 32). The fleet 32
log says "0/1 GPUs": the learner ran on the CPU while the RTX 2070 SUPER (8 GB) was idle, because
`bedtime.bash` never passed `--gpu` and maybe also maybe never use more CPU than one core. Graph v2 adds two rack faces per aisle vertex, so a depth-5 window holds
about three times as many vertices in the aisles.

## Step 1. Use the GPU (no model change)

- `slap-mapd train --gpu` exists (`src/slap_mapd_coupling/main.py`, line 140), and `--batch-on-cpu` keeps the
  train batch in host memory and moves one minibatch at a time (`training/learner.py`).
- Measure seconds per iteration at 8, 16 and 32 agents with and without the GPU, on the same seed and budget,
  a few iterations each. Check GPU memory at 32 and 64 agents.
- Add `--gpu` to the training commands in `thesis-progress/results/J_training/README.md`.

## Step 2. Keep the leaves out of the router's window, only if step 1 is not enough (model change)

The router needs the walkable floor. A slot matters only when it is the robot's target or a robot stands in it.

- The leaves become features of their aisle vertex, for example "a robot is in one of my slots" and "my target
  slot hangs here", and the action "step into my target slot" is available at that vertex.
- The window is then the size of the backbone, as on graph v1.
- The cost: which of the two slots at a vertex is occupied is lost.
- Changes `eq:localsubgraph`, `eq:features` and the action set in the chapters, so it gets an `[Axx]` tag.
  Code: `environment/observation.py`, `models/local_subgraph_encoding.py`, `models/window_tables.py`,
  `environment/action_masking.py`.
- A waay to reduce memory needed to run as less RAM model the GNN better
## Related plans

`../memory_reduction_plan.md`, `../../done/embed_once_design.md`, `../scaling_to_1024_agents.md`.
continue with the next plan, 09 visualisation