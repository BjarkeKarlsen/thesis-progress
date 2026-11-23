# Test results, fleet 8, centralised, trained under demand storage

Mean and 95 % interval over the 20 test seeds, 10000 steps with a 5000-step warm-up. The chosen policy is the result, the last checkpoint a check. The paired gain between storage rules is in `evaluate_summary.md` and the fleet's `comparison.md`.

| measure | chosen (checkpoint_000013) under demand | last (checkpoint_000027) under demand |
|---|---|---|
| throughput, tasks per step | 0.112 [0.099, 0.124] | 0.029 [0.018, 0.040] |
| share of seeds that keep up | 0.450 [0.211, 0.689] | 0.000 [0.000, 0.000] |
| pick service time, steps | 1053.306 [623.435, 1483.176] | 3610.746 [3123.490, 4098.001] |
| wait before an agent takes it | 997.907 [570.369, 1425.446] | 3527.491 [3039.173, 4015.809] |
| travel | 43.818 [40.884, 46.752] | 58.063 [54.272, 61.855] |
| blocked | 11.580 [10.357, 12.803] | 25.191 [23.496, 26.887] |
| order completion, steps | 1794.954 [1208.148, 2381.760] | 3267.130 [-11117.471, 17651.730] |
| put-away service time | 1094.678 [666.348, 1523.008] | 3646.901 [3164.068, 4129.734] |
| crowding | 0.104 [0.093, 0.116] | 0.082 [0.074, 0.089] |
| longest stretch with no task done | 53.700 [38.262, 69.138] | 56.800 [51.183, 62.417] |
| longest time two agents held a task at once | 160.300 [133.921, 186.679] | 209.800 [188.299, 231.301] |
| decision runtime, s | 0.040 [0.039, 0.040] | 0.039 [0.039, 0.039] |
| seeds with two agents holding a task 500 steps or more | 0 | 0 |
| seeds with two agents holding a task 1250 steps or more | 0 | 0 |
