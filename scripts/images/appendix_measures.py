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
    ax.set_ylabel("gain over fixed\n(share of fixed)")
    style(ax)
    if not found:
        placeholder(ax, "results/H_horizon/fleet_<m>/load_sweep.jsonl")
    fleet_legend(fig, y=1.1)
    return save(fig, "app_horizon_gain.png")


def stand_still():
    """The stall length against what a healthy fleet reaches (app:cal:stall, [A118]). Per fleet,
    the longest stretch after the warm-up in which no agent finished a task, over the Token
    Passing runs at the main load (fixed and demand storage, 20 seeds each, the demand sweep at
    its thesis values, results/F_demand/fleet_<m>/demand.skew at skew 1), one box per fleet. The
    bar is the stall length, 36 order lines' worth of arrivals, 36 / arrival_rate steps."""
    fig, ax = plt.subplots(figsize=(5.2, 2.8))
    data, labels, stall = [], [], []
    for fleet in FLEETS:
        rows = read_jsonl(os.path.join(RESULTS, "F_demand", f"fleet_{fleet}", "demand.skew",
                                       "load_sweep.jsonl"))
        rows = [r for r in rows if r.get("value") == 1.0
                and r.get("longest_completion_gap") is not None]
        if not rows:
            continue
        data.append([r["longest_completion_gap"] for r in rows])
        labels.append(f"{fleet}")
        stall.append(round(36 / rows[0]["arrival_rate"]))
    if data:
        ax.boxplot(data, tick_labels=labels, widths=0.5,
                   medianprops=dict(color=C["accent"], lw=2))
        for i, value in enumerate(stall, start=1):
            ax.hlines(value, i - 0.35, i + 0.35, color=C["text"], lw=2, ls="--")
            ax.annotate(f"{value}", (i + 0.38, value), va="center", fontsize=8, color=C["text"])
        ax.set_yscale("log")
    else:
        placeholder(ax, "results/F_demand/fleet_<m>/demand.skew")
    ax.set_xlabel("agents $m$")
    ax.set_ylabel("longest stretch with\nno task finished (steps)")
    style(ax)
    return save(fig, "app_stand_still.png")


def appendix_measures():
    return [horizon_trace(), horizon_gain(), stand_still()]


if __name__ == "__main__":
    for path in appendix_measures():
        print(path)
