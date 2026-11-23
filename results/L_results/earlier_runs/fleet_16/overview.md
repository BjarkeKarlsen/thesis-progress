# Fleet 16, the four learned arms and Token Passing

Written by `thesis-progress/scripts/images/fleet16_results.py`. Each rule is played with the policy trained under it (Regime 2). Test: 20 seeds, 10000 steps, 5000 warm-up, chosen checkpoint. Validation: 5 seeds, 2000 steps. Mean [95 % interval].

| arm | rule | chosen | validation throughput | test throughput | seeds keeping up | pick service, steps | decision time, ms (GPU) |
|---|---|---|---|---|---|---|---|
| centralised | fixed | 21 | 0.158 [0.148, 0.168] | 0.036 [0.017, 0.055] | 0 of 20 | 3655 (13 seeds with a pick done) | 109 |
| centralised | demand | 23 | 0.138 [0.127, 0.148] | 0.026 [0.011, 0.041] | 0 of 20 | 3824 (11 seeds with a pick done) | 110 |
| centralised | congestion-aware | 15 | 0.168 [0.155, 0.180] | 0.058 [0.036, 0.080] | 0 of 20 | 3350 (16 seeds with a pick done) | 110 |
| section-based | fixed | 24 | 0.225 [0.207, 0.242] | 0.131 [0.087, 0.174] | 1 of 20 | 1377 (14 seeds with a pick done) | 73 |
| section-based | demand | 25 | 0.185 [0.166, 0.203] | 0.055 [0.031, 0.080] | 0 of 20 | 3237 (14 seeds with a pick done) | 74 |
| section-based | congestion-aware | 27 | 0.213 [0.204, 0.223] | 0.121 [0.086, 0.155] | 0 of 20 | 2168 (17 seeds with a pick done) | 72 |
| decentralised | fixed | 19 | 0.088 [0.057, 0.120] | 0.000 [0.000, 0.000] | 0 of 20 | no pick done | 11 |
| decentralised | demand | 22 | 0.120 [0.111, 0.129] | 0.007 [-0.003, 0.016] | 0 of 20 | 4120 (4 seeds with a pick done) | 12 |
| decentralised | congestion-aware | 27 | 0.210 [0.191, 0.229] | 0.104 [0.069, 0.138] | 0 of 20 | 2306 (16 seeds with a pick done) | 14 |
| decentralised with messages | fixed | 15 | 0.136 [0.120, 0.151] | 0.004 [-0.003, 0.011] | 0 of 20 | 4214 (3 seeds with a pick done) | 15 |
| decentralised with messages | demand | 10 | 0.082 [0.070, 0.094] | 0.000 [0.000, 0.000] | 0 of 20 | no pick done | 14 |
| decentralised with messages | congestion-aware | 13 | 0.131 [0.104, 0.158] | 0.004 [-0.002, 0.010] | 0 of 20 | 4274 (3 seeds with a pick done) | 14 |
| Token Passing | fixed | n/a | n/a | 0.265 [0.255, 0.274] | 20 of 20 | 126 | 1.9 (CPU) |
| Token Passing | demand | n/a | n/a | 0.284 [0.274, 0.294] | 20 of 20 | 107 | 2.0 (CPU) |
| Token Passing | congestion-aware | n/a | n/a | 0.285 [0.275, 0.296] | 20 of 20 | 108 | 2.0 (CPU) |
