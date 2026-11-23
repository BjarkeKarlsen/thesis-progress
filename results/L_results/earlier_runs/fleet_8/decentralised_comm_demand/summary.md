# Test results, fleet 8, decentralised, with messages, trained under demand storage

Mean and 95 % interval over the 20 test seeds, 10000 steps with a 5000-step warm-up. The chosen policy is the result, the last checkpoint a check. The paired gain between storage rules is in `evaluate_summary.md` and the fleet's `comparison.md`.

| measure | chosen (checkpoint_000018) under demand | last (checkpoint_000027) under demand |
|---|---|---|
| throughput, tasks per step | 0.053 [0.023, 0.083] | 0.067 [0.044, 0.090] |
| share of seeds that keep up | 0.350 [0.121, 0.579] | 0.200 [0.008, 0.392] |
| pick service time, steps | 1363.663 [312.797, 2414.529] | 1681.061 [1012.214, 2349.907] |
| wait before an agent takes it | 1315.267 [267.987, 2362.547] | 1615.143 [954.147, 2276.139] |
| travel | 33.658 [29.721, 37.595] | 44.258 [35.097, 53.419] |
| blocked | 14.738 [11.928, 17.548] | 21.659 [17.491, 25.828] |
| order completion, steps | 1505.279 [322.424, 2688.134] | 1894.159 [954.525, 2833.793] |
| put-away service time | 1432.373 [335.156, 2529.589] | 1708.139 [1060.453, 2355.826] |
| crowding | 0.154 [0.129, 0.179] | 0.141 [0.122, 0.160] |
| longest stretch with no task done | 866.700 [249.541, 1483.859] | 238.450 [171.014, 305.886] |
| longest time two agents held a task at once | 2424.550 [1053.082, 3796.018] | 610.350 [429.514, 791.186] |
| decision runtime, s | 0.011 [0.011, 0.012] | 0.012 [0.011, 0.012] |
| seeds with two agents holding a task 500 steps or more | 13 | 9 |
| seeds with two agents holding a task 1250 steps or more | 9 | 2 |
