# F. Demand drift

**Answers.** Whether the gain of demand over fixed storage holds when the demand settings move. They are
fixed by the thesis ([A34]), so this is a robustness check, not a calibration.
**Fills.** `fig:app:demandsweep`, `app:demand:sweep`.
**Run.** 2026-10-24, 20 seeds per value, each fleet at its main load (`../E_load/`), T = 2000, Token
Passing, fixed and demand storage. The default value of each setting gives the same episodes in every folder.

## Commands, per fleet m, with LOAD the fleet's main load

    for s in "demand.skew 0.5 1.0 1.5" "demand.rotation_period 100 200 400" "demand.rotation_shift 2 5 10"; do
        set -- $s; setting=$1; shift
        mkdir -p $R/F_demand/fleet_$m/$setting
        cp configs/fleet_$m/decentralised.yaml $R/F_demand/fleet_$m/$setting/config.yaml
        $PY scripts/sweep/load_sweep.py --config configs/fleet_$m/decentralised.yaml --rates $LOAD \
            --seeds 20 --storage-modes fixed demand --vary $setting --values "$@" \
            --out $R/F_demand/fleet_$m/$setting
    done
