# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 11.0, largest 15.0, ratio 1.36.

| vertex | d_trip |
|---|---|
| 1 | 11.0 |
| 23 | 15.0 |
| 58 | 12.0 |
| 122 | 14.0 |

## arrival.margin = 0.25

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.12 | 20 | 20 / 20 | 0.197 | 0.936 | 24.650 | 0.000 | 7.400 | 33092.400 | 26763.650 | 24.711 | 9.553 | 133.303 | 0.000 |
| fixed | 0.12 | 20 | 20 / 20 | 0.202 | 0.976 | 7.950 | 0.150 | 10.100 | 24044.850 | 22965.900 | 47.224 | 9.205 | 69.690 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.12 | n/a | 0.072 |
| fixed | 0.12 | n/a | 0.072 |

## arrival.margin = 0.5

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.12 | 20 | 20 / 20 | 0.197 | 0.938 | 24.050 | 0.000 | 6.800 | 32755.750 | 26631.300 | 24.798 | 9.527 | 132.114 | 0.000 |
| fixed | 0.12 | 20 | 20 / 20 | 0.202 | 0.977 | 7.500 | 0.150 | 10.150 | 23620.050 | 22610.600 | 46.091 | 9.192 | 69.234 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.12 | n/a | 0.072 |
| fixed | 0.12 | n/a | 0.072 |

## arrival.margin = 1

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

## arrival.margin = 1.5

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.12 | 20 | 20 / 20 | 0.198 | 0.942 | 22.000 | 0.000 | 6.300 | 35085.300 | 28929.200 | 24.879 | 9.512 | 145.430 | 0.000 |
| fixed | 0.12 | 20 | 20 / 20 | 0.201 | 0.979 | 6.350 | 0.150 | 10.250 | 23038.250 | 22179.250 | 45.234 | 9.080 | 68.286 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.12 | n/a | 0.072 |
| fixed | 0.12 | n/a | 0.072 |

## arrival.margin = 2

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.12 | 20 | 20 / 20 | 0.200 | 0.954 | 17.000 | 0.000 | 6.500 | 34637.350 | 29519.550 | 25.518 | 9.460 | 144.554 | 0.000 |
| fixed | 0.12 | 20 | 20 / 20 | 0.200 | 0.979 | 6.250 | 0.150 | 11.250 | 22834.100 | 21959.500 | 46.288 | 8.963 | 66.260 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.12 | n/a | 0.072 |
| fixed | 0.12 | n/a | 0.072 |

