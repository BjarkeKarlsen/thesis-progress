# Test results, fleet 16, section, trained under demand storage

Mean and 95 % interval over the 20 test seeds, 10000 steps with a 5000-step warm-up. The chosen policy is the result, the last checkpoint a check. The paired gain between storage rules is in `evaluate_summary.md` and the fleet's `comparison.md`.

| measure | chosen (checkpoint_000025) under demand | last (checkpoint_000027) under demand |
|---|---|---|
| throughput, tasks per step | 0.055 [0.031, 0.080] | 0.039 [0.020, 0.059] |
| share of seeds that keep up | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| pick service time, steps | 3236.919 [2701.056, 3772.781] | 3556.217 [3051.451, 4060.982] |
| wait before an agent takes it | 3151.911 [2618.389, 3685.433] | 3468.331 [2966.967, 3969.695] |
| travel | 59.271 [54.077, 64.464] | 61.601 [55.928, 67.274] |
| blocked | 25.737 [22.950, 28.524] | 26.284 [22.789, 29.779] |
| order completion, steps | 3698.918 [1561.090, 5836.745] | 4703.400 [4470.258, 4936.542] |
| put-away service time | 3239.508 [2703.626, 3775.389] | 3573.988 [3071.061, 4076.915] |
| crowding | 0.159 [0.133, 0.185] | 0.108 [0.099, 0.118] |
| longest stretch with no task done | 75.000 [47.454, 102.546] | 49.600 [40.205, 58.995] |
| longest time two agents held a task at once | 743.500 [374.758, 1112.242] | 471.300 [372.458, 570.142] |
| decision runtime, s | 0.090 [0.086, 0.094] | 0.093 [0.087, 0.098] |
| seeds with two agents holding a task 500 steps or more | 8 | 6 |
| seeds with two agents holding a task 1250 steps or more | 4 | 0 |
