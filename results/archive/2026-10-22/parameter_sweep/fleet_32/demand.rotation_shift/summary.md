# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 5.0, largest 35.0, ratio 7.00.

| vertex | d_trip |
|---|---|
| 23 | 35.0 |
| 74 | 7.0 |
| 80 | 11.0 |
| 95 | 32.0 |
| 102 | 9.0 |
| 115 | 5.0 |
| 145 | 10.0 |
| 161 | 29.0 |
| 223 | 16.0 |
| 229 | 21.0 |
| 252 | 20.0 |
| 292 | 16.0 |
| 305 | 26.0 |
| 365 | 15.0 |
| 366 | 17.0 |
| 459 | 12.0 |

## demand.rotation_shift = 2

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.36 | 20 | 20 / 20 | 0.502 | 0.878 | 123.050 | 5.600 | 23.550 | 176720.300 | 125347.350 | 62.846 | 22.270 | 261.861 | 0.000 |
| fixed | 0.36 | 20 | 20 / 20 | 0.510 | 0.916 | 55.900 | 28.850 | 29.250 | 118494.400 | 98472.000 | 95.950 | 20.587 | 97.468 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.36 | n/a | 0.216 |
| fixed | 0.36 | n/a | 0.216 |

## demand.rotation_shift = 5

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.36 | 20 | 20 / 20 | 0.496 | 0.864 | 139.000 | 6.300 | 21.400 | 155726.500 | 97539.400 | 49.975 | 22.512 | 208.590 | 0.000 |
| fixed | 0.36 | 20 | 20 / 20 | 0.527 | 0.949 | 37.050 | 8.300 | 29.700 | 102950.550 | 93075.850 | 90.512 | 20.480 | 83.827 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.36 | n/a | 0.216 |
| fixed | 0.36 | n/a | 0.216 |

## demand.rotation_shift = 10

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.36 | 20 | 20 / 20 | 0.498 | 0.870 | 133.200 | 4.200 | 25.450 | 158536.450 | 100057.600 | 53.903 | 22.232 | 205.520 | 0.000 |
| fixed | 0.36 | 20 | 20 / 20 | 0.523 | 0.944 | 47.100 | 0.900 | 29.750 | 93643.550 | 81168.350 | 78.679 | 20.288 | 75.413 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.36 | n/a | 0.216 |
| fixed | 0.36 | n/a | 0.216 |

