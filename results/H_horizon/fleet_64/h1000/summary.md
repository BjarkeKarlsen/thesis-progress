# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 4.0, largest 56.0, ratio 14.00, over 32 storage vertices. The ratio bounds what storage can save on a trip.

## The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest stand-still, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.3 | 20 | 0 / 20 | 20 / 20 | 0 / 20 | 83 | 9.03 | 0.00 | 0.00 |
| fixed | 0.3 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 76 | 0.46 | 0.00 | 0.00 |

## Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | n/a | 0.3 | n/a |
| fixed | 0.3 | n/a | 0.18 |

