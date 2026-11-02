# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 13.1, largest 72.9, ratio 5.55, over 160 storage vertices. The ratio bounds what storage can save on a trip.

## storage_rule.epoch_length = 50

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.3 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 27 | -0.02 | 0.00 | 0.00 |
| demand | 0.3 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 40 | -0.03 | 0.00 | 0.00 |
| fixed | 0.3 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 35 | -0.19 | 1127.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | 0.3 | n/a | 0.18 |
| demand | 0.3 | n/a | 0.18 |
| fixed | 0.3 | n/a | 0.18 |

## storage_rule.epoch_length = 100

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.3 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 40 | -0.07 | 0.00 | 0.00 |
| demand | 0.3 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 53 | -0.04 | 0.00 | 0.00 |
| fixed | 0.3 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 30 | -0.24 | 705.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | 0.3 | n/a | 0.18 |
| demand | 0.3 | n/a | 0.18 |
| fixed | 0.3 | n/a | 0.18 |

## storage_rule.epoch_length = 200

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.3 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 47 | -0.16 | 0.00 | 0.00 |
| demand | 0.3 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 44 | -0.14 | 0.00 | 0.00 |
| fixed | 0.3 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 32 | -0.31 | 467.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | 0.3 | n/a | 0.18 |
| demand | 0.3 | n/a | 0.18 |
| fixed | 0.3 | n/a | 0.18 |

## storage_rule.epoch_length = 400

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.3 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 32 | -0.21 | 0.00 | 0.00 |
| demand | 0.3 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 33 | -0.18 | 0.00 | 0.00 |
| fixed | 0.3 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 34 | -0.33 | 329.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | 0.3 | n/a | 0.18 |
| demand | 0.3 | n/a | 0.18 |
| fixed | 0.3 | n/a | 0.18 |

