You are right. I approached this as a completion checklist and kept adding details, rather than assessing whether the existing text earns its place. I also repeatedly treated the three work-in-progress sections as deficiencies after you had explicitly excluded them.

The correct first task is a structural and editorial review: identify repetition, assess whether the separation between chapters makes sense, and decide what to keep, condense, move, or remove. You review those proposals before another agent edits anything.

I will leave Results, Discussion and Future work out of this pass. I will also stop expanding the checklist with statistical reporting details such as 95% intervals.

# Status after checking against the text (2026-11-24)

Sections 3 and 4 below were checked against the current `2.Introduction.tex` and
`3.Background.tex`. Corrections to this checklist:

- **4.3, Deep Q-learning.** Do not remove. Related Work uses Deep Q-learning twice (van
  Knippenberg, Ma 2021), so Background keeps it as one sentence that defines it.
- **4.3, CTDE.** Remove from Background. The Method explains it with its citation where it
  is rejected (`4.Implementation.tex`, [A128]).
- **4.5, tragedy of the commons.** Keep (author, 2026-11-24). It returns in the Discussion.
- **3.1 to 3.3.** Confirmed. The design (three controllers, main and higher load) is told four
  times, in the Introduction, Aim and scope, the RQs and Expected outcome. The percentage-gain
  paragraph after the RQs is nearly word for word the one beside `eq:relgain` in the Problem
  Formulation. Agreed split: Introduction gives the problem, the coupling and one paragraph on
  what is compared. Aim and scope gives the factors and the scope. RQs give only the questions.
  Expected outcome gives only predictions.
- **New, 3.2.** The Introduction never mentions communication, yet RQ4 asks about it.
- **3.4.** The Contributions lead-in repeats the Problem Formulation opening and the research gap.
- **4.2.** Nothing after Background uses CBS, so it shrinks to one sentence.
- **4.4.** Nothing later cites Tien or Lischka, and the Tien link is broken.
- **4.6.** Cut the 47% (MAGAT). Keep 6.3% (size of a storage gain), 1024 agents (scale) and
  Pham's switch-off test (bears on RQ4 and the crowd reward).
- **3.5 and 4.1.** Already as proposed. Nothing to do.
- Sections 5 and 6 (Problem Formulation) applied as [A133] on 2026-11-25, with two follow-up rounds
  [A134] (design reasons to the Method) and [A135] (seams, figure sizes). Review PDFs v1 to v4 in
  `done/review_problem_formulation*.pdf`. The checklist is finished.

Applied as [A129] on 2026-11-24. Review PDF in `done/review_intro_background.pdf`. RQ4 reworded and scope paragraph cut, same tag.

# Structural Review for Your Approval

## 1. What the review should decide

For each passage, the question should be:

> Does this help the reader understand the research question, the model, the proposed method, or why a design choice matters?

The actions should be:

| Action | When it applies |
|---|---|
| Keep | The material contributes directly to the argument or prevents a consequential misunderstanding. |
| Condense | The point matters, but the explanation is longer than its value warrants. |
| Merge | Two passages perform substantially the same function. |
| Move | The content is useful, but appears in the wrong chapter. |
| Appendix | The content supports verification, derivation or reproduction without being necessary to follow the argument. |
| Remove | The passage adds neither a new idea nor useful clarification. |

An appendix should not become a dumping ground for repetition. Repeated explanations should normally be deleted; detailed evidence or worked derivations can be moved.

## 2. Overall assessment of the chapter separation

The broad separation between Background, Related Work, Problem Formulation and Method makes sense. The problem is that their responsibilities overlap within the text.

In particular, Chapter 5 contains not only the warehouse model, but also descriptions of the chosen storage heuristics, controller mechanisms, observation engineering, evaluation procedures and pilot justifications. That makes it harder to see where the problem ends and your solution begins.
### Proposed responsibility for each chapter

| Chapter | Its main responsibility | What should not dominate it |
|---|---|---|
| Introduction | Explain the problem, its importance and the thesis's central question. | Detailed experimental factors and metric explanations. |
| Project Description | State the research questions, scope, contributions and hypotheses. | Repeating the introduction's warehouse explanation. |
| Background | Explain the concepts required to understand the thesis. | Paper-by-paper comparisons or your implementation choices. |
| Related Work | Explain how existing approaches relate to your research gap. | Re-teaching the background concepts. |
| Problem Formulation | Define the warehouse, its entities, dynamics, constraints and objective. | Detailed descriptions of the particular algorithms being compared. |
| Method | Explain the storage rules, controllers and learning procedure you chose. | Reintroducing the warehouse model. |
| Implementation | Explain consequential implementation decisions and validation. | A catalogue of code modules or every logged field. |
| Experimental setup | Explain how the comparison is performed. | Repeating all model and method definitions. |

