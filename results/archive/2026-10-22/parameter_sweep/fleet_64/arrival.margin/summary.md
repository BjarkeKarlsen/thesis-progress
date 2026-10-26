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

## arrival.margin = 0.25

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.42 | 20 | 0 / 20 | 0.470 | 0.712 | 272.000 | 86.250 | 70.400 | 447892.600 | 251350.700 | 161.829 | 25.262 | 570.872 | 0.000 |
| fixed | 0.42 | 20 | 20 / 20 | 0.585 | 0.914 | 82.300 | 5.100 | 71.350 | 162590.600 | 138431.550 | 146.945 | 23.137 | 69.299 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | n/a | 0.42 | n/a |
| fixed | 0.42 | n/a | 0.252 |

## arrival.margin = 0.5

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.42 | 20 | 0 / 20 | 0.472 | 0.717 | 272.050 | 79.450 | 69.950 | 442912.150 | 251774.050 | 162.249 | 25.205 | 563.910 | 0.000 |
| fixed | 0.42 | 20 | 20 / 20 | 0.583 | 0.913 | 83.150 | 4.550 | 67.200 | 161899.600 | 137266.450 | 146.122 | 22.928 | 68.760 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | n/a | 0.42 | n/a |
| fixed | 0.42 | n/a | 0.252 |

## arrival.margin = 1

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

## arrival.margin = 1.5

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.42 | 20 | 3 / 20 | 0.510 | 0.779 | 228.350 | 38.150 | 78.000 | 389075.750 | 260368.550 | 158.362 | 24.755 | 500.641 | 0.000 |
| fixed | 0.42 | 20 | 20 / 20 | 0.574 | 0.912 | 84.250 | 3.250 | 71.650 | 159434.200 | 134954.200 | 145.456 | 22.027 | 67.133 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | n/a | 0.42 | n/a |
| fixed | 0.42 | n/a | 0.252 |

## arrival.margin = 2

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.42 | 20 | 15 / 20 | 0.524 | 0.803 | 207.950 | 24.650 | 75.500 | 362111.750 | 259107.750 | 153.507 | 24.363 | 476.100 | 0.000 |
| fixed | 0.42 | 20 | 20 / 20 | 0.569 | 0.911 | 80.400 | 6.350 | 65.650 | 154397.900 | 129782.900 | 140.868 | 21.385 | 64.743 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | n/a | 0.42 | n/a |
| fixed | 0.42 | n/a | 0.252 |

