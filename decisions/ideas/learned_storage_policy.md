# Idea: a learned storage policy (PPO)

**Status 2026-10-20. Extra, to look into after the long run.** Not planned, not
in the thesis. Raised by the author: is the coupling not meant to be between
two policies, one for storage and one for routing?

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
