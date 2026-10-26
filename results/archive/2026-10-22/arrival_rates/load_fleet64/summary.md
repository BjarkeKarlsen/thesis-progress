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

## Means over seeds

| rule | rate | seeds | keep up | throughput | completed share | longest stand-still | total service | total service finished | mean pick service | put-aways per arrival | put-away service | unplaced units |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fixed | 0.7 | 50 | 50 / 50 | 0.817 | 0.824 | 74.540 | 443816.480 | 298785.240 | 239.670 | 30.672 | 77.921 | 0.000 |
| fixed | 0.8 | 50 | 11 / 50 | 0.882 | 0.789 | 70.160 | 578877.940 | 357373.040 | 269.063 | 33.256 | 79.846 | 0.000 |
| fixed | 0.9 | 50 | 0 / 50 | 0.933 | 0.754 | 69.480 | 725100.200 | 412524.360 | 296.887 | 35.373 | 81.751 | 0.000 |

## Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| fixed | 0.7 | 0.8 | 0.42 |
