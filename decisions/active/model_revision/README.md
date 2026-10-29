# Model revision after the queue of 2026-10-23

Agreed with the author on 2026-10-26, in one discussion that read the results of the two-day queue
(`../../../notes/queue_findings_2026-10-26.md`). The queue showed that several results came from how the
model was built, not from the question. This folder is the plan for fixing that, one file per step, so each
step can be handed to another session.

Steps 01 and 02 are applied. Every step that changes the model gets an `[Axx]` tag in the
chapters and an entry in `../../GAPS.md`. The last tag used is `[A62]` (graph v2). The tags below are proposals, to be
given out in the order the steps are applied.

## Why

| what the queue showed | cause | step |
|---|---|---|
| random storage as good as demand storage, the gain all in waiting, none in travel | few shelves (m/2) on the through-aisles, delivery spread inside, so distance hardly varies (11 to 15 steps at 8 agents) and robots queue at shelves under Token Passing | 02 |
| ε changes nothing, shelves 78 % full at 8 agents and 16 % at 64 | the floor x_min = 8 per SKU sets almost all stock | 04 |
| demand storage's put-aways fail at 32 and 64 agents | a put-away carries one period's units of one SKU, so about 4 in 10 robot trips are put-aways | 05 |
| unit sizes and shelf capacity have no clear purpose | follows from the two rows above. Sizes stay, for room only, and the capacity must hold one refill | 05 |
| the gain moves with the horizon, and changes sign at 16 and 64 agents | the mean counts the empty start, and 2000 steps is half a demand cycle | 06 |
| "delivery" names both a role and the end of every task, so a put-away's delivery vertex is a shelf | naming | 03 |
| training slow at 32 agents (540 s per iteration) | the learner ran on the CPU, the GPU was idle (`--gpu` not passed) | 10 |

## Decisions