This is a proposal for clearer ownership, not a recommendation to add more chapters.

# 3. Introduction and Project Description

## 3.1 Introduction: merge the two congestion explanations

### What is repeated

The introduction first explains that popular stock near a workstation attracts traffic. The next paragraph gives almost the same example: placing popular stock near workstations produces short nominal trips but crowded aisles. Both paragraphs establish the same relationship between distance and congestion. 
### Proposed action: merge

- Keep the explanation that storage determines traffic and traffic changes effective access time.
- Incorporate the short-trip-versus-crowding example into that explanation.
- Remove the second full introduction of the same idea.

### Why

The example is useful, but the reader does not need the mechanism explained twice before reaching the thesis question.

### Instruction for the editing agent, after approval

> Merge the second and third introductory paragraphs into one paragraph. Preserve the two directions of influence and one concrete example. Do not add another warehouse example.

## 3.2 Introduction versus Section 2.1: assign different jobs

### What is repeated

Both sections explain the storage–routing relationship, the controller comparison, the congestion-aware extension and the load-based evaluation. Section 2.1 then explains much of the scoring logic as well. 
### Proposed action: keep the separation, reduce the overlap

Keep in the introduction:

- The practical problem.
- The reason separate storage and routing decisions may interact.
- A brief statement of what the thesis investigates.

Keep in Section 2.1:

- What is varied and what is held fixed.
- What falls inside and outside the study.
- The distinction between the main comparison and additional investigations.

Remove from Section 2.1:

- The elementary explanation of what an order and a pick task are.
- The extended account of how service time is split.
- The detailed explanation of why falling-behind runs use a different measure.

### Why

The separation is justified only if Chapter 2 becomes a research specification rather than a second introduction.

I would not merge the chapters automatically. First remove their duplication; then assess whether Chapter 2 still has enough distinct material to stand alone.

## 3.3 Research questions: keep questions separate from measurement details

The paragraph following RQ4 explains percentage gains and why absolute savings can favour a slower controller. That is an evaluation decision rather than part of the questions themselves. 
### Proposed action: move

- Keep the RQs together.
- Move the explanation of percentage gain to the evaluation protocol.
- Avoid explaining it again beside the formal gain equation.

### Why

Readers should be able to identify the research questions without passing through a justification of the measurement procedure.

## 3.4 Contributions: make them distinct rather than longer

The model and simulator contributions are related, while “results that answer each research question” describes an expected thesis output more than a specific contribution. 

### Proposed action: condense and distinguish

- Model contribution: what relationship or constraint the formulation captures.
- Method contribution: what the congestion-aware rule adds.
- Simulator contribution: what controlled comparison it enables.
- Empirical contribution: leave its final wording until the unfinished sections are ready.

### What should go

Remove generic lead-ins that merely say the thesis combines problems or produces results if the numbered contributions immediately say the same thing.

## 3.5 Expected outcome: preserve its prospective role

### Proposed action: keep

The expectations belong together as hypotheses. Do not add the eventual outcomes here, as I previously suggested.

### Why

Putting both predictions and outcomes in this section would blur its purpose and duplicate the later interpretation. The useful separation is:

- Here: what you expected and why.
- Later: what happened and how that changes the interpretation.

# 4. Background and Related Work

## 4.1 Keep these chapters separate

The existing distinction is useful: Chapter 3 explains SLAP, MAPF/MAPD, RL, GNNs and congestion, while Chapter 4 compares specific studies against your problem.

### Proposed action: keep the separation

However, move paper-specific application examples out of Background when their main purpose is positioning rather than explaining a concept.

## 4.2 Section 3.2: shorten material that does not support later choices

The section covers centralised search, decoupled search, CBS, prioritised planning, MAPD and well-formedness. 

### Proposed action

- Keep MAPF and MAPD definitions.
- Keep vertex and swap conflicts at a conceptual level.
- Keep prioritised planning because it helps explain later controller choices.
- Keep well-formedness because it matters to the Token Passing reference.
- Condense the CBS explanation if the method is not subsequently used.

### Why

The reader needs the concepts that explain your choices, not a miniature survey of MAPF solvers.

### What should not move to an appendix

Do not move the essential MAPD and well-formedness explanations out of the main text. They support the interpretation of the reference method.

