---
name: validating-latex-theses
description: Audits complete multi-file LaTeX thesis projects for compilation problems, citation and cross-reference issues, undefined terminology, inconsistent notation, structural weaknesses, rubric alignment, and writing-style problems. Use when reviewing a thesis repository, dissertation draft, academic LaTeX project, or a collection of connected .tex files.
compatibility: Requires access to the thesis project files. Python 3, latexmk, BibTeX or Biber, and ChkTeX are recommended for complete validation.
---

# LaTeX Thesis Validator

## Purpose

Audit an entire LaTeX thesis as one connected academic document.

Do not review included files as unrelated documents when their meaning depends on the complete thesis order. Distinguish deterministic LaTeX errors from semantic academic-writing concerns. Preserve traceability from every finding to its source file and line.

Do not modify thesis files unless the user explicitly requests automatic corrections. Default to analysis and recommended actions.

## Core Principles

1. Resolve the real document order before evaluating prose.
2. Run deterministic checks before semantic checks.
3. Distinguish bibliography citations from internal cross-references.
4. Distinguish confirmed errors from heuristic concerns.
5. Attach a location, severity, and confidence to every finding.
6. Never invent source support, bibliography entries, definitions, or requirements.
7. Evaluate observable writing characteristics instead of claiming to determine authorship.
8. Preserve the student's terminology and intended technical meaning.
9. Prioritize correctness, traceability, and argument quality over superficial wording.
10. Treat the thesis as a connected argument rather than a collection of sentences.

## Expected Inputs

Obtain or infer the following:

- Project root directory.
- Root LaTeX document.
- Assignment instructions or formal demands.
- Evaluation criteria or grading rubric.
- University, department, or course requirements.
- Bibliography system: BibTeX, Biber, biblatex, natbib, or another system.
- Desired scope: full thesis, selected chapters, or changed files.
- Desired mode: report only, suggested patches, or approved automatic fixes.

The demands and criteria may be omitted. If they are unavailable, perform technical, citation, reference, definition, structure, and style reviews without pretending to provide rubric-alignment scores.

## Validation Modes

### Full validation

Use for final or milestone reviews. Traverse the complete project, compile it, run all specialist audits, and produce a consolidated report.

### Incremental validation

Use for changed files or a Git diff. Resolve enough surrounding context to understand the changes, then report new or affected findings separately from existing findings.

### Focused validation

Use when the user asks about one area, such as citations, equations, definitions, or chapter structure. Still load enough project context to avoid isolated and misleading judgments.

## Workflow

### Phase 1: Discover the project

1. Search for `.tex`, `.bib`, `.sty`, `.cls`, image, glossary, acronym, and configuration files.
2. Locate candidate root documents containing `\documentclass`.
3. If multiple candidates exist, rank them using include relationships, compilation configuration, and directory conventions.
4. Read project configuration such as `.latexmkrc`, `latexmkrc`, `arara.yaml`, editor settings, and build scripts when present.
5. Identify the bibliography backend and commands.
6. Follow `\input`, `\include`, `\subfile`, and known custom inclusion commands recursively.
7. Normalize paths without losing the original path spelling used in source files.
8. Detect missing, duplicate, conditional, and cyclic includes.
9. Determine the effective thesis reading order.
10. Preserve a mapping from extracted content to source file, line range, section path, and include chain.

Do not assume alphabetical file order equals document order.

### Phase 2: Run deterministic validation

When tools are available:

1. Compile the root document with the project's configured build command or `latexmk`.
2. Run enough compilation passes to resolve references and bibliography data.
3. Record the exit code, errors, warnings, overfull boxes, underfull boxes, rerun requests, and missing resources.
4. Run ChkTeX or the configured LaTeX linter.
5. Extract every citation command and citation key.
6. Extract every bibliography entry key.
7. Extract all labels and internal references.
8. Find missing and duplicate identifiers.
9. Detect missing graphics, listings, data files, glossary entries, and included files.
10. Detect hard-coded object numbers where semantic references are expected.
11. Detect malformed commands and unbalanced environments when reliably possible.
12. Record tool versions and unavailable checks.

A compilation failure is a blocker. Do not hide it behind a high semantic score.

