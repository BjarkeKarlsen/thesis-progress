# Test results, fleet 8, decentralised, with messages, trained under fixed storage

Mean and 95 % interval over the 20 test seeds, 10000 steps with a 5000-step warm-up. The chosen policy is the result, the last checkpoint a check. The paired gain between storage rules is in `evaluate_summary.md` and the fleet's `comparison.md`.

| measure | chosen (checkpoint_000021) under fixed | chosen (checkpoint_000021) under demand | last (checkpoint_000027) under fixed | last (checkpoint_000027) under demand |
|---|---|---|---|---|
| throughput, tasks per step | 0.128 [0.118, 0.138] | 0.133 [0.122, 0.145] | 0.101 [0.078, 0.124] | 0.098 [0.074, 0.123] |
| share of seeds that keep up | 0.900 [0.756, 1.044] | 0.850 [0.679, 1.021] | 0.600 [0.365, 0.835] | 0.450 [0.211, 0.689] |
| pick service time, steps | 346.223 [50.283, 642.163] | 418.282 [93.426, 743.138] | 1121.030 [497.670, 1744.391] | 1418.932 [697.615, 2140.250] |
| wait before an agent takes it | 302.758 [10.527, 594.989] | 373.959 [52.676, 695.242] | 1056.640 [446.437, 1666.843] | 1359.831 [645.015, 2074.648] |
| travel | 35.269 [31.499, 39.039] | 35.696 [32.033, 39.360] | 43.628 [34.117, 53.139] | 40.187 [32.964, 47.410] |
| blocked | 8.196 [6.764, 9.627] | 8.627 [7.280, 9.974] | 20.762 [14.354, 27.170] | 18.914 [13.962, 23.867] |
| order completion, steps | 448.421 [158.705, 738.137] | 554.195 [265.911, 842.479] | 1092.992 [501.073, 1684.911] | 1231.350 [712.337, 1750.363] |
| put-away service time | 374.388 [78.190, 670.587] | 451.645 [126.299, 776.990] | 1151.419 [533.892, 1768.946] | 1455.331 [739.513, 2171.150] |
| crowding | 0.082 [0.071, 0.093] | 0.098 [0.086, 0.109] | 0.117 [0.095, 0.139] | 0.130 [0.110, 0.150] |
| longest stretch with no task done | 134.800 [103.530, 166.070] | 105.250 [75.613, 134.887] | 130.300 [86.738, 173.862] | 127.500 [82.857, 172.143] |
| longest time two agents held a task at once | 129.150 [104.931, 153.369] | 148.000 [125.149, 170.851] | 300.850 [186.973, 414.727] | 311.850 [222.568, 401.132] |
| decision runtime, s | 0.009 [0.009, 0.009] | 0.009 [0.009, 0.009] | 0.009 [0.008, 0.009] | 0.009 [0.009, 0.009] |
| seeds with two agents holding a task 500 steps or more | 0 | 0 | 3 | 6 |
| seeds with two agents holding a task 1250 steps or more | 0 | 0 | 0 | 0 |
