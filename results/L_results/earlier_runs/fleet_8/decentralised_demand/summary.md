# Test results, fleet 8, decentralised, trained under demand storage

Mean and 95 % interval over the 20 test seeds, 10000 steps with a 5000-step warm-up. The chosen policy is the result, the last checkpoint a check. The paired gain between storage rules is in `evaluate_summary.md` and the fleet's `comparison.md`.

| measure | chosen (checkpoint_000016) under demand | last (checkpoint_000027) under demand |
|---|---|---|
| throughput, tasks per step | 0.103 [0.078, 0.128] | 0.102 [0.084, 0.120] |
| share of seeds that keep up | 0.500 [0.260, 0.740] | 0.400 [0.165, 0.635] |
| pick service time, steps | 623.695 [248.466, 998.923] | 1122.270 [750.661, 1493.879] |
| wait before an agent takes it | 572.290 [205.960, 938.620] | 1064.045 [696.984, 1431.106] |
| travel | 36.698 [31.100, 42.296] | 39.180 [34.891, 43.470] |
| blocked | 14.706 [10.559, 18.853] | 19.045 [15.628, 22.462] |
| order completion, steps | 1215.005 [481.586, 1948.425] | 1879.412 [1301.722, 2457.102] |
| put-away service time | 659.280 [289.964, 1028.596] | 1159.415 [796.202, 1522.628] |
| crowding | 0.133 [0.112, 0.154] | 0.100 [0.089, 0.110] |
| longest stretch with no task done | 467.750 [-18.282, 953.782] | 116.600 [74.231, 158.969] |
| longest time two agents held a task at once | 921.450 [-30.534, 1873.434] | 355.200 [186.019, 524.381] |
| decision runtime, s | 0.010 [0.010, 0.010] | 0.010 [0.010, 0.011] |
| seeds with two agents holding a task 500 steps or more | 5 | 3 |
| seeds with two agents holding a task 1250 steps or more | 2 | 1 |
