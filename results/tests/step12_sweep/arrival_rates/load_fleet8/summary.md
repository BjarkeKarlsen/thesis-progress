# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 14.5, largest 39.0, ratio 2.69, over 40 storage vertices. The ratio bounds what storage can save on a trip.

## The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| fixed | 0.1 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 219 | -0.08 | 190.00 | 0.00 |
| fixed | 0.125 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 187 | -0.08 | 252.00 | 0.00 |
| fixed | 0.15 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 128 | -0.06 | 390.00 | 0.00 |
| fixed | 0.175 | 20 | 19 / 20 | 19 / 20 | 20 / 20 | 62 | -0.11 | 676.50 | 0.00 |
| fixed | 0.2 | 20 | 18 / 20 | 18 / 20 | 20 / 20 | 24 | 0.90 | 1300.50 | 0.00 |
| fixed | 0.3 | 20 | 0 / 20 | 0 / 20 | 20 / 20 | 19 | 12.40 | 4574.00 | 985.50 |

## Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| fixed | 0.15 | 0.175 | 0.09 |

