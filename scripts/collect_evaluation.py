"""Collects a finished evaluation of trained runs into one place, with everything the thesis needs
to say what was tested and how. The patch for the evaluations run before `evaluate` wrote this
itself (2026-11-13, fleet 16).

Run from a `slap-mapd-coupling` checkout at the evaluate commit, with the venv's python:

    cd ~/worktrees/eval-test-seeds
    PYTHONPATH=src ~/.venvs/rl/bin/python ~/Documents/thesis/thesis-progress/scripts/collect_evaluation.py \
        --fleet 16 --queue ~/thesis_runs/eval_2026-11-13_fleet16

For every run `~/thesis_runs/training/fleet_<m>/<arm>/<regime>` whose evaluation folder holds a
`summary.md` (the evaluation finished), it

1. moves the evaluation folder to `~/thesis_runs/evaluation/fleet_<m>/<arm>/<regime>/` and leaves
   a note `MOVED.md` where it was,
2. writes there `evaluation.json` (what was trained, which policy was tested and why, how it was
   tested), `summary.md` (the test results of the run, mean and 95 % interval over the test seeds)
   and `README.md` (the same in words, with the exact commands). evaluate's own summary is kept as
   `evaluate_summary.md`,
3. writes `comparison.md` for the fleet: the gain of demand and congestion-aware storage over fixed
   storage per controller, each run's chosen policy on the same test seeds, paired seed by seed
   (eq:rqformal, the main result),
4. copies the small files to `thesis-progress/results/L_results/fleet_<m>/`.

Runs whose evaluation has not finished are listed and left alone, so it can run again later.
"""

import argparse
import datetime
import glob
import json
import re
import shutil
import subprocess
from pathlib import Path

from slap_mapd_coupling.evaluation.comparison import _mean_and_interval, compare_paired
from slap_mapd_coupling.evaluation.metrics import RunMetrics

ROOT = Path.home() / "thesis_runs"
RESULTS = Path(__file__).resolve().parents[1] / "results" / "L_results"
CODE = "https://github.com/BjarkeKarlsen/slap-mapd-coupling"
# The measures the run summary gives, in this order.
MEASURES = (
    ("throughput", "throughput, tasks per step"),
    ("keeps_up", "share of seeds that keep up"),
    ("mean_service_time", "pick service time, steps"),
    ("mean_wait_for_agent", "wait before an agent takes it"),
    ("mean_travel_time", "travel"),
    ("mean_blocked_time", "blocked"),
    ("mean_order_completion", "order completion, steps"),
    ("mean_putaway_service_time", "put-away service time"),
    ("mean_crowding", "crowding"),
    ("longest_completion_gap", "longest stretch with no task done"),
    ("mean_decision_runtime_seconds", "decision runtime, s"),
)


def rows(path):
    return [json.loads(line) for line in open(path) if line.strip()]


def checkpoint_iteration(name, frequency):
    """checkpoint_000N is saved after training iteration frequency * (N + 1)."""
    return frequency * (int(name.split("_")[-1]) + 1)


def interval(values):
    values = [float(v) for v in values if v is not None]
    if not values:
        return None
    if len(values) < 2:
        return {"mean": values[0], "ci_low": None, "ci_high": None, "seeds": 1}
    mean, low, high = _mean_and_interval(values, 0.95)
    return {"mean": mean, "ci_low": low, "ci_high": high, "seeds": len(values)}


def training_best(run):
    """The checkpoint training kept as its best by its own score, from the last such line."""
    best = None
    for line in open(run / "train.log", errors="replace"):
        match = re.search(r"Best checkpoint by (\S+) saved to .*/(checkpoint_\d+)", line)
        if match:
            best = (match.group(1), match.group(2))
    return best


def where_trained(run):
    done = (run / "done").read_text().strip() if (run / "done").exists() else ""
    commit = (run / "commit.txt").read_text().split()[0] if (run / "commit.txt").exists() else ""
    if not commit:
        match = re.search(r"commit (\w+)", done)
        commit = match.group(1) if match else "unknown"
    place = "Kaggle" if "kaggle" in done else "Colab" if "colab" in done else "this PC"
    return {"place": place, "commit": commit, "done_file": done}


