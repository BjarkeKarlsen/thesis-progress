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
