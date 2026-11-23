# Warehouse instances

Means over the seeds per fleet size. The discard rate is the share of sampled layouts
that no role placement made well-formed. `used` is the instance of the config's seed.

| m | seeds | pass | discard | V | walkable | V per agent | segments | aisles | cross-aisles | str | del | rcv | ep | role share | degree | roles on leaves | d^trip min | d^trip mean | d^trip max | d^trip ratio | seconds |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 8 | 50 | 50/50 | 0.00 | 184 | 128 | 23.0 | 205 | 6.0 | 4.2 | 40 | 4 | 4 | 8 | 0.304 | 2.23 | 56.0 | 16.8 | 26.3 | 37.9 | 2.66 | 0.1 |
| 16 | 50 | 50/50 | 0.00 | 368 | 256 | 23.0 | 409 | 7.0 | 7.9 | 80 | 8 | 8 | 16 | 0.304 | 2.22 | 112.0 | 18.3 | 32.1 | 48.2 | 2.95 | 0.4 |
| 32 | 50 | 50/50 | 0.00 | 736 | 512 | 23.0 | 815 | 10.0 | 10.9 | 160 | 16 | 16 | 32 | 0.304 | 2.22 | 224.0 | 20.1 | 41.5 | 65.3 | 3.49 | 1.6 |
| 64 | 50 | 50/50 | 0.00 | 1472 | 1024 | 23.0 | 1638 | 15.0 | 17.3 | 320 | 32 | 32 | 64 | 0.304 | 2.22 | 448.0 | 22.4 | 52.8 | 85.9 | 3.96 | 7.0 |

## The instance each config uses

- m=8, seed 42: |V|=184 (128 walkable), 204 segments, 6 aisles of length 6 to 8, 4 cross-aisles, d^trip 14 to 40 (mean 25.4, ratio 2.72), 1 layout(s) sampled, well-formed True.
- m=16, seed 42: |V|=368 (256 walkable), 409 segments, 7 aisles of length 11 to 16, 9 cross-aisles, d^trip 20 to 52 (mean 32.1, ratio 2.67), 1 layout(s) sampled, well-formed True.
- m=32, seed 42: |V|=736 (512 walkable), 818 segments, 10 aisles of length 12 to 24, 9 cross-aisles, d^trip 21 to 68 (mean 42.5, ratio 3.21), 1 layout(s) sampled, well-formed True.
- m=64, seed 42: |V|=1472 (1024 walkable), 1639 segments, 15 aisles of length 22 to 32, 17 cross-aisles, d^trip 25 to 77 (mean 52.8, ratio 3.04), 1 layout(s) sampled, well-formed True.
