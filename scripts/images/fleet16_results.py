"""
Fleet 16 results of the four learned arms, each rule played with the policy trained under it
(Regime 2), next to Token Passing. A first look for the author, not yet in the thesis.

Run:  python thesis-progress/scripts/images/fleet16_results.py   (from the workspace root)
Out:  thesis-progress/scripts/Images/fleet16_served.png         share of arriving work served
      thesis-progress/scripts/Images/fleet16_val_vs_test.png    short validation against long test
      thesis-progress/scripts/Images/fleet16_runtime.png        decision time per arm
      thesis-progress/results/L_results/earlier_runs/fleet_16/overview.md    the same numbers as tables

Reads the rows `slap-mapd evaluate` wrote. They are copied first from
~/thesis_runs/evaluation/fleet_16/<arm>/<rule>/ into results/L_results/earlier_runs/fleet_16/rows/ (small
files), so the figure can be redrawn from the repo alone.
- test: 20 test seeds, 10000 steps with a 5000-step warm-up, chosen checkpoint ([A60]).
- validation: 5 validation seeds, 2000 steps, the chosen checkpoint's rows.
- runtime: 3 test seeds on the GPU of the PC (RTX 2070 SUPER), alone on the machine.
Token Passing: results/F_demand (fixed, demand at skew 1) and results/G_storage (congestion
at weight 1), seeds 0 to 19, same episode length. Its decision time is on the CPU.
"""
import json
import os
import shutil
import statistics

from appendix_data import (RESULTS, C, plt, read_jsonl, mean_and_half_width, style,
                           panel_title, save)

FLEET = 16
SOURCE = os.path.expanduser(f"~/thesis_runs/evaluation/fleet_{FLEET}")
ROWS = os.path.join(RESULTS, "L_results", "earlier_runs", f"fleet_{FLEET}", "rows")
EVAL = "evaluation_horizon10000_warmup5000"
ARMS = {"centralised": "centralised", "section": "section-based",
        "decentralised": "decentralised", "decentralised_comm": "decentralised\nwith messages"}
ARM_COLOUR = {"token_passing": C["node"], "centralised": C["accent"], "section": C["ep_e"],
              "decentralised": C["del_e"], "decentralised_comm": C["comm"]}
RULES = {"fixed": "fixed", "demand": "demand", "congestion": "congestion-aware"}
RULE_HATCH = {"fixed": "", "demand": "//", "congestion": ".."}


def copy_rows():
    """Copies the small row files of every run into the repo, when the run folder is here."""
    if not os.path.isdir(SOURCE):
        return
    for arm in ARMS:
        for rule in RULES:
            for sub, files in ((EVAL, ("test.jsonl", "validation.jsonl", "evaluation.json")),
                               ("evaluation_served_horizon10000_warmup5000", ("test.jsonl",)),
                               ("runtime_gpu", ("test.jsonl",))):
                for name in files:
                    src = os.path.join(SOURCE, arm, rule, sub, name)
                    if os.path.exists(src):
                        dst = os.path.join(ROWS, arm, rule, sub, name)
                        os.makedirs(os.path.dirname(dst), exist_ok=True)
                        shutil.copy2(src, dst)


def rows(arm, rule, sub, name, role="chosen"):
    found = read_jsonl(os.path.join(ROWS, arm, rule, sub, name))
    return [r for r in found if r.get("role", role) == role and r["storage_mode"] == rule]


def chosen_validation(arm, rule):
    """The validation rows of the chosen checkpoint."""
    path = os.path.join(ROWS, arm, rule, EVAL, "evaluation.json")
    with open(path) as f:
        record = json.load(f)
    chosen = (record.get("chosen") or record["policy"]["chosen"])["checkpoint"]
    return [r for r in read_jsonl(os.path.join(ROWS, arm, rule, EVAL, "validation.jsonl"))
            if r["checkpoint"] == chosen], chosen


def token_passing():
    skew = read_jsonl(os.path.join(RESULTS, "F_demand", f"fleet_{FLEET}", "demand.skew",
                                   "load_sweep.jsonl"))
    weight = read_jsonl(os.path.join(RESULTS, "G_storage", f"fleet_{FLEET}",
                                     "storage_rule.congestion_weight", "load_sweep.jsonl"))
    out = {m: [r for r in skew if r.get("value") == 1.0 and r["storage_mode"] == m]
           for m in ("fixed", "demand")}
    out["congestion"] = [r for r in weight if r.get("value") == 1.0
                         and r["storage_mode"] == "congestion"]
    return out


