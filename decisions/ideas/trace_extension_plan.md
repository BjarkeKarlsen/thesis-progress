# Trace extension plan, 2026-10-16

Local note at the workspace root. It describes what the episode trace records today, what is missing for
finding out where a task goes wrong, and one small change that adds it. Nothing here is implemented yet.
The trace code is `slap-mapd-coupling/src/slap_mapd_coupling/evaluation/trace.py`.

## Why

The first campaign showed that the learned fleets finish about 0.21 tasks per step however fast tasks
arrive, while Token Passing finishes 0.27. Each task costs a learned agent about 4 steps more than it costs
Token Passing (see `campaign_findings_2026-10-16.md`). To see where those steps go, one task at a time, we
need to know for every task when it was released, when it was given to an agent, which agent, when the
pickup happened and when it finished. The current trace does not say this.

## What the trace holds today

One JSON line per timestep, after a header line.

- Header. The configuration, the vertices with their roles, the edges with their costs, and where each agent starts.
- Per step. The step number, tasks completed so far, tasks released so far, the backlog (a count), and for every agent:
  where it is, the move it wanted, whether it moved, whether conflict resolution overrode it, the task it was
  serving, the phase (to pickup or to delivery) and the goal vertex.

So the task an agent is serving at each step is already there. That covers "which agent has which active task"
as long as the task is active.

## What is missing

1. **Waiting tasks.** Only their count is logged. Which tasks are waiting, and since when, is not.
2. **Release time and assignment time per task.** They can only be guessed from the step where a task first
   appears on an agent. The release time cannot be recovered at all.
3. **The pickup and delivery vertices of a task that never got an agent.** A task still waiting at the horizon
   leaves no trace of its existence beyond the count.
4. **The SKU of the task.** Needed once adaptive storage moves units between vertices.

All four are fields the simulator already holds. A `Task` has `release_time`, `assignment_time`,
`pickup_time`, `finish_time`, `assigned_agent`, `pickup_vertex`, `delivery_vertex` and `sku`.

## Proposal

Write one extra line at the end of the file, after the last step, that lists every task with the fields above.

```
{"type":"tasks","tasks":[{"id":1,"released":3,"assigned":3,"agent":2,"pickup_at":9,"finished":21,
  "from":39,"to":24,"sku":"tea"}, ...]}
```

A field that never happened is `null`. The pickup and finish steps are the ones the task stores, so they are
defined as in the thesis (`t_j^pickup`, `t_j^finish`).

Why a line at the end and not a list in every step.
- It is complete. A per-step queue list repeats the same task many times.
- It is small. A 630 step episode has 100 to 190 tasks, about 120 bytes each. That is roughly 20 KB on top of
  the 240 KB trace that exists now, about 8%.
- A step line stays as it is, so nothing that reads steps needs to change.

What per-step state can still be read. At any step t, a task is waiting if `released <= t < assigned`, active
if `assigned <= t < finished`, and the agent holding it is `agent`. So the waiting list and the holder of each
active task at every step follow from this one line.

## Format and compatibility

The writer would set `TRACE_FORMAT = 2`. `load_trace` currently returns every line after the header as a step,
and it rejects any format other than the current one. Two changes.

- `load_trace` returns the steps only (lines with `"type": "step"`), and a new `load_tasks` returns the task line,
  or None for a trace without one.
- It accepts format 1 and 2. A format 1 file has no task line, and everything that works on steps keeps working.

The 120 existing campaign traces are format 1. They stay readable. They have no task line, so the per task view
for them is limited to what the steps give (the leg tool works from the steps alone, see below).

## What it enables

- Waiting for an agent per task (assigned minus released), not only as a mean over tasks. The mean is in the sweep
  already. The spread and the tail are not.
- A check that the assignment rule gave a task to an agent that was free, and how far the agent was from the pickup.
- Tasks left at the horizon, with how long they had waited.
- With adaptive storage, which SKU each task asked for and where the pickup vertex was when it was released.

## Tests

- A trace of a short episode has the task line last, and its counts match the step lines (completed and released at the end).
- Every task with `finished` set has `assigned <= pickup <= finished`.
- `load_trace` reads a format 1 file and a format 2 file, and the steps are identical for the same episode.
- Writing the task line does not change the run metrics. The existing test of that stays.
- A run with no task released still ends with a task line with an empty list.

## Open questions

- Whether the planner trace (Token Passing) should carry the same line. It should, since the planner runs
  through the same environment and the writer only reads it.
- Whether to also log the agents that were free and had no task each step. That is already visible as
  `"task": null`.

## Order of work

This is the first of three pieces, written up before any code. The second is the memory note
(`memory_reduction_plan.md`). The third is the leg tool, which works on the steps of today's traces and
uses the task line when a trace has one.
