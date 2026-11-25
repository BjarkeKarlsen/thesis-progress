# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 21.0, largest 49.0, ratio 2.33, over 80 storage vertices. The ratio bounds what storage can save on a trip.

## The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.18 | 5 | 5 / 5 | 5 / 5 | 5 / 5 | 129 | 0.35 | 0.00 | 0.00 |

## Capacity

The highest rate that keeps up on every seed with f_up = 0.9, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | 0.18 | n/a | 0.108 |

