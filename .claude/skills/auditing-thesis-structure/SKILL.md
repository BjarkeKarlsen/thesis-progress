---
name: auditing-thesis-structure
description: Evaluates thesis organization and argument flow at document, chapter, section, and paragraph levels. Checks alignment among problem statement, research questions, background, methodology, implementation, experiments, results, discussion, limitations, and conclusion.
compatibility: Requires the ordered thesis structure and works best when research questions and assignment requirements are available.
---

# Thesis Structure Auditor

## Purpose

Evaluate whether the thesis presents a coherent, traceable argument from motivation and problem definition through method, evidence, interpretation, and conclusion.

This skill evaluates organization and reasoning, not merely heading presence.

## Principles

1. A thesis structure should support the research questions.
2. Content belongs where readers need it, not simply where it was written first.
3. Background, method, implementation, results, and discussion serve different purposes.
4. A section can have the correct title but still fail its function.
5. Paragraph quality depends on logical role, evidence, and connection, not a rigid template.
6. Repetition can indicate missing synthesis or misplaced content.
7. Structural recommendations should respect disciplinary and institutional conventions.
8. Do not impose a universal chapter order when the supplied rubric permits alternatives.

## Inputs

- Ordered chapter and section hierarchy.
- Paragraph-level text with locations.
- Research questions or hypotheses.
- Assignment instructions and evaluation criteria.
- Lists of figures, tables, experiments, and results.
- Abstract, introduction, discussion, and conclusion.
- Supervisor or department structure requirements.

## Workflow

### 1. Identify the thesis argument

Extract or infer:

- Motivation.
- Problem statement.
- Research gap.
- Aim.
- Research questions or hypotheses.
- Claimed contributions.
- Methodological approach.
- Evaluation strategy.
- Main results.
- Interpretation.
- Limitations.
- Final answers to research questions.

Mark each item as explicit, implicit, missing, or not assessable.

### 2. Build a traceability map

For each research question, map:

- Introduction or statement location.
- Background concepts needed.
- Method components used to address it.
- Data or experiment supporting it.
- Result locations.
- Discussion locations.
- Conclusion answer.

Report orphan research questions, methods without questions, experiments without analytical purpose, and conclusions without results.

### 3. Evaluate document-level structure

Check whether:

- The abstract represents the completed thesis accurately.
- The introduction establishes context, problem, gap, aim, and contributions.
- Background contains necessary prior knowledge rather than original results.
- Related work synthesizes literature rather than listing papers.
- The problem statement defines the studied system precisely.
- The methodology explains how questions will be answered.
- Implementation detail supports reproducibility without replacing methodological reasoning.
- Experimental design connects metrics and baselines to research questions.
- Results report evidence clearly.
- Discussion interprets evidence and addresses validity.
- Limitations are explicit and meaningful.
- The conclusion answers the research questions without introducing new evidence.

### 4. Evaluate section-level structure

For each section determine:

- Stated or inferable purpose.
- Main claim or function.
- Required context.
- Actual content.
- Relationship to preceding and following sections.
- Whether the title accurately describes the content.
- Whether the section is too fragmented, overloaded, misplaced, or repetitive.

### 5. Evaluate paragraph-level structure

For each substantive paragraph, identify when feasible:

- Primary purpose.
- Main proposition.
- Evidence or explanation.
- Reasoning connection.
- Relationship to the section purpose.
- Transition to adjacent material.

Flag paragraphs that:

- Contain several unrelated purposes.
- Begin without enough context.
- Present evidence without interpretation.
- Make a conclusion without evidence.
- Repeat prior material without synthesis.
- Consist mainly of citations or paper summaries.
- Use transitions that do not reflect the actual logic.

Do not require every paragraph to follow a fixed topic-evidence-conclusion template.

### 6. Evaluate literature synthesis

Check whether related-work and background passages:

- Group sources by concept, method, assumption, or finding.
- Compare rather than list.
- Identify agreements and disagreements.
- Connect prior work to the thesis gap.
- Explain why selected baselines or frameworks matter.
- Distinguish literature facts from the student's interpretation.

### 7. Evaluate repetition and placement

Identify repeated definitions, motivation statements, method descriptions, results, and conclusions. Classify repetition as:

- Necessary reminder.
- Useful summary.
- Redundant duplication.
- Contradictory restatement.
- Evidence that content is in the wrong section.

## Rule Catalogue

### STR001 — Missing problem statement

The thesis lacks a precise description of the problem being solved.

Default severity: Critical.

### STR002 — Research question not operationalized

A research question is stated but no method, metric, or evidence path addresses it.

Default severity: Critical.

### STR003 — Method without research purpose

A substantial method or implementation component is not connected to a research question or contribution.

Default severity: Major.

### STR004 — Experiment without analytical role

An experiment is described without explaining what claim or question it tests.

Default severity: Major.

### STR005 — Result not discussed

An important result is reported but not interpreted.

Default severity: Major.

### STR006 — Conclusion does not answer research question

The conclusion summarizes work but fails to provide an evidenced answer.

Default severity: Critical or Major.

### STR007 — New evidence in conclusion

The conclusion introduces substantive results or arguments not developed earlier.

Default severity: Major.

### STR008 — Background and contribution mixed

Original decisions or results are presented as background, or literature content is presented as the student's contribution.

Default severity: Major.

### STR009 — Paper-by-paper literature list

Related work summarizes sources sequentially without synthesis or connection to the gap.

Default severity: Major.

### STR010 — Section-title mismatch

A section's content does not match its heading or stated purpose.

Default severity: Minor or Major.

### STR011 — Overloaded paragraph

A paragraph contains several independent claims or purposes that should be separated.

Default severity: Minor.

### STR012 — Fragmented structure

Excessive short sections or paragraphs interrupt the argument.

Default severity: Minor or Major.

### STR013 — Redundant repetition

Material is repeated without a new purpose, synthesis, or level of detail.

Default severity: Minor or Major.

### STR014 — Missing transition

The relationship between adjacent sections or paragraphs is unclear where a transition is needed.

Default severity: Minor.

### STR015 — Limitation omitted

A central methodological or empirical limitation is evident but not acknowledged.

Default severity: Major.

### STR016 — Metric-question mismatch

The selected metric does not clearly measure the property asked about in the research question.

Default severity: Critical or Major.

### STR017 — Baseline lacks justification

A comparison baseline is used without explaining why it is appropriate.

Default severity: Major.

### STR018 — Contribution not distinguished

The reader cannot tell what was adopted, implemented, modified, or newly proposed.

Default severity: Critical or Major.

## Output Requirements

Provide:

- Thesis argument map.
- Research-question traceability matrix.
- Document-level findings.
- Section-level findings.
- Selected paragraph-level findings.
- Repetition and placement findings.
- Structural strengths.
- Prioritized restructuring plan.

A traceability matrix should use this form:

| Research question | Method | Evidence | Discussion | Conclusion | Status |
|---|---|---|---|---|---|
| RQ1 | Section and location | Experiment/result | Section and location | Answer location | OK / Needs Adjustment |

Do not fill missing cells with invented content.

## Revision Guidance

Recommend structural actions before sentence rewriting:

- Move a definition before the method that depends on it.
- Merge repeated literature summaries into a comparative synthesis.
- Split method rationale from implementation detail.
- Add a result-to-question bridge at the start of the discussion.
- Reorganize experiments by research question.
- Rewrite the conclusion around explicit answers rather than chapter summaries.
- Add a contribution map distinguishing adopted, adapted, and original elements.

## Constraints

- Do not impose IMRaD mechanically.
- Do not penalize alternative thesis structures that satisfy the rubric.
- Do not infer that a missing heading means the content is missing without checking the body.
- Do not recommend moving material without considering references and definitions that depend on its order.
- Do not turn every paragraph-level observation into a high-severity issue.