## 4.3 Section 3.3: remove side explanations without a later role

The section includes the aside that not every RL method has a critic, using deep Q-learning as an example. It also introduces parameter sharing, CTDE and sequential action selection. 
### Proposed action

- Keep Deep Q-learning as one defining sentence, because Related Work uses it twice. Drop the "not every method has a critic" framing.
- Keep the actor–critic explanation needed for PPO.
- Keep parameter sharing.
- Keep reward shaping, but avoid explaining the same shaping rationale again at full length in Method.
- Remove CTDE from Background. The Method explains it where it is rejected ([A128]).
- Put sequential action selection with the controller explanation if it interrupts the RL foundations.

### Why

A concept belongs here because the reader needs it, not merely because it is related to RL.

My previous suggestion to add a PPO objective automatically was not justified. Add it only if the later methodological argument actually uses it.

## 4.4 Section 3.4: move application examples to Related Work

The final paragraph discusses GNN applications to vehicle routing and edge-based routing problems. 
### Proposed action: move or remove

- Move those papers to Related Work if they directly inform your architectural choice.
- Otherwise remove them.
- Keep the conceptual distinction between graphs over places and graphs over agents.

### Why

That distinction helps readers understand your system. Additional routing applications do not necessarily do so.

## 4.5 Section 3.5: remove the broad analogy unless it does analytical work

The congestion section introduces the tragedy of the commons before returning to warehouse coordination. 

### Decision: keep (author, 2026-11-24), because it returns in the Discussion

### Original proposal: remove or reduce to one sentence

Keep:

- Shared-resource contention.
- The distinction between occupancy and costly delay.
- Why individually reasonable decisions can create poor joint behaviour.

### Why

Those mechanisms explain the thesis directly. The broader analogy adds another conceptual frame without clearly changing the model or method.

## 4.6 Related Work: reduce isolated benchmark numbers

Sections 4.1–4.4 include several reported performance percentages and scale figures from other papers.
### Proposed action: selectively condense

Retain a number when it establishes something relevant, such as demonstrated scale or the effect of communication.

Remove a number when:

- Its benchmark differs substantially from yours.
- It is not used in a later comparison.
- The reader needs the methodological difference, not the score.

### Why

A sequence of percentages can look informative while contributing little to your positioning.

### Preferred paragraph structure

For each relevant study:

1. What decision does it solve?
2. What information does it use?
3. What is fixed?
4. How does that differ from this thesis?

A comparison table is optional—not automatically another required addition.

# 5. Problem Formulation: the Main Restructuring Target

## 5.1 Keep the chapter, but narrow its responsibility

The chapter's central value is the shared model: stock, orders, tasks and robot movements affect one another. That should remain in the main text. The repeated algorithm descriptions and elementary worked calculations are better candidates for reduction. 
## 5.2 Section 5.1: retain the environment, reduce repeated background

### Proposed action

Keep:

- Directed graph and special vertex sets.
- Time and movement assumptions.
- Shortest-path distance.
- The relevant connectivity and endpoint requirements.

Condense:

- Repeated explanations that a vertex is somewhere an agent stands.
- Repeated references back to the full title of the Background section.

Appendix:

- Detailed generator construction.
- Verification or derivation of the generated layouts' properties.

### Why

Readers need the warehouse abstraction, but not another full introduction to graph-based MAPF.

## 5.3 Section 5.2: distinguish constraints from enforcement

The collision constraints and the explanation of conflict resolution currently appear together. 
### Proposed action

Keep here:

- Legal moves.
- Vertex and swap constraints.
- A short statement that execution enforces those constraints.

Move to Method:

- How intended moves are changed.
- Priority handling.
- Which agent yields.
- Cascading consequences of rejected moves.

### Why

“No collision is allowed” defines the problem. “This procedure prevents collisions” defines a solution mechanism.

Figure 5.2 can remain if it makes the two constraints easier to understand. If it remains, shorten the surrounding explanation rather than repeating its caption in prose.

## 5.4 Section 5.3: split stock dynamics from storage policies

This section mixes inventory definitions, replenishment, specific storage rules, policy inputs and a pilot justification. 

### Proposed action

Keep in Problem Formulation:

- Stock quantities.
- Shelf capacity.
- In-transit stock and reserved capacity.
- Replenishment dynamics.
- Whether existing stock may relocate.
- What happens to unplaced pallets.

Move to Method:

- The three particular storage rules.
- Their ranking logic.
- Demand and congestion estimators where they are algorithmic choices.
- The choice not to learn storage.

