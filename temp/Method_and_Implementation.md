# From Problem Formulation to Method and Implementation
## The contract that makes the next sections writable
The single most useful decision at this stage is to fix an explicit division of labour between three sections and then enforce it mechanically. Without it, the Method chapter re-derives things already in Section IV and the reader loses track of what is settled.

| Section | Answers | Contains | Never contains |
|---|---|---|---|
| IV Problem formulation | *What* the objects are | Sets, constraints, metrics, the coupling condition, the objective as a framing device | Algorithms, network layers, hyperparameters, heuristics, resolution rules |
| V Method | *How* each open component is realised | Storage heuristics, controller algorithms, RL formulation (observation features, mask, reward), architecture, training procedure | Code structure, logging, runtime, seeds, test suites |
| VI Implementation | *How* it is built and verified | Simulator modules, instance generator, instrumentation, computational cost, correctness checks | New modelling decisions |

The mechanical enforcement is a rule: **Section V may only refer to Section IV by equation number, never restate a definition**. If a Method paragraph needs to define something, that object either belongs in Section IV or was never a problem-level object at all. Applying this rule is also the fastest way to detect the misplaced material discussed below.

A complete drop-in skeleton for both sections is provided, structured exactly this way, with `\label`/`\ref` cross-references back into Section IV, two new figures, and parameter tables holding the TBD values you will fill after the first runs.
## What is too detailed in the Problem Formulation
Six items in the current Section IV are *choices*, not *definitions*, and each should move forward. The test in every case is the same: could a different thesis, attacking the same problem, make the opposite choice and still be attacking the same problem? If yes, it is Method.

**The three controller architectures (subsection E).** Centralised, section-based and decentralised are *the experimental treatments*. The problem formulation needs only the abstract signature of a controller — a map from information to assignment plus routing — plus the statement that architectures differ in what information they may condition on. Everything about prioritised planning, matching costs, zone hand-off protocols and boundary priority belongs in Section V. This is the largest single cut available and it removes roughly a page of the hardest reading.

**The encoder and message-passing equations (subsection F).** The two-stage encoder \(z_i = \mathrm{Enc}_G(\mathcal{G}^{(d)}_i)\) followed by \(Q\) rounds of \(\phi_q, \psi_q\) is a model, not a problem. What Section IV must define is the observation \(o_i(t)\) — the induced subgraph, the potential \(\eta_i\), and the communication graph \(G^{\mathcal{A}}_t\) — because those specify *what an agent is allowed to know*, which is a property of the problem. How that information is embedded is Section V, and it is precisely where the architecture figure belongs.

**The exact form of the storage objective's three terms.** Keep the statement that \(x_t\) is chosen from \(\mathcal{X}\) to trade off access distance, congestion exposure and reassignment cost. Move the specific functional forms of \(D\), \(K\), \(R\) and the weights \(\alpha, \beta, \chi\) to Section V, where they can sit next to the greedy heuristic that actually optimises them and the sweep table for the weights. As it stands the reader meets a weighted scalarisation before knowing that no exact solver will be used.

**The reward function, if present in Section IV.** The reward is not part of the problem — the objective functional \(\mathcal{J}\) is. The reward is an instrument for getting a policy to do well on \(\mathcal{J}\), and it can be redesigned without changing the problem at all. It belongs in the RL formulation subsection of Section V.

**The justification passages.** The defences flagged in the previous rewrite ("this definition avoids applying the edge-cost function to a wait transition", "a collision penalty alone does not establish collision freedom", "it is clearer to define this baseline directly than to use the informal value \(\Delta = \infty\)") each have a natural new home. The first stays as a one-line footnote. The second becomes the *motivation for action masking* in Section V and reads far better there, because the sentence that follows it can be the solution rather than an apology. The third becomes one line in the storage-rules subsection introducing \(F_{\mathrm{fix}}\).

**The full notation table.** Keep it, but move it to an appendix and leave only the symbols used more than twice in the running text. A reader who must consult a table on first reading is reading a reference manual.

Two things that look like candidates for removal should **stay** in Section IV. The conflict constraints are genuine problem-level definitions — they say what a valid solution *is* — even though the enforcement mechanism is Method. And the coupling condition \(x_{r_j}(k_j, s_j) > 0\) must stay and should be the most prominent equation in the chapter, since it is the formal statement of the thesis contribution.
## What is missing from the Problem Formulation
Cutting is only half the adjustment. Three additions make Section IV a better launchpad.

