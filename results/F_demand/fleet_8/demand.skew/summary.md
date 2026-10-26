# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 11.0, largest 15.0, ratio 1.36, over 4 storage vertices. The ratio bounds what storage can save on a trip.

## demand.skew = 0.5

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest stand-still, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.12 | 20 | 19 / 20 | 20 / 20 | 19 / 20 | 10 | 2.02 | 0.00 | 0.00 |
| fixed | 0.12 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 16 | 0.18 | 0.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | n/a | 0.12 | n/a |
| fixed | 0.12 | n/a | 0.072 |

## demand.skew = 1

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest stand-still, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.12 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 20 | 1.54 | 0.00 | 0.00 |
| fixed | 0.12 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 15 | 0.59 | 0.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.12 | n/a | 0.072 |
| fixed | 0.12 | n/a | 0.072 |

## demand.skew = 1.5

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest stand-still, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.12 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 11 | -0.17 | 0.00 | 0.00 |
| fixed | 0.12 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 13 | 0.77 | 0.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.12 | n/a | 0.072 |
| fixed | 0.12 | n/a | 0.072 |

