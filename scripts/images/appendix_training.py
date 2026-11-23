"""
The figures of the Model and training appendix (J.Training.tex, app:training).

Run:  python thesis-progress/scripts/images/appendix_training.py   (from the workspace root)
Out:  thesis-progress/scripts/Images/app_training_curves.png   fig:app:trainingcurves
      thesis-progress/scripts/Images/app_training_health.png   fig:app:traininghealth

training_curves() reads the long 16-agent runs of the main result, see LONG_RUNS below: per arm
and storage rule, validation.jsonl (one row per saved checkpoint and validation seed) and
evaluation.json (the chosen checkpoint, the budget and the checkpoint period) of
`slap-mapd evaluate`.

training_health() reads, for each learned arm trained under fixed storage (fixed_only),
- results/J_training/fleet_<m>/<arm>/fixed_only/validation.jsonl, one row per saved checkpoint
  and validation seed, the rows of `slap-mapd evaluate` with the checkpoint's iteration and
  env_steps added. The training curves come from validation, not from the training return
  (measures_catalogue.md, "What each phase records").
- results/J_training/fleet_<m>/<arm>/fixed_only/training.jsonl, one line per training
  iteration with env_steps, policy_loss, value_loss, entropy and kl, cut from RLlib's
  result.json.
Both are written by thesis-progress/scripts/collect_run.py from an evaluated run. A missing run
is drawn as a placeholder.
"""
import json
import os
import statistics

from appendix_data import (RESULTS, run_folder, ARMS, ARM_COLOUR, C, plt, read_jsonl, share, style,
                           panel_title, placeholder, save, RULES)

TRAINING = os.path.join(RESULTS, "J_training")
REGIME = "fixed"  # or fixed_only, for runs trained before the rename (run_folder)
LEARNED = ("centralised", "section", "decentralised")


def by_checkpoint(rows):
    """Validation rows grouped by the env_steps of their checkpoint."""
    out = {}
    for r in rows:
        out.setdefault(r["env_steps"], []).append(r)
    return dict(sorted(out.items()))


def chosen_checkpoint(groups):
    """The checkpoint rule of [A60]. Among the checkpoints that keep up on every validation
    seed, the one with the shortest mean pick service time. If none does, the one with the
    highest throughput."""
    passing = {s: rows for s, rows in groups.items() if all(r["keeps_up"] for r in rows)}
    if passing:
        return min(passing, key=lambda s: statistics.fmean(r["mean_service_time"]
                                                           for r in passing[s]))
    return max(groups, key=lambda s: statistics.fmean(r["throughput"] for r in groups[s]))


# The long 16-agent runs of the main result ([A109]): each learned arm warm-started and trained
# for 2 000 000 more steps on episodes of 16 000 steps, some resumed as <rule>_long_part2. Their
# evaluations, with the validation rows of every saved checkpoint (5 seeds of 16 000 steps), are
# in ~/thesis_runs/evaluation/fleet_16/<arm>/<rule>_long*/<EVALUATION>/.
LONG_RUNS = os.path.expanduser("~/thesis_runs/evaluation/fleet_16")
EVALUATION = "evaluation_served_horizon10000_warmup5000"
LONG_ARMS = ("centralised", "section", "decentralised", "decentralised_comm")
LONG_LABEL = {**ARMS, "decentralised_comm": "with messages"}
LONG_COLOUR = {**ARM_COLOUR, "decentralised_comm": C["comm"]}
LONG_BUDGET = 2_000_000
# An iteration gathers one 16 000-step episode from each of 3 runners, and a checkpoint is saved
# every `checkpoint_every` iterations, the k-th (from 0) at iteration checkpoint_every * (k + 1).
STEPS_PER_ITERATION = 3 * 16_000


def long_run(arm, rule):
    """The evaluation folder of the long run of `arm` under `rule`, the first part or, failing
    that, the resumed part. None when neither has been evaluated."""
    for name in (f"{rule}_long", f"{rule}_long_part2"):
        path = os.path.join(LONG_RUNS, arm, name, EVALUATION)
        if os.path.exists(os.path.join(path, "validation.jsonl")):
            return path
    return None


def long_checkpoints(path):
    """Per validated checkpoint of one long run, in saving order, its environment steps of the
    long training and its validation rows, and the name of the chosen checkpoint. A resumed
    part (budget below 2 000 000) starts where the first part stopped, so its steps are offset
    by what the first part trained."""
    with open(os.path.join(path, "evaluation.json")) as handle:
        evaluation = json.load(handle)
    offset = LONG_BUDGET - evaluation["budget_env_steps"]
    every = evaluation["checkpoint_every"]
    groups = {}
    for r in read_jsonl(os.path.join(path, "validation.jsonl")):
        groups.setdefault(r["checkpoint"], []).append(r)
    points = [(offset + STEPS_PER_ITERATION * every * (int(name.split("_")[-1]) + 1), rows)
              for name, rows in sorted(groups.items())]
    return points, evaluation["chosen"]["checkpoint"], sorted(groups)


