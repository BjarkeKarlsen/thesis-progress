---
name: reviewing-thesis-style
description: Reviews academic thesis prose for clarity, specificity, cohesion, repetitive patterns, vague claims, excessive signposting, abrupt voice changes, and loss of authorial reasoning. Provides revision guidance without claiming to detect whether AI wrote the text.
compatibility: Requires thesis prose with locations. A grammar checker may supplement but must not replace contextual review.
---

# Thesis Writing-Style Reviewer

## Purpose

Help the student turn technically correct content into clear academic writing that expresses their actual reasoning, decisions, observations, and limitations.

This skill does not determine whether a human or AI wrote the text. It evaluates observable prose characteristics only.

## Principles

1. Do not estimate an “AI-written percentage.”
2. Do not recommend detector evasion or superficial humanization.
3. Preserve technical meaning and the student's natural level of formality.
4. Prefer specific revision advice over generic commands to “sound academic.”
5. Distinguish grammar errors from style preferences.
6. Prioritize unclear reasoning over minor wording issues.
7. Do not erase appropriate disciplinary terminology.
8. Encourage the student to add genuine project knowledge, not artificial imperfections.

## Inputs

- Ordered prose with source locations.
- Discipline and thesis level.
- User's preferred language variant.
- University writing requirements.
- Terminology and notation registry.
- Known non-native-language considerations when voluntarily provided.

## Workflow

### 1. Review clarity

Check for:

- Unclear subjects.
- Unclear pronoun references.
- Sentences with too many logical operations.
- Noun-heavy constructions hiding actions.
- Ambiguous comparison words.
- Undefined evaluative terms.
- Missing causal or contrast relationships.
- Claims whose level of certainty is unclear.

### 2. Review specificity

Flag vague wording such as:

- “significant” without statistical or practical meaning.
- “efficient” without a metric or comparison.
- “better” without a baseline.
- “large” or “small” without scale.
- “various” or “several” where the items matter.
- “this” without a clear noun.
- “the system” where several systems are in scope.
- “research shows” without source boundaries.

Do not require a number when a qualitative distinction is sufficient.

### 3. Review cohesion

Check whether:

- Adjacent sentences have a clear logical relationship.
- Transitions match the actual relation: addition, contrast, cause, consequence, example, or limitation.
- Topic shifts are signalled.
- Paragraphs maintain a stable subject.
- Terminology stays consistent.

### 4. Review formulaic patterns

Identify repeated patterns such as:

- Many paragraphs beginning with “Furthermore,” “Moreover,” or “Additionally.”
- Repeated “It is important to note that.”
- Repeated three-part lists with generic wording.
- Repeated section-ending summaries that add no information.
- Uniform sentence length and syntax over long passages.
- Generic openings such as “In today's rapidly evolving world.”
- Empty statements that a topic is “crucial,” “robust,” or “comprehensive.”

Describe the pattern without claiming it proves AI authorship.

### 5. Review authorial reasoning

Look for missing explanation of:

- Why a method was selected.
- Why an alternative was rejected.
- What changed during implementation.
- Which assumptions were necessary.
- What an unexpected result means.
- How a limitation affects interpretation.
- Which parts were adopted versus designed by the student.
- What evidence changed the student's initial expectation.

Recommend adding real project-specific reasoning where it is relevant and known to the student.

### 6. Review voice and stance

Check for:

- Abrupt changes between highly formal and conversational language.
- Unexplained movement between “we,” “I,” passive voice, and impersonal constructions.
- Overconfident claims unsupported by evidence.
- Excessive hedging that obscures conclusions.
- Evaluative wording presented as fact.
- First-person usage inconsistent with institutional policy.

Do not ban passive voice. Use active or passive constructions according to emphasis and disciplinary convention.

### 7. Review grammar and mechanics

Report recurring or meaning-changing issues such as:

- Subject-verb agreement.
- Article usage.
- Sentence fragments.
- Run-on sentences.
- Tense inconsistency.
- Punctuation around citations and equations.
- Capitalization of defined terms.
- Hyphenation consistency.

Avoid flooding the report with isolated low-impact corrections. Group recurring patterns and provide representative locations.

## Rule Catalogue

### STY001 — Vague evaluative claim

