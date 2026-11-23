# Test results, fleet 16, section, trained under fixed storage

Mean and 95 % interval over the 20 test seeds, 10000 steps with a 5000-step warm-up. The chosen policy is the result, the last checkpoint a check. The paired gain between storage rules is in `evaluate_summary.md` and the fleet's `comparison.md`.

| measure | chosen (checkpoint_000024) under fixed | chosen (checkpoint_000024) under demand | last (checkpoint_000027) under fixed | last (checkpoint_000027) under demand |
|---|---|---|---|---|
| throughput, tasks per step | 0.131 [0.087, 0.174] | 0.125 [0.084, 0.166] | 0.109 [0.073, 0.145] | 0.108 [0.073, 0.142] |
| share of seeds that keep up | 0.050 [-0.055, 0.155] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| pick service time, steps | 1377.494 [1047.781, 1707.207] | 1565.806 [1255.245, 1876.367] | 2302.228 [1703.117, 2901.340] | 2076.739 [1637.939, 2515.540] |
| wait before an agent takes it | 1310.829 [985.370, 1636.288] | 1499.438 [1191.539, 1807.337] | 2231.694 [1631.013, 2832.374] | 2005.111 [1569.727, 2440.495] |
| travel | 51.146 [46.643, 55.648] | 50.182 [46.616, 53.747] | 53.183 [46.760, 59.607] | 53.263 [49.219, 57.307] |
| blocked | 15.519 [13.468, 17.571] | 16.186 [14.443, 17.929] | 17.352 [13.627, 21.077] | 18.365 [16.305, 20.425] |
| order completion, steps | 2712.627 [2051.134, 3374.119] | 3123.735 [2475.851, 3771.619] | 2888.887 [1923.549, 3854.226] | 3261.673 [2377.594, 4145.751] |
| put-away service time | 1393.990 [1067.521, 1720.459] | 1585.635 [1277.910, 1893.360] | 2320.582 [1722.080, 2919.085] | 2098.248 [1662.601, 2533.895] |
| crowding | 0.194 [0.136, 0.252] | 0.196 [0.144, 0.249] | 0.127 [0.110, 0.144] | 0.136 [0.116, 0.156] |
| longest stretch with no task done | 212.800 [34.273, 391.327] | 310.650 [24.893, 596.407] | 80.300 [35.173, 125.427] | 58.300 [32.385, 84.215] |
| longest time two agents held a task at once | 1703.150 [583.158, 2823.142] | 1312.050 [267.029, 2357.071] | 445.950 [245.965, 645.935] | 494.100 [244.231, 743.969] |
| decision runtime, s | 0.088 [0.083, 0.092] | 0.095 [0.088, 0.102] | 0.100 [0.094, 0.106] | 0.097 [0.091, 0.102] |
| seeds with two agents holding a task 500 steps or more | 7 | 6 | 6 | 5 |
| seeds with two agents holding a task 1250 steps or more | 7 | 6 | 1 | 2 |
