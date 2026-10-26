# E. Load and capacity

**Answers.** The capacity of each fleet under fixed storage, the highest arrival rate at which every seed
keeps up ([A59]), and the main load, 0.6 of it. Every other folder runs at these main loads.
**Fills.** `tab:app:capacity`, `fig:app:loadsweep`, `fig:app:loadvalidity`, `app:cal:load`, and
`fig:app:standstill` of H (the `longest_stand_still` field).
**Run.** 2026-10-24, 20 seeds per rate, T = 2000, Token Passing, fixed storage.

| fleet | capacity | first failing | main load |
|---|---|---|---|
| 8 | 0.2 | 0.225 | 0.12 |
| 16 | 0.2 | 0.25 | 0.12 |
| 32 | 0.6 | 0.7 | 0.36 |
| 64 | 0.5 | 0.6 | 0.3 |

Fleet 16's rows at 0.3 to 0.6 are 50-seed rows from before [A59], with no pick and put-away check.

## Commands, per fleet m

1. The grid of [A58], rates per agent 0.0125 to 0.1:

       $PY scripts/sweep/load_sweep.py --config configs/fleet_$m/decentralised.yaml --seeds 20 \
           --stop-when-overloaded --out $R/E_load/fleet_$m \
           --rates-per-agent 0.0125 0.025 0.0375 0.05 0.0625 0.075 0.0875 0.1

2. Rates where an earlier sweep put the capacity, if any (this run: 16 `0.25 0.3 0.35`, 32 `0.5 0.6 0.7`,
   64 `0.42 0.5 0.6 0.7`), with the same command and `--rates <rates>` in place of `--rates-per-agent`.
3. Twice, three rates evenly between the last passing rate and the first failing rate of `capacity.json`,
   with `--rates`. Stop when the two are a quarter of a grid step (0.0125 m / 4) apart.
4. The main load is `by_mode.fixed.main_load` in `$R/E_load/fleet_$m/capacity.json`.
