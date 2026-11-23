# Test results, fleet 8, decentralised, with messages, trained under congestion storage

Mean and 95 % interval over the 20 test seeds, 10000 steps with a 5000-step warm-up. The chosen policy is the result, the last checkpoint a check. The paired gain between storage rules is in `evaluate_summary.md` and the fleet's `comparison.md`.

| measure | chosen (checkpoint_000023) under congestion | last (checkpoint_000027) under congestion |
|---|---|---|
| throughput, tasks per step | 0.101 [0.073, 0.128] | 0.105 [0.080, 0.131] |
| share of seeds that keep up | 0.600 [0.365, 0.835] | 0.600 [0.365, 0.835] |
| pick service time, steps | 1129.508 [441.542, 1817.474] | 969.062 [332.367, 1605.757] |
| wait before an agent takes it | 1074.565 [393.182, 1755.947] | 914.352 [286.057, 1542.646] |
| travel | 40.478 [32.712, 48.243] | 41.156 [33.811, 48.502] |
| blocked | 14.466 [10.358, 18.574] | 13.554 [10.699, 16.409] |
| order completion, steps | 1240.323 [436.060, 2044.586] | 1011.068 [389.143, 1632.993] |
| put-away service time | 1154.569 [477.235, 1831.903] | 991.875 [373.170, 1610.581] |
| crowding | 0.113 [0.095, 0.130] | 0.107 [0.091, 0.123] |
| longest stretch with no task done | 428.550 [-12.796, 869.896] | 242.600 [13.675, 471.525] |
| longest time two agents held a task at once | 918.300 [33.256, 1803.344] | 522.350 [-14.955, 1059.655] |
| decision runtime, s | 0.010 [0.010, 0.010] | 0.010 [0.010, 0.010] |
| seeds with two agents holding a task 500 steps or more | 5 | 3 |
| seeds with two agents holding a task 1250 steps or more | 2 | 1 |
