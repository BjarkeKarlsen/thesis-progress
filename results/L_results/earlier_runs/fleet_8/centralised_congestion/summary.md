# Test results, fleet 8, centralised, trained under congestion storage

Mean and 95 % interval over the 20 test seeds, 10000 steps with a 5000-step warm-up. The chosen policy is the result, the last checkpoint a check. The paired gain between storage rules is in `evaluate_summary.md` and the fleet's `comparison.md`.

| measure | chosen (checkpoint_000009) under congestion | last (checkpoint_000027) under congestion |
|---|---|---|
| throughput, tasks per step | 0.088 [0.074, 0.102] | 0.022 [0.012, 0.032] |
| share of seeds that keep up | 0.050 [-0.055, 0.155] | 0.000 [0.000, 0.000] |
| pick service time, steps | 1550.058 [1149.731, 1950.386] | 3751.343 [3278.360, 4224.326] |
| wait before an agent takes it | 1486.231 [1087.193, 1885.269] | 3661.085 [3183.441, 4138.728] |
| travel | 50.251 [46.841, 53.660] | 67.366 [59.131, 75.602] |
| blocked | 13.577 [11.907, 15.247] | 22.892 [19.678, 26.106] |
| order completion, steps | 2721.342 [2015.781, 3426.904] | 3369.000 |
| put-away service time | 1584.062 [1184.994, 1983.131] | 3710.362 [3242.445, 4178.279] |
| crowding | 0.091 [0.081, 0.102] | 0.069 [0.064, 0.074] |
| longest stretch with no task done | 46.150 [38.734, 53.566] | 62.100 [56.045, 68.155] |
| longest time two agents held a task at once | 183.500 [152.316, 214.684] | 220.000 [198.610, 241.390] |
| decision runtime, s | 0.045 [0.045, 0.046] | 0.044 [0.044, 0.045] |
| seeds with two agents holding a task 500 steps or more | 0 | 0 |
| seeds with two agents holding a task 1250 steps or more | 0 | 0 |