| | decision | step |
|---|---|---|
| D1 | Van Knippenberg et al.'s (2021) principles on our warehouse backbone, not their yard layout. Graph v1 results are kept as archived evidence | 02 |
| D2 | Every endpoint (slot, workstation, dock, parking) is a leaf, a vertex with one edge, off the through traffic | 02 |
| D3 | A pair of one-way main aisles in the centre of the rack area, with no endpoints on them | 02 |
| D4 | U-flow. Workstations on the front wall, docks grouped near one front corner on the side wall | 02 |
| D5 | Rack faces on both sides of every aisle vertex, plus slots on the rack side of the front lane. Slots hold several SKUs | 02 |
| D6 | 16 m walkable vertices, leaves added on top. Parking leaves on the side walls | 02 |
| D7 | Rename delivery vertex to workstation and receiving vertex to dock, in text and code. Task ends stay pickup and delivery | 03 |
| D8 | Remove x_min. Replace ε by a service level, the textbook way. Unit sizes stay, for room only | 04 |
| D9 | Stock arrives in fixed refills of Q units once Q has been picked, one delivery per Δ, one refill one put-away. Named a refill, standing for a pallet or case. Put-aways stay lifelong MAPD tasks. The demand rule ranks by demand and the text says so | 05 |
| D10 | Horizon by Welch's method: cut the warm-up, measure over whole demand cycles | 06 |
| D11 | Assignment stays oldest first for picks and put-aways alike, with the reason in one clause | 07 |
| D12 | Δ = 100, half the rotation period. β = 1, a step of waiting weighs the same as a step of travel | 07 |
| D13 | ~~Packing, holding an order until its last line, and the trip to outbound are outside the model~~ Replaced by D21 (2026-10-27). Packing stays outside | 07 |
| D14 | Reproduce Ma et al.'s (2017) Token Passing results on their grid warehouse, loaded as a graph | 08 |
| D15 | Figures: the instance in van Knippenberg's style next to the grid drawing, and the stock per slot at a few moments | 09 |
| D16 | Train on the GPU first, and keep leaves out of the router's window only if that is not enough | 10 |
| D17 | Fixed storage stays the reference of the main result. Random storage is only a check, under Token Passing in appendix G: is demand's gain due to demand information or only to spreading stock | 07, 11 |
| D18 | The stall is defined at fleet level: no task finished by anyone for X steps, one X for every fleet size | 06 |
| D19 | ~~Every fleet starts with its shelves 0.4 full (`start_fill`), the number of SKUs derived from it, so storage has the same problem at every fleet size. Tested in appendix G~~ Replaced by D22 (2026-10-27) | 05 |
| D20 | The demand ranking rotates by a share of the SKUs (5 % every 200 steps), so it turns once in about 4000 steps at every fleet | 06 |
| D21 | Shipping. When the last line of an order reaches its workstation, one shipping task carries the order from the workstation to a dock drawn at random. The order is done when it leaves at the dock, so its service time includes the trip out. Refills also come in at a dock drawn at random. The workstation holds whatever arrives, with no capacity and no processing time. Shipping is an ordinary task, assigned like picks and put-aways. Orders keep several lines (author, 2026-10-26 and 2026-10-27) | 12 |
| D22 | One start for training and evaluation. Every SKU starts on one slot drawn at random, holding its S_k units (step 05's service level), so half the slots start empty and the start carries no demand information. Evaluation adds a warm-up of about 5000 steps before scoring, so the refills placed by the storage rule replace the random start. The stall (D18) is checked only after the warm-up. Replaces D19 and the empty start of 2026-10-26 (author, 2026-10-27) | 12 |
| D23 | ~~Training starts with random stock, evaluation empty~~ Merged into D22 (2026-10-27) | 12 |
| D24 | The workstations are rack faces drawn at random anywhere in the warehouse, per seed, instead of spread along the front wall. The docks are spread evenly along the whole left wall, front to back, instead of grouped at the front left corner, so inbound and outbound traffic also enters through the middle (author, 2026-10-27) | 12 |
| D25 | Slots = 2 x SKUs, spread evenly over the rack faces left after the workstations, the rest become parking leaves or are removed. The SKU count and Q follow from measured throughput: a middle-ranked SKU is refilled about 4 times per demand cycle. Slot capacity holds S_k of the most popular SKU. One SKU per slot only at the start, later a slot holds several (D5). Orders stay drawn over every SKU, the service level keeps them in stock, test B reports the share of lines that waited | 12 |
| D25, sized | Q = 12 units at every fleet, so put-aways are the same share of trips everywhere. A line takes one pick and 3 / Q put-aways, an order of L lines one shipment, so put-aways are (3 / Q) / (1 + 1 / L + 3 / Q) of trips, 17 % with the 5 lines per order of `[A46]` (11 % with one line). The rerun switches multi-line orders on, `lines_per_order: {distribution: shifted_poisson, mean: 5}`, since `configs/step12/` set none and every order of the sweep had one line. The SKU count follows the main load, n = 250 x main load rounded to a multiple of 20, which gives every SKU about 4 refills per 4000-step demand cycle (12000 x load / (n Q)) and keeps the 5 % rotation share a whole number of SKUs, so the ranking turns once in exactly 4000 steps (D20). At today's main loads n = 20, 40, 40 and 60 at 8, 16, 32 and 64 agents, 40, 80, 80 and 120 slots, all within the rack faces left (45, 95, 174, 368 on the tightest of 20 warehouses). "Middle-ranked" in D25 reads as the mean over the cycle, since the rotation takes every SKU through every rank. Re-applied once to the main loads of the rerun. Arithmetic and check in `results/tests/step12_sweep/README.md` (author, 2026-10-29) | 12 |
| D25, safety stock | Every SKU's safety stock is sized at the most popular rank: S_k = Q + the 99 % quantile of one epoch's units at rank 0, for every k, instead of at the SKU's rank at t = 0. The rotation takes every SKU to the top once per cycle, so only this keeps the service level over the whole cycle. Checked on fleet 8 at Q = 15: the orders that waited for stock fell from 5.7 % to 0.0 % and picks got 14 % faster, for a mean shelf fill of 24 % against 17 %. It overshoots the 1 % aim, which is accepted. Code (`refill_starting_stock`) and thesis text still to do (author, 2026-10-29) | 12 |
| D26 | Idle robots of every controller follow Token Passing's parking rule. When a waiting task needs the vertex an idle robot stands on, the nearest free parking leaf becomes its target, reserved for it. Replaces the own-vertex target of issue #102 for idle robots. The thesis line "waits at an endpoint, where it blocks no one" then holds for every controller (author, 2026-10-27) | 12 |
| D26, refined | An idle robot (no task) goes to the nearest free parking leaf only when it is in the way: its vertex is the pickup or delivery of an unfinished task, or another robot tried to move onto it this step and was stopped. A robot in nobody's way stays (author, 2026-10-27) | 12 |
| D27 | A new warehouse every episode. The episode seed draws the layout (aisle lengths, links, workstations) and the start stock. 250 training warehouses, one per episode of today's budget (500 000 steps of 2000-step episodes), built ahead of time. Validation and test seeds have their own warehouses, never trained on. Fixed and demand storage play the same warehouse per test seed. Closes the gap with Appendix D ("one seed always gives the same warehouse, which the split into training and evaluation seeds relies on"), where the code fixed one warehouse per fleet (author, 2026-10-27) | 12 |
| D28 | The warehouse grows by stacking rack blocks of a fixed depth, 4 rack rows, with a two-way cross lane between neighbouring blocks and the one-way pair in the middle, instead of deeper blocks around one pair. Every inner aisle segment, in every block, hangs from the lane on the side of the pair at a length drawn from the seed. 6 aisles and 2 blocks at 8 agents, 7 and 4 at 16, 10 and 6 at 32, 15 and 8 at 64 (author, 2026-10-27, after the irregular lower block of the same day) | 12 |
| D29 | Each SKU belongs to one workstation, option (a) of the random-workstation gap ("Still open", 2026-10-29). An order goes to one workstation and draws all its lines from that workstation's SKUs, so a SKU has one place it is needed. There are W = n / 10 workstations, each owning 10 SKUs, so an order of 5 lines takes about half of them: 2, 4, 4 and 6 at today's SKU counts, against 4, 8, 16 and 32 before. Every 1000 steps two SKUs of different workstations swap, about 4 swaps per 4000-step demand cycle, a new setting the sensitivity sweep can vary. Fixed storage knows the starting link only, its class-based homes (`[A69]`) sit near each SKU's starting workstation and never move, so the gain measures what following the swaps and the rotation is worth. Defaults, confirmed by the author: SKUs dealt to the workstations in turn by starting rank, so each owns the same mix of popular and slow SKUs; an order picks its workstation in proportion to the current demand of its SKUs, so each SKU's demand stays Zipf; the second leg of `eq:tripdistance` becomes the distance to the SKU's workstation, which demand storage reads from the lines of its window like its demand estimate. Replaces random workstations per order (D24 keeps the random rack faces) (author, 2026-10-29) | 12 |

## Still open

- **Found 2026-10-29, an order's workstation is random, so storage has no place to aim for.** Raised by the
  author after the step 12 sweep. Every order draws its workstation at random
  (`multi_agent_env.py`, the order release), and since D24 the workstations sit on random rack faces all over
  the warehouse. The rules still score a shelf by its distance to the nearest workstation (`eq:tripdistance`,
  second leg, and `access_distance` in `storage/demand.py`). The thesis calls that leg "a stand-in for the
  delivery trip" that ranks a shelf by "how close it sits to the delivery side" (`4.Implementation.tex`,
  line 65, `[A55]`). With workstations spread at random there is no delivery side any more. Measured on 5
  step 12 warehouses per fleet: the best fifth of shelves by the rule lie about 3 steps from their nearest
  workstation, but 11, 16, 24 and 34 steps on average from the workstation an order uses, against 12.5, 17,
  25 and 35 for an average shelf, at 8, 16, 32 and 64 agents. So the rule's best shelves are only 3 % to
  10 % closer in practice, and even the best shelves for a random workstation are only 10 % to 21 % closer.
  The same reasoning made `[A70]` take the mean over the docks for the first leg. The proposal is that each
  workstation keeps needing the same items, fixed or changing slowly, so an item has a real place to be
  close to. Ways to define it, not agreed:
  - (a) Each SKU belongs to one workstation. An order goes to one workstation and draws its lines from that
    workstation's SKUs, and at each rotation a few SKUs move to another workstation. The simplest.
  - (b) Each workstation has its own popularity ranking, overlapping the others by a set amount, rotating
    slowly.
  - (c) Keep random workstations and score the second leg by the mean over the workstations, as `[A70]`
    does for the docks. No model change, but storage then matters little for the trip to the workstation.

  **Decided 2026-10-29, option (a), see D29.** Fewer workstations (W = n / 10), fixed storage knows the
  starting link only, and two SKUs swap workstations every 1000 steps. Code and thesis text still to do,
  with an `[Axx]` tag, before the step 12 sweep is rerun. Overview of the sweep:
  https://claude.ai/artifact/8tht3tBrq9Agtp7Vi4Y9sw (question 2).
