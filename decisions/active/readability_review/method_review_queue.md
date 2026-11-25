# Method chapter review, queue and open points

The author-style review of `4.Implementation.tex`, one section at a time.
Each section gets margin notes (an annotated PDF) and a comments file with
tick boxes. Readability points wait for the author. Small known mistakes
([A107], [A108]) and the worst text-to-code mistakes ([A109]) were fixed on
2026-11-20 at the author's request, see GAPS.md. Every fixed point carries
"Fixed ([A10x])" in its comments file. Fixed and decided points were removed
from the comments files on 2026-11-23, the full files are in `full_2026-11-20/`.
At the end, all readability points go into one review PDF for the chapter.

## Sections

| Section | Label | Status | Comments file |
|---|---|---|---|
| Method opening, loop, Fig. 12 | `sec:method` | **done 24 Nov** ([A123]) | `done/review_method_storage.pdf` |
| Where arriving stock goes | `sec:method:storage` | **done 24 Nov** ([A123]) | `done/review_method_storage.pdf` |
| Who takes which task | `sec:method:assignment` | **done 24 Nov** ([A123]) | `done/review_method_storage.pdf` (`done/method_model_comments.md` part A) |
| How an agent chooses its move | `sec:method:model` | **done 24 Nov** ([A124]) | `done/review_method_model.pdf` |
| Choosing together | `sec:method:controllers` | **done 24 Nov** ([A125]) | `done/review_method_controllers.pdf` |
| When moves still clash | `sec:method:resolution` | **done 24 Nov** ([A126]) | `done/review_method_resolution.pdf` |
| What an agent is rewarded for | `sec:method:rl` | **done 24 Nov** ([A127]) | `done/review_method_reward.pdf` |
| How the controllers learn | `sec:method:training` | **done 24 Nov** ([A128]) | `done/review_method_training.pdf` |
| A reference point | `sec:method:reference` | reviewed 20 Nov | `method_reference_comments.md` |
| Implementation (simulator, logging, cost, checks) | `sec:implementation` | reviewed 20 Nov | `implementation_comments.md` |
| Appendices A to L | `app:*` | reviewed 20 Nov | `appendix_<X>_<name>_comments.md` |

## Decisions waiting for the author (20 Nov, most important first)

These are choices, not facts, so no agent fixed them.

1. **Which training setup gives the main result.** The Method, `sec:exp:setup`
   and Appendix J say the policies trained under fixed storage. Appendix L and
   the main-text gain use each rule's own policy (`method_training_comments.md` A1).
1. **Decided 2026-11-23.** Only the setup where each rule has its own policy.
   Regime 1 dropped, data in `results/dropped/regime1_fixed_trained/`,
   review `review_training_setup.pdf` v2 waits for the author.
2. **Author's direction 2026-11-23 (decisions 2 and 3, under discussion).**
   Checkpoints are chosen on 5 validation seeds, and that stays. The long
   fleet 16 runs are the main result. The 500 000-step runs are kept as
   earlier runs, where the issues and reasons were found, and nothing is
   deleted. Fleet 8 training is probably too short to go in the thesis.
   Only the fleet 16 training is used. Fleet 8 is tested again only by the
   scaling test (`scaling_plan.md`, fleet 16 policies). The earlier runs
   are kept as research into the problem: why training got longer, and why
   the main warehouse has 16 agents (at 8 agents the learned arms gained
   nothing from congestion-aware storage, at 16 they did with the same
   short training). Their served counts stay with them, and the text calls
   every one of them an earlier run.
   Checked 2026-11-23 (replay rows, served counts at f_up 0.9): congestion
   against fixed at 8 agents, served share 0.86 to 0.81, 0.87 to 0.91,
   0.84 to 0.82, 0.96 to 0.82 (centralised, section, decentralised, with
   messages). At 16 agents 0.54 to 0.59, 0.63 to 0.69, 0.12 to 0.66, 0.37
   to 0.34. Blocked steps per pick are about the same at 8 (8 to 19) as at
   16 (15 to 24), so do NOT write "too few agents to crowd". Agreed wording:
   at 8 agents the fleet nearly kept up, so there was little for the
   storage rule to win. The 16-agent decentralised jump is mostly its weak
   run under fixed storage.
   Original point:
   **Which checkpoint counts.** The served replays chose checkpoints again on 2
   validation seeds, so Appendix L mixes two policies (16 agents decentralised
   fixed, five arms at 8 agents) (`appendix_L_results_comments.md` A1).
3. **Decided 2026-11-23.** The long fleet 16 runs are the main result. Text
   must say the results use them, with the reasons (author): the warm start
   shortens training time, and the long episodes make training closer to the
   test, a more real scenario. Appendix J gets the episode-length pilot as a
   plot (2000, 8000, 16 000 steps). These go in one review PDF with the
   Appendix L "earlier runs" rewrite. Code: `feat/warm-start-a93` is not on
   `main` (author opens the PR). Original point:
   **Which fleet 16 policies the results use**, the 500 000-step ones or the
   long warm-start runs (`appendix_J_training_comments.md` B3).
