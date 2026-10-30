# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 12.8, largest 61.9, ratio 4.85, over 100 storage vertices. The ratio bounds what storage can save on a trip.

## The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| fixed | 0.1 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 81 | -0.01 | 84.00 | 0.00 |
| fixed | 0.2 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 24 | 0.07 | 216.00 | 0.00 |
| fixed | 0.3 | 20 | 20 / 20 | 19 / 20 | 20 / 20 | 16 | 1.48 | 784.50 | 0.00 |
| fixed | 0.4 | 20 | 12 / 20 | 0 / 20 | 20 / 20 | 15 | 7.84 | 2992.50 | 0.00 |
| fixed | 0.8 | 20 | 0 / 20 | 0 / 20 | 20 / 20 | 12 | 46.44 | 16569.00 | 1842.00 |

## Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| fixed | 0.3 | 0.4 | 0.18 |

