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

## arrival.margin = 0.25

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.15 | 20 | 20 / 20 | 0.232 | 0.914 | 38.550 | 0.100 | 31.200 | 84658.550 | 73638.100 | 87.426 | 11.255 | 266.287 | 0.000 |
| fixed | 0.15 | 20 | 20 / 20 | 0.235 | 0.938 | 27.100 | 0.200 | 28.800 | 40708.200 | 36370.750 | 88.790 | 10.865 | 61.089 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.15 | n/a | 0.09 |
| fixed | 0.15 | n/a | 0.09 |

## arrival.margin = 0.5

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.15 | 20 | 20 / 20 | 0.232 | 0.913 | 39.200 | 0.050 | 30.850 | 84776.950 | 73493.600 | 87.355 | 11.240 | 266.603 | 0.000 |
| fixed | 0.15 | 20 | 20 / 20 | 0.235 | 0.938 | 26.700 | 0.200 | 28.650 | 40367.200 | 36003.550 | 87.916 | 10.838 | 60.550 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.15 | n/a | 0.09 |
| fixed | 0.15 | n/a | 0.09 |

## arrival.margin = 1

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

## arrival.margin = 1.5

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.15 | 20 | 20 / 20 | 0.237 | 0.936 | 27.800 | 0.000 | 35.050 | 77666.750 | 69597.900 | 83.969 | 11.125 | 239.061 | 0.000 |
| fixed | 0.15 | 20 | 20 / 20 | 0.233 | 0.939 | 25.800 | 0.150 | 28.150 | 40086.200 | 35861.100 | 88.310 | 10.650 | 60.100 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.15 | n/a | 0.09 |
| fixed | 0.15 | n/a | 0.09 |

## arrival.margin = 2

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.15 | 20 | 20 / 20 | 0.239 | 0.949 | 21.050 | 0.100 | 30.100 | 72099.250 | 65730.200 | 85.727 | 11.043 | 211.819 | 0.000 |
| fixed | 0.15 | 20 | 20 / 20 | 0.232 | 0.938 | 26.250 | 0.300 | 28.150 | 40284.300 | 35875.250 | 89.848 | 10.497 | 58.946 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.15 | n/a | 0.09 |
| fixed | 0.15 | n/a | 0.09 |

