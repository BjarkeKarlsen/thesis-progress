# Comments on Appendix B, "Parameters and where each value comes from"

Scope: `thesis/Appendices/B.Parameters.tex` (its own PDF, 4 pages, rebuilt
2026-11-20 after the fixes below). It is a reference table, so it is checked
for truth more than for flow. Checked against `slap-mapd-coupling` on `main`
(`8ba3048`): `configs/fleet_8`, `configs/fleet_16` (and `fleet_32`,
`fleet_64` for the counts), `training/spec.py`, `training/config.py`,
`core/experiment_config.py`, `environment/multi_agent_env.py`,
`environment/storage_estimates.py`, `environment/zones.py`,
`training/arm.py`. Also against Appendices E, F, G, H, I and J,
`4.Implementation.tex` (`sec:method:storage`, `sec:method:training`),
`5.Experiments.tex`, `GAPS.md` ([A31], [A46], [A58], [A73], [A91], [A96],
[A106]), van Knippenberg et al. 2021 (Tables 1 and 5,
`papers/knippenberg21a.pdf`) and Krnjaic et al. 2022 (their configuration
table, `papers/2212.11498v3.pdf`). Equation numbers checked against
`main.aux` of 2026-11-20 and they all match.

The annotated pages are next to this file:
`appendix_B_parameters_comments.pdf` (pages 2 to 4 of `B.Parameters.pdf`).

A note on the code: every config header says "The arm, model, PPO and
checkpoint sections are illustrative, not thesis values". The trained runs
used them, so that header is out of date. Not changed (code repo).

How to answer: tick one box per point and add a note if you want.

---

## A. Is it true (checked against the code, GAPS and the appendices)

### A1. The load row
**Fixed ([A108]).** `tab:evalparams` said "load levels, tasks per step,
0.15, 0.25, 0.3, 0.4, tested, E.4.4". Those are the 3-agent pilot values of
[A31], superseded by [A58]. `lambda_task` counts order lines ([A106]), and
E.4.4 (`app:cal:load`) is the keep-up threshold, not the sweep. Now "main
load, order lines per step, 0.6 of the capacity, at 8, 16, 32 and 64 agents,
0.09, 0.18, 0.3, 0.6, tested, E.4.2" (`tab:app:capacity`, configs
`arrival_rate` 0.09 and 0.18). The RQ3 load levels are still TBD in the
Experiments and have no row here.

### A2. What f_up is a share of
**Fixed ([A108]).** It said "share of the release rate the throughput must
reach", the check of [A49]. Since [A96] it is the work finished in the
measured steps against the work released, picks and put-aways apart. Now
"share of the work released in the measured steps that must be finished,
picks and put-aways apart".

### A3. Evaluation seeds
**Fixed ([A108]).** TBD became 20, set. [A91] (2026-11-12) decided 20 test
seeds, every config has `test_seed_count: 20`, and the Experiments tables
report "of 20".

