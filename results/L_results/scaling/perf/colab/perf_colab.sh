#!/bin/bash
# Colab lane of the performance test (author 2026-11-24): the episodes nobody has claimed yet go to
# one Colab CPU high-mem machine (8 cores, ~0.26 units/h), so the PC is free for the step time test.
# Served share does not depend on the machine, so the rows join the PC's and the Lenovo's.
# Same code (main bdfda94, as ~/worktrees/main-bdfda94), same job.sh, same runs and checkpoints,
# same prepared warehouses.
#
#   perf_colab.sh smoke   open the session, install, play 40 steps of the dearest job, claims nothing
#   perf_colab.sh run     claim every unclaimed job, play them in LANES lanes, fetch until done
#   perf_colab.sh watch   resume watching a running session (after the watcher was stopped)
#
# Claims go in perf/claims like the other lanes, so PC and Lenovo lanes skip these jobs. If the
# session dies or fails, every claimed job without an exit file at home is released again.
# Rows and logs land in perf/rows and perf/logs, and "colab lane" lines in perf/log.
# Session f16-perf (the keep-alive pings every f16-* session). Unit colab-perf. Log: colab/colab.log.
export PATH=$HOME/.local/bin:$PATH
P=$HOME/thesis_runs/scaling_2026-11/perf; C=$P/colab; S=f16-perf
LANES=${LANES:-7}; INTERVAL=${INTERVAL:-900}
mkdir -p $C
log() { echo "$(date '+%F %T') $*" >> $C/colab.log; }
plog() { echo "$(date '+%F %T') colab lane: $*" >> $P/log; }

remote() {  # python on stdin, runs on the session, retried when the connection drops
  local code out try; code=$(cat)
  for try in 1 2 3; do
    out=$(printf '%s\n' "$code" | timeout 900 colab exec -s $S 2>&1)
    grep -q "Connection was lost" <<< "$out" || { printf '%s\n' "$out"; return 0; }
    sleep 20
  done
  printf '%s\n' "$out"; return 1; }

