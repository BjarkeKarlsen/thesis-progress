# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 14.2, largest 35.0, ratio 2.46, over 60 storage vertices. The ratio bounds what storage can save on a trip.

## The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| fixed | 0.2 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 21 | 0.29 | 282.00 | 0.00 |
| fixed | 0.25 | 20 | 20 / 20 | 15 / 20 | 20 / 20 | 18 | 1.78 | 999.00 | 0.00 |
| fixed | 0.3 | 20 | 16 / 20 | 0 / 20 | 20 / 20 | 15 | 4.93 | 2773.50 | 0.00 |
| fixed | 0.35 | 20 | 3 / 20 | 0 / 20 | 20 / 20 | 15 | 9.29 | 4939.50 | 0.00 |
| fixed | 0.4 | 20 | 0 / 20 | 0 / 20 | 20 / 20 | 15 | 13.91 | 7542.00 | 24.00 |

## Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| fixed | 0.25 | 0.3 | 0.15 |