- **Found 2026-10-26, idle robots of the learned routers.** Token Passing parks an idle agent on the
  nearest free parking leaf when a waiting task needs the vertex it stands on as its delivery vertex, and
  otherwise leaves it where its last path ended (`planners/token_passing.py`, rules 2 and 3). Its no-deadlock
  guarantee rests on this, so the parking leaves stay while it is the baseline. The learned routers have no
  such rule. A free robot's target is its own vertex (`environment/reward_function.py`, issue #102), so it
  stays where it stopped, often on the workstation or dock leaf of its last task, and gets no signal to
  leave. The thesis says every idle robot "waits at an endpoint in V_ep, where it blocks no one"
  (`2.Introduction.tex`, line 141), true for Token Passing only. Not yet checked how often a learned robot
  blocks a leaf another robot needs, or what conflict resolution does then. Proposed, not agreed: Token
  Passing's rule for every controller, the nearest free parking leaf becoming the idle robot's target only
  when a waiting task needs its vertex. A model change, so an `[Axx]` tag and its own step file once agreed.
- The crowding weight of the reward, n_cng = 0.1 now. Proposed n_cng = c_wait = 0.2, a fully crowded window
  costs one step stood still. Only training can show whether it changes behaviour, so it waits for the reruns.
- The learned storage policy stays a maybe (author, 2026-10-26). The policy exists (`~/worktrees/pilot-learned-storage`).
  On graph v2 it has a real distance lever to learn. One pilot after the first rerun (`11_reruns.md`), adapted to
  place refills, then decide whether it enters the thesis.

