# Research goals, proposed changes, 2026-10-18

**Status: changes 1, 3, 4, 6, 7 and 9 applied 2026-10-19 as `[A41]` and `[A33]`, change 5 as `[A42]`. change 2 superseded by `[A44]` (reworded main result), change 10 open, change 11 made obsolete by the arrival model.** Original status: proposal. The author asked to note the changes to
the research goals and not to edit the Introduction yet. Each change becomes an `[Axx]` tag and
a `GAPS.md` entry when it is applied. `[A33]` (commons question, `thesis-progress/archive/workspace/ROADMAP.md`) is still
unapplied, and `stock_template_2026-10-17.md` has proposed `[A38]` to `[A40]`, so the changes
here would start at `[A41]`.

## Why

The thesis asks one main question, five sub-questions and a proposed commons question, over five
factors (storage rule, controller, congestion sensitivity in two layers, load, communication)
and two training regimes. The author asked for one clearly defined main result, and agreed on
2026-10-18 to the one in `short_run_2026-10-18.md`:

> How much adaptive storage shortens service time, and how that gain depends on how many agents
> one decision covers.

The short run backs this up. RQ1 has a clear answer for three of the four routers. The
differences between controllers are the open, interesting part. Congestion-aware storage at
β 3 gained nothing for any arm. So the goals should put RQ1 and RQ2 at the centre and make the
rest the limits of that result.

## The changes

Line numbers are for `thesis/Chapters/2.Introduction.tex` as of commit `5fbb4f8`.

### 1. A main result paragraph (new, after the RQ list, after line 67)

Proposed text:

> The main result answers RQ1 and RQ2 together. It is the gain in mean service time that
> adaptive storage gives over fixed storage under each controller, with its 95\% interval and
> the part of service time that moved. RQ3 and RQ4 mark where this result holds. RQ3 asks
> whether steering stock around congestion adds to the gain, and RQ4 asks at what load the gain
> stops.

Reason: a reader should know from the start which comparison the thesis stands on.

### 2. The main question (line 45 to 46), optional

Now: "How does closed-loop coupling between storage assignment and MAPD control affect service
time and congestion in a graph-based warehouse?"

Proposed:

> How much does closed-loop storage adaptation shorten service time in a graph-based warehouse,
> and how does that gain depend on how many agents one decision of the controller covers?

Reason: the main question then names the main result. "Congestion" moves to RQ3, where it is
measured. Keep the current wording if the title should stay with "coupling", and let change 1
carry the focus instead.

### 3. RQ1 (lines 51 to 53)

Proposed:

> Does closed-loop storage adaptation shorten service time relative to fixed storage under
> otherwise matched conditions, at a load where the fleet keeps up, and which part of service
> time changes?

Reason: service time only counts when the fleet keeps up (`sec:pf:measures`). The short run
showed that at load 0.3 one arm keeps up on 5 of 6 seeds and another on none, so the load is
part of the question.

### 4. RQ2 (lines 54 to 56)

Proposed:

> How does the gain of RQ1 differ among centralised, section-based and decentralised
> controllers that share one learning method and differ in how many agents one decision covers?

Reason: "the effect of coupling" becomes the gain of RQ1, so RQ2 is read on the same measure.
Add one sentence where RQ2 is formalised (near line 1600), because the short run showed that a
fleet close to its limit turns the same travel saving into a larger cut in waiting:

> The gain is read together with its split, because a fleet that runs close to its limit turns
> the same saving in travel into a larger cut in the wait for an agent.

### 5. RQ3 (lines 57 to 59), a scope decision for the author

Now RQ3 covers congestion sensitivity in both layers, the storage rule (β > 0) and the routing
reward (a realisation of the crowding reading).

Proposed, storage only:

> Does congestion-aware storage reduce crowding and blocked time beyond demand-only storage, and
> does the travel it adds cost more service time than it saves?

Reason: congestion sensitivity in routing means training every arm a second time, which doubles
the training budget, and it is a question about the controller, not about the coupling. The
storage half is cheap, since it needs only evaluation. At β 3 it gained nothing for any arm in
the short run, and the probe's only gain was at β 1, so β 1 becomes the test value.

If routing sensitivity stays, mark it conditional, like RQ5.

### 6. RQ4 (lines 60 to 61)

Proposed:

> At what load, in fleet size and arrival rate, does the gain of RQ1 stop holding, and at what
> load does each controller stop keeping up?

Reason: RQ4 then bounds the main result rather than standing beside it.

### 7. The commons question (`[A33]`, proposed as RQ6 in `thesis-progress/archive/workspace/ROADMAP.md`)

Proposed: fold it into RQ4 instead of adding a sixth question. RQ4 already runs the fleet sweep.
One sentence where RQ4 is formalised:

> On the same sweep, throughput per agent shows whether each agent finishes fewer tasks as the
> fleet grows, and whether that loss is faster when one decision covers fewer agents.

Reason: it uses the same runs and the same measure, and a separate question would split the
reader's attention.

### 8. RQ5 (lines 62 to 67)

No change. It stays conditional.

### 9. The factors in Aim and scope (lines 30 to 36)

Proposed, to mark which factors carry the main result:
- Item 1, now "storage mode: fixed or periodically updated", becomes "storage rule: fixed,
  demand-only or congestion-aware".
- After the list, one sentence:

> Storage rule and controller carry the main result. Congestion sensitivity, load and
> communication bound where it holds.

- Item 3 follows the decision in change 5.

### 10. The formal factors (lines 1600 to 1611)

Now: "The study then asks how the gain depends on three factors."

Proposed:

> The main factor is the controller, how many agents one decision of $\pi$ covers. Congestion
> sensitivity and load mark where the result holds.

Then the existing sentences on β and on load, adjusted to change 5.

### 11. Scope (around line 1632), depends on the relocation decision

If option 1 of the relocation discussion is taken (split inventory kept, the cap applied per
SKU, pickup in proportion to units), add one item to the scope list:

> \item[Shelves not matched to delivery points] A SKU held at several storage vertices serves
>   its orders in proportion to the units at each, whatever the order's delivery vertex. Keeping
>   stock near each delivery vertex is therefore not rewarded.

Reason: the thesis lists split inventory as something the state can represent (line 354), and
the reader should know what it does and does not buy in the experiments.

## Outside the Introduction, for when the above is applied

- `5.Experiments.tex`, `tab:expfactors`: mark the main factors, and drop or mark conditional the
  routing half of congestion sensitivity (change 5).
- `5.Experiments.tex`, "Mapping questions to comparisons": the same wording for RQ1 to RQ4.
- `5.Experiments.tex`, results opening: lead with the main result and `tab:exp:rq1`.
- `thesis-progress/archive/workspace/ROADMAP.md`: the commons question as part of RQ4, not RQ6.

## Decisions asked of the author

1. Apply changes 1, 3, 4, 6 and 9? (Recommended. They follow from the agreed main result.)
2. Change the main question (change 2), or keep it and let change 1 carry the focus?
3. RQ3 for storage only, or keep routing congestion sensitivity as a conditional part?
4. Commons question folded into RQ4, or kept as RQ6?
5. The relocation rule, option 1 or 2 (see the chat of 2026-10-18 and `short_run_2026-10-18.md`),
   which decides change 11.
