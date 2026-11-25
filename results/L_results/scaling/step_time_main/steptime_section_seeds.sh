#!/bin/bash
# Section-based at 32 and 64 agents on two more seeds (author 2026-11-24). On seed 200000 the time
# did not grow from 32 to 64 (63, 60 ms) because the busiest zone held about 22 agents at 32 and 16
# at 64, and the section router takes one round per agent of its busiest zone. These runs show
# whether 32 is one jammed seed or a pattern. Same code, checkpoint and settings as steptime_main.sh.
D=$HOME/thesis_runs/scaling_2026-11; O=$D/timing/main_bdfda94/section_seeds
W=$HOME/worktrees/main-bdfda94; PY=$HOME/.venvs/rl/bin/python
T=$HOME/thesis_runs/training/fleet_16; E=$HOME/thesis_runs/evaluation/fleet_16
FLEETS=${FLEETS:-"32 64"}; SEEDS=${SEEDS:-"200001 200002"}
export PYTHONPATH=src OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 SLAP_WAREHOUSE_STORE=$HOME/thesis_runs/warehouses
mkdir -p $O; cd $W
log() { echo "$(date '+%F %T') $*" >> $O/log; }
eval "$(sed -n '/^run_dir() {/,/^done; }/p;/^checkpoint() {/,/evaluation.json \$c09; }/p' $D/run.sh)"
eval "$(sed -n '/^quiet() {/,/^  done; }/p' $D/steptime_main.sh)"
R=$(run_dir section); CK=$(checkpoint section $R) || { log "no checkpoint"; exit 1; }
log "start: main $(git rev-parse --short HEAD), fleets $FLEETS, seeds $SEEDS, $(basename $CK)"
for s in $SEEDS; do
  for m in $FLEETS; do
    quiet; log "fleet $m section seed $s"
    $PY $D/timing_probe.py $R $CK --target configs/fleet_$m/section.yaml --sections $((3 * m / 16)) \
      --steps 3000 --warmup 2000 --seed $s --gpu --output $O/rows.jsonl > $O/${m}_$s.log 2>&1
    log "fleet $m seed $s exit $?: $(tail -1 $O/${m}_$s.log)"
  done
done
log "finished"
