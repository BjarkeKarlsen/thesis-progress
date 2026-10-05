---
name: auditing-thesis-definitions
description: Audits first use and consistency of technical terms, acronyms, mathematical symbols, sets, functions, graph notation, reinforcement-learning notation, and thesis-specific concepts. Detects undefined terms, conflicting definitions, symbol reuse, notation drift, and inconsistencies between notation tables and prose.
compatibility: Requires ordered thesis content. Mathematical parsing and a project glossary improve accuracy.
---

# Thesis Definition and Notation Auditor

## Purpose

Ensure that readers encounter concepts, abbreviations, and symbols in a usable order and that each remains consistent throughout the thesis.

This skill is especially important for mathematically dense work involving graphs, multi-agent systems, reinforcement learning, warehouse models, algorithms, and custom problem formulations.

## Principles

1. Define specialized concepts before they are needed for reasoning.
2. First appearance in the compiled reading order matters more than file order.
3. One symbol should not silently represent several concepts.
4. One concept should not drift between multiple names or symbols without explanation.
5. Standard notation can still require clarification when the thesis gives it a project-specific meaning.
6. A notation table complements definitions but does not always replace definitions in the main text.
7. Local redefinition is acceptable only when scope is explicit.
8. Mathematical correctness takes priority over stylistic uniformity.

## Inputs

- Ordered prose and mathematical environments.
- Section hierarchy.
- Acronym and glossary files.
- Notation table.
- Custom-command definitions.
- Assignment terminology requirements.
- Baseline papers or frameworks the thesis claims to follow.

## Workflow

### 1. Build a terminology registry

Collect candidates from:

- Explicit definition phrases: “is defined as,” “we define,” “denotes,” “refers to,” and “let.”
- Definition environments.
- Acronym commands.
- Glossary entries.
- Capitalized or repeated domain-specific noun phrases.
- Mathematical displays and inline mathematics.
- Notation tables.
- Figure captions and algorithm descriptions.

For each term, record:

- Canonical form.
- Variants.
- First use.
- First definition.
- Later redefinitions.
- Section scope.
- Related symbols.
- Source attribution when the definition is borrowed.

### 2. Build an acronym registry

For each acronym, record:

- Short form.
- Long form.
- First use.
- First expansion.
- Plural and possessive forms.
- Glossary registration.
- Re-expansion after long gaps if required by project style.

Ignore common measurement units and universally understood abbreviations only when appropriate to the field and rubric.

### 3. Build a notation registry

For every mathematical symbol or structured expression, record:

- Symbol source form.
- Rendered semantic role when inferable.
- First use.
- Definition location.
- Type: scalar, vector, set, graph, function, random variable, policy, state, action, observation, reward, index, or parameter.
- Domain and codomain when specified.
- Scope.
- Later uses and conflicting meanings.

Track related expressions, for example:

- `G`, `G_t`, and `G_i`.
- `V` as graph vertices versus value function.
- `A` as agent set versus action space.
- `N` as number of agents versus neighborhood.
- `\mathcal{A}` as agent set versus action set.
- `\pi` as policy.
- `s_t`, `o_t`, `a_t`, `r_t`.

Do not assume visually similar symbols are identical when macros or subscripts indicate distinct meanings.

### 4. Check definition order

Report when:

- A specialized term is used materially before being defined.
- An acronym appears before expansion.
- A symbol is used in an equation before its meaning is stated.
- A function is used without enough information about inputs or outputs.
- A set is referenced before its members or role are described.
- A definition appears much later than sustained use.

A brief intuitive mention before a formal definition can be acceptable. Evaluate whether the reader can understand the earlier passage.

### 5. Check consistency

Compare all definitions and uses for:

- Conflicting wording.
- Changed scope.
- Singular/plural drift.
- Symbol reuse.
- Capitalization drift.
- Hyphenation changes that alter terminology.
- Different names for the same method or component.
- Notation-table mismatches.
- Baseline-paper notation mismatches when alignment is claimed.

### 6. Check definition quality

A useful formal definition should specify enough of the following for its role:

- Entity type.
- Constituent elements.
- Domain and codomain.
- Constraints.
- Temporal index.
- Agent index.
- Relationship to previously defined objects.
- Difference from similar concepts.

Do not demand all fields for every informal definition.

### 7. Check contribution boundaries

Determine whether the thesis distinguishes:

- Standard field terminology.
- Definitions adopted from prior work.
- Definitions adapted by the student.
- New project-specific definitions.

Borrowed formal definitions should normally be cited. New definitions should be clearly presented as part of the thesis formulation.