### A4. Discount, observation depth and three PPO values
**Fixed ([A108]).**
- gamma: TBD became 0.99, cited, Schulman et al. Table 3. Appendix I
  ("The discount is the one of the PPO paper") and Appendix J ("as is the
  discount") both set it, and every config has `discount: 0.99`.
- d_obs: "TBD (sweep)" became 5, cited, van Knippenberg et al. Table 5,
  "checked in I.4.1". Appendix I takes 5 from their Table 5 (checked in the
  paper, 5 is best or near best for 16 to 128 agents) and plans no sweep.
  Every config has `observation_depth: 5`. The window count of I.4.1 is
  still TBD, so the "checked" part waits for it.
- Learning rate, clip and GAE: TBD became 3e-4, 0.2, 0.95, cited, Schulman
  et al. Tables 3 and 1, J.3. Appendix J's conclusion says they "are cited
  from them", and every config uses them.

### A5. Where the five readings are set
**Fixed ([A108]).** The source pointed to G.4.3 (`app:cal:beta`), which
never mentions five readings. The reason is in VI-A beside eq. (40) ("one
reading alone jumps around"), and the code has `SHELF_READINGS = 5`
(`storage_estimates.py:121`). Now "set, Section VI-A".

### A6. Zones p
**Fixed ([A109]).**
**Where:** p. 3, "zones p, TBD (sweep), open".

Every trained section run has `num_zones: 3` (all configs, and the default
in `spec.py:327`), cut as blocks of neighbouring aisles (`zones_by_aisle`).
No sweep was run. The scaling probe uses 6 and 12 (3 x fleet/16). GAPS still
has "decide the number of zones p" as an open box, so I did not change it.

- [ ] Write "3, set", and say the probe uses more
- [ ] Keep TBD
- Note:

### A7. Message-passing rounds and widths
**Fixed ([A109]).**
**Where:** p. 3, "L, TBD (sweep, incl. L = 0)" and "hidden width, TBD".

Every trained config has `num_rounds: 2`, `hidden_width: 32` and
`head_hidden_width: 32`. Appendix J plans L = 0 to 5 and widths 32 and 64,
but its tables are all TBD. Were they run? If not, the values are 2 and 32,
source open (not tested). The head width has no row.

- [ ] Give 2 and 32, open, and add a head width row
- [ ] The sweeps will be run
- Note:

### A8. The other PPO values
**Fixed ([A109]).**
**Where:** p. 3, "minibatch size, epochs/update, rollout length" and
"entropy coeff., value-loss coeff.", both TBD.

Configs: minibatch 128, 5 epochs, entropy 0.02, value loss 1.0. The rollout
is one whole episode per runner (`train_batch_size_per_learner` is runners
times horizon, `training/config.py:362`). Appendix J says the epochs,
minibatch and entropy have no source, so "open" is right, but the value
should be given. The value-loss coefficient of 1 is the one of Schulman et
al.'s Atari table (Table 5), so it could be cited, but J does not say so.

- [ ] Give the values, source open
- [ ] Also cite the value-loss coefficient (J must say it first)
- Note:

### A9. Train, validation and test seeds
**Fixed ([A109]).**
**Where:** p. 3, "train/eval seed counts, disjoint split, TBD".

Configs: 250 training, 5 validation, 20 test. [A73] says 250 at 500 000
steps of 2000-step episodes. Appendix J's checkpoint table says "of 10"
validation seeds, but validation is on 5. The fleet 16 long runs add
2,000,000 steps of 16000-step episodes, so 125 more warehouses.

- [ ] Give 250, 5, 20 and note the fleet 16 long runs
- Note:

### A10. The training budget
**Fixed ([A109]).**
**Where:** p. 3, "training budget, TBD".

VI-G already says "the current budget of 500 000 steps in episodes of
2000", and every config has `training_budget_env_steps: 500000`. Since
2026-11-19 fleet 16 is retrained from those checkpoints for 2,000,000 more
steps on 16000-step episodes. Which budget does the thesis report, and is
it still equal across controllers at fleet 8?

- [ ] 500 000, and the fleet 16 long runs in their own row
- Note:

### A11. The horizon
**Where:** p. 4, "T, evaluation horizon, 2000 or more, open".

Every test runs 10000 steps and leaves the first 5000 out (E.3, G.4.3, the
Discussion "a test lasts 10000", `evaluate --horizon 10000 --warmup 5000`).
Training episodes are 2000 steps (configs), 16000 for the fleet 16 long
runs. "2000 or more" is not wrong, but it hides the values. H and the
Experiments ("a warm-up of TBD steps") also still leave it open.

- [ ] Two rows: test horizon 10000 with 5000 left out, and training episode length
- Note:

**Fixed ([A109]).** T row: 10000, first 5000 left out as warm-up, training episodes 2000, set.

### A12. The reward weights
**Fixed ([A109]).**
**Where:** p. 2, "n_deliver, n_blocked, n_crowd, TBD (sweep)".

Every trained config has 10, 0.5 and 0.1. Appendix I plans a pilot of
n_deliver 1 against 10 and n_crowd 0, 0.1, 1, 2, not a sweep, and says any
n_blocked above 0 does the job. The config comment says n_deliver was
raised to 10 after a run with zero completions.

- [ ] Give 10, 0.5, 0.1, open until I.4.2 has the runs
- Note:

### A13. Stall and lock
**Where:** p. 4, "stall, TBD, open".

The stall length is still open (H waits for it). The lock rule of [A91]
(a seed is locked when two agents each hold one task for 500 steps or more)
is set and reported in the results (`tab:exp:locks`), but has no row. The PF
still defines the stall.

- [ ] Add a lock row, 500 steps, set
- [ ] Does the stall stay in the PF?
- Note:

**Partly fixed ([A109]).** Stall row now reads the fleet-level gap, still TBD. The lock row is not part of this fix.

### A14. Lines per order
**Fixed ([A109]).**
**Where:** p. 4, "5, distribution TBD".

The code has one choice only, `shifted_poisson`, one plus a Poisson count
of mean 4 (`experiment_config.py:39-46`, `multi_agent_env.py:1166`). [A46]
keeps the distribution open. The code decides now.

- [ ] "5, one plus a Poisson count"
- Note:

### A15. Safety stock "per fleet"
**Fixed ([A109]).**
**Where:** p. 4. G.3.1 has the numbers, 16, 18, 17, 16 units. Give them, as
the cap(v) row does.

- [ ] Agree
- Note:

### A16. Checked and matching the code
- beta 1 (`congestion_weight: 1.0`), Delta 100 (`epoch_length: 100`), half
  the rotation period 200.
- Service level 0.99, Q 10 (`refill_units: 10`), cap(v) 52, 56, 54, 52 from
  `tab:app:shelfcap`.
- c_wait 0.2 and c_move 0.1 in every config. Van Knippenberg Table 1 has
  move -0.1 and wait (off goal) -0.2.
- Skew 1, drift 200 steps and 5 percent, 20 SKUs per section, 4
  workstations per section, |K| and |V_str| at 2.5 and 5 per agent for all
  four fleets.
- Units per line uniform on 1 to 5 (`integers(low, high + 1)`).
- Krnjaic et al. have 5 order lines per order on average in three of their
  four configurations.
- Window padding cap set to the largest window, none truncated
  (`training/arm.py:49`). One message hop per timestep. Per-edge head
  ([A17]). The critic reads z_i ([A13]).
- Every equation number in the tables matches `main.aux` of 2026-11-20.

---

## B. Reasons and sources

### B1. "set" is not in the legend
**Where:** p. 2, the opening paragraph.

The legend has cited, derived, tested, open and design. The tables use
"set" ten times. What is "set" against "open"? Service level 0.99 is set,
skew 1 is open, units per line is open, and all three are our choice. Add
"set" to the legend, or split them into design and open.

- [ ] Add "set" to the legend
- [ ] Use only the five kinds
- Note:

### B2. Skew open, drift tested
**Where:** p. 4. Appendix F treats both the same (pilot values, and the
sweep shows the gain holds over the range). F has a TODO asking you this.
Pick one word for both.

- [ ] Both tested
- [ ] Both open
- Note:

### B3. Reasons in the Source column
**Where:** p. 2, beta "a step standing still counts as a step of travel"
and Delta "half the rotation period". Neither is a source kind. Write
"design" (beta) and "derived" (Delta), and keep the reason in the
appendix.

- [ ] Agree
- Note:

### B4. "Fixed before the main runs"
**Where:** p. 2, the last sentence of the opening, and the captions of B.1,
B.2 and B.5. The main runs are done, and B.1 has no TBD left. Say which
values the runs used and which are still open, once A6 to A13 are
answered.

- [ ] Agree
- Note:

### B5. "Below the cheapest edge"
**Where:** p. 2, c_wait. Every edge costs 1 now, so the clause adds little.
It came from the old example with edges of 0.5. Drop it, or say why the
wait must cost less than a step.

- [ ] Drop
- [ ] Keep with the reason
- Note:

### B6. Two "set" rows without a pointer
**Where:** p. 4, "workstations per section" and "|V_str|". F.5 argues the
sections and G.4.4 the sizing. Point there.

- [ ] Agree
- Note:

---

## C. Names, plain words, symbols

### C1. "Router" and "wider routers"
**Where:** p. 3, four times in B.3. [A106] made "controller" the one name.
Say "the centralised and section-based controllers".

- [ ] Agree
- Note:

### C2. Zones and sections in one appendix
B.3 has "zones p" and B.5 "SKUs per section". The open point of
`method_controllers_comments.md` C1 applies here too.

### C3. A bare eta_i
**Where:** p. 3, "with that agent's eta_i". Say "its own distance labels".

- [ ] Agree
- Note:

### C4. "FC layers"
**Where:** p. 3, hidden width. Code language. Write "vertex embedding
width" and add "head hidden width" (A7).

- [ ] Agree
- Note:

### C5. "PPO core", "epochs/update", "coeff."
**Where:** p. 3. "PPO core" says nothing three times, and the slash and
abbreviations read like code. One plain meaning per row.

- [ ] Agree
- Note:

### C6. "fixed (ablation, none)"
**Where:** p. 3, pooled embedding. Which ablation? The full-view setting
left in [A106], and no config turns pooling off. Drop it unless a run
exists.

- [ ] Drop
- Note:

### C7. Two kinds of round
**Where:** p. 3, L "rounds" and "communication rounds". Call the second
"message hops per timestep".

- [ ] Agree
- Note:

---

## D. Reading order and repetition

### D1. Design rows in a parameter table
**Where:** p. 3, B.3. Five of ten rows (one pass per agent, claim mask,
padding, policy head, critic input) are choices without a number, and they
retell the Method. Be critical. I think they can go, and the table then
lists values only. A reader of an appendix of values looks for numbers.

- [ ] Keep only values
- [ ] Keep as is
- Note:

### D2. Warehouse and demand values under "Evaluation"
**Where:** p. 4, B.5. Q, |K|, |V_str|, sections, skew, drift and lines per
order describe the warehouse and its demand, not how a run is scored. A
table of their own would be easier to find.

- [ ] Agree
- Note:

---

## E. Tables

### E1. Layout
**Fixed ([A108]).** B.1 ran 154pt off the page (its Source cell was cut
off). B.2's Meaning column was one word wide, because the citations sat in
the Value column. Both are now `tabularx` with a wrapping Source column, the
citations moved to Source. B.4 got the same so its new citation fits.

Still open: B.3 runs 42pt past the margin (`tabular` with a fixed
`p{0.45\linewidth}`), and the front page title is 30pt too wide (class,
every appendix).

- [ ] Fix B.3 the same way
- Note:

---

## F. What reads well
- The legend of source kinds is a good idea. A reader sees at once what
  is borrowed and what is ours.
- Every cited value names the table it comes from.
- The references point to the subsection that holds the test.

## The three changes that would help the reader most
1. Give every value the trained runs used, even where the source is still
   open (A6 to A13). A reader of this appendix cannot tell today that every
   run had L = 2, width 32, three zones and 500 000 steps.
2. Settle the source kinds (B1 to B3), so "set", "open" and "tested" each
   mean one thing.
3. Keep only values in B.3 and give the warehouse and demand values their
   own table (D1, D2).