### Phase 3: Build a document model

Construct a structured representation containing:

- Chapter and section hierarchy.
- Ordered paragraph list.
- File and line provenance.
- Include graph.
- Figure, table, algorithm, listing, theorem, and equation registry.
- Citation registry.
- Bibliography registry.
- Label and cross-reference registry.
- Acronym registry.
- Definition and terminology registry.
- Mathematical notation registry.
- Research-question registry.
- Claim and evidence candidates.
- Requirement-to-location map.

Exclude or specially mark:

- Comments.
- Generated files.
- Verbatim environments.
- Source-code listings.
- Bibliography output.
- Package implementation code.
- Frontmatter that is not part of the assessed prose.
- Appendices when a criterion explicitly excludes them.

Do not discard captions, footnotes, table cells, or theorem statements; they can contain definitions, claims, citations, and references.

### Phase 4: Delegate specialist audits

Invoke the available specialist skills:

- `auditing-thesis-citations`.
- `auditing-thesis-references`.
- `auditing-thesis-definitions`.
- `auditing-thesis-structure`.
- `reviewing-thesis-style`.
- `evaluating-thesis-rubric` when demands or criteria are provided.

Pass each specialist the document model, relevant files, deterministic findings, and project-specific conventions.

### Phase 5: Consolidate findings

1. Normalize every finding to the common schema.
2. Merge duplicates referring to the same underlying issue.
3. Preserve the strongest supporting evidence.
4. Resolve severity disagreements conservatively.
5. Separate confirmed findings from contextual suggestions.
6. Group repeated local symptoms under one systemic finding when appropriate.
7. Keep independent issues separate even when they occur in the same sentence.
8. Sort first by severity, then by thesis order.
9. Identify quick fixes, manual revisions, and supervisor decisions.
10. Identify checks that could not be completed.

## Bundled Scripts

Phases 1 to 3 and 5 are deterministic. Run the scripts in `scripts/` for them rather than extracting facts by reading files, and read their JSON output instead of re-deriving it. They need only Python 3 (the standard library); compilation also needs `latexmk`, and ChkTeX is used when installed.

Write every output into a work directory outside the thesis project, for example `$WORK=$(mktemp -d)`, never into the thesis folder itself.

```bash
S=<this skill's directory>/scripts
python3 $S/discover_project.py <project_root> --out $WORK/discovery.json
python3 $S/compile_project.py $WORK/discovery.json --outdir $WORK/build --out $WORK/compile.json
python3 $S/collect_identifiers.py $WORK/discovery.json --out $WORK/identifiers.json
python3 $S/extract_structure.py $WORK/discovery.json --out $WORK/structure.json
# ... specialist audits write $WORK/<skill>.json in references/finding-schema.md ...
python3 $S/aggregate_findings.py --discovery $WORK/discovery.json --compile $WORK/compile.json \
    --identifiers $WORK/identifiers.json --structure $WORK/structure.json \
    --findings $WORK/auditing-thesis-*.json $WORK/reviewing-thesis-style.json \
    --out-json $WORK/findings.json --out-md $WORK/report.md
```

- `discover_project.py`: root document, reading order with include chains, missing, cyclic and duplicate includes, unreached `.tex` files, bibliography backend, package options, and user macros that generate labels or graphics (such as a figure macro whose fourth argument becomes `fig:#4`). Pass `--root` when the ranking picks the wrong root.
- `compile_project.py`: builds into its own output directory, so an editor that runs `latexmk` in the project folder is never disturbed, and waits for a running TeX build first. Reports status, errors, undefined references and citations, missing files, over- and underfull boxes with file and line (attribution parsed from the log, best effort), bibliography-tool problems, ChkTeX warnings and tool versions.
- `collect_identifiers.py`: citations, bibliography entries, labels (including macro-generated ones), references with forward-reference and sentence-start flags, graphics, hard-coded object numbers. Cross-checks undefined, unused, duplicate and case-mismatched keys and missing graphics.
- `extract_structure.py`: section hierarchy in true reading order, paragraphs with section paths, numbered objects with captions, research questions, acronym first uses, definition-phrase candidates. This is the document model of Phase 3.
- `aggregate_findings.py`: turns the deterministic results into findings (rule IDs in `references/finding-schema.md`), validates and merges the specialists' findings, removes duplicates, sorts by severity and reading order, and writes JSON and Markdown. It computes no scores. Scores are written by this skill from the report.
- `tests/`: `python3 -m unittest discover -s tests -v`, run from `scripts/`.

