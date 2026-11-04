"""Training curves of every run of one fleet, drawn next to the runs, one figure per measure.

Run from the workspace root, with the venv's python:

    ~/.venvs/rl/bin/python thesis-progress/scripts/training_curves.py 16

Reads every run folder ~/thesis_runs/training/fleet_<m>/<arm>/<regime>/ that holds a progress log,
finished or not (a run from bedtime.bash or from Colab, cloud/colab_cli):
- <name>_training_progress.jsonl, one line per iteration: return, tasks, backlog, standing still,
  overrides, times;
- RLlib's result.json in the Tune folder, for the losses, entropy, KL and explained variance.
Writes ~/thesis_runs/training/fleet_<m>/figures/<measure>.png, replacing what was there, and
table.md with the first and last five iterations of each run. Pass --training DIR for runs kept
elsewhere.

These are training episodes (a random start, horizon steps each). They show whether and how fast
an arm learns. They are not the evaluation: whether demand storage beats fixed storage is read
from `slap-mapd evaluate` on the test seeds (appendix_results.py).
"""

import argparse
import glob
import json
import os
import statistics
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "images"))
from appendix_data import ARMS, ARM_COLOUR, plt, style  # noqa: E402

ORDER = ("token_passing", "centralised", "section", "decentralised", "decentralised_comm")
REGIME_STYLE = {"fixed_only": ("-", "fixed"), "matched": ("--", "demand")}
RUNNERS = 3  # env runners on every machine, so an iteration is 3 episodes

# (file the measure is in, field, axis label)
MEASURES = [
    ("progress", "episode_return_mean", "episode return"),
    ("progress", "tasks_completed", "tasks done per episode"),
    ("progress", "tasks_released", "tasks released per episode"),
    ("progress", "done_share", "share of released tasks done"),
    ("progress", "backlog", "backlog at episode end"),
    ("progress", "standing_still_fraction", "share of robot steps standing still"),
    ("progress", "override_rate", "share of choices overridden"),
    ("progress", "time_this_iter_s", "seconds per iteration"),
    ("health", "policy_loss", "policy loss"),
    ("health", "value_loss", "value loss"),
    ("health", "entropy", "entropy"),
    ("health", "kl", "KL divergence"),
    ("health", "explained", "value explained variance"),
]


def read_jsonl(path):
    return [json.loads(line) for line in open(path) if line.strip()]


def label(arm):
    return ARMS.get(arm, arm.replace("decentralised_comm", "decentralised, communication"))


def colour(arm):
    return ARM_COLOUR.get(arm, "#7a5195")


def load_run(folder):
    """The progress and health rows of one run folder, or None without a progress log."""
    progress = glob.glob(os.path.join(folder, "*_training_progress.jsonl"))
    if not progress:
        return None
    rows = read_jsonl(progress[0])
    for r in rows:
        if r.get("tasks_released"):
            r["done_share"] = r["tasks_completed"] / r["tasks_released"]
    horizon = 2000
    spec = glob.glob(os.path.join(folder, "*_spec.json"))
    if spec:
        horizon = json.load(open(spec[0])).get("experiment", {}).get("horizon", horizon)
    health = []
    result = glob.glob(os.path.join(folder, "*", "*", "result.json"))
    if result:
        for r in read_jsonl(result[0]):
            learner = r.get("learners", {}).get("shared_policy", {})
            health.append(dict(iteration=r["training_iteration"],
                               policy_loss=learner.get("policy_loss"),
                               value_loss=learner.get("vf_loss"), entropy=learner.get("entropy"),
                               kl=learner.get("mean_kl_loss"),
                               explained=learner.get("vf_explained_var")))
    return dict(progress=rows, health=health, steps=RUNNERS * horizon,
                done=os.path.exists(os.path.join(folder, "done")))


def find_runs(fleet_dir):
    runs = {}
    for folder in sorted(glob.glob(os.path.join(fleet_dir, "*", "*"))):
        arm, regime = folder.split(os.sep)[-2:]
        if regime not in REGIME_STYLE or ".failed" in arm:
            continue
        run = load_run(folder)
        if run:
            runs[(arm, regime)] = run
    return dict(sorted(runs.items(), key=lambda kv: (ORDER.index(kv[0][0])
                                                     if kv[0][0] in ORDER else 99, kv[0][1])))


def draw(runs, fleet, out):
    paths = []
    for source, field, axis in MEASURES:
        fig, ax = plt.subplots(figsize=(7.5, 4.2))
        drawn = False
        for (arm, regime), run in runs.items():
            rows = [r for r in run[source] if r.get(field) is not None]
            if not rows:
                continue
            drawn = True
            ls, rule = REGIME_STYLE[regime]
            ax.plot([r["iteration"] * run["steps"] / 1000 for r in rows], [r[field] for r in rows],
                    color=colour(arm), ls=ls, lw=1.6,
                    label=f"{label(arm)}, {rule}{'' if run['done'] else ' (running)'}")
        if not drawn:
            plt.close(fig)
            continue
        ax.set_xlabel("training timesteps (thousands)")
        ax.set_ylabel(axis)
        ax.set_title(f"Fleet {fleet} training: {axis}", loc="left", fontsize=11)
        style(ax)
        ax.legend(frameon=False, fontsize=8, ncol=3, loc="upper center",
                  bbox_to_anchor=(0.5, -0.18))
        path = os.path.join(out, f"{field}.png")
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        paths.append(path)
    return paths


def table(runs, out):
    def mean(rows, field):
        values = [r[field] for r in rows if r.get(field) is not None]
        return statistics.fmean(values) if values else float("nan")

    lines = ["| run | iterations | return | done share | backlog | standing still | overridden |"
             " s per iteration |", "|---|---|---|---|---|---|---|---|"]
    for (arm, regime), run in runs.items():
        p = run["progress"]
        first, last = p[:5], p[-5:]
        lines.append(
            f"| {label(arm)}, {REGIME_STYLE[regime][1]}{'' if run['done'] else ' (running)'} | "
            f"{len(p)} | {mean(first, 'episode_return_mean'):.0f} to "
            f"{mean(last, 'episode_return_mean'):.0f} | {mean(first, 'done_share'):.0%} to "
            f"{mean(last, 'done_share'):.0%} | {mean(first, 'backlog'):.0f} to "
            f"{mean(last, 'backlog'):.0f} | {mean(last, 'standing_still_fraction'):.2f} | "
            f"{mean(last, 'override_rate'):.2f} | {mean(p, 'time_this_iter_s'):.0f} |")
    path = os.path.join(out, "table.md")
    open(path, "w").write("First five iterations to the last five.\n\n" + "\n".join(lines) + "\n")
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("fleet", type=int)
    parser.add_argument("--training", default=os.path.expanduser("~/thesis_runs/training"))
    args = parser.parse_args()
    fleet_dir = os.path.join(args.training, f"fleet_{args.fleet}")
    runs = find_runs(fleet_dir)
    if not runs:
        raise SystemExit(f"No run with a progress log in {fleet_dir}.")
    out = os.path.join(fleet_dir, "figures")
    os.makedirs(out, exist_ok=True)
    for path in draw(runs, args.fleet, out):
        print(path)
    print(table(runs, out))


if __name__ == "__main__":
    main()
