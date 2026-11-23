# Comments on Appendix J, "Model and training"

Scope: `thesis/Appendices/J.Training.tex` (its own PDF, `J.Training.pdf`, 6
pages, rebuilt 2026-11-20 after the fixes below). Checked against
`slap-mapd-coupling` on `main` (`8ba3048`): `training/config.py`,
`training/trainer.py`, `training/evaluate_run.py`, `models/gnn_encoder.py`,
`models/base_model.py`, `evaluation/metrics.py`; the configs in
`configs/fleet_8`, `configs/fleet_16`; every `*_spec.json` under
`~/thesis_runs/training/`; the fleet 8 `evaluation.json` files under
`~/thesis_runs/evaluation/fleet_8/<arm>/fixed/evaluation_served_horizon10000_warmup5000/`;
`thesis-progress/RUNS.md`; `SESSION_CONTEXT.md` (fleet 16 long training);
the Method section `sec:method:training` (read only, another agent reviews
it); the PF (`eq:throughput` and the sentence after it, [A96]);
`E.Load.tex`, `I.Reward.tex`, `B.Parameters.tex`; GAPS [A56], [A60], [A73],
[A96]; van Knippenberg et al. 2021 (`papers/knippenberg21a.pdf`, Section
4.2); Schulman et al. 2017 (not in `papers/`, values checked against the
arXiv tables the text names); the RLlib defaults of the installed 2.57.0
(`~/.venvs/rl`).

The annotated pages are next to this file: `appendix_J_training_comments.pdf`.

How to answer: tick one box per point and add a note if you want.

---

## A. Is it true (checked against the code and the runs)

### A1. The Method describes runs that were not run
**Fixed ([A109]).**
**Where:** p. 2, "The rounds of message passing, the hidden widths and the
budget are tested on the 8-agent warehouse", and p. 3, "Larger fleets may
need more, which is checked on each fleet".

**Runs:** every trained run, at 8, 16 and 32 agents and under every storage
rule, uses L = 2, hidden and head width 32 and the same PPO values. No
L sweep and no width run exists. The budget was 500,000 steps on 2000-step
episodes at every fleet. Then fleet 16 was trained again: a warm start from
the checkpoint each old run was tested with, plus 2,000,000 steps on
16,000-step episodes (`fleet_16/<arm>/<regime>_long`, five of them continued
as `_long_part2` with 1,856,000). So the budget question was answered on
fleet 16, by episode length, not on fleet 8 by where the validation curves
level off. SESSION_CONTEXT step 5 says the episode-length pilot (2000,
8000, 16,000) goes into this appendix once the author says so. The Method
should say what was run, and why L = 2 and width 32 if the sweeps are not
run (B2).

- [ ] Agree, rewrite the Method to the runs
- [ ] Run the sweeps
- Note:

### A2. "The number of training seeds is the number of training episodes"
**Fixed ([A109]).**
**Where:** p. 2, Setting.

At 500,000 steps it is close but not exact. Three runners each play one
whole episode per iteration, so a run stops after 84 iterations, 504,000
steps and 252 episodes on 250 seeds (`trainer.py`, the budget overshoots by
up to one iteration). For the long fleet 16 runs it is false. 2,000,000
steps of 16,000 is 125 episodes over 250 training seeds. Say "about one
episode per warehouse" or give both setups.

- [ ] Agree
- Note:

### A3. The PPO loss is not only the paper's clipped objective
**Fixed ([A109]).**
**Where:** p. 2 and 3, "The configs use these four".

The four values match (their Table 3 and Table 1, checked). But
`build_ppo_config` (`training/config.py:356`) leaves RLlib's own defaults.
In RLlib 2.57.0 those add a KL penalty on top of the clipping
(`use_kl_loss=True`, `kl_coeff=0.2`, `kl_target=0.01`) and clip the value
loss at 10. Schulman et al. compare clipping with a KL penalty in their
Table 1 and the clipping alone wins. So the loss we train is "clipping plus
an adaptive KL penalty". Either say it, or switch the penalty off for later
runs. The value loss weight 1.0 is not named either. It matches their Atari
value c1 = 1 (Table 5). Check the RLlib version on Kaggle and Colab is the
same.

- [ ] Say it in the text
- [ ] Switch it off for later runs
- Note:

