# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 11.0, largest 15.0, ratio 1.36.

| vertex | d_trip |
|---|---|
| 1 | 11.0 |
| 23 | 15.0 |
| 58 | 12.0 |
| 122 | 14.0 |

## demand.rotation_shift = 2

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.12 | 20 | 20 / 20 | 0.196 | 0.933 | 26.350 | 0.050 | 5.850 | 33334.000 | 27338.250 | 29.245 | 9.560 | 130.441 | 0.000 |
| fixed | 0.12 | 20 | 20 / 20 | 0.204 | 0.990 | 2.450 | 0.050 | 11.000 | 19961.450 | 19746.200 | 37.063 | 9.162 | 62.795 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.12 | n/a | 0.072 |
| fixed | 0.12 | n/a | 0.072 |

## demand.rotation_shift = 5

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.12 | 20 | 20 / 20 | 0.197 | 0.939 | 23.550 | 0.000 | 7.750 | 33189.350 | 27120.150 | 24.868 | 9.535 | 134.369 | 0.000 |
| fixed | 0.12 | 20 | 20 / 20 | 0.202 | 0.977 | 7.250 | 0.150 | 10.150 | 23327.900 | 22358.900 | 45.394 | 9.162 | 68.811 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.12 | n/a | 0.072 |
| fixed | 0.12 | n/a | 0.072 |

## demand.rotation_shift = 10

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.12 | 20 | 20 / 20 | 0.200 | 0.962 | 12.700 | 0.000 | 5.650 | 23842.950 | 21899.050 | 31.421 | 9.367 | 86.408 | 0.000 |
| fixed | 0.12 | 20 | 20 / 20 | 0.200 | 0.967 | 11.000 | 0.050 | 8.850 | 20777.100 | 19525.350 | 43.613 | 9.145 | 55.343 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.12 | n/a | 0.072 |
| fixed | 0.12 | n/a | 0.072 |

