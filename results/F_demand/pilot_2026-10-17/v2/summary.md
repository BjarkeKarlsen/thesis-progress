Token Passing on the 8-agent warehouse, mean ± spread over seeds. The gain is adaptive minus fixed throughput, paired by seed, for the same skew and rotation.

| router | rate | SKUs | placement | skew s | period P | rule | Δ | ν | β | throughput | gain over fixed | service time | travel | blocked | crowding | relocated per update | waits charged per step |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| decentralised_seed0/checkpoint_000002 | 0.3 | 100 | blocks | 1.0 | 200 | fixed |  |  |  | 0.286 ± 0.009 |  | 32.1 | 14.3 | 3.07 | 0.120 | 0.0 | 0.14 |
| decentralised_seed0/checkpoint_000002 | 0.3 | 100 | blocks | 1.0 | 200 | demand | 100 | 48 |  | 0.290 ± 0.011 | 0.003 ± 0.003 | 13.3 | 10.9 | 1.94 | 0.122 | 48.0 | 0.13 |
| decentralised_seed0/checkpoint_000002 | 0.3 | 100 | blocks | 1.0 | 200 | congestion | 100 | 48 | 1.0 | 0.289 ± 0.011 | 0.003 ± 0.003 | 13.0 | 11.0 | 1.75 | 0.119 | 48.0 | 0.05 |
| decentralised_seed0/checkpoint_000002 | 0.3 | 100 | blocks | 1.0 | 200 | congestion | 100 | 48 | 3.0 | 0.289 ± 0.011 | 0.003 ± 0.003 | 13.2 | 11.3 | 1.65 | 0.117 | 48.0 | 0.04 |
| decentralised_seed0/checkpoint_000002 | 0.3 | 100 | blocks | 1.0 | 200 | congestion | 100 | 48 | 10.0 | 0.289 ± 0.011 | 0.003 ± 0.003 | 13.3 | 11.4 | 1.68 | 0.118 | 48.0 | 0.05 |
| decentralised_seed0/checkpoint_000002 | 0.3 | 100 | blocks | 1.0 | 200 | congestion_rho | 100 | 48 | 1.0 | 0.290 ± 0.011 | 0.003 ± 0.003 | 13.3 | 10.9 | 1.94 | 0.122 | 48.0 | 0.05 |
| decentralised_seed0/checkpoint_000002 | 0.3 | 100 | blocks | 1.0 | 200 | congestion_rho | 100 | 48 | 3.0 | 0.290 ± 0.011 | 0.003 ± 0.003 | 13.3 | 10.9 | 1.94 | 0.122 | 48.0 | 0.05 |
| decentralised_seed0/checkpoint_000002 | 0.3 | 100 | blocks | 1.0 | 200 | congestion_rho | 100 | 48 | 10.0 | 0.290 ± 0.011 | 0.003 ± 0.003 | 13.3 | 10.9 | 1.94 | 0.122 | 48.0 | 0.05 |
| decentralised_seed0/checkpoint_000002 | 0.3 | 100 | blocks | 1.0 | 200 | congestion_v2 | 100 | 48 | 1.0 | 0.290 ± 0.011 | 0.003 ± 0.004 | 13.0 | 10.9 | 1.77 | 0.122 | 48.0 | 0.05 |
| decentralised_seed0/checkpoint_000002 | 0.3 | 100 | blocks | 1.0 | 200 | congestion_v2 | 100 | 48 | 3.0 | 0.289 ± 0.011 | 0.003 ± 0.003 | 15.9 | 11.5 | 2.05 | 0.120 | 48.0 | 0.05 |
| decentralised_seed0/checkpoint_000002 | 0.3 | 100 | blocks | 1.0 | 200 | congestion_v2 | 100 | 48 | 10.0 | 0.288 ± 0.010 | 0.002 ± 0.004 | 15.5 | 12.2 | 2.06 | 0.118 | 48.0 | 0.04 |
| decentralised_seed0/checkpoint_000002 | 0.6 | 100 | blocks | 1.0 | 200 | fixed |  |  |  | 0.391 ± 0.029 |  | 262.9 | 15.3 | 4.92 | 0.136 | 0.0 | 0.64 |
| decentralised_seed0/checkpoint_000002 | 0.6 | 100 | blocks | 1.0 | 200 | demand | 100 | 48 |  | 0.492 ± 0.015 | 0.101 ± 0.029 | 190.3 | 12.9 | 3.11 | 0.132 | 48.0 | 0.72 |
| decentralised_seed0/checkpoint_000002 | 0.6 | 100 | blocks | 1.0 | 200 | congestion | 100 | 48 | 1.0 | 0.491 ± 0.008 | 0.100 ± 0.031 | 174.3 | 13.3 | 2.74 | 0.126 | 48.0 | 0.09 |
| decentralised_seed0/checkpoint_000002 | 0.6 | 100 | blocks | 1.0 | 200 | congestion | 100 | 48 | 3.0 | 0.489 ± 0.009 | 0.098 ± 0.022 | 200.7 | 13.4 | 2.74 | 0.126 | 48.0 | 0.09 |
| decentralised_seed0/checkpoint_000002 | 0.6 | 100 | blocks | 1.0 | 200 | congestion | 100 | 48 | 10.0 | 0.487 ± 0.007 | 0.096 ± 0.028 | 185.9 | 13.6 | 2.61 | 0.124 | 48.0 | 0.08 |
| decentralised_seed0/checkpoint_000002 | 0.6 | 100 | blocks | 1.0 | 200 | congestion_rho | 100 | 48 | 1.0 | 0.492 ± 0.015 | 0.101 ± 0.029 | 190.3 | 12.9 | 3.11 | 0.132 | 48.0 | 0.10 |
| decentralised_seed0/checkpoint_000002 | 0.6 | 100 | blocks | 1.0 | 200 | congestion_rho | 100 | 48 | 3.0 | 0.492 ± 0.015 | 0.101 ± 0.029 | 190.3 | 12.9 | 3.11 | 0.132 | 48.0 | 0.10 |
| decentralised_seed0/checkpoint_000002 | 0.6 | 100 | blocks | 1.0 | 200 | congestion_rho | 100 | 48 | 10.0 | 0.493 ± 0.012 | 0.103 ± 0.028 | 192.3 | 13.0 | 3.02 | 0.131 | 48.0 | 0.10 |
| decentralised_seed0/checkpoint_000002 | 0.6 | 100 | blocks | 1.0 | 200 | congestion_v2 | 100 | 48 | 1.0 | 0.477 ± 0.021 | 0.087 ± 0.040 | 218.9 | 13.3 | 3.29 | 0.131 | 48.0 | 0.09 |
| decentralised_seed0/checkpoint_000002 | 0.6 | 100 | blocks | 1.0 | 200 | congestion_v2 | 100 | 48 | 3.0 | 0.461 ± 0.010 | 0.071 ± 0.029 | 220.9 | 13.5 | 3.60 | 0.131 | 48.0 | 0.10 |
| decentralised_seed0/checkpoint_000002 | 0.6 | 100 | blocks | 1.0 | 200 | congestion_v2 | 100 | 48 | 10.0 | 0.457 ± 0.013 | 0.066 ± 0.039 | 226.5 | 14.1 | 3.14 | 0.126 | 48.0 | 0.08 |
| decentralised_seed1000/checkpoint_000003 | 0.3 | 100 | blocks | 1.0 | 200 | fixed |  |  |  | 0.288 ± 0.011 |  | 25.1 | 14.1 | 2.86 | 0.120 | 0.0 | 0.04 |
| decentralised_seed1000/checkpoint_000003 | 0.3 | 100 | blocks | 1.0 | 200 | demand | 100 | 48 |  | 0.290 ± 0.011 | 0.002 ± 0.001 | 14.0 | 10.7 | 1.72 | 0.120 | 48.0 | 0.03 |
| decentralised_seed1000/checkpoint_000003 | 0.3 | 100 | blocks | 1.0 | 200 | congestion | 100 | 48 | 1.0 | 0.290 ± 0.011 | 0.002 ± 0.001 | 12.4 | 10.7 | 1.54 | 0.117 | 48.0 | 0.00 |
| decentralised_seed1000/checkpoint_000003 | 0.3 | 100 | blocks | 1.0 | 200 | congestion | 100 | 48 | 3.0 | 0.290 ± 0.011 | 0.001 ± 0.001 | 15.5 | 11.2 | 1.79 | 0.120 | 48.0 | 0.00 |
| decentralised_seed1000/checkpoint_000003 | 0.3 | 100 | blocks | 1.0 | 200 | congestion | 100 | 48 | 10.0 | 0.289 ± 0.011 | 0.001 ± 0.001 | 14.5 | 11.3 | 1.95 | 0.119 | 48.0 | 0.00 |
| decentralised_seed1000/checkpoint_000003 | 0.3 | 100 | blocks | 1.0 | 200 | congestion_rho | 100 | 48 | 1.0 | 0.290 ± 0.011 | 0.002 ± 0.001 | 14.0 | 10.7 | 1.72 | 0.120 | 48.0 | 0.00 |
| decentralised_seed1000/checkpoint_000003 | 0.3 | 100 | blocks | 1.0 | 200 | congestion_rho | 100 | 48 | 3.0 | 0.290 ± 0.011 | 0.002 ± 0.001 | 14.0 | 10.7 | 1.72 | 0.120 | 48.0 | 0.00 |
| decentralised_seed1000/checkpoint_000003 | 0.3 | 100 | blocks | 1.0 | 200 | congestion_rho | 100 | 48 | 10.0 | 0.290 ± 0.011 | 0.002 ± 0.001 | 14.0 | 10.7 | 1.72 | 0.120 | 48.0 | 0.00 |
| decentralised_seed1000/checkpoint_000003 | 0.3 | 100 | blocks | 1.0 | 200 | congestion_v2 | 100 | 48 | 1.0 | 0.290 ± 0.011 | 0.001 ± 0.001 | 12.4 | 10.6 | 1.60 | 0.118 | 48.0 | 0.00 |
| decentralised_seed1000/checkpoint_000003 | 0.3 | 100 | blocks | 1.0 | 200 | congestion_v2 | 100 | 48 | 3.0 | 0.290 ± 0.011 | 0.002 ± 0.001 | 15.8 | 11.1 | 2.04 | 0.121 | 48.0 | 0.00 |
| decentralised_seed1000/checkpoint_000003 | 0.3 | 100 | blocks | 1.0 | 200 | congestion_v2 | 100 | 48 | 10.0 | 0.289 ± 0.011 | 0.001 ± 0.001 | 17.1 | 12.1 | 2.02 | 0.119 | 48.0 | 0.00 |
| decentralised_seed1000/checkpoint_000003 | 0.6 | 100 | blocks | 1.0 | 200 | fixed |  |  |  | 0.418 ± 0.013 |  | 271.0 | 14.8 | 4.01 | 0.135 | 0.0 | 0.12 |
| decentralised_seed1000/checkpoint_000003 | 0.6 | 100 | blocks | 1.0 | 200 | demand | 100 | 48 |  | 0.469 ± 0.031 | 0.051 ± 0.030 | 243.9 | 12.9 | 3.89 | 0.140 | 48.0 | 0.15 |
| decentralised_seed1000/checkpoint_000003 | 0.6 | 100 | blocks | 1.0 | 200 | congestion | 100 | 48 | 1.0 | 0.475 ± 0.027 | 0.057 ± 0.030 | 216.2 | 13.1 | 3.53 | 0.137 | 48.0 | 0.01 |
| decentralised_seed1000/checkpoint_000003 | 0.6 | 100 | blocks | 1.0 | 200 | congestion | 100 | 48 | 3.0 | 0.465 ± 0.011 | 0.047 ± 0.009 | 210.6 | 13.2 | 3.64 | 0.137 | 48.0 | 0.01 |
| decentralised_seed1000/checkpoint_000003 | 0.6 | 100 | blocks | 1.0 | 200 | congestion | 100 | 48 | 10.0 | 0.447 ± 0.018 | 0.029 ± 0.031 | 258.0 | 13.8 | 3.85 | 0.142 | 48.0 | 0.01 |
| decentralised_seed1000/checkpoint_000003 | 0.6 | 100 | blocks | 1.0 | 200 | congestion_rho | 100 | 48 | 1.0 | 0.469 ± 0.031 | 0.051 ± 0.030 | 243.9 | 12.9 | 3.89 | 0.140 | 48.0 | 0.01 |
| decentralised_seed1000/checkpoint_000003 | 0.6 | 100 | blocks | 1.0 | 200 | congestion_rho | 100 | 48 | 3.0 | 0.469 ± 0.031 | 0.051 ± 0.030 | 243.9 | 12.9 | 3.89 | 0.140 | 48.0 | 0.01 |
| decentralised_seed1000/checkpoint_000003 | 0.6 | 100 | blocks | 1.0 | 200 | congestion_rho | 100 | 48 | 10.0 | 0.469 ± 0.031 | 0.051 ± 0.030 | 243.9 | 12.9 | 3.89 | 0.140 | 48.0 | 0.01 |
| decentralised_seed1000/checkpoint_000003 | 0.6 | 100 | blocks | 1.0 | 200 | congestion_v2 | 100 | 48 | 1.0 | 0.464 ± 0.030 | 0.046 ± 0.020 | 236.1 | 13.1 | 3.87 | 0.138 | 48.0 | 0.01 |
| decentralised_seed1000/checkpoint_000003 | 0.6 | 100 | blocks | 1.0 | 200 | congestion_v2 | 100 | 48 | 3.0 | 0.441 ± 0.063 | 0.023 ± 0.068 | 250.8 | 13.6 | 4.58 | 0.148 | 48.0 | 0.01 |
| decentralised_seed1000/checkpoint_000003 | 0.6 | 100 | blocks | 1.0 | 200 | congestion_v2 | 100 | 48 | 10.0 | 0.476 ± 0.013 | 0.058 ± 0.014 | 212.2 | 13.5 | 3.03 | 0.127 | 48.0 | 0.01 |
| token_passing | 0.3 | 100 | blocks | 1.0 | 200 | fixed |  |  |  | 0.260 ± 0.007 |  | 54.1 | 12.8 | 0.19 | 0.094 | 0.0 | 0.11 |
| token_passing | 0.3 | 100 | blocks | 1.0 | 200 | demand | 100 | 48 |  | 0.275 ± 0.009 | 0.015 ± 0.003 | 39.4 | 11.1 | 0.33 | 0.096 | 48.0 | 0.25 |
| token_passing | 0.3 | 100 | blocks | 1.0 | 200 | congestion | 100 | 48 | 1.0 | 0.273 ± 0.006 | 0.013 ± 0.001 | 39.9 | 11.5 | 0.29 | 0.096 | 48.0 | 0.08 |
| token_passing | 0.3 | 100 | blocks | 1.0 | 200 | congestion | 100 | 48 | 3.0 | 0.272 ± 0.006 | 0.012 ± 0.002 | 43.2 | 11.7 | 0.25 | 0.096 | 48.0 | 0.07 |
| token_passing | 0.3 | 100 | blocks | 1.0 | 200 | congestion | 100 | 48 | 10.0 | 0.270 ± 0.006 | 0.010 ± 0.003 | 43.9 | 11.7 | 0.25 | 0.096 | 48.0 | 0.07 |
| token_passing | 0.3 | 100 | blocks | 1.0 | 200 | congestion_rho | 100 | 48 | 1.0 | 0.275 ± 0.009 | 0.015 ± 0.003 | 39.4 | 11.1 | 0.33 | 0.096 | 48.0 | 0.09 |
| token_passing | 0.3 | 100 | blocks | 1.0 | 200 | congestion_rho | 100 | 48 | 3.0 | 0.275 ± 0.009 | 0.015 ± 0.003 | 39.4 | 11.1 | 0.33 | 0.096 | 48.0 | 0.09 |
| token_passing | 0.3 | 100 | blocks | 1.0 | 200 | congestion_rho | 100 | 48 | 10.0 | 0.275 ± 0.009 | 0.015 ± 0.003 | 39.4 | 11.1 | 0.33 | 0.096 | 48.0 | 0.09 |
| token_passing | 0.3 | 100 | blocks | 1.0 | 200 | congestion_v2 | 100 | 48 | 1.0 | 0.275 ± 0.009 | 0.015 ± 0.003 | 39.8 | 11.1 | 0.33 | 0.097 | 48.0 | 0.09 |
| token_passing | 0.3 | 100 | blocks | 1.0 | 200 | congestion_v2 | 100 | 48 | 3.0 | 0.276 ± 0.007 | 0.016 ± 0.003 | 39.2 | 11.2 | 0.32 | 0.097 | 48.0 | 0.09 |
| token_passing | 0.3 | 100 | blocks | 1.0 | 200 | congestion_v2 | 100 | 48 | 10.0 | 0.275 ± 0.008 | 0.015 ± 0.003 | 40.2 | 11.2 | 0.30 | 0.097 | 48.0 | 0.08 |
| token_passing | 0.6 | 100 | blocks | 1.0 | 200 | fixed |  |  |  | 0.374 ± 0.006 |  | 116.2 | 10.4 | 0.20 | 0.095 | 0.0 | 0.58 |
| token_passing | 0.6 | 100 | blocks | 1.0 | 200 | demand | 100 | 48 |  | 0.432 ± 0.012 | 0.057 ± 0.012 | 93.6 | 8.8 | 0.38 | 0.101 | 48.0 | 1.19 |
| token_passing | 0.6 | 100 | blocks | 1.0 | 200 | congestion | 100 | 48 | 1.0 | 0.422 ± 0.005 | 0.047 ± 0.005 | 78.5 | 9.1 | 0.29 | 0.098 | 48.0 | 0.12 |
| token_passing | 0.6 | 100 | blocks | 1.0 | 200 | congestion | 100 | 48 | 3.0 | 0.423 ± 0.007 | 0.049 ± 0.006 | 74.1 | 9.1 | 0.27 | 0.098 | 48.0 | 0.11 |
| token_passing | 0.6 | 100 | blocks | 1.0 | 200 | congestion | 100 | 48 | 10.0 | 0.413 ± 0.007 | 0.038 ± 0.003 | 79.9 | 9.4 | 0.21 | 0.097 | 48.0 | 0.09 |
| token_passing | 0.6 | 100 | blocks | 1.0 | 200 | congestion_rho | 100 | 48 | 1.0 | 0.432 ± 0.012 | 0.057 ± 0.012 | 93.6 | 8.8 | 0.38 | 0.101 | 48.0 | 0.16 |
| token_passing | 0.6 | 100 | blocks | 1.0 | 200 | congestion_rho | 100 | 48 | 3.0 | 0.432 ± 0.012 | 0.057 ± 0.012 | 93.6 | 8.8 | 0.38 | 0.101 | 48.0 | 0.16 |
| token_passing | 0.6 | 100 | blocks | 1.0 | 200 | congestion_rho | 100 | 48 | 10.0 | 0.432 ± 0.011 | 0.058 ± 0.012 | 90.9 | 8.7 | 0.39 | 0.101 | 48.0 | 0.17 |
| token_passing | 0.6 | 100 | blocks | 1.0 | 200 | congestion_v2 | 100 | 48 | 1.0 | 0.427 ± 0.008 | 0.053 ± 0.005 | 89.4 | 8.9 | 0.36 | 0.102 | 48.0 | 0.15 |
| token_passing | 0.6 | 100 | blocks | 1.0 | 200 | congestion_v2 | 100 | 48 | 3.0 | 0.426 ± 0.013 | 0.051 ± 0.013 | 91.8 | 8.9 | 0.36 | 0.101 | 48.0 | 0.15 |
| token_passing | 0.6 | 100 | blocks | 1.0 | 200 | congestion_v2 | 100 | 48 | 10.0 | 0.425 ± 0.006 | 0.051 ± 0.007 | 88.7 | 9.0 | 0.34 | 0.101 | 48.0 | 0.15 |