A term such as “better,” “efficient,” or “significant” lacks a criterion or context.

Default severity: Minor or Major.

### STY002 — Generic filler

A sentence adds little technical or argumentative content.

Default severity: Minor.

### STY003 — Repetitive transition pattern

The same transition is used repeatedly or without the correct logical relationship.

Default severity: Minor.

### STY004 — Formulaic paragraph pattern

A long passage repeats nearly identical paragraph or sentence structures.

Default severity: Minor or Suggestion.

### STY005 — Missing authorial reasoning

A design choice, result, or limitation is stated without explaining the student's reasoning where that reasoning is central.

Default severity: Major.

### STY006 — Abrupt voice change

The prose changes voice, terminology, or sophistication in a way that harms coherence.

Default severity: Minor or Major.

### STY007 — Excessive certainty

A claim is stronger than the presented evidence permits.

Default severity: Major.

### STY008 — Excessive hedging

Repeated cautious qualifiers obscure the actual conclusion.

Default severity: Minor.

### STY009 — Ambiguous pronoun or demonstrative

“It,” “this,” “that,” or “they” has multiple plausible antecedents.

Default severity: Minor.

### STY010 — Overloaded sentence

A sentence contains too many claims, qualifications, or logical relationships to follow reliably.

Default severity: Minor.

### STY011 — Terminology inconsistency

Word choice changes in a way that suggests different entities or concepts.

Default severity: Major or Minor. Coordinate with the definition auditor.

### STY012 — Unsupported emphasis

Words such as “clearly,” “obviously,” or “undoubtedly” substitute for evidence.

Default severity: Minor or Major.

### STY013 — Redundant restatement

A sentence repeats adjacent content without adding synthesis, precision, or consequence.

Default severity: Minor.

### STY014 — Grammar pattern affecting clarity

A recurring grammatical issue interferes with meaning.

Default severity: Minor or Major.

### STY015 — Unclear comparison

A comparative statement does not identify the compared methods, metric, or reference condition.

Default severity: Major.

## Authorial Revision Method

For passages needing substantial revision, recommend this sequence:

1. State the intended technical point in plain language.
2. Identify whether it is a fact, source-based claim, design choice, observation, result, or interpretation.
3. Add the evidence or reasoning appropriate to that type.
4. Remove generic framing that contributes no meaning.
5. Use the thesis's established terminology.
6. Adjust sentence structure only after the logic is clear.
7. Read the passage aloud and verify that the student could defend every claim orally.

When giving examples, distinguish between:

- Minimal correction.
- Clearer academic revision.
- Questions the student must answer before a responsible rewrite is possible.

## Output Requirements

Use the heading:

### Writing Style and Authorial Revision

Provide:

- Overall style strengths.
- Highest-impact clarity problems.
- Repeated patterns with representative locations.
- Passages missing authorial reasoning.
- Grammar patterns affecting meaning.
- A prioritized revision plan.
- A small number of representative before-and-after examples when requested.

For each finding include severity, confidence, location, excerpt, explanation, and revision strategy.

## Constraints

- Never classify text as AI-written or human-written.
- Never assign an AI probability.
- Never recommend adding mistakes, slang, or random variation to evade detection.
- Never replace precise technical language merely to sound more casual.
- Never rewrite claims whose intended evidence or meaning is unknown; ask for the missing reasoning or mark the issue for student revision.
- Never present a stylistic preference as a formal rule unless the rubric states it.

## In This Workspace

The author has written down their own prose rules in the "Thesis writing style" section of the workspace-root `CLAUDE.md`, and caption rules in `LATEX.md` ("Figure captions"). These count as stated requirements, so a breach of one is a finding, not a preference. Cite the rule by name. Among them: no `--` or `---` in prose, no colon or semicolon joining two clauses, the idea in words before its equation ("Formally,"), one idea per paragraph led by its point, no meta-commentary, examples named explicitly, the reason given for each choice, UK spelling, and a list of words to avoid ("information regime", "instrument", "internalise", "mixing time", "stale").

Use `reviewing-thesis-style` findings to point at text. Rewrites follow `CLAUDE.md`'s "Discuss before rewriting": propose, and change the thesis only once the author agrees.
