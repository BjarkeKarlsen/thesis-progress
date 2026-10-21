# Handoff: restructure the appendices

Written 2026-10-21 for the agent that does the restructure. The structure is agreed with
the author. What is left is moving the files, changing how the main text includes them,
adding the Source column and leaving skeletons for the calibration tests.

Background, read these first:
- `decisions/ideas/Appendixes.md`. The rule this structure serves: every number that
  does not come from a paper gets an appendix that shows how it was found. It also has
  the source of every value (*cited*, *derived*, *tested*, *open*).
- `decisions/ideas/split_up_appendix_for_better_structure.md`. Group the appendices by
  the question a reader brings, not by topic of the code. Label pilots as pilots.
- `decisions/active/appendix_plan.md`. How the current 13 appendices came about, and
  the rule for moving text.
- `LATEX.md` at the workspace root, "Appendix document", and `thesis/tools/sync_xrefs.py`.
- `CLAUDE.md` at the workspace root, "Thesis writing style".

## Before you start

- `thesis/` had 16 uncommitted changes on 2026-10-21. Ask the author to commit and push
  them, then `git pull` in `thesis/`. Do not start on a dirty tree, so the restructure is
  one reviewable change on its own.
- Do not commit or push. Leave the work uncommitted and report what changed. The author
  commits it and syncs Overleaf.
- `decisions/active/graph_appendix_handoff.md` writes into `app:instances` at the same
  time. Keep that label on the warehouse appendix (C below), so the two handoffs do not
  clash. If its text has already landed in `C.Instances.tex`, move it along with the rest.

## Decisions taken

### 0. An appendix extends a part of the main text

An appendix is not a place for text cut out of a chapter. Each one takes a topic the
main text covers, for example the warehouse instances of `sec:impl:instances` or the
storage rule of `sec:pf:storage`, and gives it in full, with the details, derivations,
worked examples and calibration the main text leaves out. A reader should be able to
read one appendix on its own and come away with the whole topic.

So every appendix is built the same way.
1. **An opening recap.** One short paragraph that says in plain words what the main text
   says about the topic, and which section says it. It uses the same terms and the same
   definitions as the main text. It never restates a definition differently, because
   the chapters stay the source of truth.
2. **The extension.** The subsections with the detail, each opening with its point. Moved
   text goes here. Where moved text only makes sense next to the paragraph it left, add
   one bridging sentence rather than more moved text.
3. **Calibration last.** The subsections that say how the values were found (see 6).

When merging, check that each appendix covers its topic as a whole. Where a part is
missing (the load sweep is only a TODO today, and the generated graphs have no figures
yet), list it in the report instead of filling the gap with more text from the chapters.
The main text keeps the idea in words and the result, as `appendix_plan.md` says, so do
not move more out of the chapters in this change.

### 1. The appendices go at the end of `main.tex`

Today the appendices are a separate document (`appendix.tex`), and the two documents
share labels through `tools/sync_xrefs.py` and the generated `styles/xref-*.tex`.
This changes as follows.

- **The appendices move to their own folder, `thesis/Appendices/`**, next to
  `Chapters/`. They are not chapters, and one level less makes every relative path
  shorter (`../appendix.tex`, `../Images/`). Use `git mv`. Update the
  `\documentclass[../appendix.tex]{subfiles}` line and the `\graphicspath` of each file.
- **Each appendix stays its own file**, a `subfiles` document that compiles on its own.
  Today it does not do so cleanly (tested 2026-10-21, all 13 alone). Every file gives a
  PDF, but references into the main text and every citation print as ??, because
  `appendix.tex` and `styles/preamble.tex` load `styles/xref-main.tex` and
  `references.bib` by paths relative to `thesis/`. `B.WellFormed.tex` stops with an
  error, because `\myfig` and its variants in `styles/mymacros.sty` read `./Images/`.
  Wrap these paths in `\subfix{...}` (subfiles package), or put `Images/` on the
  `\graphicspath` and drop the `./Images/` prefix from the macros. After the fix, a file
  compiled alone shows only references to other appendices as ??.
- **One shared list file**, `Appendices/appendices.tex`, holds everything both
  builds need, in this order:
  1. `\appendices` and the numbering setup now in `appendix.tex` (the `\counterwithin`
     and `\renewcommand` lines, so numbers read B.1, C.2).
  2. The overview, as an unnumbered section "Overview of the appendices" (see 4).
  3. The `\subfile` lines, one per appendix. Their order sets the letters, and this is
     the only place the order is written.
- **`main.tex`** inputs the list file right after `\printbibliography`, replacing the
  comment block "The appendices are a separate document". Add `\onecolumn` before it if
  the appendix tables need the full width, as `appendix.tex` does today. So the
  overview sits at the end of the thesis, before the first appendix.
