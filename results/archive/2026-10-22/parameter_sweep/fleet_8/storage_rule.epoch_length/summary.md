# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 11.0, largest 15.0, ratio 1.36.

| vertex | d_trip |
|---|---|
| 1 | 11.0 |
| 23 | 15.0 |
| 58 | 12.0 |
| 122 | 14.0 |

## storage_rule.epoch_length = 50

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.12 | 20 | 20 / 20 | 0.208 | 0.936 | 26.450 | 0.000 | 7.350 | 32458.200 | 26445.250 | 24.446 | 5.284 | 114.615 | 0.000 |
| demand | 0.12 | 20 | 20 / 20 | 0.208 | 0.936 | 26.450 | 0.000 | 7.350 | 32458.200 | 26445.250 | 24.446 | 5.284 | 114.615 | 0.000 |
| fixed | 0.12 | 20 | 20 / 20 | 0.210 | 0.953 | 18.550 | 0.150 | 8.900 | 31599.800 | 28352.150 | 49.446 | 5.152 | 89.608 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | 0.12 | n/a | 0.072 |
| demand | 0.12 | n/a | 0.072 |
| fixed | 0.12 | n/a | 0.072 |

## storage_rule.epoch_length = 100

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.12 | 20 | 20 / 20 | 0.197 | 0.939 | 23.550 | 0.000 | 7.750 | 33189.350 | 27120.150 | 24.868 | 9.535 | 134.369 | 0.000 |
| demand | 0.12 | 20 | 20 / 20 | 0.197 | 0.939 | 23.550 | 0.000 | 7.750 | 33189.350 | 27120.150 | 24.868 | 9.535 | 134.369 | 0.000 |
| fixed | 0.12 | 20 | 20 / 20 | 0.202 | 0.977 | 7.250 | 0.150 | 10.150 | 23327.900 | 22358.900 | 45.394 | 9.162 | 68.811 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | 0.12 | n/a | 0.072 |
| demand | 0.12 | n/a | 0.072 |
| fixed | 0.12 | n/a | 0.072 |

## storage_rule.epoch_length = 200

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.12 | 20 | 20 / 20 | 0.186 | 0.959 | 13.150 | 0.150 | 6.450 | 33492.700 | 29830.150 | 26.485 | 16.495 | 172.335 | 0.000 |
| demand | 0.12 | 20 | 20 / 20 | 0.186 | 0.959 | 13.150 | 0.150 | 6.450 | 33492.700 | 29830.150 | 26.485 | 16.495 | 172.335 | 0.000 |
| fixed | 0.12 | 20 | 20 / 20 | 0.188 | 0.989 | 2.450 | 0.150 | 10.100 | 19884.550 | 19617.750 | 41.013 | 15.590 | 70.557 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | 0.12 | n/a | 0.072 |
| demand | 0.12 | n/a | 0.072 |
| fixed | 0.12 | n/a | 0.072 |

## storage_rule.epoch_length = 400

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.12 | 20 | 20 / 20 | 0.171 | 0.974 | 6.850 | 0.300 | 7.100 | 30885.650 | 28260.750 | 26.760 | 28.200 | 202.335 | 0.000 |
| demand | 0.12 | 20 | 20 / 20 | 0.171 | 0.974 | 6.850 | 0.300 | 7.100 | 30885.650 | 28260.750 | 26.760 | 28.200 | 202.335 | 0.000 |
| fixed | 0.12 | 20 | 20 / 20 | 0.172 | 0.991 | 1.400 | 0.200 | 8.500 | 20029.650 | 19903.450 | 38.075 | 26.820 | 99.866 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | 0.12 | n/a | 0.072 |
| demand | 0.12 | n/a | 0.072 |
| fixed | 0.12 | n/a | 0.072 |

