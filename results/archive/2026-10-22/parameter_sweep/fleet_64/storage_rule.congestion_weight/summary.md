# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 4.0, largest 56.0, ratio 14.00.

| vertex | d_trip |
|---|---|
| 8 | 11.0 |
| 35 | 5.0 |
| 110 | 15.0 |
| 130 | 36.0 |
| 145 | 16.0 |
| 181 | 17.0 |
| 235 | 8.0 |
| 249 | 9.0 |
| 268 | 29.0 |
| 440 | 20.0 |
| 449 | 38.0 |
| 492 | 4.0 |
| 512 | 30.0 |
| 534 | 15.0 |
| 536 | 15.0 |
| 550 | 41.0 |
| 558 | 6.0 |
| 575 | 26.0 |
| 595 | 8.0 |
| 633 | 22.0 |
| 642 | 40.0 |
| 650 | 56.0 |
| 743 | 21.0 |
| 775 | 18.0 |
| 811 | 23.0 |
| 817 | 31.0 |
| 836 | 13.0 |
| 876 | 21.0 |
| 898 | 9.0 |
| 923 | 32.0 |
| 947 | 23.0 |
| 1019 | 32.0 |

## storage_rule.congestion_weight = 0

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.42 | 20 | 0 / 20 | 0.491 | 0.749 | 249.550 | 57.700 | 75.050 | 415286.800 | 255412.400 | 160.589 | 24.850 | 525.294 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | n/a | 0.42 | n/a |

## storage_rule.congestion_weight = 0.5

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.42 | 20 | 1 / 20 | 0.497 | 0.759 | 244.100 | 48.450 | 75.300 | 410719.700 | 258567.250 | 161.269 | 24.822 | 519.139 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | n/a | 0.42 | n/a |

## storage_rule.congestion_weight = 1

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.42 | 20 | 2 / 20 | 0.497 | 0.758 | 244.900 | 49.550 | 75.000 | 401783.400 | 247398.950 | 158.575 | 24.840 | 487.934 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | n/a | 0.42 | n/a |

## storage_rule.congestion_weight = 2

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.42 | 20 | 2 / 20 | 0.507 | 0.774 | 227.050 | 44.150 | 78.050 | 387862.200 | 247131.700 | 158.121 | 24.810 | 458.397 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | n/a | 0.42 | n/a |

## storage_rule.congestion_weight = 3

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.42 | 20 | 6 / 20 | 0.513 | 0.784 | 223.000 | 37.050 | 72.300 | 377523.900 | 243472.150 | 156.166 | 24.678 | 440.906 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | n/a | 0.42 | n/a |

## storage_rule.congestion_weight = 4

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.42 | 20 | 9 / 20 | 0.520 | 0.796 | 211.100 | 31.400 | 70.600 | 360909.100 | 240786.400 | 154.153 | 24.560 | 420.233 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | n/a | 0.42 | n/a |

