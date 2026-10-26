# Idea: a learned storage policy (PPO)

**Status 2026-10-20. Extra, to look into after the long run.** Not planned, not
in the thesis. Raised by the author: is the coupling not meant to be between
two policies, one for storage and one for routing?

**Update 2026-10-22.** The author wants a learned storage policy and to test it
in a pilot PR before deciding. Reward (c) is chosen. The discussion is at the
end of this file, under "Discussion 2026-10-22". Nothing is in the thesis yet.

## The question

Today storage uses three hand-written rules (fixed, demand, congestion-aware)
and only the routers learn. Should storage also be a learned PPO policy, so the
thesis couples two policies?

The project description in `thesis/Chapters/Thesis_idea.tex` holds both
readings. Line 21 says a simple closed-loop heuristic for storage, with
learning as an optional extension. Line 58 says graph-neural policies for both
storage and routing. The Introduction follows the first. Which one was agreed
with the supervisor is still to be checked.

## Case against (the current recommendation)

- **The main result gets muddied.** With a fixed rule, a change in the gain
  between controllers comes from the router. With two learners it could come
  from either side, or from the two adapting to each other.
- **Two learners chase each other.** Each changes the world the other learns
  in, so training is less stable and needs more seeds.
- **The reward arrives late.** A shelf choice pays off only when the stock is
  picked, often hundreds of steps later.
- **The training budget grows**, on top of the four router arms and the fleet
  sizes for RQ4.

## Case for (devil's advocate)

1. **Without it the coupling may not be tested.** The demand rule reads only
   the orders, so traffic never reaches it. The congestion-aware rule placed
   stock as the demand rule did at beta 1. If RQ3 shows nothing, an examiner
   can ask whether coupling was studied at all.
2. **The confound can be designed around.** A 2x2 design crosses rule or
   learned storage with a router trained alone or trained with storage.
   Freezing one side and swapping the other shows whether the two adapted to
   each other, which is the self-organisation the project description names.
3. **The congestion-aware rule is the invented part.** Its score and beta are
   hand-picked, while the costs follow van Knippenberg to avoid invented
   numbers. A learned policy finds its own trade-off between distance and
   traffic.
4. **The late reward is manageable.** Storage acts once per arrival batch
   (Delta 100). The reward can be the service time of the placed units,
   credited when they are picked. Waubert de Puiseau et al. (2022) trained
   this kind of policy with deep RL on real data.
5. **The two learners can take turns.** Fix the router and train storage, then
   fix storage and fine-tune the router. That avoids the moving target and
   costs one extra phase, not a doubled budget.
6. **It speaks to RQ2.** If each router gets a different learned layout, how
   many agents one decision covers changes the coupling itself.

## Weak points of the case for

- Schedule. The long run, the RQ4 sweep to 64 agents and memory reduction come
  first.
- Risk. A learned storage policy that trains badly gives a negative result
  that is hard to read.
- Point 6 needs one storage policy per router, which multiplies runs.

## Middle path, if it is taken up

- Keep the main result (RQ1 and RQ2) on the rules, unchanged.
- Add the learned policy as a fourth storage option in RQ3 only.
- One router, the decentralised one because it is cheapest, trained in turns.
- Decide after the long run, from the RQ3 traffic heatmap. If the
  congestion-aware rule shows nothing, that is the argument for trying this.

## Related

- `../../notes/how_the_system_works.md`, section "Is the storage rule a SLAP?"
- `../active/thesis_plan.md`, section 4.2 (RQ3) and section 10 (order of work)

# My thoughts

If we keep the already existing as the baseline where we have F(\dot), so it does not learn anything and everything is fixed is good. The overall problem is what we are measuring righ now does not really belong in the SLAP or the DSLAP world. Here we either need to know it can apply for counting as a SLAP or DSLAP what we have built first and foremost. When we know that we know which direction to go. 

If this does not account for a SLAP or DSLAP then we would need to create a learned policy, which is what i think no matter what since the study is all about this. If we site the DSLAP and used their update rules and their contruction then we will have the DSLAP in place and can start to train it. 

# Discussion 2026-10-22

## Does what we built count as a DSLAP?

**The decision does.** Waubert de Puiseau et al. (2022) define DSLAP as "where
to optimally store goods upon entry or reentry into the system". The storage
update (`eq:storageupdate`) places stock when it arrives, never moves stock on
a shelf, and keeps every shelf within capacity. `[A48]` already says so.

