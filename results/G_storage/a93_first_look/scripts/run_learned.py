"""One episode of a learned checkpoint under one storage variant, appended as a JSON row.

The same checkpoint plays every variant on the same test seeds, so the comparison is paired.
Usage: run_learned.py RUN_DIR CHECKPOINT VARIANT BETA SEED HORIZON WARMUP OUT.jsonl
"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import variants  # noqa: E402

from slap_mapd_coupling.evaluation.evaluator import row_keeps_up  # noqa: E402
from slap_mapd_coupling.training.evaluate_run import (  # noqa: E402
    build_test_study, load_run_spec, play)
from slap_mapd_coupling.training.spec import build_study  # noqa: E402

run_dir, checkpoint, variant, beta, seed, horizon, warmup, out = sys.argv[1:]
beta, seed, horizon, warmup = float(beta), int(seed), int(horizon), int(warmup)
run = Path(run_dir)
spec = load_run_spec(run)
if variant in ("fixed", "demand", "congestion"):
    mode = variant
else:
    variants.install(variant, beta)
    mode = "congestion"
spec = spec.model_copy(update={"storage_rule": spec.storage_rule.model_copy(
    update={"congestion_weight": beta})}) if mode == "congestion" else spec
study = build_study(spec)  # prepare: sets the padding cap the policy was trained with; stored seeds are skipped
test_spec, test_study = build_test_study(spec, study, None, horizon, warmup)
ckpt = next(run.glob(f"*/PPO_*/{checkpoint}"))
t0 = time.time()
m = play(test_study, test_spec, ckpt, seed, storage_mode=mode).model_dump(mode="json")
row = dict(m, variant=variant, beta=beta, seed=seed, checkpoint=checkpoint,
           seconds=round(time.time() - t0), keeps_up=row_keeps_up(m, spec.experiment.keep_up_threshold))
with open(out, "a") as f:
    f.write(json.dumps(row) + "\n")
print(variant, beta, seed, row["mean_service_time"], row["keeps_up"], row["seconds"], "s")
