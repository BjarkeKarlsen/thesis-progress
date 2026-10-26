# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 6.0, largest 17.0, ratio 2.83, over 8 storage vertices. The ratio bounds what storage can save on a trip.

## The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest stand-still, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| fixed | 0.12 | 3 | 3 / 3 | 3 / 3 | 3 / 3 | 44 | -0.89 | 0.00 | 0.00 |

## Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| fixed | 0.12 | n/a | 0.072 |

