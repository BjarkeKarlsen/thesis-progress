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

## storage_rule.epoch_length = 50

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.42 | 20 | 0 / 20 | 0.480 | 0.672 | 353.150 | 94.600 | 73.200 | 542836.250 | 261231.450 | 155.461 | 15.099 | 573.478 | 0.000 |
| demand | 0.42 | 20 | 0 / 20 | 0.468 | 0.655 | 370.200 | 102.800 | 71.150 | 549780.400 | 258833.450 | 154.827 | 15.154 | 608.595 | 0.000 |
| fixed | 0.42 | 20 | 20 / 20 | 0.624 | 0.904 | 94.900 | 12.800 | 71.300 | 191562.850 | 164163.600 | 156.311 | 13.889 | 95.728 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | n/a | 0.42 | n/a |
| demand | n/a | 0.42 | n/a |
| fixed | 0.42 | n/a | 0.252 |

## storage_rule.epoch_length = 100

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.42 | 20 | 2 / 20 | 0.497 | 0.758 | 244.900 | 49.550 | 75.000 | 401783.400 | 247398.950 | 158.575 | 24.840 | 487.934 | 0.000 |
| demand | 0.42 | 20 | 0 / 20 | 0.491 | 0.749 | 249.550 | 57.700 | 75.050 | 415286.800 | 255412.400 | 160.589 | 24.850 | 525.294 | 0.000 |
| fixed | 0.42 | 20 | 20 / 20 | 0.578 | 0.911 | 82.550 | 7.000 | 71.550 | 159978.100 | 135038.150 | 144.577 | 22.535 | 67.890 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | n/a | 0.42 | n/a |
| demand | n/a | 0.42 | n/a |
| fixed | 0.42 | n/a | 0.252 |

## storage_rule.epoch_length = 200

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.42 | 20 | 20 / 20 | 0.516 | 0.870 | 111.250 | 22.350 | 69.800 | 263059.800 | 208706.500 | 142.475 | 38.355 | 364.788 | 0.000 |
| demand | 0.42 | 20 | 20 / 20 | 0.509 | 0.857 | 126.850 | 22.500 | 70.350 | 272872.100 | 210792.850 | 143.509 | 38.645 | 385.905 | 0.000 |
| fixed | 0.42 | 20 | 20 / 20 | 0.529 | 0.917 | 61.650 | 10.700 | 73.850 | 143108.750 | 120675.500 | 133.756 | 34.635 | 67.164 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | 0.42 | n/a | 0.252 |
| demand | 0.42 | n/a | 0.252 |
| fixed | 0.42 | n/a | 0.252 |

## storage_rule.epoch_length = 400

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.42 | 20 | 20 / 20 | 0.473 | 0.891 | 70.400 | 26.450 | 78.400 | 205301.500 | 167192.350 | 140.306 | 55.220 | 313.418 | 0.000 |
| demand | 0.42 | 20 | 20 / 20 | 0.470 | 0.885 | 72.950 | 30.100 | 73.550 | 208496.250 | 167544.450 | 140.572 | 55.330 | 322.736 | 0.000 |
| fixed | 0.42 | 20 | 20 / 20 | 0.475 | 0.909 | 49.050 | 24.550 | 57.050 | 139881.200 | 116341.050 | 135.426 | 50.650 | 74.809 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | 0.42 | n/a | 0.252 |
| demand | 0.42 | n/a | 0.252 |
| fixed | 0.42 | n/a | 0.252 |