# run and checkpoint of each arm, as perf.sh chose them (its "ARM: path" lines)
ckpt_of() { grep -E "^.{20}$1: training/" $P/log | tail -1 | sed "s/^.\{20\}$1: //"; }
run_of() { local c; c=$(ckpt_of $1); echo ${c%%/$1_congestion/*}; }

release() {  # gives back every claimed job that has no exit file at home
  local n=0
  while read -r m a s; do
    [ -f $P/logs/${m}_${a}_$s.exit ] || { rmdir $P/claims/${m}_${a}_$s 2>/dev/null && n=$((n+1)); }
  done < $C/jobs.claimed
  log "released $n jobs"; plog "released $n unfinished jobs to the PC and Lenovo lanes"; }

start() {  # $1 = 1 for the smoke test (claims nothing)
  local smoke=$1 tmp full jobs_json="" arms="" m a s
  tmp=$(mktemp -d)
  full=$(git -C $HOME/worktrees/main-bdfda94 rev-parse HEAD)
  : > $C/jobs.claimed
  while read -r m a s; do
    if [ $smoke = 1 ]; then [ -d $P/claims/${m}_${a}_$s ] && continue
    else mkdir $P/claims/${m}_${a}_$s 2>/dev/null || continue; fi
    echo "$m $a $s" >> $C/jobs.claimed
  done < $P/jobs.txt
  [ -s $C/jobs.claimed ] || { log "nothing left to claim"; return 1; }
  [ $smoke = 1 ] && tail -1 $C/jobs.claimed > $C/jobs.smoke && cp $C/jobs.smoke $C/jobs.claimed
  arms=$(awk '{print $2}' $C/jobs.claimed | sort -u)
  while read -r m a s; do
    jobs_json+="[$m, \"$a\", $s, \"$(run_of $a)\", \"$(ckpt_of $a)\"],"
  done < $C/jobs.claimed
  echo "{\"commit\": \"$full\", \"lanes\": $LANES, \"smoke_only\": $([ $smoke = 1 ] && echo true || echo false), \"jobs\": [${jobs_json%,}]}" > $tmp/perf_job.json
  (cd $HOME/thesis_runs && tar -czf $tmp/runs.tgz $(for a in $arms; do run_of $a; done))
  (cd $HOME/thesis_runs/warehouses && tar -czf $tmp/warehouses.tgz \
     $(for m in $(awk '{print $1}' $C/jobs.claimed | sort -u); do for a in $arms; do
         cfg=$a; [ $a = decentralised_comm ] && cfg=decentralised; ls -d fleet${m}_${cfg}_*; done; done))
  log "$(wc -l < $C/jobs.claimed) jobs ($arms), runs $(du -h $tmp/runs.tgz | cut -f1), warehouses $(du -h $tmp/warehouses.tgz | cut -f1)"
  local ok=
  for try in 1 2 3 4 5 6; do
    colab sessions 2>/dev/null | grep -q "^\[$S\] " && { ok=1; break; }
    log "opening $S (CPU high-mem), try $try"
    colab new -s $S --high-mem >> $C/colab.log 2>&1 && { ok=1; break; }
    colab stop -s $S >> $C/colab.log 2>&1; sleep 600
  done
  [ -n "$ok" ] || { log "no Colab machine"; [ $smoke = 1 ] || release; return 1; }
  remote <<< 'import os; os.makedirs("/content/in", exist_ok=True)' > /dev/null
  for f in runs.tgz warehouses.tgz; do
    colab upload -s $S $tmp/$f /content/in/$f >> $C/colab.log 2>&1 || { log "upload $f failed"; [ $smoke = 1 ] || release; return 1; }
  done
  colab upload -s $S $tmp/perf_job.json /content/perf_job.json > /dev/null &&
  colab upload -s $S $P/job.sh /content/job.sh > /dev/null &&
  colab upload -s $S $C/perf_remote.py /content/perf_remote.py > /dev/null || { [ $smoke = 1 ] || release; return 1; }
  remote <<'EOF' >> $C/colab.log
import os, subprocess, sys
# a retried call must not start a second copy (a start hung in colab exec on 2026-11-24)
if subprocess.run("pgrep -f perf_remote.py", shell=True, capture_output=True).returncode == 0 \
        or os.path.exists("/content/state.txt"):
    print("started (already running)")
else:
    subprocess.Popen(f"nohup {sys.executable} /content/perf_remote.py > /content/job.log 2>&1 &",
                     shell=True, start_new_session=True)
    print("started")
EOF
  [ $smoke = 1 ] || plog "$(wc -l < $C/jobs.claimed) jobs claimed, on $S ($LANES lanes)"
  rm -rf $tmp; }

fetch() {  # copies finished rows and logs home, prints STATE ...
  local tmp out m a s k
  tmp=$(mktemp -d)
  out=$(remote <<'EOF'
import os, subprocess
st = open("/content/state.txt").read().strip() if os.path.exists("/content/state.txt") else "none"
subprocess.run("tar -czf /content/out.tgz rows logs", shell=True,
               cwd="/root/thesis_runs/scaling_2026-11/perf")
print("STATE", st)
EOF
) || { rm -rf $tmp; return 1; }
  if colab download -s $S /content/out.tgz $tmp/out.tgz > /dev/null 2>&1 && tar -xzf $tmp/out.tgz -C $tmp; then
    while read -r m a s; do k=${m}_${a}_$s
      [ -f $tmp/logs/$k.exit ] && [ ! -f $P/logs/$k.exit ] || continue
      cp $tmp/logs/$k.log $P/logs/ 2>/dev/null; cp $tmp/rows/$k.jsonl $P/rows/ 2>/dev/null
      cp $tmp/logs/$k.exit $P/logs/
      plog "$m $a $s exit $(cat $P/logs/$k.exit)"
    done < $C/jobs.claimed
  fi
  rm -rf $tmp
  grep "^STATE" <<< "$out" | tail -1; }

watch() {
  local line misses=0
  while :; do
    line=$(fetch); log "${line:-no answer}"
    case $line in
      "STATE finished"*|"STATE failed"*)
        colab download -s $S /content/job.log $C/job.log > /dev/null 2>&1
        colab stop -s $S >> $C/colab.log 2>&1
        [ -f $C/jobs.smoke ] && [ "$(cat $C/jobs.claimed)" = "$(cat $C/jobs.smoke)" ] || release
        log "ended: $line"; return 0 ;;
      "") misses=$((misses+1)); [ $misses -ge 4 ] && { log "session gone"; release; return 1; } ;;
      *) misses=0 ;;
    esac
    sleep $INTERVAL
  done; }

case ${1:-} in
  smoke) rm -f $C/jobs.smoke; start 1 && INTERVAL=120 watch; exit ;;
  run) rm -f $C/jobs.smoke; start 0 && watch; exit ;;
  watch) watch; exit ;;   # resume watching a running session (jobs.claimed kept)
  *) sed -n 2,15p $0; exit 2 ;;
esac
