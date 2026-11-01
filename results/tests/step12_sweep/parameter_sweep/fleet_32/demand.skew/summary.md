# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 13.1, largest 72.9, ratio 5.55, over 160 storage vertices. The ratio bounds what storage can save on a trip.

## demand.skew = 0.5

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.3 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 28 | -0.19 | 0.00 | 0.00 |
| fixed | 0.3 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 35 | -0.24 | 615.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.3 | n/a | 0.18 |
| fixed | 0.3 | n/a | 0.18 |

## demand.skew = 1

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.3 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 53 | -0.04 | 0.00 | 0.00 |
| fixed | 0.3 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 30 | -0.24 | 705.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.3 | n/a | 0.18 |
| fixed | 0.3 | n/a | 0.18 |

## demand.skew = 1.5

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.3 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 36 | -0.09 | 0.00 | 0.00 |
| fixed | 0.3 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 46 | -0.21 | 807.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.3 | n/a | 0.18 |
| fixed | 0.3 | n/a | 0.18 |

