# Validation pass — `2.Introduction.tex` (after readability edits)

Re-read of the chapter after the edits from `Introduction-readability-review.md`
were applied. Two questions: (1) how much AI-writing signature is left, (2) how
steep is the math for a reader who doesn't already know this material. Ends with
a verdict and a prioritized list of further changes.

One bug fixed along the way, not a style choice: `\bottomrule)` at the end of
the measures table (old L1075) had a stray `)` that would have broken the table
— removed.

---

## Verdict

**AI-writing signature: substantially reduced, not eliminated.** The first-pass
edits killed the worst repetition (duplicated case breakdowns, the
Method-vs-Problem-Formulation boilerplate, the defensive hedges). What's left
is lower-frequency and more structural: the chapter still explains almost
everything twice (once informally, once formally) and still narrates its own
scope decisions ("this is a design decision... not a property of the
problem"). That's a genre convention as much as an AI tic at this point — a
human author writing careful problem-formulation prose does some of this too
— so further cuts have diminishing returns unless you want a genuinely
different, terser register throughout.

**Math density for a new reader: uneven, with one clear spike.** Sections
3.3–3.6 and 3.8 pace themselves well — formal definition, then a grounded
example, most of the time. Section 3.7 ("The learning problem", the POSG) is
a different register: it's the one place that introduces a full formalism
(an 8-tuple) with no worked example anywhere in it, and it assumes the reader
already knows what a POSG, a discount factor, and centralised-training-
decentralised-execution are. If your reader is a committee member without
an RL background, this subsection — not 3.1's well-formedness detour, not the
observation section already revised — is where they will actually get lost.
There's also a smaller, structural problem in §3.1: the well-formedness
digression (L194–228) is placed before agents and collisions even exist in
the reader's model, which front-loads a fairly advanced correctness caveat
about *other people's* baselines before the reader has the core model at
all.

---

## 1. Remaining AI-writing traces

### 1.1 New, self-inflicted repetition from the last edit pass

Three "is realised in Section~X" pointers now read almost identically, where
before they were varied but individually wordier:

> "How $q_i(t)$ is set for a free agent... is realised in
> Section~\ref{sec:method:model}." (L821–822)
>
> "...) is realised in Section~\ref{sec:method:controllers}." (L755–756)
>
> "...are choices made in Section~\ref{sec:method:model}." (L911–912)

Minor, and arguably fine — this is a much lower-cost repetition than the
sentence-length boilerplate it replaced — but flagging since converging on
one templated phrase across edits is exactly the pattern being screened for.
**Suggested change:** leave two of the three as "is realised in ...", vary
the third to something like "Section~\ref{sec:method:controllers} specifies
how."

### 1.2 "Explain, then immediately justify why it needed explaining" still recurs

A few instances survived the first pass because they weren't flagged as
defensive hedges specifically — they're closer to a narrated design-log
voice:

> "This guarantee is a property of those particular baselines, not a general
> feasibility requirement of the coupled storage-routing model studied
> here." (L197–198)
>
> "This is a design decision of the study rather than a property of the
> problem, and it is made so that a difference in results is attributable to
> the routing architecture..." (L719–721)
>
> "This is the only instance where the querying entity is itself an occupant
> of $S$, and so the only one that excludes anyone." (L744–745)

**Suggested change:** these are lower priority than the ones already cut —
each does carry real information (not pure hedge) — but the third one
(L744–745) restates the same fact twice in one sentence ("the only instance
where..." / "the only one that..."). Could compress to: "The decentralised
case is the only one where the querying agent is itself inside $S$, so it is
the only one that excludes anyone."

### 1.3 Roadmap/meta-narration at section openings — largely a genre choice now

L72–79 ("This section makes that picture precise... and proceeds in the
order in which a simulation run unfolds") and L81 (the what-vs-how framing)
remain. These were deliberately kept in the first pass as useful signposting.
On re-read, they still read a little "generated," but removing them would
cost real navigational value in a 1200-line formal section. **No change
recommended** unless you want to cut navigational aids generally, which is a
bigger call than a wording fix.

### 1.4 What's genuinely gone

Worth naming so it's clear the first pass had effect: the duplicated
wait/move breakdown, the four-times-repeated Method-vs-Problem-Formulation
disclaimer, the communication-graph/well-formedness/notation hedges, and the
"not because any candidate could otherwise violate them" aside are all
cleanly resolved. Score.md's specific complaint list (repetitive
explanatory patterns, "This is..." constructions, uniform formality) is
meaningfully addressed for the parts it targeted.

---

## 2. Math density, section by section

Rated for how much a reader has to hold in their head with no concrete
grounding before the next foothold (example, figure, or table).

| Section | Density for a new reader | Notes |
|---|---|---|
| 3.1 Environment | Medium, one bad placement | Graph/roles fine; well-formedness digression (L194–228) is advanced and arrives before agents exist in the model — see §2.1 below |
| 3.2 Agents and collisions | Low–medium | Every formal piece gets a worked case (wait/move, vertex/swap conflict) plus a figure |
| 3.3 Where the items are | Low | Best-grounded subsection — matrix example, numeric knapsack check, tea/coffee/mugs table all present before anything abstract is asked of the reader |
| 3.4 Where the work comes from | Low | $\tau_1$ running example carries the whole subsection |
| 3.5 Who decides | Medium | Table 2 (info regimes) does a lot of the work; the occupancy-fraction definition (\Cref{eq:occupancy}) is stated once abstractly, then made concrete per architecture — reasonable pacing |
| 3.6 What a decentralised agent sees | Low–medium (after edits) | Now has numeric examples at both previously-bare spots ($\eta_i$ bound, $\delta_i$) |
| **3.7 The learning problem** | **High** | See §2.2 below — the density spike of the chapter |
| 3.8 How the two layers close the loop | Low | Plain prose, one equation pair, a figure |
| 3.9 How a run is scored | Medium | Table previews every quantity before its equation, which helps; the entropy/concentration equations ($H_T$, $C_T$) are the one spot here with no worked number, only a schematic figure |
| 3.10 Notation | Low | Short, now just a pointer |
| 3.11 Scope and assumptions | Low | List format, plain prose |

### 2.1 §3.1: well-formedness digression is early and advanced

L194–228 explains a completeness condition (Ma et al.'s "well-formed"
instances) that only matters for *some baseline algorithms this thesis
compares against* — it's a property of other people's methods, not of the
model being defined. It currently sits between the basic action-cost
equations and the Agents/Collisions subsection, i.e. before the reader has
even met $\mathcal{A}$, $\ell_i(t)$, or a single collision rule. A reader
building a mental model for the first time hits a two-directional-path
graph-theoretic condition about a third party's algorithm before they know
what an agent is.

**Suggested change:** move this whole block (L194–228, plus
Figure~\ref{fig:wellformed}) to either (a) immediately after §3.2 (Agents and
collisions), once $\mathcal{A}$ and endpoints-as-agent-behavior exist, or (b)
into Scope and Assumptions (§3.11), since it's already framed as "imposed on
the generated instance as an assumption... reported only for the baselines
that actually require it" — which is exactly what §3.11 is for. Option (b)
is the bigger structural change; option (a) is a smaller, safer move that
still fixes the ordering problem.

### 2.2 §3.7: the POSG is the density spike

Compare this subsection's texture to every other one: it opens with one
sentence of motivation ("Because each agent acts from $o_i(t)$..."), then
goes straight to the 8-tuple $\mathcal{M} = (\mathcal{A}, \mathcal{S},
\{\mathcal{U}_i\}, P, \{\mathcal{O}_i\}, \{O_i\}, \{R_i\}, \gamma)$. Table 3
helps by mapping each symbol back to something defined earlier, which is a
good instinct — but the table is still eight abstract symbols with no
numbers attached, unlike every table/example elsewhere in the chapter.

Concrete gaps for a reader without RL background:
- "partially observable stochastic game" is used before being motivated —
  the reader isn't told *why* this formalism is the right one, only that it
  "is an instance of the standard formalism."
- The action-masking paragraph (L974–981) is abstract set theory
  ($\mathcal{U}_i := \bigcup_v \mathcal{U}(v)$, zero probability under $P$)
  with no concrete instance — contrast with §3.2, which grounded the same
  kind of idea ("if $\ell_i(t)=A$...") every time.
- The objective (\Cref{eq:objective}, the discounted team-average return) is
  given with zero grounding: no toy numbers, no sentence like "so a fleet
  that completes tasks sooner and more often scores higher."
- $\gamma$ (discount factor) is introduced only as "a training parameter,
  Section~\ref{sec:method:training}" — a reader unfamiliar with RL won't
  know discount factors trade off near-term vs. long-term reward unless they
  already know that.

**Suggested change (biggest single win available in the chapter):** add one
short grounding paragraph before or after \Cref{eq:posg} — plain language,
no notation — saying something like: *"Every timestep, each agent looks at
what it can see, all agents act at once, the warehouse updates, and each
agent gets a number back saying how good that was. Doing this over and over,
under uncertainty about what other agents will do and unable to see the
whole warehouse, is exactly what a partially observable stochastic game
formalises."* Then let the tuple and table follow as the formal restatement,
the same what-then-how pattern the rest of the chapter uses successfully.
A one-sentence gloss on $\gamma$ ("weights near-term reward over reward far
in the future") would also close the gap cheaply.

### 2.3 §3.9: entropy/concentration could use one worked number

$H_T$ and $C_T$ are given a schematic figure (two qualitative patterns) but
no numeric instance, unlike almost every other equation in the chapter. A
small worked example — e.g. three edges used with counts 8, 1, 1 — would
match the pacing set everywhere else and take two sentences.

**Suggested change:** after \Cref{eq:entropy}, add: *"For three edges used
$8$, $1$ and $1$ times, $p_T = (0.8, 0.1, 0.1)$ and $H_T \approx 0.39$; for
three edges used evenly ($p_T = (1/3,1/3,1/3)$), $H_T = 1$."* Optional, but
consistent with the chapter's own established convention.

---

## 3. Priority order for further changes

1. **§3.7 grounding paragraph** — highest impact, cheapest fix, addresses the
   one real comprehension gap in the chapter.
2. **§3.1 well-formedness relocation** — structural fix, no new prose needed,
   just moves an existing block.
3. §3.9 entropy worked example — optional, consistency-driven, low cost.
4. §1.1/§1.2 minor phrasing variation — cosmetic, skip unless you want to be
   thorough.

Mark up with ✅/✂️/❌/💬 as before and send back — nothing above has been
applied to the `.tex` file.
