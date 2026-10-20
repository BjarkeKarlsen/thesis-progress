# Orders with several lines and amounts, proposed `[A46]`

**Status 2026-10-19. Applied as `[A46]`, with decision 1 changed by the author: a line may take units from several shelves, one task per shelf. Quantity 1 to 5 per line, uniform. The text below is the original proposal.** The author
asked on 2026-10-19 for orders with several items and amounts to go in before the long run.
Once approved, the text below is applied with `% [A46]` tags and a `GAPS.md` entry, and gated
step G1 of `code_changes_plan_2026-10-19.md` is written out as code steps.

## What the thesis already says

The problem formulation is already general. An order is a multiset of SKU-quantity pairs,
$z = \{(k_1,q_1), \dots, (k_n,q_n)\}$, "converted into one or more transport tasks by a
task-generation rule" (`sec:pf:tasks`). The notation table already has $q$ as the quantity.
What is missing is the rule itself. The Method then narrows it, "each order asks for one SKU"
(`sec:impl:instances`, `[A34]`), with an implicit quantity of 1.

So `[A46]` states the task-generation rule and widens the demand model. It does not change the
controllers, the observation, the reward or Token Passing.

## The model, in short

It is the goods-to-person setting of Krnjaic et al. (2022), already cited. Each order line is
one trip. An agent fetches the line's SKU from one shelf and brings it to the order's delivery
vertex. The order is complete when its last line is delivered.

- **One task per order line.** Every line of an order has the same release time and the same
  delivery vertex, drawn once per order.
- **A line takes its whole quantity from one shelf**, the shelf nearest the delivery vertex
  among those holding at least that many units. If no shelf holds enough, the line waits for
  stock, as an order does today (`[A39]`).
- **Service time stays per task**, so per order line. That keeps the main result, the
  measures and the comparison with Ma et al. (2017) unchanged. Throughput then counts order
  lines per timestep, the pick rate of Krnjaic et al.
- **Order completion time is added as a reported measure**, the time from an order's release
  to the delivery of its last line.
- **The load stays $\lambda_{\mathrm{task}}$, tasks per timestep.** Orders arrive at
  $\lambda_{\mathrm{task}}$ divided by the mean number of lines.

## Decisions for the author

1. **Where a line takes its units.** Recommended: from one shelf, and wait if no shelf holds
   enough. Every line is then exactly one task under every storage rule, so the paired
   comparison stays exact. The alternative, splitting a line over several shelves, means no
   wait while stock exists. But the number of tasks then depends on the storage rule, so fixed
   and adaptive storage no longer score the same task set, and the service time split needs
   redefining per line. Waiting should be rare, since a shelf holds many units and a quantity
   is small. The code logs how often it happens.
2. **Lines per order.** Krnjaic et al. use an average of 5 order lines per order (2 in their
   "Disjoint" warehouse). They give the mean, not the distribution. Proposed: mean 5 from
   them, with the shape of the distribution TBD. Note that 5 lines released at once to one
   delivery vertex make arrivals burstier than today, so the queue will grow at the same
   $\lambda_{\mathrm{task}}$. The Token Passing load sweep sets capacity after this change, not
   before.
3. **Quantity per line.** No source found yet. Krnjaic et al. define a quantity per line but
   give no values. Proposed: quantity TBD, a config field with no default, and 1 until a
   source is found. Suggested place to look: order profiles in e-commerce warehousing reviews
   (for example Boysen et al. 2019, "Warehousing in the e-commerce era"), checked before it
   is cited.
4. **Two estimates instead of one.** Placement should follow trips, so $\hat\rho_t(k)$ counts
   order lines. Arrivals must cover units, so the fill level uses the units ordered. With
   quantity 1 they are equal. Proposed: keep $\hat\rho_t(k)$ for lines, and add a units
   estimate $\hat\rho^{\mathrm{unit}}_t(k)$ used only by the arrivals.

## Proposed thesis text

### `sec:pf:tasks`, after the task definition

Replace "and each order is converted into one or more transport tasks by a task-generation
rule. The task definition makes each task a quadruple" with

> and each line of an order becomes one transport task, a trip that fetches the line's
> quantity of its SKU from one shelf and brings it to the order's delivery vertex. This is
> the goods-to-person setting of \citet{krnjaic2022warehouse_marl}. All lines of an order
> share its release time and its delivery vertex, and the order is complete when its last
> line is delivered. The \emph{task definition} makes each task a tuple

and the task gains its quantity,

$$\tau_j = (t_j^{\mathrm{released}},\, s_j,\, g_j,\, k_j,\, q_j), \qquad q_j \in \mathbb{N}.$$

### The stock condition and the pickup rule

> The pickup vertex must hold at least the line's quantity of its SKU,
> $x_t(k_j, s_j) \ge q_j$.

> Among the vertices that hold at least $q_j$ units of the SKU, a line takes its units from
> the one nearest its delivery vertex. If none holds enough, the line waits until stock
> arrives.

$$s_j = \arg\min_{v \in V_{\mathrm{str}} :\, x_t(k_j, v) \ge q_j} d_G(v, g_j),$$

and $x_t(k_j, s_j)$ falls by $q_j$.

### The estimates and the arrivals

$\hat\rho_t(k)$ counts order lines for $k$ in the window. A second estimate
$\hat\rho^{\mathrm{unit}}_t(k)$ counts the units ordered, and the fill level uses it,

$$x^{\mathrm{up}}_t(k) = \max\bigl(x_{\min},\, \lceil (1+\varepsilon)\, \Delta\, \hat\rho^{\mathrm{unit}}_t(k) \rceil\bigr).$$

Waiting orders add their units, not their count.

### `sec:pf:measures`, one reported measure

> **Order completion.** An order is complete when its last line is delivered. Its completion
> time is the largest service time among its lines, and its mean over the orders completed in
> the run is reported next to the mean service time. It is what a customer waits.

Plus one row in `tab:measures` (reported, after Krnjaic et al.).

### `sec:impl:instances`, the demand model (`[A34]` paragraph)

Replace "At each timestep the number of new orders is Poisson with mean
$\lambda_{\mathrm{task}}$, and each order asks for one SKU." with

> At each timestep the number of new orders is Poisson, with a mean chosen so that
> $\lambda_{\mathrm{task}}$ lines arrive per timestep on average. An order has
> \mockup{distribution TBD} lines, 5 on average as in \citet{krnjaic2022warehouse_marl}, each for
> a different SKU, and each line asks for \mockup{quantity TBD} units.

The Zipf law and the drift stay. The SKUs of one order are drawn from the ranking without
replacement and independently of each other.

### Scope, two items

> \item[Goods to person only] Each line is its own trip. One agent never collects a whole
>   order, the person-to-goods setting of \citet{krnjaic2022warehouse_marl}, which would make a
>   task a tour of several shelves.
> \item[SKUs ordered independently] The SKUs of one order are drawn independently, so no two
>   SKUs are ordered together more often than chance. Storage that places SKUs ordered together
>   near each other is therefore not studied.

### Notation

$q_j$ joins the task row. $\hat\rho^{\mathrm{unit}}_t(k)$ gets a row. Order completion time
gets a row if it is given a symbol.

## Code impact (for step G1)

Order generator (lines, quantities, one delivery vertex per order, order id on each task), the
task model (quantity), the pickup rule (at least $q_j$ units), the arrivals (units), waiting
orders (per line), and the metrics (order completion time, count of lines that waited while
the SKU's total stock would have covered them). No change to controllers, observations,
reward, Token Passing or training. The order stream still does not look at stock, so the
pairing holds. Every result changes, which is why it goes in before the long run.
