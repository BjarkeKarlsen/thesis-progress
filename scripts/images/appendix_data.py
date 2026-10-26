"""
Shared reading and drawing helpers for the appendix result figures (appendix_*.py).

Every appendix figure is measured, not schematic. It reads the rows the runs of
slap-mapd-coupling write and draws them. While a run has not been done, its
figure is drawn as a placeholder with the axes it will have and the path it waits
for, so the appendices build. Where every value goes, and which run fills it, is
in thesis-progress/decisions/active/appendix_values_overview.md.

The row fields are those of notes/measures_catalogue.md. A row is one seed of
one run, the same in every *.jsonl that slap-mapd-coupling's evaluation writes.
"""
import glob
import json
import os
import statistics

from scipy.stats import t as student_t

from base import OUT, C, plt

RESULTS = "thesis-progress/results"
FLEETS = (8, 16, 32, 64)
FLEET_STYLE = {8: (C["accent"], "o"), 16: (C["del_e"], "s"), 32: (C["ep_e"], "^"),
               64: (C["comm"], "D")}
ARMS = {"token_passing": "Token Passing", "centralised": "centralised",
        "section": "section-based", "decentralised": "decentralised"}
ARM_COLOUR = {"token_passing": C["node"], "centralised": C["accent"],
              "section": C["ep_e"], "decentralised": C["del_e"]}
RULES = {"fixed": "fixed", "demand": "demand", "congestion": "congestion-aware"}


# ---------------------------------------------------------------- reading
def read_jsonl(path):
    """The rows of one JSON Lines file, or [] if the run has not been done."""
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def read_glob(pattern):
    rows = []
    for path in sorted(glob.glob(pattern)):
        rows += read_jsonl(path)
    return rows


def read_json(path):
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def mean_and_half_width(values):
    """Mean over seeds and the half width of its 95 % t interval."""
    values = [v for v in values if v is not None]
    if not values:
        return float("nan"), 0.0
    if len(values) < 2:
        return values[0], 0.0
    n = len(values)
    return statistics.fmean(values), student_t.ppf(0.975, n - 1) * statistics.stdev(values) / n ** 0.5


def paired_gain(rule_rows, fixed_rows, field="mean_service_time"):
    """The gain of a rule over fixed storage as a share of fixed, paired by seed
    (eq:relgain). Above 0 means the rule is faster."""
    fixed = {r["seed"]: r for r in fixed_rows}
    shares = []
    for r in rule_rows:
        base = fixed.get(r["seed"])
        if base and base.get(field) and r.get(field) is not None:
            shares.append((base[field] - r[field]) / base[field])
    return mean_and_half_width(shares)


def paired_ratio(rule_rows, fixed_rows, field="mean_putaway_service_time"):
    """A rule's value over that of fixed storage, paired by seed. Above 1 costs more."""
    fixed = {r["seed"]: r for r in fixed_rows}
    ratios = []
    for r in rule_rows:
        base = fixed.get(r["seed"])
        if base and base.get(field) and r.get(field):
            ratios.append(r[field] / base[field])
    return mean_and_half_width(ratios)


def share(rows, field):
    """The share of seeds on which a boolean field holds."""
    return sum(bool(r.get(field)) for r in rows) / len(rows) if rows else float("nan")


def sweep_points(rows, parameter, rule, fixed_default=None):
    """Per swept value of a parameter sweep (rows with "varied" and "value"), the
    paired gain of the rule over fixed, its put-away cost against fixed, the keep-up
    shares of picks and put-aways, and the mean of any other row field on request.

    fixed_default names the value whose fixed rows stand in when fixed storage does
    not read the parameter (the congestion weight), as in plot_parameter_sweep.py."""
    by_value = {}
    for r in rows:
        if r.get("varied") == parameter and r["storage_mode"] == rule:
            by_value.setdefault(r["value"], []).append(r)
    points = []
    for x in sorted(by_value):
        if fixed_default is None:
            fixed = [r for r in rows if r.get("varied") == parameter
                     and r["storage_mode"] == "fixed" and r["value"] == x]
        else:
            name, value = fixed_default
            fixed = [r for r in rows if r.get("varied") == name
                     and r["storage_mode"] == "fixed" and r["value"] == value]
        here = by_value[x]
        points.append(dict(
            x=x, rows=here,
            gain=paired_gain(here, fixed),
            cost=paired_ratio(here, fixed),
            picks=share(here, "keeps_up_picks"),
            putaways=share(here, "keeps_up_putaways"),
        ))
    return points


