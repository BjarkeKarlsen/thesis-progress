# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 18.1, largest 103.8, ratio 5.75, over 320 storage vertices. The ratio bounds what storage can save on a trip.

## The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.6 | 5 | 0 / 5 | 0 / 5 | 4 / 5 | 93 | 3.94 | 0.00 | 0.00 |

## Capacity

The highest rate that keeps up on every seed with f_up = 0.9, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | n/a | 0.6 | n/a |

