# Brief for the section review subagents (2026-11-20)

You review ONE part of the thesis the way the author does, and fix only the
small known mistakes in that part. Many agents run at the same time on
other parts, so stay inside your scope.

## Read first
- `/home/bjarkek/Documents/thesis/CLAUDE.md` and `AGENTS.md` (workspace rules,
  thesis writing style). The style rules apply to every sentence you add.
- Invoke the skill `reviewing-like-the-author` (Skill tool) and follow it.
- `thesis-progress/decisions/active/readability_review/method_review_queue.md`,
  especially "Carry forward", "Mistakes against the code" and "Discussion".
- The earlier comments files in that folder (`method_storage_comments.md`,
  `method_model_comments.md`, `method_controllers_comments.md`,
  `method_resolution_comments.md`). Do not repeat a point already made.
  `method_controllers_comments.md` is the model for layout and tone.
- `thesis-progress/decisions/GAPS.md` for every `[Axx]` tag in your part
  (the newest entry settles a conflict) before asking for a reason.

## What the reader already has
- A Method section: the Introduction, Background, the Problem Formulation
  and every Method section before yours.
- An appendix: each appendix is its own short paper, readable without the
  thesis (see `LATEX.md`, "Appendices"; `D.Warehouses.tex` is the template).
  The reader has the appendix itself, and the thesis only where the appendix
  points to it. Notation (A) and Parameters (B) are reference tables, so
  check them for truth and consistency with the chapters and the code more
  than for flow.

## Check
- Every claim against `slap-mapd-coupling` on `main`
  (`src/slap_mapd_coupling/`, configs in `configs/`). From 2026-11-18 the
  code decides where text and code differ. Do NOT edit the code repo.
- A borrowed idea against the cited paper in `thesis-progress/papers`.
- Numbers of figures, tables, equations and sections against the compiled
  PDF, not the `.tex`.

## Outputs, in `thesis-progress/decisions/active/readability_review/`
1. `<name>_comments.md` with tick boxes, same layout as
   `method_controllers_comments.md`: A (is it true, incl. a "checked and
   matching" list), B (reasons and sources), C (names, plain words,
   symbols), D (reading order, repetition), E (figures), F (what reads
   well), then the three changes that would help the reader most.
   Mark every point you already fixed with "**Fixed ([A108]).**" and no tick
   boxes.
2. `<name>_comments.pdf`: margin notes with the skill's `annotate.py`, only
   your pages. FIRST copy the PDF you annotate into your own scratch folder
   (a Method section: `thesis/main.pdf`; an appendix: its own
   `thesis/Appendices/<X>.pdf`) and annotate the copy, so other agents'
   rebuilds do not change it under you. Look at one page render to check
   placement.

## Fix the small known mistakes yourself
A small known mistake is a sentence, caption, table cell or symbol that
says something the code, the cited paper or an earlier part of the thesis
plainly contradicts, where the fix is local (one to three sentences) and
needs no modelling decision. Examples: a wrong equation number, a wrong
claim about what the code does, a missing citation for an idea the text
already says is borrowed, a typo in a name, a value that the code and
`GAPS.md` both fix while the text says TBD.

NOT small: readability rewrites, moving or cutting paragraphs, new figures,
anything with a choice the author must make, anything that needs a reason
the author has not given, a value that GAPS does not settle. Those go in
the comments file only.

How to fix:
- Edit only the lines of your own section or appendix file, with the Edit
  tool (no sed or scripts on thesis files). If an Edit fails because the
  file changed, Read it again and retry, since other agents edit other
  sections of the same file.
- Tag each changed line `% [A108]`. Do not write in `GAPS.md`.
- Follow the thesis style rules (no dashes, no colons or semicolons joining
  clauses, UK spelling, plain words, one name per idea, no meta-commentary).
- Do NOT run latexmk on `main.tex` (the main session rebuilds it). An
  appendix agent may rebuild its own appendix only:
  `cd thesis/Appendices && latexmk -pdf -interaction=nonstopmode -quiet <X>.tex`
  and must check its log has no errors. Do not run `tools/sync_xrefs.py`.
- Do not commit, push or touch `method_review_queue.md`, `GAPS.md` or other
  agents' files.

## Double check before you report
Re-read every comment and every fix against the source. Check every quoted
phrase, number and label.

## Report back (this is all the main session sees)
1. The most important points, grouped like the comments file, with page and
   phrase. Short.
2. FIXED: one line per fix, `file:line`, old text, new text, and the reason
   (code `file:line`, paper section or thesis label).
3. QUEUE: lines ready to paste into `method_review_queue.md` under
   "Mistakes against the code", "Points that go to the Discussion" and
   "Carry forward", and the open questions line for your file.
4. The paths you wrote.
