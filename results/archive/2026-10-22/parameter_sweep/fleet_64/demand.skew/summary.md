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

## demand.skew = 0.5

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.42 | 20 | 0 / 20 | 0.502 | 0.683 | 407.400 | 37.850 | 80.250 | 531551.150 | 241339.400 | 125.653 | 33.375 | 557.471 | 0.000 |
| fixed | 0.42 | 20 | 20 / 20 | 0.678 | 0.939 | 61.900 | 0.050 | 74.550 | 150700.800 | 133450.050 | 124.746 | 31.925 | 64.493 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | n/a | 0.42 | n/a |
| fixed | 0.42 | n/a | 0.252 |

## demand.skew = 1

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

## demand.skew = 1.5

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.42 | 20 | 20 / 20 | 0.499 | 0.867 | 113.250 | 15.450 | 62.050 | 260090.250 | 215350.050 | 175.873 | 16.430 | 331.826 | 0.000 |
| fixed | 0.42 | 20 | 20 / 20 | 0.480 | 0.875 | 109.450 | 8.700 | 54.350 | 172286.650 | 140187.350 | 173.320 | 13.468 | 68.283 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.42 | n/a | 0.252 |
| fixed | 0.42 | n/a | 0.252 |

