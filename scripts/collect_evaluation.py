"""Documents a finished evaluation of trained runs, with everything the thesis needs to say what
was tested, how and why, and builds the fleet's comparison tables.

Run from the `slap-mapd-coupling` checkout that evaluated, with the venv's python:

    cd ~/worktrees/validation-during-training
    PYTHONPATH=src ~/.venvs/rl/bin/python ~/Documents/thesis/thesis-progress/scripts/collect_evaluation.py \
        --fleet 16 --queue ~/thesis_runs/eval_2026-11-13_fleet16

`evaluate` (main 9261061 on) writes each run's evaluation to
`~/thesis_runs/evaluation/fleet_<m>/<arm>/<regime>/<evaluation name>/`, with its rows and an
`evaluation.json`. For every such folder whose evaluation finished (it holds `summary.md`) this

1. renames evaluate's own summary to `evaluate_summary.md` (for a run played under fixed and an
   adaptive rule it already holds the paired gain of that run),
2. adds to `evaluation.json` what evaluate does not know: where and on which commit the run
   trained, its iterations, training's own best checkpoint, the validation numbers of the chosen
   one, the queue, and the test results (mean and 95 % interval per measure),
3. writes `summary.md` (the test results) and `README.md` (the same in words, with the commands),
4. writes the fleet's `comparison.md`, beside the runs:
   - the main setup ([A84]): a run trained under fixed storage played under fixed and under demand
     storage, the same policy, paired seed by seed (eq:rqformal),
   - the second setup: the run trained under fixed storage played under fixed, against the run
     trained under demand storage played under demand, paired seed by seed,
5. copies the small files to `thesis-progress/results/L_results/fleet_<m>/`.

It can run again: a folder already collected is collected again from its rows.
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
# The lock measure ([A91]) is a number per episode. These thresholds are only reported, the
# threshold used in the thesis is chosen from how the numbers spread.
LOCK_THRESHOLDS = (500, 1250)
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
    ("longest_two_agent_hold", "longest time two agents held a task at once"),
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


def collect_run(folder, run, fleet, queue):
    """`folder` is the evaluation, `run` the training run it evaluated."""
    spec = json.loads(next(run.glob("*_spec.json")).read_text())
    evaluate_record = json.loads((folder / "evaluation.json").read_text()).get(
        "evaluate", json.loads((folder / "evaluation.json").read_text()))
    if not (folder / "evaluate_summary.md").exists():
        (folder / "summary.md").rename(folder / "evaluate_summary.md")
    validation = rows(folder / "validation.jsonl")
    test = rows(folder / "test.jsonl")
    frequency = spec["checkpoint"]["frequency"]
    progress = rows(next(run.glob("*_training_progress.jsonl")))
    chosen = next(r["checkpoint"] for r in test if r["role"] == "chosen")
    last = next(r["checkpoint"] for r in test if r["role"] == "last")
    best = training_best(run)
    per_checkpoint = {}
    for r in validation:
        per_checkpoint.setdefault(r["checkpoint"], []).append(r)

    def policy(name):
        played = per_checkpoint.get(name, [])
        return {
            "checkpoint": name, "training_iteration": checkpoint_iteration(name, frequency),
            "path": str(next(run.glob(f"*/*/{name}"), "")),
            "validation": {
                "seeds": [r["seed"] for r in played],
                "all_keep_up": all(r["keeps_up"] for r in played) if played else None,
                "throughput": interval(r["throughput"] for r in played),
                "mean_service_time": interval(r["mean_service_time"] for r in played),
            },
        }

    modes = list(dict.fromkeys(r["storage_mode"] for r in test))
    results = {}
    for role in ("chosen", "last"):
        for mode in modes:
            played = [r for r in test if r["role"] == role and r["storage_mode"] == mode]
            cell = {name: interval(r.get(name) for r in played) for name, _ in MEASURES}
            cell["seeds"] = [r["seed"] for r in played]
            holds = [r.get("longest_two_agent_hold") for r in played]
            cell["locked_seeds"] = {
                str(x): [r["seed"] for r, h in zip(played, holds) if h is not None and h >= x]
                for x in LOCK_THRESHOLDS
            }
            results.setdefault(role, {})[mode] = cell
    first = test[0]
    info = {
        "run": {
            "fleet": fleet, "controller": spec["controller"], "arm_folder": run.parent.name,
            "communication": spec.get("communication", False),
            # The folder name, fixed, demand or congestion. Runs trained before the rename (PR #206)
            # store fixed_only or matched in their settings, kept beside it.
            "trained_under": run.name, "regime_in_settings": spec["regime"], "run_dir": str(run),
            "trained": where_trained(run),
            "budget_env_steps": spec["ppo"]["training_budget_env_steps"],
            "iterations": len(progress), "checkpoint_every": frequency,
            "training_load": spec["arrival_rate"],
            "training_episode": {"horizon": spec["horizon"], "warmup": spec["warmup"]},
        },
        "policy": {
            "rule": "[A60]: of the checkpoints that keep up on every validation seed, the one with "
                    "the shortest mean pick service time. If none keeps up, the highest throughput.",
            "checkpoints_validated": len(per_checkpoint),
            "chosen": policy(chosen), "last": policy(last),
            "training_best": {"score": best[0], **policy(best[1])} if best else None,
            "chosen_is_training_best": bool(best and best[1] == chosen),
        },
        "evaluation": {
            "commit": evaluate_record.get("code_commit"), "code": CODE,
            "device": evaluate_record.get("device"),
            "command": (f"PYTHONPATH=src python -m slap_mapd_coupling.main evaluate {run} "
                        f"--test-seeds {len(results['chosen'][modes[0]]['seeds'])} "
                        f"--horizon {first['horizon']} --warmup {first['warmup']}"
                        + "".join(f" --storage-modes {m}" for m in modes if len(modes) > 1)
                        + (" --gpu" if evaluate_record.get("device") == "cuda" else "")),
            "queue": str(queue) if queue else None,
            "validation": {"seeds": sorted({r["seed"] for r in validation}),
                           "horizon": validation[0]["horizon"], "warmup": validation[0]["warmup"],
                           "storage_mode": validation[0]["storage_mode"]},
            "test": {"seeds": results["chosen"][modes[0]]["seeds"], "horizon": first["horizon"],
                     "warmup": first["warmup"], "storage_modes": modes,
                     "load": first["arrival_rate"], "num_agents": first["num_agents"]},
            "finished": evaluate_record.get("finished") or datetime.datetime.fromtimestamp(
                (folder / "test.jsonl").stat().st_mtime).isoformat(timespec="minutes"),
            "lock_measure": "longest_two_agent_hold per episode ([A91]). Seeds at or above "
                            f"{', '.join(map(str, LOCK_THRESHOLDS))} steps are listed. The "
                            "threshold the thesis uses is chosen from how the numbers spread.",
        },
        "results": results,
        "evaluate": evaluate_record,
    }
    (folder / "evaluation.json").write_text(json.dumps(info, indent=1))
    (folder / "summary.md").write_text(run_summary(info))
    (folder / "README.md").write_text(run_readme(info))
    return info, folder


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
    e = info["evaluation"]
    columns = [(role, mode) for role in ("chosen", "last") for mode in e["test"]["storage_modes"]]
    lines = [f"# Test results, {title(info)}", "",
             f"Mean and 95 % interval over the {len(e['test']['seeds'])} test seeds, "
             f"{e['test']['horizon']} steps with a {e['test']['warmup']}-step warm-up. The chosen "
             "policy is the result, the last checkpoint a check. The paired gain between storage "
             "rules is in `evaluate_summary.md` and the fleet's `comparison.md`.", "",
             "| measure | " + " | ".join(
                 f"{role} ({info['policy'][role]['checkpoint']}) under {mode}"
                 for role, mode in columns) + " |",
             "|---|" + "---|" * len(columns)]
    for name, label in MEASURES:
        lines.append(f"| {label} | " + " | ".join(
            fmt(info["results"][role][mode].get(name)) for role, mode in columns) + " |")
    for x in LOCK_THRESHOLDS:
        lines.append(f"| seeds with two agents holding a task {x} steps or more | " + " | ".join(
            str(len(info["results"][role][mode]["locked_seeds"][str(x)]))
            for role, mode in columns) + " |")
    return "\n".join(lines) + "\n"


def run_readme(info):
    r, p, e = info["run"], info["policy"], info["evaluation"]
    best = p["training_best"]
    best_line = (f"Training's own best by `{best['score']}` was `{best['checkpoint']}` (iteration "
                 f"{best['training_iteration']}), "
                 + ("the same checkpoint." if p["chosen_is_training_best"] else "a different one.")
                 ) if best else "Training logged no best checkpoint."
    setup = ("the main setup ([A84]): the policy trained under fixed storage, played under every "
             "storage rule" if r["trained_under"] == "fixed" and len(e["test"]["storage_modes"]) > 1
             else "the second setup: the policy played under the storage rule it trained with")
    return f"""# Evaluation, {title(info)}

