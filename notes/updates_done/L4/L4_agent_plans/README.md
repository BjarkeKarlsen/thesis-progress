# L4 agent plans

One plan per package for subagents, written from `../L4_design.md` on 2026-10-13. Start every agent with
`00_rules.md`. Each plan names its branch, what it starts from, what to read, what to change, the tests to write and
what to hand back. The author runs the checks and opens the PR.

## Order and parallelism

```
B1 zones             ─┐
B2 window            ─┼─> B3 pooling ─┐
                                       │
A1 stage timing ─> A2 assigner, one step mode, driver ─> A3 reward ─> A4 adapter ─> A5 policy ─> A6 examples
                                       (A4 starts from A3 and brings in B1, B2 and B3)
```

- B1 and B2 start now, in parallel. B3 starts from the B2 branch.
- Track A is one branch, `fix/one-env-adapter`, and one agent per package in order, because every package edits
  `environment/multi_agent_env.py` or its callers. Start each agent from the previous agent's worktree or branch.
- A1 to A3 can start at once, in parallel with B1 to B3, since they do not need them. A4 waits for B1, B2, B3 and A3.
- The PR is one PR from `fix/one-env-adapter`. B1 to B3 are cherry-picked into it as the first commits of A4, or the
  author may open them as small PRs first.

## Why the order differs from `../L4_design.md`

The design listed the stage move, then the `Assigner`, then the single step mode. That order leaves the self-assigning
router broken after the stage move, because the first assignment would run in `reset` before the router exists. A1
therefore resolves the planner router eagerly (a temporary step) and A2 replaces it with the `Assigner` argument. A2 also
keeps a temporary controller driver so evaluation of the existing controllers works until A5 deletes it.

## Tags and reviewers

| Package | Tag | Notes |
|---|---|---|
| B1 | [simple] | A Sonnet class model can do it from the plan |
| B2, B3 | [review] | An Opus session or the author checks the branch against the thesis |
| A1 to A6 | [review] | A1 to A3 touch simulator behaviour and must keep the golden comparison identical |

## Checks that cross packages

- Golden comparison (`00_rules.md`) after A1, A2, A3 and A5, and after any change to `environment/` or `evaluation/`.
- The author runs `pytest`, `black`, `flake8` and `mypy` at each handed-back commit. Agents do not.

## Open questions that block a package

- Global pooling is decided (each arm pools over its own space, section over the zone only). The thesis rows are the
  author's to edit.
- Gap issues (zone rule, the two encoder sentences, pooling rows) are not opened. The author has not said yes.
- Decision 17 (sample or most likely action in evaluation) stays open and is not touched.
