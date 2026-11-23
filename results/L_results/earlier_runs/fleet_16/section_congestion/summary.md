# Test results, fleet 16, section, trained under congestion storage

Mean and 95 % interval over the 20 test seeds, 10000 steps with a 5000-step warm-up. The chosen policy is the result, the last checkpoint a check. The paired gain between storage rules is in `evaluate_summary.md` and the fleet's `comparison.md`.

| measure | chosen (checkpoint_000027) under congestion | last (checkpoint_000027) under congestion |
|---|---|---|
| throughput, tasks per step | 0.121 [0.086, 0.155] | 0.121 [0.086, 0.155] |
| share of seeds that keep up | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| pick service time, steps | 2168.011 [1647.933, 2688.089] | 2168.011 [1647.933, 2688.089] |
| wait before an agent takes it | 2096.072 [1579.123, 2613.022] | 2096.072 [1579.123, 2613.022] |
| travel | 58.519 [53.493, 63.546] | 58.519 [53.493, 63.546] |
| blocked | 13.420 [11.909, 14.930] | 13.420 [11.909, 14.930] |
| order completion, steps | 3348.844 [2440.855, 4256.833] | 3348.844 [2440.855, 4256.833] |
| put-away service time | 2187.997 [1669.763, 2706.231] | 2187.997 [1669.763, 2706.231] |
| crowding | 0.132 [0.114, 0.149] | 0.132 [0.114, 0.149] |
| longest stretch with no task done | 49.000 [28.162, 69.838] | 49.000 [28.162, 69.838] |
| longest time two agents held a task at once | 340.850 [254.814, 426.886] | 340.850 [254.814, 426.886] |
| decision runtime, s | 0.101 [0.094, 0.107] | 0.089 [0.083, 0.094] |
| seeds with two agents holding a task 500 steps or more | 4 | 4 |
| seeds with two agents holding a task 1250 steps or more | 0 | 0 |
