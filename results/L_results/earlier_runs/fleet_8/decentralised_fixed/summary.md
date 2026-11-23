# Test results, fleet 8, decentralised, trained under fixed storage

Mean and 95 % interval over the 20 test seeds, 10000 steps with a 5000-step warm-up. The chosen policy is the result, the last checkpoint a check. The paired gain between storage rules is in `evaluate_summary.md` and the fleet's `comparison.md`.

| measure | chosen (checkpoint_000024) under fixed | chosen (checkpoint_000024) under demand | last (checkpoint_000027) under fixed | last (checkpoint_000027) under demand |
|---|---|---|---|---|
| throughput, tasks per step | 0.094 [0.071, 0.117] | 0.089 [0.064, 0.113] | 0.102 [0.087, 0.117] | 0.098 [0.081, 0.115] |
| share of seeds that keep up | 0.500 [0.260, 0.740] | 0.400 [0.165, 0.635] | 0.450 [0.211, 0.689] | 0.300 [0.080, 0.520] |
| pick service time, steps | 1163.445 [566.195, 1760.696] | 1235.119 [718.840, 1751.398] | 1010.700 [634.051, 1387.349] | 1304.432 [875.227, 1733.637] |
| wait before an agent takes it | 1101.843 [512.894, 1690.791] | 1172.898 [663.450, 1682.345] | 954.091 [580.972, 1327.210] | 1244.765 [820.250, 1669.279] |
| travel | 42.843 [35.346, 50.341] | 42.265 [36.315, 48.214] | 40.954 [36.124, 45.784] | 41.564 [35.606, 47.522] |
| blocked | 18.759 [13.294, 24.224] | 19.957 [16.182, 23.731] | 15.655 [13.313, 17.997] | 18.103 [14.968, 21.238] |
| order completion, steps | 1509.366 [655.717, 2363.014] | 1828.371 [980.586, 2676.155] | 1773.911 [1140.554, 2407.267] | 2357.106 [1631.494, 3082.717] |
| put-away service time | 1192.982 [597.943, 1788.021] | 1268.570 [753.627, 1783.513] | 1043.933 [671.949, 1415.918] | 1347.024 [924.462, 1769.586] |
| crowding | 0.116 [0.097, 0.135] | 0.128 [0.111, 0.146] | 0.100 [0.088, 0.112] | 0.110 [0.098, 0.122] |
| longest stretch with no task done | 245.950 [150.746, 341.154] | 309.650 [158.688, 460.612] | 125.100 [92.069, 158.131] | 161.550 [94.895, 228.205] |
| longest time two agents held a task at once | 533.900 [313.536, 754.264] | 549.200 [365.388, 733.012] | 266.650 [224.222, 309.078] | 325.050 [234.629, 415.471] |
| decision runtime, s | 0.008 [0.008, 0.008] | 0.008 [0.008, 0.008] | 0.008 [0.008, 0.008] | 0.008 [0.008, 0.009] |
| seeds with two agents holding a task 500 steps or more | 8 | 8 | 0 | 2 |
| seeds with two agents holding a task 1250 steps or more | 3 | 2 | 0 | 0 |
