# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 12.8, largest 61.9, ratio 4.85, over 100 storage vertices. The ratio bounds what storage can save on a trip.

## arrival.refill_units = 15

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.18 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 25 | -0.01 | 0.00 | 0.00 |
| fixed | 0.18 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 22 | 0.04 | 144.00 | 0.00 |
| random | 0.18 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 21 | 0.04 | 0.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.18 | n/a | 0.108 |
| fixed | 0.18 | n/a | 0.108 |
| random | 0.18 | n/a | 0.108 |

## arrival.refill_units = 30

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.18 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 25 | 0.03 | 0.00 | 0.00 |
| fixed | 0.18 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 21 | 0.06 | 171.00 | 0.00 |
| random | 0.18 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 25 | 0.06 | 0.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.18 | n/a | 0.108 |
| fixed | 0.18 | n/a | 0.108 |
| random | 0.18 | n/a | 0.108 |

## arrival.refill_units = 60

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.18 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 23 | -0.03 | 0.00 | 0.00 |
| fixed | 0.18 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 26 | -0.01 | 222.00 | 0.00 |
| random | 0.18 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 25 | 0.04 | 0.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.18 | n/a | 0.108 |
| fixed | 0.18 | n/a | 0.108 |
| random | 0.18 | n/a | 0.108 |

