# Test results, fleet 16, decentralised, with messages, trained under congestion storage

Mean and 95 % interval over the 20 test seeds, 10000 steps with a 5000-step warm-up. The chosen policy is the result, the last checkpoint a check. The paired gain between storage rules is in `evaluate_summary.md` and the fleet's `comparison.md`.

| measure | chosen (checkpoint_000013) under congestion | last (checkpoint_000027) under congestion |
|---|---|---|
| throughput, tasks per step | 0.004 [-0.002, 0.010] | 0.000 [0.000, 0.000] |
| share of seeds that keep up | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| pick service time, steps | 4273.692 [2458.946, 6088.438] | n/a |
| wait before an agent takes it | 4201.399 [2271.729, 6131.069] | n/a |
| travel | 54.827 [-17.551, 127.204] | n/a |
| blocked | 17.466 [-25.862, 60.795] | n/a |
| order completion, steps | n/a | n/a |
| put-away service time | 4457.939 [3369.457, 5546.422] | n/a |
| crowding | 0.171 [0.142, 0.200] | 0.115 [0.102, 0.128] |
| longest stretch with no task done | 303.750 [-61.429, 668.929] | 208.150 [160.985, 255.315] |
| longest time two agents held a task at once | 3401.950 [1985.402, 4818.498] | 3656.200 [2305.563, 5006.837] |
| decision runtime, s | 0.024 [0.023, 0.025] | 0.021 [0.020, 0.022] |
| seeds with two agents holding a task 500 steps or more | 18 | 20 |
| seeds with two agents holding a task 1250 steps or more | 14 | 18 |
