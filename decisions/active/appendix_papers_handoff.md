# Handoff: write the appendices as short papers

Written 2026-10-21 for the agent that continues the appendix work. The structure is built
and agreed with the author. Appendix C is the finished template, apart from its results
table. What is left is finishing C and then writing D to J in the same shape.

## Read first

- `CLAUDE.md` and `AGENTS.md` at the workspace root. "Thesis writing style" in `CLAUDE.md`
  applies to every sentence you write.
- `LATEX.md` at the workspace root, section "Appendices". It covers how an appendix file
  starts, the label scheme and the build.
- `thesis/Appendices/C.Warehouses.tex`, the template. Read the PDF too
  (`thesis/Appendices/C.Warehouses.pdf`).
- `thesis-progress/decisions/ideas/Appendixes.md`. It lists every number with its source
  (*cited*, *derived*, *tested*, *open*) and the test proposed for each open one. That file
  is the work list for D to H.
- `thesis-progress/decisions/active/appendix_plan.md`, section "Third round". It has the
  table of all eleven appendices and where their text came from.

## What the author wants an appendix to be

Each topic appendix is a short paper a reader can understand without the thesis. It goes
deeper into one subject the main text only summarises. It is not a place for text cut out
of a chapter. Notation (A), Parameters (B) and Definitions in full (K) are reference
material and stay as they are.

Every topic appendix has the same five parts, as subsections:

1. **Summary.** The question, the answer, and which values it sets in the thesis. Four to
   six sentences.
2. **Setting.** The few terms the paper needs, one sentence each, with exactly the
   definitions and symbols of the thesis (the chapters are the source of truth, and
   `Appendices/A.Notation.tex` decides which letter means what). End with why the subject
   matters for the thesis.
3. **Method.** How the thing is built, measured or tested, in plain words first and then
   "Formally," where an equation helps. Give the reason for every choice. A topic with
   formal detail but no experiment (F, I) puts that detail here, in subsections with
   their own titles, as C does with "Well-formed instances".
4. **Results.** Tables and figures, then one or two sentences on what they show, without
   restating them. Pilot runs go here as `\subsubsection{Pilot: ...}`.
5. **Conclusion.** What is settled, with its source, and what is tested for feasibility
   only or still open.

### The thesis holds the design, the appendices hold the experiments (author, 2026-10-23)

The thesis keeps the argument and the design: the definitions, the equations and a short,
precise reason for each choice. The appendices hold the experiments behind those choices.
An experiment appendix is a short paper on one test or one group of tests that sets values
the thesis uses, for example the warehouse sizes or the main load. Its Setting names only
the few terms the test needs and points to the thesis for the design. It does not restate
the whole design.

The thesis cites each test with one sentence of the form "tested with Token Passing in
Appendix X, so the experiments use this value, because ...". **For now this is only
noted.** The thesis chapters stay exactly as they are, and only the appendices change.

Design text that was moved out of the chapters to save pages (worked examples,
derivations, the formal equations) is reference material, not an experiment. It is kept
in reference appendices, ordered like the thesis.

**The formal definition of the model stays in the thesis (author, 2026-10-23).** The
equations that define the model are what the examiners grade in the Problem Formulation,
so they are never moved out of the thesis. The formal statements now in
`C.ModelDetails.tex` (the subsection "Definitions in full", `app:defs`) were moved out
earlier to save pages. When the thesis is reworked, they go back into the Problem
Formulation and the Method, and C keeps only derivations and worked examples. Until then
nothing moves, and the thesis stays as it is.

**Background and related work stay in the thesis.** They are graded parts that show where
the work fits. If either grows too long, the extension goes in an appendix paper, for
example an extended survey or a comparison table, and the argument stays in the thesis.

The submission is a main paper plus a zip folder of appendix papers, so every appendix is
its own document and must be readable on its own for its experiment.

Text already in an appendix was moved from the chapters word for word. Keep it, but you may
make it part of the discussion as C does. Change a sentence that only made sense where it
used to be, and remove phrases such as "this appendix" or "fixed above". List every change
to moved text in your report.

## Status on 2026-10-23, after the split

The appendices were split by experiment on 2026-10-23 (agreed with the author). The
reference appendices hold the design text moved out of the chapters, and every other
appendix is a short paper on one experiment. Every label moved with its text and kept its
name, apart from three new placeholder labels (`app:demand:sweep`, `app:results:tests`,
`app:results:stock`). The files before the split are in
`~/thesis_backups/appendices_before_split_2026-10-23.tar.gz`.

