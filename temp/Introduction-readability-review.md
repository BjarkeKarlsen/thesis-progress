# Readability review — `2.Introduction.tex`

Source: `thesis/Chapters/2.Introduction.tex` (Introduction, Project Description,
Problem Formulation). Based on the "AI writing" and "writing quality" findings in
`Score.md` (dense, self-referential, repetitive explanatory patterns, long
sentences, heavy cross-referencing, uniform formality, redundant re-explanation).

This is a **punch list for you to annotate**, not a finished edit. For each item,
mark: ✅ do it / ✂️ do it but less aggressively / ❌ leave as is / 💬 comment.
Nothing in the .tex file has been changed yet.

---

## 1. Recurring patterns (apply once, fix everywhere)

These show up many times across the chapter. Rather than list every occurrence,
each gets one representative example — if you agree with the direction, it gets
applied wherever the pattern recurs.

### 1.1 Near-duplicated "Wait case / Move case" explanation ✅

The same two-case breakdown is written out in full **twice**, ~90 lines apart,
for two closely related equations (`eq:onestepcost` and `eq:transition`):

> **First occurrence (lines 183–191):**
> "Wait case] $v = w$: the agent stayed put, the same situation
> \Cref{eq:transition}'s wait case describes. If $v = w = A$, the cost
> charged is $c_{\mathrm{wait}}$... Move case] $(v,w) \in E$: the agent
> traversed an edge, matching \Cref{eq:transition}'s move case. If $v = A$,
> $w = B$, and $(A,B) \in E$, the cost charged is $c(A,B)$..."
>
> **Second occurrence (lines 275–283):**
> "Wait case] $\ell_i(t+1) = \ell_i(t)$: the agent stays at the same
> vertex between $t$ and $t+1$. If $\ell_i(t) = A$, then $\ell_i(t+1) = A$
> too... Move case] $\bigl(\ell_i(t), \ell_i(t+1)\bigr) \in E$: the agent
> moves to a vertex directly reachable by one edge... If $\ell_i(t) = A$,
> $\ell_i(t+1) = B$, and $(A,B) \in E$, this is what selecting $\mathrm{move}(B)$ produces."

**Suggested change:** the two equations already cross-reference each other
("the same situation \Cref{eq:transition}'s wait case describes"). Keep the
full worked breakdown in one place (probably `eq:transition`, since it comes
first structurally) and shorten the other to one sentence: *"waiting
($v=w$) costs $c_{\mathrm{wait}}$; moving costs $c(v,w)$, per
\Cref{eq:transition}."*


### 1.2 "This is a Problem Formulation choice, not a Method one" repeated near-verbatim ✅

Appears at least four times, almost word for word:
- L764–765: *"is a Method-level choice, Section~\ref{sec:method:controllers}, not a Problem-Formulation one."*
- L832: *"is a Method-level choice, Section~\ref{sec:method:model}."*
- L907: *"are choices made in Section~\ref{sec:method:model}."*
- L1184–1185: *"is Implementation, not Problem Formulation (Section~\ref{sec:impl:cost})."*
- L1275–1276 / L1288: *"this would redefine what a valid or well-scored solution is, which makes it a change to the Problem Formulation, not the Method."* / *"That redefines what $\pi^{\mathrm{assign}}$ is allowed to output, not merely how it is computed, so the same holds here: it belongs to the Problem Formulation, not the Method."*

**Suggested change:** state the Problem-Formulation-vs-Method boundary rule
**once**, early (you already do this at L81–84: *"this section states what the
objects are, not how they are computed... Realisations ... are deferred to
Section~\ref{sec:method}"*), and afterwards just give the section pointer
without re-explaining the rule each time, e.g. *"realised in
Section~\ref{sec:method:model}"* instead of restating why it's deferred.

### 1.3 Defensive "this is X, not Y" hedges against a misreading nobody's making ✅

A recurring move: state something, then pre-empt a misinterpretation the
reader likely wasn't going to have.

> "This communication graph is a different object from the warehouse graph
> $G$, not the same thing under a new name: its nodes are agents, not
> places, and its edges mean 'can talk to', not 'can move to'." (L894–896)
>
> "This is a statement about which vertices the well-formedness check
> ranges over, not a redefinition of $V_{\mathrm{ep}}$..." (L229–231)
>
> "None of these are typos or the same object under different names."
> (§Notation, L1227–1228)
>
> "not because any candidate $(F,\pi)$ could otherwise violate them"
> (L1199–1200)

**Suggested change:** these read as if anticipating a reviewer's objection
rather than explaining to a reader. Most can be cut to the positive
statement alone — e.g. *"$G^{\mathcal{A}}_t$'s nodes are agents and its
edges mean 'can talk to', distinct from $G$."* Trust the notation ($G$ vs.
$G^{\mathcal{A}}_t$) to carry the distinction; you don't need to also say
what it *isn't*.

