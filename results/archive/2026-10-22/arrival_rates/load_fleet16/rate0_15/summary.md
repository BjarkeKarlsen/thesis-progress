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

## Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fixed | 0.15 | 50 | 50 / 50 | 0.238 | 0.941 | 25.520 | 0.240 | 26.180 | 43332.700 | 39036.360 | 96.558 | 10.876 | 61.418 | 0.000 |

## Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| fixed | 0.15 | n/a | 0.09 |

