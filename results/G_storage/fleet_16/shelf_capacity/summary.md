# Token Passing load sweep

## Trip distance of the storage vertices

Smallest 6.0, largest 17.0, ratio 2.83, over 8 storage vertices. The ratio bounds what storage can save on a trip.

## storage.vertex_capacity = 170

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest stand-still, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.12 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 43 | -0.35 | 0.00 | 0.00 |
| demand | 0.12 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 46 | -0.34 | 0.00 | 0.00 |
| fixed | 0.12 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 47 | 0.70 | 0.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | 0.12 | n/a | 0.072 |
| demand | 0.12 | n/a | 0.072 |
| fixed | 0.12 | n/a | 0.072 |

## storage.vertex_capacity = 200

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest stand-still, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.12 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 43 | -1.56 | 0.00 | 0.00 |
| demand | 0.12 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 43 | -0.28 | 0.00 | 0.00 |
| fixed | 0.12 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 47 | 0.70 | 0.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | 0.12 | n/a | 0.072 |
| demand | 0.12 | n/a | 0.072 |
| fixed | 0.12 | n/a | 0.072 |

## storage.vertex_capacity = 300

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest stand-still, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.12 | 20 | 19 / 20 | 20 / 20 | 19 / 20 | 43 | 0.14 | 0.00 | 0.00 |
| demand | 0.12 | 20 | 19 / 20 | 20 / 20 | 19 / 20 | 43 | 0.15 | 0.00 | 0.00 |
| fixed | 0.12 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 47 | 0.70 | 0.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | n/a | 0.12 | n/a |
| demand | n/a | 0.12 | n/a |
| fixed | 0.12 | n/a | 0.072 |

## storage.vertex_capacity = 400

### The check per rate

| rule | rate | seeds | keep up | picks keep up | put-aways keep up | longest stand-still, highest | backlog slope per 100 steps | overflow units | unplaced units |
|---|---|---|---|---|---|---|---|---|---|
| congestion | 0.12 | 20 | 18 / 20 | 20 / 20 | 18 / 20 | 43 | 0.40 | 0.00 | 0.00 |
| demand | 0.12 | 20 | 18 / 20 | 20 / 20 | 18 / 20 | 43 | 0.40 | 0.00 | 0.00 |
| fixed | 0.12 | 20 | 20 / 20 | 20 / 20 | 20 / 20 | 47 | 0.70 | 0.00 | 0.00 |

### Capacity

The highest rate that keeps up on every seed with f_up = 0.8, every lower rate
too, the first rate that fails, and the main load at 0.6 of the capacity.

| rule | capacity | first failing rate | main load |
|---|---|---|---|
| congestion | n/a | 0.12 | n/a |
| demand | n/a | 0.12 | n/a |
| fixed | 0.12 | n/a | 0.072 |

