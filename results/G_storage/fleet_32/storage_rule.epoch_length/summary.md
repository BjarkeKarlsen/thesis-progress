# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 12.8, largest 61.9, ratio 4.85, over 100 storage vertices. The ratio bounds what storage can save on a trip.

## storage_rule.epoch_length = 50

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.18 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 21 | -0.01 | 0.00 | 0.00 |
| demand | 0.18 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 28 | 0.00 | 0.00 | 0.00 |
| fixed | 0.18 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 22 | 0.04 | 381.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | 0.18 | n/a | 0.108 |
| demand | 0.18 | n/a | 0.108 |
| fixed | 0.18 | n/a | 0.108 |

## storage_rule.epoch_length = 100

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.18 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 26 | 0.04 | 0.00 | 0.00 |
| demand | 0.18 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 25 | 0.03 | 0.00 | 0.00 |
| fixed | 0.18 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 21 | 0.06 | 171.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | 0.18 | n/a | 0.108 |
| demand | 0.18 | n/a | 0.108 |
| fixed | 0.18 | n/a | 0.108 |

## storage_rule.epoch_length = 200

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.18 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 24 | 0.03 | 0.00 | 0.00 |
| demand | 0.18 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 26 | 0.04 | 0.00 | 0.00 |
| fixed | 0.18 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 23 | 0.07 | 93.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | 0.18 | n/a | 0.108 |
| demand | 0.18 | n/a | 0.108 |
| fixed | 0.18 | n/a | 0.108 |

## storage_rule.epoch_length = 400

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.18 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 25 | 0.06 | 0.00 | 0.00 |
| demand | 0.18 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 22 | 0.09 | 0.00 | 0.00 |
| fixed | 0.18 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 24 | 0.09 | 36.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | 0.18 | n/a | 0.108 |
| demand | 0.18 | n/a | 0.108 |
| fixed | 0.18 | n/a | 0.108 |

