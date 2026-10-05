---
name: auditing-thesis-references
description: Audits LaTeX labels and internal references for equations, figures, tables, sections, algorithms, listings, appendices, and theorem-like environments. Detects undefined or duplicate labels, hard-coded numbers, unclear object references, missing introductions, and inconsistent naming conventions.
compatibility: Works best with compilation logs, ordered source files, and a registry of numbered LaTeX objects.
---

# Thesis Internal Reference Auditor

## Purpose

Ensure that numbered and named objects can be located, understood, and maintained reliably.

This skill handles internal references such as `\ref`, `\pageref`, `\eqref`, `\autoref`, `\cref`, `\Cref`, ranges, and custom reference macros. It does not evaluate external bibliography citations.

## Principles

1. Use semantic references instead of hard-coded numbers.
2. A forward reference is valid when it helps navigation.
3. Every referenced object must exist and be uniquely labeled.
4. A reference should make the object type clear in prose.
5. Figures, tables, and equations should normally be introduced and interpreted, not merely inserted.
6. Label naming conventions improve maintenance but are secondary to correctness.
7. Compilation output has priority over heuristic pattern matching.

## Inputs

- Label registry.
- Reference registry.
- Object registry.
- Compilation warnings.
- Ordered thesis content.
- Project reference conventions.
- Loaded packages such as `hyperref`, `cleveref`, and `varioref`.

## Workflow

### 1. Inventory labels

For every `\label`, record:

- Key.
- File and line.
- Section path.
- Closest numbered object.
- Object type.
- Whether label placement can bind to the intended counter.

Check labels in:

- Sections and chapters.
- Equations and aligned equations.
- Figures and subfigures.
- Tables.
- Algorithms.
- Listings.
- Theorems, definitions, lemmas, and propositions.
- Appendices.

### 2. Inventory references

For every internal reference, record:

- Command.
- Keys.
- File and line.
- Sentence context.
- Expected object type.
- Whether it is a forward or backward reference.

### 3. Validate resolution

Detect:

- Undefined labels.
- Duplicate labels.
- Empty labels.
- Labels containing suspicious whitespace or malformed content.
- References that resolve to an unexpected object type.
- Labels placed before or after the wrong counter-changing command.
- Stale labels from deleted objects.

### 4. Check reference semantics

Review whether:

- Equation references use `\eqref` or semantic commands consistently.
- `\cref` and `\Cref` capitalization matches sentence position.
- Multiple objects use a range or list command correctly.
- The prose identifies the object type clearly.
- References avoid ambiguous phrases such as “the figure below” when numbering is available.
- Directional words such as “above” and “below” remain valid under layout changes.
- Page references are useful rather than redundant.

### 5. Detect hard-coded references

Search prose for patterns such as:

- Figure 3.
- Table 2.
- Equation 10.
- Section 4.2.
- Chapter 5.
- Appendix A.
- Algorithm 1.

Exclude cases that intentionally refer to external publications, source numbering, version numbers, or data labels. Recommend semantic LaTeX references when the number belongs to the current thesis.

### 6. Check object integration

For each figure, table, algorithm, listing, and important equation, determine whether it is:

- Introduced before or near its appearance.
- Referenced from the prose.
- Given a meaningful caption when required.
- Interpreted rather than left unexplained.
- Placed in a section where it supports the argument.

An unreferenced decorative figure is not automatically an error, but central analytical objects should be integrated into the prose.

## Rule Catalogue

### REF001 — Undefined label

A reference key has no matching label.

Default severity: Major; Critical when widespread or central.

### REF002 — Duplicate label

The same label key is defined more than once.

Default severity: Major.

### REF003 — Hard-coded internal number

A current-thesis figure, table, equation, section, or similar object is referred to by typed number.

Default severity: Minor.

### REF004 — Unclear object type

The reference output or surrounding prose does not tell the reader whether the target is an equation, figure, table, or section.

Default severity: Minor.

### REF005 — Incorrect capitalization command

Lowercase `\cref` is used at a sentence start, or uppercase `\Cref` is used where project style requires lowercase.

Default severity: Minor.

### REF006 — Object never introduced

A figure, table, or equation appears without a prose introduction where one is academically needed.

Default severity: Minor or Major.

### REF007 — Object never interpreted

A central result object is shown but its implication is not discussed.

Default severity: Major.

### REF008 — Referenced object type mismatch

Prose calls the target a figure while the label resolves to a table, equation, or another type.

Default severity: Major.

### REF009 — Fragile directional reference

“The figure below,” “the equation above,” or similar wording is used where float movement can make the direction false.

Default severity: Minor.

### REF010 — Inconsistent label convention

Labels use conflicting prefixes or naming patterns.

Default severity: Suggestion or Minor.

### REF011 — Misbound label

A label appears in a location where it may capture the wrong counter.

Default severity: Major.

### REF012 — Unreferenced central object

An important numbered object is never mentioned in the prose.

Default severity: Minor or Major.

### REF013 — Redundant manual object name

Prose combines a manual object name with a reference command that already emits the type, producing wording such as “Equation Equation 10.”

Default severity: Minor.

### REF014 — Ambiguous multi-reference

Several targets are cited in a way that obscures which proposition belongs to which object.

Default severity: Minor.

## Recommended Conventions

When `cleveref` is configured:

- Use `\Cref{eq:coupling}` at the start of a sentence.
- Use `\cref{eq:coupling}` mid-sentence.
- Use `\cref{fig:a,fig:b}` for multiple objects.
- Use consistent prefixes such as `ch:`, `sec:`, `subsec:`, `fig:`, `tab:`, `eq:`, `alg:`, and `lst:`.

Do not force these conventions if the project has another coherent standard.

## Output Requirements

For each finding include:

- Rule ID.
- Severity and confidence.
- File and line.
- Section.
- Reference command and key.
- Resolved target when available.
- Explanation.
- Recommended action.
- Automatic-fix status.

Also report:

- Number of labels.
- Number of references.
- Undefined-label count.
- Duplicate-label count.
- Unreferenced numbered-object count.
- Hard-coded internal-number candidates.

## Constraints

- Do not call a forward reference an error solely because the target occurs later.
- Do not replace `\eqref` with `\Cref` unless that matches the project's style.
- Do not change label keys without updating all references.
- Do not assume every equation requires a label or prose reference.
- Do not confuse citations with cross-references.