4. **Settled by [A111] (2026-11-23).** At f_up 0.9 with the served counts
   the load sweep gives back the capacities of Table E.1. Left: the Kaggle
   replay of the lower rates (`slap-load-sweep-low`, `% TODO [A111]` in E).
   Original point:
   **Appendix E capacities.** Found with the old keep-up check. The [A96]
   check gives 0.175, 0.35, 0.6, 1.2, so the main loads are about 0.5 of
   capacity, not 0.6 (`appendix_E_load_comments.md` A1).
5. **Names and symbols.** Zone or section, w, message, h(k), B and Q, q
   (`appendix_A_notation_comments.md` C2 to C9, `method_controllers_comments.md` C1).
6. **Report the order gain beside the pick gain** in Appendix F (order gain
   14 to 18 percent) (`appendix_F_demand_comments.md` A1).
7. **Trip legs** (`review_trip_legs.pdf`, now also Appendix G).
8. **The stall length** and whether a fleet-level gap is fair across loads
   (`appendix_H_horizon_comments.md` A2).
9. **Merge the 32 and 64 congestion rows** of the tp-a93 rerun into Appendix G
   (`appendix_G_storagevalues_comments.md` A1).
10. **Figures to redraw.** H.1 to H.3, D.2, D.3, L.1, L.2, Fig. 15 in viewer
    colours, J.1 (data exists), K.1.
11. **Questions answered and APPLIED 2026-11-23 as [A119]** (swap clause, halo cited to DistDGL, the priority sign read once, new `fig:claimmask`). The rest of the review's wording APPLIED 2026-11-23 as [A120], review moved to done/. Original point: **`review_controllers.pdf`** questions 1 to 6, refreshed against [A107].
12. **Reasons the text still lacks**, listed under B in each comments file.

## Where the review stands (2026-11-23, author)

- `review_training_setup.pdf` v3: APPLIED 2026-11-23 as [A114] (Method,
  Experiments, Appendix J, Appendix L section removed). Builds clean.
- Names (5): APPLIED 2026-11-23 as [A115], builds clean. Done after:
  `workstation_lock.png` redrawn with W_1 (t = 1160 in the text is a step
  between panels (c) and (d), from the trace, not an error); the t of
  d^trip(k,v) dropped (also the d^trip_0 of fixed storage); unused
  `Chapters/2.Notation.tex` removed (git rm, backup in the session scratchpad).
- Appendix F: APPLIED 2026-11-23 as [A116] (whole appendix rewritten, new
  `tab:app:demandgain`, labels `app:demand:first`, `app:demand:changes`).
- Finished reviews moved to `readability_review/done/` (2026-11-23):
  training_setup, appendix_F, seed_spread, workstation_lock, served_share,
  served_share_lines, project_description, loop_figure, figures (with
  figures_review/), shelf_blocking; later also arrivals, where_items_are,
  pf_content, results_fleet16, results_discussion_fleet16, thesis_adjustments,
  FIX_BRIEF.md, SUBAGENT_BRIEF.md, pf_scoring, observation_learning (author:
  done). Open: none. evaluation_setup moved to done/ ([A121] filled its one
  useful point). PRs opened 2026-11-23: #211 fix/stall-length, #212
  feat/warm-start-a93. Still open: controllers, trip_legs, evaluation_setup,
  results_fleet16, results_discussion_fleet16.
- Trip legs (7): follow the code, the policies are trained on it. Remove
  "A SKU with no line yet" from the text: under the run configs a refill
  comes only after a SKU was ordered (`refill_amounts`, `refill_units: 10`)
  and the guessed section keeps the last one seen, so it never happens. The
  worked example could be drawn on the tea figure `fig:storageexample`
  (`arrival_storage.png`). Review PDF still to be updated to this.
- Names (5), decided by the author 2026-11-23, to go into one review PDF
  (a sweep of all chapters, appendices, notation table, figures):
  1. The SKU group "section" becomes **category** (h(k): the SKU's
     category). Zone and the section-based controller stay.
  2. Fig. 15 (`fig:workstationlock`, `4.Implementation.tex:471-483`): the
     workstation w becomes W_1, as in the PF examples. Redraw if the image
     writes w.
  3. s: leave (each use in its own part, clear where used).
  4. h(k): keep the letter, drop the hat. Lines of SKU k only ever go to its
     own category (`multi_agent_env.py:1167-1174`) and a refill only follows
     a line, so the guess equals h(k) whenever a rule uses it. Say in words
     that the demand rules are not told h(k) and learn it from the first
     line. (Open: author asked whether a hat is better since it is a guess.)
  5. q: rename only the current target q_i(t) to v*_i(t).
  6. Backlog B_t becomes N_t (N^pick_T, N^put_T). Fonts unchanged.
  7. Keep V = {v_1, ..., v_|V|}. Rename the shelves of the pickup rule
     (`3.ProblemFormulation.tex:689`) to v_(1), v_(2).
  Update `A.Notation.tex` in the same change, and GAPS.md.
