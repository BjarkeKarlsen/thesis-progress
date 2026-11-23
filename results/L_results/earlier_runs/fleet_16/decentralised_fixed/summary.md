# Test results, fleet 16, decentralised, trained under fixed storage

Mean and 95 % interval over the 20 test seeds, 10000 steps with a 5000-step warm-up. The chosen policy is the result, the last checkpoint a check. The paired gain between storage rules is in `evaluate_summary.md` and the fleet's `comparison.md`.

| measure | chosen (checkpoint_000019) under fixed | chosen (checkpoint_000019) under demand | last (checkpoint_000027) under fixed | last (checkpoint_000027) under demand |
|---|---|---|---|---|
| throughput, tasks per step | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [-0.001, 0.001] | 0.000 [0.000, 0.000] |
| share of seeds that keep up | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| pick service time, steps | n/a | n/a | 4550.111 | n/a |
| wait before an agent takes it | n/a | n/a | 4484.333 | n/a |
| travel | n/a | n/a | 53.593 | n/a |
| blocked | n/a | n/a | 12.185 | n/a |
| order completion, steps | n/a | n/a | n/a | n/a |
| put-away service time | n/a | n/a | 4587.182 | n/a |
| crowding | 0.192 [0.177, 0.207] | 0.200 [0.181, 0.218] | 0.146 [0.132, 0.159] | 0.154 [0.141, 0.168] |
| longest stretch with no task done | 954.350 [214.762, 1693.938] | 1140.750 [390.336, 1891.164] | 585.450 [22.789, 1148.111] | 588.450 [23.476, 1153.424] |
| longest time two agents held a task at once | 4144.900 [2861.298, 5428.502] | 3425.900 [2442.968, 4408.832] | 3943.450 [2401.021, 5485.879] | 2899.850 [1709.655, 4090.045] |
| decision runtime, s | 0.021 [0.018, 0.023] | 0.017 [0.017, 0.018] | 0.016 [0.015, 0.017] | 0.015 [0.014, 0.016] |
| seeds with two agents holding a task 500 steps or more | 20 | 20 | 20 | 20 |
| seeds with two agents holding a task 1250 steps or more | 17 | 17 | 14 | 13 |
