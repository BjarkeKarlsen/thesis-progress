# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 18.1, largest 103.8, ratio 5.75, over 320 storage vertices. The ratio bounds what storage can save on a trip.

## The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| fixed | 0.8 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 10 | -0.94 | 3158.50 | 0.00 |
| fixed | 1 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 8 | 2.33 | 6145.50 | 0.00 |
| fixed | 1.2 | 20 | 14 / 20 | 14 / 20 | 20 / 20 | 7 | 11.43 | 11305.50 | 0.00 |
| fixed | 1.4 | 20 | 0 / 20 | 0 / 20 | 18 / 20 | 6 | 34.98 | 19326.50 | 137.00 |
| fixed | 1.6 | 20 | 0 / 20 | 0 / 20 | 9 / 20 | 7 | 63.01 | 26004.50 | 1715.00 |

## Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| fixed | 1 | 1.2 | 0.6 |

