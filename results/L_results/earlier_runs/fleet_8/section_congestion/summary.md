# Test results, fleet 8, section, trained under congestion storage

Mean and 95 % interval over the 20 test seeds, 10000 steps with a 5000-step warm-up. The chosen policy is the result, the last checkpoint a check. The paired gain between storage rules is in `evaluate_summary.md` and the fleet's `comparison.md`.

| measure | chosen (checkpoint_000025) under congestion | last (checkpoint_000027) under congestion |
|---|---|---|
| throughput, tasks per step | 0.116 [0.097, 0.135] | 0.088 [0.072, 0.104] |
| share of seeds that keep up | 0.650 [0.421, 0.879] | 0.300 [0.080, 0.520] |
| pick service time, steps | 833.281 [449.429, 1217.132] | 1605.574 [1165.199, 2045.949] |
| wait before an agent takes it | 777.097 [399.711, 1154.482] | 1539.501 [1104.004, 1974.998] |
| travel | 43.840 [38.580, 49.100] | 51.013 [46.049, 55.977] |
| blocked | 12.343 [9.820, 14.866] | 15.060 [12.712, 17.408] |
| order completion, steps | 1439.579 [802.688, 2076.471] | 2730.713 [1873.501, 3587.925] |
| put-away service time | 860.874 [482.196, 1239.553] | 1642.755 [1208.066, 2077.444] |
| crowding | 0.107 [0.092, 0.122] | 0.088 [0.078, 0.098] |
| longest stretch with no task done | 80.850 [57.650, 104.050] | 51.200 [41.632, 60.768] |
| longest time two agents held a task at once | 182.900 [143.310, 222.490] | 192.600 [157.428, 227.772] |
| decision runtime, s | 0.033 [0.032, 0.033] | 0.032 [0.032, 0.032] |
| seeds with two agents holding a task 500 steps or more | 0 | 0 |
| seeds with two agents holding a task 1250 steps or more | 0 | 0 |
