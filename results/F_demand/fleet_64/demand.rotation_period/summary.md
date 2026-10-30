# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 20.9, largest 81.8, ratio 3.91, over 200 storage vertices. The ratio bounds what storage can save on a trip.

## demand.rotation_period = 100

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.24 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 22 | -0.07 | 0.00 | 0.00 |
| fixed | 0.24 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 22 | -0.06 | 180.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.24 | n/a | 0.144 |
| fixed | 0.24 | n/a | 0.144 |

## demand.rotation_period = 200

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.24 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 21 | -0.08 | 0.00 | 0.00 |
| fixed | 0.24 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 21 | -0.07 | 238.50 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.24 | n/a | 0.144 |
| fixed | 0.24 | n/a | 0.144 |

## demand.rotation_period = 400

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.24 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 21 | -0.09 | 0.00 | 0.00 |
| fixed | 0.24 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 20 | -0.15 | 351.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.24 | n/a | 0.144 |
| fixed | 0.24 | n/a | 0.144 |

