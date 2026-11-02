# F. Demand drift

**Answers.** How much the gain of demand over fixed storage depends on the demand settings.
**Fills.** `app:demand:sweep` and `fig:app:demandsweep` of Appendix F, and the findings behind
`app:demand:workstation` and `app:demand:conclusion` (see the findings below).
**Settings file.** `configs/step12/fleet_<m>.yaml`, copied as `config.yaml` into every folder. Setup in
`../README.md`.

## Commands, per fleet m

Each runs at the fleet's main load from `../E_load/fleet_<m>/capacity.json` (0.09, 0.18, 0.3 and 0.6 for
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

- **The gain holds at every value.** At the thesis values demand storage shortens a pick against fixed
  storage by 10.9, 13.9, 13.2 and 10.2 % at 8, 16, 32 and 64 agents (paired by seed, standard error 1.3
  to 2.7), and by 9 to 15 % over the whole range. Every seed keeps up.
- **Storage now has a target.** Each SKU belongs to a section of 4 workstations (`[A76]`, `[A77]`), so
  demand storage cuts a pick's travel by 19 to 23 % (17.0 to 13.2 steps at 8 agents, 25.1 to 20.3 at
  64). In the first sweep, where an order went to any workstation, it cut travel by 9 to 11 %.
- **But travel is a small part of a pick.** A pick waits 4 to 7 times as long as it drives, mostly
  because another robot's path ends at its workstation (see `../E_load/README.md`). So a travel saving
  of a fifth gives a service time gain of 10 to 14 %.
- **The skew hardly matters now.** The gain moves by at most 3.5 points between 0.5 and 1.5 (it was the
  setting that mattered most in the first sweep, through stock running out). With the top-rank safety
  stock, 0.1 to 0.3 % of lines wait for stock at every value.
- **The drift period and share hardly matter.** They move the gain by 1 to 3 points, with no shared
  pattern.
- **One point is a repeat.** At 8 agents, with 20 SKUs, a drift share of 2.5 % and 5 % both round to one
  SKU, so the two runs are identical. At the other fleets the three shares give three different whole
  numbers of SKUs per step, as meant.

## The first sweep, for comparison (rows at `524ef5a`)

Each order went to a random workstation anywhere and had one line, Q = 30. The gain was 9, 9, 5 and 10 %.
The shelves demand storage ranked best were about 3 steps from their nearest workstation, but 11 to 34
steps from the one an order used, which led to the sections (D29, `[A76]`). At a skew of 1.5 up to 28 %
of orders waited for stock, which led to the top-rank safety stock (`[A75]`).
