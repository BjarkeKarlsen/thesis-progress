# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 18.1, largest 103.8, ratio 5.75, over 320 storage vertices. The ratio bounds what storage can save on a trip.

## arrival.refill_units = 15

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.6 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 11 | -0.90 | 0.00 | 0.00 |
| fixed | 0.6 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 13 | -1.26 | 1591.50 | 0.00 |
| random | 0.6 | 20 | 0 / 20 | 0 / 20 | 20 / 20 | 15 | 16.11 | 0.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.6 | n/a | 0.36 |
| fixed | 0.6 | n/a | 0.36 |
| random | n/a | 0.6 | n/a |

## arrival.refill_units = 30

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.6 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 12 | -3.51 | 0.00 | 0.00 |
| fixed | 0.6 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 14 | -3.66 | 1525.50 | 0.00 |
| random | 0.6 | 20 | 0 / 20 | 0 / 20 | 20 / 20 | 14 | 12.90 | 0.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.6 | n/a | 0.36 |
| fixed | 0.6 | n/a | 0.36 |
| random | n/a | 0.6 | n/a |

## arrival.refill_units = 60

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.6 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 14 | -10.13 | 0.00 | 0.00 |
| fixed | 0.6 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 15 | -8.33 | 1512.00 | 0.00 |
| random | 0.6 | 20 | 0 / 20 | 0 / 20 | 20 / 20 | 15 | 10.73 | 0.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.6 | n/a | 0.36 |
| fixed | 0.6 | n/a | 0.36 |
| random | n/a | 0.6 | n/a |