| | File | Kind | Came from | State |
|---|---|---|---|---|
| A | `A.Notation.tex` | reference | A | leave alone, except to add a symbol a paper needs |
| B | `B.Parameters.tex` | reference, with a Source column | B | update a Source entry when a paper settles a value |
| C | `C.ModelDetails.tex` | reference | design parts of old E, F, H, and old J and K | moved text, ordered like the thesis |
| D | `D.Warehouses.tex` | experiment, generator | old C | **template**, Setting trimmed to the terms the test needs |
| E | `E.Load.tex` | experiment, Token Passing | old D | Method written, sweep placeholders, pilot of load levels |
| F | `F.Demand.tex` | experiment, Token Passing | old D | skeleton, drift pilot and sweep figure in Results |
| G | `G.StorageValues.tex` | experiment, Token Passing | tests of old E | skeleton, shelf capacity in Method, three calibrations in Results |
| H | `H.Horizon.tex` | experiment, Token Passing | tests of old H | skeleton, horizon and stall placeholders. **Horizon not decided** |
| I | `I.Reward.tex` | experiment, training | tests of old F | skeleton, depth, reward and discount placeholders |
| J | `J.Training.tex` | experiment, training | old G | skeleton, checkpoint rule in Method, four calibrations in Results |
| K | `K.Checks.tex` | experiment, every run | old I | moved text, not yet in five parts |
| L | `L.Results.tex` | full results of the test runs | test tables of old H and E | placeholders, waits for the long run |

The research questions stay in the Experiments chapter. L only holds every measure of the
test runs. Where each value goes is in `appendix_values_overview.md`.

## Order of work

The steps below were written before the split and name the old letters. Read them by
topic: old C is D, the load parts of old D are E and its drift parts F, the tests of old E
are G, the tests of old F are I, old G is J, the tests of old H are H, old I is K. The
design text of old E, F, H, J and K is now in C and needs no new writing.

### 1. Finish C (done 2026-10-21)

The table is filled from the run below, and every seed passed. Kept for reference.

The 50-seed instance report was started on 2026-10-21 and writes to
`~/thesis_runs/instance_report_2026-10-21/`. If `summary.md` is there, use it. If not, run it
again (about 30 minutes, from the worktree of the branch that holds the generator):

```bash
cd ~/worktrees/fix-warehouse-scaling
~/.venvs/rl/bin/python scripts/instance_report.py \
    --configs configs/fleet_8/centralised.yaml configs/fleet_16/centralised.yaml \
              configs/fleet_32/centralised.yaml configs/fleet_64/centralised.yaml \
    --seeds 50 --out ~/thesis_runs/instance_report_2026-10-21
```

Then, in "Results" of C:
- Replace the TODO with a table (`booktabs`, one row per fleet size). The columns are
  |V|, aisles, cross-aisles, role counts, the share of role vertices, mean degree, discard
  rate, pass rate over 50 seeds, mean $d^{\mathrm{trip}}$ and generation time. Leave out
  a column that tells the reader nothing.
- Add one or two sentences on what the table shows.
- Check the sentence in "Summary" that says every generated warehouse passes. It carries a
  `% TODO: confirm` comment. If not every seed passes, say so honestly in Summary, Results
  and Conclusion, and tell the author.
- `thesis-progress/decisions/active/graph_appendix_handoff.md` has more detail on this
  step. Its section "What to write" is done apart from the table.

### 2. Write what needs no new runs

These can be written now from the thesis chapters, the code and the text already in the
files: E, F, H, I and J in full, and the Setting and Method of D and G. Do them one
appendix at a time, and show the author each finished one before starting the next. The
author asked to read C before it is used as the template, so if they have not given
feedback on C yet, ask for it first.

What each one holds:
- **D, Load and demand.** Orders, lines and units, the release rate, the Zipf law and its
  drift, keep-up and $f_{\mathrm{up}}$ (`sec:impl:instances`, `sec:pf:tasks`,
  `sec:pf:measures`). The two pilots stay in Results. The load sweep is the method and the
  main result, so it waits for step 3.
- **E, Storage and inventory.** Capacity with the worked example, the arrivals, the
  starting stock, ties, and shelf capacity. Shelf capacity is *derived* in `Appendixes.md`
  section 2, so it can be written now as a calculation. The arrival-against-relocation
  pilot goes in Results. Δ and β wait for their sweeps.
