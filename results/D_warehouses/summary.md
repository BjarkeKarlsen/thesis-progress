# Warehouse instances

Means over the seeds per fleet size. The discard rate is the share of sampled layouts
that no role placement made well-formed. `used` is the instance of the config's seed.

| m | seeds | pass | discard | V | V per agent | segments | aisles | cross-aisles | str | del | rcv | ep | role share | degree | roles on leaves | d^trip mean | seconds |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 8 | 50 | 50/50 | 0.07 | 128 | 16.0 | 178 | 11.0 | 6.2 | 4 | 4 | 4 | 8 | 0.156 | 2.77 | 0.7 | 11.2 | 0.1 |
| 16 | 50 | 50/50 | 0.29 | 256 | 16.0 | 355 | 17.0 | 8.0 | 8 | 8 | 8 | 16 | 0.156 | 2.77 | 1.1 | 13.0 | 0.4 |
| 32 | 50 | 50/50 | 0.50 | 512 | 16.0 | 751 | 23.4 | 12.8 | 16 | 16 | 16 | 32 | 0.156 | 2.93 | 1.5 | 16.2 | 1.8 |
| 64 | 50 | 50/50 | 0.88 | 1024 | 16.0 | 1573 | 33.7 | 19.8 | 32 | 32 | 32 | 64 | 0.156 | 3.07 | 1.4 | 20.6 | 17.5 |

## The instance each config uses

- m=8, seed 42: |V|=128, 180 segments, 12 aisles of length 1 to 12, 7 cross-aisles, d^trip 11 to 15 (mean 13.0), 1 layout(s) sampled, well-formed True.
- m=16, seed 42: |V|=256, 329 segments, 18 aisles of length 2 to 16, 6 cross-aisles, d^trip 6 to 17 (mean 12.4), 1 layout(s) sampled, well-formed True.
- m=32, seed 42: |V|=512, 747 segments, 22 aisles of length 14 to 23, 12 cross-aisles, d^trip 5 to 35 (mean 17.6), 2 layout(s) sampled, well-formed True.
- m=64, seed 42: |V|=1024, 1549 segments, 34 aisles of length 5 to 32, 19 cross-aisles, d^trip 4 to 56 (mean 21.6), 8 layout(s) sampled, well-formed True.
