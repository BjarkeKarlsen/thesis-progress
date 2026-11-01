# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 21.0, largest 49.0, ratio 2.33, over 80 storage vertices. The ratio bounds what storage can save on a trip.

## demand.rotation_period = 100

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.18 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 132 | 0.03 | 0.00 | 0.00 |
| fixed | 0.18 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 98 | -0.04 | 329.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.18 | n/a | 0.108 |
| fixed | 0.18 | n/a | 0.108 |

## demand.rotation_period = 200

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.18 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 114 | 0.01 | 0.00 | 0.00 |
| fixed | 0.18 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 99 | -0.05 | 337.50 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.18 | n/a | 0.108 |
| fixed | 0.18 | n/a | 0.108 |

## demand.rotation_period = 400

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.18 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 104 | 0.06 | 0.00 | 0.00 |
| fixed | 0.18 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 101 | -0.17 | 341.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.18 | n/a | 0.108 |
| fixed | 0.18 | n/a | 0.108 |

