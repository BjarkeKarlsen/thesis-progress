# Test results, fleet 16, centralised, trained under congestion storage

Mean and 95 % interval over the 20 test seeds, 10000 steps with a 5000-step warm-up. The chosen policy is the result, the last checkpoint a check. The paired gain between storage rules is in `evaluate_summary.md` and the fleet's `comparison.md`.

| measure | chosen (checkpoint_000015) under congestion | last (checkpoint_000027) under congestion |
|---|---|---|
| throughput, tasks per step | 0.058 [0.036, 0.080] | 0.000 [0.000, 0.000] |
| share of seeds that keep up | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| pick service time, steps | 3350.211 [2869.823, 3830.600] | n/a |
| wait before an agent takes it | 3263.149 [2783.578, 3742.720] | n/a |
| travel | 71.359 [67.445, 75.272] | n/a |
| blocked | 15.704 [14.473, 16.935] | n/a |
| order completion, steps | 3487.337 [-13750.707, 20725.380] | n/a |
| put-away service time | 3354.579 [2872.678, 3836.480] | n/a |
| crowding | 0.114 [0.099, 0.130] | 0.079 [0.074, 0.084] |
| longest stretch with no task done | 53.850 [39.062, 68.638] | 62.650 [56.587, 68.713] |
| longest time two agents held a task at once | 335.150 [264.012, 406.288] | 453.400 [425.440, 481.360] |
| decision runtime, s | 0.186 [0.174, 0.198] | 0.167 [0.161, 0.172] |
| seeds with two agents holding a task 500 steps or more | 2 | 4 |
| seeds with two agents holding a task 1250 steps or more | 0 | 0 |
