# Test results, fleet 16, decentralised, with messages, trained under demand storage

Mean and 95 % interval over the 20 test seeds, 10000 steps with a 5000-step warm-up. The chosen policy is the result, the last checkpoint a check. The paired gain between storage rules is in `evaluate_summary.md` and the fleet's `comparison.md`.

| measure | chosen (checkpoint_000010) under demand | last (checkpoint_000027) under demand |
|---|---|---|
| throughput, tasks per step | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| share of seeds that keep up | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| pick service time, steps | n/a | n/a |
| wait before an agent takes it | n/a | n/a |
| travel | n/a | n/a |
| blocked | n/a | n/a |
| order completion, steps | n/a | n/a |
| put-away service time | n/a | n/a |
| crowding | 0.205 [0.162, 0.247] | 0.163 [0.139, 0.187] |
| longest stretch with no task done | 266.250 [139.466, 393.034] | 550.200 [378.456, 721.944] |
| longest time two agents held a task at once | 2725.600 [1845.136, 3606.064] | 8149.650 [7443.672, 8855.628] |
| decision runtime, s | 0.022 [0.020, 0.024] | 0.018 [0.017, 0.018] |
| seeds with two agents holding a task 500 steps or more | 20 | 20 |
| seeds with two agents holding a task 1250 steps or more | 13 | 20 |
