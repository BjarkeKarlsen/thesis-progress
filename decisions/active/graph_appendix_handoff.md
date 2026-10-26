# Handoff: the warehouse graph appendix (`app:instances`)
Link this issue to the `split_up_appendix_for_better_structure.md` since the appendix structure as it right now does not work
Written 2026-10-21 for the agent that writes the appendix. The decisions are taken and the
code is done. What is left is running the measurements and writing the text.
Link this issue to the `appendix_plan.md` since the appendix structure as it right now does not work
## Goal

The appendix shows how the warehouse graph is generated for every fleet size
(m = 8, 16, 32, 64). It explains in plain words why each instance is well-formed and
reports the structure of many generated instances. It ties the sizes to van Knippenberg
et al. (2021). This is the first of the "one test per number no paper gives us" appendices
listed in `thesis-progress/decisions/ideas/Appendixes.md`.

## Decisions already taken (`[A57]` in `GAPS.md`)

- The fleet size decides the warehouse. `|V| = 16 m` gives 128, 256, 512 and 1024 vertices.
  These are the sizes van Knippenberg et al. (2021) use for 32 and 64 agents
  (`thesis-progress/papers/knippenberg21a.pdf`, Tables 4 and 5). Their 64-agent runs use
  1024 nodes, and they note that gridlock weighs heavily on the results for smaller graphs.