## Order of work

One step at a time, each in its own session with its step file as the brief, and a test after each before the
next starts (author, 2026-10-26). The tests come early so each big risk below is seen before the next big piece
of work.

1. **01** is done. Update `RUNS.md` when convenient.
2. **02 graph.** Then **test A**: Token Passing on graph v2 with today's arrival rule, 8 agents, fixed, demand
   and random storage, 20 seeds. Does demand beat random on picks, and does travel per pick drop? (risk 2)
   *Done 2026-10-26.* PRs #193 (graph v2) and #194 (random rule), thesis text `[A62]`. Answer: no. Demand
   beats fixed by 14 %, random beats fixed by 18 %, travel per pick drops by under a step
   (`../../../results/tests/A_graph_v2/README.md`).
3. **04 stock and 05 refill**, together, one session, with `05_refill.md` as the brief. Then **test B**: test A again. What does the refill rule change, and
   how many storage decisions does a run still have? (risk 3)
   *Code done 2026-10-26*, uncommitted in `~/worktrees/refill` (branch `feat/refill`, on `main` with PR #194
   cherry-picked). Test B postponed by the author. Decisions taken on the way are in `05_refill.md`.
4. **06 horizon and the stall.** Then **test C**: Welch runs at each fleet under fixed storage. Does the
   warehouse settle at the candidate load? (risk 4)
   *Code done 2026-10-26*, uncommitted in `~/worktrees/refill`. Test C not run. See `06_horizon_welch.md`.
5. **10 step 1 (GPU) and M5** (`../measures_plan.md`). Then **test D**: a short training run on graph v2 with
   `--gpu`, at 8 and 16 agents. Does the learned router learn and keep up? (risk 1)
6. **11 reruns.**
7. As time allows: **03 rename** (its own PR, before or after 02, not mixed into another step), **08 Ma et al.**,
   **09 figures**, **10 step 2**.
8. **07 text reasons** go in with the step each belongs to.
   *Written 2026-10-26*, uncommitted in `thesis/`, each sentence tagged `% model revision 07, Dxx`, for the
   author to approve. See `07_text_reasons.md`, "Written".
9. **08 Ma et al.** *Done 2026-10-26* (tests B and C skipped by the author that day). Code uncommitted on
   branch `feat/ma-reproduction` in `~/worktrees/refill` (on `feat/welch-window`). Rows and answer in
   `../../../results/K_checks/ma2017/`, text in `app:repro:ma`. Within about 10 %, always on the fast side.
10. **12 flow and start** (D21 to D26), agreed with the author on 2026-10-26, evening, and its questions
   settled on 2026-10-27. Brief: `12_flow_and_start.md`. Implementation started 2026-10-27. It changes the model, so tests A to D
   and figures 1 and 2 of step 09 follow it, not the other way round.

## Risks

1. **The learned routers.** On graph v1, 16 and 32 agents were unstable and ended near the keep-up line, and the
   centralised and section arms have not been trained. Graph v2 is bigger. The GPU makes training faster, not
   more stable. The main result is per controller, so this is the biggest risk. Test D.
