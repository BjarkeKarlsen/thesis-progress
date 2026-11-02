"""
The main result across the controllers (L.Results.tex, app:results), and the rows of its tables.

Run:  python thesis-progress/scripts/images/appendix_results.py   (from the workspace root)
Out:  thesis-progress/scripts/Images/app_results_gain.png        the gain per controller
      thesis-progress/results/L_results/fleet_<m>/tables.tex       the rows of tab:app:check,
                                                                   tab:app:result, tab:app:cost,
                                                                   tab:app:backlog, tab:app:stock

Reads, per fleet,
- the learned arms: results/L_results/fleet_<m>/<arm>/fixed_only/test.jsonl, the test rows of
  `slap-mapd evaluate --storage-modes fixed demand --horizon 10000 --warmup 5000`, copied there
  by thesis-progress/scripts/collect_run.py. Only the chosen checkpoint is read.
- Token Passing: the rows of the updated Token Passing run at the main load and the thesis
  values, fixed and demand storage from results/F_demand/fleet_<m>/demand.skew at skew 1, and
  congestion-aware storage from results/G_storage/fleet_<m>/storage_rule.congestion_weight at
  weight 1. Both played 10000 steps with a 5000-step warm-up, as the learned arms' test seeds do.

The gain of a rule is paired by seed with fixed storage under the same controller (eq:relgain).
Token Passing and the learned arms play different seeds (Token Passing 0 to 19, the learned
arms the test seeds of their split), so the controllers are compared by their gains, not seed
by seed. A missing run is drawn as a placeholder and left TBD in the tables.
"""
import os
import statistics

from appendix_data import (RESULTS, FLEETS, ARMS, ARM_COLOUR, RULES, C, plt, read_jsonl,
                           paired_gain, share, style, panel_title, placeholder, save)

LEARNED = ("centralised", "section", "decentralised")
CONTROLLERS = ("token_passing",) + LEARNED
REGIME = "fixed_only"
RULE_ORDER = ("fixed", "demand", "congestion")
RULE_MARK = {"demand": "o", "congestion": "s"}


def token_passing_rows(fleet):
    """Token Passing's rows per storage rule at the main load and the thesis values."""
    skew = read_jsonl(os.path.join(RESULTS, "F_demand", f"fleet_{fleet}", "demand.skew",
                                   "load_sweep.jsonl"))
    weight = read_jsonl(os.path.join(RESULTS, "G_storage", f"fleet_{fleet}",
                                     "storage_rule.congestion_weight", "load_sweep.jsonl"))
    rows = {mode: [r for r in skew if r.get("value") == 1.0 and r["storage_mode"] == mode]
            for mode in ("fixed", "demand")}
    rows["congestion"] = [r for r in weight if r.get("value") == 1.0
                          and r["storage_mode"] == "congestion"]
    return {mode: found for mode, found in rows.items() if found}


def learned_rows(fleet, arm):
    """A learned arm's test rows of its chosen checkpoint, per storage rule."""
    rows = read_jsonl(os.path.join(RESULTS, "L_results", f"fleet_{fleet}", arm, REGIME,
                                   "test.jsonl"))
    out = {}
    for r in rows:
        if r.get("role", "chosen") == "chosen":
            out.setdefault(r["storage_mode"], []).append(r)
    return out


def rows_of(fleet):
    """{controller: {rule: rows}} for every controller with a run on this fleet."""
    found = {"token_passing": token_passing_rows(fleet)}
    found.update({arm: learned_rows(fleet, arm) for arm in LEARNED})
    return {c: rules for c, rules in found.items() if rules}


def results_gain():
    """Per fleet with a run, (a) the gain of demand and congestion-aware storage over fixed
    storage, paired by seed, with its 95 % interval, and (b) the share of test seeds that keep
    up under each rule, per controller. Token Passing is the reference."""
    fleets = [f for f in FLEETS if rows_of(f)] or [8]
    fig, axes = plt.subplots(2, len(fleets), figsize=(3.6 * len(fleets) + 1.2, 4.8),
                             squeeze=False, sharey="row",
                             gridspec_kw=dict(height_ratios=(3, 2), hspace=0.35))
    for j, fleet in enumerate(fleets):
        top, bottom = axes[0][j], axes[1][j]
        data = rows_of(fleet)
        for i, controller in enumerate(CONTROLLERS):
            rules = data.get(controller, {})
            fixed = rules.get("fixed", [])
            for k, rule in enumerate(("demand", "congestion")):
                if rule in rules and fixed:
                    gain, half = paired_gain(rules[rule], fixed)
                    top.errorbar(i + (k - 0.5) * 0.25, gain, yerr=half, ls="none",
                                 marker=RULE_MARK[rule], ms=6, capsize=3,
                                 color=ARM_COLOUR[controller],
                                 mfc=ARM_COLOUR[controller] if rule == "demand" else "white")
            for k, rule in enumerate(RULE_ORDER):
                if rule in rules:
                    bottom.bar(i + (k - 1) * 0.25, share(rules[rule], "keeps_up"), width=0.22,
                               color=ARM_COLOUR[controller], alpha=(1.0, 0.65, 0.35)[k])
        top.axhline(0, color=C["text"], lw=0.8)
        top.set_title(f"{fleet} agents", fontsize=10)
        for ax, label in ((top, "(a)"), (bottom, "(b)")):
            ax.set_xticks(range(len(CONTROLLERS)))
            ax.set_xlim(-0.6, len(CONTROLLERS) - 0.4)
            ax.set_xticklabels([ARMS[c] for c in CONTROLLERS], rotation=20, fontsize=8)
            panel_title(ax, f"{label[:-1]}{'' if len(fleets) == 1 else j + 1})")
            style(ax)
        bottom.set_ylim(0, 1.05)
        top.tick_params(labelbottom=False)
        if len(data) <= 1:
            placeholder(top, "the learned arms")
    axes[0][0].set_ylabel("gain over fixed\n(share of fixed)")
    axes[1][0].set_ylabel("test seeds\nthat keep up")
    handles = [plt.Line2D([], [], ls="none", marker="o", color=C["text"], label=RULES["demand"]),
               plt.Line2D([], [], ls="none", marker="s", mfc="white", color=C["text"],
                          label=RULES["congestion"])]
    handles += [plt.Rectangle((0, 0), 1, 1, color=C["text"], alpha=a, label=f"{RULES[r]} (bars)")
                for r, a in zip(RULE_ORDER, (1.0, 0.65, 0.35))]
    fig.legend(handles=handles, loc="upper center", ncol=5, frameon=False,
               bbox_to_anchor=(0.5, 1.04), fontsize=9)
    return save(fig, "app_results_gain.png")


