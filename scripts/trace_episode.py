"""Play one checkpoint of a trained run on one seed and write a per-step trace, to look for what
goes wrong in an episode.

Run from the workspace root, with the venv's python:

    ~/.venvs/rl/bin/python thesis-progress/scripts/trace_episode.py RUN_DIR [--checkpoint N]
        [--seed S] [--storage-mode fixed] [--horizon H] [--warmup W]

RUN_DIR is a run folder, ~/thesis_runs/training/fleet_<m>/<arm>/<regime>. The defaults are the
last checkpoint, the first test seed, the storage rule the run trained with, and the run's own
episode length. Checkpoint N is saved after iteration 3 (N + 1). Writes
RUN_DIR/traces/checkpoint_<N>_<mode>_seed<S>.jsonl and prints the trace summary (stalls, robots
that wander, the longest stretch the whole fleet stood still). Replay it with

    ~/.venvs/rl/bin/python -m slap_mapd_coupling.viz.pygame_renderer <trace>

`slap-mapd evaluate --trace-seeds` traces the chosen and last checkpoints too, but only after
playing every checkpoint on the validation seeds, which takes hours. This plays one episode.
"""

import argparse
import subprocess
import sys
from pathlib import Path

from slap_mapd_coupling.training.config import split_seeds
from slap_mapd_coupling.training.evaluate_run import (build_test_study, checkpoints_of,
                                                      load_run_spec, play)
from slap_mapd_coupling.training.spec import build_study, training_storage_mode


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--checkpoint", type=int, default=None, help="default: the last")
    parser.add_argument("--seed", type=int, default=None, help="default: the first test seed")
    parser.add_argument("--storage-mode", default=None, help="default: the training rule")
    parser.add_argument("--horizon", type=int, default=None, help="default: the run's own")
    parser.add_argument("--warmup", type=int, default=None)
    args = parser.parse_args()

    run_dir = args.run_dir.expanduser()
    checkpoints = checkpoints_of(run_dir)
    if not checkpoints:
        raise SystemExit(f"{run_dir} holds no checkpoints.")
    if args.checkpoint is None:
        checkpoint = checkpoints[-1]
    else:
        named = [c for c in checkpoints if c.name == f"checkpoint_{args.checkpoint:06d}"]
        if not named:
            raise SystemExit(f"No checkpoint_{args.checkpoint:06d} in {run_dir}, it has "
                             f"{checkpoints[0].name} to {checkpoints[-1].name}.")
        checkpoint = named[0]

    spec = load_run_spec(run_dir)
    study = build_study(spec)
    test_spec, test_study = build_test_study(spec, study, None, args.horizon, args.warmup)
    seed = args.seed if args.seed is not None else split_seeds(study.seed_split).test[0]
    mode = args.storage_mode or training_storage_mode(test_spec)
    trace = run_dir / "traces" / f"{checkpoint.name}_{mode}_seed{seed}.jsonl"
    trace.parent.mkdir(parents=True, exist_ok=True)

    print(f"playing {checkpoint.name} on seed {seed} under {mode}, {test_spec.horizon} steps",
          flush=True)
    metrics = play(test_study, test_spec, checkpoint, seed, args.storage_mode, trace)
    print(f"completed {metrics.num_completed_tasks} tasks ({(metrics.completed_share or 0):.0%} of "
          f"those released), backlog {metrics.backlog}, keeps up {metrics.keeps_up}, longest "
          f"stand still {metrics.longest_stand_still}, mean pick service time "
          f"{metrics.mean_service_time}, of it waiting for a robot {metrics.mean_wait_for_agent} "
          f"and blocked {metrics.mean_blocked_time}")
    print(trace)
    subprocess.run([sys.executable, "-m", "slap_mapd_coupling.evaluation.trace", str(trace)],
                   check=False)
    print(f"\nReplay: {sys.executable} -m slap_mapd_coupling.viz.pygame_renderer {trace}")


if __name__ == "__main__":
    main()