**The model already admits a learned policy.** The set $\mathcal{F}$ in
`sec:pf:storage` is every admissible way of putting arriving stock away, and
the decision problem ranges over all of it. A PPO policy is one more element
of $\mathcal{F}$. Adding one changes the realisation in Chapter 4, not the
problem formulation in Chapter 2.

**The measure does in part.** SLAP work judges storage by travel cost, and
Waubert de Puiseau use a fixed cost per zone (1, 2 and 10). The result here is
mean service time, a lifelong MAPD measure. The service-time split
(`eq:split`) bridges the two. Its travel part is the SLAP measure, and the
wait before assignment and the blocked time are the MAPD side. Report travel
next to the result. The coupling is then what storage changes in the blocked
time, which a SLAP-only evaluation would miss.

## What carries over from Waubert de Puiseau et al.

They give no update rule to borrow. Ours (`eq:storageupdate`) already plays
that part. What carries over is how they set the problem up for RL.

| Waubert de Puiseau | Here |
|---|---|
| decide when a pallet arrives | decide at each arrival epoch ($\Delta$), per arriving SKU |
| action: zone A, B or C (3 choices) | action: a zone, then a fixed rule picks the shelf inside it |
| full zones masked (masked PPO) | zones without room masked, from the capacity condition |
| observation: zone fill, SKU one-hot, day of year | shelf fill, $\hat\rho_t$, $\hat\mu_t$, $\hat w_t$ on the graph (GCN encoder can be reused) |
| reward: immediate cost of the chosen zone | does not carry over, see below |
| baselines: ABC, random, Just-in-Order | fixed storage, the demand rule |

The small action space is deliberate. Three zones is what made their training
stable. A choice over every shelf would not be.

## Reward: (c) is chosen

Their reward works because a zone's cost is known when it is chosen, and
there is no fleet. Three options were weighed.

- (a) Immediate access cost $D$. Stable, but traffic never enters the reward,
  so the policy learns to copy the demand rule. It does not test the coupling.
- (b) Immediate $\alpha D + \beta K$. Learns to approximate the storage
  objective (`eq:storageobjective`), which is the congestion-aware rule again,
  with $\beta$ still hand-picked.
- (c) The realised service time of the placed units, credited when they are
  picked. The only option where the fleet's traffic drives storage.

**(c) is chosen** (author, 2026-10-22). The cost is a reward that arrives
hundreds of steps late. Option (a) can still serve as a first check that the
setup trains at all, before switching to (c).

## The storage options

- **Fixed**, $F_{\mathrm{fix}}$. Dedicated storage, learns nothing. The baseline.
- **Demand rule**, $F_{\mathrm{dem}}$. Class-based storage by the
  cube-per-order index (Heskett 1963, de Koster et al. 2007). It is the same
  family as the ABC classes that Waubert de Puiseau use as their baseline,
  except that ours ranks SKUs by measured demand instead of classes set by
  workers. It is also the $\beta = 0$ case of the storage objective. This is
  our counterpart of their ABC baseline.
- **Learned**, a PPO policy with reward (c). The candidate to take the place
  of the congestion-aware rule $F_{\mathrm{cng}}$, which is the hand-picked part.

Whether the learned policy replaces $F_{\mathrm{cng}}$ in the thesis is **not
concluded**. The author wants the pilot experiment first.

## Open: what a zone is

A zone-level action needs a split of the storage vertices into zones. Two
candidates, both built from definitions the thesis already has.

1. **The router's zones** (`eq:partition`, `environment/zones.py`), blocks of
   consecutive aisles. No new definition, and the choice spreads stock across
   aisles, which is the traffic lever. But a block of aisles may not separate
   shelves near the receiving side from far ones, depending on how the aisles
   run.
2. **Bands of trip distance** (`eq:tripdistance`), for example the nearest,
   middle and farthest third of shelves. Closest to Waubert de Puiseau's A, B
   and C, which are zones of equal transport cost. Needs only the cut points,
   but it offers no choice between aisles.

Crossing the two (band by aisle block) gives both levers at the cost of a
larger action space. To decide before the pilot.

## Next: a pilot PR

A test in `slap-mapd-coupling`, not thesis text. A new `[Axx]` tag, a change
to `[A48]` and to the future-work paragraph follow only if the pilot is
adopted. The plan is to be agreed before work starts.

# Definition 2026-10-22

Agreed with the author on 2026-10-22, after the memory check below. Draft
Introduction text is in `learned_storage_intro.tex` next to this file. It is
not in the thesis.

## Decisions

