systemd-inhibit --what=sleep:idle:handle-lid-switch --who="rllib-training"   --why="Long RL training runs" bash -c '
for ex in 04_decentralised_training 02_centralised_fixed 03_section_based; do
  ~/.venvs/rl/bin/python examples/$ex.py --budget-env-steps=50000 --eval-seeds=3 --env-runners=7 --gpu 2>&1 | tee run_$ex.log
done'