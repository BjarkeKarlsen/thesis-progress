---
name: auditing-thesis-citations
description: Reviews citations and bibliography use across a LaTeX thesis. Detects unresolved citation keys, unclear citation placement, unsupported technical claims, ambiguous citation scope, citation-only sentences, source-type mismatches, and bibliography inconsistencies. Use for academic source and claim traceability checks.
compatibility: Works best with an ordered thesis document model, .bib files, and compilation logs. Full claim-support verification requires access to the cited sources.
---

# Thesis Citation Auditor

## Purpose

Evaluate whether claims are connected clearly and responsibly to sources.

This skill handles bibliography citations such as `\cite`, `\citep`, `\citet`, `\parencite`, `\textcite`, `\autocite`, and project-specific citation macros. It does not handle internal figure, equation, table, or section references; delegate those to `auditing-thesis-references`.

## Principles

1. A citation's location should make its scope clear.
2. Citation placement depends on syntax and attribution; citations are not always required at sentence ends.
3. A nearby citation does not prove that the source supports the claim.
4. Common knowledge and the student's own methods do not automatically require external citations.
5. Technical, empirical, historical, comparative, and borrowed conceptual claims usually require traceability.
6. Source quality and source relevance are different questions.
7. Never accuse the student of plagiarism or fabrication based only on citation patterns.
8. Never invent a missing source.

## Required Inputs

Use as many of these as are available:

- Ordered prose with source locations.
- Citation-command registry.
- Bibliography-key registry.
- Compilation warnings.
- Assignment citation requirements.
- Citation style and backend.
- Full text or metadata of cited sources.
- Project-specific exclusions and accepted conventions.

## Workflow

### 1. Inventory citations

For each citation occurrence, record:

- Citation command.
- Citation keys.
- Optional prenote and postnote.
- File and line.
- Section path.
- Sentence and paragraph context.
- Whether it is narrative or parenthetical.
- Whether the same keys occur repeatedly nearby.

### 2. Validate keys

Check:

- Citation key exists in a bibliography source.
- Key spelling and capitalization are consistent.
- Multiple bibliography files do not contain conflicting duplicate keys.
- Compilation resolved the citation.
- Required bibliography fields are present when this can be checked reliably.
- Cited works appear in the generated bibliography.
- Uncited bibliography entries are intentional or reported as informational findings.

### 3. Identify claim candidates

Flag sentences that appear to contain:

- Technical definitions borrowed from literature.
- Quantitative statements.
- Historical claims.
- Statements about established methods.
- Comparisons between algorithms or systems.
- Claims about performance, scalability, safety, or limitations.
- Descriptions of another paper's method or results.
- Generalizations about research practice.
- Statements using phrases such as “studies show,” “it is known,” or “research demonstrates.”

Do not automatically demand citations for:

- Explicit descriptions of the student's own implementation.
- Directly reported results from the thesis's own experiment.
- Clearly marked research goals or design decisions.
- Logical transitions.
- Widely accepted common knowledge, subject to field context.

### 4. Evaluate placement and scope

Classify each citation pattern.

#### Clear parenthetical support

```latex
Warehouse agents receive local observations \citep{source}.
```

The citation follows the supported clause or sentence.

#### Clear narrative attribution

```latex
\textcite{source} define the problem as ...
```

The citation precedes the proposition because the source is grammatically integrated as the subject.

#### Potentially unclear prefix citation

```latex
\citep{source} Warehouse agents receive local observations.
```

This is not automatically invalid, but it normally has unclear grammatical and evidential scope.

#### Ambiguous multi-claim citation

```latex
Method A is decentralized, scales linearly, and always avoids deadlocks
\citep{source}.
```

Determine whether the citation is intended to support all claims. If source access is unavailable, request manual verification rather than asserting mismatch.

#### Paragraph-final citation

A citation at the end of a paragraph can be ambiguous when the paragraph contains several distinct claims or sources. Evaluate whether its intended coverage is evident.

### 5. Check citation coverage

Find claim candidates that have no plausible supporting citation in the same sentence, adjacent sentence, or clearly scoped paragraph context.

Do not use a fixed character-distance rule as proof. Distance can prioritize review but cannot determine support by itself.

### 6. Check source use

When source content is available, compare the thesis claim with the source at a high level:

- Directly supported.
- Partially supported.
- Overstated.
- Contradicted.
- Source discusses the topic but not the specific claim.
- Not assessable from available source content.

Do not reconstruct or quote copyrighted source text extensively. Use short descriptions and location information.

