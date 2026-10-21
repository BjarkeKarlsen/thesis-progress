Agreed 2026-10-21, combined with `Appendixes.md` (one test per number no paper gives us). The structure is in `decisions/active/appendix_split_handoff.md`.

## Recommended structure

A good structure would be:

### Appendix A — Experimental overview

Explain:

- Which research question each experiment addresses.
- Which variables are changed.
- Which variables are kept fixed.
- Which metric produces each reported number.
- Which random seeds are used.

This gives the reader a map before the technical details.

### Appendix B — Storage and inventory

Include:

- Initial stock generation.
- Storage rules: fixed, demand-based, and congestion-aware.
- Stock reservations and physical inventory.
- Capacity checks.
- A worked example of a storage update.
- Tests proving that no shelf is over capacity.

This is especially important because the inventory semantics are currently being corrected.

### Appendix C — Warehouse and demand generation

Include:

- Graph-generation parameters.
- Number of vertices and edges.
- Storage, receiving, delivery, and endpoint generation.
- SKU popularity distribution.
- Demand drift.
- Order and quantity generation.
- Load-sweep procedure.

This appendix explains how the environments behind the experimental numbers were created.

### Appendix D — Controllers and reinforcement learning

Include:

- Centralised controller.
- Section-based controller.
- Decentralised controller.
- Observation spaces.
- GNN architecture.
- Action masks.
- Reward function.
- PPO parameters.
- Training budget and checkpoint selection.

This keeps all controller-related details together instead of scattering them across several appendices.

### Appendix E — Collision resolution and correctness

Include:

- The conflict-resolution algorithm.
- Vertex and swap-conflict handling.
- The corrected algorithm or pseudocode.
- Proof or explanation of why it is safe.
- Collision edge cases.
- Automated collision tests.

This should be a dedicated appendix because collision freedom is a **correctness requirement**, not merely an implementation detail.

### Appendix F — Metrics and statistical testing

Include:

- Exact definition of every reported metric.
- Service time.
- Order completion time.
- Throughput.
- Backlog.
- Crowding.
- Blocked time.
- Runtime.
- Keep-up criterion.
- Confidence intervals.
- Paired tests.
- Handling of unfinished tasks.
- Multiple-comparison correction, if used.

This appendix should allow a reader to reproduce every number in the results tables.

### Appendix G — Reproducibility and logged data

Include:

- Software versions.
- Hardware.
- Code commit.
- Configuration files.
- Random-seed policy.
- Training/evaluation split.
- Logged fields.
- Determinism checks.
- Output-file format.
- Mapping from log fields to result tables and figures.

This is where you explain how a value in the thesis was actually generated.

### Appendix H — Pilot experiments and calibration

Include:

- How load levels were selected.
- How the storage period was selected.
- How reward weights were selected.
- How demand drift was chosen.
- Preliminary experiments that motivated the final configuration.

Clearly label these as **pilot or calibration experiments**, not as evidence for the main research questions.

### Appendix I — Additional results

Include:

- Results not needed for the main argument.
- Full tables.
- Results for all seeds.
- Training curves.
- Backlog plots.
- Runtime measurements.
- Additional controller/storage combinations.
- Failed or discarded runs.

This keeps the main thesis readable while preserving transparency.

## Why this is better

This structure makes each appendix answer a different reader question:

| Reader question | Appendix |
|---|---|
| What experiment answers each research question? | A |
| How does storage work? | B |
| How were warehouse instances generated? | C |
| How were the controllers trained? | D |
| Why are the simulations collision-free? | E |
| How was each result calculated? | F |
| Can the experiment be reproduced? | G |
| Why were these parameters selected? | H |
| What additional evidence exists? | I |

The reader can therefore verify a particular result without searching through a single long appendix. For example, a reported storage improvement would lead to:

1. **Appendix A:** the research question and comparison.
2. **Appendix B:** the storage rule and inventory semantics.
3. **Appendix F:** the service-time calculation and statistical test.
4. **Appendix G:** the relevant logged data and reproducibility information.

## Separate files or one file?

For the submitted thesis, I would normally recommend:

- **One thesis PDF.**
- Separate appendix chapters labelled Appendix A, Appendix B, and so on.
- Optionally, a separate supplementary repository containing code, raw logs, configuration files, and large result tables.

A single long PDF is not automatically a problem. The problem is a long appendix that has weak navigation or mixes unrelated subjects. Separate appendix chapters solve that without creating many files that examiners must open individually.

Separate files are useful for material that is too large for the thesis:

- Full raw result tables.
- Complete logs.
- All generated warehouse graphs.
- Source code.
- Trained model checkpoints.
- Large parameter sweeps.
- Videos or animations.

These should be supplementary material, not normal thesis appendices.

## Important design rule

Organise the appendices by **verification purpose**, not only by the order in which the code is written.

For example, “`multi_agent_env.py` functions” is not a good appendix structure. Instead, group the material around questions such as:

- How is inventory represented?
- How are tasks generated?
- How are collisions prevented?
- How is service time measured?
- How can the reported numbers be reproduced?

This makes the thesis easier to evaluate scientifically.

## My recommendation for your thesis

Use the following final structure:

1. **Appendix A: Experimental map and research-question matrix**
2. **Appendix B: Storage, inventory, and capacity**
3. **Appendix C: Warehouse, order, and load generation**
4. **Appendix D: Controllers, observations, and PPO training**
5. **Appendix E: Collision resolution and correctness tests**
6. **Appendix F: Metrics and statistical analysis**
7. **Appendix G: Reproducibility, logging, and implementation checks**
8. **Appendix H: Pilot and calibration experiments**
9. **Appendix I: Complete additional results**

This is better than keeping the current long sequence of A–M if the current sections feel like independent technical notes. The current content can mostly be moved into this structure: for example, the existing notation, capacity, learning-problem, metric, parameter, logging, pilot, controller, and formal-definition sections can be reorganised under the broader research-purpose appendices. 

One final point: do not create an appendix for every small topic. A one-page subject should usually be combined with a related appendix. The goal is that each appendix has a clear purpose, enough content to justify its existence, and a direct connection to a method, result, or correctness claim.