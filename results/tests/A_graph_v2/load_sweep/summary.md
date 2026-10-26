# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 6.0, largest 37.0, ratio 6.17, over 58 storage vertices. The ratio bounds what storage can save on a trip.

## The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest stand-still, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| fixed | 0.1 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 18 | 0.03 | 0.00 | 0.00 |
| fixed | 0.2 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 15 | 2.75 | 0.00 | 0.00 |
| fixed | 0.225 | 20 | 14 / 20 | 14 / 20 | 20 / 20 | 18 | 4.30 | 0.00 | 0.00 |
| fixed | 0.25 | 20 | 3 / 20 | 3 / 20 | 20 / 20 | 16 | 5.95 | 0.00 | 0.00 |
| fixed | 0.275 | 20 | 0 / 20 | 0 / 20 | 20 / 20 | 16 | 8.47 | 0.00 | 0.00 |
| fixed | 0.3 | 20 | 0 / 20 | 0 / 20 | 20 / 20 | 22 | 11.66 | 0.00 | 0.00 |

## Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| fixed | 0.2 | 0.225 | 0.12 |

