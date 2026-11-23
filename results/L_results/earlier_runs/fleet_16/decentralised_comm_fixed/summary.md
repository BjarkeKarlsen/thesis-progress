# Test results, fleet 16, decentralised, with messages, trained under fixed storage

Mean and 95 % interval over the 20 test seeds, 10000 steps with a 5000-step warm-up. The chosen policy is the result, the last checkpoint a check. The paired gain between storage rules is in `evaluate_summary.md` and the fleet's `comparison.md`.

| measure | chosen (checkpoint_000015) under fixed | chosen (checkpoint_000015) under demand | last (checkpoint_000027) under fixed | last (checkpoint_000027) under demand |
|---|---|---|---|---|
| throughput, tasks per step | 0.004 [-0.003, 0.011] | 0.003 [-0.002, 0.009] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| share of seeds that keep up | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| pick service time, steps | 4213.586 [2287.648, 6139.525] | 4288.319 [2413.309, 6163.328] | n/a | n/a |
| wait before an agent takes it | 4135.090 [2146.276, 6123.904] | 4211.095 [2245.274, 6176.917] | n/a | n/a |
| travel | 54.873 [-1.086, 110.832] | 54.640 [0.958, 108.321] | n/a | n/a |
| blocked | 23.623 [-3.760, 51.006] | 22.583 [-18.995, 64.161] | n/a | n/a |
| order completion, steps | n/a | n/a | n/a | n/a |
| put-away service time | 4390.504 [3237.057, 5543.952] | 4305.857 [2481.554, 6130.160] | n/a | n/a |
| crowding | 0.186 [0.154, 0.218] | 0.208 [0.170, 0.247] | 0.141 [0.124, 0.159] | 0.147 [0.130, 0.164] |
| longest stretch with no task done | 138.900 [77.131, 200.669] | 219.050 [73.799, 364.301] | 156.050 [122.199, 189.901] | 192.350 [120.466, 264.234] |
| longest time two agents held a task at once | 3722.850 [2407.328, 5038.372] | 3796.750 [2466.591, 5126.909] | 3729.450 [2395.378, 5063.522] | 3207.550 [2183.688, 4231.412] |
| decision runtime, s | 0.025 [0.022, 0.028] | 0.021 [0.019, 0.023] | 0.017 [0.016, 0.017] | 0.016 [0.015, 0.016] |
| seeds with two agents holding a task 500 steps or more | 19 | 19 | 20 | 20 |
| seeds with two agents holding a task 1250 steps or more | 15 | 15 | 15 | 14 |
