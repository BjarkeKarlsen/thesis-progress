# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 6.0, largest 37.0, ratio 6.17, over 58 storage vertices. The ratio bounds what storage can save on a trip.

## The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest stand-still, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.12 | 20 | 18 / 20 | 20 / 20 | 18 / 20 | 10 | 1.46 | 0.00 | 0.00 |
| fixed | 0.12 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 18 | 0.06 | 0.00 | 0.00 |
| random | 0.12 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 21 | -0.06 | 0.00 | 0.00 |

## Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | n/a | 0.12 | n/a |
| fixed | 0.12 | n/a | 0.072 |
| random | 0.12 | n/a | 0.072 |

