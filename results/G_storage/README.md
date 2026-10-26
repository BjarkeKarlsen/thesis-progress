# G. Storage rule values

**Answers.** What the storage period Δ, the congestion weight β, the stock margin ε and the shelf
capacity do to the gain, its put-away cost and the check, so each value can be given a reason.
**Fills.** `app:cal:period` (`fig:app:storageperiod`), `app:cal:beta` (`fig:app:storagebeta`),
`app:cal:margin`, `app:storage:shelfcap` (`tab:app:shelfcap`).
**Run.** 2026-10-24, 20 seeds per value, each fleet at its main load (`../E_load/`), T = 2000, Token Passing.

| folder | rules | values |
|---|---|---|
| `storage_rule.epoch_length` | fixed, demand, congestion | 50 100 200 400 |
| `storage_rule.congestion_weight` | congestion | 0.0 0.5 1.0 2.0 3.0 4.0 |
| `arrival.margin` | fixed, demand | 0.25 0.5 1.0 1.5 2.0 |
| `shelf_capacity` | fixed, demand, congestion | 8: 260 300 400 600, 16: 170 200 300 400, 32: 160 200 300 400, 64: 140 200 300 400 |

β has no fixed rows of its own. Its reference is the fixed rows of `storage_rule.epoch_length` at Δ = 100.

## Commands, per fleet m, with LOAD the fleet's main load

    for s in "storage_rule.epoch_length|fixed demand congestion|50 100 200 400" \
             "storage_rule.congestion_weight|congestion|0.0 0.5 1.0 2.0 3.0 4.0" \
             "arrival.margin|fixed demand|0.25 0.5 1.0 1.5 2.0"; do
        IFS='|' read -r setting modes values <<< "$s"
        mkdir -p $R/G_storage/fleet_$m/$setting
        cp configs/fleet_$m/decentralised.yaml $R/G_storage/fleet_$m/$setting/config.yaml
        $PY scripts/sweep/load_sweep.py --config configs/fleet_$m/decentralised.yaml --rates $LOAD \
            --seeds 20 --storage-modes $modes --vary $setting --values $values \
            --out $R/G_storage/fleet_$m/$setting
    done

The shelf capacity, with CAPS the fleet's values from the table:

    $PY scripts/sweep/load_sweep.py --config configs/fleet_$m/decentralised.yaml --rates $LOAD \
        --seeds 20 --storage-modes fixed demand congestion \
        --vary storage.vertex_capacity --values $CAPS --out $R/G_storage/fleet_$m/shelf_capacity
