#!/usr/bin/env bash
# Train one arm of slap-mapd-coupling on Colab from this PC, with the Colab command line.
# Drive cannot be mounted from the command line, so the run lives on the Colab machine's disk
# and `watch` copies it home every INTERVAL seconds. A dropped session loses at most that much.
#
#   colab.bash start  SESSION FLEET ARM REGIME   open the session if needed and start training
#   colab.bash status SESSION                    the state, the last log lines, the units left
#   colab.bash fetch  SESSION FLEET ARM REGIME   copy what is new of the run (and warehouses) home
#   colab.bash watch  SESSION FLEET ARM REGIME   fetch every INTERVAL until it is done, then finish
#                                                the run as bedtime.bash does and stop the session.
#                                                A run stopped at HOURS, or whose machine is gone,
#                                                is continued on a fresh machine (RESTARTS)
#   colab.bash stop   SESSION                    stop the session
#
# ARM is decentralised or section, REGIME the storage rule it trains under: fixed, demand or
# congestion. The run goes to TRAINING/fleet_<m>/<arm>/<regime>, the same place as bedtime.bash.
# When that folder already holds a run, start sends it up and the machine continues it with
# `slap-mapd resume`.
#
# Settings, from the environment:
#   TRAINING  where runs live at home (~/thesis_runs/training; a scratch folder for a smoke test)
#   COMMIT    the slap-mapd-coupling commit to train (origin/main; a continued run keeps its own)
#   PATCH     a diff applied on top of COMMIT, to try a change before it is on GitHub (none)
#   LEARNER_CPUS  CPUs of the learner (the cores the runners leave; 1 as at home)
#   GPU       a GPU for the learner, such as T4 or L4 (none, a CPU machine). A run keeps the
#             machine type it started on, so continue a GPU run with the same GPU set
#   BATCH_ON_CPU  1 keeps the train batch in host memory, for a batch too big for the GPU
#   BUDGET    env steps, empty keeps the config's budget
#   HOURS     stop cleanly after this many hours (20)
#   RUNNERS   env runners, the same on every machine (3, as bedtime.bash)
#   INTERVAL  seconds between fetches of `watch` (1800)
#   STOP      1 stops the session when `watch` ends (1)
#   RESTARTS  times `watch` continues a stopped run on a fresh machine (6)
set -uo pipefail

HERE=$(cd "$(dirname "$0")" && pwd)
ROOT=~/Documents/thesis
REPO=$ROOT/slap-mapd-coupling
PYTHON=~/.venvs/rl/bin/python
TRAINING=${TRAINING:-$HOME/thesis_runs/training}
STORE=$HOME/thesis_runs/warehouses
RESULTS=$ROOT/thesis-progress/results
HOURS=${HOURS:-20}
RUNNERS=${RUNNERS:-3}
BUDGET=${BUDGET:-}
PATCH=${PATCH:-}
GPU=${GPU:-}
BATCH_ON_CPU=${BATCH_ON_CPU:-}
# The Colab CLI turns a GPU name it does not know into an A100, the dearest one, so only these.
case ${GPU,,} in
"" | t4 | l4 | g4 | h100 | a100) ;;
*) echo "GPU=$GPU is not one of T4, L4, G4, H100, A100" >&2; exit 2 ;;
esac
LEARNER_CPUS=${LEARNER_CPUS:-}
INTERVAL=${INTERVAL:-1800}
STOP=${STOP:-1}
RESTARTS=${RESTARTS:-6}

log() { echo "$(date '+%Y-%m-%d %H:%M') $*"; }

# Python from stdin on the session, tried three times since a connection can drop.
remote() {
    local session=$1 code out try
    code=$(cat)
    for try in 1 2 3; do
        out=$(printf '%s\n' "$code" | timeout 900 colab exec -s "$session" 2>&1)
        if ! grep -q "Connection was lost" <<< "$out"; then
            printf '%s\n' "$out"
            return 0
        fi
        log "connection lost, try $try of 3" >&2
        sleep 20
    done
    printf '%s\n' "$out"
    return 1
}

