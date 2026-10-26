# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 11.0, largest 15.0, ratio 1.36.

| vertex | d_trip |
|---|---|
| 1 | 11.0 |
| 23 | 15.0 |
| 58 | 12.0 |
| 122 | 14.0 |

## demand.skew = 0.5

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.12 | 20 | 20 / 20 | 0.212 | 0.941 | 24.500 | 0.000 | 5.950 | 34128.250 | 28323.800 | 26.716 | 11.155 | 117.043 | 0.000 |
| fixed | 0.12 | 20 | 20 / 20 | 0.222 | 0.988 | 3.300 | 0.000 | 9.950 | 19437.300 | 19006.500 | 34.874 | 11.075 | 51.648 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.12 | n/a | 0.072 |
| fixed | 0.12 | n/a | 0.072 |

## demand.skew = 1

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

## demand.skew = 1.5

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.12 | 20 | 20 / 20 | 0.182 | 0.991 | 1.450 | 0.100 | 7.200 | 15433.150 | 15217.700 | 27.630 | 6.755 | 67.928 | 0.000 |
| fixed | 0.12 | 20 | 20 / 20 | 0.174 | 0.974 | 6.100 | 0.950 | 9.250 | 21193.850 | 20367.950 | 60.171 | 6.200 | 54.953 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.12 | n/a | 0.072 |
| fixed | 0.12 | n/a | 0.072 |

