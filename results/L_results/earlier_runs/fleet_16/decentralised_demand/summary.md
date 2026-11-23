# Test results, fleet 16, decentralised, trained under demand storage

Mean and 95 % interval over the 20 test seeds, 10000 steps with a 5000-step warm-up. The chosen policy is the result, the last checkpoint a check. The paired gain between storage rules is in `evaluate_summary.md` and the fleet's `comparison.md`.

| measure | chosen (checkpoint_000022) under demand | last (checkpoint_000027) under demand |
|---|---|---|
| throughput, tasks per step | 0.007 [-0.003, 0.016] | 0.004 [-0.003, 0.010] |
| share of seeds that keep up | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| pick service time, steps | 4120.494 [2554.497, 5686.491] | 4009.901 [-5778.044, 13797.846] |
| wait before an agent takes it | 4058.204 [2448.050, 5668.358] | 3907.657 [-5612.203, 13427.516] |
| travel | 48.084 [14.509, 81.659] | 67.598 [-86.357, 221.552] |
| blocked | 14.206 [-1.103, 29.515] | 34.646 [-79.485, 148.778] |
| order completion, steps | n/a | n/a |
| put-away service time | 4134.174 [2564.333, 5704.015] | 3956.789 [-5423.065, 13336.644] |
| crowding | 0.135 [0.118, 0.152] | 0.166 [0.144, 0.188] |
| longest stretch with no task done | 142.400 [78.617, 206.183] | 269.000 [45.031, 492.969] |
| longest time two agents held a task at once | 2214.750 [1214.683, 3214.817] | 3887.250 [2873.655, 4900.845] |
| decision runtime, s | 0.023 [0.021, 0.026] | 0.019 [0.018, 0.020] |
| seeds with two agents holding a task 500 steps or more | 20 | 20 |
| seeds with two agents holding a task 1250 steps or more | 8 | 19 |
