# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 13.1, largest 72.9, ratio 5.55, over 160 storage vertices. The ratio bounds what storage can save on a trip.

## The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| fixed | 0.4 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 17 | -0.18 | 1183.00 | 0.00 |
| fixed | 0.5 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 11 | 0.39 | 2205.50 | 0.00 |
| fixed | 0.6 | 20 | 17 / 20 | 17 / 20 | 20 / 20 | 11 | 3.93 | 4059.50 | 0.00 |
| fixed | 0.7 | 20 | 8 / 20 | 8 / 20 | 20 / 20 | 9 | 10.97 | 7396.50 | 0.00 |
| fixed | 0.8 | 20 | 0 / 20 | 0 / 20 | 20 / 20 | 10 | 21.21 | 11268.00 | 129.00 |

## Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| fixed | 0.5 | 0.6 | 0.3 |