- Appendix F (6): no rerun, numbers still valid (Token Passing setting
  sweep). The author finds F unfinished. Open points in
  `appendix_F_demand_comments.md` (A1 order gain, A5 to A9, B1 to B3, C, D,
  E1).
- 7 Trip legs (2026-11-23): follow the code. Fixed storage overflow goes by
  the leg-weighted trip (`_refill_scores`): workstation leg x lines per step +
  dock leg x pallets per step. For one SKU the shelf order depends only on the
  ratio of the two, about Q / units per line, the same for every SKU, so it does
  not favour popular SKUs (SKUs placed in id order). Overflow share: TP fixed
  ~8 % of arriving units, learned fixed 40 to 60 %. Text: plain words first
  (approved wording: two trips, counted per pick and per pallet), then
  "Formally," with d^work, d^dock, pallet rate. One sentence on fixed overflow.
  APPLIED 2026-11-23 as [A122], review moved to done/. Follow-up: draw the tea
  example on fig:storageexample.
- 8 Stall: APPLIED 2026-11-23 as [A118]. Stall length 36 / lambda_task =
  400/200/120/60 steps (TP max 316/114/53/12). PF, B, H (new Fig. H.3), TODO in
  L. Code: branch fix/stall-length (worktree ~/worktrees/stall-length,
  uncommitted, author opens the PR). Pre-existing failing test on main:
  test_the_file_and_the_example_build_the_same_study[decentralised].
- 9 Appendix G: APPLIED 2026-11-23 as [A117].
- 10 Figures: D.2, D.3, J.1 REDRAWN 2026-11-23 (D.2 rings categories, zones on
  16 agents; J.1 from the long 16-agent validation rows, captions updated).
  Rerun `appendix_training.py` once centralised demand_long is evaluated (J.1
  shows 3 arms under demand). D.Warehouses.tex:290-292 (docks move per seed)
  stays, author: it is about every fleet, not only 8. D:166 does not say
  workstations come in groups of four per category (left for the read-through). L waits for the long runs,
  H waits on point 8.
- **Still to review: 8 to 12**, and the open points in every comments file.

## Mistakes against the code (fix before the readability pass)

