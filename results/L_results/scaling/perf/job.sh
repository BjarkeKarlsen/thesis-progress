#!/bin/bash
# One performance test episode, on the PC or the Lenovo (same script on both). Usage:
#   job.sh FLEET ARM SEED RUN_DIR CHECKPOINT  (RUN_DIR, CHECKPOINT relative to ~/thesis_runs)
# 10000 steps, 5000 warm-up, as the fleet 16 test rows, on the CPU (both machines alike), one
# thread. Every probe of a store prepares the same 20 test seeds (--pool-seeds). Writes
# rows/FLEET_ARM_SEED.jsonl and logs/FLEET_ARM_SEED.{log,exit} under $P.
m=$1 arm=$2 s=$3 R=$HOME/thesis_runs/$4 CK=$HOME/thesis_runs/$5
P=${P:-$HOME/thesis_runs/scaling_2026-11/perf}
W=${W:-$HOME/worktrees/main-bdfda94}  # main bdfda94 (#213 to #215, same decisions) from 2026-11-24; before: main-run 811b8f2, scaling-run
PY=${PY:-$HOME/.venvs/rl/bin/python}
cfg=$arm; [ $arm = decentralised_comm ] && cfg=decentralised
extra=""; [ $arm = section ] && extra="--sections $(( m == 8 ? 2 : 3 * m / 16 ))"
mkdir -p $P/rows $P/logs; rm -f $P/logs/${m}_${arm}_$s.exit
cd $W && env PYTHONPATH=src OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  SLAP_WAREHOUSE_STORE=$HOME/thesis_runs/warehouses RAY_TMPDIR=/var/tmp/ray_p$s \
  $PY -m slap_mapd_coupling.training.scaling_probe $R $CK --target configs/fleet_$m/$cfg.yaml $extra \
  --steps 10000 --warmup 5000 --seed $s --pool-seeds $(seq 200000 200019) \
  --output $P/rows/${m}_${arm}_$s.jsonl > $P/logs/${m}_${arm}_$s.log 2>&1
echo $? > $P/logs/${m}_${arm}_$s.exit
