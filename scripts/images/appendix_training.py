"""
The figures of the Model and training appendix (J.Training.tex, app:training).

Run:  python thesis-progress/scripts/images/appendix_training.py   (from the workspace root)
Out:  thesis-progress/scripts/Images/app_training_curves.png   fig:app:trainingcurves
      thesis-progress/scripts/Images/app_training_health.png   fig:app:traininghealth

Reads
- results/J_training/fleet_<m>/<arm>/validation.jsonl, one row per saved checkpoint and
  validation seed, the evaluation row of the catalogue plus env_steps. The training curves
  come from validation, not from the training return (measures_catalogue.md, "What each
  phase records"). Written by M5 of decisions/active/measures_plan.md, not built yet.
- results/J_training/fleet_<m>/<arm>/progress.jsonl, one line per training iteration with
  env_steps, policy_loss, value_loss, entropy and kl (assumed names, also M5).
A missing run is drawn as a placeholder.
"""
import os
import statistics

from appendix_data import (RESULTS, ARMS, ARM_COLOUR, C, plt, read_jsonl, share, style,
                           panel_title, placeholder, save)

TRAINING = os.path.join(RESULTS, "J_training")
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


def training_curves(fleet=8):
    """Per learned arm, against the environment steps of training, (a) the share of
    validation seeds that keep up and (b) the mean pick service time over them. A ring marks
    the checkpoint [A60] chooses. The budget is where the slowest arm levels off
    (app:cal:budget)."""
    fig, (top, bottom) = plt.subplots(2, 1, figsize=(5.6, 4.6), sharex=True,
                                      gridspec_kw=dict(height_ratios=(2, 3), hspace=0.3))
    found = False
    for arm in LEARNED:
        groups = by_checkpoint(read_jsonl(os.path.join(TRAINING, f"fleet_{fleet}", arm,
                                                       "validation.jsonl")))
        if not groups:
            continue
        found = True
        steps = list(groups)
        service = [statistics.fmean(r["mean_service_time"] for r in g if r["mean_service_time"])
                   for g in groups.values()]
        colour = ARM_COLOUR[arm]
        top.plot(steps, [share(g, "keeps_up") for g in groups.values()], color=colour, lw=1.8,
                 label=ARMS[arm])
        bottom.plot(steps, service, color=colour, lw=1.8)
        best = chosen_checkpoint(groups)
        bottom.plot(best, service[steps.index(best)], marker="o", ms=9, mfc="none",
                    mec=colour, mew=1.8)
    top.set_ylabel("validation seeds\nthat keep up")
    top.set_ylim(-0.05, 1.05)
    bottom.set_ylabel(r"mean pick service" "\n" r"time $\bar\zeta_T$")
    bottom.set_xlabel("environment steps of training")
    for ax, label in ((top, "(a)"), (bottom, "(b)")):
        panel_title(ax, label)
        style(ax)
    if found:
        top.legend(frameon=False, fontsize=9)
    else:
        placeholder(bottom, f"results/J_training/fleet_{fleet}/<arm>/validation.jsonl")
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
        rows = read_jsonl(os.path.join(TRAINING, f"fleet_{fleet}", arm, "progress.jsonl"))
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
        placeholder(axes[0], f"results/J_training/fleet_{fleet}/<arm>/progress.jsonl")
    return save(fig, "app_training_health.png")


def appendix_training():
    return [training_curves(), training_health()]


if __name__ == "__main__":
    for path in appendix_training():
        print(path)
