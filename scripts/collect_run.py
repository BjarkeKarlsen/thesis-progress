"""Copy one trained and evaluated run into the results folders the appendix figures read.

Run from the workspace root:

    python thesis-progress/scripts/collect_run.py RUN_DIR [--evaluation NAME]

RUN_DIR is the --output of `slap-mapd train` (at home ~/thesis_runs/training/..., or a run folder
downloaded from Kaggle), evaluated with `slap-mapd evaluate`. NAME is the evaluation folder inside
it, by default the one of the Token Passing setting, evaluation_horizon10000_warmup5000, made by

    slap-mapd evaluate RUN_DIR --storage-modes fixed demand --horizon 10000 --warmup 5000

The arm, fleet and regime come from the run's spec. It writes

    results/J_training/fleet_<m>/<controller>/<regime>/  training.jsonl, spec.json, validation.jsonl
    results/L_results/fleet_<m>/<controller>/<regime>/   test.jsonl, summary.md

replacing what was there. training.jsonl is RLlib's own log (result.json), one line per training
iteration, cut to the fields the figures read: the environment steps, the return and the losses.
The full log repeats the whole config on every line, about 22 kB, so it stays in the run
folder. appendix_training.py draws the J folders and appendix_results.py the L folders.
"""

import argparse
import glob
import json
import os
import shutil

RESULTS = "thesis-progress/results"


def _cut(row):
    """The fields of one RLlib result line the figures read."""
    learner = row.get("learners", {}).get("shared_policy", {})
    runners = row.get("env_runners", {})
    return {
        "iteration": row["training_iteration"],
        "env_steps": row.get("num_env_steps_sampled_lifetime"),
        "seconds": row.get("time_this_iter_s"),
        "episode_return_mean": runners.get("episode_return_mean"),
        "policy_loss": learner.get("policy_loss"),
        "value_loss": learner.get("vf_loss"),
        "entropy": learner.get("entropy"),
        "kl": learner.get("mean_kl_loss"),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("run_dir")
    parser.add_argument("--evaluation", default="evaluation_horizon10000_warmup5000")
    args = parser.parse_args()

    (spec_path,) = glob.glob(os.path.join(args.run_dir, "*_spec.json"))
    spec = json.load(open(spec_path))
    controller, regime = spec["controller"], spec["regime"]
    fleet = spec["experiment"]["num_agents"]
    # A run continued after a stop has one trial folder per session, so every result.json is
    # joined in the order of its iterations.
    results = sorted(glob.glob(os.path.join(args.run_dir, "*", "*", "result.json")))
    if not results:
        raise SystemExit(f"{args.run_dir} holds no result.json, is it a training run?")
    evaluation = os.path.join(args.run_dir, args.evaluation)
    for name in ("validation.jsonl", "test.jsonl"):
        if not os.path.exists(os.path.join(evaluation, name)):
            raise SystemExit(f"{evaluation} holds no {name}, run slap-mapd evaluate first.")

    training = os.path.join(RESULTS, "J_training", f"fleet_{fleet}", controller, regime)
    test = os.path.join(RESULTS, "L_results", f"fleet_{fleet}", controller, regime)
    for folder in (training, test):
        os.makedirs(folder, exist_ok=True)
    lines = {}
    for path in results:
        for line in open(path):
            if line.strip():
                row = json.loads(line)
                lines[row["training_iteration"]] = _cut(row)
    with open(os.path.join(training, "training.jsonl"), "w") as out:
        out.writelines(json.dumps(lines[i]) + "\n" for i in sorted(lines))
    shutil.copy(spec_path, os.path.join(training, "spec.json"))
    # evaluate names each validation row by its checkpoint. Checkpoint k is saved after
    # iteration frequency * (k + 1), the last one at the end, so each row gets its steps.
    frequency = (spec.get("checkpoint") or {}).get("frequency") or 0
    last = max(lines)
    rows = [json.loads(line) for line in open(os.path.join(evaluation, "validation.jsonl"))
            if line.strip()]
    names = sorted({r["checkpoint"] for r in rows})
    with open(os.path.join(training, "validation.jsonl"), "w") as out:
        for r in rows:
            k = names.index(r["checkpoint"])
            iteration = last if not frequency or k == len(names) - 1 else min(
                frequency * (k + 1), last)
            r.update(iteration=iteration, env_steps=lines[iteration]["env_steps"])
            out.write(json.dumps(r) + "\n")
    shutil.copy(os.path.join(evaluation, "test.jsonl"), test)
    if os.path.exists(os.path.join(evaluation, "summary.md")):
        shutil.copy(os.path.join(evaluation, "summary.md"), test)
    print(f"{controller}, fleet {fleet}, {regime}: {len(lines)} iterations to {training}, "
          f"the test rows to {test}")


if __name__ == "__main__":
    main()
