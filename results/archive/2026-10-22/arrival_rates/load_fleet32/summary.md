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

## Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fixed | 0.5 | 50 | 50 / 50 | 0.676 | 0.909 | 30.840 | 218139.040 | 185446.280 | 153.266 | 25.387 | 106.121 | 0.000 |
| fixed | 0.6 | 50 | 50 / 50 | 0.761 | 0.873 | 32.000 | 329036.420 | 265821.080 | 204.032 | 28.434 | 117.185 | 0.000 |
| fixed | 0.7 | 50 | 46 / 50 | 0.818 | 0.822 | 31.600 | 478251.800 | 348731.800 | 258.090 | 31.030 | 128.684 | 0.000 |
| fixed | 0.8 | 50 | 1 / 50 | 0.857 | 0.762 | 30.340 | 659596.440 | 419111.240 | 303.754 | 33.997 | 139.079 | 0.000 |
| fixed | 0.9 | 50 | 0 / 50 | 0.882 | 0.705 | 29.980 | 848349.140 | 477733.460 | 342.629 | 36.850 | 147.427 | 0.000 |

## Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| fixed | 0.6 | 0.7 | 0.36 |