### 1.4 Formulaic transitions and openers ✅

Score.md calls this out directly. Examples in this chapter:
- "This subsection explains each of the four in turn..." (L789–790)
- "This section makes that picture precise... and proceeds in the order in which a simulation run unfolds..." (L72–79)
- "Throughout, this section states *what* the objects are, not *how* they are computed." (L81)
- "Intuitively, the warehouse is a map of..." (L90) / "Intuitively," is used as a stock opener a few times.

**Suggested change:** not all need to go — L72–79 is a genuinely useful
roadmap sentence and is fine to keep. But collapse the throat-clearing ones
("This subsection explains...", "This section states...") into the
sentence that follows, or drop them. Score.md's own suggested fix:
*"This subsection explains..."* → *"Next, we describe..."* — or just start
with the content.

### 1.5 No authorial "we" anywhere except once ✅

"We formalise this as a finite directed graph" (L92) is the only first-person
verb in ~500 lines. Everything else is impersonal ("This section defines...",
"The model further assumes...", "This thesis investigates...").

**Suggested change:** Score.md explicitly recommends this ("Instead of 'It
is shown that…', write 'We show that…'"). You don't need "we" everywhere —
formal problem-formulation prose is conventionally impersonal in this
field — but a few reintroduced instances at natural points (defining the
objective, stating the scope decisions, motivating a design choice) would
break the uniformity Score.md flags. Candidates: L19 ("The main
contribution is..." → "Our main contribution is..."), L1013 ("The loop
closes in two directions" could become "We close the loop in two
directions" if you want more authorial voice), L1238 ("The model above is
deliberately narrower..." → "We deliberately keep the model narrower...").

### 1.6 Worked numeric examples after nearly every definition ✅

The chapter follows almost every formal definition with a fully worked
example using the same running characters ($\tau_1$, agent $a_2$, tea at
vertex $A$). E.g. L546–548, 569–573, 598–604, 642–644, 652–653, 838–843.

This is **not automatically a problem** — a consistent running example
across a whole formal section is a good pedagogical device and is part of
what the "OK / strong formalism" score in Score.md is praising. But the
density is very high: almost every equation gets a full "If $v=A$... then
..." gloss immediately after it, which is part of why Score.md calls the
writing "occasionally dense."

**Suggested change:** keep the running example, but trim roughly every
second instance to a half-sentence instead of a full worked-through
paragraph, particularly where the example doesn't add information beyond
restating the equation in words (e.g. L642–644, L652–653 could each lose
a sentence).

### 1.7 Sentence length / clause stacking ✅

Some sentences carry 3–4 subordinate clauses and multiple em-dashes in a
row, which is where the "dense" complaint in Score.md is sharpest:

> "That assumption is weaker than the blanket strong-connectivity condition
> \citet{vanKnippenberg2021} relies on for the same purpose, in the
> non-lattice MAPF formulation this section otherwise follows closely for
> the environment and observation model." (L152–155, one sentence)
>
> "Strong connectivity would be simpler to state and check, but it would
> also rule out an unreachable side-room or a maintenance-only spur, the
> kind of 'irregular block' this formulation is meant to allow." (L156–158)
>
> "The independent boundary is used so that time lost travelling to $s_j$
> counts as part of the active phase, eligible for the blocking measure
> $W_T$, defined in Section~\ref{sec:pf:measures} (\Cref{eq:waiting}), rather
> than being folded into generic pre-assignment queueing." (L613–616)

**Suggested change:** split into two sentences each. E.g. L152–155 →
*"That assumption is weaker than the strong-connectivity condition
\citet{vanKnippenberg2021} relies on for the same purpose. Their
formulation is non-lattice MAPF, and this section otherwise follows it
closely for the environment and observation model."*

### 1.8 Cross-reference density interrupting flow ✅

Score.md flags this specifically. Some sentences carry 2–3 `\Cref`/`\citep`
pointers, e.g.:

> "The two cases are joined by 'or,' not folded into one, because waiting
> does not require a self-loop $(A,A) \in E$: $E$ never contains self-loops
> (Section~\ref{sec:pf:env}), so the wait case has to be stated on its own
> rather than treated as a degenerate move." (L284–287)

**Suggested change:** not all cross-references can go — this is a formal
section and traceability matters — but low-value ones (pointing back to
something stated one paragraph earlier, or a self-evident fact like "$E$
never contains self-loops") can be cut without losing anything. Reserve
`\Cref` for pointers a reader would actually want to follow.

---

## 2. Section-by-section notes

### 2.1 Introduction (§1, L9–19) ✅

This section is in comparatively good shape — shortest, most direct part of
the chapter, and the one place with only light AI-pattern fingerprints. Minor
items:

- L11: one long sentence covers both SLAP and MAPD/MAPF in one breath; could
  split at "The former is commonly studied...".
- L13: "Optimising either layer while treating the other as fixed can
  therefore produce a configuration that is locally attractive but poor at
  system level." — good sentence, no change needed.
- L19: "The main contribution is not a new general-purpose MAPF, MAPD, or
  SLAP solver. It is (i)..." — fine, matches Score.md's "modest, precise
  contribution" praise. Could go to "Our main contribution is..." per §1.5
  above.

**Overall: light touch here, this section reads the most human already.**

### 2.2 Project Description (§2, L21–65) ✅

Also comparatively clean. One item:

- L47: "it is decomposed into four primary questions:" — lowercase "it" at
  the start of a line after a line break reads like a typo/formatting
  slip, not a style issue — worth a capitalisation/consistency check
  regardless of this readability pass.
- L64: "operation conditions" is probably meant to be "operating
  conditions" — flagging as a likely typo, not a style note.

### 2.3 Problem Formulation (§3, L66–1293) ✅

This is where nearly all of §1's patterns concentrate — it's ~90% of the
chapter's length and carries the bulk of the "dense", "self-referential"
critique from Score.md. Beyond the recurring patterns above, a few
section-specific spots:

- **§3.1 The environment (L87–249):** heaviest concentration of defensive
  hedging (§1.3) and long sentences (§1.7). The well-formedness discussion
  (L199–237) in particular re-explains the same distinction (single-path vs.
  bidirectional-path requirement) three times across L212–220 and L222–237.
  Worth tightening to one clear statement plus the figure.

- **§3.5 Who decides (L668–779):** the congestion-instrument paragraph
  (L732–767) repeats the phrase "own window"/"own information regime" four
  times in quick succession (L746, 747, 758, 761) — reads mechanical.
  Suggested: vary the phrasing or drop the repeated qualifier once it's
  established.

- **§3.6 What a decentralised agent sees (L782–920):** actually the
  **best-written subsection** in the chapter — it opens with a genuinely
  plain-language framing ("A decentralised agent does not see the whole
  warehouse. At every timestep it builds a local observation $o_i(t)$ out of
  four things...", L785–790) before going formal. This is the tone Score.md
  is asking for throughout. **Worth using as the template** for revising the
  denser subsections (3.1, 3.3, 3.7) rather than writing new guidance from
  scratch.

- **§3.9 Notation used more than once (L1222–1232):** very short, but the
  whole paragraph is defensive framing (§1.3) — "None of these are typos or
  the same object under different names" is explaining to the reader that
  you didn't make a mistake, rather than telling them something useful.
  Could shrink to two sentences: state that several symbol families share a
  base letter, point to the appendix table.

- **§3.10 Scope and assumptions (L1235–1293):** clear and direct list
  structure, no complaints here. The closing paragraph (L1290–1293) is a
  good, human-sounding summary sentence — no change needed.

---

## 3. What NOT to change

To be explicit about the flip side, since Score.md's "theoretical rigour: 9"
and "strong formalism" praise depends on this staying intact:

- Don't loosen the formal definitions, equations, or the worked numeric
  examples in general — trim volume (§1.6), don't remove precision.
- Don't remove the scope/assumptions list (§3.10) or the Problem-Formulation
  vs. Method boundary itself (§1.2) — only the repeated *restating* of that
  boundary rule.
- §3.6 (What a decentralised agent sees) doesn't need rewriting — it's
  already the tone the rest should move toward.

---

💬 Section from what agents sees becomes very mathmatically hard and no example used. Here we should make the writing less dense and explain it more as the reader do not unerstand the things beforehand 

## 4. Your call

Mark up the sections above (✅/✂️/❌/💬) and send this back — I'll apply
only the items you approve directly to `2.Introduction.tex`.
