# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 14.5, largest 39.0, ratio 2.69, over 40 storage vertices. The ratio bounds what storage can save on a trip.

## demand.rotation_period = 100

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.09 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 299 | -0.01 | 0.00 | 0.00 |
| fixed | 0.09 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 297 | -0.03 | 152.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.09 | n/a | 0.054 |
| fixed | 0.09 | n/a | 0.054 |

## demand.rotation_period = 200

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.09 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 301 | -0.01 | 0.00 | 0.00 |
| fixed | 0.09 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 316 | -0.03 | 146.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.09 | n/a | 0.054 |
| fixed | 0.09 | n/a | 0.054 |

## demand.rotation_period = 400

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.09 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 302 | -0.03 | 0.00 | 0.00 |
| fixed | 0.09 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 312 | -0.08 | 154.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.09 | n/a | 0.054 |
| fixed | 0.09 | n/a | 0.054 |

