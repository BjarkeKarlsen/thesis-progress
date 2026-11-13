"""One Token Passing episode of one variant, appended as a JSON row.

Usage: run_variant.py CONFIG VARIANT BETA RATE SEED HORIZON WARMUP OUT.jsonl
VARIANT: fixed | demand | congestion (the rules on main) | demand_smooth | aisle | pressure
"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import variants  # noqa: E402

from slap_mapd_coupling.core.experiment_config import ExperimentConfig  # noqa: E402
from slap_mapd_coupling.evaluation.evaluator import row_keeps_up, run_episode  # noqa: E402
from slap_mapd_coupling.training.spec import (  # noqa: E402
    build_experiment_config, build_study, load_spec, override_spec)

config, variant, beta, rate, seed, horizon, warmup, out = sys.argv[1:]
beta, rate, seed, horizon, warmup = float(beta), float(rate), int(seed), int(horizon), int(warmup)
spec = override_spec(load_spec(Path(config)), arrival_rate=rate, horizon=horizon, warmup=warmup)
if variant in ("fixed", "demand", "congestion"):
    mode = variant
else:
    variants.install(variant, beta)
    mode = "congestion"
study = build_study(spec, prepare=False)
played = study if study.pool is None else study.pool.warehouse(seed)
cfg = build_experiment_config(spec, seed, mode)
cfg = ExperimentConfig.model_validate(
    {**cfg.model_dump(), "controller": None, "planner": "token_passing",
     **({"congestion_weight": beta} if mode == "congestion" else {})})
t0 = time.time()
m = run_episode(played.instance.graph, played.skus, played.counts, played.capacities, cfg,
                positions=played.instance.positions).model_dump(mode="json")
row = dict(m, variant=variant, beta=beta, rate=rate, seed=seed, seconds=round(time.time() - t0),
           keeps_up=row_keeps_up(m, spec.experiment.keep_up_threshold))
with open(out, "a") as f:
    f.write(json.dumps(row) + "\n")
print(variant, beta, rate, seed, row["mean_service_time"], row["keeps_up"], row["seconds"], "s")
