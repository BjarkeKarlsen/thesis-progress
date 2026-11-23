#!/usr/bin/env bash
# Evaluate trained runs on one Colab machine, all at once, from this PC (eval.py does the work).
#
#   colab_eval.bash start SESSION RUN...   open the session, send the runs, start the evaluation
#   colab_eval.bash fetch SESSION          copy the evaluations home, print the machine's state
#   colab_eval.bash watch SESSION          fetch every INTERVAL until finished, then stop the session
#
# RUN is FLEET/ARM/REGIME, e.g. 8/section/fixed, the run in ~/thesis_runs/training. A run trained
# under fixed storage plays under fixed and demand ([A84]), the others under their own rule.
# MODES=demand (for one run) overrides that, to split a run's evaluation between two machines.
# OUTNAME names the result folder at home (evaluation_horizon10000_warmup5000; Regime 1 under
# congestion uses evaluation_congestion_horizon10000_warmup5000, beside the main one).
# WORKERS=4 plays each run's episodes 4 at a time (evaluate --workers, needs a COMMIT that has it,
# such as 02d407a). The warehouse tables of each run are sent along when this PC has them.
# Results land where the PC queue puts them,
# ~/thesis_runs/evaluation/fleet_<m>/<arm>/<regime>/evaluation_horizon10000_warmup5000, and the
# validation rows in the run's validation/ folder. Each session remembers its runs in
# ~/thesis_runs/colab_eval/<session>.runs.
# NEW is what `colab new` asks for (--high-mem, a CPU machine, by default; "--gpu L4" for 12 cores).
# PATCH is a diff applied on top of COMMIT, for uncommitted code (2026-11-22, the served counts [A96]).
# EXTRA are more evaluate options for every run, e.g. --chosen-only.
set -uo pipefail

HERE=$(cd "$(dirname "$0")" && pwd)
REPO=~/Documents/thesis/slap-mapd-coupling
TRAINING=$HOME/thesis_runs/training
EVALUATION=$HOME/thesis_runs/evaluation
BOOK=$HOME/thesis_runs/colab_eval
INTERVAL=${INTERVAL:-1800}
MODES=${MODES:-}
WORKERS=${WORKERS:-1}
NEW=${NEW:---high-mem}
PATCH=${PATCH:-}
EXTRA=${EXTRA:-}
OUTNAME=${OUTNAME:-evaluation_horizon10000_warmup5000}
STORE=$HOME/thesis_runs/warehouses
mkdir -p "$BOOK"

log() { echo "$(date '+%Y-%m-%d %H:%M') $*"; }
name_of() { echo "f${1//\//_}"; }   # 8/section/fixed -> f8_section_fixed

remote() {
    local session=$1 code out try
    code=$(cat)
    for try in 1 2 3; do
        out=$(printf '%s\n' "$code" | timeout 900 colab exec -s "$session" 2>&1)
        grep -q "Connection was lost" <<< "$out" || { printf '%s\n' "$out"; return 0; }
        log "connection lost, try $try of 3" >&2; sleep 20
    done
    printf '%s\n' "$out"; return 1
}