Move to an appendix:

- The detailed pilot comparison supporting arrival-only placement.
- The matrix arithmetic demonstrating shelf capacity.
- The extended storage-update calculation.

### Why

The reader must understand what stock can do. They do not need all arithmetic examples to understand that model.

### Important distinction

Keep the fact that unplaced pallets are lost. That is not low-value implementation detail: it changes the simulated system's behaviour.

## 5.5 Figures and examples in Sections 5.3–5.5: keep those that reveal interactions

### Proposed decisions

| Item | Proposed action | Reason |
|---|---|---|
| Table 5.1 and capacity matrix calculation | Appendix | Illustrates basic capacity arithmetic rather than the coupling. |
| Figure 5.3: incoming stock under fixed and demand storage | Keep, relocate with storage-rule explanation | Shows the important distinction between placement of arrivals and relocation. |
| Figure 5.4: one storage update | Appendix | Adds less conceptual value once capacity and placement are defined. |
| Figure 5.5: one agent's task route | Candidate for removal or appendix | A pickup-to-delivery route may already be clear from the task definition. |
| Figure 5.6: splitting one line across shelves | Keep | Explains how storage changes task generation. |
| Figure 5.7: task lifecycle | Keep | Clarifies the consequential distinction between release, assignment and completion. |

These decisions concern the explanatory functions indicated by the text and captions, not a visual-quality assessment of the figures. 
## 5.6 Section 5.4: separate task generation from the chosen pickup heuristic

### Proposed action

Keep:

- Orders and order lines.
- The three task types.
- Stock reservation.
- Partial fulfilment and stockouts.
- Shipment dependency on all order lines arriving.

Move to Method:

- Nearest-shelf ordering.
- Congestion-adjusted shelf ordering.
- The detailed greedy allocation procedure.

### Why

The fact that one line can create multiple tasks is part of the model. The ranking used to choose those shelves is a method choice.

### Table 5.3

Move it beside the storage-rule definitions in Method. It is a useful summary, but keeping it far from the full algorithm explanation creates another place where the same distinction must be retold.

## 5.7 Section 5.5: keep the lifecycle, cut the arithmetic repetition

The lifecycle section gives definitions, a timeline, the task-time equation and the numerical subtraction for the running example. 

### Proposed action

- Keep the stages and timestamps.
- Keep the timeline.
- Keep the service-time definition.
- Remove the explicit subtraction example.
- Condense repeated explanations of when an agent is busy or free.

### Why

The timeline explains the non-obvious distinction. The arithmetic does not add another insight.

## 5.8 Section 5.6: move most controller design to Method

### Proposed action

Keep in Problem Formulation:

- Assignment and routing as distinct decisions.
- The admissible information available under each control setting, if these define the comparison.

Move to Method:

- Sequential action generation.
- Priority order.
- Reservations and masks.
- Controller-specific credit.
- The detailed centralised, section-based and decentralised implementations.

Keep one comparison table at the start of the controller method section.

### Why

The chapter currently describes not merely what a controller must decide but how your controllers choose actions. That is the main source of overlap with Sections 6.3–6.4.
## 5.9 Section 5.7: move observation engineering alongside the policy

### Proposed action

Move to Method:

- Field-of-view construction.
- Target-distance features.
- Crowding feature.
- Communication graph and learned messages.

Keep any general information restrictions in Problem Formulation.

### Further reduction

- Merge 5.7.5 into the section introduction or conclusion; a standalone subsection for assembling the observation tuple is unnecessary.
- Keep one integrated observation example.
- Move the separate crowding arithmetic example to an appendix or remove it.
- Move idle-agent relocation behaviour out of the target-feature explanation and into the method's execution rules.

### Why

This places the input features next to the network that consumes them, rather than making the reader reconstruct that connection across chapters. 

## 5.10 Section 5.8: condense the game formulation

This section defines the stochastic game, provides a component table, explains policy versus transition kernel, and revisits the controller observations. 

### Proposed action

Keep:

- A compact formal formulation.
- The essential state, action and transition definitions.
- The learning objective.

Condense or remove:

- The lengthy explanation that a transition kernel is a rule rather than a state.
- The illustrative action-probability example.
- Repeated descriptions of what the three controllers see.
- Either the component table or the prose inventory where they say the same thing.

Appendix:

- Extended formal elaboration that is not used subsequently.

### Why

The formalism should expose an assumption or support the method. It should not require several pages merely to rename concepts already established.

## 5.11 Section 5.9: preserve the coupling, eliminate its repeated narration