- **A one-paragraph "scope and assumptions" close.** State plainly what the model does not represent: unit-capacity robots, no battery, no kinematics, no human pickers, deterministic execution. Examiners look for this, and stating it in Section IV prevents each Method subsection from apologising individually.
- **An explicit information-availability table.** One small table with rows "assignment sees / routing sees" and columns for the three architectures makes the experimental design legible before any algorithm is described, and it is the natural anchor for the controller signature that replaces subsection E.
- **A named, numbered statement of the research question in formal terms.** Something of the form: does there exist \(F\) such that \(\mathcal{J}(F, \pi_\theta) < \mathcal{J}(F_{\mathrm{fix}}, \pi_\theta)\) by a margin exceeding seed variance, and is the improvement larger for \(\pi_\theta\) than for \(\pi_{\mathrm{cen}}\)? Section V then has an obvious job: realise each symbol in that statement.
## Structuring the Method chapter
The skeleton uses seven subsections, ordered so each depends only on its predecessors.

**V.A Overview.** One paragraph plus the environment-step figure. Its job is to show that all three controllers plug into the same six-stage loop, which is what makes the comparison matched. Readers who stop here should still know the shape of the system.

**V.B Storage update rule.** Three named rules — \(F_{\mathrm{fix}}\) (identity baseline), \(F_{\mathrm{dem}}\) (demand-only greedy, the classical slotting heuristic), \(F_{\mathrm{cng}}\) (congestion-aware). Naming them as a ladder is worth more than any single sophisticated rule, because the difference between \(F_{\mathrm{dem}}\) and \(F_{\mathrm{cng}}\) isolates exactly the contribution: the value of *traffic* information over *demand* information. Note the reassignment penalty is implemented as a hard cap of \(\nu\) changes per epoch, which realises \(R\) without adding another weight to tune.

**V.C Controller realisations.** The three architectures, moved here from Section IV. The critical design note: keep task assignment identical across all three, and learn only routing. Otherwise a difference in results cannot be attributed to the architecture, because assignment quality is confounded with it.

**V.D Reinforcement-learning formulation.** Four fixed components — observation features, action space with masking, reward, objective.

The reward deserves care. Write the progress term strictly as \(\gamma\Phi_i(t+1) - \Phi_i(t)\) with \(\Phi_i(t) = -\eta_i(\ell_i(t), t)\). Potential-based shaping of this form does not alter the Nash equilibria of the underlying stochastic game, and the guarantee extends to dynamic potentials that change over time — which matters directly here, because \(q_i(t)\) changes at every reassignment, making \(\Phi_i\) non-stationary by construction. A naive "reward for decreasing distance" term lacks this guarantee and admits policies that loiter near the goal to farm shaping reward. This is a two-sentence justification in the thesis that buys a real theoretical claim.[^1][^2][^3]

Action masking should be presented as the mechanism that makes collision freedom hold *by construction* rather than in expectation: pad the action head to \(d_{\max} = \max_v |N^{+}(v)|\), set infeasible logits to \(-\infty\) before the softmax. Note that RLlib's new API stack does not ship action masking as a built-in and it must be implemented in a custom module or connector[^4], so budget time for it.

**V.E Model architecture.** The encoder equations moved from Section IV, plus the figure. State that the no-communication ablation is \(Q = 0\) — a one-line change that isolates the value of communication.

**V.F Conflict resolution operator.** Masking makes each individual action legal; it does not make the joint action legal. A deterministic operator with a per-episode fixed priority permutation resolves the remainder and flags overridden agents so the feasibility penalty applies. Determinism here is not fussiness — it is what makes paired seed comparisons valid.

**V.G Training procedure.** PPO with full parameter sharing across homogeneous agents is the standard scaling lever and is a few lines of configuration in RLlib's multi-agent API, mapping every agent to one shared policy. State the disjoint train/eval seed split, and state whether training happens under fixed or adaptive storage — training under adaptive storage makes the task distribution non-stationary from the learner's perspective, which is a genuine experimental variable, not a detail.[^5][^6]
## Structuring the Implementation chapter
Five subsections, all of which answer questions an examiner will ask.

**VI.A Simulator.** Precompute all-pairs shortest paths once per instance — the graph is static and \(d_G\) is queried by both the observation builder and the storage rule at every step. Keep task generation, assignment, routing, resolution and logging as separate modules with explicit interfaces, which is what allows a controller swap without touching the environment. The parallel multi-agent convention, where all agents act simultaneously and results are returned as dictionaries keyed by agent ID, matches the partially observable stochastic game formalism directly, and RLlib's `MultiAgentEnv` follows the same dictionary-keyed convention.[^7][^8][^6]

**VI.B Instance generation.** Generate warehouse graphs from parameters (aisle count, aisle length, cross-aisles, one-way fraction) rather than hand-drawing one map — this is what substantiates the "non-lattice" claim. Validate each instance against the connectivity assumption, and against the endpoint conditions of well-formed MAPD instances where a baseline needs them, since token-passing style algorithms are complete only on that subclass. Report the discard rate. Seed the order generator separately from the policy and the environment so the same order stream replays under different controllers.[^9][^10]

