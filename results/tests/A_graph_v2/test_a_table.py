"""Test A tables: per rule means, and paired gains by seed, graph v2 against graph v1."""

import json
import math
import statistics as st
import sys
from pathlib import Path

T_19 = 2.093  # two-sided 95 % t quantile, 19 degrees of freedom (20 seeds)

FIELDS = [
    ("keeps_up", "keeps up"),
    ("keeps_up_picks", "picks keep up"),
    ("keeps_up_putaways", "put-aways keep up"),
    ("mean_service_time", "pick service time"),
    ("mean_wait_for_agent", "wait for a robot"),
    ("mean_travel_time", "travel"),
    ("mean_blocked_time", "blocked"),
    ("mean_stock_wait", "stock wait"),
    ("mean_pick_wait_pickup_taken", "shelf-taken wait (pick)"),
    ("mean_putaway_service_time", "put-away service time"),
    ("robot_busy_share", "robot busy share"),
    ("num_completed_putaways", "put-aways done"),
    ("mean_split_skus", "SKUs on more than one shelf"),
    ("peak_shelf_fill_share", "peak shelf fill"),
]


def load(path: Path, value: float | None = None) -> dict[str, dict[int, dict]]:
    by_mode: dict[str, dict[int, dict]] = {}
    for line in path.read_text().splitlines():
        row = json.loads(line)
        if value is not None and row.get("value") != value:
            continue
        by_mode.setdefault(row["storage_mode"], {})[row["seed"]] = row
    return by_mode


def mean(rows, key):
    values = [r[key] for r in rows if r.get(key) is not None]
    if not values:
        return "n/a"
    if isinstance(values[0], bool):
        return f"{sum(values)} / {len(rows)}"
    return f"{st.mean(values):.2f}"


def paired(a: dict[int, dict], b: dict[int, dict], key: str) -> str:
    """Mean of a - b over the seeds both have, its 95 % interval, and as a share of b's mean."""
    seeds = sorted(set(a) & set(b))
    diffs = [a[s][key] - b[s][key] for s in seeds if a[s][key] is not None and b[s][key] is not None]
    if len(diffs) < 2:
        return "n/a"
    m = st.mean(diffs)
    half = T_19 * st.stdev(diffs) / math.sqrt(len(diffs))
    base = st.mean(b[s][key] for s in seeds if b[s][key] is not None)
    return f"{m:+.2f} [{m - half:+.2f}, {m + half:+.2f}], {100 * m / base:+.1f} % of {base:.2f}"


def report(title: str, by_mode: dict[str, dict[int, dict]]) -> None:
    modes = [m for m in ("fixed", "demand", "random") if m in by_mode]
    print(f"### {title}\n")
    print("| measure | " + " | ".join(modes) + " |")
    print("|---|" + "---|" * len(modes))
    for key, name in FIELDS:
        print(f"| {name} | " + " | ".join(mean(list(by_mode[m].values()), key) for m in modes) + " |")
    print()
    print("Paired by seed, the second rule minus the first. Negative is shorter under the second.\n")
    print("| measure | demand - fixed | random - fixed | demand - random |")
    print("|---|---|---|---|")
    for key, name in FIELDS[3:11]:
        cells = []
        for a, b in (("demand", "fixed"), ("random", "fixed"), ("demand", "random")):
            cells.append(paired(by_mode[a], by_mode[b], key) if a in by_mode and b in by_mode else "")
        print(f"| {name} | " + " | ".join(cells) + " |")
    print()


if __name__ == "__main__":
    v2 = load(Path(sys.argv[1]))
    report("Graph v2, 8 agents, load 0.12", v2)
    if len(sys.argv) > 2:
        v1 = load(Path(sys.argv[2]), value=100.0)
        report("Graph v1, 8 agents, load 0.12, Delta = 100 (results/G_storage)", v1)