## Rule Catalogue

### DEF001 — Term used before definition

A specialized term is required for understanding before it is introduced adequately.

Default severity: Major or Minor.

### DEF002 — Acronym used before expansion

An acronym appears before its long form in the relevant reading context.

Default severity: Minor.

### DEF003 — Symbol used before definition

A mathematical symbol has a substantive use before its meaning is stated.

Default severity: Major.

### DEF004 — Conflicting definitions

The same term receives incompatible meanings.

Default severity: Critical or Major.

### DEF005 — Symbol reuse

One symbol represents different concepts without explicit scope or disambiguation.

Default severity: Critical or Major.

### DEF006 — Terminology drift

The same concept is named inconsistently, making identity uncertain.

Default severity: Major or Minor.

### DEF007 — Notation-table mismatch

The notation table conflicts with the thesis body.

Default severity: Major.

### DEF008 — Incomplete function definition

A function central to the formulation lacks needed domain, codomain, arguments, or interpretation.

Default severity: Major.

### DEF009 — Undefined set membership

A set is introduced without explaining what its elements represent.

Default severity: Minor or Major.

### DEF010 — Borrowed definition lacks attribution

A formal definition appears adopted from prior work but has no clear citation or attribution.

Default severity: Major.

### DEF011 — Redundant definition

A concept is redefined without adding precision or signalling that the definition is repeated.

Default severity: Minor or Suggestion.

### DEF012 — Conflicting acronym expansion

The same acronym is expanded differently or two concepts use the same acronym.

Default severity: Major.

### DEF013 — Index ambiguity

An index is used without stating whether it denotes time, agent, node, item, order, or another dimension.

Default severity: Major or Minor.

### DEF014 — Scope ambiguity

A local definition may be mistaken for a document-wide definition or vice versa.

Default severity: Major.

### DEF015 — Standard and project-specific meaning conflated

A common term is used with a narrowed or altered project-specific meaning without explanation.

Default severity: Major.

## Domain-Sensitive Checks

For graph-based multi-agent and reinforcement-learning theses, inspect carefully:

- Whether `G=(V,E)` denotes a warehouse topology, communication graph, observation graph, or another graph.
- Whether graph vertices represent locations, agents, tasks, or heterogeneous entities.
- Whether edges are static, dynamic, directed, weighted, or typed.
- Whether the agent set and action space use distinct notation.
- Whether global state and local observation are distinguished.
- Whether policies are shared or agent-specific.
- Whether rewards are individual, team-based, or mixed.
- Whether time, episode, and decision-step indices are consistent.
- Whether warehouse locations, storage faces, workstations, orders, and SKUs have distinct sets.
- Whether the problem formulation matches the notation table and implementation chapter.

These checks are contextual and must not impose one notation standard universally.

## Output Requirements

Provide:

- Definition and notation registry summary.
- Terms used before definition.
- Acronym findings.
- Symbol findings.
- Conflicting definitions.
- Notation-table inconsistencies.
- Baseline-alignment concerns.
- Recommended order of corrections.

Every finding must include the first use, definition location if present, conflicting locations, severity, confidence, and a concrete resolution strategy.

## Revision Guidance

Prefer actions such as:

- Add a concise intuitive definition at first use and retain the formal definition later.
- Move the formal definition before the first equation that depends on it.
- Rename one conflicting symbol and update all uses.
- State explicitly that a symbol has local scope.
- Align the notation table with the final body notation.
- Distinguish the warehouse graph from the agent communication graph.
- Add domain and codomain to a central function.

Do not rewrite mathematical notation automatically unless all dependent occurrences can be updated safely.

## Constraints

- Do not require definitions for every common word.
- Do not assume a term is standard merely because it appears frequently.
- Do not force notation from a baseline paper when the thesis explicitly defines a coherent alternative.
- Do not treat local scoping as conflict when it is clear.
- Do not change symbols without checking equations, algorithms, figures, tables, and code listings.

## In This Workspace

- `thesis/Chapters/2.Notation.tex` (`tab:notation`, the notation appendix) is the authority on which letter means what. A symbol used in the chapters but missing from the table, or used with a different meaning, is a DEF007 finding. The table lists symbols a reader meets more than once, not helpers local to one equation, so a missing local helper is not a finding.
- `notation_renames.md` at the workspace root lists the clashes already known and the renames agreed for them. Report a known clash as known, with its agreed rename, rather than as a new discovery.
- Model changes are tagged `% [Axx]` in the chapters with their reasons in `thesis-progress/temp/GAPS.md`. Check there before reporting a renamed or redefined symbol as drift.
