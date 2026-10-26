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

## demand.rotation_period = 100

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.36 | 20 | 20 / 20 | 0.498 | 0.868 | 134.900 | 4.250 | 22.900 | 165631.250 | 103756.900 | 52.692 | 22.465 | 221.165 | 0.000 |
| fixed | 0.36 | 20 | 20 / 20 | 0.526 | 0.955 | 35.250 | 1.800 | 28.400 | 95332.850 | 86778.950 | 85.007 | 19.925 | 77.428 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.36 | n/a | 0.216 |
| fixed | 0.36 | n/a | 0.216 |

## demand.rotation_period = 200

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

## demand.rotation_period = 400

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.36 | 20 | 20 / 20 | 0.501 | 0.876 | 122.100 | 8.600 | 25.950 | 190096.900 | 138432.650 | 67.653 | 22.262 | 294.964 | 0.000 |
| fixed | 0.36 | 20 | 20 / 20 | 0.514 | 0.924 | 53.350 | 22.500 | 31.500 | 120500.600 | 101283.600 | 100.689 | 20.625 | 94.129 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.36 | n/a | 0.216 |
| fixed | 0.36 | n/a | 0.216 |

