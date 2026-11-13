# [A93] first look, 2026-11-13

The short tests that led to [A93] (congestion = the time picks stand still at each shelf). They ran
on run-time patches of `slap-mapd-coupling` main `faf9abc` (worktree `~/worktrees/congestion-fixes`),
before the rule was coded. The real rule is on `main` from `d204dbd`. These rows are evidence for the
decision, not results for the thesis. Rerun with the code on `main` for the numbers that go in.

## Rows

| file | what |
|---|---|
| `fleet8_decentralised.jsonl`, `fleet16_section.jsonl`, `fleet16_decentralised.jsonl`, `fleet32_decentralised.jsonl` | learned policies trained under demand, best checkpoint (8 dec ck24, 16 sec ck25, 16 dec ck23, 32 dec ck2), 5 test seeds, 4000 steps, 1000 left out. `variant` demand or shelfblock, `changes` "" or "pickb" (signal in the pick choice) |
| `tp_edge_variants_fleet8.jsonl` | Token Passing, fleet 8, load 0.09, 10 seeds, 10000/5000: the edge-signal variants (congestion as it was, demand_smooth, aisle, traffic, pressure, combo) |
| `tp_new_rule_fleet8.jsonl`, `tp_new_rule_fleet16_partial.jsonl` | Token Passing, demand against the new rule with (`shelfblock`) and without (`shelfblock_raw`) averaged demand, 20 seeds at fleet 8, fleet 16 not complete |
| `tp_model_changes_fleet8_partial.jsonl`, `learned_model_changes_fleet8_ck27_partial.jsonl` | least-busy workstation (`ws`), pick by expected waiting (`pick`), moving old stock (`reloc`), partial, last checkpoint |

The shelfblock variant in these rows kept one fifth of each new reading (an exponential average) and
averaged the demand numbers. The thesis and the code use the plain average of the last five
readings and do not average the demand numbers.

## Scripts

`scripts/`: `variants.py` and `model_changes.py` (the patches), the runners, and `compare.py`
(`python compare.py rows/fleet8_decentralised.jsonl`). They need `PYTHONPATH` on a
`slap-mapd-coupling` checkout at `faf9abc`, and `SHELF_SIGNAL=1` for the shelf signal.
