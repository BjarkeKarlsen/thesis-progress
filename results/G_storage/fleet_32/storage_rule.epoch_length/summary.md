# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 5.0, largest 35.0, ratio 7.00, over 16 storage vertices. The ratio bounds what storage can save on a trip.

## storage_rule.epoch_length = 50

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest stand-still, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.36 | 20 | 1 / 20 | 20 / 20 | 1 / 20 | 33 | 8.21 | 0.00 | 0.00 |
| demand | 0.36 | 20 | 1 / 20 | 20 / 20 | 1 / 20 | 33 | 8.22 | 0.00 | 0.00 |
| fixed | 0.36 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 42 | 0.68 | 0.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | n/a | 0.36 | n/a |
| demand | n/a | 0.36 | n/a |
| fixed | 0.36 | n/a | 0.216 |

## storage_rule.epoch_length = 100

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest stand-still, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.36 | 20 | 0 / 20 | 20 / 20 | 0 / 20 | 31 | 9.94 | 0.00 | 0.00 |
| demand | 0.36 | 20 | 0 / 20 | 20 / 20 | 0 / 20 | 31 | 10.03 | 0.00 | 0.00 |
| fixed | 0.36 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 36 | 0.66 | 0.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | n/a | 0.36 | n/a |
| demand | n/a | 0.36 | n/a |
| fixed | 0.36 | n/a | 0.216 |

## storage_rule.epoch_length = 200

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest stand-still, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.36 | 20 | 1 / 20 | 20 / 20 | 1 / 20 | 43 | 6.73 | 0.00 | 0.00 |
| demand | 0.36 | 20 | 1 / 20 | 20 / 20 | 1 / 20 | 43 | 6.74 | 0.00 | 0.00 |
| fixed | 0.36 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 37 | 0.74 | 4.75 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | n/a | 0.36 | n/a |
| demand | n/a | 0.36 | n/a |
| fixed | 0.36 | n/a | 0.216 |

## storage_rule.epoch_length = 400

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest stand-still, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.36 | 20 | 12 / 20 | 20 / 20 | 12 / 20 | 40 | 3.78 | 0.00 | 0.00 |
| demand | 0.36 | 20 | 12 / 20 | 20 / 20 | 12 / 20 | 34 | 3.85 | 0.00 | 0.00 |
| fixed | 0.36 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 40 | -0.39 | 1.95 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | n/a | 0.36 | n/a |
| demand | n/a | 0.36 | n/a |
| fixed | 0.36 | n/a | 0.216 |

