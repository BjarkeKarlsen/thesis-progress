"""
The figures of the Evaluation horizon and stall length appendix (H.Horizon.tex, app:horizon).

Run:  python thesis-progress/scripts/images/appendix_measures.py   (from the workspace root)
Out:  thesis-progress/scripts/Images/app_horizon_trace.png   fig:app:horizontrace
      thesis-progress/scripts/Images/app_horizon_gain.png    fig:app:horizongain
      thesis-progress/scripts/Images/app_stand_still.png     fig:app:standstill

Reads
- results/H_horizon/fleet_<m>/trace_seed<k>.jsonl, episode traces of Token Passing under fixed
  storage at the main load (slap_mapd_coupling.evaluation.trace, one "step" line per
  timestep with t, completed and backlog). Not run yet.
- results/H_horizon/fleet_<m>/load_sweep.jsonl, test rows of Token Passing under fixed and demand
  storage at the main load, run at several horizons (the "horizon" field). Not run yet.
- results/E_load/fleet_<m>/, the load sweep, for longest_stand_still.
A missing run is drawn as a placeholder.
"""
import glob
import os
import statistics

from appendix_data import (RESULTS, FLEETS, FLEET_STYLE, C, plt, read_jsonl, read_json,
                           paired_gain, style, panel_title, placeholder, fleet_legend, save)

HORIZON = os.path.join(RESULTS, "H_horizon")
LOAD = os.path.join(RESULTS, "E_load")
DRIFT = 200   # drift period in steps, tab:evalparams
WINDOW = 100  # steps over which the throughput of the trace is taken


def _traces(fleet):
    """Per seed, the step lines of one trace."""
    out = []
    for path in sorted(glob.glob(os.path.join(HORIZON, f"fleet_{fleet}", "trace_seed*.jsonl"))):
        out.append([line for line in read_jsonl(path) if line.get("type") == "step"])
    return out


def horizon_trace():
    """Token Passing under fixed storage at the main load, mean over seeds, (a) the backlog
    and (b) the throughput over the last 100 steps, against time. Dotted lines are the
    demand drifts. The warm-up ends where the backlog settles (app:cal:horizon)."""
    fig, (top, bottom) = plt.subplots(2, 1, figsize=(6.0, 4.6), sharex=True,
                                      gridspec_kw=dict(hspace=0.3))
    found, end = False, 0
    for fleet in FLEETS:
        traces = _traces(fleet)
        if not traces:
            continue
        found = True
        colour, _ = FLEET_STYLE[fleet]
        n = min(len(s) for s in traces)
        end = max(end, n)
        t = [traces[0][i]["t"] for i in range(n)]
        top.plot(t, [statistics.fmean(s[i]["backlog"] for s in traces) for i in range(n)],
                 color=colour, lw=1.4)
        rate = [statistics.fmean((s[i]["completed"] - s[i - WINDOW]["completed"]) / WINDOW
                                 for s in traces) for i in range(WINDOW, n)]
        bottom.plot(t[WINDOW:], rate, color=colour, lw=1.4)
    for ax in (top, bottom):
        for x in range(DRIFT, end, DRIFT):
            ax.axvline(x, color=C["edge"], ls=":", lw=0.8)
        style(ax)
    top.set_ylabel("backlog $B_t$")
    bottom.set_ylabel("tasks finished\nper step")
    bottom.set_xlabel("timestep $t$")
    panel_title(top, "(a)")
    panel_title(bottom, "(b)")
    if not found:
        placeholder(top, "results/H_horizon/fleet_<m>/trace_seed<k>.jsonl")
    fleet_legend(fig)
    return save(fig, "app_horizon_trace.png")


def horizon_gain():
    """The gain of demand over fixed storage under Token Passing, paired by seed, against
    the number k of drift periods after the warm-up. The horizon is the warm-up plus the
    smallest k at which the estimate stops moving."""
    fig, ax = plt.subplots(figsize=(5.2, 2.8))
    found = False
    for fleet in FLEETS:
        rows = read_jsonl(os.path.join(HORIZON, f"fleet_{fleet}", "load_sweep.jsonl"))
        if not rows:
            continue
        found = True
        colour, marker = FLEET_STYLE[fleet]
        horizons = sorted({r["horizon"] for r in rows})
        warm = min(horizons) % DRIFT
        points = []
        for h in horizons:
            here = [r for r in rows if r["horizon"] == h]
            gain = paired_gain([r for r in here if r["storage_mode"] == "demand"],
                               [r for r in here if r["storage_mode"] == "fixed"])
            points.append(((h - warm) / DRIFT, gain))
        ax.errorbar([p[0] for p in points], [p[1][0] for p in points],
                    yerr=[p[1][1] for p in points], color=colour, marker=marker, ms=5, lw=2,
                    capsize=3, elinewidth=1)
    ax.set_xlabel("drift periods $k$ after the warm-up")
    ax.set_ylabel("gain of demand\nover fixed")
    style(ax)
    if not found:
        placeholder(ax, "results/H_horizon/fleet_<m>/load_sweep.jsonl")
    fleet_legend(fig, y=1.1)
    return save(fig, "app_horizon_gain.png")


def stand_still():
    """The longest time a robot holding a task stood still in a run, Token Passing under fixed
    storage at the rate nearest the main load, one box per fleet. The stall length is set
    above what a healthy run reaches (tab:evalparams, still TBD)."""
    fig, ax = plt.subplots(figsize=(5.2, 2.8))
    data, labels = [], []
    for fleet in FLEETS:
        rows = read_jsonl(os.path.join(LOAD, f"fleet_{fleet}", "load_sweep.jsonl"))
        main = ((read_json(os.path.join(LOAD, f"fleet_{fleet}", "capacity.json")) or {})
                .get("by_mode", {}).get("fixed", {}).get("main_load"))
        rows = [r for r in rows if r["storage_mode"] == "fixed"]
        if not rows or main is None:
            continue
        nearest = min({r["arrival_rate"] for r in rows}, key=lambda x: abs(x - main))
        data.append([r["longest_stand_still"] for r in rows if r["arrival_rate"] == nearest])
        labels.append(f"{fleet}")
    if data:
        ax.boxplot(data, tick_labels=labels, widths=0.5,
                   medianprops=dict(color=C["accent"], lw=2))
    else:
        placeholder(ax, "results/E_load/fleet_<m>")
    ax.set_xlabel("agents $m$")
    ax.set_ylabel("longest stand-still\n(steps)")
    style(ax)
    return save(fig, "app_stand_still.png")


def appendix_measures():
    return [horizon_trace(), horizon_gain(), stand_still()]


if __name__ == "__main__":
    for path in appendix_measures():
        print(path)
