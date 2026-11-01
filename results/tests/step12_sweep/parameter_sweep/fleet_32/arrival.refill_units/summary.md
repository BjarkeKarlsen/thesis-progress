# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 13.1, largest 72.9, ratio 5.55, over 160 storage vertices. The ratio bounds what storage can save on a trip.

## arrival.refill_units = 15

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.3 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 49 | -0.12 | 0.00 | 0.00 |
| fixed | 0.3 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 26 | -0.30 | 669.75 | 0.00 |
| random | 0.3 | 20 | 11 / 20 | 11 / 20 | 20 / 20 | 26 | 3.37 | 0.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.3 | n/a | 0.18 |
| fixed | 0.3 | n/a | 0.18 |
| random | n/a | 0.3 | n/a |

## arrival.refill_units = 30

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.3 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 62 | -0.38 | 0.00 | 0.00 |
| fixed | 0.3 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 32 | -0.61 | 622.50 | 0.00 |
| random | 0.3 | 20 | 18 / 20 | 18 / 20 | 20 / 20 | 28 | 2.31 | 0.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.3 | n/a | 0.18 |
| fixed | 0.3 | n/a | 0.18 |
| random | n/a | 0.3 | n/a |

## arrival.refill_units = 60

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.3 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 34 | -3.59 | 0.00 | 0.00 |
| fixed | 0.3 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 20 | -3.28 | 594.00 | 0.00 |
| random | 0.3 | 20 | 18 / 20 | 18 / 20 | 20 / 20 | 27 | 1.40 | 0.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.3 | n/a | 0.18 |
| fixed | 0.3 | n/a | 0.18 |
| random | n/a | 0.3 | n/a |