- **`main.tex` no longer loads `styles/xref-appendix.tex`.** The appendix labels are now
  defined in the same document, and loading the file would define them twice. Delete
  `styles/xref-appendix.tex`.
- **`appendix.tex`** stays as a standalone build of the appendices alone. It inputs the
  same list file instead of its own `\subfile` lines and overview. It keeps loading
  `styles/xref-main.tex`, so a reference into the main text still resolves there and
  when one appendix file is compiled on its own.
- **`tools/sync_xrefs.py`** keeps only the direction main.aux to `styles/xref-main.tex`.
  Remove the other direction and update its docstring. Its existing rule of skipping
  labels defined in both documents takes care of the appendix labels that main.aux now
  contains.
- The page limit counts the main text up to the bibliography, so including the
  appendices in the same PDF does not count against it. biblatex collects citations from
  the whole document, so a source cited only in an appendix still appears in the
  bibliography. Check this after the build (see "Checks").

### 2. The structure, 13 appendices down to 10

| | File | Title | Main label | Takes in |
|---|---|---|---|---|
| A | `A.Notation.tex` | Notation | `app:notation` | A, unchanged |
| B | `B.Parameters.tex` | Parameters and where each value comes from | `app:params` | H, plus the Source column (see 3) |
| C | `C.Warehouses.tex` | Warehouses, demand and load | `app:instances` | B (well-formed), C (graphs part), D (load sweep), J (load levels, demand drift) |
| D | `D.Storage.tex` | Storage and inventory | `app:storage` | G, C (starting stock part), J (arriving against relocated stock) |
| E | `E.Controllers.tex` | Controllers, observations and reward | `app:controllers` | E (learning problem), K |
| F | `F.Training.tex` | Model and training | `app:training` (new) | new, calibration skeletons only |
| G | `G.Measures.tex` | Measures and evaluation | `app:measures` | F, plus the horizon calibration skeleton |
| H | `H.Checks.tex` | Logging and correctness checks | `app:repro` | I, unchanged |
| I | `I.Scope.tex` | What the model leaves out | `app:scope` | L, plus a skeleton for dock capacity |
| J | `J.Definitions.tex` | Definitions in full | `app:defs` | M, unchanged |

Notes on the table.
- Use `git mv` for files that keep most of their content (A, G to D.Storage, H to
  B.Parameters, I to H.Checks, L to I.Scope, M to J.Definitions, C to C.Warehouses,
  K to E.Controllers), so history follows them. Content merged from other files is cut
  and pasted into them, and the emptied files are deleted.
- Order inside a merged appendix follows the reader. C: the generated graphs and their
  well-formedness, then demand, then the load sweep. D: the starting stock, then the
  storage rule details. E: the learning problem, then the controllers and observations.
- F has no text today. If the author decides not to run the model and PPO tests, merge
  F into E and drop `app:training`. Ask rather than decide.
- An "Additional results" appendix comes later, once results exist. Do not create it now.

### 3. The parameter tables get a Source column

Every table in `B.Parameters.tex` (`tab:storageparams`, `tab:rlparams`,
`tab:modelparams`, `tab:trainparams`, `tab:evalparams`) gets a fourth column, Source.
It holds one of these:

- *cited*: the reference, `\citet{...}` with table or section if `Appendixes.md` gives it.
- *derived*: "derived, \ref{...}" pointing at the subsection with the calculation.
- *tested*: "tested, \ref{...}" pointing at the calibration subsection.
- *open*: "open". The value stays TBD or the config value as it stands in the table now.

Fill it from `Appendixes.md` only. Where that file does not cover a value, write *open*.
Do not upgrade a value to *cited* on the strength of "a common default", and do not
change any value in the Value column. The short paragraph at the top of the appendix says
what the four labels mean, in two or three plain sentences.

### 4. The overview

The overview replaces the "How to read the appendices" section of `appendix.tex`. Keep its
table (appendix, contents, referred from) and update it to the ten appendices above. Add
two sentences under it. The first says that the Source column of Appendix B says where
every value comes from. The second says that a subsection titled "Calibration" reports a
pilot that set a value, not evidence for a research question. Drop the sentence about the
separate document and the shared numbers, which no longer applies.

### 5. Subsections become numbered and labelled

The appendices use `\subsection*` today, so a subsection cannot be referred to. Change
them to `\subsection` with a label, so the Source column and the main text can point to
"C.3". Label scheme: `app:<appendix>:<topic>`, for example `app:storage:capacity`.

