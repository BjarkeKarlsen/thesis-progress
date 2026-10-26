### Graph v2, 8 agents, load 0.12

| measure | fixed | demand | random |
|---|---|---|---|
| keeps up | 20 / 20 | 18 / 20 | 20 / 20 |
| picks keep up | 20 / 20 | 20 / 20 | 20 / 20 |
| put-aways keep up | 20 / 20 | 18 / 20 | 20 / 20 |
| pick service time | 44.30 | 37.91 | 36.28 |
| wait for a robot | 24.23 | 19.21 | 16.96 |
| travel | 18.37 | 17.53 | 18.01 |
| blocked | 1.70 | 1.17 | 1.31 |
| stock wait | 0.01 | 0.15 | 0.01 |
| shelf-taken wait (pick) | 5.67 | 10.46 | 1.51 |
| put-away service time | 41.31 | 148.08 | 39.78 |
| robot busy share | 0.62 | 0.38 | 0.60 |
| put-aways done | 174.25 | 151.25 | 174.20 |
| SKUs on more than one shelf | 0.00 | 39.97 | 46.61 |
| peak shelf fill | 0.11 | 0.82 | 0.12 |

Paired by seed, the second rule minus the first. Negative is shorter under the second.

| measure | demand - fixed | random - fixed | demand - random |
|---|---|---|---|
| pick service time | -6.40 [-7.82, -4.98], -14.4 % of 44.30 | -8.02 [-9.49, -6.56], -18.1 % of 44.30 | +1.63 [+0.17, +3.08], +4.5 % of 36.28 |
| wait for a robot | -5.02 [-6.33, -3.70], -20.7 % of 24.23 | -7.27 [-8.66, -5.88], -30.0 % of 24.23 | +2.25 [+0.88, +3.62], +13.3 % of 16.96 |
| travel | -0.84 [-1.08, -0.60], -4.6 % of 18.37 | -0.36 [-0.55, -0.18], -2.0 % of 18.37 | -0.48 [-0.70, -0.26], -2.7 % of 18.01 |
| blocked | -0.53 [-0.61, -0.46], -31.4 % of 1.70 | -0.39 [-0.47, -0.30], -22.8 % of 1.70 | -0.15 [-0.21, -0.08], -11.1 % of 1.31 |
| stock wait | +0.14 [-0.02, +0.30], +2830.0 % of 0.01 | +0.00 [-0.00, +0.01], +58.3 % of 0.01 | +0.14 [-0.02, +0.30], +1751.0 % of 0.01 |
| shelf-taken wait (pick) | +4.79 [+3.44, +6.14], +84.5 % of 5.67 | -4.16 [-4.84, -3.48], -73.3 % of 5.67 | +8.95 [+7.41, +10.49], +591.9 % of 1.51 |
| put-away service time | +106.77 [+88.26, +125.28], +258.5 % of 41.31 | -1.52 [-2.29, -0.76], -3.7 % of 41.31 | +108.29 [+89.53, +127.06], +272.2 % of 39.78 |
| robot busy share | -0.24 [-0.24, -0.23], -38.1 % of 0.62 | -0.02 [-0.02, -0.01], -2.6 % of 0.62 | -0.22 [-0.23, -0.21], -36.5 % of 0.60 |

