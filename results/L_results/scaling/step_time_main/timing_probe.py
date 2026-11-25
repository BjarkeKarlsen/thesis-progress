"""The step time test (author 2026-11-23): one scaling_probe episode, with the decision time
also averaged over the measured window only (steps from --warmup on) and per 100 steps, so a
time that climbs with a growing queue shows. The probe's own mean covers every step, warm-up
included, which reads low because the warehouse starts empty. Same arguments as scaling_probe;
the row is appended to --output with the extra fields. From 2026-11-24 the row also holds the
GPU, RAM and CPU measures of resources.py (res_* fields, over the same window) and the machine.
Run from the worktree of the code it times (~/worktrees/main-bdfda94 from 2026-11-24)."""
import json, sys, tempfile
from pathlib import Path
import slap_mapd_coupling.environment.multi_agent_env as mae
from slap_mapd_coupling.training import scaling_probe
sys.path.insert(0, str(Path(__file__).resolve().parent))
import resources

LOGS = []
_init = mae.EpisodeLog.__init__
def _record(self, *a, **k):
    _init(self, *a, **k)
    LOGS.append(self)
mae.EpisodeLog.__init__ = _record

# Every routing time is tagged with the step it belongs to: the number of assignments made so
# far, since each step ends with one assignment. Arms record routing a varying number of times a
# step (the section arm once per busy section), so the count alone cannot align them.
_route = mae.EpisodeLog.record_routing_runtime
def _route_tagged(self, seconds):
    _route(self, seconds)
    self.__dict__.setdefault("routing_step", []).append(len(self.assignment_runtime_seconds) - 1)
mae.EpisodeLog.record_routing_runtime = _route_tagged

def main(argv):
    out = Path(argv[argv.index("--output") + 1])
    with tempfile.TemporaryDirectory() as tmp:
        argv = list(argv); argv[argv.index("--output") + 1] = str(Path(tmp) / "row.jsonl")
        steps_done = lambda: max((len(l.assignment_runtime_seconds) for l in LOGS), default=0)
        warm = int(argv[argv.index("--warmup") + 1])
        sampler = resources.Sampler(step=steps_done, mark=warm).start()
        scaling_probe.main(argv)
        sampler.stop()
        row = json.loads((Path(tmp) / "row.jsonl").read_text())
    log = max(LOGS, key=lambda l: len(l.routing_runtime_seconds))
    n = row["horizon"] - row["warmup"]
    steps = log.assignment_runtime_seconds
    per_step_all = list(steps)
    for seconds, i in zip(log.routing_runtime_seconds, log.routing_step):
        per_step_all[i] += seconds
    assert len(log.routing_step) == len(log.routing_runtime_seconds)
    assert abs(sum(per_step_all) / row["horizon"] - row["mean_decision_runtime_seconds"]) < 1e-9
    a = per_step = per_step_all[-n:]
    r = [i for i in log.routing_step if i >= len(steps) - n]
    row.update(
        timing_window_steps=n,
        timed_assignment_calls=len(log.assignment_runtime_seconds),
        timed_routing_calls=len(log.routing_runtime_seconds),
        window_decision_runtime_seconds=sum(per_step) / len(per_step),
        decision_runtime_per_100_steps=[sum(per_step[i:i + 100]) / len(per_step[i:i + 100])
                                        for i in range(0, len(per_step), 100)],
    )
    row.update(resources.summary(sampler.samples, from_step=row["warmup"]))
    row.update(resources.hardware())
    import torch
    row["res_torch_gpu_peak_mb"] = (torch.cuda.max_memory_allocated() / 2**20
                                    if torch.cuda.is_available() and torch.cuda.is_initialized() else None)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("a") as h:
        h.write(json.dumps(row) + "\n")
    b = row["decision_runtime_per_100_steps"]
    print(f"window {row['window_decision_runtime_seconds']:.4f} s (all steps "
          f"{row['mean_decision_runtime_seconds']:.4f}), first/last 100 {b[0]:.4f}/{b[-1]:.4f}, "
          f"calls {len(a)}/{len(r)} of {row['horizon']}, RAM peak {row['res_ram_peak_window_gb']:.2f} GB, "
          f"CPU {row['res_cpu_seconds_per_step']} s/step, {row['res_cpu_cores_used']} cores, "
          f"GPU {row['res_gpu_busy_mean_pct']} % busy, "
          f"own GPU {row['res_gpu_own_peak_mb']} MB, others {row['res_other_gpu_programs']}")

if __name__ == "__main__":
    main(sys.argv[1:])