SERVED = "evaluation_served_horizon10000_warmup5000"
F_UP = 0.8


def served_shares(arm, rule, tp):
    """The share of the arriving work served in the measured steps, per test seed, and whether it
    is exact. Exact from the replay with the served counts ([A96] proposal) once it is home.
    Until then estimated from the backlog slope: the backlog grows by what arrives less what is
    finished, so the share is about 1 - slope / (100 x release rate). The release rate is
    Token Passing's throughput under the same rule, since Token Passing keeps up and the arms
    play the same arrival process. The backlog also counts order lines waiting for stock, so the
    estimate is rough."""
    exact = [r["served_share"] for r in rows(arm, rule, SERVED, "test.jsonl")
             if r.get("served_share") is not None]
    if exact:
        return exact, True
    rate = statistics.fmean(r["throughput"] for r in tp[rule])
    return [max(1 - r["backlog_slope"] / (100 * rate), 0.0)
            for r in rows(arm, rule, EVAL, "test.jsonl")], False


def served_figure(tp):
    fig, ax = plt.subplots(figsize=(7.5, 3.6))
    width = 0.26
    estimated = False
    for i, arm in enumerate(ARMS):
        for j, rule in enumerate(RULES):
            shares, exact = served_shares(arm, rule, tp)
            estimated |= not exact
            m, h = mean_and_half_width(shares)
            ax.bar(i + (j - 1) * width, m, width, yerr=h, color=ARM_COLOUR[arm],
                   hatch=RULE_HATCH[rule], edgecolor="white", capsize=2, ecolor=C["text"])
    ax.axhline(1.0, color=ARM_COLOUR["token_passing"], ls="--", lw=1.2)
    ax.text(len(ARMS) - 0.5, 0.98, "all arriving work served (Token Passing)", ha="right",
            va="top", fontsize=9, color=C["text"])
    ax.axhline(F_UP, color=C["edge"], ls=":", lw=1.2)
    ax.text(len(ARMS) - 0.5, F_UP, "keep-up threshold", ha="right", va="bottom", fontsize=9,
            color=C["text"])
    ax.set_ylim(0, 1.22)
    ax.set_xticks(range(len(ARMS)), list(ARMS.values()), fontsize=10)
    ax.set_ylabel("share of arriving work served" + ("\n(estimate)" if estimated else ""))
    handles = [plt.Rectangle((0, 0), 1, 1, fc="white", ec=C["text"], hatch=RULE_HATCH[r])
               for r in RULES]
    ax.legend(handles, list(RULES.values()), frameon=False, fontsize=9, loc="upper left",
              ncol=3)
    style(ax)
    return save(fig, "fleet16_served.png")


def val_vs_test_figure():
    fig, ax = plt.subplots(figsize=(4.6, 4.2))
    top = 0.0
    for arm in ARMS:
        for rule in RULES:
            val, _ = chosen_validation(arm, rule)
            v = statistics.fmean(r["throughput"] for r in val)
            t = statistics.fmean(r["throughput"] for r in rows(arm, rule, EVAL, "test.jsonl"))
            top = max(top, v, t)
            ax.scatter(v, t, color=ARM_COLOUR[arm], marker={"fixed": "o", "demand": "s",
                       "congestion": "^"}[rule], s=40, zorder=3)
    top *= 1.1
    ax.plot([0, top], [0, top], color=C["edge"], lw=1, ls=":")
    ax.set_xlim(0, top)
    ax.set_ylim(0, top)
    ax.set_xlabel("validation, 2000 steps")
    ax.set_ylabel("test, 10000 steps")
    arm_handles = [plt.Line2D([], [], color=ARM_COLOUR[a], marker="o", ls="", label=ARMS[a].replace("\n", " "))
                   for a in ARMS]
    rule_handles = [plt.Line2D([], [], color=C["text"], marker=mk, ls="", label=RULES[r])
                    for r, mk in (("fixed", "o"), ("demand", "s"), ("congestion", "^"))]
    ax.legend(handles=arm_handles + rule_handles, frameon=False, fontsize=8, loc="upper left")
    style(ax)
    return save(fig, "fleet16_val_vs_test.png")