- Roles: `|V_ep| = m` (parking, the fewest well-formedness allows), `|V_str| = m/2` (so that
  agents need the same shelves, the author's choice), and `|V_del| = |V_rcv| = m/2`. Two
  agents per dock at every fleet size, so the crowding at a dock means the same at every
  size. An earlier `max(4, m/4)` was dropped because its floor gave m = 8 a different ratio.
  The ratio 2 has no source or test beyond well-formedness, so the text must not claim more.
- Every edge is two-way in the experiments. One-way edges remain a feature of the model.
  The reason given in the text ("so a difference between fleet sizes cannot come from which
  segments happen to be one-way") is a proposal the author still has to confirm.
- The shape bounds follow from |V|: aisle length at most `ceil(sqrt|V|)`, at most
  `ceil(1.1 sqrt|V|)` aisles, and at most `ceil(0.7 x aisle bound)` cross-aisles. The factors
  1.1 and 0.7 are our own numbers. Their test is the pass rate over 50 seeds below.
- Fleet warehouses place roles by the exact well-formedness check alone
  (`role_backbone: false`). Older configs keep the stricter "plain vertices stay strongly
  connected" condition (`role_backbone: true`, the default), so they still give the same
  instances.
- The receiving vertices count as endpoints in the well-formedness check. A put-away task
  is picked up at one.

## Code (slap-mapd-coupling)

Branch `fix/warehouse-scaling`, worktree `~/worktrees/fix-warehouse-scaling`. The author
merges it into `main`.

- `src/slap_mapd_coupling/instances/generator.py`: `fleet_defaults(num_agents)` holds the
  rule above, and `GeneratorParams.role_backbone` switches the role check.
- `src/slap_mapd_coupling/training/spec.py`: `TrainingSpec.instance_settings()` and
  `instance_params(spec)` give `fleet_defaults(num_agents)` when the config has no
  `instance:` section, and that section as written otherwise. `GeneratorParams` is
  unchanged, so a warehouse built outside training takes the same input as before.
- `configs/fleet_{8,16,32,64}/*.yaml`: there is no instance section, so the warehouse comes
  from `experiment.num_agents` alone, with seed `FLEET_INSTANCE_SEED = 42` in the code. A
  config that has an `instance:` section (all older configs) builds that warehouse exactly
  as written.
- `scripts/instance_report.py`: generates every fleet over the seeds, checks connectivity
  and well-formedness, and measures each instance.

## How to run everything

Run from the workspace root (`~/Documents/thesis`) unless noted. Use the shared venv.

1. Tests (in `slap-mapd-coupling`, after the merge):

   ```bash
   cd slap-mapd-coupling
   ~/.venvs/rl/bin/python -m pytest tests/unit                  # everything, about 5 min
   ~/.venvs/rl/bin/python -m pytest tests/unit/test_generator.py tests/unit/test_validation.py \
       tests/unit/test_training_spec.py --no-cov                # the graph tests only
   ```

   `test_arrival_config.py` already fails 16 times on `main`, before this branch. That is not
   from this work.

2. Instance report, 50 seeds per fleet. About 30 min, mostly the 64-agent well-formedness
   check:

   ```bash
   cd slap-mapd-coupling
   ~/.venvs/rl/bin/python scripts/instance_report.py \
       --configs configs/fleet_8/centralised.yaml configs/fleet_16/centralised.yaml \
                 configs/fleet_32/centralised.yaml configs/fleet_64/centralised.yaml \
       --seeds 50 --out ~/thesis_runs/instance_report_2026-10-21
   ```

   The run writes three files:
   - `instance_report.jsonl` has one row per instance.
   - `summary.md` has the table per fleet size (pass rate, discard rate, |V|, segments,
     aisles, cross-aisles, role counts, role share, mean degree, roles on leaves, mean
     d^trip, seconds) and the instance each config uses (seed 42).
   - `instances_used.json` holds the four seed-42 instances for the figure.

   A run on 2026-10-21 is in `~/thesis_runs/instance_report_2026-10-21`. Use it unless the
   code changed.

3. Figure of the four warehouses:

   ```bash
   cp ~/thesis_runs/instance_report_2026-10-21/instances_used.json \
      thesis-progress/scripts/images/data/instances_used.json
   ~/.venvs/rl/bin/python thesis-progress/scripts/images/warehouses.py
   cp thesis-progress/scripts/Images/warehouses.png thesis/Images/warehouses.png
   ```

   `warehouses.py` reads only the JSON, so it needs nothing from the codebase. It is also
   called from `figure.py`, but that rebuilds every figure.

## What to write

In `thesis/Appendices/C.Warehouses.tex` (written 2026-10-21 except the results table), replace the TODO in Results. Keep the
starting-stock part that is already there. Suggested order, one idea per paragraph:

1. **How a warehouse is generated.** In words:
   - Aisles of different lengths, with a front row on the inbound side and random
     cross-aisles. Every edge costs 1.
   - Receiving vertices on the front row. The other roles are drawn at random from the
     rest.
   - A layout that no role placement makes well-formed is dropped, and the next one is
     drawn from the same seed.
   - Cite `\citet{vanKnippenberg2021}` as the inspiration (a generated non-lattice graph,
     unit costs). Their graphs are train-yard shaped with diagonal links, and ours are
     aisles, so say that ours differ in one clause.
2. **Why the result is well-formed, in simple terms.** The check is the condition of
   `app:wellformed`. There are m parking vertices by construction. A search from every role
   vertex must reach every other one without passing through a third. Every edge is two-way,
   but the check is run in both directions anyway. The guarantee that Token Passing never
   deadlocks is the theorem of `\citet{ma2017lifelong_mapf}`. Cite it and don't prove it
   again.
3. **The sizes.** The 16 m rule and the role rule, with the reason for each (see above). Name
   the rejected alternative in one clause at most. The size used to be drawn at random per
   seed (86 to 131 vertices at m = 8).
4. **The test.** A table with one row per fleet size from `summary.md`: |V|, segments,
   aisles, cross-aisles, each role count, the vertices that are role vertices, the mean
   degree, the discard rate, the pass rate over 50 seeds, the mean d^trip, and the
   generation time. Then one or two sentences on what the table shows, without repeating
   it.
5. **The figure.** `\myfig[t]{warehouses.png}{...}{warehouses}`. Caption 25 words or fewer,
   and don't restate the legend or colours.

Check `thesis/Chapters/Appendix/A.Notation.tex` before using a symbol. |V|, m, V_ep,
V_str, V_del, V_rcv and d^trip already exist. If a new symbol is needed, add it to the
table.

Writing rules (workspace `CLAUDE.md`, "Thesis writing style"):
- Words first, then the equation ("Formally,").
- No dashes, and no colons or semicolons joining clauses.
- Short paragraphs that lead with the idea.
- UK spelling.
- No meta-commentary.
- Give the reason for each choice.
- Don't restate the figure.

Add `% [A57]` to the new paragraphs.

## Thesis text already edited (uncommitted in `thesis/`)

- `4.Implementation.tex`, `sec:impl:instances`: two-way edges, the 16 m and role rules,
  and the dropped claim that our placement follows Ma et al.
- `Appendix/B.WellFormed.tex`: the receiving vertices are endpoints.
- `GAPS.md`: the `[A57]` entry.

Still to align once the appendix is written:
- **Experiments chapter.** The "Instances" paragraph of `5.Experiments.tex` is still a
  mockup. It can point to `app:instances`.
- **Appendix H.** Add a row per instance parameter (16 m, m/2 shelves, m/2 docks, the shape
  factors).

## Open, for the author

- Confirm the reason for two-way edges.
- **Shelf capacity.** The 8-agent configs use `vertex_capacity: 300`, because 4 shelves hold
  up to 240 units at the start. Settling this is the storage appendix's job
  (`Appendixes.md`, "The Storage").
- The arrival rate per fleet size comes from the Token Passing load sweep at 0.6 of each
  fleet's capacity, not from linear scaling (`Appendixes.md`).