### A4. "TBD of 10" validation seeds
**Fixed ([A109]).**
**Where:** p. 3 and 4, all three tables.

Every config and every evaluation so far validates on 5 seeds
(100000 to 100004, `evaluation.json`), and memory/SESSION_CONTEXT say
"always 5". GAPS [A60] still lists the number as open, so it is not fixed
here. Settle it at 5 and the tables say "of 5". Also not said: validation
plays the training episode length with no warm-up (2000 steps, or 16,000
for the long fleet 16 runs), while the test plays 10,000 steps with a
5000-step warm-up. The reader needs both.

- [ ] Settle at 5, and say the validation episode length
- Note:

### A5. Table J.1 has the wrong rows
**Fixed ([A109]).**
**Where:** p. 3, Table J.1.

It lists three controllers at 8, 16, 32 and 64 agents. Trained runs exist
for four controllers (decentralised with messages too) at 8 and 16, and
only decentralised and section-based at 32 (section-based demand
unfinished). Fleet 64 has no trained run (Probe A waits). The fleet 8 data
is there now. Chosen checkpoints under fixed storage: centralised 13
(iteration 42), section-based 10 (33), decentralised 12 (39), with messages
21 (66). Also, which storage rule's run does a row show? Each controller
has one run per rule.

- [ ] Agree, fix the rows and fill fleet 8
- Note:

### A6. Knippenberg does not give the number of layers
**Fixed ([A108]).** p. 2. The text said they "give the number of layers of
each experiment but not their sizes". Their Section 4.2 says only that the
number of layers "depends on the particular experiment", and no table gives
it. Now: "say only that the number of layers depends on the experiment, and
give neither the numbers nor the sizes".

### A7. A run that does not keep up is reported by its served share
**Fixed ([A108]).** p. 3. "reported by its throughput" became "reported by
its served share", as the PF says after `eq:throughput` and E.Load says
([A96]). The choice among failing checkpoints still uses the highest
throughput, as the code does (`choose_checkpoint`).

### A8. Checked and matching
- Checkpoint rule ([A60]): keep up on every validation seed, then the
  shortest mean pick service time, else the highest mean throughput
  (`evaluate_run.py:168`). A tie goes to the later checkpoint (not said,
  fine).
- `mean_service_time` is over completed picks only (`metrics.py:176`), so
  "mean service time of picks" is right.
- The budget counts timesteps, one per timestep (`trainer.py:39`).
- One shared policy (`DEFAULT_POLICY_ID`). Training, validation and test
  seeds are disjoint ranges (`config.py`, 100000 and 200000).
- L = 0 is a real ablation (`gnn_encoder.py:76`). Hidden width is the
  width of the message and update layers, head width the hidden layer of
  the move score, wait score and value networks (`base_model.py:46`).
- d_obs = 5 in every config.
- Schulman et al.: 3e-4, lambda 0.95, discount 0.99 and 10 epochs,
  minibatch 64 (Table 3), clipping 0.2 best (Table 1), 3 epochs and entropy
  0.01 for Atari (Table 5).
- Equation and section numbers (27), (29), (34), (48), VI-C, VI-G match
  `main.pdf` of 20 Nov. The discount source is in Appendix I.
- The training return is dominated by shaping: fleet 8 centralised fixed,
  iteration 1, shaping 3221 against delivery 23.

---

## B. Reasons and sources

### B1. Why 5 epochs, minibatch 128 and entropy 0.02?
**Where:** p. 3, and the Conclusion, "have no source".

The text is honest that they have no source. But the reader still asks why
these values. Where did they come from (the rl_review of 2026-11-10?). Give
the reason in one clause, or say they were not tuned and are the same for
every controller. TODO in the `.tex` already asks this.

- [ ] Give the reason (which?)
- [ ] Say "not tuned, the same for every controller"
- Note:

### B2. Why L = 2?
**Where:** p. 2, "With L = 5 the agent's vector reaches the whole field of
view".

Every run uses L = 2, so the agent's vector reaches 2 of the 5 steps it
can see. Why 2? If the sweep is not run, this is the choice the reader
needs a reason for. Same for width 32.

- [ ] Agree, give the reason
- Note:

### B3. The warm start is a training choice with no word
**Where:** p. 2, "under the same budget".

