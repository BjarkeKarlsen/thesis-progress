# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 7.5, largest 36.0, ratio 4.80, over 40 storage vertices. The ratio bounds what storage can save on a trip.

## demand.rotation_period = 100

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.105 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 57 | -0.03 | 0.00 | 0.00 |
| fixed | 0.105 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 87 | -0.05 | 81.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.105 | n/a | 0.063 |
| fixed | 0.105 | n/a | 0.063 |

## demand.rotation_period = 200

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.105 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 35 | -0.01 | 0.00 | 0.00 |
| fixed | 0.105 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 66 | -0.03 | 99.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.105 | n/a | 0.063 |
| fixed | 0.105 | n/a | 0.063 |

## demand.rotation_period = 400

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.105 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 51 | -0.02 | 0.00 | 0.00 |
| fixed | 0.105 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 58 | -0.07 | 126.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.105 | n/a | 0.063 |
| fixed | 0.105 | n/a | 0.063 |