def collect_run(run, fleet, eval_name, queue, eval_commit, device):
    spec_path = next(run.glob("*_spec.json"))
    spec = json.loads(spec_path.read_text())
    src = run / eval_name
    arm = run.parent.name
    regime = run.name
    dest = ROOT / "evaluation" / f"fleet_{fleet}" / arm / regime
    validation = rows(src / "validation.jsonl")
    test = rows(src / "test.jsonl")
    frequency = spec["checkpoint"]["frequency"]
    progress = rows(next(run.glob("*_training_progress.jsonl")))

    chosen = next(r["checkpoint"] for r in test if r["role"] == "chosen")
    last = next(r["checkpoint"] for r in test if r["role"] == "last")
    best = training_best(run)
    per_checkpoint = {}
    for r in validation:
        per_checkpoint.setdefault(r["checkpoint"], []).append(r)

    def validation_of(name):
        played = per_checkpoint.get(name, [])
        return {
            "seeds": [r["seed"] for r in played],
            "all_keep_up": all(r["keeps_up"] for r in played) if played else None,
            "throughput": interval(r["throughput"] for r in played),
            "mean_service_time": interval(r["mean_service_time"] for r in played),
        }

    def policy(name):
        return {"checkpoint": name, "training_iteration": checkpoint_iteration(name, frequency),
                "path": str(next(run.glob(f"*/*/{name}"), "")), "validation": validation_of(name)}

    results = {}
    for role in ("chosen", "last"):
        played = [r for r in test if r["role"] == role]
        results[role] = {name: interval(r.get(name) for r in played) for name, _ in MEASURES}
        results[role]["seeds"] = [r["seed"] for r in played]
    first = test[0]
    info = {
        "run": {
            "fleet": fleet, "controller": spec["controller"], "arm_folder": arm,
            "communication": spec.get("communication", False),
            # The folder name, fixed, demand or congestion. Runs trained before the rename (PR #206)
            # store fixed_only or matched in their settings, kept beside it.
            "trained_under": regime, "regime_in_settings": spec["regime"], "run_dir": str(run),
            "trained": where_trained(run),
            "budget_env_steps": spec["ppo"]["training_budget_env_steps"],
            "iterations": len(progress),
            "checkpoint_every": frequency,
            "checkpoints": len(per_checkpoint),
            "training_load": spec["arrival_rate"],
            "training_episode": {"horizon": spec["horizon"], "warmup": spec["warmup"]},
        },
        "policy": {
            "rule": "[A60]: of the checkpoints that keep up on every validation seed, the one with "
                    "the shortest mean pick service time. If none keeps up, the highest throughput.",
            "chosen": policy(chosen),
            "last": policy(last),
            "training_best": {"score": best[0], **policy(best[1])} if best else None,
            "chosen_is_training_best": bool(best and best[1] == chosen),
        },
        "evaluation": {
            "commit": eval_commit, "code": CODE, "device": device,
            "command": (f"PYTHONPATH=src python -m slap_mapd_coupling.main evaluate {run} "
                        f"--test-seeds {len(results['chosen']['seeds'])} --horizon {first['horizon']} "
                        f"--warmup {first['warmup']}" + (" --gpu" if device == "cuda" else "")),
            "queue": str(queue) if queue else None,
            "validation": {"seeds": sorted({r["seed"] for r in validation}),
                           "horizon": validation[0]["horizon"], "warmup": validation[0]["warmup"],
                           "storage_mode": validation[0]["storage_mode"],
                           "checkpoints_played": len(per_checkpoint)},
            "test": {"seeds": results["chosen"]["seeds"], "horizon": first["horizon"],
                     "warmup": first["warmup"], "storage_mode": first["storage_mode"],
                     "load": first["arrival_rate"], "num_agents": first["num_agents"]},
            "finished": datetime.datetime.fromtimestamp(
                (src / "summary.md").stat().st_mtime).isoformat(timespec="minutes"),
            "lock_measure": "none in this round. longest_completion_gap shows a whole-fleet stop "
                            "only, so locks of one section ([A91]) are under-counted.",
        },
        "results": results,
    }

    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        raise SystemExit(f"{dest} exists already, not moving {src} over it.")
    shutil.move(str(src), str(dest))
    (run / "MOVED.md").write_text(f"The evaluation {eval_name} moved to {dest}.\n")
    if (dest / "summary.md").exists():
        (dest / "summary.md").rename(dest / "evaluate_summary.md")
    (dest / "evaluation.json").write_text(json.dumps(info, indent=1))
    (dest / "summary.md").write_text(run_summary(info))
    (dest / "README.md").write_text(run_readme(info))
    return info, dest


