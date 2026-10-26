# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 4.0, largest 56.0, ratio 14.00, over 32 storage vertices. The ratio bounds what storage can save on a trip.

## The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest stand-still, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| fixed | 0.42 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 87 | 2.18 | 0.00 | 0.00 |
| fixed | 0.5 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 91 | 3.85 | 0.00 | 0.00 |
| fixed | 0.6 | 20 | 15 / 20 | 15 / 20 | 20 / 20 | 91 | 7.41 | 0.45 | 0.00 |
| fixed | 0.7 | 20 | 0 / 20 | 0 / 20 | 20 / 20 | 109 | 12.15 | 5.90 | 0.00 |
| fixed | 0.8 | 20 | 0 / 20 | 0 / 20 | 20 / 20 | 94 | 16.32 | 38.55 | 0.00 |

## Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| fixed | 0.5 | 0.6 | 0.3 |

