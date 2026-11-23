# The thesis, explained simply

A guide for someone who has never seen the project. No maths needed. Where
a real number from the project helps, it is given.

## 1. What is this about?

Picture a big warehouse, like the one behind an online shop. Small robots
drive around inside it. They fetch products from shelves and bring them to
packing desks, so the orders can be sent to customers.

Two things decide how fast this goes.

1. **Where the products are kept.** If popular products sit far away, the
   robots drive a long way every time.
2. **How the robots drive.** If they get in each other's way, they stand
   still and wait.

These two affect each other. Where the products are decides where the
robots drive. Where the robots drive decides which aisles get busy. A clever
shelf rule could even look at the busy aisles and avoid them. That circle
is called a loop, and it is what the thesis is about.

The thesis asks one question.

> If we keep popular products close by, how much faster do orders get done?
> And does that depend on how the robots are controlled?

In the research world, choosing shelves is called **SLAP** (storage location
assignment problem). Moving many robots to fetch and deliver things is
called **MAPD** (multi-agent pickup and delivery). The thesis joins the two.

## 2. The warehouse

The warehouse is a map of spots connected by paths, like dots joined by
lines. A robot moves one spot per tick of the clock. Only one robot can
stand on a spot at a time, so robots can block each other in a narrow
aisle, like people in a school corridor.

The map has a few kinds of spots.

- **Aisles,** where robots drive.
- **Shelves,** where products are kept.
- **Workstations,** the packing desks, where picked products go.
- **Docks,** doors on the left wall where finished orders leave.
- **Parking spots,** where an idle robot can wait out of the way.

Every shelf, desk, dock and parking spot sits just off an aisle. So a robot
standing at a shelf never blocks the aisle for others.

There are lanes that go both ways between blocks of shelves, and a one-way
loop through the middle, like a roundabout. Some aisles are dead ends. So
the map is not a neat chessboard. It looks more like a real building.

**Four sizes.** A bigger fleet gets a bigger warehouse, so every robot has
the same amount of room.

| Robots | 8 | 16 | 32 | 64 |
|---|---|---|---|---|
| Spots to drive on | 128 | 256 | 512 | 1024 |
| Shelves | 40 | 80 | 160 | 320 |
| Different products | 20 | 40 | 80 | 160 |
| Packing desks | 4 | 8 | 16 | 32 |
| Docks | 4 | 8 | 16 | 32 |

**A new warehouse every time.** The computer draws the warehouse from a
number called a seed. The same seed always gives the same warehouse, so
every method can be tested on exactly the same building. Different seeds
give different buildings, so the result does not depend on one lucky
layout.

**Shelf space is tight.** There are only two shelves per product. If there
were lots of empty shelves next to every desk, every shelf rule would do
equally well and there would be nothing to compare.

## 3. The orders

**How often.** Orders come in at random, all the time. The busier we make
it, the more orders per tick.

**What is in an order.** An order has about 5 lines. Each line is one
product, 1 to 5 of it. Each line becomes one trip for a robot, from the
shelf to the order's packing desk. When all lines are at the desk, the
order is packed and driven to a dock. Then it is done.

**What is popular.** A few products are bought much more than others. The
most popular one is bought twice as often as number two, three times as
often as number three, and so on. This pattern is called a Zipf law, and
it shows up in real shops.

**Popularity changes.** Every 200 ticks, about 5 % of the products swap
places in the ranking. So the hits slowly cool down and other products take
over, like songs in a chart. After 4000 ticks the ranking has gone all the
way round.

This change is the key. If popularity never changed, you could sort the
shelves once and be done, and a smart shelf rule would have nothing to win.

**Sections.** The products are split into groups of 20, called sections.
Each section has its own 4 packing desks. An order goes to one desk and
only asks for products from that desk's section.

**New stock.** Picking uses stock up. Every so often a delivery of 10 more
of a product arrives. A robot has to carry it from where deliveries come in to a shelf.
That trip is called a put-away, and it uses robot time just like a pick.
Products already on a shelf never move.

**The same customers every time.** The orders come from their own random
number stream. So with the same seed, the same customers order the same
things, whatever shelf rule or controller we use. This makes the comparison
fair.

## 4. Three ways to choose a shelf

