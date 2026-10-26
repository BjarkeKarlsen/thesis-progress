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

## demand.rotation_shift = 2

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.15 | 20 | 20 / 20 | 0.225 | 0.893 | 46.600 | 2.250 | 33.800 | 117435.000 | 100810.450 | 136.817 | 11.053 | 362.985 | 0.000 |
| fixed | 0.15 | 20 | 20 / 20 | 0.230 | 0.921 | 35.200 | 0.450 | 27.200 | 41581.750 | 34782.700 | 85.830 | 10.777 | 61.084 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.15 | n/a | 0.09 |
| fixed | 0.15 | n/a | 0.09 |

## demand.rotation_shift = 5

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

## demand.rotation_shift = 10

### Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| demand | 0.15 | 20 | 20 / 20 | 0.244 | 0.961 | 14.800 | 0.000 | 28.750 | 56954.000 | 53309.700 | 76.023 | 11.305 | 151.433 | 0.000 |
| fixed | 0.15 | 20 | 20 / 20 | 0.241 | 0.964 | 12.650 | 0.000 | 31.450 | 38929.700 | 36138.100 | 87.221 | 10.785 | 57.738 | 0.000 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.15 | n/a | 0.09 |
| fixed | 0.15 | n/a | 0.09 |