pool_key() {  # pool_key FLEET ARM: the warehouse store folder of that config
    (cd "$REPO" && "$PYTHON" -c '
import sys
from pathlib import Path
from slap_mapd_coupling.training.spec import load_spec
from slap_mapd_coupling.training.warehouses import pool_key
print(pool_key(load_spec(Path(f"configs/fleet_{sys.argv[1]}/{sys.argv[2]}.yaml"))))' "$1" "$2")
}

start() {
    local session=$1 fleet=$2 arm=$3 regime=$4
    local dest=$TRAINING/fleet_$fleet/$arm/$regime key commit tmp
    tmp=$(mktemp -d)
    trap 'rm -rf "$tmp"; trap - RETURN' RETURN  # the trap clears itself, so it does not fire again in watch
    # `colab status` exits 0 for a session that does not exist, so look in the list.
    if ! colab sessions 2>/dev/null | grep -q "^\[$session\] "; then
        log "opening session $session${GPU:+ with a $GPU GPU}"
        colab new -s "$session" --high-mem ${GPU:+--gpu "$GPU"} || return 1
    fi
    if [ -f "$dest/commit.txt" ]; then
        commit=$(head -n 1 "$dest/commit.txt" | cut -d' ' -f1)
    else
        git -C "$REPO" fetch -q origin main
        commit=${COMMIT:-$(git -C "$REPO" rev-parse origin/main)}
    fi
    key=$(pool_key "$fleet" "$arm") || return 1
    log "fleet $fleet $arm $regime at $commit, warehouses $key, run $dest"

    # The warehouse tables, when this PC has them.
    if [ -f "$STORE/$key/manifest.json" ]; then
        tar -czf "$tmp/warehouses.tgz" -C "$STORE" "$key"
        log "sending the warehouse tables, $(du -h "$tmp/warehouses.tgz" | cut -f1)"
        colab upload -s "$session" "$tmp/warehouses.tgz" /content/warehouses.tgz || return 1
    fi
    # A run already started, to continue.
    if ls "$dest"/*_spec.json > /dev/null 2>&1; then
        tar -czf "$tmp/run.tgz" -C "$dest" .
        log "sending the run to continue, $(du -h "$tmp/run.tgz" | cut -f1)"
        colab upload -s "$session" "$tmp/run.tgz" /content/run.tgz || return 1
    fi
    "$PYTHON" -c 'import json, sys
fleet, arm, regime, commit, hours, runners, budget, learner, gpu, on_cpu, out = sys.argv[1:]
json.dump(dict(fleet=int(fleet), controller=arm, regime=regime, commit=commit,
               hours=float(hours), runners=int(runners), budget=int(budget) if budget else None,
               learner_cpus=int(learner) if learner else None, gpu=bool(gpu),
               batch_on_cpu=on_cpu == "1"),
          open(out, "w"))' "$fleet" "$arm" "$regime" "$commit" "$HOURS" "$RUNNERS" "$BUDGET" \
        "$LEARNER_CPUS" "$GPU" "$BATCH_ON_CPU" "$tmp/job.json"
    colab upload -s "$session" "$tmp/job.json" /content/job.json || return 1
    if [ -n "$PATCH" ]; then
        log "sending the patch $PATCH"
        colab upload -s "$session" "$PATCH" /content/code.patch || return 1
    fi
    colab upload -s "$session" "$HERE/train.py" /content/train.py || return 1

    remote "$session" <<'EOF'
import os, subprocess, sys
if os.path.exists("/content/state.txt") and open("/content/state.txt").read().split()[0] in (
        "installing", "warehouses", "training"):
    print("already running:", open("/content/state.txt").read().strip())
else:
    for name, target in (("warehouses.tgz", "/content/warehouses"), ("run.tgz", "/content/run")):
        path = f"/content/{name}"
        if os.path.exists(path):
            os.makedirs(target, exist_ok=True)
            subprocess.run(["tar", "-xzf", path, "-C", target], check=True)
            os.remove(path)
    subprocess.Popen(f"nohup {sys.executable} /content/train.py > /content/job.log 2>&1 &",
                     shell=True, start_new_session=True)
    print("started")
EOF
}

status() {
    local session=$1
    remote "$session" <<'EOF'
import subprocess
print(subprocess.run("cat /content/state.txt; tail -n 4 /content/job.log; echo ...; "
                     "tail -n 6 /content/run/train.log; uptime",
                     shell=True, capture_output=True, text=True).stdout)
EOF
    colab usage 2>&1 | tail -n 3
}

# Copies home what changed in the run since the last fetch, and the warehouse tables the
# machine built when this PC does not have them yet. Prints the machine's state last.
fetch() {
    local session=$1 fleet=$2 arm=$3 regime=$4
    local dest=$TRAINING/fleet_$fleet/$arm/$regime key tmp out
    tmp=$(mktemp -d)
    trap 'rm -rf "$tmp"' RETURN
    mkdir -p "$dest"
    key=$(pool_key "$fleet" "$arm") || return 1
    local want=True
    [ -f "$STORE/$key/manifest.json" ] && want=False
    # Only $key and $want come from this side. The stamp is set to the time before the search,
    # so a file written during the search is fetched again next time rather than missed.
    out=$(remote "$session" <<EOF
import os, subprocess, time
KEY, WANT_TABLES = "$key", $want
state = open("/content/state.txt").read().strip() if os.path.exists("/content/state.txt") else "none"
now = time.time()
stamp = "/content/fetched.stamp"
newer = ["-newer", stamp] if os.path.exists(stamp) else []
files = []
if os.path.isdir("/content/run"):
    files = subprocess.run(["find", ".", "-type", "f", *newer], cwd="/content/run",
                           capture_output=True, text=True).stdout.split()
if files:
    subprocess.run(["tar", "-czf", "/content/run_new.tgz", *files], cwd="/content/run", check=True)
    print("RUN", len(files))
# The mark moves to this time only once home has the files (commit_fetch below).
open("/content/fetch.pending", "w").write(str(now))
tables = f"/content/warehouses/{KEY}"
if WANT_TABLES and os.path.exists(f"{tables}/manifest.json") and state.split()[0] not in (
        "installing", "warehouses"):
    subprocess.run(["tar", "-czf", "/content/tables.tgz", "-C", "/content/warehouses", KEY],
                   check=True)
    print("TABLES")
print("STATE", state)
EOF
) || { log "fetch: no answer from $session"; printf '%s\n' "$out"; return 1; }
    if grep -q "^RUN" <<< "$out"; then
        if colab download -s "$session" /content/run_new.tgz "$tmp/run_new.tgz" > /dev/null \
            && tar -xzf "$tmp/run_new.tgz" -C "$dest"; then
            log "fetched $(grep '^RUN' <<< "$out" | cut -d' ' -f2) files into $dest"
            commit_fetch "$session"
        else
            log "fetch: the download failed, the same files come again next time"
        fi
    else
        commit_fetch "$session"
    fi
    if grep -q "^TABLES" <<< "$out"; then
        colab download -s "$session" /content/tables.tgz "$tmp/tables.tgz" > /dev/null \
            && tar -xzf "$tmp/tables.tgz" -C "$STORE" \
            && log "fetched the warehouse tables into $STORE/$key"
    fi
    grep "^STATE" <<< "$out" | tail -n 1
}

commit_fetch() {  # moves the machine's "fetched up to" mark to the time of the last fetch
    remote "$1" > /dev/null <<'EOF'
import os
if os.path.exists("/content/fetch.pending"):
    now = float(open("/content/fetch.pending").read())
    open("/content/fetched.stamp", "a").close()
    os.utime("/content/fetched.stamp", (now, now))
    os.remove("/content/fetch.pending")
EOF
}

# As bedtime.bash's finish_training: the progress log where the appendix figures read it.
finish() {
    local fleet=$1 arm=$2 regime=$3 dest=$TRAINING/fleet_$1/$2/$3
    [ -f "$dest/done" ] || return 0
    echo "$(date '+%Y-%m-%d %H:%M') colab, $RUNNERS runners" >> "$dest/done"
    if [ "$TRAINING" = "$HOME/thesis_runs/training" ]; then
        mkdir -p "$RESULTS/training/fleet_$fleet/${arm}_$regime"
        cp "$dest"/*_training_progress.jsonl \
            "$RESULTS/training/fleet_$fleet/${arm}_$regime/progress.jsonl" 2>/dev/null || true
    fi
}

iterations_at_home() {  # iterations_at_home FLEET ARM REGIME: lines of the progress log at home
    cat "$TRAINING/fleet_$1/$2/$3"/*_training_progress.jsonl 2>/dev/null | wc -l
}

# Continues a run on a fresh machine: stops what is left of the old one and starts again, which
# sends the run from home and resumes it from its latest checkpoint.
restart() {
    local session=$1
    colab stop -s "$session" > /dev/null 2>&1 || true
    unset COMMIT  # a continued run keeps the commit in its commit.txt
    start "$@"
}

# Fetches every INTERVAL until the run is done. A run stopped at HOURS (timeout's exit code
# 124), or whose machine stopped answering, is continued on a fresh machine, up to RESTARTS
# times. A restart that brought no new iteration home ends the watch, so a run that fails at
# once is not restarted again and again.
watch() {
    local session=$1 fleet=$2 arm=$3 regime=$4 line misses=0 restarts=0 before
    before=$(iterations_at_home "$fleet" "$arm" "$regime")
    while true; do
        line=$(fetch "$@" | tee /dev/stderr | grep '^STATE' | tail -n 1)
        case $line in
        "")
            misses=$((misses + 1))
            log "no state from $session ($misses of 3)"
            [ "$misses" -lt 3 ] && { sleep "$INTERVAL"; continue; }
            log "$session seems gone"
            ;;
        "STATE finished 0")
            log "$line, the run is done"
            finish "$fleet" "$arm" "$regime"
            [ "$STOP" = 1 ] && colab stop -s "$session"
            return 0
            ;;
        "STATE finished 124")
            log "$line, stopped at $HOURS h before its budget"
            ;;
        "STATE finished"* | "STATE failed"*)
            log "$line, stopped with an error, see train.log. Not continued."
            [ "$STOP" = 1 ] && colab stop -s "$session"
            return 1
            ;;
        *)
            misses=0
            sleep "$INTERVAL"
            continue
            ;;
        esac
        # Here the run stopped before its budget, or its machine is gone.
        local now
        now=$(iterations_at_home "$fleet" "$arm" "$regime")
        if [ "$restarts" -gt 0 ] && [ "$now" -le "$before" ]; then
            log "no new iteration since the last restart ($now), not continued"
            return 1
        fi
        if [ "$restarts" -ge "$RESTARTS" ]; then
            log "restarted $restarts times already, not continued"
            return 1
        fi
        restarts=$((restarts + 1)) before=$now misses=0
        log "continuing on a fresh machine, restart $restarts of $RESTARTS, $now iterations at home"
        restart "$@" || { log "the restart failed"; return 1; }
        sleep "$INTERVAL"
    done
}

# Bash reads a script as it runs it. Every branch ends in exit, so a watch that runs for days
# never reads on into this file after it was edited.
command=${1:-}
shift || true
case $command in
start | fetch | watch) [ $# -eq 4 ] || { sed -n 2,14p "$0"; exit 2; }; "$command" "$@"; exit ;;
status | stop) [ $# -eq 1 ] || { sed -n 2,14p "$0"; exit 2; }
    if [ "$command" = stop ]; then colab stop -s "$1"; else status "$1"; fi; exit ;;
*) sed -n 2,28p "$0"; exit 2 ;;
esac
exit
