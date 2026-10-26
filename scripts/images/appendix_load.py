"""
The figures of the Load and capacity appendix (E.Load.tex, app:load) and of the Demand drift
appendix (F.Demand.tex, app:demand), which demand_sweep() draws.

Run:  python thesis-progress/scripts/images/appendix_load.py   (from the workspace root)
Out:  thesis-progress/scripts/Images/app_load_sweep.png      fig:app:loadsweep
      thesis-progress/scripts/Images/app_load_validity.png   fig:app:loadvalidity
      thesis-progress/scripts/Images/app_demand_sweep.png    fig:app:demandsweep

Reads the Token Passing load sweep (results/E_load/fleet_<m>/, rows and
capacity.json from slap-mapd-coupling's scripts/sweep/load_sweep.py) and the demand columns
of the parameter sweep (results/F_demand/fleet_<m>/demand.*/, from
scripts/sweep/parameter_sweep.bash). A missing run is drawn as a placeholder.
load_sweep.py draws one fleet per figure for reading a sweep. These put the four fleets in
one figure, on the rate per agent, which is the grid of the sweep (app:load:method).
"""
import os
import statistics

from appendix_data import (RESULTS, FLEETS, FLEET_STYLE, C, plt, read_jsonl, read_json, share,
                           style, panel_title, placeholder, fleet_legend, save, sweep_figure)

LOAD = os.path.join(RESULTS, "E_load")
SWEEP = os.path.join(RESULTS, "F_demand")


def _fixed_by_rate(fleet):
    rows = read_jsonl(os.path.join(LOAD, f"fleet_{fleet}", "load_sweep.jsonl"))
    by_rate = {}
    for r in rows:
        if r["storage_mode"] == "fixed":
            by_rate.setdefault(r["arrival_rate"], []).append(r)
    return by_rate


def load_sweep_fleets():
    """(a) The backlog at the end of the run against the rate per agent, mean over seeds.
    (b) The share of seeds that keep up, picks solid and put-aways dashed ([A59]). A hollow
    marker is each fleet's capacity, a filled one its main load (0.6 of capacity)."""
    fig, (top, bottom) = plt.subplots(2, 1, figsize=(5.4, 4.8), sharex=True,
                                      gridspec_kw=dict(height_ratios=(3, 2), hspace=0.3))
    found = False
    for fleet in FLEETS:
        by_rate = _fixed_by_rate(fleet)
        if not by_rate:
            continue
        found = True
        colour, marker = FLEET_STYLE[fleet]
        rates = sorted(by_rate)
        x = [rate / fleet for rate in rates]
        backlog = [statistics.fmean(r["backlog"] for r in by_rate[rate]) for rate in rates]
        top.plot(x, backlog, color=colour, marker=marker, ms=4, lw=1.8)
        bottom.plot(x, [share(by_rate[rate], "keeps_up_picks") for rate in rates],
                    color=colour, marker=marker, ms=4, lw=1.8)
        bottom.plot(x, [share(by_rate[rate], "keeps_up_putaways") for rate in rates],
                    color=colour, ls="--", lw=1.2)
        found_at = (read_json(os.path.join(LOAD, f"fleet_{fleet}", "capacity.json")) or {})
        fixed = found_at.get("by_mode", {}).get("fixed", {})
        for key, face in (("capacity", "white"), ("main_load", colour)):
            rate = fixed.get(key)
            if rate is not None:
                bottom.plot(rate / fleet, 1.0, marker=marker, ms=8, mfc=face, mec=colour,
                            mew=1.5, ls="none", clip_on=False, zorder=5)
    top.set_ylabel("backlog at\nthe end")
    top.set_ylim(bottom=0)
    bottom.set_ylabel("seeds that\nkeep up")
    bottom.set_ylim(-0.05, 1.08)
    bottom.set_xlabel(r"arrival rate per agent $\lambda_{\mathrm{task}}/m$")
    for ax, label in ((top, "(a)"), (bottom, "(b)")):
        panel_title(ax, label)
        style(ax)
    if not found:
        placeholder(top, "results/E_load/fleet_<m>")
    fleet_legend(fig)
    return save(fig, "app_load_sweep.png")


def load_validity():
    """Units put off their home shelf (overflow_units, a) and units that fitted on no shelf
    (unplaced_units, b) against the rate per agent, fixed storage, mean over seeds. Both are
    0 at the main loads (measures_catalogue.md, Validity)."""
    fig, axes = plt.subplots(1, 2, figsize=(7.6, 2.8), sharex=True,
                             gridspec_kw=dict(wspace=0.35))
    found = False
    for fleet in FLEETS:
        by_rate = _fixed_by_rate(fleet)
        if not by_rate:
            continue
        found = True
        colour, marker = FLEET_STYLE[fleet]
        rates = sorted(by_rate)
        x = [rate / fleet for rate in rates]
        for ax, field in zip(axes, ("overflow_units", "unplaced_units")):
            ax.plot(x, [statistics.fmean(r[field] for r in by_rate[rate]) for rate in rates],
                    color=colour, marker=marker, ms=4, lw=1.8)
        main = ((read_json(os.path.join(LOAD, f"fleet_{fleet}", "capacity.json")) or {})
                .get("by_mode", {}).get("fixed", {}).get("main_load"))
        if main is not None:
            for ax in axes:
                ax.axvline(main / fleet, color=colour, ls=":", lw=1)
    axes[0].set_ylabel("units off their\nhome shelf")
    axes[1].set_ylabel("units placed\non no shelf")
    for ax, label in zip(axes, ("(a)", "(b)")):
        ax.set_xlabel(r"$\lambda_{\mathrm{task}}/m$")
        ax.set_ylim(bottom=0)
        panel_title(ax, label)
        style(ax)
    if not found:
        placeholder(axes[0], "results/E_load/fleet_<m>")
    fleet_legend(fig, y=1.08)
    return save(fig, "app_load_validity.png")


def demand_sweep():
    """The Zipf exponent, the drift period and the drift step, each swept with Token Passing
    under demand storage and paired with fixed storage at the same value."""
    columns = [
        ("demand.skew", "demand", r"Zipf exponent", 1.0, None),
        ("demand.rotation_period", "demand", "drift period (steps)", 200, None),
        ("demand.rotation_shift", "demand", "drift step (ranks)", 5, None),
    ]
    return sweep_figure("app_demand_sweep.png", columns, SWEEP)


def appendix_load():
    return [load_sweep_fleets(), load_validity(), demand_sweep()]


if __name__ == "__main__":
    for path in appendix_load():
        print(path)