start() {
    local session=$1; shift
    local tmp runs_json="" commit r name modes
    tmp=$(mktemp -d)
    git -C "$REPO" fetch -q origin main
    commit=${COMMIT:-$(git -C "$REPO" rev-parse origin/main)}
    if ! colab sessions 2>/dev/null | grep -q "^\[$session\] "; then
        log "opening session $session"
        colab new -s "$session" $NEW || return 1
    fi
    remote "$session" <<< 'import os; os.makedirs("/content/in", exist_ok=True)' > /dev/null
    : > "$BOOK/$session.runs"
    for r in "$@"; do
        local rd=$TRAINING/fleet_${r%%/*}/${r#*/}
        [ -f "$rd/done" ] || { log "$r is not trained, left out"; continue; }
        name=$(name_of "$r")
        if [ -n "$MODES" ]; then modes=$MODES
        elif [ "${r##*/}" = fixed ]; then modes="fixed demand"
        else modes=${r##*/}; fi
        tar -czf "$tmp/$name.tgz" -C "$rd" --exclude=./train.log .
        key=$(cd "$REPO" && PYTHONPATH=src ~/.venvs/rl/bin/python -c "
import glob, sys
from pathlib import Path
from slap_mapd_coupling.training.spec import load_spec
from slap_mapd_coupling.training.warehouses import pool_key
print(pool_key(load_spec(Path(glob.glob(sys.argv[1] + '/*_spec.json')[0]))))" "$rd" 2>/dev/null | tail -1)
        if [ -n "$key" ] && [ -f "$STORE/$key/manifest.json" ] && [ ! -f "$tmp/tables_$key.tgz" ]; then
            tar -czf "$tmp/tables_$key.tgz" -C "$STORE" "$key"
            log "sending the tables $key ($(du -h "$tmp/tables_$key.tgz" | cut -f1))"
            colab upload -s "$session" "$tmp/tables_$key.tgz" "/content/in/tables_$key.tgz" > /dev/null || return 1
        fi
        log "sending $r ($(du -h "$tmp/$name.tgz" | cut -f1)), plays under $modes"
        colab upload -s "$session" "$tmp/$name.tgz" "/content/in/$name.tgz" > /dev/null || return 1
        echo "$r $name $OUTNAME" >> "$BOOK/$session.runs"
        runs_json+="{\"name\": \"$name\", \"workers\": $WORKERS, \"modes\": [$(printf '"%s",' $modes | sed 's/,$//')]},"
    done
    local extra_json=""
    [ -n "$EXTRA" ] && extra_json=$(printf '"%s",' $EXTRA | sed 's/,$//')
    echo "{\"commit\": \"$commit\", \"extra\": [$extra_json], \"runs\": [${runs_json%,}]}" > "$tmp/eval_job.json"
    if [ -n "$PATCH" ]; then
        colab upload -s "$session" "$PATCH" /content/code.patch > /dev/null || return 1
    fi
    colab upload -s "$session" "$tmp/eval_job.json" /content/eval_job.json > /dev/null || return 1
    colab upload -s "$session" "$HERE/eval.py" /content/eval.py > /dev/null || return 1
    remote "$session" <<'EOF'
import os, subprocess, sys
if os.path.exists("/content/state.txt") and open("/content/state.txt").read().split()[0] in (
        "installing", "warehouses", "evaluating"):
    print("already running:", open("/content/state.txt").read().strip())
else:
    subprocess.Popen(f"nohup {sys.executable} /content/eval.py > /content/job.log 2>&1 &",
                     shell=True, start_new_session=True)
    print("started")
EOF
    rm -rf "$tmp"
}

fetch() {
    local session=$1 tmp out r name dest
    tmp=$(mktemp -d)
    out=$(remote "$session" <<'EOF'
import os, subprocess
state = open("/content/state.txt").read().strip() if os.path.exists("/content/state.txt") else "none"
if os.path.isdir("/content/evals"):
    subprocess.run("tar -czf /content/evals.tgz evals $(cd /content && ls -d runs/*/validation 2>/dev/null)",
                   shell=True, cwd="/content", check=True)
    print("EVALS")
print("STATE", state)
EOF
) || { log "fetch: no answer from $session"; return 1; }
    if grep -q "^EVALS" <<< "$out" \
        && colab download -s "$session" /content/evals.tgz "$tmp/evals.tgz" > /dev/null \
        && tar -xzf "$tmp/evals.tgz" -C "$tmp"; then
        while read -r r name outname; do
            dest=$EVALUATION/fleet_${r%%/*}/${r#*/}/${outname:-evaluation_horizon10000_warmup5000}
            if [ -d "$tmp/evals/$name" ]; then
                mkdir -p "$dest"; cp -r "$tmp/evals/$name/." "$dest/"
                log "$r: $(cat "$dest/test.jsonl" 2>/dev/null | wc -l) test rows$([ -f "$dest/done" ] && echo ', done')"
            fi
            local rd=$TRAINING/fleet_${r%%/*}/${r#*/}
            [ -d "$tmp/runs/$name/validation" ] && mkdir -p "$rd/validation" \
                && cp -rn "$tmp/runs/$name/validation/." "$rd/validation/"
        done < "$BOOK/$session.runs"
    fi
    rm -rf "$tmp"
    grep "^STATE" <<< "$out" | tail -n 1
}

watch() {
    local session=$1 line misses=0
    while true; do
        line=$(fetch "$session" | tee /dev/stderr | grep '^STATE' | tail -n 1)
        case $line in
        "STATE finished"* | "STATE failed"*)
            log "$line"; colab stop -s "$session"; return 0 ;;
        "")
            misses=$((misses + 1)); log "no state from $session ($misses of 3)"
            [ "$misses" -ge 3 ] && { log "$session seems gone"; return 1; } ;;
        *) misses=0 ;;
        esac
        sleep "$INTERVAL"
    done
}

# Bash reads a script as it runs it, so every branch ends in exit.
command=${1:-}
shift || true
case $command in
start) [ $# -ge 2 ] || { sed -n 2,16p "$0"; exit 2; }; start "$@"; exit ;;
fetch | watch) [ $# -eq 1 ] || { sed -n 2,16p "$0"; exit 2; }; "$command" "$@"; exit ;;
*) sed -n 2,16p "$0"; exit 2 ;;
esac
exit
