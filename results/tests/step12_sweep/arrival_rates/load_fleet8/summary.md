# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 7.5, largest 36.0, ratio 4.80, over 40 storage vertices. The ratio bounds what storage can save on a trip.

## The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| fixed | 0.1 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 68 | -0.03 | 96.00 | 0.00 |
| fixed | 0.125 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 36 | 0.12 | 162.00 | 0.00 |
| fixed | 0.15 | 20 | 20 / 20 | 19 / 20 | 20 / 20 | 23 | 0.82 | 393.00 | 0.00 |
| fixed | 0.175 | 20 | 20 / 20 | 7 / 20 | 20 / 20 | 19 | 1.96 | 913.50 | 0.00 |
| fixed | 0.2 | 20 | 13 / 20 | 4 / 20 | 20 / 20 | 18 | 3.64 | 1821.00 | 0.00 |
| fixed | 0.3 | 20 | 0 / 20 | 0 / 20 | 20 / 20 | 18 | 12.36 | 6153.00 | 225.00 |

## Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| fixed | 0.175 | 0.2 | 0.105 |

