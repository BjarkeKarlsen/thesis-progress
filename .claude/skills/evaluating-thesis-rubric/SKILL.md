---
name: evaluating-thesis-rubric
description: Evaluates a thesis or assignment against supplied demands and grading criteria. Identifies critical requirements, maps evidence to each criterion, marks fulfillment status, scores assessable criteria from 1 to 10, and reports strengths, weaknesses, and prioritized adjustments.
compatibility: Requires assignment demands, evaluation criteria, and assignment text or a structured thesis model. Missing components must be requested or marked Not Assessable.
---

# Thesis Rubric Evaluator

## Purpose

Evaluate an assignment against the requirements actually supplied by the user, institution, course, or supervisor.

This skill must not replace explicit requirements with generic academic preferences. It uses findings from the technical and semantic thesis audits as evidence, but it evaluates only criteria that can be mapped responsibly.

## Required Components

Read and distinguish:

### A. Assignment instructions or demands

These state what the student must produce, include, demonstrate, or avoid.

### B. Evaluation criteria

These state how quality or fulfillment is judged.

### C. Student assignment text

This is the work being evaluated. For a LaTeX project, use the compiled reading order and preserve file/line locations.

If one or more components are missing:

- State what is missing.
- Continue only with the assessable components.
- Use `Not Assessable` instead of fabricating a judgment.

## Principles

1. Identify critical requirements before scoring.
2. Separate presence from quality.
3. Use evidence locations for every substantive judgment.
4. Treat mandatory demands differently from optional guidance.
5. Do not give a high score when a central mandatory requirement is absent.
6. Do not let grammar alone dominate a technically focused rubric.
7. Do not reward length unless length is a requirement or contributes to quality.
8. Use whole-number scores only.
9. Explain uncertainty.
10. Distinguish thesis problems from missing evaluator information.

## Workflow

### 1. Parse the demands

Convert the instructions into atomic requirements. For each requirement record:

- Requirement ID.
- Exact or concise requirement wording.
- Mandatory, recommended, optional, or ambiguous status.
- Expected evidence.
- Applicable thesis section.
- Dependencies.
- Failure consequence when stated.

Split compound requirements only when their parts can be evaluated independently.

### 2. Parse the criteria

For each criterion record:

- Criterion ID and name.
- Description.
- Weight when supplied.
- Performance descriptors.
- Required evidence.
- Relationship to demands.
- Whether it can be assessed from the submitted material.

Do not invent equal weighting when formal weights are available.

### 3. Identify critical parts

Mark as critical when a part:

- Is explicitly mandatory.
- Has high rubric weight.
- Is necessary for technical validity.
- Is necessary to answer the research questions.
- Is a prerequisite for other criteria.
- Can cap or fail the assignment if absent.

Examples may include:

- Correct problem formulation.
- Research questions.
- Method justification.
- Reproducible evaluation.
- Source traceability.
- Results connected to conclusions.
- Required format or deliverables.

### 4. Build an evidence map

For each requirement and criterion, locate:

- Direct evidence.
- Partial evidence.
- Contradictory evidence.
- Missing evidence.
- Relevant technical-validator findings.
- Relevant citation, definition, structure, or style findings.

Evidence must include file and line or section when available.

### 5. Evaluate each critical part

Use one of these statuses:

- `OK`: The part is fulfilled at the expected level with no material adjustment needed.
- `Needs Adjustment`: The part is present but incomplete, unclear, incorrect, weak, or missing.
- `Not Assessable`: Required information or material is unavailable.
- `Accepted Exception`: A requirement is intentionally inapplicable and the exception is documented.

For each part provide:

- Status.
- Evidence.
- Reasoning.
- Adjustment needed.
- Severity.
- Confidence.

### 6. Score each criterion

Use whole numbers from 1 to 10:

- 1: Missing or unusable.
- 2: Extremely weak fulfillment.
- 3: Major deficiencies.
- 4: Weak and incomplete.
- 5: Partly adequate.
- 6: Adequate with substantial adjustments.
- 7: Good with clear improvements needed.
- 8: Very good with limited material issues.
- 9: Excellent with only minor issues.
- 10: Fully meets or exceeds all stated expectations with no material weakness found.

For every score include:

- Score.
- Short justification.
- Evidence locations.
- Confidence.
- Most important action needed for the next score level.

Do not score a criterion that is not assessable.

### 7. Determine the overall score

Use supplied weights. If no weights exist:

1. Prioritize critical and mandatory criteria.
2. Consider the separate criterion scores.
3. Apply justified caps for blockers, critical omissions, or non-compliance.
4. State the reasoning briefly.

Do not hide behind a precise decimal. Give a whole-number final score.

## Score Caps

Apply a score cap only when justified by demands or central academic validity.

Possible examples:

- Thesis does not compile: overall score normally cannot exceed 5 until fixed.
- Central research question is unanswered: overall score normally cannot exceed 6.
- No usable methodology or evaluation: overall score normally cannot exceed 4–5.
- Widespread unresolved citations affecting traceability: citation criterion cannot receive a high score.

These are defaults, not institutional rules. Explicit rubric rules override them.

## Required Output Structure

### 1. Critical Parts Identified

List the critical parts derived from the demands and criteria.

### 2. Evaluation of Each Part

For every critical part:

- **Status:** OK / Needs Adjustment / Not Assessable / Accepted Exception.
- **Evidence:** File, line, section, or quoted requirement.
- **Reasoning:** Brief explanation.
- **Adjustment:** Specific action when needed.

### 3. Criteria Scoring (1–10)

For every assessable criterion:

- **Criterion name: score/10.**
- Short justification.
- Evidence location.
- Confidence.
- Next-level action.

List unassessable criteria separately without numeric scores.

### 4. Strengths

List evidenced strengths tied to demands, criteria, or technical quality.

### 5. Weaknesses

List the most consequential weaknesses. Do not duplicate the complete findings list.

### 6. Writing Style and Authorial Revision

Describe observable writing issues and how the student can revise the work to express their own reasoning more clearly. Do not claim to detect AI authorship.

### 7. Prioritized Adjustments

Separate:

- Must fix.
- Should fix.
- Optional.
- Requires supervisor clarification.

### 8. Final Overall Score (1–10)

Give the score, confidence, applicable caps, and a concise reason.

## Strength and Weakness Rules

Strengths must be specific, for example:

- “The experimental metrics in Section 5.2 map directly to RQ1.”
- “The problem formulation defines graph nodes, edges, and agent observations consistently.”

Avoid generic praise such as:

- “The assignment is good.”
- “The structure is nice.”
- “The student clearly worked hard.”

Weaknesses must identify effect, not merely preference. Explain whether the issue affects correctness, traceability, reproducibility, readability, or criterion fulfillment.

## Constraints

- Never invent demands or criteria.
- Never assign a numeric score to an unassessable criterion.
- Never reward polished language when core content is absent.
- Never treat the validator's general preferences as formal rubric requirements.
- Never infer academic misconduct from writing style.
- Never ignore contradictory evidence.
- Never give a final score without showing how critical requirements influenced it.
