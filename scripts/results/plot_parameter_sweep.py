"""
The Token Passing parameter sweep in one figure. A working plot, not a thesis figure.

Run:  python thesis-progress/scripts/results/plot_parameter_sweep.py [RESULTS_DIR]   (from the workspace root)
Out:  thesis-progress/results/plots/parameter_sweep.png

Reads <RESULTS_DIR>/F_demand/fleet_<m>/demand.*/ and <RESULTS_DIR>/G_storage/fleet_<m>/<setting>/
(the storage rule and margin settings, not shelf_capacity), the load_sweep.jsonl rows that
slap-mapd-coupling's scripts/sweep/load_sweep.py --vary writes (commands in results/README.md). Each column is one varied
parameter, each line one fleet, and the rows follow how a run is read (notes/measures_catalogue.md).
(1) The result, the pick service time gain of the rule over fixed storage, paired by seed, as a
share of fixed. (2) Its cost, the put-away service time of the rule over that of fixed storage,
paired by seed. (3) The check, the share of seeds on which the rule keeps up, picks and put-aways
separately ([A59]), solid, and the same for fixed storage, dashed. The rule is demand storage,
apart from the congestion_weight column, which runs the congestion rule and pairs it with fixed
storage at the default values. Points are the mean over seeds, bars the 95 % t interval, the
dotted line the value the other columns hold fixed.
"""
import glob
import json
import os
import statistics
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RESULTS = sys.argv[1] if len(sys.argv) > 1 else "thesis-progress/results"
OUT = os.path.join(RESULTS, "plots")
FLEETS = {8: ("#2a78d6", "o"), 16: ("#eb6834", "s"), 32: ("#1baf7a", "^"), 64: ("#e87ba4", "D")}
DEFAULTS = {"arrival.margin": 1.0, "storage_rule.epoch_length": 100,
            "storage_rule.congestion_weight": 1.0, "demand.skew": 1.0,
            "demand.rotation_period": 200, "demand.rotation_shift": 5}
INK, MUTED, GRID = "#2b2b2b", "#6b6b6b", "#e4e4e0"
T95 = 2.093  # t quantile for 19 degrees of freedom, 20 seeds

plt.rcParams.update({"font.size": 10, "axes.edgecolor": MUTED, "axes.labelcolor": INK,
                     "xtick.color": MUTED, "ytick.color": MUTED, "savefig.dpi": 150,
                     "savefig.bbox": "tight"})


def rows(fleet):
    out = []
    for setting in DEFAULTS:
        folder = "F_demand" if setting.startswith("demand.") else "G_storage"
        path = os.path.join(RESULTS, folder, f"fleet_{fleet}", setting, "load_sweep.jsonl")
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            out += [json.loads(line) for line in f if line.strip()]
    return out


def mean_and_half_width(values):
    if len(values) < 2:
        return (values[0] if values else float("nan")), 0.0
    return statistics.mean(values), T95 * statistics.stdev(values) / len(values) ** 0.5


def points(fleet_rows, parameter):
    """Per swept value, the paired gain over fixed, the paired put-away cost against fixed, and
    the shares of seeds on which the rule and fixed storage keep up."""
    rule = "congestion" if parameter == "storage_rule.congestion_weight" else "demand"
    # Fixed storage does not read the congestion weight, so its default rows stand in.
    fixed_parameter = "storage_rule.epoch_length" if rule == "congestion" else parameter
    fixed = {}
    for r in fleet_rows:
        if r["varied"] == fixed_parameter and r["storage_mode"] == "fixed":
            value = DEFAULTS[fixed_parameter] if rule == "congestion" else r["value"]
            if r["value"] == value:
                fixed[(value if rule == "demand" else None, r["seed"])] = r
    by_value = {}
    for r in fleet_rows:
        if r["varied"] == parameter and r["storage_mode"] == rule:
            by_value.setdefault(r["value"], []).append(r)
    xs, gain, cost, keep, keep_fixed = sorted(by_value), [], [], [], []
    for x in xs:
        shares, ratios, bases = [], [], []
        for r in by_value[x]:
            base = fixed[(x if rule == "demand" else None, r["seed"])]
            bases.append(base)
            shares.append((base["mean_service_time"] - r["mean_service_time"]) / base["mean_service_time"])
            if r["mean_putaway_service_time"] and base["mean_putaway_service_time"]:
                ratios.append(r["mean_putaway_service_time"] / base["mean_putaway_service_time"])
        gain.append(mean_and_half_width(shares))
        cost.append(mean_and_half_width(ratios) if ratios else (float("nan"), 0.0))
        keep.append(sum(bool(r["keeps_up"]) for r in by_value[x]) / len(by_value[x]))
        keep_fixed.append(sum(bool(b["keeps_up"]) for b in bases) / len(bases))
    return xs, gain, cost, keep, keep_fixed


def style(ax):
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)


def plot():
    fleet_rows = {fleet: rows(fleet) for fleet in FLEETS}
    fig, axes = plt.subplots(3, len(DEFAULTS), figsize=(20, 9), sharey="row",
                             gridspec_kw={"height_ratios": (2, 1.5, 1)})
    for j, parameter in enumerate(DEFAULTS):
        top, middle, bottom = axes[0][j], axes[1][j], axes[2][j]
        for fleet, (colour, marker) in FLEETS.items():
            if not fleet_rows[fleet]:
                continue
            xs, gain, cost, keep, keep_fixed = points(fleet_rows[fleet], parameter)
            top.errorbar(xs, [g[0] for g in gain], yerr=[g[1] for g in gain], color=colour,
                         marker=marker, ms=6, lw=2, capsize=3, elinewidth=1)
            middle.errorbar(xs, [c[0] for c in cost], yerr=[c[1] for c in cost], color=colour,
                            marker=marker, ms=6, lw=2, capsize=3, elinewidth=1)
            bottom.plot(xs, keep, color=colour, marker=marker, ms=6, lw=2)
            bottom.plot(xs, keep_fixed, color=colour, ls="--", lw=1.2)
        for ax in (top, middle, bottom):
            ax.axvline(DEFAULTS[parameter], color=MUTED, ls=":", lw=1)
            style(ax)
        top.axhline(0, color=INK, lw=0.8)
        middle.axhline(1, color=INK, lw=0.8)
        rule = "congestion" if parameter == "storage_rule.congestion_weight" else "demand"
        top.set_title(f"{parameter}\n({rule} rule)", color=INK)
        bottom.set_ylim(-0.05, 1.05)
        bottom.set_xlabel("value")
    axes[0][0].set_ylabel("pick service gain over fixed\n(share of fixed, above 0 is better)")
    axes[1][0].set_ylabel("put-away service time\nover fixed (above 1 costs)")
    axes[2][0].set_ylabel("share of seeds keeping up\n(dashed: fixed)")
    handles = [plt.Line2D([], [], color=c, marker=m, lw=2, ms=6, label=f"{fleet} agents")
               for fleet, (c, m) in FLEETS.items()]
    fig.legend(handles=handles, loc="upper center", ncol=len(handles), frameon=False,
               bbox_to_anchor=(0.5, 1.0))
    seeds = len({r["seed"] for rows_ in fleet_rows.values() for r in rows_})
    fig.suptitle(f"Token Passing parameter sweep, {seeds} seeds per point. Read top to bottom: "
                 "result, cost, check.", y=1.04, color=INK)
    path = os.path.join(OUT, "parameter_sweep.png")
    fig.savefig(path)
    plt.close(fig)
    return path


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print(plot())
