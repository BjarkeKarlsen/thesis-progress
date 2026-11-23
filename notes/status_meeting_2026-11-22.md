# Status meeting, week 48 (written 2026-11-22, updated 2026-11-23 07:20)

## Short version

**Done since last time**
- The first round of runs is complete for all four controllers under all three storage rules (fixed, demand and congestion-aware).
- It showed that the policies needed longer training. Every run is now retrained for longer, continuing from where it stopped.
- The longer training helps clearly. Seven runs are evaluated so far, and all of them improved.
- Under congestion-aware storage, all three controllers evaluated so far serve about 80% of tasks and keep up on about half the test seeds, against 60 to 70% before.
- Congestion-aware storage is the best rule for every controller so far.
- The introduction and part of the method chapter are rewritten.

**Now**
- All runs but one have finished training. The last one, centralised demand, finishes Tuesday morning.
- Every evaluation should be done Tuesday, possibly before the afternoon.

**Next week**
- Finish rewriting the method chapter.
- Then start writing the results, once the evaluations are in.

## More detail

### The setup in one paragraph

The warehouse has 16 agents. Four controllers are compared: centralised, section (one controller per zone), decentralised, and decentralised with communication. Each is trained under three storage rules: fixed, demand and congestion-aware. That gives 12 trained policies. Every policy is a graph network trained with PPO.

### Why longer training

- The first round trained with shorter episodes and a smaller budget. Its training curves were still rising at the end, so the policies had not finished learning.
- The long runs continue from the last checkpoint of the first round (a warm start). They use episodes of 16,000 steps and a budget of about 2 million steps, which is 42 iterations.
- The runs that started on a CPU continue on a GPU as a second part, from their latest checkpoint.

### Results so far

All 12 runs, four controllers under three storage rules, on 20 test seeds each. Seven long runs are evaluated so far. The first-round result is in brackets, and every first-round run is evaluated. Served is the share of tasks finished within the measuring window. Keep up counts the test seeds out of 20 where the controller keeps up with the arriving work.

| Controller | Storage rule | Tasks per step | Served | Keep up | Long run |
|---|---|---|---|---|---|
| Centralised | Fixed | (0.143) | (0.54) | (0) | Being evaluated on the PC |
| Centralised | Demand | (0.138) | (0.52) | (0) | Training on Colab, done Tuesday |
| Centralised | Congestion-aware | 0.239 (0.161) | 0.81 (0.59) | 10 (0) | Evaluated |
| Section | Fixed | 0.216 (0.178) | 0.76 (0.63) | 9 (7) | Evaluated |
| Section | Demand | (0.147) | (0.54) | (0) | Being evaluated on the Lenovo |
| Section | Congestion-aware | 0.233 (0.198) | 0.79 (0.69) | 9 (5) | Evaluated |
| Decentralised | Fixed | 0.069 (0.025) | 0.29 (0.12) | 0 (0) | Evaluated |
| Decentralised | Demand | 0.144 (0.096) | 0.53 (0.39) | 0 (0) | Evaluated |
| Decentralised | Congestion-aware | 0.235 (0.186) | 0.80 (0.66) | 8 (2) | Evaluated |
| Decentralised, communication | Fixed | 0.177 (0.091) | 0.63 (0.37) | 4 (0) | Evaluated |
| Decentralised, communication | Demand | (0.064) | (0.28) | (0) | Trained, evaluated next on the PC |
| Decentralised, communication | Congestion-aware | (0.084) | (0.34) | (0) | Trained, evaluated next on the PC |

What this shows so far:
- Every run improved with longer training, some by a lot.
- Congestion-aware storage is the best rule, and with it the three controllers are nearly level, at about 80% served.
- Fixed and demand storage stay behind, most of all for the decentralised controller. The section controller is the exception so far: under fixed storage it nearly matches congestion-aware storage (0.76 against 0.79 served).
- Communication helps the decentralised controller a lot under fixed storage (0.63 served against 0.29).

These numbers are still incomplete. The five open long runs come in by Tuesday. In the first round, congestion-aware storage was already the best rule for three of the four controllers. The communication controller was the exception, and its long runs will show whether that still holds.

### How a policy is chosen and tested

- **Train:** a checkpoint is saved every 3 iterations, about 144,000 steps apart. A long run has 14 checkpoints.
- **Validation:** every checkpoint plays 5 seeds it never trained on, and one is chosen.
- **Test:** only the chosen checkpoint plays 20 other seeds. Those seeds choose nothing, so the reported numbers are fair.
- **Why every 3 iterations and not every one:** PPO moves the policy only a little per iteration. Over 3 iterations, the validation mean changes by about 1.5 to 2 times its seed noise. Over one iteration, the change would be smaller than the noise, so the choice would mostly pick a lucky checkpoint.
- **Why choosing matters:** decentralised demand peaks at 0.171 tasks per step on validation but ends at 0.096, so taking the last checkpoint would be much worse.
- This argument is now written into Appendix J, Checkpoint selection.

### Where the work runs

Training and evaluation are spread over several machines to finish sooner:

| Machine | What it does |
|---|---|
| Google Colab (L4 GPU) | Trains the last run, centralised demand, then evaluates it straight away |
| Lenovo server | Evaluates section demand, then the next free run |
| Own PC | Trained centralised fixed (done Monday 05:08), now evaluates it, then the two communication runs |
| Kaggle | Trained the decentralised runs (finished), not used any more |

The plan for the rest is simple. Colab trains, and the Lenovo and the PC evaluate. One evaluation takes between 2.5 and 17 hours, so the two evaluators run side by side.

**Could Colab or Kaggle help more?** No, it would not finish anything sooner.
- The last run to finish is centralised demand, and it is still training. One run cannot be split across machines, so more machines do not speed it up.
- Moving it to the PC would mean starting a third part from its last checkpoint, and the PC is no faster.
- The Lenovo and the PC should finish every other evaluation by Monday night, before centralised demand is trained. Extra evaluators on Colab or Kaggle would only bring those results a few hours forward.
- Kaggle has no tested evaluation setup, and its machines have 4 cores, half of Colab's.

### Problems along the way, now handled

- **Centralised fixed crashed twice when memory ran out.** It now continues from its last checkpoint, with the memory limit that stopped it removed.
- **Some runs trained on Kaggle could not be continued elsewhere.** Kaggle saves training state with a newer Python. They continue as a second part from their latest checkpoint instead.
- **Two Colab sessions were refused or slow to start.** There is now a fallback to another GPU type.

None of these change the results. They cost time, and that is why the last run finishes on Tuesday.

### Timeline

| When | What |
|---|---|
| Monday 05:08 | Centralised fixed finished training on the PC |
| Monday | Section demand, centralised fixed and the two comm runs are evaluated |
| Tuesday morning | Centralised demand finishes training on Colab |
| Tuesday | Its evaluation finishes, so all 12 long runs are evaluated |
| Rest of next week | Finish the method rewrite, then start the results chapter |

### Thesis writing

- **Done:** the introduction and part of the method chapter are rewritten for readability, with shorter sentences and plain words.
- **Next:** the rest of the method chapter.
- **After that:** the results chapter. It is built around the main result: how much demand storage improves service time over fixed storage, for each controller.

### Risks

- If a run crashes again, it continues from its last checkpoint, which costs a few hours at most.
- Colab credit is enough for the remaining run, with a small buffer.
- With 5 validation seeds the checkpoint choice is a little noisy. It does not bias the test numbers.
