# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 5.0, largest 35.0, ratio 7.00, over 16 storage vertices. The ratio bounds what storage can save on a trip.

## demand.skew = 0.5

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest stand-still, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.36 | 20 | 0 / 20 | 20 / 20 | 0 / 20 | 38 | 12.38 | 0.00 | 0.00 |
| fixed | 0.36 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 39 | -0.24 | 0.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | n/a | 0.36 | n/a |
| fixed | 0.36 | n/a | 0.216 |

## demand.skew = 1

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest stand-still, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.36 | 20 | 0 / 20 | 20 / 20 | 0 / 20 | 31 | 10.03 | 0.00 | 0.00 |
| fixed | 0.36 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 36 | 0.66 | 0.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | n/a | 0.36 | n/a |
| fixed | 0.36 | n/a | 0.216 |

## demand.skew = 1.5

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest stand-still, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.36 | 20 | 15 / 20 | 20 / 20 | 15 / 20 | 32 | 4.58 | 0.00 | 0.00 |
| fixed | 0.36 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 48 | 0.38 | 59.80 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | n/a | 0.36 | n/a |
| fixed | 0.36 | n/a | 0.216 |

