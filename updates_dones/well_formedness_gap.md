# Gap: what the thesis claims well-formedness guarantees

Found 2026-10-13 while implementing Token Passing (B18, branch
`fix/token-passing-planner`). For the author to decide. Belongs with B19 (the
thesis edits) and with `endpoint_count_gap.md`, which covers only the endpoint count.
The well-formedness paragraph is in `2.Introduction.tex`, near line 289.

## 1. The thesis lists two conditions, the paper has three (decided: keep two)

Ma et al. (2017), Definition 1, call an instance well-formed if

- a) the number of tasks is finite,
- b) there are no fewer non-task endpoints than agents,
- c) for any two endpoints there is a path between them that traverses no other
  endpoint.

The thesis lists b) and c). **Decision (author, 2026-10-13): condition a) is not
needed in the thesis.** It is a property of the order stream and not of the instance,
and the paragraph is about instance properties.

The one point that stays is the wording of the guarantee. The paper says its algorithms
solve well-formed instances "even though they might not execute all tasks in case the
number of tasks is infinite". As I read it, the guarantee is no deadlock and that any
finite set of tasks gets done. It says nothing about whether the backlog empties under an
unbounded stream, and the measured backlog and keep-up ratio are about exactly that. So
the thesis should say "no deadlock", not "the backlog empties".

## 2. The guarantee is for the paper's collision model and task rule, not this environment

Three things the guarantee depends on differ here.

- **Collisions.** The paper forbids two agents on one vertex and two agents swapping.
  Agents may follow each other in a line. Here, conflict resolution is stricter. It
  also blocks an agent entering a vertex in the step another leaves it when the
  leaving agent has the lower priority (`sec:method:resolution`).
- **Task rule.** The proof needs the agent to choose a task only among those whose pickup
  and delivery vertices are not the end of another agent's path. The shared assignment
  does not do this, so the guarantee does not apply to a run that uses it. This is why
  the Token Passing planner picks its own tasks.
- **Starting positions.** The proof needs each agent to start on an endpoint. The
  environment places agents on V_ep vertices, so this holds.

My reasoning, not a proof, is that Token Passing still keeps its guarantee here. Its
plans take a vertex one step before and after another agent is on it, so conflict
resolution never overrides them, and the paper's argument has a new agent move after
the others have settled, which the extra padding does not change. The tests show zero
overrides on the example 04 instance, a hand-built dead-end corridor and generated
instances, but they do not prove it.

The thesis sentence "Token Passing and the centralised MAPD baseline ... are only
guaranteed to avoid deadlock" therefore needs the task rule and the collision model
named, and the prioritised A* planner is neither of the two baselines it mentions.
The prioritised planner has no guarantee here at all, and on the example 04 instance it
completes 12 tasks in 2000 steps with 3889 overridden steps, where Token Passing
completes 614 with none.

## 3. Required as an assumption, but sufficient and not necessary in the paper

**Decision (author, 2026-10-13): well-formedness is necessary.** That holds as an
assumption of the thesis. Every generated instance has to be well-formed, so the baseline
has its guarantee and every controller is compared on the same kind of graph, and the
thesis already says this.

The paper's own wording is that it is "a sufficient condition that makes MAPD instances
solvable". It does not say that every solvable instance is well-formed. So the thesis
text should not call it necessary for solvability, and "only guaranteed on well-formed
instances" is accurate where "needs a well-formed instance to work" goes further than the
paper.

## Why the code cannot resolve it

All three are statements about what the model and the baseline guarantee, so they belong
in the thesis. The code already enforces b) and c) in `instances/validation.py`, places agents
on endpoints, and passes the tests above. Nothing in the code would change.

## Decisions

1. Done: condition a) stays out. Word the guarantee as no deadlock.
2. Done 2026-10-13, see `GAPS.md` [A28]: name the task rule and the collision model that the guarantee needs, and say that
   Token Passing, not the shared assignment or prioritised A*, is the baseline that has it.
3. Done: well-formedness is required of every instance. Avoid saying it is necessary for
   solvability.

After the decision, log it in `GAPS.md` and tag the changed text with `% [Axx]`.
