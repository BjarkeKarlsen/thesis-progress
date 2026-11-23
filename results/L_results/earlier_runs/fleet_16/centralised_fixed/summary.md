# Test results, fleet 16, centralised, trained under fixed storage

Mean and 95 % interval over the 20 test seeds, 10000 steps with a 5000-step warm-up. The chosen policy is the result, the last checkpoint a check. The paired gain between storage rules is in `evaluate_summary.md` and the fleet's `comparison.md`.

| measure | chosen (checkpoint_000021) under fixed | chosen (checkpoint_000021) under demand | last (checkpoint_000027) under fixed | last (checkpoint_000027) under demand |
|---|---|---|---|---|
| throughput, tasks per step | 0.036 [0.017, 0.055] | 0.035 [0.017, 0.054] | 0.001 [-0.001, 0.004] | 0.002 [-0.002, 0.005] |
| share of seeds that keep up | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| pick service time, steps | 3654.990 [3092.506, 4217.475] | 3592.747 [3109.851, 4075.642] | 4137.287 | 3926.221 |
| wait before an agent takes it | 3566.308 [3003.215, 4129.402] | 3501.993 [3020.535, 3983.452] | 4011.989 | 3800.049 |
| travel | 69.682 [64.642, 74.722] | 70.036 [64.632, 75.440] | 93.638 | 95.041 |
| blocked | 19.000 [16.465, 21.535] | 20.717 [17.879, 23.556] | 31.660 | 31.131 |
| order completion, steps | 2733.884 | 3688.923 | n/a | n/a |
| put-away service time | 3657.261 [3093.231, 4221.292] | 3614.531 [3124.470, 4104.591] | 4116.955 | 3948.875 |
| crowding | 0.139 [0.118, 0.160] | 0.149 [0.127, 0.172] | 0.082 [0.076, 0.089] | 0.086 [0.080, 0.091] |
| longest stretch with no task done | 68.050 [50.698, 85.402] | 82.550 [51.506, 113.594] | 55.300 [44.939, 65.661] | 51.250 [45.837, 56.663] |
| longest time two agents held a task at once | 461.150 [332.291, 590.009] | 476.250 [333.319, 619.181] | 417.100 [356.067, 478.133] | 418.450 [389.037, 447.863] |
| decision runtime, s | 0.201 [0.201, 0.202] | 0.201 [0.200, 0.202] | 0.203 [0.201, 0.204] | 0.378 [0.335, 0.421] |
| seeds with two agents holding a task 500 steps or more | 5 | 6 | 2 | 1 |
| seeds with two agents holding a task 1250 steps or more | 1 | 1 | 0 | 0 |