def fmt(cell):
    if cell is None:
        return "n/a"
    if cell["ci_low"] is None:
        return f"{cell['mean']:.3f}"
    return f"{cell['mean']:.3f} [{cell['ci_low']:.3f}, {cell['ci_high']:.3f}]"


def title(info):
    r = info["run"]
    comm = ", with messages" if r["communication"] else ""
    return f"fleet {r['fleet']}, {r['controller']}{comm}, trained under {r['trained_under']} storage"


def run_summary(info):
    lines = [f"# Test results, {title(info)}", "",
             f"Mean and 95 % interval over the {len(info['results']['chosen']['seeds'])} test "
             f"seeds, {info['evaluation']['test']['horizon']} steps with a "
             f"{info['evaluation']['test']['warmup']}-step warm-up, played under "
             f"{info['evaluation']['test']['storage_mode']} storage. The chosen policy is the result. "
             "The last checkpoint is a check.", "",
             f"| measure | chosen ({info['policy']['chosen']['checkpoint']}) "
             f"| last ({info['policy']['last']['checkpoint']}) |", "|---|---|---|"]
    for name, label in MEASURES:
        lines.append(f"| {label} | {fmt(info['results']['chosen'].get(name))} "
                     f"| {fmt(info['results']['last'].get(name))} |")
    return "\n".join(lines) + "\n"


def run_readme(info):
    r, p, e = info["run"], info["policy"], info["evaluation"]
    best = p["training_best"]
    best_line = (f"Training's own best by `{best['score']}` was `{best['checkpoint']}` (iteration "
                 f"{best['training_iteration']}), "
                 + ("the same checkpoint." if p["chosen_is_training_best"] else "a different one.")
                 ) if best else "Training logged no best checkpoint."
    return f"""# Evaluation, {title(info)}

## What was trained

{r['controller']} controller{' with messages' if r['communication'] else ''}, {r['fleet']} agents,
trained under {r['trained_under']} storage at load {r['training_load']} on {r['trained']['place']},
`slap-mapd-coupling` commit `{r['trained']['commit']}`. Budget {r['budget_env_steps']} env steps,
{r['iterations']} iterations, a checkpoint every {r['checkpoint_every']}. Run folder `{r['run_dir']}`.

## Which policy was tested, and why

Every one of the {e['validation']['checkpoints_played']} checkpoints played the validation seeds
{e['validation']['seeds']} ({e['validation']['horizon']} steps, warm-up {e['validation']['warmup']},
{e['validation']['storage_mode']} storage). The rule {p['rule']}

- Chosen: `{p['chosen']['checkpoint']}`, after training iteration {p['chosen']['training_iteration']}.
  On validation: all keep up {p['chosen']['validation']['all_keep_up']}, throughput
  {fmt(p['chosen']['validation']['throughput'])}, pick service time
  {fmt(p['chosen']['validation']['mean_service_time'])}.
- {best_line}
- The last checkpoint, `{p['last']['checkpoint']}`, is tested as a check.

The validation and test seeds are different warehouses, and neither is a training warehouse, so the
result is not measured on the seeds that chose the policy.

## How it was tested

The test seeds {e['test']['seeds'][0]} to {e['test']['seeds'][-1]} ({len(e['test']['seeds'])}
warehouses), {e['test']['horizon']} steps with a {e['test']['warmup']}-step warm-up as the Token
Passing runs, at load {e['test']['load']}, under {e['test']['storage_mode']} storage, the rule the
run trained with. Policy on {e['device'] or 'the CPU'}, episodes on the CPU. Evaluate commit
`{e['commit']}` ({e['code']}), finished {e['finished']}.

    cd <slap-mapd-coupling at {e['commit']}>
    {e['command']}

Queue that ran it: `{e['queue']}`. Collected with `thesis-progress/scripts/collect_evaluation.py`.

Lock measure ([A91]): {e['lock_measure']}

## Files

- `summary.md`: the test results, mean and 95 % interval over the test seeds.
- `evaluation.json`: everything above in a form scripts read.
- `validation.jsonl`, `test.jsonl`: one row per episode.
- `evaluate_summary.md`: evaluate's own summary (no comparison, one storage rule per run).
"""