When new stock arrives, a rule picks which shelf it goes on. The rules are
a ladder. Each step up uses one more kind of information.

- **Fixed.** Every product has its own home shelf. The homes are picked at
  the start from what is popular then, so it starts out sensible. But it
  never changes, even when popularity changes. This is the baseline that
  everything is compared to.
- **Demand.** Looks at what people have been buying lately. The most bought
  products go to the shelves with the shortest trip to their desk. As
  popularity changes, it changes too.
- **Congestion-aware.** Like demand, but it also measures where robots get
  stuck. It avoids shelves whose trips go through busy aisles. This is the
  only rule that closes the loop, because it is the only one that looks at
  the robots.

There is also **random**, which puts stock anywhere. It is only used as a
check. If demand beats random, the win comes from knowing what is popular,
not just from spreading things out.

## 5. Three ways to control the robots

Each robot has a small brain, a neural network. A special kind, a **graph
neural network**, is used because the warehouse is a map of dots and lines,
and this kind of network is built to read maps like that.

**What the robot sees.** The robot looks at the spots near it. For each
spot it knows a few simple facts. What kind of spot it is. Whether another
robot stands there. And whether the spot is one step closer to its goal or
one step further away. From that, the brain gives a score to each possible
move, and the robot picks one.

All three controllers use the same brain. The only difference is who
decides together.

- **Centralised.** One boss plans for all robots at once. The robots choose
  one after another, and each one can see where the earlier ones are going.
  So they never pick the same spot. The downside is time. With 64 robots,
  the brain has to run 64 times every tick.
- **Section-based.** The warehouse is split into zones, and each zone has
  its own boss that works like the centralised one. If robots in two
  different zones clash at the border, that is sorted out afterwards.
- **Decentralised.** Every robot decides for itself, from what it can see
  around it. It is the fastest, but robots can't plan around each other.
  They can optionally send short messages to nearby robots.

**Two extras**, not part of the main comparison.

- **Token Passing** is a well-known method that does not learn. There is
  one "token", like a talking stick, that holds every robot's plan. A
  robot that needs a new job takes the token, picks the nearest job, and
  plans a path that avoids all the others. It shows whether our learning
  robots are any good.
- **Full view** is a decentralised robot that can see the whole warehouse.
  It helps answer whether centralised wins because it *sees more* or
  because the robots *plan together*.

## 6. How the robots learn

The robots learn by trial and error, called **reinforcement learning**. A
robot gets points for good moves and loses points for bad ones. Over many
tries it learns to get more points.

**The points.** Roughly, close to its goal:

- a step towards the goal is worth about +0.75
- waiting costs about 0.2
- a step away from the goal costs about 1.25
- finishing a job gives a bonus
- being stopped because of a crash costs extra
- standing in a crowd costs a little

So driving on is best, and waiting is better than a detour. These values are
being changed right now (see section 11).

**Team points.** A robot gets the average points of the robots it decided
together with. For centralised, that is the whole fleet. For section-based,
its zone. For decentralised, just itself. This pushes the robots that plan
together to help each other.

**Practice.** The learning method is called **PPO**. Every controller gets
the same amount of practice, 500 000 ticks, so none has an unfair head
start. Practice is split into games of 2000 ticks, and every game is in a
new warehouse. That way the robots can't just learn one map by heart.

**Two ways to practise.**

- **fixed_only.** Practise with fixed shelves, then test with every shelf
  rule. The main result uses this one, because then the same robot brain
  is used on both days of the comparison.
- **matched.** Practise with the shelf rule you will be tested with.

**Test warehouses are new.** The warehouses used for testing are ones the
robots never saw in practice.

## 7. What happens every tick

Every tick of the clock, the same six things happen, whatever the
controller.

1. **New orders** turn into jobs and join the queue.
2. **Free robots get a job.** The oldest job goes to the closest free robot.
3. **Each robot picks its next step.** This is the only part that is
   different between the controllers.
4. **Crash check.** If two robots would hit each other or swap places, one
   of them waits instead.
5. **The robots move,** and everything is written to a log.
6. **Now and then, new stock arrives** and the shelf rule places it.

Because only step 3 changes, any difference in the results comes from the
controller and nothing else.

