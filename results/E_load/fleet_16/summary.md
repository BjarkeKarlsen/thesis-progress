# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 21.0, largest 49.0, ratio 2.33, over 80 storage vertices. The ratio bounds what storage can save on a trip.

## The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| fixed | 0.2 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 51 | -0.10 | 421.50 | 0.00 |
| fixed | 0.25 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 29 | -0.33 | 676.50 | 0.00 |
| fixed | 0.3 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 16 | 0.20 | 1232.50 | 0.00 |
| fixed | 0.35 | 20 | 16 / 20 | 16 / 20 | 20 / 20 | 17 | 2.34 | 2284.00 | 0.00 |
| fixed | 0.4 | 20 | 8 / 20 | 8 / 20 | 20 / 20 | 13 | 6.60 | 4041.00 | 5.50 |
| fixed | 0.6 | 20 | 0 / 20 | 0 / 20 | 20 / 20 | 15 | 29.00 | 9264.00 | 2730.50 |

## Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| fixed | 0.3 | 0.35 | 0.18 |

