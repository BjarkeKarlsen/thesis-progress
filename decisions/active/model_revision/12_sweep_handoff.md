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
`1056911` or later, on `configs/step12/fleet_{8,16,32,64}.yaml`, from `bedtime.bash step12` (restarted
2026-10-27 after the layout changes, the first start's partial rows are in
`~/thesis_runs/archive/step12_sweep_old_layout*/` and are not to be used):
- step 1 and 2, Token Passing load sweeps under fixed storage, 20 seeds per rate, then finer rates around
  each fleet's capacity, in `arrival_rates/load_fleet<m>/` (`load_sweep.jsonl`, `capacity.json`,
  `summary.md`),
- step 3, each fleet's main load, 0.6 of its capacity,
- step 4, the sensitivity sweeps at the main load, 20 seeds per value, in
  `parameter_sweep/fleet_<m>/<setting>/`: `arrival.refill_units` (Q = 15, 30, 60, under fixed, demand and
  random storage), `storage_rule.epoch_length`, `storage_rule.congestion_weight`, `demand.skew`,
  `demand.rotation_period`, `demand.rotation_share`.

Every episode ran 10000 steps with a 5000-step warm-up left out of the measures, and every seed played
its own warehouse (D27). The warehouses are the agreed step 12 model: stacked rack blocks of 4 rows with
cross lanes and the one-way pair in the middle (6 aisles and 2 blocks at 8 agents, 7 and 4 at 16, 10 and
6 at 32, 15 and 8 at 64), every inner aisle segment irregular, delivery vertices on random rack faces,
receiving vertices along the left wall, exactly $m$ parking vertices spread over the rack faces left,
shipping to a random dock, fixed storage with class-based homes
(`[A69]`) and the put-away leg as the mean over the docks (`[A70]`). The SKU counts are provisional,
20, 30, 50 and 100 SKUs at 8, 16, 32 and 64 agents, with two shelves per SKU and Q = 30.

**Check first** that the run is this one: `~/thesis_runs/queue_<date>/code_step12/base_commit.txt` on the
PC that ran it should be `1056911` or later. If it is earlier, the run is the first start, so stop and
tell the author.

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
