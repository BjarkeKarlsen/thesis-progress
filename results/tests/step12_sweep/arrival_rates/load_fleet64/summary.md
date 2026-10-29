# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 20.9, largest 81.8, ratio 3.91, over 200 storage vertices. The ratio bounds what storage can save on a trip.

## The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| fixed | 0.2 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 22 | -0.06 | 175.50 | 0.00 |
| fixed | 0.4 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 12 | 1.14 | 675.00 | 0.00 |
| fixed | 0.6 | 20 | 8 / 20 | 0 / 20 | 20 / 20 | 12 | 12.04 | 3187.50 | 0.00 |
| fixed | 0.8 | 20 | 0 / 20 | 0 / 20 | 20 / 20 | 11 | 30.36 | 9031.50 | 0.00 |

## Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| fixed | 0.4 | 0.6 | 0.24 |

