# Test results, fleet 16, centralised, trained under demand storage

Mean and 95 % interval over the 20 test seeds, 10000 steps with a 5000-step warm-up. The chosen policy is the result, the last checkpoint a check. The paired gain between storage rules is in `evaluate_summary.md` and the fleet's `comparison.md`.

| measure | chosen (checkpoint_000023) under demand | last (checkpoint_000027) under demand |
|---|---|---|
| throughput, tasks per step | 0.026 [0.011, 0.041] | 0.010 [0.000, 0.020] |
| share of seeds that keep up | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| pick service time, steps | 3824.379 [3363.787, 4284.971] | 4301.762 [3700.376, 4903.149] |
| wait before an agent takes it | 3731.124 [3270.774, 4191.474] | 4209.453 [3602.212, 4816.693] |
| travel | 70.654 [65.924, 75.385] | 67.661 [57.786, 77.535] |
| blocked | 22.601 [20.482, 24.720] | 24.649 [20.258, 29.041] |
| order completion, steps | 4363.143 | n/a |
| put-away service time | 3833.430 [3376.579, 4290.281] | 4293.670 [3691.934, 4895.407] |
| crowding | 0.131 [0.110, 0.152] | 0.122 [0.106, 0.138] |
| longest stretch with no task done | 75.150 [44.243, 106.057] | 60.500 [45.271, 75.729] |
| longest time two agents held a task at once | 480.050 [266.698, 693.402] | 465.300 [378.743, 551.857] |
| decision runtime, s | 0.186 [0.174, 0.198] | 0.169 [0.163, 0.175] |
| seeds with two agents holding a task 500 steps or more | 3 | 7 |
| seeds with two agents holding a task 1250 steps or more | 1 | 0 |
