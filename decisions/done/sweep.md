# Task: finish the load sweep (set fleet 8 and 16 rates, figures, appendix text)

Workspace: ~/Documents/thesis. Read CLAUDE.md and AGENTS.md at the root first. They hold the
thesis prose style rules and the caption rules (LATEX.md, "Figure captions"). Use
~/.venvs/rl/bin/python, never bare python. Do not commit or push anything. The author does that.

## 0. Check the runs are finished
Results are in ~/Documents/thesis/thesis-progress/results/arrival_rates/load_fleet{8,16,32,64}/.
Each folder has load_sweep.jsonl, summary.md and capacity.json, written by
slap-mapd-coupling/scripts/sweep/load_sweep.py.
- Make sure no `scripts/sweep/load_sweep.py` process is still running (`ps -eo pid,args | grep load_sweep`).
- Every rate should have 50 seeds. Expected rates are fleet 8 at 0.2 0.3 0.4 0.5,
  fleet 16 at 0.1 0.2 0.25 0.3 0.4 0.5 0.6, fleet 32 at 0.5 to 0.9 plus 0.36,
  fleet 64 at 0.7 0.8 0.9 plus 0.42. Fleets 8 and 16 should also have a row set at their own main load.
- If anything is missing, stop and tell the author which (fleet, rate) has fewer than 50 seeds.
  Do not start runs yourself.
- Leave load_fleet8/*.before-2026-10-22.* alone. They are the rows from before 2026-10-22, kept for reference.

## 1. Set arrival_rate for fleets 8 and 16
Read "main_load" from load_fleet8/capacity.json and load_fleet16/capacity.json (0.6 × capacity).
If either is null, stop and report. Do not guess a rate.
In slap-mapd-coupling/configs/fleet_8/*.yaml and configs/fleet_16/*.yaml (centralised,
decentralised, section), make the same change already made to fleets 32 (0.36) and 64 (0.42).
Use configs/fleet_32/centralised.yaml as the reference.
- Header comment becomes:
  "# Values are illustrative and are not thesis values, apart from the arrival rate, which the
   # Token Passing load sweep sets (scripts/sweep/load_sweep.py). Everything else is
   # configs/medium_arrival. ..."
- The "# An overload on this instance. ..." block above arrival_rate becomes the
  "# Selected main load from the fixed-storage Token Passing load sweep, ..." block, and
  `arrival_rate: <main_load>`.
configs/fleet_8/decentralised.yaml has uncommitted author edits (sku_names). Change only the
two comment blocks and the rate line there, nothing else.
Check with:
  ~/.venvs/rl/bin/python -c "from slap_mapd_coupling.training.spec import load_spec; from pathlib import Path; [print(f, load_spec(f).arrival_rate) for f in sorted(Path('configs').glob('fleet_*/*.yaml'))]"
Every fleet's three arms must agree.

## 2. Figures
From ~/Documents/thesis:
  ~/.venvs/rl/bin/python thesis-progress/scripts/images/load_sweep.py
This writes thesis-progress/scripts/Images/load_fleet{8,16,32,64}.png. Open each PNG and check
that labels don't collide and that the capacity (dashed) and main load (solid) lines are there.
Fix any problem in the script, not in the PNG. Then copy the four PNGs into thesis/Images/.
Always copy from thesis-progress to thesis, never the other way.

## 3. Appendix text
File: thesis/Appendices/D.LoadDemand.tex, subsubsection "The load sweep" (\label{app:sweep}).
Replace its TODO comment. thesis/ syncs with Overleaf, so change nothing else in the file.
- Four figures with \myfig[t]{load_fleet<m>.png}{<caption>}{load_fleet<m>}. The label becomes fig:load_fleet<m>.
- Captions follow LATEX.md. One or two sentences, at most 25 words, with no dashes, colons or semicolons.
- Prose follows the "Thesis writing style" rules in CLAUDE.md. Short paragraphs, each leading
  with its point. Plain words. No `--`/`---`, and no colons or semicolons joining clauses. UK spelling.
- Content to cover, using the numbers in the final data (recompute them from load_sweep.jsonl, do not copy these):
  * The capacity and main load of each fleet, as a small table (fleet, capacity, first failing rate, main load).
  * Tasks waiting for a robot at the end of the run grow steeply past the capacity. At the main
    load they stay low. Give the mean at the main load per fleet.
  * Waiting is almost all tasks waiting for a robot, not orders waiting for stock (num_waiting_orders is small).
  * About half the fleet is busy (num_active_tasks ≈ m/2) even when hundreds of tasks wait, and
    fleet 64 finishes about as many tasks as fleet 32 at the same rate. Do NOT write a cause for
    this into the thesis. Report it to the author as an open question (Token Passing assignment
    rule or too few delivery/receiving vertices is a guess, not verified).
- Do not touch the Summary or Conclusion TODOs. Propose text for them in your reply instead.
- If thesis/tools/sync_xrefs.py exists, run `python3 tools/sync_xrefs.py --build` from thesis/
  so the new labels resolve. Compile the appendix per LATEX.md and report any warnings.

## Report back
The rates set for each fleet, the figure paths, and a diff of D.LoadDemand.tex. Also report
anything odd in the data, and proposed Summary and Conclusion text. The author reviews before
anything is committed.