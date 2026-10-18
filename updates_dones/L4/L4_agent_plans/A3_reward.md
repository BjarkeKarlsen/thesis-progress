# A3. The reward for every arm [review]

Branch `fix/one-env-adapter`, continuing after A2. Read `00_rules.md` first, then the golden comparison section.

## Goal

All three arms learn and share the reward, so the simulator must compute it for every learned arm, with the congestion
term included. Today `ExperimentConfig._controller_parameters` requires the four reward weights only for
`controller="decentralised"`, `_compute_rewards` returns zero for every other controller
(`multi_agent_env.py:470`), and the congestion term is the constant `0.0` (`multi_agent_env.py:499`).

Thesis to read: `sec:method:rl` (the reward and its congestion term), `sec:pf:controllers` (the congestion feature),
`sec:method:training` (credit signal, which this package does not touch).

## Changes

1. `core/experiment_config.py`. Require the four reward weights and the discount for any set `controller`. A config
   with a `planner` keeps them optional. Keep the rule that communication applies to the decentralised arm only.
2. `environment/multi_agent_env.py`.
   - Compute the congestion feature of every robot once per timestep, on the field of view with the existing helper,
     in the place `_record_crowding` runs. Store it as the current `congestion_by_agent` mapping, log the sum for the
     crowding measure as before, and pass each robot's value to the reward. The reward uses the value at the step the
     action was chosen in. With A1 the mapping for the new `t` is computed at the end of the step and in `reset`, under
     the same skip at the episode end as the assignment, so the log keeps exactly `horizon` entries and the same values.
   - Remove the early return for non-decentralised controllers. A planner config returns zero rewards.
   - Expose `congestion_by_agent` as a read-only property so the adapter (package A4) can reuse it.
3. Docstrings. Drop the statements that only the decentralised arm has a reward.

## Tests

- The reward has a non-zero congestion term on a crowded fixture and equals the reward without it when the weight is
  zero.
- Configs for centralised and section arms without weights are rejected. Planner configs without weights are accepted
  and give zero rewards.
- Each arm gets a non-zero reward on a fixture where a robot delivers.
- `congestion_by_agent` equals the observation builder's value for the same state.

## Done when

The golden comparison shows identical metrics (`mean_crowding` must not move), and the trace is classified as before.
