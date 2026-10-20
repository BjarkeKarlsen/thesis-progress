# "Who decides" reformulation — proposed improvements

Comparing your pasted rewrite against the current `sec:pf:controllers` text.
Mark each ✅ accept / ❌ decline / 💬 comment, send back, I'll apply only what
you approve. Nothing has been changed in the `.tex` yet.

---

## Clear wins (I'd recommend accepting these)

### 1. Define what $\Pi$ actually is

I checked. Nowhere in the current chapter is $\Pi$ ever stated in plain
words. It's used constantly ($\pi \in \Pi$, "$\Pi$ places no further
restriction...", later the decision problem optimizes over $\Pi$), but never
introduced. Your rewrite's opening fixes this directly:

> "We represent a controller by $\pi \in \Pi$, where $\Pi$ is the set of
> admissible controllers studied in this thesis."

This is a real gap-fill, not just rewording. Recommend adopting.

### 2. Explain *why* it's called a "partial" matching

Current text just asserts "some agents or tasks may remain unmatched." Your
version explains the term itself:

> "The matching is called partial because not every free agent or waiting
> task must be paired: there may be more tasks than agents, or more agents
> than tasks."

Also adds a one-line concrete example ("agent $a_1$ serving task $\tau_3$").
Good, minor clarity win. (Small note: this introduces a throwaway pairing
disconnected from the running $\tau_1$/$a_2$ example used everywhere else in
the chapter. Not wrong, just flagging the inconsistency in case you'd rather
it use symbols already in play.)

### 3. Ground "global state" for the centralised controller

Current text just says "may condition on the global state" without saying
what that contains ($s_t$ itself isn't formally defined until later, in "The
learning problem"). Your addition,

> "...including all agent positions, tasks, and relevant traffic
> information"

bridges that gap usefully, since the reader hits this before $s_t$ exists.
Recommend adopting.

---

## Needs a technical fix if adopted (not fatal, just needs care)

### 4. New symbol $\mathbf{u}(t)$ for the joint action collides with existing notation

Your rewrite names the joint action $\mathbf{u}(t)$. But
`Section~\ref{sec:pf:coupling}` ("How the two layers close the loop") already
uses **$u_t$** (no bold, different form) for the exact same object:

> `$s_{t+1} \sim P(\cdot \mid s_t, u_t)$, $u_t \sim \pi(\cdot \mid s_t)$`

If we adopt $\mathbf{u}(t)$ here, that later section needs to be updated to
match, or we should just not introduce a new symbol and let the tuple stay
unnamed like it is now (only written out in full each time it's needed,
which is what the current text does). Your call: rename the later use to
match, or drop the new symbol here.

The problem is we already use the symbol without describing it in the section. Do which letter is best to update and which is best to keep. Also update the Notation.

### 5. Splitting `eq:partition` into three equations needs the label moved correctly

Currently the whole partition definition ($\mathcal{Y}=\{Y_1,\dots,Y_p\}$,
covers $V_{\mathrm{mov}}$, pairwise disjoint) is **one** equation labelled
`eq:partition`, cited later in the congestion-instrument paragraph
("reusing the partition \Cref{eq:partition} already defined above"). Your
rewrite splits this into three separate equations with prose between them.
If adopted, `\label{eq:partition}` needs to move to whichever one of the
three should resolve when `\Cref{eq:partition}` is used later (I'd put it on
the first, the one defining $\mathcal{Y}$ itself). Doable, just needs doing
carefully, not a blocker.

---

## Judgment calls — these push in the opposite direction of the trims we've been making all session

Score.md's original complaint (the one that kicked off this whole editing
pass) was that the chapter over-explains standard notation and concepts.
Several of your additions reintroduce exactly that pattern. Not wrong, just
flagging the tension so you can decide deliberately rather than by default:

Here we take the solution that provides most clarity to the reader

### 6. Explaining the $\sim$ symbol

> "The symbol $\sim$ means that the action may be sampled from the
> probabilities produced by the policy."

"Distributed as / sampled from" via $\sim$ is completely standard
probability notation. Explaining it here reads as the kind of over-explained
basic-notation aside we've been cutting elsewhere in this chapter (e.g. we
did *not* explain what $\in$ or $\forall$ mean). Leaning decline, but your
call if you think a reader without a probability background needs it.

Only take the notation that is needed for good readuning 


### 7. Defining "deterministic" vs. "stochastic" in prose

> "A deterministic rule always chooses the same action for the same
> available information. A stochastic rule instead gives probabilities to
> legal actions and samples one of them."

Same category as #6, both terms are standard vocabulary for this thesis's
target reader (an MSc committee in RL/MARL). Current text just says
"possibly stochastic" and moves on. Leaning decline.

Maybe give a little more explantion but not too much

### 8. Splitting the partition equation into three, each with its own explanatory sentence

Beyond the label-mechanics issue in #5: is a partition (disjoint sets whose
union is the whole set) really unclear enough to this audience to need three
separate equations and three sentences unpacking each one? The current
single compact equation says the same thing in one line. Leaning decline,
matching the "trust standard notation" principle used elsewhere in this
chapter, but this is very subjective, happy to defer to you.

Keep what is best for the reader. 

### 9. Restating the CTDE paragraph at length

Current:
> "Parameter sharing is appropriate for homogeneous agents and does not make
> execution centralised. Where global information is used during training
> only, the method is described as centralised training with decentralised
> execution."

Yours adds a full explanation of why execution stays decentralised despite
shared parameters, and restates $o_i(t)$ independence. Says nothing false,
just more words for the same claim. Leaning decline, but weaker opinion than
#6-8, this one's genuinely borderline.

If this help the reader to understand it 

### 10. Dropped: pointer to where $o_i(t)$ is formally defined

Current text says the decentralised controller "conditions only on the
local observation *defined in Section~\ref{sec:pf:observations}*". Your
version drops that pointer. Since $o_i(t)$ isn't formally built until the
very next subsection, I'd keep the pointer, recommend restoring it
regardless of what else you accept from this rewrite.

do as you see fit

---

## Bottom line

Accept 1-3 outright. 4-5 are fine to adopt but need the technical fix done
alongside them, not standalone. 6-9 I'd lean decline since they cut against
the density work we've already done this session, but they're genuinely
matters of taste, not correctness. 10 should be kept regardless of the rest.