The forward and backward paths are already explained in the introduction and earlier Chapter 5 sections. Nevertheless, bringing the complete loop together is useful. 

### Proposed action

Keep:

- One compact synthesis of the two timescales.
- One clear account of what information passes in each direction.
- Figure 5.11 if it is the clearest demonstration of the feedback loop.

Remove:

- Another full explanation of what fixed and demand storage do.
- Repeated statements that demand storage only creates one-way coupling.

Move:

- Storage-period calibration and sweep justification to Method or its supporting appendix.

### Why

This should be the point where the model comes together, not another introduction to its parts.

## 5.12 Section 5.10: split the objective from the evaluation procedure

My earlier recommendation to move all of 5.10 was too blunt.

### Keep in Problem Formulation

- The primary system objective.
- The fact that keeping up matters.
- The distinction between order-level performance and task-level diagnostics.
- A compact formal statement of the decision problem, if useful later.

### Move to experimental setup

- Measurement windows.
- Operational keep-up test.
- Paired comparison procedure.
- Percentage-gain calculation.
- Reporting conventions.

### Move to appendix or condense

- Elementary averaging examples.
- Detailed accounting illustrations.
- Repeated explanations of why unfinished work matters.

### Why

The model needs an objective. The experiment needs a measurement protocol. Those are related, but not identical.

## 5.13 Section 5.11: separate assumptions from proposed extensions

### Proposed action

Keep:

- What is not modelled.
- Assumptions that affect interpretation.

Remove or move:

- Instructions describing how deadlines or reassignment could be added.
- The conditional statement about whether RQ4 will be reached.
- Repeated explanations of assumptions already defined elsewhere.

### Why

A scope section should state the study's boundary. It should not become an early future-work section.

# 6. Concrete Inconsistencies That Matter More Than Extra Detail

These should be reviewed before an editing agent restructures the text.

## 6.1 “Only the observation changes” is too narrow

Section 5.6 says the controllers differ in visibility, prior action information and whose rewards judge actions. Section 5.8 then says only the observation changes. Those descriptions do not communicate the same comparison. 
### Proposed correction

Choose one consistent account:

> The controllers share the warehouse dynamics and base components, but differ in information scope, action coordination and reward aggregation.

The final wording must match the actual implementation.

## 6.2 Assignment appears both inside the controller and outside it

Section 5.6 defines the controller as assignment plus routing. Section 5.8 places the shared assignment rule in the transition kernel and says it is not part of any policy. 
### Proposed correction

Distinguish:

- The full warehouse controller.
- The learned routing policy.
- The fixed assignment mechanism.

Then use those terms consistently. Moving a passage alone will not resolve this conceptual mismatch.

## 6.3 Arrival placement versus pickup selection

Section 5.3 says a storage rule decides where arriving stock goes “and nothing else,” but the congestion-aware condition also changes which shelf supplies an order line. 
### Proposed correction

Either:

- Define the experimental condition as a storage-and-pickup policy; or
- Define placement and pickup selection as separate components.

This distinction belongs in the main text because it changes what the comparison means.

# 7. What I Withdraw From the Earlier Checklist

The following should not be automatic requirements:

- Adding more confidence-interval detail.
- Requiring new training runs as part of an editorial pass.
- Rewriting RQs to accommodate unfinished findings.
- Adding hardware commands or a code-module catalogue.
- Adding a PPO equation merely because PPO is used.
- Adding more numerical examples.
- Calling the architecture or reward table missing without checking the existing figures and Table 6.1.
- Adding “human imperfections” or first-person passages to make the writing appear less AI-generated.

The document already lists architecture-related figures and a reward table. The right question is whether they explain the method adequately—not whether another table can be added. 

# 8. Handoff to the Editing Agent

No changes should be made until you have reviewed the proposals.

For each approved item, the handoff should contain:

```markdown
## Change ID
S-01

## Location
Chapter and section; opening words of the relevant passage.

## Proposed action
Keep / Condense / Merge / Move / Appendix / Remove

## Problem
What is repeated, misplaced, unclear, or unnecessary?

## Reader value
What does the reader need to retain, and why?

## Edit boundary
What must not change?

## Destination
Exact destination for moved material.

## Acceptance check
How to verify the edit preserves the meaning.

## User decision
Pending / Approved / Rejected / Revise proposal
```

For the first editing pass, I would prioritise three decisions: the boundary between Chapters 5 and 6, the overlap between Chapters 1 and 2, and which worked examples genuinely explain the coupling. Those changes address the reading experience before adding anything else.