- **F, Controllers, observations and reward.** The learning problem, what each controller
  reads, the example observation and the distance-label bound go in Method. The reward
  weights and $d_{\mathrm{obs}}$ wait for their tests. The source for $d_{\mathrm{obs}} = 5$
  (van Knippenberg et al. 2021, Table 5) needs checking in
  `thesis-progress/papers/knippenberg21a.pdf` before it is cited.
- **G, Model and training.** Write the Setting now. The rest waits for step 3. Checkpoint
  selection is a decision for the author (see below).
- **H, Measures and evaluation.** Order completion, put-away time, runtime, the decision
  problem and blocked time. The horizon waits (see below).
- **I, Logging and correctness checks.** Write it as a paper with the question "does the
  simulator implement the model?". The Method is what is logged and the four checks. The
  Results are the outcome of the checks on the runs, if they are logged anywhere. If they
  are not, leave a TODO.
- **J, What the model leaves out.** Deadlines and re-tasking. Dock capacity is a TODO with
  a proposed answer that the author has not yet decided. Keep it short, since it is a
  discussion without experiments, so Results may be empty. Say so in the Summary rather
  than adding an empty subsection.

### 3. Tests, only after the author agrees

Many values in `Appendixes.md` need a run: the load sweep (D), Δ and β (E), the reward
weights and $d_{\mathrm{obs}}$ (F), L, widths, PPO values and budget (G), and the horizon (H).
**Do not start a training run or a sweep without the author's go-ahead.** Agree the plan
for each test with them first. Then the run goes in Results, the value in Conclusion, and
its Source entry in `B.Parameters.tex` changes from *open* to *tested*. Tests with Token
Passing only, such as the load sweep, Δ and β, are cheaper. Propose those first.

## Rules

- **No commits, no pushes.** `thesis/` holds a lot of uncommitted work and syncs with
  Overleaf. Leave everything uncommitted and report what changed.
- **Build and check after every appendix.** Run from `thesis/`:

  ```bash
  python3 tools/sync_xrefs.py --build
  for f in main.log Appendices/*.log; do echo "$f $(grep -cE '(Reference|Citation) .* undefined' $f) $(grep -c 'multiply defined' $f)"; done
  ```

  Every count must be 0. Then look at the PDF of the appendix you changed (`pdftoppm`
  renders pages you can read).
- **Labels.** The scheme is `app:<topic>:<part>`, and `app:cal:<what>` for a calibration.
  Never remove a label that `Chapters/*.tex` or `B.Parameters.tex` refers to. Move it to the
  place that now holds its content.
- **The model stays in the chapters.** An appendix restates a definition in the same words
  and symbols, never differently. An experiment appendix names only the terms its test needs and points to the
  thesis for the rest. If writing shows that the chapters are wrong or unclear,
  report it rather than changing the chapters.
- **Captions.** 25 words or fewer, naming what the figure shows (`LATEX.md`, "Figure
  captions").
- **Citations.** Cite only what the paper in `thesis-progress/papers/` actually says. Mark
  anything you could not check with `% TODO: check`.
- **Do not invent values.** A value that `Appendixes.md` marks *open* stays open until a
  test or the author settles it.

## Decisions that are the author's

List these when you meet them. Do not settle them yourself.
- **Evaluation horizon.** It is T = 630 in `tab:evalparams` (`[A31]`) and `horizon: 2000` in
  the configs. THIS IS NOT DECIDED AND SHOULD BE REASONED FOR
- **Checkpoint selection.** It is by training return in the configs and on validation seeds
  in the thesis.
- **Dock capacity.** Should it be unlimited, as `Appendixes.md` section 2 proposes? I think so 
- **The ratio of two agents per shelf and dock.** Cite a source, or test it with m/4?
- **The reason for two-way edges.** It is still unconfirmed (`graph_appendix_handoff.md`).

## Also open, small

About ten places in `Chapters/2.Introduction.tex` use `\Nref` in the middle of a sentence,
for example lines 221 and 808, so they print a capital "The". They should be `\nref`. Fix
them only if the author agrees, since it touches the chapters.

## Report back, after each appendix

- What you wrote, and which moved sentences you changed.
- Any definition you could not match to the chapters.
- Citations you could not check.
- Values whose Source changed in `B.Parameters.tex`.
- The build result.
