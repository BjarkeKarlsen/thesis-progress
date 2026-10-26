# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 6.0, largest 17.0, ratio 2.83.

| vertex | d_trip |
|---|---|
| 6 | 14.0 |
| 12 | 10.0 |
| 20 | 17.0 |
| 36 | 14.0 |
| 43 | 6.0 |
| 65 | 12.0 |
| 217 | 10.0 |
| 223 | 16.0 |

## demand.rotation_period = 100

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.15 | 20 | 20 / 20 | 0.245 | 0.962 | 14.250 | 0.000 | 29.750 | 53275.900 | 49437.500 | 74.646 | 11.353 | 134.561 | 0.000 |
| fixed | 0.15 | 20 | 20 / 20 | 0.240 | 0.962 | 12.750 | 0.000 | 32.700 | 40987.050 | 37851.550 | 91.148 | 10.793 | 60.845 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.15 | n/a | 0.09 |
| fixed | 0.15 | n/a | 0.09 |

## demand.rotation_period = 200

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.15 | 20 | 20 / 20 | 0.233 | 0.920 | 35.350 | 0.100 | 30.800 | 82330.850 | 71780.100 | 86.376 | 11.203 | 255.317 | 0.000 |
| fixed | 0.15 | 20 | 20 / 20 | 0.234 | 0.938 | 26.200 | 0.300 | 25.350 | 40561.750 | 36255.650 | 89.143 | 10.770 | 60.490 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.15 | n/a | 0.09 |
| fixed | 0.15 | n/a | 0.09 |

## demand.rotation_period = 400

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.15 | 20 | 20 / 20 | 0.226 | 0.900 | 42.200 | 3.200 | 31.100 | 112509.150 | 99551.200 | 135.652 | 11.008 | 351.023 | 0.000 |
| fixed | 0.15 | 20 | 20 / 20 | 0.231 | 0.927 | 31.250 | 1.150 | 25.550 | 44087.900 | 37270.600 | 93.083 | 10.742 | 63.067 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.15 | n/a | 0.09 |
| fixed | 0.15 | n/a | 0.09 |

