# Test results, fleet 8, section, trained under demand storage

Mean and 95 % interval over the 20 test seeds, 10000 steps with a 5000-step warm-up. The chosen policy is the result, the last checkpoint a check. The paired gain between storage rules is in `evaluate_summary.md` and the fleet's `comparison.md`.

| measure | chosen (checkpoint_000013) under demand | last (checkpoint_000027) under demand |
|---|---|---|
| throughput, tasks per step | 0.098 [0.077, 0.118] | 0.060 [0.048, 0.071] |
| share of seeds that keep up | 0.350 [0.121, 0.579] | 0.000 [0.000, 0.000] |
| pick service time, steps | 1376.570 [785.951, 1967.190] | 2444.869 [2056.666, 2833.073] |
| wait before an agent takes it | 1312.903 [729.401, 1896.404] | 2369.563 [1982.624, 2756.502] |
| travel | 45.592 [40.612, 50.573] | 49.679 [46.563, 52.795] |
| blocked | 18.075 [13.647, 22.504] | 25.628 [23.614, 27.641] |
| order completion, steps | 1863.651 [1139.366, 2587.936] | 3284.421 [2535.568, 4033.275] |
| put-away service time | 1405.056 [824.682, 1985.429] | 2485.916 [2103.585, 2868.246] |
| crowding | 0.128 [0.107, 0.149] | 0.101 [0.088, 0.115] |
| longest stretch with no task done | 86.300 [55.549, 117.051] | 92.200 [26.644, 157.756] |
| longest time two agents held a task at once | 299.900 [193.240, 406.560] | 263.100 [161.896, 364.304] |
| decision runtime, s | 0.020 [0.020, 0.020] | 0.019 [0.019, 0.020] |
| seeds with two agents holding a task 500 steps or more | 5 | 1 |
| seeds with two agents holding a task 1250 steps or more | 0 | 0 |