Here is where each step lives in the code, in
`slap-mapd-coupling/src/slap_mapd_coupling/`.

| Step | Folder or file |
|---|---|
| 1. New jobs | `core/tasks.py` |
| 2. Give out jobs | `controllers/assignment.py` |
| 3. Pick a step | `models/` (the brain), `environment/observation.py` (what it sees) |
| 4. Crash check | `resolution/conflict_resolution.py` |
| 5. Move and log | `environment/multi_agent_env.py` |
| 6. Place stock | `storage/` (`fixed.py`, `demand.py`, `congestion.py`) |

Other useful places.

- `instances/generator.py` builds the warehouse from a seed.
- `environment/reward_function.py` hands out the points.
- `planners/token_passing.py` is Token Passing.
- `training/` runs the practice.
- `evaluation/` works out the scores.
- `viz/pygame_renderer.py` plays a run back like a video, so you can watch
  the robots.

## 8. How we score a run

In the Token Passing tests, a run lasts 10 000 ticks and the first 5000 are a
warm-up that doesn't count. The length for the main tests is not decided yet.
At the start the stock is placed at random, and the warm-up gives the shelf
rule time to put its own stamp on the warehouse.

**First, can the robots keep up?** If orders come in faster than the robots
can finish them, the queue grows forever, like a traffic jam that never
clears. Then the run has failed, and we don't compare it. Picks and
put-aways are checked apart. Otherwise lots of quick picks could hide that
the put-aways are falling behind.

**Then, how long does an order take?** We time each order from when the
customer orders until it leaves through a dock. Then we take the average
over all finished orders. This is the main score. Shorter is better. It
includes every wait: for stock, for a robot, for the last line, and for the
trip to the dock. The customer waits through all of them.

**Why was it fast or slow?** Every tick of a pick trip is put in one of
three boxes, and the three add up to the whole trip.

- **Waiting for a robot.** The job is in the queue and no robot has taken
  it. Grows when there are too few robots.
- **Driving.** The robot is moving. Good shelves make this shorter. This
  is where we expect demand shelves to help.
- **Stuck.** The robot stands still because another robot is in the way.
  Grows when the aisles are crowded.

Example: a pick waits 10 ticks for a robot, the robot drives 20 ticks and
is stuck for 5. The trip takes 35 ticks. If demand shelves cut the driving
to 15, the trip takes 30.

**Other things we write down.**

- **Crowding.** How full the space around each robot was, on average.
- **Orders finished** per tick.
- **Put-away time.** What the shelf rule costs in robot time. Putting stock
  near the desks can make put-aways longer.
- **Thinking time.** How long the controller takes to decide each tick.

## 9. The number that answers the question

We play the same day in the warehouse twice. The same customers order the
same things both times. The robot brain is the same both times. The only
change is the shelf rule.

- Day A uses **fixed** shelves.
- Day B uses **demand** shelves.

Then we subtract.

> **Gain = average order time on day A minus average order time on day B**

If the gain is positive, demand shelves made orders faster.

**Many days, not one.** One day could be lucky. So we do this for many
different days (seeds) and take the average gain. We also work out how sure
we can be, with a 95 % confidence interval. That is a range that very
likely holds the true gain. If the whole range is above zero, we say demand
storage really helps. The test is called a paired t-test. "Paired" means
each day A is matched with its own day B.

**To compare the controllers,** we turn the gain into a percentage of day
A's time.

| Controller | Day A (fixed) | Day B (demand) | Gain | Gain in % |
|---|---|---|---|---|
| example 1 | 100 ticks | 90 ticks | 10 ticks | 10 % |
| example 2 | 200 ticks | 185 ticks | 15 ticks | 7.5 % |

In ticks, example 2 looks better. In percent, example 1 is better. Percent
is the fair one, as the next section explains. (These are made-up numbers.)

**How busy.** We test at one level of orders, busy but not too busy, where
every controller can still keep up. For each size, that is 60 % of the most
the fleet can handle. In numbers, 0.09, 0.18, 0.3 and 0.6 order lines per
tick for 8, 16, 32 and 64 robots.

So the main result, in one sentence:

> For each controller, how many percent faster orders get with demand
> shelves than with fixed shelves, how sure we are, and which of the three
> boxes (waiting, driving, stuck) changed.

