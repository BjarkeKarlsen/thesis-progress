"""
The Token Passing load sweep of each fleet, for the Load and demand appendix.

Run:  python thesis-progress/scripts/images/load_sweep.py   (from the workspace root)
Out:  thesis-progress/scripts/Images/load_fleet<m>.png, one per fleet

Reads thesis-progress/results/E_load/fleet_<m>/, the rows and capacity.json that
slap-mapd-coupling's scripts/sweep/load_sweep.py writes. Measured, not schematic.
(a) the tasks waiting for a robot at the end of the run, mean over seeds with the range
over seeds, (b) the share of seeds that keep up. Dashed is the capacity, solid the main load.
"""
import json
import os
import statistics

from base import OUT, C, plt

RESULTS = "thesis-progress/results/E_load"
FLEETS = (8, 16, 32, 64)


def _rows(fleet):
    path = os.path.join(RESULTS, f"fleet_{fleet}", "load_sweep.jsonl")
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def _capacity(fleet):
    path = os.path.join(RESULTS, f"fleet_{fleet}", "capacity.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)["by_mode"]["fixed"]


def load_fleet(fleet):
    by_rate = {}
    for row in _rows(fleet):
        if row["storage_mode"] == "fixed":
            by_rate.setdefault(row["arrival_rate"], []).append(row)
    rates = sorted(by_rate)
    waiting = [[r["num_waiting_tasks"] for r in by_rate[x]] for x in rates]
    mean = [statistics.fmean(w) for w in waiting]
    kept = [100 * statistics.fmean(bool(r["keeps_up"]) for r in by_rate[x]) for x in rates]
    found = _capacity(fleet)

    fig, (top, bottom) = plt.subplots(2, 1, figsize=(5.2, 4.6), sharex=True,
                                      gridspec_kw=dict(height_ratios=(3, 2), hspace=0.3))
    top.fill_between(rates, [min(w) for w in waiting], [max(w) for w in waiting],
                     color=C["store_f"], lw=0)
    top.plot(rates, mean, color=C["accent"], lw=2, marker="o", ms=5)
    top.set_ylabel("tasks waiting\nat the end")
    top.set_ylim(bottom=0)
    top.set_title("(a)", loc="left", fontsize=11, color=C["text"])

    bottom.plot(rates, kept, color=C["accent"], lw=2, marker="o", ms=5)
    bottom.set_ylabel("seeds that\nkeep up (%)")
    bottom.set_ylim(-5, 105)
    bottom.set_xlabel(r"arrival rate $\lambda_{\mathrm{task}}$ (tasks per step)")
    bottom.set_title("(b)", loc="left", fontsize=11, color=C["text"])

    for key, style, name in (("capacity", "--", "capacity"), ("main_load", "-", "main load")):
        x = found[key]
        if x is None:
            continue
        for ax in (top, bottom):
            ax.axvline(x, color=C["node"], ls=style, lw=1)
        top.annotate(f"{name} {x:g}", (x, 1), xycoords=("data", "axes fraction"),
                     xytext=(3, -3), textcoords="offset points", va="top", fontsize=9,
                     color=C["text"])

    for ax in (top, bottom):
        ax.grid(axis="y", color=C["edge"], alpha=0.3, lw=0.6)
        ax.spines[["top", "right"]].set_visible(False)
    fig.savefig(os.path.join(OUT, f"load_fleet{fleet}.png"))
    plt.close(fig)


def load_sweep():
    for fleet in FLEETS:
        load_fleet(fleet)


if __name__ == "__main__":
    load_sweep()