def runtime_figure(tp):
    fig, ax = plt.subplots(figsize=(7.4, 3.2))
    names, values, colours = [], [], []
    for arm in ARMS:
        found = [r["mean_decision_runtime_seconds"] for rule in RULES
                 for r in rows(arm, rule, "runtime_gpu", "test.jsonl")]
        names.append(ARMS[arm])
        values.append(statistics.fmean(found))
        colours.append(ARM_COLOUR[arm])
    tp_rt = statistics.fmean(r["mean_decision_runtime_seconds"] for found in tp.values() for r in found)
    names.append("Token Passing\n(CPU)")
    values.append(tp_rt)
    colours.append(ARM_COLOUR["token_passing"])
    ax.bar(range(len(names)), values, color=colours)
    for i, v in enumerate(values):
        ax.text(i, v, f"{v * 1000:.0f} ms" if v >= 0.01 else f"{v * 1000:.1f} ms",
                ha="center", va="bottom", fontsize=9, color=C["text"])
    ax.set_xticks(range(len(names)), names, fontsize=9)
    ax.set_ylabel("seconds per decision")
    style(ax)
    return save(fig, "fleet16_runtime.png")


def overview(tp):
    lines = [f"# Fleet {FLEET}, the four learned arms and Token Passing", "",
             "Written by `thesis-progress/scripts/images/fleet16_results.py`. Each rule is played "
             "with the policy trained under it (Regime 2). Test: 20 seeds, 10000 steps, 5000 "
             "warm-up, chosen checkpoint. Validation: 5 seeds, 2000 steps. Mean [95 % interval].",
             "", "| arm | rule | chosen | validation throughput | test throughput | seeds keeping up "
             "| pick service, steps | decision time, ms (GPU) |", "|---|---|---|---|---|---|---|---|"]
    for arm in ARMS:
        for rule in RULES:
            val, chosen = chosen_validation(arm, rule)
            test = rows(arm, rule, EVAL, "test.jsonl")
            vm, vh = mean_and_half_width([r["throughput"] for r in val])
            tm, th = mean_and_half_width([r["throughput"] for r in test])
            svc = [r["mean_service_time"] for r in test if r["mean_service_time"] is not None]
            rt = [r["mean_decision_runtime_seconds"] for r in rows(arm, rule, "runtime_gpu", "test.jsonl")]
            lines.append(
                f"| {ARMS[arm].replace(chr(10), ' ')} | {RULES[rule]} | {chosen[-2:]} "
                f"| {vm:.3f} [{vm - vh:.3f}, {vm + vh:.3f}] | {tm:.3f} [{tm - th:.3f}, {tm + th:.3f}] "
                f"| {sum(r['keeps_up'] for r in test)} of {len(test)} "
                f"| {statistics.fmean(svc):.0f} ({len(svc)} seeds with a pick done) "
                f"| {statistics.fmean(rt) * 1000:.0f} |" if svc else
                f"| {ARMS[arm].replace(chr(10), ' ')} | {RULES[rule]} | {chosen[-2:]} "
                f"| {vm:.3f} [{vm - vh:.3f}, {vm + vh:.3f}] | {tm:.3f} [{tm - th:.3f}, {tm + th:.3f}] "
                f"| {sum(r['keeps_up'] for r in test)} of {len(test)} | no pick done "
                f"| {statistics.fmean(rt) * 1000:.0f} |")
    for rule, found in tp.items():
        tm, th = mean_and_half_width([r["throughput"] for r in found])
        svc = statistics.fmean(r["mean_service_time"] for r in found)
        rt = statistics.fmean(r["mean_decision_runtime_seconds"] for r in found)
        lines.append(f"| Token Passing | {RULES[rule]} | n/a | n/a | {tm:.3f} [{tm - th:.3f}, "
                     f"{tm + th:.3f}] | {sum(r['keeps_up'] for r in found)} of {len(found)} "
                     f"| {svc:.0f} | {rt * 1000:.1f} (CPU) |")
    path = os.path.join(RESULTS, "L_results", "earlier_runs", f"fleet_{FLEET}", "overview.md")
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    return path


if __name__ == "__main__":
    copy_rows()
    tp = token_passing()
    for path in (served_figure(tp), val_vs_test_figure(), runtime_figure(tp), overview(tp)):
        print("wrote", path)
