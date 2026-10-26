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

## storage_rule.epoch_length = 50

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.15 | 20 | 20 / 20 | 0.264 | 0.976 | 8.700 | 0.000 | 32.900 | 77971.050 | 75991.850 | 82.532 | 6.329 | 213.688 | 0.000 |
| demand | 0.15 | 20 | 20 / 20 | 0.246 | 0.909 | 44.250 | 0.050 | 30.900 | 103281.500 | 90632.150 | 92.665 | 6.341 | 303.708 | 0.000 |
| fixed | 0.15 | 20 | 20 / 20 | 0.248 | 0.928 | 34.600 | 0.350 | 24.900 | 49573.700 | 44048.450 | 98.138 | 6.178 | 76.259 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | 0.15 | n/a | 0.09 |
| demand | 0.15 | n/a | 0.09 |
| fixed | 0.15 | n/a | 0.09 |

## storage_rule.epoch_length = 100

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.15 | 20 | 20 / 20 | 0.246 | 0.973 | 9.500 | 0.000 | 31.650 | 60866.650 | 58853.350 | 77.371 | 11.183 | 174.492 | 0.000 |
| demand | 0.15 | 20 | 20 / 20 | 0.233 | 0.920 | 35.350 | 0.100 | 30.800 | 82330.850 | 71780.100 | 86.376 | 11.203 | 255.317 | 0.000 |
| fixed | 0.15 | 20 | 20 / 20 | 0.234 | 0.938 | 26.200 | 0.300 | 25.350 | 40561.750 | 36255.650 | 89.143 | 10.770 | 60.490 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | 0.15 | n/a | 0.09 |
| demand | 0.15 | n/a | 0.09 |
| fixed | 0.15 | n/a | 0.09 |

## storage_rule.epoch_length = 200

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.15 | 20 | 20 / 20 | 0.226 | 0.970 | 9.550 | 0.200 | 28.400 | 47841.750 | 45191.150 | 72.505 | 19.020 | 144.140 | 0.000 |
| demand | 0.15 | 20 | 20 / 20 | 0.222 | 0.952 | 17.350 | 0.200 | 31.150 | 61083.600 | 55405.300 | 81.829 | 19.135 | 197.033 | 0.000 |
| fixed | 0.15 | 20 | 20 / 20 | 0.217 | 0.948 | 19.000 | 0.200 | 25.750 | 35381.400 | 32030.950 | 80.048 | 18.100 | 62.319 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | 0.15 | n/a | 0.09 |
| demand | 0.15 | n/a | 0.09 |
| fixed | 0.15 | n/a | 0.09 |

## storage_rule.epoch_length = 400

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.15 | 20 | 20 / 20 | 0.203 | 0.964 | 10.350 | 0.750 | 24.050 | 43805.550 | 40556.150 | 69.066 | 31.770 | 168.119 | 0.000 |
| demand | 0.15 | 20 | 20 / 20 | 0.203 | 0.963 | 10.700 | 0.750 | 26.100 | 48619.750 | 45088.900 | 75.048 | 32.040 | 188.943 | 0.000 |
| fixed | 0.15 | 20 | 20 / 20 | 0.200 | 0.960 | 11.300 | 0.750 | 20.350 | 33725.450 | 31224.400 | 77.401 | 30.450 | 78.142 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | 0.15 | n/a | 0.09 |
| demand | 0.15 | n/a | 0.09 |
| fixed | 0.15 | n/a | 0.09 |

