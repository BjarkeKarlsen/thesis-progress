# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 5.0, largest 35.0, ratio 7.00, over 16 storage vertices. The ratio bounds what storage can save on a trip.

## The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest stand-still, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| fixed | 0.4 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 37 | 0.44 | 0.00 | 0.00 |
| fixed | 0.5 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 37 | 0.52 | 19.05 | 0.00 |
| fixed | 0.6 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 46 | 4.58 | 73.05 | 0.00 |
| fixed | 0.7 | 20 | 0 / 20 | 0 / 20 | 20 / 20 | 42 | 10.31 | 144.95 | 0.00 |
| fixed | 0.8 | 20 | 0 / 20 | 0 / 20 | 20 / 20 | 45 | 19.42 | 324.70 | 0.00 |

## Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| fixed | 0.6 | 0.7 | 0.36 |