Heuristic candidates from the scripts (hard-coded numbers, acronyms used before expansion, unreferenced figures) carry Medium or Low confidence and must be reviewed in context before they count as confirmed findings.

## Using This Suite in This Workspace

This suite lives in `thesis-progress/.claude/skills/`, with links from the workspace root. When it validates the thesis in this workspace:

- **Project.** The thesis is `thesis/` (Overleaf-synced), root `thesis/main.tex`, chapters included with `\subfile`, bibliography biblatex with biber. Never write into `thesis/`, and never run a build there: the author's editor runs its own `latexmk` and two builds at once corrupt the `.aux` files. `compile_project.py` avoids both.
- **Deliberate decisions.** Model changes are tagged `% [Axx]` (and older `[Gxx]`, `[Kxx]`, `[Mxx]`) in the chapters, with their reasons in `thesis-progress/temp/GAPS.md` and `GAPS.tex`. Before reporting something tagged as a weakness, read its entry. A documented, reasoned choice is an `Accepted Exception` unless the finding shows the reasoning itself is wrong. Parameters marked TBD in the Method tables are genuinely undecided, not omissions.
- **Style rules.** The author's own writing rules are in the "Thesis writing style" section of the workspace-root `CLAUDE.md` (no dashes in prose, no colons or semicolons joining clauses, words before equations, banned words, one idea per paragraph, UK spelling, and others). Treat them as project requirements for `reviewing-thesis-style`, not as generic preferences, and cite the rule a finding breaks.
- **Captions.** Caption rules are in `AGENTS.md` and, in full, in `LATEX.md` under "Figure captions" (about 25 words, under 45, under 25 for `\mywrapfig`).
- **Notation.** `thesis/Chapters/2.Notation.tex` (`tab:notation`) decides which letter means what. Known clashes and agreed renames are in `notation_renames.md`. Use both in `auditing-thesis-definitions`.
- **Rubric.** No assessment criteria are stored in the workspace. Ask the user for the demands and criteria. Without them, mark rubric scores Not Assessable.
- **Report.** Write the report to the work directory and give the user the path. Do not change any thesis file unless the user asks for fixes, and then follow `CLAUDE.md` ("Discuss before rewriting").

## Severity Levels

### Blocker

Prevents compilation, prevents the thesis from being read reliably, or prevents meaningful assessment.

Examples:

- Root document cannot compile.
- Required chapter is missing.
- Bibliography cannot be generated.
- Include cycle prevents project traversal.

### Critical

Undermines technical correctness, academic traceability, or the central thesis argument.

Examples:

- Research question is not addressed by the method or conclusion.
- Central result is unsupported or contradicted.
- Core notation changes meaning without explanation.
- Extensive citation keys are unresolved.

### Major

Materially reduces clarity, reproducibility, or academic quality but does not invalidate the complete thesis.

Examples:

- Important technical claims lack citations.
- Definitions are introduced after sustained use.
- Results and discussion are systematically mixed against the rubric.
- Central figures are not introduced or interpreted.

### Minor

A localized correctness, consistency, presentation, or clarity issue.

Examples:

- One acronym is not expanded.
- One figure reference is hard-coded.
- A paragraph has an unclear transition.

### Suggestion

An optional improvement that is not a violation or demonstrated weakness.

Examples:

- Consider adding a roadmap sentence.
- Consider splitting a long paragraph.
- Consider moving supplementary detail to an appendix.

## Confidence Levels

### High

The issue follows directly from compilation output, explicit project structure, an exact rubric requirement, or unambiguous local evidence.

### Medium

The issue is strongly indicated but depends on academic context, source interpretation, or an inferred relationship.

### Low

The issue is exploratory, subjective, or depends on missing information. Low-confidence findings must not be presented as confirmed errors.

## Common Finding Schema