def training_curves():
    """The long 16-agent runs, one column per storage rule. Per arm and saved checkpoint, the
    two means over the 5 validation seeds that the checkpoint rule [A60] reads, (a) the
    throughput and (b) the mean pick service time. A filled mark keeps up on every validation
    seed. A ring marks the chosen checkpoint, on the service time when some checkpoint of the
    run keeps up on every seed and on the throughput when none does. Runs not yet evaluated
    are listed on stdout."""
    rules = ("fixed", "demand", "congestion")
    fig, axes = plt.subplots(2, 3, figsize=(10.5, 5.6), sharex=True, sharey="row",
                             gridspec_kw=dict(hspace=0.18, wspace=0.08))
    missing = []
    for col, rule in enumerate(rules):
        top, bottom = axes[0, col], axes[1, col]
        for arm in LONG_ARMS:
            path = long_run(arm, rule)
            if path is None:
                missing.append(f"{arm}/{rule}_long")
                continue
            points, chosen, names = long_checkpoints(path)
            steps = [s / 1e6 for s, _ in points]
            through = [statistics.fmean(r["throughput"] for r in rows) for _, rows in points]
            service = [statistics.fmean(r["mean_service_time"] for r in rows
                                        if r["mean_service_time"]) for _, rows in points]
            passing = [all(r["keeps_up"] for r in rows) for _, rows in points]
            colour = LONG_COLOUR[arm]
            for ax, values in ((top, through), (bottom, service)):
                ax.plot(steps, values, color=colour, lw=1.4, label=LONG_LABEL[arm])
                ax.scatter(steps, values, s=16, color=colour, zorder=3,
                           facecolors=[colour if p else "white" for p in passing],
                           edgecolors=colour, linewidths=1.0)
            i = names.index(chosen)
            ring = bottom if any(passing) else top
            ring.plot(steps[i], (service if any(passing) else through)[i], marker="o", ms=11,
                      mfc="none", mec=colour, mew=1.6, zorder=4)
        panel_title(top, f"({'abc'[col]}) {RULES[rule]} storage")
        bottom.set_yscale("log")
        bottom.set_yticks((500, 1000, 2000, 5000), labels=("500", "1000", "2000", "5000"))
        bottom.minorticks_off()
        for ax in (top, bottom):
            style(ax)
    axes[0, 0].set_ylabel("throughput\n(tasks per step)")
    axes[1, 0].set_ylabel(r"mean pick service" "\n" r"time $\bar\zeta_T$ (steps)")
    fig.supxlabel("environment steps of the long training (millions)", y=0.0, fontsize=11)
    from matplotlib.lines import Line2D
    handles = [Line2D([], [], color=LONG_COLOUR[a], lw=1.6, marker="o", ms=4, label=LONG_LABEL[a])
               for a in LONG_ARMS]
    handles += [Line2D([], [], ls="", marker="o", ms=5, mfc=C["text"], mec=C["text"],
                       label="keeps up on every seed"),
                Line2D([], [], ls="", marker="o", ms=5, mfc="white", mec=C["text"],
                       label="does not")]
    fig.legend(handles=handles, loc="lower center", ncol=len(handles), frameon=False,
               bbox_to_anchor=(0.5, -0.07), fontsize=9, handletextpad=0.4, columnspacing=1.2)
    for run in missing:
        print("not evaluated yet:", run)
    return save(fig, "app_training_curves.png")


def training_health(fleet=8):
    """PPO health per learned arm against the environment steps, (a) policy loss, (b) value
    loss, (c) entropy, (d) KL divergence. Entropy near 0 means the policy stopped
    exploring."""
    fields = (("policy_loss", "policy loss"), ("value_loss", "value loss"),
              ("entropy", "entropy"), ("kl", "KL divergence"))
    fig, axes = plt.subplots(2, 2, figsize=(7.4, 4.8), sharex=True,
                             gridspec_kw=dict(hspace=0.35, wspace=0.35))
    axes = axes.ravel()
    found = False
    for arm in LEARNED:
        rows = read_jsonl(os.path.join(run_folder(TRAINING, fleet, arm, REGIME),
                                       "training.jsonl"))
        if not rows:
            continue
        found = True
        steps = [r["env_steps"] for r in rows]
        for ax, (field, _) in zip(axes, fields):
            ax.plot(steps, [r.get(field) for r in rows], color=ARM_COLOUR[arm], lw=1.4,
                    label=ARMS[arm])
    for ax, (_, label), panel in zip(axes, fields, "abcd"):
        ax.set_ylabel(label)
        panel_title(ax, f"({panel})")
        style(ax)
    for ax in axes[2:]:
        ax.set_xlabel("environment steps")
    if found:
        axes[0].legend(frameon=False, fontsize=8)
    else:
        placeholder(axes[0], f"results/J_training/fleet_{fleet}/<arm>/{REGIME}/training.jsonl")
    return save(fig, "app_training_health.png")


def appendix_training():
    return [training_curves(), training_health()]


if __name__ == "__main__":
    for path in appendix_training():
        print(path)
