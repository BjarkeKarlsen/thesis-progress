# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 14.5, largest 39.0, ratio 2.69, over 40 storage vertices. The ratio bounds what storage can save on a trip.

## arrival.refill_units = 15

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.09 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 290 | -0.01 | 0.00 | 0.00 |
| fixed | 0.09 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 316 | -0.03 | 129.75 | 0.00 |
| random | 0.09 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 261 | -0.07 | 0.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.09 | n/a | 0.054 |
| fixed | 0.09 | n/a | 0.054 |
| random | 0.09 | n/a | 0.054 |

## arrival.refill_units = 30

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.09 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 335 | -0.02 | 0.00 | 0.00 |
| fixed | 0.09 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 310 | -0.03 | 111.00 | 0.00 |
| random | 0.09 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 281 | -0.07 | 0.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.09 | n/a | 0.054 |
| fixed | 0.09 | n/a | 0.054 |
| random | 0.09 | n/a | 0.054 |

## arrival.refill_units = 60

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.09 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 316 | -0.06 | 0.00 | 0.00 |
| fixed | 0.09 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 306 | -0.07 | 111.00 | 0.00 |
| random | 0.09 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 258 | -0.03 | 0.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.09 | n/a | 0.054 |
| fixed | 0.09 | n/a | 0.054 |
| random | 0.09 | n/a | 0.054 |