## 10. Why this number?

- **The order time, because that is what the customer feels.** They don't
  care about one robot trip. They care about when the parcel leaves.
- **Same customers and same brain both days,** so the only difference is
  the shelves. Otherwise a quiet day could look like a win.
- **Fixed shelves to compare against,** because they start sensible but
  never change. So the gain shows what it is worth to keep up with what is
  popular, not just that a good layout beats a bad one.
- **Percent, not ticks.** A slow controller has more time to lose, so in
  ticks it would look like the biggest winner just for being bad. Percent
  is fair, and it is how other storage studies report their results.
- **Keep up first,** because when the queue keeps growing, the average only
  counts the orders that got done and hides the rest.
- **Split into three boxes,** so we know *why* it got faster, not just that
  it did.

## 11. The research questions

- **RQ1.** Do demand shelves make orders faster, and which box changes?
  Answered by the gain.
- **RQ2.** Is the gain bigger when more robots decide together? Answered by
  comparing the percent gain of centralised, section-based and
  decentralised.
- **RQ3.** Does looking at busy aisles help even more? Compare
  congestion-aware with demand. Look at crowding and stuck time against
  the extra driving.
- **RQ4.** With more orders or more robots, when does the gain stop, and
  when does each controller stop keeping up?
- **RQ5.** Does it help if decentralised robots send messages? Only if
  there is time.

RQ1 and RQ2 together are the main result. The others show when it holds.

## 12. The results chapter

The results are in `thesis/Chapters/5.Experiments.tex`. It goes in this
order.

1. **Training.** A graph of points against practice time for each
   controller. Did the robots learn properly, and did they stop improving
   before testing?
2. **Keeping up.** Which runs kept up and can be compared. One run that
   failed, so the reader sees what a growing queue looks like.
3. **RQ1.** A table with, for each controller, the order time with fixed
   shelves and the gain with demand and congestion-aware shelves. A bar
   chart of the three boxes for each controller and shelf rule.
4. **RQ2.** The percent gains side by side, with how long each controller
   takes to think next to it.
5. **RQ3.** Crowding against order time, demand against congestion-aware.
6. **RQ4.** Gain against how busy it is, with a mark where each controller
   stops keeping up.
7. **RQ5.** Messages on against off, or one line saying it was not done.
8. **Costs.** Put-away time for each shelf rule, and thinking and practice
   time for each controller.

**How to read the RQ1 table.** Column one is how slow each controller is
with fixed shelves. Column two is the gain. Divide column two by column one
for the RQ2 percentage. If the range around a gain goes below zero, that
controller shows no clear gain.

None of it is filled in yet.

## 13. What we know so far

**Token Passing has been tested.** With demand shelves, orders got about
**11, 14, 13 and 10 % faster** than with fixed shelves, for 8, 16, 32 and 64
robots. Random shelves were 48 to 210 % *slower* than fixed. So knowing
what is popular is what helps, not just moving things around. Avoiding busy
aisles changed almost nothing, within 2 %.

**A surprise with Token Passing.** A pick drives only 17 to 25 ticks but
waits 67 to 156 ticks for a robot. Token Passing lets only one robot head
for a packing desk at a time, so robots stand idle while jobs wait. This is
how Token Passing was designed, so it is kept and noted as a weakness.

**The learning robots are not ready.** The first practice runs with 32
robots got better at first, then fell apart. The robots found a trick.
Moving cost less than waiting, so a blocked robot stepped back and forth
instead of standing still, and got fewer points taken off. Five fixes to
the points are agreed, and one is done. The practice runs start again after
that.

So the warehouse clearly gives good shelves something to win. The main
result still needs the three learning controllers.

## 14. Where things are

- **The code:** `slap-mapd-coupling/`. See section 7 for which folder does
  what.
- **The thesis:** `thesis/Chapters/`. Chapter 3 is the model, chapter 4 is
  how it is built, chapter 5 is the experiments and results.
- **Why each choice was made:** `thesis-progress/decisions/GAPS.md`.
- **Token Passing results:** `thesis-progress/results/E_load`, `F_demand`,
  `G_storage`.
- **Where the project stands today:** `SESSION_CONTEXT.md` at the
  workspace root.