2. **Demand may still not beat random on graph v2.** A legitimate finding, but the thesis must be framed to carry
   it. Test A.
3. **The refill rule gives storage fewer decisions.** Slow SKUs are rarely refilled, so the starting layout,
   the same under every rule, dominates for longer and the gain may shrink. Q trades realism against effect
   size. Name it, and show it with the Q test in G. Test B.
4. **The warehouse may not settle at the main load.** On graph v1 fixed storage was still slowing at 4000 steps.
   If so, the main load comes down (for example 0.5 of capacity). Test C.
5. **Scope.** Mark each step essential or nice to have once the deadline is known.
6. **Smaller points.** The "non-lattice" claim rests on uneven aisles, dead ends and extra links, which the
   generator must keep. Chapter wording needs the author's approval, with the 60-page limit and the Overleaf
   sync. The Ma et al. numbers may match only within a few percent. Update `SESSION_CONTEXT.md` as steps land.

## Rules for whoever picks up a step

- Read `~/Documents/thesis/CLAUDE.md` and `AGENTS.md` first. The thesis writing style rules apply to every
  sentence that goes into `thesis/`.
- Propose chapter text to the author before writing it. Until now the chapters were left alone and only the
  appendices changed (`appendix_papers_handoff.md`). These steps change the model, so they touch the
  chapters, and the author approves the wording.
- `slap-mapd-coupling` changes go in small PRs from `main`, left uncommitted for the author, who opens the PRs.
  Match the chapters exactly, and do not invent a value they leave open.
- Do not commit or push `thesis/`. It syncs with Overleaf.
- A symbol that is added, renamed or removed changes `thesis/Appendices/A.Notation.tex` in the same change.
- Check a citation in the paper before writing it. Sources named here as "to check" are not checked yet.

## Where things live

| what | where | note |
|---|---|---|
| the model's code | `~/Documents/thesis/slap-mapd-coupling`, `main` at `e1abc67` | the main checkout holds uncommitted M1 to M4 work (`../measures_plan.md`). Do not disturb it, work in a worktree |
| the learned storage policy (code) | `~/worktrees/pilot-learned-storage`, branch `pilot/learned-storage`, based on `5f8dfca` | all uncommitted. New files: `src/slap_mapd_coupling/storage/learned.py` (the rule), `models/storage_policy.py` (its network), `training/storage_ppo.py` (its PPO training and the evaluation, which also holds the random rule, line 456), `scripts/storage_pilot.py`, `scripts/storage_pilot_night.bash`, `configs/pilot_storage/`, `tests/unit/test_learned_storage.py`. It also changes several shared files (`multi_agent_env.py`, `metrics.py`, `gnn_encoder.py`, `token_passing.py` and others), so it must be rebased onto graph v2 and the refill rule before its pilot (the "maybe" of `Still open`). Plan: `../../ideas/learned_storage_pilot_plan.md` |
| the learned storage policy (runs) | `~/thesis_runs/pilot/2026-10-24_1021/` (8 agents and 64 agents, each with `train/` holding `checkpoints/`, `progress.jsonl`, `settings.json`, and `eval/summary.md`), older nights in `~/thesis_runs/archive/storage_pilot_*` | graph v1. The 64-agent stage ran at load 0.42, the old main load |
| the learned routers (checkpoints) | `~/thesis_runs/training/fleet_<m>/<regime>/` (`fixed_only`, `matched`) for 8, 16 and 32 agents, every checkpoint kept | graph v1, the decentralised arm only. No checkpoint chosen by `[A60]` yet. Their progress logs are copied to `thesis-progress/results/J_training/` |
| the learned routers (code) | `slap-mapd-coupling/src/slap_mapd_coupling/models/` (`gnn_encoder.py`, `local_subgraph_encoding.py`, `window_tables.py`, `rl_module.py`) and `training/` | step 10 touches these |
| the graph v1 instances | `thesis-progress/results/D_warehouses/` (instance report, drawings, layouts per seed) | the reference that `layout="v1"` must reproduce (step 02) |
| the Token Passing results | `thesis-progress/results/<appendix>/`, see its `README.md` | graph v1, to move to `archive/graph_v1/` when step 02 lands |
| the papers | `thesis-progress/papers/` (van Knippenberg et al. is `knippenberg21a.pdf`, Ma et al. is `3091125.3091243.pdf`) | |
