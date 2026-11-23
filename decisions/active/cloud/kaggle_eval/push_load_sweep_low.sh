#!/usr/bin/env bash
# Push load_sweep_low.py as a private Kaggle CPU kernel ([A111]): Token Passing below each
# fleet's capacity, 20 seeds, served counts. No dataset needed.
#   push_load_sweep_low.sh            (BRANCH=main by default)
# Fetch:  kaggle kernels output bjarkekarlsen/slap-load-sweep-low -p ~/thesis_runs/load_low_kaggle
# then copy E_load/fleet_<m>/served_check_low into thesis-progress/results/E_load/fleet_<m>/.
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
slug=slap-load-sweep-low
work=$(mktemp -d)
sed -e "s#@BRANCH@#${BRANCH:-main}#" $here/load_sweep_low.py > $work/sweep.py
cat > $work/kernel-metadata.json <<J
{"id": "bjarkekarlsen/$slug", "title": "$slug", "code_file": "sweep.py", "language": "python",
 "kernel_type": "script", "is_private": true, "enable_gpu": false, "enable_tpu": false,
 "enable_internet": true, "dataset_sources": [], "competition_sources": [], "kernel_sources": []}
J
out=$(kaggle kernels push -p $work 2>&1); echo "$out"
rm -rf $work
grep -q "successfully pushed" <<< "$out"
