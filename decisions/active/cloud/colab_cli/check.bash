#!/usr/bin/env bash
# One look at every Colab training run, read from the machines and from this PC.
#
#   check.bash              the four fleet 32 runs
#   check.bash FLEET        the runs of another fleet, named c<fleet>-<arm>-<regime> as below
#
# Per run: the machine's state, its last iteration, the CPUs Ray uses, the load, the time per
# iteration and the steps done (from the copy at home), the checkpoints at home, and whether its
# watcher is running. Then the units left.
set -uo pipefail

FLEET=${1:-32}
TRAINING=${TRAINING:-$HOME/thesis_runs/training}
PYTHON=~/.venvs/rl/bin/python
JOBS=("dec-fix decentralised fixed" "dec-dem decentralised demand"
      "sec-fix section fixed" "sec-dem section demand")

live=$(colab sessions 2>/dev/null)
for job in "${JOBS[@]}"; do
    set -- $job
    session=c$FLEET-$1 arm=$2 regime=$3
    home=$TRAINING/fleet_$FLEET/$arm/$regime
    echo "== $session ($arm, $regime)"

    if grep -q "^\[$session\] " <<< "$live"; then
        timeout 150 colab exec -s "$session" 2>&1 <<'EOF' | grep -E "^  " || echo "  machine: no answer"
import os, re, subprocess
def tail(path, pattern):
    try:
        lines = [l for l in open(path, errors="replace") if re.search(pattern, l)]
        return lines[-1].strip() if lines else "none yet"
    except OSError:
        return "none yet"
state = open("/content/state.txt").read().strip() if os.path.exists("/content/state.txt") else "none"
print("  machine state:", state)
print("  last iteration:", tail("/content/run/train.log", r"iter \d+/\d+")[:110])
print("  ray:", tail("/content/run/train.log", "Logical resource usage"))
print("  load:", open("/proc/loadavg").read().split()[0], "on", os.cpu_count(), "cores")
EOF
    else
        echo "  machine: not running"
    fi

    progress=$(ls "$home"/*_training_progress.jsonl 2>/dev/null | head -n 1)
    if [ -n "$progress" ]; then
        "$PYTHON" - "$progress" "$home" <<'EOF'
import json, sys
rows = [json.loads(line) for line in open(sys.argv[1]) if line.strip()]
spec = next(iter(__import__("glob").glob(sys.argv[2] + "/*_spec.json")), None)
budget = json.load(open(spec))["ppo"]["training_budget_env_steps"] if spec else None
if rows:
    last = rows[-1]
    # The rows hold no step count. An iteration is one episode per runner, 3 runners.
    steps = int(last.get("iteration", len(rows)) * 3 * last.get("episode_step", 0))
    times = [r["time_this_iter_s"] for r in rows[-5:] if "time_this_iter_s" in r]
    per = sum(times) / len(times) if times else None
    line = f"  at home: {len(rows)} iterations, {steps} of {budget} steps"
    if per:
        line += f", {per:.0f} s an iteration"
        if budget and steps:
            left = (budget - steps) / (steps / len(rows)) * per / 3600
            line += f", about {left:.1f} h to go"
    print(line)
EOF
    else
        echo "  at home: no progress yet"
    fi
    echo "  checkpoints at home: $(find "$home" -maxdepth 3 -type d -name 'checkpoint_*' 2>/dev/null | wc -l)$([ -f "$home/done" ] && echo ', done')"
    if pgrep -f "colab.bash watch $session " > /dev/null; then
        echo "  watcher: running"
    else
        echo "  watcher: NOT running"
    fi
done
echo "== units"
colab usage 2>&1 | tail -n 3 | sed 's/^/  /'
