# Warehouse instances

Means over the seeds per fleet size. The discard rate is the share of sampled layouts
that no role placement made well-formed. `used` is the instance of the config's seed.

| m | seeds | pass | discard | V | walkable | V per agent | segments | aisles | cross-aisles | str | del | rcv | ep | role share | degree | roles on leaves | d^trip min | d^trip mean | d^trip max | d^trip ratio | seconds |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 8 | 50 | 50/50 | 0.00 | 184 | 128 | 23.0 | 205 | 6.0 | 4.2 | 40 | 4 | 4 | 8 | 0.304 | 2.23 | 56.0 | 10.9 | 21.7 | 31.9 | 3.11 | 0.1 |
| 16 | 50 | 50/50 | 0.00 | 348 | 256 | 21.8 | 389 | 7.0 | 7.9 | 60 | 8 | 8 | 16 | 0.264 | 2.24 | 92.0 | 13.0 | 26.9 | 40.8 | 3.27 | 0.3 |
| 32 | 50 | 50/50 | 0.00 | 676 | 512 | 21.1 | 755 | 10.0 | 10.9 | 100 | 16 | 16 | 32 | 0.243 | 2.23 | 164.0 | 15.5 | 35.1 | 55.0 | 3.59 | 1.2 |

## The instance each config uses

- m=8, seed 42: |V|=184 (128 walkable), 204 segments, 6 aisles of length 6 to 8, 4 cross-aisles, d^trip 11 to 36 (mean 22.9, ratio 3.23), 1 layout(s) sampled, well-formed True.
- m=16, seed 42: |V|=348 (256 walkable), 389 segments, 7 aisles of length 11 to 16, 9 cross-aisles, d^trip 10 to 38 (mean 26.9, ratio 3.80), 1 layout(s) sampled, well-formed True.
- m=32, seed 42: |V|=676 (512 walkable), 758 segments, 10 aisles of length 12 to 24, 9 cross-aisles, d^trip 16 to 57 (mean 34.5, ratio 3.64), 1 layout(s) sampled, well-formed True.
