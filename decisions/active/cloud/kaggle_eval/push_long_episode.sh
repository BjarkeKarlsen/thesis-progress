#!/usr/bin/env bash
# Long-episode test on Kaggle (author, 2026-11-18): policies play one very long episode each, no
# training, with a trace, to see after how many steps they break down.
#   push_long_episode.sh SLUG STEPS "SEEDS" label=checkpoint_dir [label=checkpoint_dir ...]
# Each checkpoint dir is <run>/<name>/PPO_*/checkpoint_N; the run's *_spec.json is sent with it.
set -euo pipefail
slug=$1 steps=$2 seeds=$3; shift 3
here=$(cd "$(dirname "$0")" && pwd)
work=$(mktemp -d); mkdir -p $work/data/pol $work/kernel
for pair in "$@"; do
    label=${pair%%=*} ck=${pair#*=}
    trial=$(dirname $ck); name=$(dirname $trial); run=$(dirname $name)
    dst=$work/data/pol/run_$label/$(basename $name)/$(basename $trial)
    mkdir -p $dst; cp -r $ck $dst/; cp $run/*_spec.json $work/data/pol/run_$label/
done
tar -C $work/data/pol -cf $work/data/policies.tar .; rm -rf $work/data/pol
cat > $work/data/dataset-metadata.json <<J
{"title": "$slug-pol", "id": "bjarkekarlsen/$slug-pol", "licenses": [{"name": "CC0-1.0"}]}
J
if kaggle datasets status bjarkekarlsen/$slug-pol >/dev/null 2>&1; then
    kaggle datasets version -p $work/data -m "policies $(date '+%F %T')"
else kaggle datasets create -p $work/data; fi
for i in $(seq 1 30); do s=$(kaggle datasets status bjarkekarlsen/$slug-pol 2>&1 || true)
    echo "dataset: $s"; case "$s" in *ready*) break;; esac; sleep 20; done
sed -e "s#@BRANCH@#${BRANCH:-replay/served-counts}#" -e "s/@STEPS@/$steps/" -e "s/@SEEDS@/${seeds// /, }/" \
    $here/long_episode.py > $work/kernel/eval.py
cat > $work/kernel/kernel-metadata.json <<J
{"id": "bjarkekarlsen/$slug", "title": "$slug", "code_file": "eval.py", "language": "python",
 "kernel_type": "script", "is_private": true, "enable_gpu": false, "enable_tpu": false,
 "enable_internet": true, "dataset_sources": ["bjarkekarlsen/$slug-pol"],
 "competition_sources": [], "kernel_sources": []}
J
out=$(kaggle kernels push -p $work/kernel 2>&1); echo "$out"; rm -rf $work
grep -q "successfully pushed" <<< "$out"
