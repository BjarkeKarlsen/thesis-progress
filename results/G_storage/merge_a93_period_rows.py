"""Merge the new congestion rows of tp-a93 into results/G_storage/fleet_<m>/storage_rule.epoch_length,
keep the old fixed and demand rows, and write summary.md and capacity.json with load_sweep's own
functions. Plays no episode."""
import json, sys
from pathlib import Path
import load_sweep as ls
load_spec, override_spec = ls.load_spec, ls.override_spec
m, old_dir, new_dir, out_dir, config = int(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4]), Path(sys.argv[5])
out_dir.mkdir(parents=True, exist_ok=True)
for name in ("load_sweep.jsonl", "timing.jsonl"):
    old = [json.loads(l) for l in open(old_dir / name)]
    new = [json.loads(l) for l in open(new_dir / name)]
    assert all(r["storage_mode"] == "congestion" for r in new)
    kept = [r for r in old if r["storage_mode"] != "congestion"]
    with open(out_dir / name, "w") as f:
        for r in kept + new:
            f.write(json.dumps(r) + "\n")
    print(name, "old kept", len(kept), "new", len(new))
rows = [json.loads(l) for l in open(out_dir / "load_sweep.jsonl")]
spec = override_spec(load_spec(config), horizon=10000, warmup=5000)
f_up = spec.experiment.keep_up_threshold
study = ls.build_study(spec, prepare=False)
by_value = {}
for row in rows:
    by_value.setdefault(row.get("value"), []).append(row)
sections, found = [], {}
for value, runs in sorted(by_value.items()):
    caps = {mode: ls.capacity(of, f_up) for mode, of in ls._by_mode(runs).items()}
    found[value] = caps
    sections.append(ls._tables(spec, runs, caps, f"{rows[0]['varied']} = {value:g}"))
(out_dir / "summary.md").write_text(ls._trips(spec, study.instance.graph) + "".join(sections), encoding="utf-8")
report = {"num_agents": spec.experiment.num_agents, "f_up": f_up, "varied": rows[0]["varied"],
          "by_value": {f"{v:g}": c for v, c in found.items()}}
(out_dir / "capacity.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print("summary and capacity written")
