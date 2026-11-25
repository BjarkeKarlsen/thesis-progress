#!/bin/bash
# Step time test (author 2026-11-23 20:00, split from the performance test). Each learned
# congestion-aware fleet 16 policy, at its [A111] checkpoint (the 0.9 rule), in the warehouse of 8,
# 16, 32 and 64 agents at that fleet's main load. One seed (200000), 3000 steps with 2000 warm-up,
# timed over the 1000 measured steps only and per 100 steps (timing_probe.py). One episode at a
# time, one core, the network on the GPU, nothing else on the PC. No Token Passing (author).
# Code: ~/worktrees/scaling-run (main 8ba3048 + scaling_probe, PR #210). Rows: timing/rows.jsonl.
# Unit scaling-timing, under systemd-inhibit. Log: timing/log.
D=$HOME/thesis_runs/scaling_2026-11
W=$HOME/worktrees/scaling-run
T=$HOME/thesis_runs/training/fleet_16
E=$HOME/thesis_runs/evaluation/fleet_16
PY=$HOME/.venvs/rl/bin/python
STEPS=${STEPS:-3000}; WARM=${WARM:-2000}; SEED=${SEED:-200000}
FLEETS=${FLEETS:-"8 16 32 64"}
ARMS=${ARMS:-"decentralised decentralised_comm section centralised"}
OUT=${OUT:-$D/timing/rows.jsonl}
export PYTHONPATH=src OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 SLAP_WAREHOUSE_STORE=$HOME/thesis_runs/warehouses
log() { echo "$(date '+%F %T') $*" | tee -a $D/timing/log; }
# run_dir and checkpoint as in run.sh (the 0.9 choice in the chosen checkpoint's folder)
eval "$(sed -n '/^run_dir() {/,/^done; }/p;/^checkpoint() {/,/evaluation.json \$c09; }/p;/^sections() {/p' $D/run.sh)"
mkdir -p $D/timing; cd $W
log "start: fleets $FLEETS, arms $ARMS, seed $SEED, $STEPS steps, warm-up $WARM"
for m in $FLEETS; do
  for arm in $ARMS; do
    R=$(run_dir $arm); CK=$(checkpoint $arm $R) || { log "fleet $m $arm: no checkpoint"; continue; }
    cfg=$arm; [ $arm = decentralised_comm ] && cfg=decentralised
    extra=""; [ $arm = section ] && extra="--sections $(sections $m)"
    log "fleet $m $arm ($(basename $CK))"
    $PY $D/timing_probe.py $R $CK --target configs/fleet_$m/$cfg.yaml $extra --steps $STEPS \
      --warmup $WARM --seed $SEED --gpu --output $OUT > $D/timing/${m}_$arm.log 2>&1
    log "fleet $m $arm exit $?: $(tail -1 $D/timing/${m}_$arm.log)"
  done
done
log "finished"
