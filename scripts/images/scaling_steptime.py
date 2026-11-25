"""
Mean runtime kappa_T (eq:runtime) against fleet size, one line per controller, from the step time
test on main bdfda94 (results/L_results/scaling/step_time_main, README there).

Run:  python thesis-progress/scripts/images/scaling_steptime.py   (from the workspace root)
Out:  thesis-progress/scripts/Images/scaling_steptime.png
      then copy it to thesis/Images/

Reads, five seeds 200000 to 200004 per controller and fleet (2026-11-24)
- rows.jsonl (seed 200000), seeds/rows.jsonl and section_seeds/rows.jsonl, the learned controllers,
  window mean over steps 2000 to 3000, network on the GPU.
- seeds/tp_<m>_<T>/timing.jsonl, Token Passing on the CPU, one row per seed, played for 2000 and
  3000 steps. kappa over the last 1000 steps = (assignment + routing at 3000 minus at 2000) / 1000.
Each point is the mean over the five seeds, the bar runs from the lowest to the highest seed.
"""
import json
import os

from appendix_data import RESULTS, C, plt, read_jsonl, style, save

FLEETS = (8, 16, 32, 64, 128)
SEEDS = range(200000, 200005)
STEP = os.path.join(RESULTS, "L_results", "scaling", "step_time_main")
ARMS = {"centralised": "centralised", "section": "section-based",
        "decentralised_comm": "decentralised with messages", "decentralised": "decentralised",
        "token_passing": "Token Passing (CPU)"}
COLOUR = {"token_passing": C["node"], "centralised": C["accent"], "section": C["ep_e"],
          "decentralised": C["del_e"], "decentralised_comm": C["comm"]}
MARKER = {"token_passing": "o", "centralised": "D", "section": "^", "decentralised": "s",
          "decentralised_comm": "v"}


def arm_of(row):
    if row["controller"] == "decentralised" and row.get("communication"):
        return "decentralised_comm"
    return row["controller"]


def learned():
    times = {}
    for name in ("rows.jsonl", "seeds/rows.jsonl", "section_seeds/rows.jsonl"):
        for r in read_jsonl(os.path.join(STEP, name)):
            if r["num_agents"] in FLEETS and r["seed"] in SEEDS:
                times.setdefault((arm_of(r), r["num_agents"]), {})[r["seed"]] = r["window_decision_runtime_seconds"]
    return times


def token_passing():
    def kappa_sums(m, n):
        rows = read_jsonl(os.path.join(STEP, "seeds", f"tp_{m}_{n}", "timing.jsonl"))
        return {r["seed"]: r["seconds"]["assignment"] + r["seconds"]["routing"] for r in rows}
    times = {}
    for m in FLEETS:
        early, late = kappa_sums(m, 2000), kappa_sums(m, 3000)
        times[("token_passing", m)] = {s: (late[s] - early[s]) / 1000 for s in SEEDS}
    return times


def figure(times, name="scaling_steptime.png"):
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    for arm, label in ARMS.items():
        xs = [m for m in FLEETS if (arm, m) in times]
        seeds = [list(times[(arm, m)].values()) for m in xs]
        mean = [sum(v) / len(v) for v in seeds]
        spread = [[a - min(v) for a, v in zip(mean, seeds)], [max(v) - a for a, v in zip(mean, seeds)]]
        ax.errorbar(xs, mean, yerr=spread, color=COLOUR[arm], marker=MARKER[arm], capsize=2.5,
                    lw=1.6, ms=5, ls="--" if arm == "token_passing" else "-", label=label)
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_xticks(FLEETS, [str(m) for m in FLEETS])
    ax.set_xlabel("agents")
    ax.set_ylabel("seconds per decision step")
    ax.set_ylim(1.5e-4, 1.0)
    style(ax)
    ax.legend(fontsize=8, frameon=False, loc="upper left", bbox_to_anchor=(1.0, 1.0))
    fig.tight_layout()
    return save(fig, name)


if __name__ == "__main__":
    times = {**learned(), **token_passing()}
    for (arm, m), t in sorted(times.items()):
        v = list(t.values())
        print(f"{m:3d} {arm:20s} {1000 * sum(v) / len(v):7.2f} ms  [{1000 * min(v):.2f}, {1000 * max(v):.2f}]  n={len(v)}")
    print(figure(times))
