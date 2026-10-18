# Prompt: analyse a finished training campaign

Paste this to a new Claude session started in `/home/bjarkek/Documents/thesis`, after
`scripts/run_campaign.py` has finished (the output folder has `CAMPAIGN.md`).

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
  `~/.venvs/rl/bin/python -m pytest <files> -q --no-cov -p no:cacheprovider`. Run black, flake8
  and mypy (`mypy src`) on what you change.
- Commit only files you changed, with explicit paths (`git commit -- <paths>`), and check
  `git show --stat HEAD` after. The author has unstaged edits (.gitignore, examples/00b) that
  must never go into your commits.
- Separate what is measured from what is inferred. State sample sizes every time.
- Thesis prose rules apply to any thesis text: no dashes, no colons or semicolons joining
  clauses, plain language, discuss before rewriting.

Goal
Write an analysis tool for a finished campaign, run it on the real campaign folder, and report
what the data says without claiming more than it can support.

The campaign folder (ask the author for the path, normally ~/thesis_runs/campaign_<date>)
- CAMPAIGN.md: which runs ran, minutes, attempts, checkpoints, failures.
- runs/<arm>[+comm]_rate<r>/: one folder per trained policy, with <arm>_training_progress.jsonl
  (one JSON object per iteration, keys include episode_return_mean, return_shaping,
  return_deliver, return_override, return_wait, return_congestion, override_rate,
  episode_tasks_completed, episode_tasks_released) and traces/<arm>_episode_<n>.jsonl, and a
  DONE.json with the checkpoint path.
- sweep/load_sweep.jsonl: one row per (condition, arrival_rate, seed). Each checkpoint was
  trained at one rate and is evaluated at that rate. Token Passing is evaluated at every rate.
  Row keys: condition, kind (controller or planner), arrival_rate, seed, horizon,
  num_completed_tasks, backlog, released, throughput, keep_up_ratio, keeps_up,
  mean_service_time, mean_wait_for_agent, mean_travel_time, mean_blocked_time, mean_crowding,
  mean_decision_runtime_seconds. If examples/05 has been extended with storage modes, rows also
  carry storage_mode and a full "metrics" dict (RunMetrics).
- report/: per-rate overviews and a load sweep from viz/study_report.py (already written).
- logs/: every run's full log.

Already in the repo, reuse and do not duplicate
- viz/study_report.py: collect(), training_stats(), trace_stats(), sweep_stats(),
  plot_overview(), plot_load_sweep(), summary_text().
- viz/training_run.py: the single-run plots and trace numbers.
- evaluation/comparison.py::compare_paired and Interval: the paired t interval of the thesis
  gain test (eq:rqformal), scipy t quantile, takes RunMetrics lists. Use its conventions for
  intervals.
- evaluation/metrics.py::RunMetrics.

Build: src/slap_mapd_coupling/viz/campaign_analysis.py with a CLI
(`python -m slap_mapd_coupling.viz.campaign_analysis --campaign DIR [--out DIR/analysis]`), tests
in tests/unit/test_campaign_analysis.py using small synthetic folders, and a docs/TRAINING.md
paragraph. scripts/run_campaign.py may call it at the end (optional flag). Output ANALYSIS.md and
figures. Contents:
1. Header: what ran, with the sample sizes in plain words: one checkpoint per arm per load, one
   training seed, N evaluation seeds, horizon, fleet size.
2. Keep-up map: per condition and load, how many seeds pass the keep-up check (f_up = 0.8,
   eq:throughput). Service time is reported as a comparison only where every compared run keeps
   up, as the thesis says. Elsewhere show it but mark it not comparable.
3. Per load, per condition: mean with a 95% t interval over evaluation seeds for completion
   share, throughput, keep-up ratio, mean service time and its three parts (waiting for an
   agent, travel, blocked), crowding, runtime.
4. Service-time split: stacked bars per condition and load.
5. Paired comparisons over evaluation seeds (same seed means the same order stream, so the
   pairing is valid): each learned arm against Token Passing, the three arms against each other,
   decentralised with communication against decentralised. Mean paired difference with a 95%
   interval, in a forest plot. Say in the file that this pairs evaluation seeds of ONE trained
   checkpoint per arm, so it does not test the training procedure, and that a difference between
   arms that the interval does not separate from zero is not a finding.
6. Training: per run late return and its spread, collapses, override rate, the reward terms
   (the new return_wait term), completion share, and the number of iterations. Reuse
   study_report.training_stats.
7. Stalls and deadlocks: from the traces, episodes with a long stretch without a completion,
   head-on swap steps, per arm and load (viz/training_run.trace_summary).
8. If sweep rows have storage_mode and "metrics", also run compare_paired per adaptive mode and
   report it, undecided where a run does not keep up.
Handle missing keys and failed runs (a `_failed` folder, a missing DONE.json) without crashing,
and say what is missing.

Then run it on the real campaign and report to the author in chat, short, with numbers:
- Is training stable with the new reward (collapses, negative returns, override rate)?
- Which conditions keep up at which load, against Token Passing?
- Service time and its split where comparable. Does any arm differ from Token Passing or from
  another arm beyond the interval?
- Does communication change anything?
- Head-on deadlocks: where and in which arms.
- What cannot be concluded and why (one checkpoint per arm, N seeds, one instance, 3 agents).

Context from the earlier pilot (old reward, old order stream, so NOT comparable to the campaign)
~/thesis_runs/pilot_2026-10-14_old_reward/ (sweep/, report2/). Token Passing finishes about 0.3
tasks per step at most with 3 agents. Policies trained at 0.15 completed 77 to 84% at 0.25 and
63 to 71% at 0.3, against 95% and 89% for Token Passing. f_up = 0.9 failed healthy Token Passing
runs because keep_up_ratio divides by the nominal rate while releases vary (85 to 108 against
94 at 0.15), and 0.8 does not.

Afterwards, if the author agrees
- Post-merge thesis alignment for the new code (tracking issue #103) and the open gaps: "waits
  attributed to e" in eq:estimates, P_ord (#94), whether a skipped storage update counts as an
  update, the rollout length now equal to the horizon, the training regime and evaluation seed
  count still TBD.
- Do not edit the thesis. Propose wording in chat first.
```
