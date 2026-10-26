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

## storage_rule.epoch_length = 50

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.36 | 20 | 20 / 20 | 0.537 | 0.862 | 154.900 | 6.300 | 25.250 | 197236.750 | 133984.050 | 56.086 | 13.456 | 248.063 | 0.000 |
| demand | 0.36 | 20 | 20 / 20 | 0.538 | 0.863 | 154.300 | 6.250 | 25.250 | 196159.100 | 133412.100 | 55.996 | 13.457 | 246.424 | 0.000 |
| fixed | 0.36 | 20 | 20 / 20 | 0.562 | 0.930 | 55.700 | 16.200 | 31.950 | 145992.050 | 129584.550 | 105.077 | 12.484 | 129.639 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | 0.36 | n/a | 0.216 |
| demand | 0.36 | n/a | 0.216 |
| fixed | 0.36 | n/a | 0.216 |

## storage_rule.epoch_length = 100

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.36 | 20 | 20 / 20 | 0.497 | 0.865 | 138.000 | 6.150 | 22.000 | 155370.100 | 97612.100 | 49.844 | 22.505 | 208.732 | 0.000 |
| demand | 0.36 | 20 | 20 / 20 | 0.496 | 0.864 | 139.000 | 6.300 | 21.400 | 155726.500 | 97539.400 | 49.975 | 22.512 | 208.590 | 0.000 |
| fixed | 0.36 | 20 | 20 / 20 | 0.527 | 0.949 | 37.050 | 8.300 | 29.700 | 102950.550 | 93075.850 | 90.512 | 20.480 | 83.827 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | 0.36 | n/a | 0.216 |
| demand | 0.36 | n/a | 0.216 |
| fixed | 0.36 | n/a | 0.216 |

## storage_rule.epoch_length = 200

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.36 | 20 | 20 / 20 | 0.459 | 0.880 | 97.800 | 17.850 | 23.100 | 142399.900 | 99630.800 | 58.064 | 35.680 | 254.434 | 0.000 |
| demand | 0.36 | 20 | 20 / 20 | 0.459 | 0.880 | 97.750 | 17.900 | 23.100 | 142314.800 | 99563.150 | 58.129 | 35.705 | 253.817 | 0.000 |
| fixed | 0.36 | 20 | 20 / 20 | 0.488 | 0.965 | 17.400 | 6.750 | 28.800 | 78052.100 | 74115.500 | 77.077 | 31.875 | 72.521 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | 0.36 | n/a | 0.216 |
| demand | 0.36 | n/a | 0.216 |
| fixed | 0.36 | n/a | 0.216 |

## storage_rule.epoch_length = 400

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.36 | 20 | 20 / 20 | 0.424 | 0.910 | 49.200 | 25.650 | 20.600 | 114711.350 | 88858.350 | 63.986 | 52.470 | 265.919 | 0.000 |
| demand | 0.36 | 20 | 20 / 20 | 0.423 | 0.909 | 49.950 | 25.800 | 19.950 | 114874.200 | 88664.350 | 63.919 | 52.490 | 266.203 | 0.000 |
| fixed | 0.36 | 20 | 20 / 20 | 0.442 | 0.967 | 6.900 | 15.750 | 27.900 | 69660.450 | 66542.750 | 72.834 | 47.750 | 82.856 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | 0.36 | n/a | 0.216 |
| demand | 0.36 | n/a | 0.216 |
| fixed | 0.36 | n/a | 0.216 |