Every finding must include:

- `id`: Stable rule identifier.
- `category`: Technical, citation, cross-reference, definition, notation, structure, rubric, or style.
- `severity`: Blocker, Critical, Major, Minor, or Suggestion.
- `confidence`: High, Medium, or Low.
- `status`: OK, Needs Adjustment, Not Assessable, or Accepted Exception.
- `location`: File and line or line range.
- `section`: Human-readable section path.
- `excerpt`: Short relevant excerpt, not an entire paragraph unless necessary.
- `explanation`: What is wrong or uncertain and why it matters.
- `recommended_action`: Specific next action.
- `automatic_fix`: Yes, No, or Review Required.
- `related_locations`: Optional connected occurrences.
- `criterion`: Optional rubric criterion identifier.

Example:

```text
ID: CIT003
Category: Citation scope
Severity: Major
Confidence: High
Status: Needs Adjustment
Location: sections/background.tex:84-85
Section: Background > Multi-Agent Path Finding
Excerpt: "\citep{cramp2023} Warehouse agents operate..."
Explanation: The citation precedes multiple claims without explicit attribution,
so the reader cannot determine its intended scope.
Recommended action: Move the citation after the supported claim or use an
author-leading construction such as `\textcite{cramp2023}`.
Automatic fix: Review Required
```

## Scoring

Provide separate whole-number scores from 1 to 10 for:

- Technical correctness.
- Citations and traceability.
- Internal references and document navigation.
- Definitions and notation.
- Structure and argumentation.
- Writing clarity.
- Rubric fulfillment, when assessable.

Interpret scores as follows:

- 1–2: Missing, unusable, or fundamentally incorrect.
- 3–4: Major deficiencies with limited fulfillment.
- 5–6: Partly adequate but substantial revision is needed.
- 7–8: Good fulfillment with identifiable adjustments.
- 9: Excellent with only minor issues.
- 10: Fully meets the stated expectations with no material issue found.

Do not calculate the overall score as a blind arithmetic average. Blockers and critical problems constrain the final score. Explain any weighting or score cap.

## Required Output

### 1. Validation Scope

State which files, chapters, requirements, tools, and checks were included or unavailable.

### 2. Critical Parts Identified

List the central technical, academic, and rubric-dependent requirements.

### 3. Compilation and LaTeX

Report build status, blockers, warnings, and deterministic findings.

### 4. Citations

Report source-citation placement, coverage, scope, and bibliography problems.

### 5. Internal References

Report labels, references, captions, and object-introduction problems.

### 6. Definitions and Notation

Report first-use, consistency, conflict, and notation-table findings.

### 7. Document Structure

Report document-, section-, and paragraph-level findings.

### 8. Evaluation of Each Critical Part

For each critical part, provide:

- Status: OK, Needs Adjustment, or Not Assessable.
- Evidence locations.
- Short reasoning.
- Recommended action when adjustment is needed.

### 9. Criteria Scoring

Give each supplied criterion a 1–10 score, short justification, and confidence. Mark unavailable criteria as Not Assessable instead of inventing a score.

### 10. Writing Style and Authorial Revision

Describe observable style patterns and concrete ways the student can restore their own reasoning, examples, decisions, and technical voice.

### 11. Prioritized Adjustments

Separate:

- Must fix before submission.
- Should fix.
- Optional improvements.
- Supervisor or policy decisions.

### 12. Strengths

Identify evidenced strengths without generic praise.

### 13. Weaknesses

Identify the main limitations without repeating every local finding.

### 14. Final Overall Score

Give a whole-number score from 1 to 10 only when enough of the thesis and rubric were available. State any score cap caused by blockers or critical issues.

## Constraints

- Never invent bibliography entries.
- Never invent source support.
- Never invent assignment requirements.
- Never silently rewrite thesis files.
- Never classify text as human-written or AI-written.
- Never present an AI-detection percentage.
- Never treat a heuristic warning as confirmed without contextual review.
- Never penalize a valid forward reference merely because its target appears later.
- Never report a problem without a location when location information is available.
- Never replace domain-specific terminology solely to make prose sound simpler.
- Never use a final score to hide critical findings.
