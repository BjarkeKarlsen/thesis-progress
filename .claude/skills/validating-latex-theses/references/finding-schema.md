# Common Finding Schema

All validator skills should emit findings that can be normalized to this structure.

```json
{
  "id": "CIT003",
  "category": "citation-scope",
  "severity": "Major",
  "confidence": "High",
  "status": "Needs Adjustment",
  "location": {
    "file": "sections/background.tex",
    "start_line": 84,
    "end_line": 85,
    "section": "Background > Multi-Agent Path Finding",
    "include_chain": ["main.tex", "sections/background.tex"]
  },
  "excerpt": "\\citep{cramp2023} Warehouse agents operate...",
  "explanation": "The citation precedes multiple claims without explicit attribution, making its scope unclear.",
  "recommended_action": "Move the citation after the supported claim or use an author-leading citation command.",
  "automatic_fix": "Review Required",
  "related_locations": [],
  "criterion": null,
  "source_skill": "auditing-thesis-citations"
}
```

## Required Fields

- `id`.
- `category`.
- `severity`.
- `confidence`.
- `status`.
- `location`.
- `excerpt`.
- `explanation`.
- `recommended_action`.
- `automatic_fix`.
- `source_skill`.

## Allowed Severity Values

- Blocker.
- Critical.
- Major.
- Minor.
- Suggestion.

## Allowed Confidence Values

- High.
- Medium.
- Low.

## Allowed Status Values

- OK.
- Needs Adjustment.
- Not Assessable.
- Accepted Exception.

## Allowed Automatic-Fix Values

- Yes.
- No.
- Review Required.

## Deduplication Key

Use a combination of:

- Underlying issue category.
- Primary location.
- Target identifier, term, criterion, or claim.
- Overlapping line range.

Do not merge findings only because they occur in the same paragraph.

## Optional Fields

- `target`: The identifier, term, key or claim the finding is about. The aggregator uses it, before the excerpt, to decide whether two findings describe the same issue.
- `section`: Human-readable section path, when known.

## Location Forms

`location` may be the object above or a string `file:line` or `file:start-end`. The aggregator normalises both.

## Deterministic Rule IDs

`scripts/aggregate_findings.py` emits these from the script outputs, alongside the catalogue IDs of the specialist skills.

| ID | Meaning | Default severity |
|---|---|---|
| TEX001 | Root document does not compile to a PDF | Blocker |
| TEX002 | LaTeX error in the log | Major (Blocker if no PDF) |
| TEX003 | Overfull box above the threshold, or a group of small ones | Minor / Suggestion |
| TEX004 | Underfull boxes, grouped | Suggestion |
| TEX005 | Other LaTeX or package warning, grouped by message | Suggestion |
| TEX006 | ChkTeX warning, grouped by number | Suggestion, Low confidence |
| TEX007 | Included file not found | Critical |
| TEX008 | Include cycle | Blocker |
| TEX009 | File included more than once | Minor |
| TEX010 | Missing graphic or other required file | Major |
| TEX011 | Bibliography tool (biber/BibTeX) reported a problem | Major |
| TEX012 | Final pass still requests a rerun | Minor |
| BIB001 | Bibliography key defined more than once | Major |
| BIB002 | Citation key differs from an entry only in case | Major |
| CIT006 | Undefined citation key (from the sources and the build log) | Major, Critical when five or more |
| CIT007 | Uncited bibliography entries, grouped | Suggestion |
| REF001 | Undefined label (from the sources and the build log) | Major, Critical when five or more |
| REF002 | Duplicate label | Major |
| REF003 | Hard-coded object number (candidate) | Minor, Medium confidence; Suggestion, Low, when next to a citation |
| REF005 | `\cref` at a sentence start (only without cleveref's `capitalize`) | Minor |
| REF011 | Empty or whitespace-containing label | Minor |
| REF012 | Figure, table, algorithm or listing never referenced (candidate) | Minor, Medium confidence |
| DEF002 | Acronym used before its expansion (candidate) | Minor, Medium or Low confidence |

Candidates are pattern matches. Review each in context before treating it as confirmed. `--no-deterministic-heuristics` drops them from the report.