Old appendix labels that disappear as appendices stay as labels on the subsection that
now holds their content, so no `\ref` in the main text breaks:
- `app:wellformed` on the well-formedness subsection of C.
- `app:sweep` on the load sweep subsection of C.
- `app:game` on the learning-problem subsection of E.
- `app:pilots` is split over three places. Give each part its own label:
  `app:cal:load` (C), `app:cal:drift` (C), `app:cal:arrival` (D). Then repoint the four
  `\ref{app:pilots}` in `Chapters/4.Implementation.tex` (around lines 684, 685, 712 and
  714) to the one that fits each sentence, and drop `app:pilots`.

Check the main-text wording around each repointed reference. "Appendix~\ref{app:sweep}"
now prints "Appendix C.3", which reads fine. A sentence such as "the appendix on pilot
runs" may not.

### 6. Calibration skeletons

For each number `Appendixes.md` marks *open* with a proposed test, add an empty
subsection "Calibration: <what>" in the appendix below, with a `% TODO:` comment that
names the test as `Appendixes.md` proposes it and links its section there. Do not write
results or run anything. The three existing pilots become "Calibration" subsections with
their text unchanged.

| Appendix | Calibration subsections |
|---|---|
| C | role counts and shape factors (graph handoff), load point 0.6 of capacity, load levels and keep-up (existing J text), demand drift (existing J text) |
| D | shelf capacity (*derived*, a calculation, title it "Shelf capacity" without "Calibration"), storage period Δ, congestion weight β, arriving against relocated stock (existing J text) |
| E | observation depth d_obs, congestion reward weight n_cng, deliver reward n_deliver, override penalty n_blocked, discount γ |
| F | message-passing rounds L, hidden widths, PPO values, training budget, checkpoint selection |
| G | evaluation horizon |
| I | dock capacity (a short argument, not a test, see `Appendixes.md` section 2) |

## Writing rules for the moved text

- Moved text stays word for word, as `appendix_plan.md` requires. The opening recap of
  each appendix and the bridges between its parts are new writing (see 0).
- New sentences follow "Thesis writing style" in the workspace `CLAUDE.md`. No dashes,
  no colons or semicolons joining clauses, short paragraphs, UK spelling, no
  meta-commentary.
- A phrase in moved text that assumes context which is now gone (for example "the fleet
  size fixed above") is listed in the report, not rewritten.

## Mismatches to flag, not resolve

Filling the Source column will meet two places where the thesis and the configs disagree.
List them in the report and leave both as they are.
- The evaluation horizon is T = 630 in `tab:evalparams` (`[A31]`) and `horizon: 2000` in
  the configs.
- Checkpoint selection is by training return (`episode_return_mean`) in the configs and
  on validation seeds in the thesis.

## Documents to update in the same change

- `LATEX.md`, "Appendix document". Describe the new mechanism, including the one-way
  sync and the list file, and the subsection label scheme.
- `AGENTS.md` at the workspace root, the `thesis/` bullet on `appendix.tex`.
- `decisions/active/appendix_plan.md`. Add a "Third round" section with the new table,
  and point to this file.
- `SESSION_CONTEXT.md` only if it names an appendix letter. It did not on 2026-10-21.

## Checks

Run from `thesis/`:

```
latexmk -pdf main.tex
latexmk -pdf appendix.tex
python3 tools/sync_xrefs.py
latexmk -pdf main.tex && latexmk -pdf appendix.tex
```

- `main.log` has no undefined references, no "multiply defined" labels and no
  undefined citations.
- Every `\ref{app:...}` in `Chapters/*.tex` resolves (`grep -o 'app:[a-z:]*'` against the
  labels).
- The main PDF ends with the bibliography, then the overview, then appendices A to J.
  Main-text page count up to the bibliography is unchanged.
- `appendix.tex` builds, and every appendix file compiled alone builds with no ?? other
  than references to other appendices.
- Run the deterministic scripts of the `validating-latex-theses` skill for references and
  labels, if they run without the full audit.

## Last step: named equation references

About 23 sentences in the chapters refer to an equation as
"(Equation~\ref{eq:...} in Appendix~\ref{app:defs})". Change each to the named form,
`\nref{...}` or `\Nref{...}` at the start of a sentence, which prints "the vertex rule
(J.3)". Every label involved has a name in `styles/eqnames.tex` (checked 2026-10-21).
Do it sentence by sentence, not by search and replace. The named reference must not
end up inside brackets ("(the action set (J.1))"), and where the sentence already
names the term in words, rephrase so the name is not said twice. Find them with
`grep -rnE 'Equations?~\\ref' Chapters`. `Chapters/2.Introduction.tex:238` is done.

## Report back

- The final file list and the letter of each appendix.
- Every main-text reference that was repointed, with its old and new label.
- Phrases in moved text that no longer read right in their new place.
- Values whose Source you could not fill beyond *open*, and the two mismatches above.
- The build result, and the main-text page count before and after.
