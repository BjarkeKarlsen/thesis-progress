#!/bin/bash
# Performance test (author 2026-11-23 20:00: split from the step time test, run on the PC and the
# Lenovo). The learned congestion-aware fleet 16 policies, at their [A111] checkpoints, at 8, 32
# and 64 agents (16 has its 20 test seeds already), 20 test seeds, 10000 steps, 5000 warm-up as the
# fleet 16 rows, on the CPU on both machines. Served share is independent of the machine and of
# what runs next to it, so the episodes run side by side; their times are not used.
# 1. waits for the step time test (unit scaling-timing) to end, so the PC is quiet while it times
# 2. builds the warehouses of the 20 seeds per fleet and arm (prep.py)
# 3. copies code, runs and warehouses to the Lenovo
# 4. PC_LANES episodes at once here, BOX_LANES on the Lenovo once its own queue (eval-lenovo) and
#    the PC queue (pc-queue, its step 4 may use the box) are done. Jobs from jobs.txt, cheapest
#    first, centralised at 64 last; each claimed once (claims/).
# Unit scaling-perf. Log: perf/log. Rows: perf/rows/FLEET_ARM_SEED.jsonl
D=$HOME/thesis_runs/scaling_2026-11; P=$D/perf; H=thesis-eval
W=$HOME/worktrees/scaling-run; PY=$HOME/.venvs/rl/bin/python
PC_LANES=${PC_LANES:-7}; BOX_LANES=${BOX_LANES:-4}
log() { echo "$(date '+%F %T') $*" >> $P/log; }
eval "$(sed -n '/^run_dir() {/,/^done; }/p;/^checkpoint() {/,/evaluation.json \$c09; }/p' $D/run.sh)"
T=$HOME/thesis_runs/training/fleet_16; E=$HOME/thesis_runs/evaluation/fleet_16
rel() { echo ${1#$HOME/thesis_runs/}; }

log "1. waiting for the step time test"
while systemctl --user is-active --quiet scaling-timing; do sleep 300; done
declare -A RUN CKPT
for arm in decentralised decentralised_comm section centralised; do
  RUN[$arm]=$(run_dir $arm); CKPT[$arm]=$(checkpoint $arm ${RUN[$arm]})
  [ -n "${CKPT[$arm]}" ] || { log "no checkpoint for $arm, stop"; exit 1; }
  log "$arm: $(rel ${CKPT[$arm]})"
done

log "2. building the warehouses of the 20 test seeds"
PREP=(); for m in 8 32 64; do for a in decentralised decentralised_comm section centralised; do
  PREP+=("$m $a ${RUN[$a]}"); done; done
(cd $W && PYTHONPATH=src OMP_NUM_THREADS=1 SLAP_WAREHOUSE_STORE=$HOME/thesis_runs/warehouses \
  $PY $P/prep.py 8 "${PREP[@]}") >> $P/log 2>&1 \
  || { log "2. failed, needs a hand"; exit 1; }

log "3. copying code, runs and warehouses to $H"
ssh -n $H "mkdir -p /root/code/scaling /root/thesis_runs/scaling_2026-11/perf /root/thesis_runs/warehouses" &&
rsync -a --delete --exclude .git $W/ $H:/root/code/scaling/ &&
rsync -a $P/job.sh $H:/root/thesis_runs/scaling_2026-11/perf/ &&
for a in "${!RUN[@]}"; do r=$(rel ${RUN[$a]}); ssh -n $H "mkdir -p /root/thesis_runs/$(dirname $r)"; rsync -a ${RUN[$a]} $H:/root/thesis_runs/$(dirname $r)/ || exit 1; done &&
rsync -a $HOME/thesis_runs/warehouses/fleet{8,32,64}_* $H:/root/thesis_runs/warehouses/ \
  || { log "3. copy failed, the Lenovo is left out"; BOX_LANES=0; }

claim() {  # prints the next unclaimed job and claims it
  while read -r m a s; do
    mkdir $P/claims/${m}_${a}_$s 2>/dev/null && { echo "$m $a $s"; return 0; }
  done < $P/jobs.txt; return 1; }
pc_lane() {
  while job=$(claim); do set -- $job
    log "PC lane $1: $job"
    bash $P/job.sh $1 $2 $3 $(rel ${RUN[$2]}) $(rel ${CKPT[$2]})
    log "PC lane $1: $job exit $(cat $P/logs/${1}_${2}_$3.exit)"
  done; }
box_lane() {
  while systemctl --user is-active --quiet eval-lenovo || systemctl --user is-active --quiet pc-queue; do sleep 600; done
  while job=$(claim); do set -- $job; k=${1}_${2}_$3
    log "box lane: $job"
    ssh -n $H "rm -f /root/thesis_runs/scaling_2026-11/perf/logs/$k.exit; setsid -f env PY=/root/venv/bin/python W=/root/code/scaling bash /root/thesis_runs/scaling_2026-11/perf/job.sh $1 $2 $3 $(rel ${RUN[$2]}) $(rel ${CKPT[$2]}) > /dev/null 2>&1 < /dev/null"
    until ssh -n $H "test -f /root/thesis_runs/scaling_2026-11/perf/logs/$k.exit" 2>/dev/null; do sleep 300; done
    rsync -a $H:/root/thesis_runs/scaling_2026-11/perf/rows/$k.jsonl $P/rows/ 2>/dev/null
    rsync -a $H:/root/thesis_runs/scaling_2026-11/perf/logs/$k.{log,exit} $P/logs/
    log "box lane: $job exit $(cat $P/logs/$k.exit)"
  done; }

log "4. $PC_LANES lanes on the PC, $BOX_LANES on $H"
for i in $(seq 1 $PC_LANES); do pc_lane & sleep 2; done
for i in $(seq 1 $BOX_LANES); do box_lane & sleep 2; done
wait
log "finished: $(ls $P/rows | wc -l) of $(wc -l < $P/jobs.txt) rows, failed: $(grep -lv '^0$' $P/logs/*.exit 2>/dev/null | wc -l)"
