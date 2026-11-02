# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 18.1, largest 103.8, ratio 5.75, over 320 storage vertices. The ratio bounds what storage can save on a trip.

## storage_rule.epoch_length = 50

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.6 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 10 | -0.62 | 0.00 | 0.00 |
| demand | 0.6 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 12 | -0.49 | 0.00 | 0.00 |
| fixed | 0.6 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 12 | -0.88 | 2703.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | 0.6 | n/a | 0.36 |
| demand | 0.6 | n/a | 0.36 |
| fixed | 0.6 | n/a | 0.36 |

## storage_rule.epoch_length = 100

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.6 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 11 | -0.70 | 0.00 | 0.00 |
| demand | 0.6 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 11 | -0.66 | 0.00 | 0.00 |
| fixed | 0.6 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 12 | -1.00 | 1740.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | 0.6 | n/a | 0.36 |
| demand | 0.6 | n/a | 0.36 |
| fixed | 0.6 | n/a | 0.36 |

## storage_rule.epoch_length = 200

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.6 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 10 | -0.91 | 0.00 | 0.00 |
| demand | 0.6 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 12 | -0.93 | 0.00 | 0.00 |
| fixed | 0.6 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 14 | -1.20 | 1021.50 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | 0.6 | n/a | 0.36 |
| demand | 0.6 | n/a | 0.36 |
| fixed | 0.6 | n/a | 0.36 |

## storage_rule.epoch_length = 400

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.6 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 13 | -1.53 | 0.00 | 0.00 |
| demand | 0.6 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 9 | -1.52 | 0.00 | 0.00 |
| fixed | 0.6 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 13 | -1.43 | 679.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | 0.6 | n/a | 0.36 |
| demand | 0.6 | n/a | 0.36 |
| fixed | 0.6 | n/a | 0.36 |