- **No zones.** The policy chooses a shelf itself. One output per storage
  vertex, masked to the shelves with room. No new division of the warehouse
  and no zone count to justify. The fleet warehouses have $|V_{\mathrm{str}}| = m/2$
  shelves (4 at 8 agents, 32 at 64), so the choice is as small as Waubert de
  Puiseau's three zones at 8 agents. Fallback if it does not train: three bands
  of trip distance.
- **One choice per put-away.** SKUs go in order of $\hat\rho_t$, as in
  $F_{\mathrm{dem}}$. The policy picks a shelf, as many units as fit go there,
  and that is one put-away task. Leftover units mean another choice among the
  shelves that still have room.
- **GCN, the routers' architecture with its own weights.** Same encoder family
  as the routers (`[A32]`). Extra vertex features for storage (shelf fill, units
  of the SKU there, traffic and waiting through the vertex, trip distance) and
  the SKU (demand estimate, unit size, units left) in the readout.
- **Reward: loaded time** (refines (c)). A shelf choice settles the put-away
  leg (receiving to shelf) and each pick leg (shelf to delivery). The time the
  units are carried, moving or blocked, is $t_j^{\mathrm{finish}} - t_j^{\mathrm{pickup}}$
  and is already recorded per task. The wait before assignment and the empty
  run to the shelf depend on where the fleet is and are left out. The objective
  is the sum over completed put-aways plus the sum over completed picks. A mean
  per placement would not charge for splitting a SKU over more shelves, and
  every pick happens whatever the rule does, so a sum is the right form.
  $d^{\mathrm{trip}}$ is the same journey in an empty warehouse, so the policy
  learns what traffic adds to it.
- **Pilot: Token Passing, fixed.** Compared with $F_{\mathrm{fix}}$,
  $F_{\mathrm{dem}}$ and $F_{\mathrm{cng}}$ under Token Passing. The Token
  Passing with learned storage row is also a result, one cell of the 2x2
  (router rule or learned, storage rule or learned).
- **Citation.** The Introduction should say where the rules come from (Part A
  of the draft). That applies whether or not the learned rule is adopted.

## Memory check

Measured on 2026-10-22 with the repo's `GNNEncoder` (L = 2, width 32, pooled
readout, 5 extra vertex features) plus a shelf-score head and a value head,
over the whole fleet warehouse. One forward and backward pass, CPU, peak
resident memory. Script: `learned_storage_gcn_size.py` next to this file.

| agents | vertices | edges | shelves | parameters | minibatch 128 | observation |
|---|---|---|---|---|---|---|
| 8 | 128 | 180 | 4 | 9 890 | 151 MB | 6.5 KB |
| 16 | 256 | 329 | 8 | 9 890 | 224 MB | 13 KB |
| 32 | 512 | 747 | 16 | 9 890 | 410 MB | 26 KB |
| 64 | 1024 | 1549 | 32 | 9 890 | 617 MB | 52 KB |

- Parameters do not depend on the warehouse size, since the weights act per
  vertex and per edge.
- Memory grows linearly with $|V|$. At 64 agents a minibatch of 128 needs about
  0.6 GB. A minibatch of 2048 needs about 8 GB, so the whole batch must never go
  through the network in one pass. Keep the minibatch at 128, as the routers do.
- Decisions per episode: at most one per arriving SKU and shelf, so at most
  about 100 SKUs times 20 epochs (horizon 2000, $\Delta = 100$), about 2000.
  At 64 agents that is about 100 MB of observations per episode if the edge
  list is stored once and not with every observation. The routers take
  $m \times 2000$ samples per episode (128 000 at 64 agents).
- The machine has 31 GB, about 14 GB free. No explosion.

## Open points for the pilot plan

- Credit per choice. A choice gets its put-away's loaded time when the put-away
  is delivered, and the loaded time of each pick that takes its units when that
  pick is delivered. Units of the same SKU on one shelf are alike, so picks take
  the oldest placement first.
- End of the horizon. Units not picked by $T$ add nothing, as in
  `eq:meanservice`. Whether to bootstrap from the value head instead.
- The learned rule is stochastic. The draft says it is an element of
  $\mathcal{F}$ per seed. Check that this reading of $\mathcal{F}$ holds.
- The SKU order is fixed (by demand), not learned. Keeps the action to one
  shelf.

## Pilot plan

`learned_storage_pilot_plan.md`, next to this file. It also records that under
Token Passing a pick is blocked for only 0.6 to 2.7 steps at every fleet size,
so the pilot runs in two stages.
