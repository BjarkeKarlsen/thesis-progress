# H. Evaluation horizon and stall length

**Answers.** Where the backlog settles (the warm-up) and the horizon at which the paired gain of demand
over fixed stops moving.
**Fills.** `fig:app:horizontrace`, `fig:app:horizongain`, `tab:app:horizon`. The stall length reads
`longest_stand_still` from `../E_load/`.
**Run.** 2026-10-24, each fleet at its main load, Token Passing. The demand ranking turns once every
|K| / shift × rotation period = 100 / 5 × 200 = 4000 steps.

| folder | what |
|---|---|
| `traces/` | 3 seeds of 4000 steps under fixed storage, with a trace per seed (`traces/traces/`) |
| `trace_seed<k>.jsonl` | the same traces, copied where `appendix_measures.py` reads them |
| `h<T>/` | 20 seeds at horizon T, fixed and demand storage |
| `load_sweep.jsonl` | every `h<T>/load_sweep.jsonl` in one file |

## Commands, per fleet m, with LOAD the fleet's main load

    $PY scripts/sweep/load_sweep.py --config configs/fleet_$m/decentralised.yaml --rates $LOAD \
        --seeds 3 --trace-seeds 3 --horizon 4000 --out $R/H_horizon/fleet_$m/traces
    for T in 1000 1500 2000 3000 4000; do
        $PY scripts/sweep/load_sweep.py --config configs/fleet_$m/decentralised.yaml --rates $LOAD \
            --seeds 20 --storage-modes fixed demand --horizon $T --out $R/H_horizon/fleet_$m/h$T
    done
    k=0; for t in $R/H_horizon/fleet_$m/traces/traces/fixed_*.jsonl; do
        cp $t $R/H_horizon/fleet_$m/trace_seed$k.jsonl; k=$((k + 1)); done
    cat $R/H_horizon/fleet_$m/h*/load_sweep.jsonl > $R/H_horizon/fleet_$m/load_sweep.jsonl
