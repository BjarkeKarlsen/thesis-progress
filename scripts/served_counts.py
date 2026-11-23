"""The served share and throughput of a test row as [A96] counts them since its revision of
2026-11-17, worked out from the counts the row already holds, so older rows need no replay.

The revision changed two things (GAPS.md [A96], review_served_share_lines.pdf):
1. An order line released in the window that still waits for stock at T counts as one released
   pick. The row holds these lines as `num_waiting_orders`.
2. The throughput counts every task finished in the window, whenever released,
   `num_finished_in_window` per step of the window.

A row written by the revised code says so (`served_counts_version` 2) and is used as it is. A row
with the first [A96] counts (from the replays of 2026-11-16 and 2026-11-17) is updated here. A row
without them (the tests before [A96]) has nothing to update from and gives None.

    python3 served_counts.py ~/thesis_runs/evaluation/fleet_16       prints the table of a fleet
"""

import json
import statistics
import sys
from pathlib import Path

F_UP = 0.9  # [A111], was 0.8
SERVED = "evaluation_served_horizon10000_warmup5000"
SERVED_R1 = "evaluation_served_congestion_horizon10000_warmup5000"
ARMS = ("centralised", "section", "decentralised", "decentralised_comm")
RULES = ("fixed", "demand", "congestion")


def recount(row: dict) -> dict | None:
    """The revised throughput, served shares and keep-up of one row, or None when the row holds
    no served counts."""
    version = row.get("served_counts_version", 1 if "num_finished_in_window" in row else 0)
    if version == 0:
        return None
    keys = ("throughput", "served_share", "served_share_picks", "served_share_putaways")
    if version >= 2:
        out = {key: row[key] for key in keys}
    else:
        window = row["horizon"] - row["warmup"]
        released, finished = row["num_released_in_window"], row["num_finished_in_window"]
        put_released = row["num_released_putaways"]  # put-aways released in the window
        put_share = row["served_share_putaways"]
        put_finished = round(put_share * put_released) if put_share is not None else 0
        waiting = row["num_waiting_orders"]  # lines from the window still waiting for stock
        pick_released = released - put_released + waiting
        pick_finished = finished - put_finished
        out = {
            "throughput": finished / window,
            "served_share": finished / (released + waiting) if released + waiting else None,
            "served_share_picks": pick_finished / pick_released if pick_released else None,
            "served_share_putaways": put_share,
        }
    picks, puts = (
        share is None or share >= F_UP
        for share in (out["served_share_picks"], out["served_share_putaways"])
    )
    return {**out, "keeps_up_picks": picks, "keeps_up_putaways": puts, "keeps_up": picks and puts}


def rows(path: Path, mode: str | None = None) -> list[dict]:
    found = [json.loads(line) for line in path.open()]
    return [r for r in found if r.get("role", "chosen") == "chosen"
            and (mode is None or r["storage_mode"] == mode)]


def summary(found: list[dict]) -> str:
    counted = [c for c in map(recount, found) if c is not None]
    if not counted:
        return "no served counts"
    mean = lambda key: statistics.fmean(c[key] for c in counted if c[key] is not None)
    return (f"{len(counted):2d} seeds  tasks/step {mean('throughput'):.3f}  "
            f"served {mean('served_share'):.2f}  picks {mean('served_share_picks'):.2f}  "
            f"put-aways {mean('served_share_putaways'):.2f}  "
            f"picks keep up {sum(c['keeps_up_picks'] for c in counted):2d}  "
            f"put-aways keep up {sum(c['keeps_up_putaways'] for c in counted):2d}  "
            f"keep up {sum(c['keeps_up'] for c in counted):2d}")


def main(fleet: Path) -> None:
    for arm in ARMS:
        for rule in RULES:
            path = fleet / arm / rule / SERVED / "test.jsonl"
            print(f"{arm:18s} {rule:10s} " + (summary(rows(path, rule)) if path.exists() else "not home"))
        path = fleet / arm / "fixed" / SERVED_R1 / "test.jsonl"
        print(f"{arm:18s} {'R1 cong.':10s} " + (summary(rows(path, "congestion")) if path.exists() else "not home"))


if __name__ == "__main__":
    main(Path(sys.argv[1]).expanduser())
