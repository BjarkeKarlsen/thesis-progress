I've written both things you asked for. One caveat before you merge: the full unit suite on the branch is still running after 18 minutes, sharing the CPU with the report. I'll send the result when it finishes.

Earlier, my first version changed the instance every seed gives and broke about 180 tests that hard-code instance details. I fixed that by keeping the old role check as the default (role_backbone: true). Only the fleet warehouses switch it off, so the other configs and the earlier runs give the same instances as before. The 16 failures in test_arrival_config.py also fail on a clean main, so they aren't from this work.

How to get the numbers

1. Merge. The branch is fix/warehouse-scaling, in the worktree at ~/worktrees/fix-warehouse-scaling. Nothing is committed yet. Commit, open the PR and merge as usual, then git pull on main in slap-mapd-coupling.
2. Tests, from slap-mapd-coupling:
~/.venvs/rl/bin/python -m pytest tests/unit/test_generator.py tests/unit/test_validation.py tests/unit/test_training_spec.py --no-cov   # graph only, about 1 min
~/.venvs/rl/bin/python -m pytest tests/unit   # everything, about 5 min on an idle machine
3. Numbers: 50 seeds per fleet size, about 30 minutes, mostly the 64-agent check:
~/.venvs/rl/bin/python scripts/instance_report.py \
  --configs configs/fleet_8/centralised.yaml configs/fleet_16/centralised.yaml \
            configs/fleet_32/centralised.yaml configs/fleet_64/centralised.yaml \
  --seeds 50 --out ~/thesis_runs/instance_report_2026-10-21
   - summary.md has the appendix table: pass rate, discard rate, |V|, roles, degree, d^trip and generation time per fleet size.
   - instance_report.jsonl has one row per instance.
   - instances_used.json holds the four seed-42 warehouses for the figure.

   This run is already going on the derived settings. It is at m=64, seed 13, and every instance so far is well-formed. You can use its output once it finishes.
4. Figure, from the workspace root:
cp ~/thesis_runs/instance_report_2026-10-21/instances_used.json thesis-progress/scripts/images/data/
~/.venvs/rl/bin/python thesis-progress/scripts/images/warehouses.py
cp thesis-progress/scripts/Images/warehouses.png thesis/Images/
   The current warehouses.png was drawn from the hand-picked bounds, so redraw it after this run.
5. Writing the appendix. Point another agent at thesis-progress/decisions/active/graph_appendix_handoff.md. It has the decisions and their reasons, these same commands, the paragraph order for app:instances, the table columns, the writing rules and the open points.

Your notes

thesis-progress/decisions/ideas/Appendixes.md is restructured into eight topics: graph, storage, episode length, agents, congestion reward, model, PPO and config values. Each question is quoted with the answer indented below it. Each number is marked cited, derived, tested or open. Where nobody knows the answer yet, a To figure out line proposes a test. Your original is saved at /tmp/claude-1000/-home-bjarkek-Documents-thesis/ad4b4d17-9572-42a8-8bd7-58397df02877/scratchpad/Appendixes_original.md.

Three mismatches came up while answering:
- Episode length. The thesis gives the evaluation horizon as T = 630 (Appendix H), but the configs use 2000.
- Checkpoint selection. The configs pick the best checkpoint by training return (episode_return_mean). The thesis plans to pick it on validation seeds.
- Congestion reward. At weight 0.1 the term is about 20 times smaller than the step costs, which would explain why it seems to do nothing. That figure is my estimate and hasn't been measured. A short run that logs each reward term per step would settle it.

Link this issue to the `split_up_appendix_for_better_structure.md` since the appendix structure as it right now does not work