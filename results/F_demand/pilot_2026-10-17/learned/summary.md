Token Passing on the 8-agent warehouse, mean ± spread over seeds. The gain is adaptive minus fixed throughput, paired by seed, for the same skew and rotation.

| router | rate | SKUs | placement | skew s | period P | rule | Δ | ν | β | throughput | gain over fixed | service time | travel | blocked | crowding | relocated per update | waits charged per step |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| decentralised_seed0/checkpoint_000002 | 0.3 | 100 | blocks | 1.0 | 200 | fixed |  |  |  | 0.286 ± 0.009 |  | 32.1 | 14.3 | 3.07 | 0.120 | 0.0 | 0.08 |
| decentralised_seed0/checkpoint_000002 | 0.3 | 100 | blocks | 1.0 | 200 | demand | 100 | 48 |  | 0.290 ± 0.011 | 0.003 ± 0.003 | 13.3 | 10.9 | 1.94 | 0.122 | 48.0 | 0.08 |
| decentralised_seed0/checkpoint_000002 | 0.3 | 100 | blocks | 1.0 | 200 | congestion | 100 | 48 | 3.0 | 0.289 ± 0.011 | 0.003 ± 0.003 | 13.2 | 11.4 | 1.62 | 0.117 | 48.0 | 0.08 |
| decentralised_seed0/checkpoint_000002 | 0.3 | 100 | blocks | 1.0 | 200 | congestion | 100 | 48 | 10.0 | 0.289 ± 0.011 | 0.003 ± 0.004 | 13.3 | 11.5 | 1.61 | 0.119 | 48.0 | 0.09 |
| decentralised_seed0/checkpoint_000002 | 0.6 | 100 | blocks | 1.0 | 200 | fixed |  |  |  | 0.391 ± 0.029 |  | 262.9 | 15.3 | 4.92 | 0.136 | 0.0 | 0.36 |
| decentralised_seed0/checkpoint_000002 | 0.6 | 100 | blocks | 1.0 | 200 | demand | 100 | 48 |  | 0.492 ± 0.015 | 0.101 ± 0.029 | 190.3 | 12.9 | 3.11 | 0.132 | 48.0 | 0.41 |
| decentralised_seed0/checkpoint_000002 | 0.6 | 100 | blocks | 1.0 | 200 | congestion | 100 | 48 | 3.0 | 0.487 ± 0.005 | 0.096 ± 0.030 | 190.1 | 13.5 | 2.63 | 0.125 | 48.0 | 0.38 |
| decentralised_seed0/checkpoint_000002 | 0.6 | 100 | blocks | 1.0 | 200 | congestion | 100 | 48 | 10.0 | 0.471 ± 0.026 | 0.080 ± 0.024 | 193.2 | 13.7 | 3.08 | 0.130 | 48.0 | 0.51 |
| decentralised_seed1000/checkpoint_000003 | 0.3 | 100 | blocks | 1.0 | 200 | fixed |  |  |  | 0.288 ± 0.011 |  | 25.1 | 14.1 | 2.86 | 0.120 | 0.0 | 0.02 |
| decentralised_seed1000/checkpoint_000003 | 0.3 | 100 | blocks | 1.0 | 200 | demand | 100 | 48 |  | 0.290 ± 0.011 | 0.002 ± 0.001 | 14.0 | 10.7 | 1.72 | 0.120 | 48.0 | 0.01 |
| decentralised_seed1000/checkpoint_000003 | 0.3 | 100 | blocks | 1.0 | 200 | congestion | 100 | 48 | 3.0 | 0.290 ± 0.011 | 0.001 ± 0.001 | 15.5 | 11.2 | 1.79 | 0.120 | 48.0 | 0.02 |
| decentralised_seed1000/checkpoint_000003 | 0.3 | 100 | blocks | 1.0 | 200 | congestion | 100 | 48 | 10.0 | 0.289 ± 0.011 | 0.001 ± 0.001 | 14.5 | 11.3 | 1.95 | 0.119 | 48.0 | 0.02 |
| decentralised_seed1000/checkpoint_000003 | 0.6 | 100 | blocks | 1.0 | 200 | fixed |  |  |  | 0.418 ± 0.013 |  | 271.0 | 14.8 | 4.01 | 0.135 | 0.0 | 0.06 |
| decentralised_seed1000/checkpoint_000003 | 0.6 | 100 | blocks | 1.0 | 200 | demand | 100 | 48 |  | 0.469 ± 0.031 | 0.051 ± 0.030 | 243.9 | 12.9 | 3.89 | 0.140 | 48.0 | 0.08 |
| decentralised_seed1000/checkpoint_000003 | 0.6 | 100 | blocks | 1.0 | 200 | congestion | 100 | 48 | 3.0 | 0.469 ± 0.025 | 0.051 ± 0.018 | 214.3 | 13.3 | 3.53 | 0.133 | 48.0 | 0.05 |
| decentralised_seed1000/checkpoint_000003 | 0.6 | 100 | blocks | 1.0 | 200 | congestion | 100 | 48 | 10.0 | 0.447 ± 0.018 | 0.029 ± 0.031 | 258.0 | 13.8 | 3.85 | 0.142 | 48.0 | 0.09 |