## What was trained

{r['controller']} controller{' with messages' if r['communication'] else ''}, {r['fleet']} agents,
trained under {r['trained_under']} storage at load {r['training_load']} on {r['trained']['place']},
`slap-mapd-coupling` commit `{r['trained']['commit']}`. Budget {r['budget_env_steps']} env steps,
{r['iterations']} iterations, a checkpoint every {r['checkpoint_every']}. Run folder `{r['run_dir']}`.

## Which policy was tested, and why

Validation goes with training and the test is kept apart. Each of the {p['checkpoints_validated']}
checkpoints played the validation seeds {e['validation']['seeds']} ({e['validation']['horizon']}
steps, warm-up {e['validation']['warmup']}, {e['validation']['storage_mode']} storage, the rule it
trained under). The rule {p['rule']}

- Chosen: `{p['chosen']['checkpoint']}`, after training iteration {p['chosen']['training_iteration']}.
  On validation: all keep up {p['chosen']['validation']['all_keep_up']}, throughput
  {fmt(p['chosen']['validation']['throughput'])}, pick service time
  {fmt(p['chosen']['validation']['mean_service_time'])}.
- {best_line}
- The last checkpoint, `{p['last']['checkpoint']}`, is tested as a check.

The validation and test seeds are different warehouses, and neither is a training warehouse, so the
result is not measured on the seeds that chose the policy.

