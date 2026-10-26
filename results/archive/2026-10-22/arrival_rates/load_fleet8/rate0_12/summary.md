# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 11.0, largest 15.0, ratio 1.36.

| vertex | d_trip |
|---|---|
| 1 | 11.0 |
| 23 | 15.0 |
| 58 | 12.0 |
| 122 | 14.0 |

## Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | tasks waiting | orders waiting | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fixed | 0.12 | 50 | 50 / 50 | 0.203 | 0.977 | 7.520 | 0.080 | 9.120 | 23768.700 | 22830.620 | 46.705 | 9.212 | 69.269 | 0.000 |

## Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| fixed | 0.12 | n/a | 0.072 |

