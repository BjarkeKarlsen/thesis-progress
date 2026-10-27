# Step 12 sweep, hand-off prompt

Paste the prompt below into a new agent session, started at the workspace root (`~/Documents/thesis`),
once the step 12 sweep has finished and pushed its results. Written 2026-10-27.

---

You are picking up the analysis of the step 12 sweep for a Master's thesis on closed-loop storage
assignment and multi-agent pickup and delivery. Read these first, in order:

1. `CLAUDE.md` and `AGENTS.md` at the workspace root (how the repos relate, writing and working rules).
2. `SESSION_CONTEXT.md` at the workspace root.
3. `thesis-progress/decisions/active/model_revision/README.md` (decisions D1 to D27, risks).
4. `thesis-progress/decisions/active/model_revision/12_flow_and_start.md` (step 12, part D is yours).
5. `thesis-progress/decisions/active/model_revision/12_thesis_drafts.md` (thesis text, `[A70]` to `[A73]`
   still waiting for the author).

**Get the results.** Run `git pull` in `thesis-progress`. The sweep commits and pushes
`results/tests/step12_sweep/` when it finishes. Check its `overnight.log` ends with "done". If the folder
is missing, the sweep has not finished or its push failed, so stop and tell the author.

**What ran.** `scripts/sweep/overnight.bash` of `slap-mapd-coupling`, branch `feat/flow-and-start` at
`b6576b1`, on `configs/step12/fleet_{8,16,32,64}.yaml`, started 2026-10-27 12:12 from `bedtime.bash step12`:
- step 1 and 2, Token Passing load sweeps under fixed storage, 20 seeds per rate, then finer rates around
  each fleet's capacity, in `arrival_rates/load_fleet<m>/` (`load_sweep.jsonl`, `capacity.json`,
  `summary.md`),
- step 3, each fleet's main load, 0.6 of its capacity,
- step 4, the sensitivity sweeps at the main load, 20 seeds per value, in
  `parameter_sweep/fleet_<m>/<setting>/`: `arrival.refill_units` (Q = 15, 30, 60, under fixed, demand and
  random storage), `storage_rule.epoch_length`, `storage_rule.congestion_weight`, `demand.skew`,
  `demand.rotation_period`, `demand.rotation_share`.

Every episode ran 10000 steps with a 5000-step warm-up left out of the measures, and every seed played
its own warehouse (D27). The SKU counts are provisional, 20, 60, 140 and 320 SKUs at 8, 16, 32 and 64
agents, with two shelves per SKU and Q = 30.

**Caveat that changes how you read it.** The sweep ran before commit `b44db09`. In it, fixed storage's
home shelves were the shelves of the random start, so fixed storage was random dedicated storage, a weak
baseline. The agreed model (`[A69]`) gives it class-based homes instead. So:
- capacities and main loads under fixed storage are likely too low,
- every gain of demand over fixed storage in the sensitivity sweeps is likely too large,
- units per step, put-aways per run, lines that waited for stock and the shape of the Q sweep are still
  usable for sizing.

A second, smaller caveat. The sweep also ran before `2817ca7`, so the storage rules weighed the put-away
leg from the nearest dock, not the mean over the docks (`[A70]`). Refills still came from random docks.
This shifts which shelves demand and congestion storage chose, not the load the fleet carried.
Say this wherever you report a number it affects.

**Your task, part D of `12_flow_and_start.md` (D25).**

1. Check completeness. Every fleet should have a `capacity.json` with a main load, and every sensitivity
   sweep its rows. List what failed, with the line of the log that shows why.
2. Per fleet, report the capacity, the first failing rate, the main load, and at the main load the
   keep-up of picks and of put-aways, the backlog slope and the longest gap between finishes. Compare the
   capacities with the old model's (`results/E_load/`), and say what changed and the likely reason
   (shipping adds a trip per order, docks along the left wall, random workstations, fewer shelves).
3. Size the SKU count and Q. Units ordered per step at the main load are the rate times the mean units
   per line (3, lines of 1 to 5 units). With Zipf skew 1 over n SKUs, a SKU of middle rank gets a known
   share of those units, so its refills per demand cycle of 4000 steps follow for each Q. Propose n and Q
   per fleet so that a SKU of middle rank is refilled about four times per demand cycle, subject to
   2n shelves fitting on the rack faces left after the workstations (counts in
   `results/D_warehouses/step12/summary.md`, shelves plus parking from the rack faces). Check the
   proposal against the Q sweep: put-aways per run, the share of lines that waited for stock (about 1 %
   is what the service level aims at), and keep-up. Show the arithmetic.
4. Name what must be rerun once the author agrees: at least the full sweep on the final configs, with the
   class-based homes of `b44db09`, after the step 12 settings move into `configs/fleet_<m>/` as part D
   says.

**Deliverables.** Write `thesis-progress/results/tests/step12_sweep/README.md` with the tables and the
proposal, and a short "Sizing proposal" under part D of `12_flow_and_start.md`. Commit and push
`thesis-progress` only those two files. Change no config, no code and no thesis text. The author decides
the values, and per `CLAUDE.md` you propose and wait. Report back in chat with the proposal and the open
questions, in plain words.

**Rules.** Run only the tests of code you change, and you change none here. Result files over 5 MB stay
out of git (`project_large_traces` in memory). UK spelling. In anything meant for the thesis, no dashes
and no colons or semicolons joining clauses.