**VI.C Instrumentation.** Accumulate every metric online. Per-edge counters give \(\mu_T(e)\) and hence \(H_T\); a per-task record of release, assignment, pickup and delivery times gives \(\zeta_j\) and lets the waiting and active phases be reported separately. Give \(W_T\) an *operational* definition here — timesteps in which an agent waited or was overridden while holding an active task — since Section IV left it abstract. Log backlog every step, not just at the horizon, so a diverging queue is visible in the trace.

**VI.D Computational cost.** Runtime is a dependent variable, not an aside: log wall-clock per decision separately for assignment and routing, on the same hardware. Report training and inference time separately for the learned controller, because the practical case for it rests on cheap inference.

**VI.E Correctness and reproducibility.** Run four assertions on *every* experiment, not once in development: no vertex or swap conflict on the realised trace; every storage configuration inside \(\mathcal{X}\); every released task in exactly one of the three task sets at every timestep; bitwise replay determinism under fixed seeds. These four checks are cheap and they are also the answer to "how do you know the simulator implements your model".
## Recommended order of work
The dependency structure suggests doing this in five passes rather than writing linearly.

- **Pass 1 — cut and relocate.** Apply the six cuts to Section IV and move the text verbatim into the Method skeleton's placeholders. Nothing is rewritten yet; this alone will shorten Section IV substantially and populate half of Section V.
- **Pass 2 — number and cross-reference.** Add `\label` to every equation in Section IV and replace each relocated definition in Section V with a `\eqref`. Any Method paragraph that cannot be phrased as a reference is a signal that something is still misplaced.
- **Pass 3 — write V.D and V.F.** The RL formulation and the resolution operator are the two subsections with real content that does not exist anywhere yet, and they are the ones that determine whether the implementation is correct.
- **Pass 4 — implement and let VI write itself.** Section VI is largely a description of code that exists. Writing it before the code exists produces fiction; writing it alongside produces an accurate chapter almost for free.
- **Pass 5 — fill the TBD tables.** Both parameter tables in the skeleton exist so that Section VII contains only results. Populate them after the first stable runs.

One warning about ordering: do not finalise the reward weights in \eqref{eq:reward} before the resolution operator works, because the override penalty \(r_{\mathrm{blk}}\) only has meaning once overrides are correctly detected, and a mis-scaled feasibility penalty is the most common cause of a MAPF policy that learns to stand still.

---

## References

1. [Dynamic Potential-Based Reward Shaping](https://eprints.whiterose.ac.uk/id/eprint/75121/2/p433_devlin.pdf) - by SM Devlin · 2012 · Cited by 398 — In this paper we prove and demonstrate a method of ex- tending ...

2. [Theoretical considerations of potential-based reward ...](https://dl.acm.org/doi/10.5555/2030470.2030503) - Potential-based reward shaping can significantly improve the time needed to learn an optimal policy ...

3. [Lu11a.dvi](https://arxiv.org/pdf/1401.3907.pdf)

4. [Stable-Baselines3 vs RLlib (2026): Which RL Library for ...](https://frontierledger.ai/reinforcement-learning/using-rllib-vs-stable-baselines3toolkit-comparison) - Side-by-side training code, 2026 algorithm tables, RLlib's new API stack, multi-agent market simulat...

5. [Section 30.10: Distributed MARL Training | Building Scalable AI](https://scalablebook.apartsin.com/part-6-multi-agent-systems/module-30-multi-agent-reinforcement-learning/section-30.10.html) - Section 30.10: Distributed MARL Training. How the algorithms of multi-agent reinforcement learning m...

6. [Multi-Agent Environments - RLlib - Ray Docs](https://docs.ray.io/en/latest/rllib/multi-agent-envs.html) - In a multi-agent environment, multiple “agents” act simultaneously, in a turn-based sequence, or thr...

7. [Parallel API - PettingZoo Documentation](https://pettingzoo.farama.org/api/parallel/)

8. [Parallel API | Farama-Foundation/PettingZoo | DeepWiki](https://deepwiki.com/Farama-Foundation/PettingZoo/2.2-parallel-api) - The Parallel API in PettingZoo is designed for multi-agent environments where all agents take action...

9. [Lifelong Multi-Agent Path Finding for Online Pickup and ...](https://arxiv.org/abs/1705.10868) - by H Ma · 2017 · Cited by 524 — We present two decoupled MAPD algorithms, Token Passing (TP) and Tok...

10. [[PDF] Lifelong Multi-Agent Path Finding for Online Pickup and Delivery ...](https://www2.cs.sfu.ca/~hangma/pub/aamas17_slides.pdf)

