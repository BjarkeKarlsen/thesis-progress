"""
The figures of the Observation depth and reward weights appendix (I.Reward.tex, app:reward).

Run:  python thesis-progress/scripts/images/appendix_controllers.py   (from the workspace root)
Out:  thesis-progress/scripts/Images/app_reward_terms.png   fig:app:rewardterms
      thesis-progress/scripts/Images/app_reward_cng.png     fig:app:rewardcng

Reads
- results/J_training/fleet_<m>/<arm>/progress.jsonl, one line per training iteration with
  env_steps, episode_step and the return terms training/callbacks.py logs per episode
  (return_shaping, return_deliver, return_override, return_wait, return_move,
  return_congestion). The file name and env_steps are assumed until M5 of
  decisions/active/measures_plan.md writes them.
- results/reward_sweep/fleet_8/<parameter>/load_sweep.jsonl, test rows of the arms trained at
  each value of a reward weight, with "varied" and "value" as in the parameter sweep. This run
  is not built yet.
A missing run is drawn as a placeholder.
"""
import os
import statistics

from appendix_data import (RESULTS, ARMS, ARM_COLOUR, C, plt, read_jsonl, mean_and_half_width,
                           style, panel_title, placeholder, save)

TRAINING = os.path.join(RESULTS, "J_training")
REWARD = os.path.join(RESULTS, "reward_sweep", "fleet_8")
TERMS = (("return_shaping", "shaping"), ("return_deliver", "delivery"),
         ("return_override", "override"), ("return_wait", "wait"), ("return_move", "move"),
         ("return_congestion", "crowding"))
LEARNED = ("centralised", "section", "decentralised")


def reward_terms(fleet=8, last=0.1):
    """The mean of each reward term per agent and step, over the last tenth of training, one
    bar group per learned arm. Shows whether the crowding term is large enough to matter
    next to the step costs (app:cal:reward, Appendixes.md section 5)."""
    fig, ax = plt.subplots(figsize=(6.4, 3.0))
    width = 0.8 / len(LEARNED)
    found = False
    for k, arm in enumerate(LEARNED):
        rows = read_jsonl(os.path.join(TRAINING, f"fleet_{fleet}", arm, "progress.jsonl"))
        if not rows:
            continue
        found = True
        tail = rows[-max(1, int(len(rows) * last)):]
        means = [statistics.fmean(r[key] / (r["episode_step"] * fleet) for r in tail)
                 for key, _ in TERMS]
        ax.barh([i + (k - 1) * width for i in range(len(TERMS))], means, height=width,
                color=ARM_COLOUR[arm], label=ARMS[arm])
    ax.set_yticks(range(len(TERMS)), [name for _, name in TERMS])
    ax.invert_yaxis()
    ax.axvline(0, color=C["text"], lw=0.8)
    ax.set_xlabel("mean reward per agent and step")
    style(ax)
    ax.grid(axis="x", color=C["edge"], alpha=0.3, lw=0.6)
    if found:
        ax.legend(frameon=False, fontsize=9)
    else:
        placeholder(ax, f"results/J_training/fleet_{fleet}/<arm>/progress.jsonl")
    return save(fig, "app_reward_terms.png")


def reward_cng():
    """The crowding weight n_cng in {0, 0.1, 1, 2} on the 8-agent warehouse: (a) the mean
    crowding, (b) the mean blocked time, (c) the throughput, one line per learned arm. Choose
    the smallest weight that lowers blocked time without lowering throughput."""
    parameter = "reward.congestion_weight"
    rows = read_jsonl(os.path.join(REWARD, parameter, "load_sweep.jsonl"))
    fields = (("mean_crowding", "mean\ncrowding"), ("mean_blocked_time", "mean blocked\ntime"),
              ("throughput", "throughput"))
    fig, axes = plt.subplots(len(fields), 1, figsize=(5.2, 6.0), sharex=True,
                             gridspec_kw=dict(hspace=0.35))
    for arm in LEARNED:
        by_value = {}
        for r in rows:
            if r.get("varied") == parameter and r["controller"] == arm:
                by_value.setdefault(r["value"], []).append(r)
        xs = sorted(by_value)
        for ax, (field, _) in zip(axes, fields):
            values = [mean_and_half_width([r.get(field) for r in by_value[x]]) for x in xs]
            ax.errorbar(xs, [v[0] for v in values], yerr=[v[1] for v in values],
                        color=ARM_COLOUR[arm], marker="o", ms=5, lw=2, capsize=3,
                        elinewidth=1, label=ARMS[arm])
    for ax, (_, label), panel in zip(axes, fields, "abc"):
        ax.set_ylabel(label)
        ax.axvline(0.1, color=C["node"], ls=":", lw=1)
        panel_title(ax, f"({panel})")
        style(ax)
    axes[-1].set_xlabel(r"crowding weight $n_{\mathrm{cng}}$")
    if rows:
        axes[0].legend(frameon=False, fontsize=9)
    else:
        placeholder(axes[0], f"results/reward_sweep/fleet_8/{parameter}")
    return save(fig, "app_reward_cng.png")


def appendix_controllers():
    return [reward_terms(), reward_cng()]


if __name__ == "__main__":
    for path in appendix_controllers():
        print(path)
