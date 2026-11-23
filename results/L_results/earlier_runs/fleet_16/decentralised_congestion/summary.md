# Test results, fleet 16, decentralised, trained under congestion storage

Mean and 95 % interval over the 20 test seeds, 10000 steps with a 5000-step warm-up. The chosen policy is the result, the last checkpoint a check. The paired gain between storage rules is in `evaluate_summary.md` and the fleet's `comparison.md`.

| measure | chosen (checkpoint_000027) under congestion | last (checkpoint_000027) under congestion |
|---|---|---|
| throughput, tasks per step | 0.104 [0.069, 0.138] | 0.104 [0.069, 0.138] |
| share of seeds that keep up | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| pick service time, steps | 2306.352 [1795.640, 2817.065] | 2306.858 [1796.583, 2817.132] |
| wait before an agent takes it | 2225.752 [1721.412, 2730.093] | 2226.224 [1722.295, 2730.153] |
| travel | 60.748 [54.400, 67.096] | 60.765 [54.422, 67.108] |
| blocked | 19.852 [17.098, 22.606] | 19.868 [17.118, 22.619] |
| order completion, steps | 2930.103 [2119.682, 3740.525] | 2933.280 [2127.643, 3738.917] |
| put-away service time | 2303.900 [1798.580, 2809.220] | 2303.978 [1798.726, 2809.230] |
| crowding | 0.150 [0.132, 0.168] | 0.150 [0.132, 0.168] |
| longest stretch with no task done | 67.950 [46.652, 89.248] | 67.850 [46.507, 89.193] |
| longest time two agents held a task at once | 463.000 [314.837, 611.163] | 462.950 [314.769, 611.131] |
| decision runtime, s | 0.024 [0.023, 0.025] | 0.023 [0.022, 0.024] |
| seeds with two agents holding a task 500 steps or more | 5 | 5 |
| seeds with two agents holding a task 1250 steps or more | 1 | 1 |
