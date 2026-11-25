# Token Passing on the test seeds, 8 to 64 agents

Token Passing at each fleet's main load (arrival rate 0.09, 0.18, 0.3 and 0.6 per step at 8, 16, 32 and 64 agents), fixed, demand and
congestion-aware storage, the 20 test seeds 200000 to 200019, 10000 steps with 5000 warm-up. Source of
`tab:exp:rq1` and `fig:exp:rq4` ([A142]). Drawn by `scripts/images/tp_fleet.py`.

- fleet_8: `~/thesis_runs/tp_testseeds8_2026-11-17`
- fleet_16: `~/thesis_runs/tp_testseeds_2026-11-16`
- fleet_32, fleet_64: `~/thesis_runs/tp_testseeds3264_2026-11-25` (Lenovo, main bdfda94 + PR #216, so the rows
  carry `longest_pair_stand_still`)
