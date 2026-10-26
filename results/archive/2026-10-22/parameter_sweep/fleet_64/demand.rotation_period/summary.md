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

## demand.rotation_period = 100

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.42 | 20 | 19 / 20 | 0.548 | 0.837 | 178.700 | 9.100 | 82.750 | 332694.600 | 252831.100 | 139.677 | 24.732 | 421.593 | 0.000 |
| fixed | 0.42 | 20 | 20 / 20 | 0.566 | 0.902 | 91.400 | 5.350 | 72.150 | 167046.950 | 139299.100 | 151.124 | 21.695 | 72.817 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | n/a | 0.42 | n/a |
| fixed | 0.42 | n/a | 0.252 |

## demand.rotation_period = 200

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.42 | 20 | 0 / 20 | 0.491 | 0.749 | 249.550 | 57.700 | 75.050 | 415286.800 | 255412.400 | 160.589 | 24.850 | 525.294 | 0.000 |
| fixed | 0.42 | 20 | 20 / 20 | 0.578 | 0.911 | 82.550 | 7.000 | 71.550 | 159978.100 | 135038.150 | 144.577 | 22.535 | 67.890 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | n/a | 0.42 | n/a |
| fixed | 0.42 | n/a | 0.252 |

## demand.rotation_period = 400

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.42 | 20 | 0 / 20 | 0.441 | 0.673 | 268.400 | 143.100 | 69.250 | 481401.750 | 242670.400 | 164.377 | 24.875 | 607.301 | 0.000 |
| fixed | 0.42 | 20 | 20 / 20 | 0.580 | 0.912 | 84.200 | 8.950 | 74.850 | 157045.450 | 134481.300 | 141.990 | 22.718 | 70.394 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | n/a | 0.42 | n/a |
| fixed | 0.42 | n/a | 0.252 |

