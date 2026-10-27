# Warehouse instances

Means over the seeds per fleet size. The discard rate is the share of sampled layouts
that no role placement made well-formed. `used` is the instance of the config's seed.

| m | seeds | pass | discard | V | walkable | V per agent | segments | aisles | cross-aisles | str | del | rcv | ep | role share | degree | roles on leaves | d^trip min | d^trip mean | d^trip max | d^trip ratio | seconds |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 8 | 50 | 50/50 | 0.00 | 200 | 128 | 25.0 | 221 | 6.0 | 4.2 | 40 | 4 | 4 | 24 | 0.360 | 2.21 | 71.9 | 10.4 | 21.3 | 33.4 | 3.46 | 0.2 |
| 16 | 50 | 50/50 | 0.00 | 403 | 256 | 25.2 | 444 | 7.0 | 7.9 | 60 | 8 | 8 | 71 | 0.365 | 2.20 | 147.2 | 12.4 | 26.2 | 42.9 | 3.56 | 0.5 |
| 32 | 50 | 50/50 | 0.00 | 786 | 512 | 24.6 | 865 | 10.0 | 10.9 | 100 | 16 | 16 | 142 | 0.349 | 2.20 | 274.1 | 15.2 | 33.9 | 55.0 | 3.66 | 2.1 |
| 64 | 50 | 50/50 | 0.00 | 1591 | 1024 | 24.9 | 1757 | 15.0 | 17.3 | 200 | 32 | 32 | 303 | 0.357 | 2.21 | 567.4 | 19.1 | 45.2 | 74.2 | 3.92 | 8.5 |

## The instance each config uses

- m=8, seed 42: |V|=203 (128 walkable), 223 segments, 6 aisles of length 6 to 8, 4 cross-aisles, d^trip 12 to 32 (mean 22.0, ratio 2.83), 1 layout(s) sampled, well-formed True.
- m=16, seed 42: |V|=403 (256 walkable), 444 segments, 7 aisles of length 11 to 16, 9 cross-aisles, d^trip 11 to 38 (mean 27.8, ratio 3.38), 1 layout(s) sampled, well-formed True.
- m=32, seed 42: |V|=786 (512 walkable), 868 segments, 10 aisles of length 12 to 24, 9 cross-aisles, d^trip 16 to 60 (mean 34.1, ratio 3.84), 1 layout(s) sampled, well-formed True.
- m=64, seed 42: |V|=1594 (1024 walkable), 1761 segments, 15 aisles of length 22 to 32, 17 cross-aisles, d^trip 21 to 70 (mean 44.7, ratio 3.29), 1 layout(s) sampled, well-formed True.
