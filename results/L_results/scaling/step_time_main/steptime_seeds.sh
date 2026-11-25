#!/bin/bash
# Step time test on seeds 200001 to 200004 (author 2026-11-24), so the thesis gives the mean over 5 seeds
# (200000 is in ../rows.jsonl). Why: the section-based time follows its busiest zone, so one seed's
# traffic can move a value (section at 32: 63 ms on 200000, 37 and 43 ms on 200001 and 200002).
# Same code, checkpoints and settings as steptime_main.sh. Waits for steptime-section to end, skips the
# section rows it already made. Out: timing/main_bdfda94/seeds/ (rows.jsonl, tp_<m>_<T> with seeds 200000 to 200004, log).
D=$HOME/thesis_runs/scaling_2026-11; O=$D/timing/main_bdfda94/seeds; S=$D/timing/main_bdfda94/section_seeds
W=$HOME/worktrees/main-bdfda94; PY=$HOME/.venvs/rl/bin/python
T=$HOME/thesis_runs/training/fleet_16; E=$HOME/thesis_runs/evaluation/fleet_16
FLEETS=${FLEETS:-"8 16 32 64 128"}; SEEDS=${SEEDS:-"200001 200002 200003 200004"}
ARMS=${ARMS:-"decentralised decentralised_comm section centralised"}
export PYTHONPATH=src OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 SLAP_WAREHOUSE_STORE=$HOME/thesis_runs/warehouses
mkdir -p $O; cd $W
log() { echo "$(date '+%F %T') $*" >> $O/log; }
eval "$(sed -n '/^run_dir() {/,/^done; }/p;/^checkpoint() {/,/evaluation.json \$c09; }/p' $D/run.sh)"
eval "$(sed -n '/^sections() {/p;/^quiet() {/,/^  done; }/p' $D/steptime_main.sh)"
while systemctl --user is-active -q steptime-section; do sleep 30; done
log "start: main $(git rev-parse --short HEAD), fleets $FLEETS, seeds $SEEDS, arms $ARMS"
declare -A LOAD=([8]=0.09 [16]=0.18 [32]=0.3 [64]=0.6 [128]=1.2)
for s in $SEEDS; do
  for m in $FLEETS; do
    for arm in $ARMS; do
      if [ $arm = section ] && [ -f $S/rows.jsonl ] && grep -q "\"num_agents\": $m,.*\"seed\": $s," $S/rows.jsonl; then
        log "fleet $m section seed $s: done in section_seeds, skipped"; continue; fi
      R=$(run_dir $arm); CK=$(checkpoint $arm $R) || { log "fleet $m $arm: no checkpoint"; continue; }
      cfg=$arm; [ $arm = decentralised_comm ] && cfg=decentralised
      extra=""; [ $arm = section ] && extra="--sections $(sections $m)"
      quiet; log "fleet $m $arm seed $s ($(basename $CK))"
      $PY $D/timing_probe.py $R $CK --target configs/fleet_$m/$cfg.yaml $extra --steps 3000 \
        --warmup 2000 --seed $s --gpu --output $O/rows.jsonl > $O/${m}_${arm}_$s.log 2>&1
      log "fleet $m $arm seed $s exit $?: $(tail -1 $O/${m}_${arm}_$s.log | cut -c1-60)"
    done
  done
done
for m in $FLEETS; do   # Token Passing: the first 5 test seeds in one run, one timing row per seed
  for N in 2000 3000; do
    quiet; log "fleet $m token_passing 5 seeds $N steps"
    $PY $D/measure_cmd.py $O/tp_${m}_$N.res.json -- $PY scripts/sweep/load_sweep.py \
      --config configs/fleet_$m/decentralised.yaml --rates ${LOAD[$m]} --seeds 5 --seed-set test \
      --storage-modes congestion --horizon $N --warmup 0 --workers 1 --out $O/tp_${m}_$N \
      > $O/tp_${m}_$N.log 2>&1
    log "fleet $m token_passing $N exit $?"
  done
done
log "finished"
