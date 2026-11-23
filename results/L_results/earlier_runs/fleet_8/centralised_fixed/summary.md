# Test results, fleet 8, centralised, trained under fixed storage

Mean and 95 % interval over the 20 test seeds, 10000 steps with a 5000-step warm-up. The chosen policy is the result, the last checkpoint a check. The paired gain between storage rules is in `evaluate_summary.md` and the fleet's `comparison.md`.

| measure | chosen (checkpoint_000013) under fixed | chosen (checkpoint_000013) under demand | last (checkpoint_000027) under fixed | last (checkpoint_000027) under demand |
|---|---|---|---|---|
| throughput, tasks per step | 0.099 [0.085, 0.112] | 0.094 [0.080, 0.107] | 0.062 [0.050, 0.074] | 0.065 [0.054, 0.077] |
| share of seeds that keep up | 0.400 [0.165, 0.635] | 0.200 [0.008, 0.392] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| pick service time, steps | 1151.170 [795.868, 1506.472] | 1324.787 [966.651, 1682.923] | 2318.851 [1906.581, 2731.122] | 2216.445 [1835.578, 2597.313] |
| wait before an agent takes it | 1091.300 [737.035, 1445.566] | 1262.636 [905.718, 1619.554] | 2245.209 [1833.846, 2656.571] | 2145.942 [1765.262, 2526.623] |
| travel | 44.270 [41.160, 47.380] | 44.722 [41.665, 47.779] | 58.715 [55.837, 61.594] | 55.840 [53.509, 58.171] |
| blocked | 15.599 [13.895, 17.304] | 17.429 [15.431, 19.427] | 14.927 [13.935, 15.920] | 14.663 [13.702, 15.624] |
| order completion, steps | 2141.864 [1450.796, 2832.932] | 2505.627 [1805.390, 3205.864] | 3260.577 [2608.406, 3912.748] | 3184.598 [2662.998, 3706.199] |
| put-away service time | 1186.492 [833.254, 1539.730] | 1544.537 [1039.164, 2049.909] | 2346.635 [1938.348, 2754.922] | 2250.812 [1871.336, 2630.289] |
| crowding | 0.101 [0.088, 0.113] | 0.114 [0.101, 0.128] | 0.080 [0.073, 0.087] | 0.089 [0.080, 0.097] |
| longest stretch with no task done | 59.200 [51.451, 66.949] | 48.300 [42.349, 54.251] | 48.150 [44.826, 51.474] | 46.500 [42.220, 50.780] |
| longest time two agents held a task at once | 173.150 [151.406, 194.894] | 192.100 [162.195, 222.005] | 162.600 [141.404, 183.796] | 170.300 [158.434, 182.166] |
| decision runtime, s | 0.047 [0.046, 0.048] | 0.047 [0.047, 0.048] | 0.046 [0.046, 0.047] | 0.045 [0.044, 0.046] |
| seeds with two agents holding a task 500 steps or more | 0 | 0 | 0 | 0 |
| seeds with two agents holding a task 1250 steps or more | 0 | 0 | 0 | 0 |
