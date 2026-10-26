# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 4.0, largest 56.0, ratio 14.00, over 32 storage vertices. The ratio bounds what storage can save on a trip.

## storage_rule.epoch_length = 50

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest stand-still, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.3 | 20 | 0 / 20 | 20 / 20 | 0 / 20 | 96 | 9.91 | 0.00 | 0.00 |
| demand | 0.3 | 20 | 0 / 20 | 20 / 20 | 0 / 20 | 96 | 9.97 | 0.00 | 0.00 |
| fixed | 0.3 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 97 | 1.02 | 0.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | n/a | 0.3 | n/a |
| demand | n/a | 0.3 | n/a |
| fixed | 0.3 | n/a | 0.18 |

## storage_rule.epoch_length = 100

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest stand-still, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.3 | 20 | 0 / 20 | 20 / 20 | 0 / 20 | 87 | 5.39 | 0.00 | 0.00 |
| demand | 0.3 | 20 | 0 / 20 | 20 / 20 | 0 / 20 | 93 | 5.88 | 0.00 | 0.00 |
| fixed | 0.3 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 97 | 0.90 | 0.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | n/a | 0.3 | n/a |
| demand | n/a | 0.3 | n/a |
| fixed | 0.3 | n/a | 0.18 |

## storage_rule.epoch_length = 200

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest stand-still, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.3 | 20 | 13 / 20 | 20 / 20 | 13 / 20 | 81 | 0.44 | 0.00 | 0.00 |
| demand | 0.3 | 20 | 9 / 20 | 20 / 20 | 9 / 20 | 81 | 0.96 | 0.00 | 0.00 |
| fixed | 0.3 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 73 | 0.43 | 0.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | n/a | 0.3 | n/a |
| demand | n/a | 0.3 | n/a |
| fixed | 0.3 | n/a | 0.18 |

## storage_rule.epoch_length = 400

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest stand-still, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.3 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 86 | -0.57 | 0.00 | 0.00 |
| demand | 0.3 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 82 | -0.41 | 0.00 | 0.00 |
| fixed | 0.3 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 84 | 0.74 | 0.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | 0.3 | n/a | 0.18 |
| demand | 0.3 | n/a | 0.18 |
| fixed | 0.3 | n/a | 0.18 |

