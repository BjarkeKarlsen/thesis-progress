# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 14.5, largest 39.0, ratio 2.69, over 40 storage vertices. The ratio bounds what storage can save on a trip.

## storage_rule.epoch_length = 50

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.09 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 314 | -0.02 | 0.00 | 0.00 |
| demand | 0.09 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 302 | -0.01 | 0.00 | 0.00 |
| fixed | 0.09 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 324 | -0.03 | 221.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | 0.09 | n/a | 0.054 |
| demand | 0.09 | n/a | 0.054 |
| fixed | 0.09 | n/a | 0.054 |

## storage_rule.epoch_length = 100

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.09 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 310 | -0.01 | 0.00 | 0.00 |
| demand | 0.09 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 301 | -0.01 | 0.00 | 0.00 |
| fixed | 0.09 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 316 | -0.03 | 146.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | 0.09 | n/a | 0.054 |
| demand | 0.09 | n/a | 0.054 |
| fixed | 0.09 | n/a | 0.054 |

## storage_rule.epoch_length = 200

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.09 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 261 | -0.03 | 0.00 | 0.00 |
| demand | 0.09 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 248 | -0.02 | 0.00 | 0.00 |
| fixed | 0.09 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 243 | -0.04 | 91.50 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | 0.09 | n/a | 0.054 |
| demand | 0.09 | n/a | 0.054 |
| fixed | 0.09 | n/a | 0.054 |

## storage_rule.epoch_length = 400

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.09 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 314 | -0.02 | 0.00 | 0.00 |
| demand | 0.09 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 301 | -0.02 | 0.00 | 0.00 |
| fixed | 0.09 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 307 | -0.05 | 63.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | 0.09 | n/a | 0.054 |
| demand | 0.09 | n/a | 0.054 |
| fixed | 0.09 | n/a | 0.054 |

