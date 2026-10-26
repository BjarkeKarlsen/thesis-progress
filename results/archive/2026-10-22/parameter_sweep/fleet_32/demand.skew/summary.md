# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 5.0, largest 35.0, ratio 7.00.

| vertex | d_trip |
|---|---|
| 23 | 35.0 |
| 74 | 7.0 |
| 80 | 11.0 |
| 95 | 32.0 |
| 102 | 9.0 |
| 115 | 5.0 |
| 145 | 10.0 |
| 161 | 29.0 |
| 223 | 16.0 |
| 229 | 21.0 |
| 252 | 20.0 |
| 292 | 16.0 |
| 305 | 26.0 |
| 365 | 15.0 |
| 366 | 17.0 |
| 459 | 12.0 |

## demand.skew = 0.5

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.36 | 20 | 20 / 20 | 0.541 | 0.848 | 184.200 | 0.400 | 23.550 | 197665.550 | 112221.850 | 42.439 | 29.275 | 215.265 | 0.000 |
| fixed | 0.36 | 20 | 20 / 20 | 0.612 | 0.972 | 22.650 | 0.000 | 31.550 | 89470.750 | 85710.500 | 64.710 | 28.218 | 76.479 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.36 | n/a | 0.216 |
| fixed | 0.36 | n/a | 0.216 |

## demand.skew = 1

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.36 | 20 | 20 / 20 | 0.496 | 0.864 | 139.000 | 6.300 | 21.400 | 155726.500 | 97539.400 | 49.975 | 22.512 | 208.590 | 0.000 |
| fixed | 0.36 | 20 | 20 / 20 | 0.527 | 0.949 | 37.050 | 8.300 | 29.700 | 102950.550 | 93075.850 | 90.512 | 20.480 | 83.827 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.36 | n/a | 0.216 |
| fixed | 0.36 | n/a | 0.216 |

## demand.skew = 1.5

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.36 | 20 | 20 / 20 | 0.457 | 0.908 | 68.350 | 11.600 | 24.450 | 111738.950 | 90630.850 | 73.361 | 14.985 | 173.128 | 0.000 |
| fixed | 0.36 | 20 | 20 / 20 | 0.446 | 0.930 | 47.650 | 6.150 | 27.900 | 123169.750 | 111765.200 | 140.753 | 12.445 | 80.473 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.36 | n/a | 0.216 |
| fixed | 0.36 | n/a | 0.216 |

