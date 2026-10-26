# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 11.0, largest 15.0, ratio 1.36.

| vertex | d_trip |
|---|---|
| 1 | 11.0 |
| 23 | 15.0 |
| 58 | 12.0 |
| 122 | 14.0 |

## Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fixed | 0.2 | 50 | 50 / 50 | 0.289 | 0.874 | 11.180 | 104692.140 | 81772.660 | 146.934 | 13.650 | 133.078 | 0.000 |
| fixed | 0.3 | 50 | 17 / 50 | 0.380 | 0.791 | 10.480 | 254165.160 | 167872.140 | 262.799 | 18.943 | 166.557 | 14.820 |
| fixed | 0.4 | 50 | 0 / 50 | 0.401 | 0.685 | 9.680 | 432791.500 | 222951.160 | 345.565 | 19.198 | 190.459 | 981.040 |
| fixed | 0.5 | 50 | 0 / 50 | 0.391 | 0.585 | 9.560 | 612214.420 | 259586.880 | 430.252 | 17.206 | 194.232 | 2912.480 |

## Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| fixed | 0.2 | 0.3 | 0.12 |
