# Prompt: make the storage rule a switch in training, evaluation and the campaign

Paste this to a new Claude session started in `/home/bjarkek/Documents/thesis`.

```
You are continuing a thesis project. Workspace: /home/bjarkek/Documents/thesis. Code repo:
slap-mapd-coupling (GitHub BjarkeKarlsen/slap-mapd-coupling), checkout
~/Documents/thesis/slap-mapd-coupling. Read the workspace CLAUDE.md, AGENTS.md and
SESSION_CONTEXT.md first and follow them. English, UK spelling.

Working rules
- The author opens PRs. Never run `gh pr create`. Push only when told. Give PR text in chat.
- `gh pr view` fails here. Use `gh api repos/BjarkeKarlsen/slap-mapd-coupling/...` and parse
  JSON with python3 -I, because `gh api` rejects --jq.
- Do NOT launch subagents until the author and you have agreed what each task is. Investigate
  and propose in chat with numbers first.
- Run only the tests of the files you change, never the full suite. Use
  `~/.venvs/rl/bin/python -m pytest <files> -q --no-cov -p no:cacheprovider`. Run black and
  flake8 on the files you change.
- Commit only files you changed, with explicit paths (`git commit -- <paths>`), and check
  `git show --stat HEAD` after. The author has unstaged edits (.gitignore, examples/00b) that
  must never go into your commits.
- Do not invent values the thesis leaves open. Make them flags with no default, and flag them.
- Separate what is measured from what is inferred.

Goal
Adaptive storage cannot be run through the learned controllers or the campaign today. Every run
so far used fixed storage. Make the storage rule a switch (fixed, demand, congestion) with its
parameters, in training, evaluation, the sweep and the campaign script. Do NOT claim adaptive
storage helps. This task builds the switch and a way to look at it. Whether adaptive storage is
worth a campaign needs the open decisions listed below.

State to check first (git log origin/main, gh api)
Main has: wait cost in the reward (c_wait = 0.1), keep-up threshold 0.8, horizon 630, default
arrival rate 0.25, the campaign script (scripts/run_campaign.py), the sweep
(examples/05_full_comparison.py), the report (viz/study_report.py), and, if the author merged
them, the storage fixes: order stream independent of storage (#149), online estimates (#60),
skip without orders (#148). If those three are not on main, say so and stop, because fixed
versus adaptive is only paired once #149 is in.

What is already done (a patch, not committed)
/home/bjarkek/Documents/thesis/storage_mode_wip.patch changes examples/04_decentralised_training.py
and examples/04b_evaluate_checkpoint.py. It applies cleanly to main (`git apply --check`).
- A `StorageSettings` NamedTuple (mode, epoch = Delta, cap = nu, weight = beta) and
  FIXED_STORAGE.
- `add_storage_arguments(parser)`: --storage-mode {fixed,demand,congestion},
  --storage-epoch, --reassignment-cap, --congestion-weight, no defaults for the three
  parameters, because the thesis leaves Delta, nu and beta TBD (tab:storageparams).
- `storage_problem` / `storage_from_args`: fixed takes no parameters, demand needs epoch and
  cap, congestion also needs weight, demand takes no weight.
- `build_config` and `evaluation_config` take `storage`. Regime "fixed_only" always trains
  under F_fix. Regime "matched" trains under `storage`. Evaluation always uses `storage`, so a
  fixed-only policy can be evaluated under an adaptive rule (the first regime of
  sec:method:training).
- 04 and 04b pass the flags through; 04's docstring describes them.
It is NOT green. tests/unit/test_example_04_cli.py::test_matched_regime_trains_under_the_evaluation_storage_rule
pins the old module constant EVALUATION_STORAGE_MODE and must be rewritten for `storage`. No new
tests exist yet.

Tasks, in order, on branch feat/storage-mode from origin/main
1. Apply the patch. Fix that test and add tests for: the flag combinations
   (storage_problem), build_config under both regimes with each mode, evaluation_config, and
   04b taking the same flags and building the same config as 04.
2. examples/05_full_comparison.py: add `--storage-modes` (default fixed) and the three
   parameter flags (reuse example_04.add_storage_arguments semantics, but modes is a list). Loop
   every planner and checkpoint over every mode. Each row gets `storage_mode`, the parameters
   used, and the full `metrics.model_dump(mode="json")` under "metrics", so that
   evaluation/comparison.py::compare_paired (the paired test of eq:rqformal, it takes
   RunMetrics) can be fed from the sweep file. The `condition` label stays the arm, the storage
   mode is its own field. Update its tests (tests/unit/test_example_05_sweep.py) and the
   docstring.
3. scripts/run_campaign.py: add `--eval-storage-modes` and the three parameter flags, forwarded
   to the sweep stage only, so the fixed-trained policies are also evaluated under the adaptive
   rules. Do NOT add training under adaptive storage (regime matched) to the campaign yet.
   Update tests/unit/test_run_campaign.py. viz/study_report.py::sweep_stats and the load figure
   group by condition and rate, so they must also group by storage mode (label such as
   "centralised [demand]") or the modes will be mixed together. Add a test.
4. Cheap look with no GPU, once the above works: Token Passing on the example 04 instance,
   fixed against demand against congestion, rate 0.25, horizon 630, 6 seeds, for example
   --storage-epoch 100 --reassignment-cap 8 --congestion-weight 1.0 (illustrative, flag them).
   Report relocated units per update, completion share, mean service time and its three parts.
   State clearly that this instance has one SKU and uniform demand, so adaptive storage cannot
   help here. The point is that the switch works and the pairing is valid (released tasks are
   identical across modes for a seed).
5. Commit in small commits. Give the author push commands and PR text. Do not push.

Open decisions the author must make before any adaptive campaign (ask, do not decide)
1. Demand model with skew and drift (#94), for example Zipf or 80/20, and how fast popularity
   drifts relative to Delta. Without it no placement beats another.
2. Starting stock x_0 (#95): place once from expected demand, popular SKUs nearest the delivery
   vertices, the same x_0 for every storage rule.
3. Which waits count as "waits attributed to e" (eq:estimates). The code counts an overridden
   move along e. Under Token Passing no move is overridden, so the wait estimate is 0 and F_cng
   equals F_dem.
4. Values of Delta, nu and beta (tab:storageparams, all TBD).
5. Instance size: several SKUs and more storage vertices (now 4 storage vertices, 1 SKU).
6. Whether a skipped storage update counts as an update in the logs.

Do not edit the thesis. If a thesis change is needed, propose the wording in chat first.
```
