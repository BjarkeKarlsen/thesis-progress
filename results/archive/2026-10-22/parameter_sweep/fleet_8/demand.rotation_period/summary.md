# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 11.0, largest 15.0, ratio 1.36.

| vertex | d_trip |
|---|---|
| 1 | 11.0 |
| 23 | 15.0 |
| 58 | 12.0 |
| 122 | 14.0 |

## demand.rotation_period = 100

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.12 | 20 | 20 / 20 | 0.200 | 0.958 | 14.650 | 0.000 | 6.100 | 24529.800 | 22277.150 | 32.289 | 9.433 | 87.729 | 0.000 |
| fixed | 0.12 | 20 | 20 / 20 | 0.199 | 0.961 | 13.250 | 0.000 | 9.650 | 22654.150 | 20808.700 | 47.319 | 9.172 | 58.648 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.12 | n/a | 0.072 |
| fixed | 0.12 | n/a | 0.072 |

## demand.rotation_period = 200

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

## demand.rotation_period = 400

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.12 | 20 | 20 / 20 | 0.197 | 0.937 | 24.250 | 0.350 | 6.500 | 31284.000 | 25978.500 | 28.902 | 9.530 | 121.820 | 0.000 |
| fixed | 0.12 | 20 | 20 / 20 | 0.204 | 0.991 | 1.650 | 0.000 | 11.150 | 19539.800 | 19376.400 | 37.099 | 9.128 | 60.660 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.12 | n/a | 0.072 |
| fixed | 0.12 | n/a | 0.072 |