### 7. Check citation quality patterns

Review:

- Heavy dependence on one source for an entire topic.
- Reviews cited where the thesis attributes an original method.
- Non-primary source used for an exact algorithm definition when the primary paper is available.
- Website or commercial source used for a central scholarly claim without justification.
- Citation clusters without explanation of how the sources differ.
- Repeated citations after every sentence where one clearly scoped citation would suffice.
- Long literature-summary passages with too few source boundaries.
- Inconsistent citation command style.
- Missing page numbers for direct quotations when required.

Source-type concerns should normally be Major, Minor, or Suggestion depending on the rubric and role of the claim. Do not judge a source only from its URL or venue name without enough context.

## Rule Catalogue

### CIT001 — Prefix citation without attribution

A parenthetical citation appears before a claim without being grammatically integrated.

Default severity: Minor or Major.

### CIT002 — Claim without nearby support

A technical or factual claim appears to require a source but no clear supporting citation is present.

Default severity: Major for central claims; Minor for local background claims.

### CIT003 — Ambiguous citation scope

The reader cannot determine which of several clauses or sentences the citation supports.

Default severity: Major.

### CIT004 — Excessive citation distance

A citation is separated from its likely claim by intervening unrelated material.

Default severity: Minor or Major.

### CIT005 — Citation-only sentence or paragraph

A citation command appears without a proposition, attribution, or clear syntactic role.

Default severity: Minor.

### CIT006 — Undefined citation key

A cited key does not resolve in available bibliography data or compilation.

Default severity: Critical when widespread; Major when isolated.

### CIT007 — Unused bibliography entry

A bibliography key is present but never cited.

Default severity: Suggestion unless the rubric forbids uncited entries.

### CIT008 — Source role mismatch

A secondary or tertiary source is used while the prose attributes an original method, definition, or result.

Default severity: Minor or Major.

### CIT009 — Claim support requires verification

The citation is present, but source content must be inspected before support can be confirmed.

Default severity: Suggestion or Major depending on claim importance. Status may be Not Assessable.

### CIT010 — Citation style inconsistency

Narrative, parenthetical, punctuation, page-number, or command conventions are inconsistent.

Default severity: Minor.

### CIT011 — Unsupported quotation

Quoted wording lacks a resolvable citation or required locator.

Default severity: Major.

### CIT012 — Citation cluster lacks synthesis

Several citations are grouped without explaining agreement, disagreement, roles, or distinctions where synthesis is expected.

Default severity: Minor or Major.

### CIT013 — Overcitation

The same source is cited repetitively where scope is already unambiguous, harming readability.

Default severity: Suggestion or Minor.

### CIT014 — Attribution drift

A paragraph begins by attributing a source, then transitions into uncited claims whose authorship is unclear.

Default severity: Major.

### CIT015 — Self-result presented as literature fact

A result from the current thesis is phrased as established external knowledge or vice versa.

Default severity: Major.

## Output Requirements

Group findings by severity and thesis order. For every issue provide:

- Rule ID.
- Status.
- Severity.
- Confidence.
- File and line.
- Section.
- Short excerpt.
- Explanation of citation scope or coverage.
- Specific recommended revision strategy.
- Whether source inspection is required.

Also report strengths such as:

- Clear narrative attribution.
- Appropriate source boundaries.
- Consistent citation style.
- Good separation of literature claims from the student's contributions.

## Revision Guidance

Prefer recommendations such as:

- Move the citation immediately after the supported clause.
- Use `\textcite{key}` when the source is the grammatical subject.
- Split a sentence containing independently sourced claims.
- Add a sentence explaining how a citation cluster relates to the argument.
- Cite the original method paper for the method description.
- Mark the statement as the current thesis's result instead of an external fact.

Do not automatically move a citation when doing so could alter its scope. Mark such fixes as Review Required.

## Constraints

- Do not demand one citation per sentence mechanically.
- Do not claim a source supports a statement without inspecting it.
- Do not mark all citation-before-text patterns as wrong.
- Do not infer misconduct from missing citations.
- Do not invent page numbers or bibliography entries.
- Do not conflate bibliography citations with `\ref`, `\eqref`, `\cref`, or `\Cref`.

## In This Workspace

Most cited papers are available as PDFs in `thesis-progress/papers/` (file names are mostly arXiv IDs or publisher IDs). Use them for CIT009 checks: read the relevant passage before marking a claim as supported, partly supported or overstated, and say which file and section you checked. A source not in the folder stays Not Assessable.
