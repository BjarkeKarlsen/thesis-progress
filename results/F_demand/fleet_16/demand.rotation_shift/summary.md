# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 6.0, largest 17.0, ratio 2.83, over 8 storage vertices. The ratio bounds what storage can save on a trip.

## demand.rotation_shift = 2

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest stand-still, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.12 | 20 | 19 / 20 | 20 / 20 | 19 / 20 | 39 | -2.84 | 0.00 | 0.00 |
| fixed | 0.12 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 47 | 1.37 | 0.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | n/a | 0.12 | n/a |
| fixed | 0.12 | n/a | 0.072 |

## demand.rotation_shift = 5

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest stand-still, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.12 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 43 | -0.28 | 0.00 | 0.00 |
| fixed | 0.12 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 47 | 0.70 | 0.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.12 | n/a | 0.072 |
| fixed | 0.12 | n/a | 0.072 |

## demand.rotation_shift = 10

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest stand-still, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.12 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 42 | 0.33 | 0.00 | 0.00 |
| fixed | 0.12 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 47 | -0.25 | 0.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.12 | n/a | 0.072 |
| fixed | 0.12 | n/a | 0.072 |

