# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 13.1, largest 72.9, ratio 5.55, over 160 storage vertices. The ratio bounds what storage can save on a trip.

## demand.rotation_share = 0.025

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.3 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 30 | -0.13 | 0.00 | 0.00 |
| fixed | 0.3 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 24 | -0.56 | 664.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.3 | n/a | 0.18 |
| fixed | 0.3 | n/a | 0.18 |

## demand.rotation_share = 0.05

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

## demand.rotation_share = 0.1

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest gap between finishes, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| demand | 0.3 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 31 | -0.03 | 0.00 | 0.00 |
| fixed | 0.3 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 25 | -0.14 | 667.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| demand | 0.3 | n/a | 0.18 |
| fixed | 0.3 | n/a | 0.18 |

