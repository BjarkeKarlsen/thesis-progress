# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 18.1, largest 103.8, ratio 5.75, over 320 storage vertices. The ratio bounds what storage can save on a trip.

## demand.skew = 0.5

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.6 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 15 | -0.50 | 0.00 | 0.00 |
| fixed | 0.6 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 11 | -0.70 | 1463.50 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.6 | n/a | 0.36 |
| fixed | 0.6 | n/a | 0.36 |

## demand.skew = 1

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.6 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 11 | -0.66 | 0.00 | 0.00 |
| fixed | 0.6 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 12 | -1.00 | 1740.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.6 | n/a | 0.36 |
| fixed | 0.6 | n/a | 0.36 |

## demand.skew = 1.5

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.6 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 12 | -0.78 | 0.00 | 0.00 |
| fixed | 0.6 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 12 | -0.82 | 1855.50 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.6 | n/a | 0.36 |
| fixed | 0.6 | n/a | 0.36 |

