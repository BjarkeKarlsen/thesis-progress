# Dropped: the fixed-trained policy under another storage rule (Regime 1)

Dropped from the thesis on 2026-11-23 (author's decision, decision 1 of
`decisions/active/readability_review/method_review_queue.md`). Stored here
as data only. Nothing in the thesis points here.

## What it was

A controller trained under fixed storage, frozen, then played under
congestion-aware storage. The policy stays the same, so any change comes
from the storage rule alone. The main results instead give each storage
rule its own policy, trained under that rule (Regime 2).

## Why it was dropped

- The rows use the old 500 000-step policies. The results now use the long
  warm-start policies (from 2026-11-19), so these rows are out of date.
- The research questions only need a policy that trains under the rule it
  runs with.
- One training run per rule, so it cannot tell the rule apart from a better
  training run either.

## What it showed (16 agents, 20 test seeds, served counts [A96])

| Controller | fixed-trained, fixed | fixed-trained, congestion | congestion-trained, congestion |
|---|---|---|---|
| Centralised | 0.143 | 0.143 | 0.161 |
| Decentralised | 0.025 | 0.028 | 0.186 |

Tasks finished per step. The rule alone changed nothing the test could
measure (95 % interval holds zero, 9 and 10 of 20 seeds better). Section-based
and with-messages rows were never written into the thesis.

## Contents

- `fleet_8/<arm>/`, `fleet_16/<arm>/`: copies of
  `~/thesis_runs/evaluation/fleet_<m>/<arm>/fixed/evaluation_served_congestion_horizon10000_warmup5000/`
  (test seeds 200000+, 10000 steps, first 5000 left out). The 6-seed
  folders were not copied.
- `text/`: the thesis text as it stood before removal, Appendix L section
  `app:results:regime1` with `tab:app:regime1:16`, the Method paragraph on
  the two training setups, the Experiments training paragraph and the
  "rule alone" sentence, and the Appendix J main-result sentence.

Rationale: see the GAPS.md entry that replaces [A56] on this point.