## How it was tested

This is {setup}. Test seeds {e['test']['seeds'][0]} to {e['test']['seeds'][-1]}
({len(e['test']['seeds'])} warehouses), {e['test']['horizon']} steps with a
{e['test']['warmup']}-step warm-up as the Token Passing runs, at load {e['test']['load']}, under
{' and '.join(e['test']['storage_modes'])} storage. Policy on {e['device']}, episodes on the CPU.
Evaluate commit `{e['commit']}` ({e['code']}), finished {e['finished']}.

    cd <slap-mapd-coupling at {e['commit']}>
    {e['command']}

Queue that ran it: `{e['queue']}`. Documented with `thesis-progress/scripts/collect_evaluation.py`.

Lock measure ([A91]): {e['lock_measure']}

## Files

- `summary.md`: the test results, mean and 95 % interval over the test seeds.
- `evaluate_summary.md`: evaluate's own summary, the paired gain when played under two rules.
- `evaluation.json`: everything above in a form scripts read, evaluate's own record under "evaluate".
- `validation.jsonl`, `test.jsonl`: one row per episode.
"""


def chosen_metrics(folder, mode):
    return [RunMetrics.model_validate({k: v for k, v in r.items() if k in RunMetrics.model_fields})
            for r in rows(folder / "test.jsonl")
            if r["role"] == "chosen" and r["storage_mode"] == mode]


def comparison_row(label, rule, fixed, adaptive):
    try:
        res = compare_paired(fixed, adaptive)
    except ValueError as error:
        return f"| {label} | {rule} | {error} |" + " |" * 8

    def mean(summary, name):
        return f"{summary[name].mean:.3f}" if name in summary else "n/a"

    gain = ci = rel = "n/a"
    if res.mean_gain is not None:
        gain, ci = f"{res.mean_gain:.3f}", f"[{res.ci_low:.3f}, {res.ci_high:.3f}]"
    if res.mean_relative_gain is not None:
        rel = f"{res.mean_relative_gain:.3f} [{res.relative_ci_low:.3f}, {res.relative_ci_high:.3f}]"
    return (f"| {label} | {rule} | {res.num_seeds} | {res.all_keep_up} | {gain} | {ci} | {rel} "
            f"| {mean(res.fixed_summary, 'mean_service_time')} "
            f"| {mean(res.adaptive_summary, 'mean_service_time')} "
            f"| {mean(res.fixed_summary, 'throughput')} "
            f"| {mean(res.adaptive_summary, 'throughput')} |")


def comparison(fleet, collected):
    header = ["| controller | rule | seeds | all keep up | gain | 95 % CI | relative gain % [CI] "
              "| pick service fixed | pick service rule | throughput fixed | throughput rule |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]
    by_arm = {}
    for info, folder in collected:
        by_arm.setdefault(info["run"]["arm_folder"], {})[info["run"]["trained_under"]] = (
            info, folder)
    main, second = [], []
    for arm, runs in sorted(by_arm.items()):
        if "fixed" not in runs:
            continue
        info, folder = runs["fixed"]
        fixed = chosen_metrics(folder, "fixed")
        for rule in info["evaluation"]["test"]["storage_modes"]:
            if rule != "fixed":
                main.append(comparison_row(arm, rule, fixed, chosen_metrics(folder, rule)))
        for rule in ("demand", "congestion"):
            if rule in runs:
                second.append(comparison_row(
                    arm, rule, fixed, chosen_metrics(runs[rule][1], rule)))
    return "\n".join([
        f"# Fleet {fleet}: adaptive storage against fixed storage", "",
        "Gain = fixed minus adaptive mean pick service time, so positive is faster, paired seed by "
        "seed on the test seeds (eq:rqformal), chosen policies. Given only when every seed keeps "
        "up.", "",
        "## Main setup ([A84]): one policy, trained under fixed storage, played under each rule", "",
        *header, *main, "",
        "## Second setup: each rule with the policy trained under it", "",
        "The run trained under fixed storage, played under fixed, against the run trained under the "
        "rule, played under it. Two different policies, so the gain mixes storage and training.", "",
        *header, *second, ""])


def main():
    global ROOT, RESULTS
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--fleet", type=int, required=True)
    parser.add_argument("--eval-name", default="evaluation_horizon10000_warmup5000")
    parser.add_argument("--queue", default=None, help="the queue folder that ran the evaluation")
    parser.add_argument("--root", default=None, help="holds training/ and evaluation/")
    parser.add_argument("--results", default=None, help="where the small files are copied")
    args = parser.parse_args()
    ROOT = Path(args.root).expanduser() if args.root else ROOT
    RESULTS = Path(args.results).expanduser() if args.results else RESULTS
    evaluation = ROOT / "evaluation" / f"fleet_{args.fleet}"
    collected, waiting = [], []
    for folder in sorted(Path(p) for p in glob.glob(str(evaluation / "*" / "*" / args.eval_name))):
        run = ROOT / "training" / f"fleet_{args.fleet}" / folder.parent.parent.name / folder.parent.name
        if (folder / "summary.md").exists() or (folder / "evaluate_summary.md").exists():
            if not (folder / "summary.md").exists():  # collected before, collect again
                shutil.copy2(folder / "evaluate_summary.md", folder / "summary.md")
            collected.append(collect_run(folder, run, args.fleet, args.queue))
            print("collected", folder)
        else:
            waiting.append(folder)
    if collected:
        (evaluation / "comparison.md").write_text(comparison(args.fleet, collected))
        out = RESULTS / f"fleet_{args.fleet}"
        for info, folder in collected:
            target = out / f"{info['run']['arm_folder']}_{info['run']['trained_under']}"
            target.mkdir(parents=True, exist_ok=True)
            for name in ("evaluation.json", "summary.md", "README.md", "evaluate_summary.md"):
                shutil.copy2(folder / name, target / name)
        shutil.copy2(evaluation / "comparison.md", out / "comparison.md")
        print("wrote", evaluation / "comparison.md", "and copied to", out)
    for folder in waiting:
        print("not finished yet, left alone:", folder)


if __name__ == "__main__":
    main()