# ---------------------------------------------------------------- drawing
def style(ax):
    ax.grid(axis="y", color=C["edge"], alpha=0.3, lw=0.6)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)


def panel_title(ax, text):
    ax.set_title(text, loc="left", fontsize=11, color=C["text"])


def placeholder(ax, waiting_for):
    """Marks an empty panel with the run it waits for."""
    ax.text(0.5, 0.5, f"placeholder\nwaits for {waiting_for}", transform=ax.transAxes,
            ha="center", va="center", fontsize=8, color=C["node"], style="italic",
            bbox=dict(boxstyle="round", fc="white", ec=C["edge"], lw=0.8))


def fleet_legend(fig, fleets=FLEETS, y=1.02):
    handles = [plt.Line2D([], [], color=FLEET_STYLE[m][0], marker=FLEET_STYLE[m][1], lw=2,
                          ms=6, label=f"{m} agents") for m in fleets]
    fig.legend(handles=handles, loc="upper center", ncol=len(handles), frameon=False,
               bbox_to_anchor=(0.5, y), fontsize=10)


def errorline(ax, points, key, colour, marker):
    xs = [p["x"] for p in points]
    ax.errorbar(xs, [p[key][0] for p in points], yerr=[p[key][1] for p in points],
                color=colour, marker=marker, ms=5, lw=2, capsize=3, elinewidth=1)


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path)
    plt.close(fig)
    return path


def sweep_figure(name, columns, results_dir, extra=None):
    """Storage or demand parameters swept with Token Passing, one column each, read top to
    bottom as the catalogue reads a run: (a) result, the pick service gain over fixed,
    (b) cost, the put-away service time over fixed, (c) check, the share of seeds that keep
    up, picks solid and put-aways dashed. A column is (parameter, rule, x label, default,
    fixed_default). extra = (row field, y label) adds a panel of that field's mean, for
    example the crowding under the congestion weight."""
    n = 4 if extra else 3
    k = len(columns)
    fig, axes = plt.subplots(n, k, figsize=(4.2 * k + 1.0, 1.7 * n + 1.2), sharex="col",
                             sharey="row", squeeze=False, gridspec_kw=dict(hspace=0.35))
    labels = ["gain over fixed\n(share of fixed)", "put-away time\nover fixed",
              "seeds that\nkeep up"] + ([extra[1]] if extra else [])
    for j, (parameter, rule, xlabel, default, fixed_default) in enumerate(columns):
        col = [axes[i][j] for i in range(n)]
        found = False
        for fleet in FLEETS:
            folders = [parameter] + ([fixed_default[0]] if fixed_default else [])
            rows = [r for folder in folders for r in read_jsonl(
                os.path.join(results_dir, f"fleet_{fleet}", folder, "load_sweep.jsonl"))]
            points = sweep_points(rows, parameter, rule, fixed_default)
            if not points:
                continue
            found = True
            colour, marker = FLEET_STYLE[fleet]
            errorline(col[0], points, "gain", colour, marker)
            errorline(col[1], points, "cost", colour, marker)
            xs = [p["x"] for p in points]
            col[2].plot(xs, [p["picks"] for p in points], color=colour, marker=marker, ms=5,
                        lw=2)
            col[2].plot(xs, [p["putaways"] for p in points], color=colour, ls="--", lw=1.2)
            if extra:
                values = [mean_and_half_width([r.get(extra[0]) for r in p["rows"]])
                          for p in points]
                col[3].errorbar(xs, [v[0] for v in values], yerr=[v[1] for v in values],
                                color=colour, marker=marker, ms=5, lw=2, capsize=3,
                                elinewidth=1)
        for i, ax in enumerate(col):
            if j == 0:
                ax.set_ylabel(labels[i])
            panel_title(ax, f"({'abcdefghijkl'[i * k + j]})")
            ax.axvline(default, color=C["node"], ls=":", lw=1)
            style(ax)
        col[0].axhline(0, color=C["text"], lw=0.8)
        col[1].axhline(1, color=C["text"], lw=0.8)
        col[2].set_ylim(-0.05, 1.05)
        col[-1].set_xlabel(xlabel)
        if not found:
            placeholder(col[0], os.path.join(results_dir, "fleet_<m>", parameter))
    fleet_legend(fig)
    return save(fig, name)