def comparison(fleet, collected):
    """The gain of each adaptive rule over fixed storage per controller, the chosen policies."""
    def metrics(dest):
        out = []
        for r in rows(dest / "test.jsonl"):
            if r["role"] == "chosen":
                out.append(RunMetrics.model_validate(
                    {k: v for k, v in r.items() if k in RunMetrics.model_fields}))
        return out

    by_arm = {}
    for info, dest in collected:
        by_arm.setdefault(info["run"]["arm_folder"], {})[info["run"]["trained_under"]] = dest
    lines = [f"# Fleet {fleet}: adaptive storage against fixed storage", "",
             "Each controller's run trained under fixed storage, played under fixed storage, against "
             "its run trained under the adaptive rule, played under that rule. Chosen policies, paired "
             "seed by seed on the test seeds (eq:rqformal). Gain = fixed minus adaptive mean pick "
             "service time, so positive is faster. Given only when every seed keeps up.", "",
             "| controller | rule | seeds | all keep up | gain | 95 % CI | relative gain % [CI] "
             "| pick service fixed | pick service rule | throughput fixed | throughput rule |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    for arm, regimes in sorted(by_arm.items()):
        if "fixed" not in regimes:
            continue
        fixed = metrics(regimes["fixed"])
        for rule in ("demand", "congestion"):
            if rule not in regimes:
                continue
            try:
                res = compare_paired(fixed, metrics(regimes[rule]))
            except ValueError as error:
                lines.append(f"| {arm} | {rule} | {error} |" + " |" * 8)
                continue
            mean = lambda s, n: f"{s[n].mean:.3f}" if n in s else "n/a"  # noqa: E731
            gain = ci = rel = "n/a"
            if res.mean_gain is not None:
                gain, ci = f"{res.mean_gain:.3f}", f"[{res.ci_low:.3f}, {res.ci_high:.3f}]"
            if res.mean_relative_gain is not None:
                rel = (f"{res.mean_relative_gain:.3f} "
                       f"[{res.relative_ci_low:.3f}, {res.relative_ci_high:.3f}]")
            lines.append(
                f"| {arm} | {rule} | {res.num_seeds} | {res.all_keep_up} | {gain} | {ci} | {rel} "
                f"| {mean(res.fixed_summary, 'mean_service_time')} "
                f"| {mean(res.adaptive_summary, 'mean_service_time')} "
                f"| {mean(res.fixed_summary, 'throughput')} "
                f"| {mean(res.adaptive_summary, 'throughput')} |")
    return "\n".join(lines) + "\n"


def main():
    global ROOT, RESULTS
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--fleet", type=int, required=True)
    parser.add_argument("--eval-name", default="evaluation_horizon10000_warmup5000")
    parser.add_argument("--queue", default=None, help="the queue folder that ran the evaluation")
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--root", default=None, help="holds training/ and evaluation/")
    parser.add_argument("--results", default=None, help="where the small files are copied")
    args = parser.parse_args()
    ROOT = Path(args.root).expanduser() if args.root else ROOT
    RESULTS = Path(args.results).expanduser() if args.results else RESULTS

    eval_commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True,
                                 text=True).stdout.strip()
    training = ROOT / "training" / f"fleet_{args.fleet}"
    collected, waiting = [], []
    for run in sorted(Path(p) for p in glob.glob(str(training / "*" / "*"))):
        if (run / args.eval_name / "summary.md").exists():
            collected.append(collect_run(run, args.fleet, args.eval_name, args.queue, eval_commit,
                                         args.device))
            print("collected", run)
        elif (run / args.eval_name).exists():
            waiting.append(run)
    # Runs collected in an earlier call count for the comparison too.
    evaluation = ROOT / "evaluation" / f"fleet_{args.fleet}"
    known = {str(d) for _, d in collected}
    for path in sorted(evaluation.glob("*/*/evaluation.json")):
        if str(path.parent) not in known:
            collected.append((json.loads(path.read_text()), path.parent))
    if collected:
        (evaluation / "comparison.md").write_text(comparison(args.fleet, collected))
        out = RESULTS / f"fleet_{args.fleet}"
        for info, dest in collected:
            target = out / f"{info['run']['arm_folder']}_{info['run']['trained_under']}"
            target.mkdir(parents=True, exist_ok=True)
            for name in ("evaluation.json", "summary.md", "README.md"):
                shutil.copy2(dest / name, target / name)
        shutil.copy2(evaluation / "comparison.md", out / "comparison.md")
        print("wrote", evaluation / "comparison.md", "and copied to", out)
    for run in waiting:
        print("not finished yet, left alone:", run)


if __name__ == "__main__":
    main()
