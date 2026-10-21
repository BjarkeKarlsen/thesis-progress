# Appendix plan

**2026-10-21. Third round agreed**, 13 appendices down to 10 and included at the end of
`main.tex`. See `appendix_split_handoff.md`.

**Status 2026-10-20. Structure built, first moves done, uncommitted in `thesis/`.**
The limit is 60 pages for the main text. The bibliography and appendices do not
count. The appendices are a separate document (`thesis/appendix.tex`), so labels
are shared through generated files (`LATEX.md`, "Appendix document").

Files. One per appendix in `thesis/Chapters/Appendix/` (`A.Notation.tex` to
`H.Parameters.tex`). The order of the `\subfile` lines in `appendix.tex` sets
the letters. A supporting experiment gets its own appendix, with its setup,
result and conclusion. The main experiments (RQ1 to RQ4) stay in the
Experiments chapter.

Checked 2026-10-20. All 16 moved blocks are in their appendix files word for
word, against the text as it stood just before the move.

Rule for a move. The main text keeps the idea in words and the result. The
appendix keeps the full derivation, details and extra figures. Labels stay the
same, and the main text marks the spot with `% [APP]`.

## Page count

| | before | after |
|---|---|---|
| main PDF, with bibliography | 65 (incl. 6 pages of notation) | 53 |
| Problem Formulation | pages 6 to 33 | pages 6 to 30 |
| Method and Implementation | pages 39 to 51 | pages 35 to 46 |
| appendix PDF | | 15 |

The results are still to be written, so expect the main text to grow by 6 to 8 pages.

## Appendices

| | Appendix | Moved from | Status |
|---|---|---|---|
| A | Notation (`app:notation`) | `main.tex` | done |
| B | Well-formed instances (`app:wellformed`) | `sec:pf:agents`, with `fig:wellformed` | done |
| C | The warehouse instances (`app:instances`) | starting stock from `sec:impl:instances` | done. Figures of the 8, 16, 32 and 64-agent warehouses to add |
| D | The load sweep (`app:sweep`) | new | to write once the Token Passing sweep is read |
| E | The learning problem in full (`app:game`) | `sec:pf:game`, `tab:posg`, the action list, assignment and conflict resolution in P | done |
| F | Measures in full (`app:measures`) | `sec:pf:measures`, order completion, CRAMP comparison, put-away distance, runtime, decision problem | done |
| G | Storage rule details (`app:storage`) | `sec:pf:storage`, the storage matrix example, arrivals, tie-breaking | done |
| H | Parameter tables (`app:params`) | the five `tab:*params` of Method and Implementation | done |

## Second round, 2026-10-20

The 60 pages count from the Introduction. Moved in this round, all checked
word for word (29 blocks in total across both rounds).

| | Appendix | Moved from |
|---|---|---|
| F | worked example, blocked time against the edge estimate | `sec:pf:measures` |
| I | Logging and correctness checks (`app:repro`) | `sec:impl:logging`, `sec:impl:validation` |
| J | Pilot runs (`app:pilots`) | `sec:method:storage`, `sec:impl:instances`, `sec:impl:logging` |
| K | Controllers and observations in detail (`app:controllers`) | `sec:pf:controllers`, `tab:observationexample` |
| L | Deadlines and re-tasking (`app:scope`) | `sec:pf:scope` |

Also. Related Work's Transformer subsection became two sentences in Future
work, the doubled SLAP papers were removed from Background (`[A48]`), and a
forced page break before the Method was removed.

Main text now pages 4 to 49 (46 pages). With results, discussion,
conclusion and future work written, about 55 to 56.

## Still to check

- Read the bridging sentences left in the main text (search `% [APP]`).
- Read the moved text in the appendix. It was moved as it was, so a few phrases
  still assume the main text around it (for example "the fleet size fixed above").
- Further candidates if the results push past 60 pages. "What a decentralised
  agent sees" (the communication graph), "Who decides", and the pilot numbers in
  `sec:method:storage` and `sec:impl:instances`.
