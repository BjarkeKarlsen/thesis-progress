# F. Demand drift

**Answers.** How much the gain of demand over fixed storage depends on the demand settings.
**Fills.** `app:demand:sweep` and `fig:app:demandsweep` of Appendix F, and the findings behind
`app:demand:workstation` and `app:demand:conclusion` (see the findings below).
**Settings file.** `configs/step12/fleet_<m>.yaml`, copied as `config.yaml` into every folder. Setup in
`../README.md`.

## Commands, per fleet m

Each runs at the fleet's main load from `../E_load/fleet_<m>/capacity.json` (0.105, 0.15, 0.18 and 0.24 for
8, 16, 32 and 64 agents), under fixed and demand storage, one setting varied at a time:

    $PY scripts/sweep/load_sweep.py --config configs/step12/fleet_$m.yaml --rates $LOAD --seeds 20 \
        --storage-modes fixed demand --vary $SETTING --values $VALUES \
        --horizon 10000 --warmup 5000 --out $R/F_demand/fleet_$m/$SETTING

| folder | `$SETTING` | `$VALUES` | thesis value |
|---|---|---|---|
| `demand.skew` | `demand.skew` | `0.5 1.0 1.5` | 1 |
| `demand.rotation_period` | `demand.rotation_period` | `100 200 400` | 200 |
| `demand.rotation_share` | `demand.rotation_share` | `0.025 0.05 0.1` | 0.05 |

## Findings

- **The gain holds at every value.** Demand storage shortens a pick against fixed storage by 9, 9, 5 and
  10 % at 8, 16, 32 and 64 agents at the thesis values, with 16 to 19 of 20 seeds agreeing, and by 3 to
  13 % over the whole range. Every seed keeps up.
- **The skew matters most.** At a skew of 1.5 the popular SKUs run out. At 64 agents 28 % of orders wait
  for stock, against 7 % at a skew of 1.
- **The drift period and step hardly matter.** They move the gain by a few percent, with no pattern shared
  by the fleets.
- **The drift was not 4000 steps at 16 and 32 agents.** With 30 and 50 SKUs, 5 % rounds to 2 SKUs, so the
  ranking went round in 3000 and 5000 steps. At 8 agents, steps of 2.5 % and 5 % both round to one SKU
  and gave the same run. So the SKU count is now a multiple of 20.
- **A random workstation per order left storage no target.** The shelves the rule ranked best were about
  3 steps from their nearest workstation, but 11, 16, 24 and 34 steps from the one an order used (an average
  shelf 12.5, 17, 25 and 35). So each SKU now belongs to one workstation's section (D29, `[A76]`).
- **Every order had one line**, since the settings file set none. The next run has 5 lines per order.
