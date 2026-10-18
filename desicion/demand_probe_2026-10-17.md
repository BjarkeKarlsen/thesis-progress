# Demand probe, 2026-10-17

What the demand probe measured, for the arguments behind the demand model, the starting stock
and the storage rules. Script and raw rows: `~/thesis_runs/demand_probe/` (`demand_probe.py`,
runs `quick/`, `quick2/`, `learned/`, `v2/`). Implementation plan that follows from it:
`adaptive_storage_impl_plan.md` at the workspace root.

## Setup

- The 8-agent warehouse of the night of 2026-10-16 (94 vertices, 10 storage vertices,
  4 delivery vertices), horizon 2000.
- Planners: Token Passing, and the night's two decentralised policies
  (`decentralised_seed0/checkpoint_000002`, `decentralised_seed1000/checkpoint_000003`), played
  without retraining. Those policies were trained on 20 SKUs, uniform demand and fixed storage,
  so their numbers are a first indication only.
- Demand: Zipf popularity, weight of rank r is `1/(r+1)^s`, the ranking rotates by 5 places
  every P steps. The order draw uses the same random numbers as the repo, so the orders of a
  seed are identical under every storage rule (checked).
- Starting stock from popularity at t = 0. "cyclic" spreads the top SKUs over all storage
  vertices nearest first, "blocks" puts the top SKUs together at the nearest vertices.
- Wait rule "standing": a robot serving a task that stands still is charged to the next edge on
  its shortest route. Without it Token Passing never feeds the wait estimate (it is never
  overridden) and the congestion rule equals the demand rule.
- Evaluation seeds 200 000 to 200 003 (4 seeds), or 6 in the first runs. Mean ± standard
  deviation over seeds. Gains paired by seed.

## Measured

**Rotation is what gives adaptive storage something to do** (`quick/`, Token Passing, load 0.6,
skew 1, Δ 100, ν 16). Fixed storage loses about 15% throughput when the ranking rotates every
200 steps (0.428 to 0.362 with 20 SKUs in blocks, 0.443 to 0.374 with 100 SKUs in blocks). The
demand rule wins most of it back (gain +0.078 ± 0.012 with 20 SKUs, +0.034 ± 0.010 with 100).
Without rotation the gain is +0.002 to +0.045, depending on how far the starting stock is from
what the demand rule builds.

**Starting stock** (`quick/`, fixed storage, no rotation). Blocks beat cyclic, 0.428 against
0.405 with 20 SKUs and 0.443 against 0.391 with 100.

**Relocation cap** (`quick2/`, 100 SKUs, blocks, rotation every 200). With ν = 16 every update
hits the cap. ν = 48 gives a larger gain, +0.057 ± 0.012 against +0.034 ± 0.010 at load 0.6.

**Service time at load 0.3** (`quick2/`, `v2/`, rotation every 200, ν 48). Every planner keeps
up there by the 80% threshold (0.26 to 0.29 of 0.30).

| planner | fixed | demand rule | change |
|---|---|---|---|
| Token Passing | 54.1 | 39.4 | −27% |
| decentralised seed 0 | 32.1 | 13.3 | −59% |
| decentralised seed 1000 | 25.1 | 14.0 | −44% |

For the decentralised policies both travel (14.3 to 10.9) and blocked time (3.07 to 1.94) drop.
The throughput gain at load 0.6 is +0.057 (Token Passing), +0.101 ± 0.029 and +0.051 ± 0.030
(decentralised).

**Congestion rules** (`v2/`, clean rerun, 100 SKUs, blocks, rotation every 200, Δ 100, ν 48).
Three scores against the demand rule:
- today's score (`eq:storagegreedy`), `ρ̂(k) d(v) + β Σ μ̂ ŵ`;
- `congestion_rho`, `ρ̂(k) (d(v) + β Σ μ̂ ŵ)` (`thesis_decisions.md` #19 option b);
- `congestion_v2`, mean distance to the delivery points plus β times the predicted waits per
  crossing on the trips, raised by the load of SKUs already placed in the update (#19 option c
  with ideas 1 and 3).

Measured:
- `congestion_rho` equals the demand rule in every cell at β 1, 3 and 10. Weighted by demand,
  the congestion term never changes a ranking at these β.
- Today's score at β = 1 lowers blocked time for the decentralised policies at both loads (1.94
  to 1.75 and 1.72 to 1.54 at load 0.3, 3.11 to 2.74 and 3.89 to 3.53 at load 0.6) without
  added travel, and service time at load 0.3 drops a little (13.3 to 13.0, 14.0 to 12.4).
  Throughput is level with the demand rule within the spread. For Token Passing it is level or
  slightly worse. At β 3 and 10 travel rises and the result gets worse.
- `congestion_v2` at β = 1 is close to today's score at load 0.3, but at load 0.6 and at higher
  β it is worse than the demand rule (decentralised seed 0: −0.014 ± 0.015 at β 1, −0.030 ±
  0.009 at β 3), and blocked time goes up, not down.

## Inferred, not measured

- Uniform or fixed-skew demand would leave RQ1 nearly empty. Drifting demand gives it an answer.
- The coupling effect differs by controller (RQ2), larger for the learned decentralised arm than
  for Token Passing, already before retraining.
- For RQ3, today's congestion score with a small β is the only variant that helped, and only for
  the arm that blocks. Neither #19 option b nor my option c variant improved on it. That argues
  for keeping the score's form and rewording K in the Introduction (#19 option a), with β around
  1, unless the retrained arms show otherwise.

## Probe bug, and which numbers it affected

The probe patched repo functions at run time, and worker processes were reused between
episodes. Until the fix (`reset_patches`, 2026-10-17), a patch leaked into later episodes of
the same worker: a "congestion" episode could run another rule, and the wait rule stacked, so
waits were charged several times (in effect a larger β). Congestion-rule numbers from `quick/`,
`quick2/` and `learned/` are therefore unreliable. Their rows are kept, the contaminated `v2/`
rows are in `v2/rows_contaminated.jsonl`. Fixed and demand numbers were not affected, because
those rules read only the demand estimate, and the order draw was replaced fresh every episode.
After the fix, a congestion episode gives identical results alone and after other rules.
