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

## arrival.margin = 0.25

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.36 | 20 | 20 / 20 | 0.502 | 0.871 | 133.050 | 5.100 | 22.750 | 160298.700 | 105363.950 | 51.794 | 22.747 | 222.652 | 0.000 |
| fixed | 0.36 | 20 | 20 / 20 | 0.531 | 0.948 | 36.100 | 10.100 | 30.150 | 105253.250 | 94913.350 | 91.029 | 21.005 | 85.926 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.36 | n/a | 0.216 |
| fixed | 0.36 | n/a | 0.216 |

## arrival.margin = 0.5

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.36 | 20 | 20 / 20 | 0.499 | 0.868 | 135.550 | 5.400 | 22.800 | 159781.800 | 103828.400 | 51.417 | 22.630 | 221.828 | 0.000 |
| fixed | 0.36 | 20 | 20 / 20 | 0.530 | 0.949 | 34.000 | 10.350 | 29.850 | 104512.600 | 94537.350 | 91.090 | 20.835 | 85.227 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.36 | n/a | 0.216 |
| fixed | 0.36 | n/a | 0.216 |

## arrival.margin = 1

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

## arrival.margin = 1.5

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.36 | 20 | 20 / 20 | 0.495 | 0.867 | 134.950 | 7.100 | 21.800 | 155206.200 | 100547.750 | 50.164 | 22.205 | 218.488 | 0.000 |
| fixed | 0.36 | 20 | 20 / 20 | 0.523 | 0.949 | 36.550 | 7.400 | 30.650 | 100639.050 | 91251.850 | 90.066 | 19.977 | 81.604 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.36 | n/a | 0.216 |
| fixed | 0.36 | n/a | 0.216 |

## arrival.margin = 2

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.36 | 20 | 20 / 20 | 0.495 | 0.867 | 133.300 | 8.100 | 22.600 | 156321.250 | 101349.050 | 49.649 | 22.105 | 223.806 | 0.000 |
| fixed | 0.36 | 20 | 20 / 20 | 0.520 | 0.952 | 34.500 | 5.050 | 31.200 | 97296.050 | 88754.900 | 88.664 | 19.425 | 78.666 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.36 | n/a | 0.216 |
| fixed | 0.36 | n/a | 0.216 |