The fleet 16 policies the Results use are warm started from the 500,000-step
runs and then trained on 16,000-step episodes. The reason is in
SESSION_CONTEXT: the old policy broke down within 10,000 to 20,000 steps. So
fleet 8 and fleet 16 are trained differently. This needs its reason here,
and a line in the Discussion. Also, the warm-start code (`--init-checkpoint`)
is on branch `feat/warm-start-a93`, not on `main`.

- [ ] Agree, add the episode-length pilot here
- Note:

### B4. Borrowed model, not borrowed learner
**Where:** p. 2, "The model descends from PRIMAL through the graph encoder
of Knippenberg".

Knippenberg's model is "essentially a Deep Q-Learning" model (his Section
4.2). We take the graph encoder and train it with PPO. Say which part is
borrowed and that PPO is our choice, with one clause of reason.

- [ ] Agree
- Note:

---

## C. One name per idea, plain words

### C1. "One training seed each"
**Where:** p. 2, Method.

Every run has 250 training seeds, one warehouse each. "One training seed
each" means one run each (one RLlib seed). Say "one run each".

- [ ] Agree
- Note:

### C2. PPO, GAE, "encoder family", "PPO health"
The appendix is its own paper, but PPO and GAE are never spelled out, and
"GAE parameter" means nothing to a reader without it. "Encoder family" is a
new term for "the same network". "PPO health" in the caption of Fig. J.2 is
jargon.

- [ ] Agree
- Note:

### C3. Column names
"mean service time" next to "put-away service time". Both are means, one of
picks. Say "pick service time" and "put-away service time". And "training
steps" in Table J.1 against "environment steps" in the text. One name.

- [ ] Agree
- Note:

---

## D. Reading order and repetition

### D1. Summary and Conclusion say the same, and neither answers
The Summary says the PPO values "match ... and are cited from it", and the
Conclusion says it again. The question the Summary asks ("which model and
training values they use") gets no answer in either. Once A1 is settled,
the Summary should give the values used.

- [ ] Agree
- Note:

### D2. The reason comes last in Setting
The third paragraph ("A controller that has not finished learning makes
its way of deciding look worse") is why the appendix exists. Lead with it.

- [ ] Agree
- Note:

### D3. Floats and empty headings
Table J.2 sits above the heading of its own subsection, Table J.3 sits under
the heading of the rounds, and both figures land after the References. The
empty subsections print as run-in headings with a colon
("J.4.2 Calibration: the hidden widths:"). Pin the floats ([H]) and put a
sentence under each heading.

- [ ] Agree
- Note:

---

## E. Figures

### E1. Fig. J.1 is a placeholder, but its data exists
The placeholder waits for `results/J_training/fleet_8/<arm>/validation.jsonl`,
which does not exist. The validation rows do exist: 28 checkpoints on 5
seeds per fleet 8 arm, in
`~/thesis_runs/evaluation/fleet_8/<arm>/fixed/evaluation_served_horizon10000_warmup5000/validation.jsonl`.
Point the script there. Fixed ([A108]): the caption said "the rule below",
but the rule is above, so now "Rings mark the chosen checkpoints."

- [ ] Agree, point the script at the evaluation folder
- Note:

### E2. Fig. J.2 cannot be drawn from what we saved
The progress files hold returns, counts and timers, but no policy loss,
value loss, entropy or KL (`*_training_progress.jsonl`). And what does the
reader learn from it? Drop it, or log the four values in later runs.

- [ ] Drop it
- [ ] Log the values
- Note:

---

## F. What reads well
- "A controller that has not finished learning makes its way of deciding
  look worse than it is." Clear reason.
- The PPO paragraph is honest about which values have a source and which
  do not.
- The checkpoint rule is the decision problem's rule, so one measure picks
  both. The reason the training return is not used is given.
- L = 0 explained as "what message passing adds at all".

## The three changes that would help the reader most
1. Rewrite the Method to the runs that exist: L = 2 and width 32
   everywhere with a reason, 500,000 steps on 2000-step episodes, and the
   fleet 16 warm start with 16,000-step episodes and the pilot behind it (A1,
   B2, B3).
2. Settle 5 validation seeds and the validation episode length, fix the
   rows of Table J.1 and fill fleet 8 (A4, A5).
3. Say the loss has RLlib's KL penalty, or switch it off, and give the
   reason for epochs, minibatch and entropy (A3, B1).
