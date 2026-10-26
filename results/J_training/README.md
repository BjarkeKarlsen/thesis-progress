# J. Model and training (and I, the reward terms)

**Answers.** Whether the decentralised router learns at each fleet's main load within the budget, and
what each reward term contributes. No checkpoint is chosen yet by [A60] (M5 of
`../../decisions/active/measures_plan.md`), so nothing here is a test result.
**Fills.** `fig:app:rewardterms` of I, and later `fig:app:trainingcurves`, `tab:app:checkpoint` of J.
`fig:app:traininghealth` needs PPO losses, entropy and KL, which these logs do not have.
**Run.** 2026-10-24 to 25, the decentralised arm, 500 000 environment steps, checkpoint every 3 iterations,
under fixed storage (`fixed_only`) and demand storage (`matched`). Checkpoints are in
`~/thesis_runs/training/fleet_<m>/<regime>/`. Only `progress.jsonl` is copied here.

## Commands, per fleet m, with LOAD the fleet's main load

Fixed storage (6 env runners up to 16 agents, 4 from 32):

    mkdir -p /var/tmp/ray_q${m}f
    RAY_TMPDIR=/var/tmp/ray_q${m}f $PY -m slap_mapd_coupling.main train \
        --config configs/fleet_$m/decentralised.yaml --controller decentralised --regime fixed_only \
        --arrival-rate $LOAD --env-runners 6 --checkpoint-every 3 \
        --output ~/thesis_runs/training/fleet_$m/fixed_only

Demand storage. First write a config with `regime: matched` and `evaluation_storage_mode: demand` added to
`configs/fleet_$m/decentralised.yaml` as `~/thesis_runs/training/fleet_$m/matched/config.yaml`, then run the
command above with that config, `--regime matched`, `/var/tmp/ray_q${m}m` and the `matched` output folder.

A run that stopped continues from its latest checkpoint with
`$PY -m slap_mapd_coupling.main resume ~/thesis_runs/training/fleet_$m/<regime>`. Keep `RAY_TMPDIR` short
(38 characters at most). When a run is done, copy
`~/thesis_runs/training/fleet_$m/<regime>/decentralised_<regime>_training_progress.jsonl` to
`$R/J_training/fleet_$m/decentralised_<regime>/progress.jsonl`.