# ------------------------------------------------------------------ the table rows
def _mean(rows, field, digits=1):
    values = [r.get(field) for r in rows if r.get(field) is not None]
    return f"{statistics.fmean(values):.{digits}f}" if values else "n/a"


def _count(rows, test):
    return f"{sum(1 for r in rows if test(r))} of {len(rows)}"


# Per table, its label and the cells of one row, in the order of its columns in L.Results.tex.
TABLES = (
    ("tab:app:check", lambda rows, c: [
        _count(rows, lambda r: r.get("keeps_up_picks")),
        _count(rows, lambda r: r.get("keeps_up_putaways")),
        _mean(rows, "completed_share", 2), _mean(rows, "backlog_slope", 2),
        str(sum(1 for r in rows if r.get("stalled")))]),
    ("tab:app:result", lambda rows, c: [
        _mean(rows, "mean_service_time"), _mean(rows, "mean_wait_for_agent"),
        _mean(rows, "mean_travel_time"), _mean(rows, "mean_blocked_time"),
        _mean(rows, "mean_stock_wait", 2), _mean(rows, "mean_crowding", 2),
        _mean(rows, "robot_busy_share", 2),
        _mean(rows, "mean_pick_wait_pickup_taken") if c == "token_passing" else "n/a"]),
    ("tab:app:cost", lambda rows, c: [
        _mean(rows, "mean_putaway_service_time"),
        _mean(rows, "mean_decision_runtime_seconds", 4),
        _mean(rows, "mean_order_completion"), _mean(rows, "orders_per_timestep", 3),
        _mean(rows, "throughput", 3), _mean(rows, "throughput_per_agent", 4)]),
    ("tab:app:backlog", lambda rows, c: [
        _mean(rows, "num_waiting_tasks"), _mean(rows, "num_active_tasks"),
        _mean(rows, "num_waiting_orders"), _mean(rows, "num_lines_waited"),
        _mean(rows, "num_released_putaways"), _mean(rows, "num_completed_putaways")]),
    ("tab:app:stock", lambda rows, c: [
        _mean(rows, "mean_split_skus"), _mean(rows, "mean_tasks_per_line", 2),
        _mean(rows, "mean_cold_prime_share", 2), _mean(rows, "mean_unit_age_at_pick", 0),
        _mean(rows, "num_storage_updates", 0), _mean(rows, "mean_arrived_units")]),
)
WIDTH = {"tab:app:check": 5, "tab:app:result": 8, "tab:app:cost": 6, "tab:app:backlog": 6,
         "tab:app:stock": 6}


def table_rows():
    """For each fleet with a run, the body rows of the five tables of app:results, as LaTeX, in
    results/L_results/fleet_<m>/tables.tex, to paste over the TBD rows."""
    paths = []
    for fleet in FLEETS:
        data = rows_of(fleet)
        if not data:
            continue
        lines = [f"% fleet {fleet}, written by thesis-progress/scripts/images/appendix_results.py"]
        for label, cells in TABLES:
            lines.append(f"% {label}")
            for rule in RULE_ORDER:
                for i, controller in enumerate(CONTROLLERS):
                    rows = data.get(controller, {}).get(rule)
                    values = cells(rows, controller) if rows else ["TBD"] * WIDTH[label]
                    first = rule.ljust(10) if i == 0 else " " * 10
                    lines.append(f"    {first} & {ARMS[controller]:<13} & "
                                 + " & ".join(values) + " \\\\")
        folder = os.path.join(RESULTS, "L_results", f"fleet_{fleet}")
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, "tables.tex")
        with open(path, "w") as out:
            out.write("\n".join(lines) + "\n")
        paths.append(path)
    return paths


def appendix_results():
    return [results_gain(), *table_rows()]


if __name__ == "__main__":
    for path in appendix_results():
        print(path)
