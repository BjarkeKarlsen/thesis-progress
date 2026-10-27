# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 11.5, largest 45.0, ratio 3.91, over 60 storage vertices. The ratio bounds what storage can save on a trip.

## The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.24 | 1 | 1 / 1 | 1 / 1 | 1 / 1 | 27 | 3.06 | 0.00 | 0.00 |

## Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.24 | n/a | 0.144 |

