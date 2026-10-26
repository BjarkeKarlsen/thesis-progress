# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 6.0, largest 17.0, ratio 2.83.

| vertex | d_trip |
|---|---|
| 6 | 14.0 |
| 12 | 10.0 |
| 20 | 17.0 |
| 36 | 14.0 |
| 43 | 6.0 |
| 65 | 12.0 |
| 217 | 10.0 |
| 223 | 16.0 |

## demand.skew = 0.5

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.15 | 20 | 20 / 20 | 0.256 | 0.929 | 34.900 | 0.000 | 31.700 | 87339.850 | 77877.550 | 69.043 | 13.565 | 253.655 | 0.000 |
| fixed | 0.15 | 20 | 20 / 20 | 0.266 | 0.969 | 11.500 | 0.000 | 27.750 | 32527.850 | 30178.650 | 65.846 | 13.435 | 45.856 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.15 | n/a | 0.09 |
| fixed | 0.15 | n/a | 0.09 |

## demand.skew = 1

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.15 | 20 | 20 / 20 | 0.233 | 0.920 | 35.350 | 0.100 | 30.800 | 82330.850 | 71780.100 | 86.376 | 11.203 | 255.317 | 0.000 |
| fixed | 0.15 | 20 | 20 / 20 | 0.234 | 0.938 | 26.200 | 0.300 | 25.350 | 40561.750 | 36255.650 | 89.143 | 10.770 | 60.490 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.15 | n/a | 0.09 |
| fixed | 0.15 | n/a | 0.09 |

## demand.skew = 1.5

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.15 | 20 | 20 / 20 | 0.209 | 0.950 | 16.650 | 0.300 | 30.150 | 61479.750 | 56244.550 | 140.105 | 7.690 | 121.749 | 0.000 |
| fixed | 0.15 | 20 | 20 / 20 | 0.193 | 0.902 | 35.750 | 2.750 | 19.750 | 50050.500 | 43365.700 | 135.892 | 7.020 | 62.720 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.15 | n/a | 0.09 |
| fixed | 0.15 | n/a | 0.09 |

