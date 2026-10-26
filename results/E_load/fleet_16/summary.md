# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 6.0, largest 17.0, ratio 2.83, over 8 storage vertices. The ratio bounds what storage can save on a trip.

## The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest stand-still, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| fixed | 0.2 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 51 | 1.93 | 0.20 | 0.00 |
| fixed | 0.25 | 20 | 7 / 20 | 7 / 20 | 20 / 20 | 55 | 3.77 | 6.40 | 0.00 |
| fixed | 0.3 | 50 | 0 / 50 | n/a | n/a | 50 | n/a | 49.76 | 0.00 |
| fixed | 0.4 | 50 | 0 / 50 | n/a | n/a | 46 | n/a | 263.20 | 0.00 |
| fixed | 0.5 | 50 | 0 / 50 | n/a | n/a | 51 | n/a | 593.74 | 64.60 |
| fixed | 0.6 | 50 | 0 / 50 | n/a | n/a | 45 | n/a | 701.62 | 1078.78 |

## Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| fixed | 0.2 | 0.25 | 0.12 |

