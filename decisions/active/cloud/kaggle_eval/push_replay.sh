#!/usr/bin/env bash
# Replay the test of one trained run on Kaggle with the served counts: upload its folder as a
# private dataset, then push eval_replay.py (a copy of push_eval.sh with the replay kernel).
#   push_replay.sh FLEET ARM REGIME      e.g. push_replay.sh 8 section fixed
# BRANCH=feat/parallel-evaluation WORKERS=4 plays 4 episodes at once (default main, 1).
# RESUME_ROWS=<folder> with BRANCH=feat/evaluate-resume finishes a test that ran out of time.
# The run is ~/thesis_runs/training/fleet_<m>/<arm>/<regime>. The kernel is
# bjarkekarlsen/slap-eval-f<m>-<arm>-<regime>. Bring the result home with fetch_eval.sh.
set -euo pipefail
fleet=$1 arm=$2 regime=$3
here=$(cd "$(dirname "$0")" && pwd)
run=$HOME/thesis_runs/training/fleet_$fleet/$arm/$regime
[ -f "$run/done" ] || { echo "$run is not trained"; exit 1; }
slug=slap-replay-f$fleet-${arm//_/-}-$regime
work=$(mktemp -d)
# The dataset: the run folder as run.tar, without anything a test does not read.
mkdir -p $work/data
tar -C "$(dirname $run)" --transform "s#^$regime#run#" --exclude="$regime/train.log" \
    -cf $work/data/run.tar $regime
# RESUME_ROWS=<an earlier evaluation folder> sends its test.jsonl, so the kernel plays only the
# missing episodes (needs BRANCH=feat/evaluate-resume).
[ -n "${RESUME_ROWS:-}" ] && cp "$RESUME_ROWS/test.jsonl" $work/data/resume_test.jsonl
cat > $work/data/dataset-metadata.json <<J
{"title": "$slug-run", "id": "bjarkekarlsen/$slug-run", "licenses": [{"name": "CC0-1.0"}]}
J
if kaggle datasets status bjarkekarlsen/$slug-run >/dev/null 2>&1; then
    kaggle datasets version -p $work/data -m "run folder $(date '+%F %T')"
else
    kaggle datasets create -p $work/data
fi
for i in $(seq 1 30); do
    s=$(kaggle datasets status bjarkekarlsen/$slug-run 2>&1 || true)
    echo "dataset: $s"; case "$s" in *ready*) break;; esac; sleep 20
done
# The warehouse tables of the run's spec, when they are on Kaggle already (upload_warehouses.py).
key=$(cd ~/worktrees/train-d204dbd && PYTHONPATH=src ~/.venvs/rl/bin/python -c "
import glob, sys
from pathlib import Path
from slap_mapd_coupling.training.spec import load_spec
from slap_mapd_coupling.training.warehouses import pool_key
print(pool_key(load_spec(Path(glob.glob(sys.argv[1] + '/*_spec.json')[0]))))" $run 2>/dev/null | tail -1)
tables=""
if [ -n "$key" ] && kaggle datasets files bjarkekarlsen/slap-wh-${key//_/-} > /dev/null 2>&1; then
    tables=", \"bjarkekarlsen/slap-wh-${key//_/-}\""; echo "tables: slap-wh-${key//_/-}"
else
    echo "tables: none on Kaggle for $key, the kernel builds them"
fi
# The kernel.
mkdir -p $work/kernel
sed -e "s/@REGIME@/$regime/" -e "s#@BRANCH@#${BRANCH:-replay/served-counts}#" -e "s/@WORKERS@/${WORKERS:-4}/" \
    $here/eval_replay.py > $work/kernel/eval.py
cat > $work/kernel/kernel-metadata.json <<J
{"id": "bjarkekarlsen/$slug", "title": "$slug", "code_file": "eval.py", "language": "python",
 "kernel_type": "script", "is_private": true, "enable_gpu": false, "enable_tpu": false,
 "enable_internet": true, "dataset_sources": ["bjarkekarlsen/$slug-run"$tables],
 "competition_sources": [], "kernel_sources": []}
J
out=$(kaggle kernels push -p $work/kernel 2>&1); echo "$out"
rm -rf $work
grep -q "successfully pushed" <<< "$out"   # a refused push (5 CPU sessions) exits 1
