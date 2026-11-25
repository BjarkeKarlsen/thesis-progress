#!/bin/bash
# Step time test from main with GPU, RAM and CPU measures (author 2026-11-24). Replaces the old
# timing.sh rows and scaling-clean128, so the figure and table of step time come from one code
# version: main bdfda94 (#213 to #215), ~/worktrees/main-bdfda94.
# Each learned congestion-aware fleet 16 policy at its [A111] checkpoint, in the warehouse of 8, 16,
# 32, 64 and 128 agents at that fleet's main load. Seed 200000, 3000 steps, 2000 warm-up, timed
# over the last 1000 (timing_probe.py, with resources.py), one core, the network on the GPU.
# Section-based: 2 sections at 8, 3m/16 to 64, 16 at 128 (one per aisle). Then Token Passing at
# every fleet on the CPU, played for 2000 and 3000 steps (the last 1000 from the difference), RAM
# and CPU through measure_cmd.py.
# The PC must be quiet: before every episode it waits until no game runs (Wow.exe, Battle.net) and
# the load over the last minute is under 2.5. Every row records the PC load and the other GPU
# programs during its window, so a disturbed row shows. Unit steptime-main. Log: timing/main_bdfda94/log.
D=$HOME/thesis_runs/scaling_2026-11; O=$D/timing/main_bdfda94
W=$HOME/worktrees/main-bdfda94; PY=$HOME/.venvs/rl/bin/python
T=$HOME/thesis_runs/training/fleet_16; E=$HOME/thesis_runs/evaluation/fleet_16
FLEETS=${FLEETS:-"8 16 32 64 128"}
ARMS=${ARMS:-"decentralised decentralised_comm section centralised"}
export PYTHONPATH=src OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 SLAP_WAREHOUSE_STORE=$HOME/thesis_runs/warehouses
mkdir -p $O; cd $W
log() { echo "$(date '+%F %T') $*" >> $O/log; }
eval "$(sed -n '/^run_dir() {/,/^done; }/p;/^checkpoint() {/,/evaluation.json \$c09; }/p' $D/run.sh)"
sections() { case $1 in 8) echo 2;; 128) echo 16;; *) echo $((3 * $1 / 16));; esac; }
quiet() {  # waits for a quiet PC, logs why it waits
  local why last=""
  while :; do
    why=""
    pgrep -f 'Wow.exe|Battle.net' > /dev/null && why="a game runs"
    awk '{exit !($1 >= 2.5)}' /proc/loadavg && why="${why:+$why, }load $(cut -d' ' -f1 /proc/loadavg)"
    [ -z "$why" ] && return
    [ "$why" != "$last" ] && log "waiting: $why"; last=$why
    sleep 60
  done; }

log "start: main $(git rev-parse --short HEAD), fleets $FLEETS, arms $ARMS"
for m in $FLEETS; do
  for arm in $ARMS; do
    R=$(run_dir $arm); CK=$(checkpoint $arm $R) || { log "fleet $m $arm: no checkpoint"; continue; }
    cfg=$arm; [ $arm = decentralised_comm ] && cfg=decentralised
    extra=""; [ $arm = section ] && extra="--sections $(sections $m)"
    quiet; log "fleet $m $arm ($(basename $CK))"
    $PY $D/timing_probe.py $R $CK --target configs/fleet_$m/$cfg.yaml $extra --steps 3000 \
      --warmup 2000 --seed 200000 --gpu --output $O/rows.jsonl > $O/${m}_$arm.log 2>&1
    log "fleet $m $arm exit $?: $(tail -1 $O/${m}_$arm.log)"
  done
done
declare -A LOAD=([8]=0.09 [16]=0.18 [32]=0.3 [64]=0.6 [128]=1.2)
for m in $FLEETS; do
  for N in 2000 3000; do
    quiet; log "fleet $m token_passing $N steps"
    $PY $D/measure_cmd.py $O/tp_${m}_$N.res.json -- $PY scripts/sweep/load_sweep.py \
      --config configs/fleet_$m/decentralised.yaml --rates ${LOAD[$m]} --seeds 1 --seed-set test \
      --storage-modes congestion --horizon $N --warmup 0 --workers 1 --out $O/tp_${m}_$N \
      > $O/tp_${m}_$N.log 2>&1
    log "fleet $m token_passing $N exit $?"
  done
done
log "finished"
