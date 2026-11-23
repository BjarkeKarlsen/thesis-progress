# Brief for the fix subagents (2026-11-20, second round)

The author said: "go through and fix the worst mistakes without me". So
these agents EDIT THE THESIS. They fix places where the text says something
the code, the run configs or the result data contradict. From 2026-11-18
the code decides where text and code differ.

## Do not decide for the author
Leave alone, and only list, anything that is a choice and not a fact:
which training setup is the main result, which checkpoint counts, renaming
(zone or section, w, message, h(k)), reporting the order gain beside the
pick gain, redrawing figures, merging or rerunning results, adding new
experiments, readability rewrites beyond what the fix needs.

## How
- Read `/home/bjarkek/Documents/thesis/CLAUDE.md` and `AGENTS.md` first. The
  thesis prose rules apply to every sentence you write (plain words, short
  sentences, no dashes, no colons or semicolons joining clauses, UK
  spelling, one name per idea, say why before the symbol, no
  meta-commentary, no forward references in the Problem Formulation).
- The comments files in
  `thesis-progress/decisions/active/readability_review/` hold the evidence
  for every point (code `file:line`, data paths). Re-check each fact in the
  code (`slap-mapd-coupling` on `main`, configs in `configs/fleet_*`) before
  writing it. Do not edit the code repo.
- Edit only with the Edit tool. Other agents edit other paragraphs of the
  same files at the same time. If an Edit fails because the file changed,
  Read it again and retry. Touch only the paragraphs of your topic.
- Tag every changed line `% [A109]`.
- Do NOT run latexmk, `tools/sync_xrefs.py`, git commit or push. The main
  session builds and checks everything at the end.
- Do NOT write in `GAPS.md` or `method_review_queue.md`. In each comments
  file you fix a point of, add "**Fixed ([A109]).**" under that point.
- Before you report, re-read every edited paragraph in the `.tex` and check
  labels you reference exist (`grep -rn 'label{...}' thesis/`).

## Report back
1. FIXED: one line per change, `file:line`, what it now says, the evidence.
2. GAPS: a short paragraph for the [A109] entry of your topic (what changed
   and why, model change or not).
3. LEFT: what you did not fix and why (author's choice).
