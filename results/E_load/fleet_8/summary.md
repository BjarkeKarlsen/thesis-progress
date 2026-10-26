# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 11.0, largest 15.0, ratio 1.36, over 4 storage vertices. The ratio bounds what storage can save on a trip.

## The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest stand-still, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| fixed | 0.1 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 15 | 0.08 | 0.00 | 0.00 |
| fixed | 0.2 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 16 | 4.86 | 14.50 | 0.00 |
| fixed | 0.225 | 20 | 14 / 20 | 14 / 20 | 20 / 20 | 15 | 5.09 | 45.60 | 0.00 |
| fixed | 0.25 | 20 | 5 / 20 | 5 / 20 | 20 / 20 | 15 | 4.73 | 92.55 | 0.00 |
| fixed | 0.275 | 20 | 0 / 20 | 0 / 20 | 20 / 20 | 14 | 6.02 | 155.10 | 0.40 |
| fixed | 0.3 | 20 | 0 / 20 | 0 / 20 | 20 / 20 | 16 | 8.44 | 203.65 | 16.40 |

## Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| fixed | 0.2 | 0.225 | 0.12 |

