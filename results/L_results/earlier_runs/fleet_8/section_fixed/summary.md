# Test results, fleet 8, section, trained under fixed storage

Mean and 95 % interval over the 20 test seeds, 10000 steps with a 5000-step warm-up. The chosen policy is the result, the last checkpoint a check. The paired gain between storage rules is in `evaluate_summary.md` and the fleet's `comparison.md`.

| measure | chosen (checkpoint_000027) under fixed | chosen (checkpoint_000027) under demand | last (checkpoint_000027) under fixed | last (checkpoint_000027) under demand |
|---|---|---|---|---|
| throughput, tasks per step | 0.112 [0.097, 0.128] | 0.112 [0.095, 0.128] | 0.112 [0.097, 0.128] | 0.112 [0.095, 0.128] |
| share of seeds that keep up | 0.600 [0.365, 0.835] | 0.500 [0.260, 0.740] | 0.600 [0.365, 0.835] | 0.500 [0.260, 0.740] |
| pick service time, steps | 736.116 [427.154, 1045.079] | 878.015 [575.321, 1180.710] | 736.116 [427.154, 1045.079] | 878.015 [575.321, 1180.710] |
| wait before an agent takes it | 679.645 [375.532, 983.759] | 819.026 [520.210, 1117.842] | 679.645 [375.532, 983.759] | 819.026 [520.210, 1117.842] |
| travel | 42.291 [38.285, 46.297] | 43.103 [39.411, 46.795] | 42.291 [38.285, 46.297] | 43.103 [39.411, 46.795] |
| blocked | 14.180 [12.036, 16.324] | 15.887 [13.831, 17.942] | 14.180 [12.036, 16.324] | 15.887 [13.831, 17.942] |
| order completion, steps | 1462.881 [839.061, 2086.702] | 1573.082 [1069.736, 2076.428] | 1462.881 [839.061, 2086.702] | 1573.082 [1069.736, 2076.428] |
| put-away service time | 764.238 [458.156, 1070.320] | 908.633 [612.600, 1204.667] | 764.238 [458.156, 1070.320] | 908.633 [612.600, 1204.667] |
| crowding | 0.096 [0.081, 0.111] | 0.109 [0.096, 0.123] | 0.096 [0.081, 0.111] | 0.109 [0.096, 0.123] |
| longest stretch with no task done | 78.650 [54.439, 102.861] | 86.900 [55.347, 118.453] | 78.650 [54.439, 102.861] | 86.900 [55.347, 118.453] |
| longest time two agents held a task at once | 235.700 [109.367, 362.033] | 215.100 [163.092, 267.108] | 235.700 [109.367, 362.033] | 215.100 [163.092, 267.108] |
| decision runtime, s | 0.024 [0.024, 0.024] | 0.024 [0.023, 0.024] | 0.024 [0.023, 0.024] | 0.024 [0.024, 0.025] |
| seeds with two agents holding a task 500 steps or more | 1 | 1 | 1 | 1 |
| seeds with two agents holding a task 1250 steps or more | 1 | 0 | 1 | 0 |
