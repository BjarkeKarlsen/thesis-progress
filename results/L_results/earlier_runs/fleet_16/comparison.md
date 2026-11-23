# Fleet 16: adaptive storage against fixed storage

Gain = fixed minus adaptive mean pick service time, so positive is faster, paired seed by seed on the test seeds (eq:rqformal), chosen policies. Given only when every seed keeps up.

## Main setup ([A84]): one policy, trained under fixed storage, played under each rule

| controller | rule | seeds | all keep up | gain | 95 % CI | relative gain % [CI] | pick service fixed | pick service rule | throughput fixed | throughput rule |
|---|---|---|---|---|---|---|---|---|---|---|
| centralised | demand | 20 | False | n/a | n/a | n/a | n/a | n/a | 0.036 | 0.035 |
| decentralised | demand | 20 | False | n/a | n/a | n/a | n/a | n/a | 0.000 | 0.000 |
| decentralised_comm | demand | 20 | False | n/a | n/a | n/a | n/a | n/a | 0.004 | 0.003 |
| section | demand | 20 | False | n/a | n/a | n/a | n/a | n/a | 0.131 | 0.125 |

## Second setup: each rule with the policy trained under it

The run trained under fixed storage, played under fixed, against the run trained under the rule, played under it. Two different policies, so the gain mixes storage and training.

| controller | rule | seeds | all keep up | gain | 95 % CI | relative gain % [CI] | pick service fixed | pick service rule | throughput fixed | throughput rule |
|---|---|---|---|---|---|---|---|---|---|---|
| centralised | demand | 20 | False | n/a | n/a | n/a | n/a | n/a | 0.036 | 0.026 |
| centralised | congestion | 20 | False | n/a | n/a | n/a | n/a | n/a | 0.036 | 0.058 |
| decentralised | demand | 20 | False | n/a | n/a | n/a | n/a | n/a | 0.000 | 0.007 |
| decentralised | congestion | 20 | False | n/a | n/a | n/a | n/a | n/a | 0.000 | 0.104 |
| decentralised_comm | demand | 20 | False | n/a | n/a | n/a | n/a | n/a | 0.004 | 0.000 |
| decentralised_comm | congestion | 20 | False | n/a | n/a | n/a | n/a | n/a | 0.004 | 0.004 |
| section | demand | 20 | False | n/a | n/a | n/a | n/a | n/a | 0.131 | 0.055 |
| section | congestion | 20 | False | n/a | n/a | n/a | n/a | n/a | 0.131 | 0.121 |