Small known mistakes are fixed directly from 2026-11-20 (author's word):
[A107] for `sec:method:controllers` and `sec:method:resolution`, [A108] for
the sections and appendices reviewed by subagents (`SUBAGENT_BRIEF.md`).

- **Trip legs.** Text, eq. (38), eq. (39) and Appendix C add the two legs
  with no weight. The code weights them by picks and pallets. Proposal:
  `review_trip_legs.pdf`, waiting for answers (question 1 first, fixed
  storage reads the demand estimate).
- **How zones are drawn.** The code cuts them as blocks of consecutive
  aisles, 3 in the trained runs. The thesis never says how, and
  `tab:modelparams` still says p is TBD (sweep) (C1). The zone cut is in
  the text since [A107]. The p value is for the Appendix B agent.
- **The lock of Fig. 15 is not a circle of the rule.** In the trace the
  agents in front of w choose to wait, and the rule only refuses the moves
  onto them. The text tells it as a circle (A3). The override penalty
  sentence holds only because of that chosen wait (A2).

## Open questions for the author (answer in the comments files)

- `method_storage_comments.md`: A2 to A4, B1 to B7, C1, C2, D1 to D7.
- `method_model_comments.md`: A1 to A5, B1 to B8.
- `method_controllers_comments.md`: A1 to A4, B1 to B4, C1, D1 to D4, E1.
- `review_controllers.pdf`: the proposed text for `sec:method:controllers`,
  questions 1 to 6. Apply only after the author approves it. Its changes
  A1, A3, A4 and the zone cut are already in the thesis ([A107]), so it
  needs a refresh against the current text before it is applied.
- `review_trip_legs.pdf`: questions 1 to 4.
- `method_resolution_comments.md`: A1 to A4, B1 to B3, C1 to C4, D1 to D3.

## Points that go to the Discussion (collect here)

- Put-aways get no priority, which may hold up picks at high load
  (`method_model_comments.md` A3).
- No memory may favour the controllers that see more (B4).
- A pallet that fits nowhere is lost (`method_storage_comments.md` A4).
- Congestion-aware storage counts only standing still, not detours (PF
  already says it, check the Discussion has it).
- The centralised controller sees L rounds around the agent plus a mean
  that one choice barely moves. What sets it apart is then the claim mask
  and the shared credit, not seeing more (`method_controllers_comments.md`
  B1).
- Only the section-based controller is overridden at zone borders, so only
  it pays the override term against the centralised one (B4).
- The workstation lock is learned behaviour. A chosen wait is cheaper than
  being overridden, so the agent in front of a workstation learns to wait,
  and nothing pays it to back out (`method_resolution_comments.md` A2, A3).
- No rule breaks a circle inside conflict resolution. Only the workstation
  cap was rejected in [A91], so the reason for the other rules is still
  open (B2).

## Carry forward to later sections

- Figure 12 and Figure 13 both draw the loop. Decide which one keeps it.
- "Message" is used for vertex messages and agent messages. Check later
  sections use the chosen names.
- Token Passing assigns its own tasks. Check `sec:method:reference` says
  it, and that the loop at the start says it too.
- Pooling: covered by eq. (47) in `sec:method:controllers`. Closed.
- Zone and section mean different things (zones of the section-based
  controller, sections of SKUs). Check later sections, Results and figures
  use the chosen names (`method_controllers_comments.md` C1).
- The override term: the claim mask paragraph says it is always zero for a
  centralised agent. Check `sec:method:rl` says the same, and says the
  section-based controller pays it at zone borders.
- The credit differs per controller (eq. credit). Check `sec:method:training`
  and the closing paragraph of `sec:method:controllers` agree once that
  paragraph is rewritten (D3).
- Knippenberg's single-agent setup scaled worse (his Table 4). Could support
  one run per agent here or in `sec:impl:cost`.
- Why Token Passing does not lock (it holds a vertex until it has left, and
  every warehouse is well-formed). Check `sec:method:reference` says it, and
  drop "plans ahead" from `sec:method:resolution`
  (`method_resolution_comments.md` B3).
- The reward: check `sec:method:rl` says a chosen wait costs c_wait and an
  override c_wait + n_blocked, since the lock story leans on it.
- "Paired seeds" is used in `sec:method:resolution` before the Experiments
  define it (C3).
- w names a neighbour vertex (eq. 46, claim mask) and a workstation (Fig.
  15). Check later sections (C2).


## Review of 20 Nov by section and appendix (merged from the subagent reports)

Points marked fixed in [A109] are marked "Fixed ([A109])" in the comments files. The lines below are as the reports gave them, before [A109].

### method_reward (no fixes)
MISTAKES:
- **Reward shaping ([A89], [A90]).** `sec:method:rl` defines Phi = -eta (distance to the current target), charges a new task once ([A79] text) and gives idle agents a parking target. The code uses minus the distance left in the whole task, counts progress within one task only, and gives idle agents no shaping (`environment/reward_function.py::potential`, `reward_terms`). Neither [A89] nor [A90] has a GAPS entry. Same change needed in the Phi row of `A.Notation.tex` and "The reward uses the distance itself" in `sec:method:model` (`method_reward_comments.md` A1 to A3).
- **"Yielding is cheaper than a detour" holds only per step.** Over a route a detour costs c_move per extra step and a wait c_wait, so a detour is cheaper ([A80] measured it) (A4).
DISCUSSION:
- Step costs make a detour cheaper than a wait of the same length, which fits the back and forth seen at fleet 32 (`method_reward_comments.md` A4).
- Shaping is potential-based only within a task ([A90]), so policy invariance holds only within a task (A3).
CARRY:
- n_deliver is paid per task, Knippenberg pays once per episode. Check `app:cal:reward` and Appendix B (`method_reward_comments.md` B2).
- gamma 0.99 and n_deliver, n_blocked, n_crowd = 10, 0.5, 0.1 are fixed in every config, Appendix B says TBD (D1).
- One name for being overridden ("overridden", "the override term") if the author agrees (C1).
- Who pays in a lock (resolution A2), settled by the code: the agent whose move is refused pays c_wait + n_blocked, an agent that chooses to wait pays c_wait.
OPEN: `method_reward_comments.md`: A1 to A5, B1 to B4, C1 to C4, D1 to D3, E.

### appendix_H_horizon (fixed 4, A108)
MISTAKES:
- **Appendix H horizon.** Every reported run uses T = 10000 with 5000 left out (E, G, L, Experiments). Appendix H says "at least 2000" with TBD values, `5.Experiments.tex:177` says "warm-up of TBD". D22's 5000 has no GAPS entry (`appendix_H_horizon_comments.md` A1).
- **The stall.** The code's `stalled` is the fleet-level gap with no task finished (`evaluator.py:694`, D18). The PF and Appendix H define it as one agent holding a task and standing still. `experiment_config.py:99` says the agent version (A2).
- **Appendix H figures.** H.1 to H.3 come from the deleted graph v1 runs of 24 Oct. H.2's "after the warm-up" is false, H.3 does not match the current E rows (A3).
DISCUSSION:
- The fleet-level stall gap depends on the load more than on the fleet, so one stall length is not neutral (`appendix_H_horizon_comments.md` A2).
- Measured windows of 5000 steps cover about 1.25 demand cycles of 4000, not whole cycles as D10 asked (B1).
CARRY:
- PF `sec:pf:measures` stall paragraph follows the A2 decision.
- `5.Experiments.tex:177` warm-up TBD becomes 5000 once A1 is decided.
- `E.Load.tex:282` says every measure counts after the warm-up, but `longest_stand_still` does not.
- `welch.py` cuts on pick service time, Appendix H says backlog (B2).
OPEN: `appendix_H_horizon_comments.md`: A1 to A4, B1 to B3, C1, C2, D1 to D3, E3.
FIXED: H.Horizon.tex measures leave out the warm-up; "a agent" typo; stall ref sec:impl:logging -> sec:pf:measures; two source comments.

### method_training (fixed 3, A108)
MISTAKES:
- **Main training setup.** `sec:method:training`, `sec:exp:setup` and Appendix J say the fixed-only policies give the main result. Appendix L and the main-text gain use each rule's own policy, and the fixed-only policies were never played under demand storage with the served share (`method_training_comments.md` A1).
- **Training numbers.** `sec:method:training` gives 500 000 steps on 2000-step episodes, which matches `main`. The fleet 16 policies now trained are a warm start plus 2 000 000 steps on 16 000-step episodes (`feat/warm-start-a93`, no GAPS entry). Update the section, Appendix B and the Experiments once these are the tested policies (A2).
- **Critic reason.** A global critic cannot teach the decentralised learner the cost it causes others under its own-reward credit. That reason belongs to the credit (A3).
DISCUSSION:
- The decentralised controller never learns the cost it causes others because of its credit, not its critic (`method_training_comments.md` A3).
- One training run per controller and rule, so training under a rule cannot be told apart from a luckier run (check the Discussion has it).
CARRY:
- Closing paragraph of `sec:method:controllers` and the Experiments' "A shared reward for the decentralised controller" should name the credit (`method_training_comments.md` D1).
- "Setups" against "regimes", pick one (C4). Training, validation and test seeds everywhere (C3).
- `references.bib` entry `rllibmultiagent` needs `{{Ray Team}}`.
OPEN: `method_training_comments.md`: A1 to A3, B1 to B4, C2 to C4, D1 to D4, E.
FIXED: "router" -> "controller"; critic "sees the same window as its own policy"; broken \nref sentence on coupling.

### appendix_J_training (fixed 4, A108)
MISTAKES:
- **Appendix J Method.** It plans an L sweep (0 to 5), widths 32/64 and a fleet 8 budget read off learning curves. Every run uses L = 2, width 32 and 500k on 2000-step episodes, and fleet 16 was retrained with a warm start plus 2M on 16 000-step episodes (`appendix_J_training_comments.md` A1).
- **Appendix J, PPO loss.** RLlib's default KL penalty (kl_coeff 0.2, target 0.01) and the value-loss clip of 10 are on in every run and not mentioned (A3).
- **Appendix J tables.** "of 10" validation seeds against 5 in the code. Table J.1 lacks the messages arm and lists untrained fleets (A4, A5).
DISCUSSION:
- Fleet 8 and fleet 16 are trained differently, fleet 16 with a warm start and 16 000-step episodes (`appendix_J_training_comments.md` B3).
- The PPO loss includes RLlib's KL penalty, which Schulman's best variant does not (A3).
CARRY:
- The warm-start code (`--init-checkpoint`) is not on `main` (B3).
- Appendix B lists the PPO values, L, width and budget as TBD, while every run uses fixed values.
OPEN: `appendix_J_training_comments.md`: A1 to A5, B1 to B4, C1 to C3, D1 to D3, E1, E2.
FIXED: Knippenberg layer sentence; checkpoint "throughput" -> "served share" in reporting; TODO comment 5 validation seeds; Fig J.1 caption.

### appendix_K_checks (fixed 3, A108)
MISTAKES:
- **Where the checks run.** `sec:impl:validation` says "Four checks run on every experiment". In the code checks 1 and 2 run every step in training (`training/callbacks.py`), the test runs (`evaluator.py`) run none, checks 3 and 4 live only in the unit tests, and CI is commented out. Appendix K is fixed ([A108]). Check the Implementation agent fixed VII-D (`appendix_K_checks_comments.md` A1).
- **The stall** (same as Appendix H A2): code flags a fleet-level stall, PF line 1402, Table B.5 and K.1 say per agent. D18/[A67] never reached GAPS (A2).
DISCUSSION:
- The correctness checks ran in training and in unit tests on small instances, not on the test runs (`appendix_K_checks_comments.md` A3, A4).
CARRY:
- Table K.2 and Fig. K.1 are placeholders. Decide what each reports before the Results.
- The stall definition must agree in the PF, Table B.5, Appendix H (`app:cal:stall`) and Appendix K once decided.
OPEN: `appendix_K_checks_comments.md`: A2 to A6, B1, B2, C1 to C3, D1 to D3, E1.
FIXED: "run on every experiment" (two places); broken sec:impl:instances ref -> sec:exp:setup.

### method_reference (fixed 3, A108)
MISTAKES:
- **Token Passing in the loop.** *Done 24 Nov ([A123]): the loop now says Token Passing selects its own tasks.* In the Method opening, steps 2 and 3 do not hold for Token Passing. It assigns its own tasks in its token round (`SelfAssigningPlanner.assign`) and in step 3 follows its planned path, not a window of Table IV (`method_reference_comments.md` A3, extends `method_storage_comments.md` A3).
- **Fixed [A108].** `sec:method:reference` said Token Passing runs only under demand storage, and called it "kept as published" although its vertex rule is stricter than Ma et al.'s.
DISCUSSION:
- The reference is the only controller whose gain can be measured, and it also sets the main load. Say why (`method_reference_comments.md` A4).
- The workstation queue under Token Passing and the lock under the learned controllers are two sides of the same one-lane workstation (A5).
CARRY:
- The [A91] reason why Token Passing never locks, proposed sentence in `method_reference_comments.md` B2. Then drop "plans ahead" from `sec:method:resolution`.
- "Router" is still used in `sec:impl:cost`, App. A notation and the Conclusion. Check against "controller" (C2).
- "Chooses its own tasks" is said in three places. Keep two (D3).
OPEN: `method_reference_comments.md`: A3 to A5, B1 to B4, C1 to C5, D1 to D4, E1.

### appendix_F_demand (fixed 3, A108)
MISTAKES:
- **Appendix F, order or pick.** The demand sweep reads the gain on the pick, the thesis result is the order ([A68]). The order gain from the same rows is 14.1, 17.5, 17.7 and 14.6 percent at 8, 16, 32, 64 agents. Text now says pick, reporting the order gain is open (`appendix_F_demand_comments.md` A1).
- **The Zipf share.** `sec:impl:instances` and Appendix F say a SKU is asked for in proportion to 1/(r+1). The code renormalises within the order's section and draws lines without replacement, so from 16 agents on the overall share is flatter (A2).
- **"Cool down".** `5.Experiments.tex` ("The orders") still says the most popular SKUs cool down. The code drops the top SKUs to the bottom in one step. Fixed in F (A3).
- **Appendix B.** Demand skew "open" while the drift is "tested", though `app:demand:sweep` sweeps both. Lines per order "TBD", code uses 1 + Poisson(4).
- **`sec:impl:instances` prints as "VIII-A0c"**, because the label is on a paragraph (C1).
DISCUSSION:
- Demand storage's gain is measured under Token Passing only. A pick there mostly waits for its workstation, so a fifth less travel gives only 10 to 14 percent in service time.
- At 8 agents there is one section, so storage has no single target there. The gain at 8 comes from other changes (`appendix_F_demand_comments.md` A8).
CARRY:
- If the order gain is adopted, Fig. F.1 and `app_demand_sweep.png` follow.
- "The same sweep" and "the initial run": check Appendices E and G use the same two run names.
- The pilot sentence is repeated in `5.Experiments.tex`. Keep it once.
OPEN: `appendix_F_demand_comments.md`: A1, A2, A5 to A9, B1 to B3, C1 to C4, D1 to D3, E1.

### appendix_I_reward (fixed 7, A108)
MISTAKES:
- Same as method_reward: `sec:method:rl` still writes Phi = -eta and the shaping guarantee ([A89], [A90] no GAPS entry) (`appendix_I_reward_comments.md` A4, A6).
- Appendix B lists d_obs, n_deliver, n_blocked and n_crowd as TBD (sweep). Every trained config uses 5, 10, 0.5 and 0.1, and no GAPS entry settles them.
DISCUSSION:
- d_obs comes from van Knippenberg's yard graphs, where 5 is the largest depth tested, not a shown optimum.
- Messages carry information from beyond d_obs to a decentralised agent (`appendix_I_reward_comments.md` A5).
- n_blocked mostly acts on the decentralised controller (B2).
CARRY:
- One name each for d_obs, the delivery reward and the override penalty across the Method and the appendices (C1, C2).
- "Window" only for what one decision sees, "field of view" for the d_obs range.
OPEN: `appendix_I_reward_comments.md`: A5 to A7, B1 to B4, C1, C2, C4, D1 to D4, E1, E2.

### appendix_E_load (fixed 3, A108)
MISTAKES:
- **Appendix E capacities.** Found with the old keep-up check. The [A96] served check gives 0.175, 0.35, 0.6, 1.2, so the main loads sit at about 0.5 of capacity, not 0.6 (`appendix_E_load_comments.md` A1, open item in `SESSION_CONTEXT.md`).
- **"Section VIII-A0c".** `sec:impl:instances` is a `\paragraph` label (`5.Experiments.tex:63`), so every reference prints the paragraph counter (C1).
DISCUSSION:
- The main loads are set by Token Passing's workstation wait, so the learned controllers run at a load picked for a planner that idles (`appendix_E_load_comments.md` B4).
- The learned controllers can lock at a workstation ([A91]). Compare the two waits (B3).
- f_up = 0.8 is loose and passes overloaded rates. The backlog trend carries the real check (B2).
CARRY:
- Once A1 is decided, check the trained-run tables and the Experiments say the right share of capacity.
- `tab:evalparams` (Appendix B) and VIII should list f_up and the main loads as E does.
- `results/E_load/README.md` says 67 to 156 and 30 to 56, the rows give 68 to 157 and 32 to 56.
OPEN: `appendix_E_load_comments.md`: A1, A3, A4, B1 to B4, C1 to C7, D1 to D4, E1, E2.

### appendix_L_results (fixed 5, A108)
MISTAKES:
- **Checkpoints changed in the served replays.** The served replays chose checkpoints again on 2 validation seeds, so they no longer match the 5-seed choice. At 16 agents decentralised fixed (19 to 24), at 8 agents five arms. Appendix L rows mix the two. [A96] said chosen checkpoints stay (`appendix_L_results_comments.md` A1).
- **Validation against test.** Fig. L.2, the p. 3 paragraph and `5.Experiments.tex:582` compare validation with the old test count. With the revised count the gap mostly goes (A2).
- **Order service time.** The code counts an order from its first task release, the PF from the order's release (A6, record in #103). The `metrics.py` comment `mean_service_time  # zeta_bar_T` is out of date since [A68].
DISCUSSION:
- Regime 1: the storage rule alone changes nothing measurable for all four controllers at 16 agents.
- The "trained under the rule" effect holds for only two of the four (`appendix_L_results_comments.md` A5).
CARRY:
- Fill the 8-agent tables, Table L.10 and the Table L.6 8-agent centralised fixed cell (0 / 0) once A1 is settled.
- Redraw `fleet16_served.png` and `fleet16_val_vs_test.png` from `served_counts.py`.
- Check `tab:exp:served` and `tab:exp:locks` use the same checkpoint as Appendix L.
OPEN: `appendix_L_results_comments.md`: A1 to A6, B1 to B3, C1 to C4, D1 to D4, E1, E2.

### implementation (fixed 5, A108)
MISTAKES:
- **Fixed [A108].** **Correctness checks** in `sec:impl:validation` no longer say "every experiment" (Appendix K fixed too) (`implementation_comments.md` A1).
- **Load levels.** `sec:impl:logging` points to E.4.4 for the load levels and f_up. E.4.4 only sets f_up, the Token Passing run is E.4.5. Its main loads (0.105 to 0.24) differ from `tab:evalparams` (0.15 to 0.4, from [A31]) (A4).
- **Runtime.** The test runs use the CPU, the GPU runtime comes from the separate [A95] run. kappa_T is assignment plus routing, and routing includes building the observations (A5).
DISCUSSION:
- The correctness checks cover the hard rules only, not the storage rules, observations or reward. Say what checks the rest, or name the gap (`implementation_comments.md` A8).
CARRY:
- Knippenberg Table 4 as one careful clause in `sec:impl:cost`. It counts solved instances, not time per decision (B1).
- kappa_T has one name in Results ("runtime"), and Results says which run it was measured on (C1, A5).
- "Learned routers" and "learned controllers" are both used. Check later chapters.
OPEN: `implementation_comments.md`: A1 to A8, B1, B2, C1, C2, D1, D2, E1.

### appendix_B_parameters (fixed 8, A108)
MISTAKES:
- **Appendix B values the runs used.** zones p = 3, L = 2, widths 32/32, minibatch 128, 5 epochs, entropy 0.02, value loss 1.0, rollout one episode, seeds 250/5/20, budget 500 000 (fleet 16 long 2M more), test horizon 10000 with 5000 left out, reward weights 10/0.5/0.1, lines per order 1 + Poisson(4). B still shows these as TBD (`appendix_B_parameters_comments.md` A6 to A14). Fixed [A108]: gamma, d_obs, the three cited PPO values, 20 test seeds, the main loads.
- **Main loads, check.** B now gives 0.09, 0.18, 0.3, 0.6 "at 0.6 of capacity" (configs). Appendix E says these are 0.5 of capacity under the [A96] check, and the Implementation review read 0.105 to 0.24 from E.4.5. Settle one set and one share.
- **Config headers.** The `slap-mapd-coupling` config headers call the arm, model and PPO sections "illustrative, not thesis values", but the trained runs used them.
CARRY:
- "Router" still in B.3, `4.Implementation.tex`, `5.Experiments.tex:176` and `A.Notation.tex`, against [A106].
- The [A91] lock rule (500 steps) has no parameter row. Check the Experiments define it.
- The RQ3 load levels are TBD in the Experiments and have no row in B.
OPEN: `appendix_B_parameters_comments.md`: A6 to A15, B1 to B6, C1, C3 to C7, D1, D2, E1.

### appendix_G_storagevalues (fixed 5, A108)
MISTAKES:
- **Appendix G congestion rows.** Fleets 32 and 64 of tp-a93 finished 14 Nov but are not merged. `results/G_storage/fleet_32` and `fleet_64` still hold the edge rule. Merge with `merge_a93_period_rows.py`, add the rows to `tab:app:beta`, and correct "less than 2 steps" and "largest at 50" (`appendix_G_storagevalues_comments.md` A1).
- **Trip legs reach Appendix G.** The Setting sentence, the "step for a step" reason of `app:cal:beta` and the fixed-storage overflow. Add Appendix G to Part 5 of `review_trip_legs.pdf` (A2).
- **`B.Parameters.tex`** Delta row still says "half the rotation period". Use "drift period".
DISCUSSION:
- beta = 1 was checked only under Token Passing, where omega-hat is 1 to 2.5 steps. Under the learned controllers it is 21 to 32 steps, as long as a trip, so beta decides the score there untested (`appendix_G_storagevalues_comments.md` B2).
- The safety stock overshoots its 1% aim (0.1 to 0.3%), so stock waits are smaller than intended (A4).
CARRY:
- "Refill" is still the axis label of Fig. G.2 (`appendix_storage.py`), against [A103].
- Run names (pilot, first sweep, initial run, updated run): check Appendices E and F use the same four.
OPEN: `appendix_G_storagevalues_comments.md`: A1 to A5, B1 to B5, C1 to C6, D1 to D4, E1 to E3.

### appendix_A_notation (fixed 10, A108)
MISTAKES:
- PF "Keeping up" says the backlog holds "orders still waiting for stock" (`3.ProblemFormulation.tex:1342`, `:1391`). The code counts waiting order lines (`evaluator.py:565`). Table fixed [A108] (`appendix_A_notation_comments.md` A5).
- `styles/eqnames.tex` had no entry for `eq:relativeeta` (main session adds it).
- App C `app:measures:blocked` (`C.ModelDetails.tex:247`) refers to omega-hat as "of eq:storageupdate". It should be eq:standstill.
- PF `sec:pf:agents` (`3.ProblemFormulation.tex:87`) writes the fleet as plain A (A10).
CARRY:
- One name per idea: "demand estimate" or "order estimate" for rho-hat; "parking vertex" or "endpoint"; "end vertex" in `sec:method:reference` (after [A105] "where the task delivers"); "storage epoch" or "storage update"; "storage vertex" in App C:23.
- Symbol clashes to settle once, then apply to chapters, figures and table: w, message, zone/section, h(k) as "home", B_t against calligraphic B_t, Q against calligraphic Q_t, q_i(t) against q_j, v_1/v_2 in the pickup rule (C2 to C9).
- Missing rows: d^trip_t(k,v), pi_theta, m_v^(r), gain_n, x^new, C^pick_T.
- `Chapters/2.Notation.tex` duplicates `tab:notation` with the same labels and is not included. Delete it or keep it in sync (D4).
- `AGENTS.md` and `SUBAGENT_BRIEF.md` point to `notation_renames.md`, deleted on 2026-10-16 (D5).
OPEN: `appendix_A_notation_comments.md`: A5, A9 to A11, B1, C1 to C13, D1 to D5.

### appendix_C_modeldetails (fixed 11, A108)
MISTAKES:
- **Crowding read by a controller.** PF V-G (`3.ProblemFormulation.tex:1074`) and Appendix C.2.2 say a zone or the centralised controller reads the delta_j of its agents. Every network reads only its own delta_i (`gnn_encoder.py` readout) (`appendix_C_modeldetails_comments.md` A1).
- **Randomness of P.** V-H says the only randomness is the arrival of orders (`3.ProblemFormulation.tex:1209`), and `sec:method:resolution` says the same. The dock of each put-away and shipment is also drawn at random (`multi_agent_env.py:899`, `:919`). Fixed in Appendix C ([A108]), PF still needs it.
- **One-step cost.** c-hat(v,w) (C.7) is used nowhere, and a move is charged c_move, not c(v,w) (A3).
CARRY:
- PRIMAL masks invalid actions in training. Credit it in the mask sentence of VI-C (`appendix_C_modeldetails_comments.md` B1).
- "Boundary protocol" still in `A.Notation.tex` and `2.Notation.tex`.
- "Distance label" against "direction to target": one name.
OPEN: `appendix_C_modeldetails_comments.md`: A1 to A3, B1 to B3, C1 to C3, D1 to D6, E1.

### appendix_D_warehouses (fixed 10, A108)
MISTAKES:
- **Fixed [A108].** Appendix D shelf count, parking placement, Table D.1 and the Results numbers predated [A77]. Rerun report kept in `thesis-progress/results/D_warehouses/instance_report_2026-11-20/` (`appendix_D_warehouses_comments.md` A3).
- Figs. D.2 and D.3 show the warehouse before [A77] (|V| = 348 at 16 agents, workstations not grouped in fours). Redraw in the [A104] viewer style (A4).
- `5.Experiments.tex`: "The rack faces left over become parking spots" is wrong (only m of them, the rest are not built), and "11 to 34 steps" at 8 agents predates the sections (now 17 to 38).
- `4.Implementation.tex` storage section says shelf ties are broken by index. The code breaks them by d^trip first, then by index (`_refill_scores`) (A9).
- Zones are bands of consecutive aisles through every block, p = 3, independent of the SKU sections. About 10 to 15 % of sections straddle two zones (A6, adds to `method_controllers_comments.md` C1).
DISCUSSION:
- Section-based zones do not follow the SKU sections or the blocks. One section's workstations can sit in two zones, and at 8 agents three zones share one section.
CARRY:
- Appendix D should name and draw both sections and zones, and say they are independent.
- Van Knippenberg (Section 4, Fig. 4) is the source for the one-way central pair, the links and the leaf goals. Check `sec:impl:instances` credits him the same way.
- 16 vertices per agent matches his 1024 nodes at 64 agents only. Check places that cite him for "the size".
OPEN: `appendix_D_warehouses_comments.md`: A3 to A8, B1 to B5, C1 to C4, D1 to D6, E1.
