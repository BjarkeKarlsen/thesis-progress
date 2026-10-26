# Warehouse instances

Means over the seeds per fleet size. The discard rate is the share of sampled layouts
that no role placement made well-formed. `used` is the instance of the config's seed.

| m | seeds | pass | discard | V | walkable | V per agent | segments | aisles | cross-aisles | str | del | rcv | ep | role share | degree | roles on leaves | d^trip min | d^trip mean | d^trip max | d^trip ratio | seconds |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 8 | 50 | 50/50 | 0.00 | 202 | 128 | 25.2 | 223 | 6.0 | 3.9 | 58 | 4 | 4 | 8 | 0.366 | 2.21 | 74.0 | 6.0 | 20.0 | 36.8 | 6.13 | 0.3 |
| 16 | 50 | 50/50 | 0.00 | 518 | 256 | 32.4 | 547 | 8.0 | 8.6 | 230 | 8 | 8 | 16 | 0.506 | 2.11 | 262.0 | 5.0 | 31.1 | 63.0 | 12.59 | 1.9 |
| 32 | 50 | 50/50 | 0.00 | 1151 | 512 | 36.0 | 1199 | 12.0 | 14.8 | 575 | 16 | 16 | 32 | 0.555 | 2.08 | 639.0 | 5.0 | 42.6 | 87.0 | 17.39 | 6.8 |
| 64 | 50 | 50/50 | 0.00 | 2508 | 1024 | 39.2 | 2580 | 18.0 | 21.9 | 1356 | 32 | 32 | 64 | 0.592 | 2.06 | 1484.0 | 5.0 | 60.0 | 131.0 | 26.20 | 23.9 |

## The instance each config uses

- m=8, seed 42: |V|=202 (128 walkable), 223 segments, 6 aisles of length 6 to 8, 4 cross-aisles, d^trip 6 to 37 (mean 19.9, ratio 6.17), 1 layout(s) sampled, well-formed True.
- m=16, seed 42: |V|=518 (256 walkable), 547 segments, 8 aisles of length 13 to 20, 9 cross-aisles, d^trip 5 to 63 (mean 31.2, ratio 12.60), 1 layout(s) sampled, well-formed True.
- m=32, seed 42: |V|=1151 (512 walkable), 1201 segments, 12 aisles of length 18 to 30, 16 cross-aisles, d^trip 5 to 87 (mean 42.3, ratio 17.40), 1 layout(s) sampled, well-formed True.
- m=64, seed 42: |V|=2508 (1024 walkable), 2584 segments, 18 aisles of length 27 to 48, 24 cross-aisles, d^trip 5 to 131 (mean 60.0, ratio 26.20), 1 layout(s) sampled, well-formed True.
