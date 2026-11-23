# Test results, fleet 8, decentralised, trained under congestion storage

Mean and 95 % interval over the 20 test seeds, 10000 steps with a 5000-step warm-up. The chosen policy is the result, the last checkpoint a check. The paired gain between storage rules is in `evaluate_summary.md` and the fleet's `comparison.md`.

| measure | chosen (checkpoint_000013) under congestion | last (checkpoint_000027) under congestion |
|---|---|---|
| throughput, tasks per step | 0.101 [0.073, 0.128] | 0.103 [0.084, 0.122] |
| share of seeds that keep up | 0.550 [0.311, 0.789] | 0.450 [0.211, 0.689] |
| pick service time, steps | 1097.346 [306.287, 1888.405] | 1312.101 [707.354, 1916.847] |
| wait before an agent takes it | 1038.925 [263.002, 1814.848] | 1252.169 [652.311, 1852.027] |
| travel | 42.893 [32.526, 53.261] | 44.716 [39.557, 49.875] |
| blocked | 15.528 [8.159, 22.897] | 15.215 [13.203, 17.228] |
| order completion, steps | 894.847 [309.901, 1479.792] | 1726.260 [1088.685, 2363.834] |
| put-away service time | 1108.554 [343.227, 1873.881] | 1339.768 [743.164, 1936.372] |
| crowding | 0.120 [0.097, 0.143] | 0.097 [0.085, 0.110] |
| longest stretch with no task done | 416.600 [-22.852, 856.052] | 138.300 [96.611, 179.989] |
| longest time two agents held a task at once | 613.450 [100.450, 1126.450] | 340.700 [209.022, 472.378] |
| decision runtime, s | 0.010 [0.009, 0.010] | 0.010 [0.010, 0.011] |
| seeds with two agents holding a task 500 steps or more | 6 | 2 |
| seeds with two agents holding a task 1250 steps or more | 1 | 1 |
