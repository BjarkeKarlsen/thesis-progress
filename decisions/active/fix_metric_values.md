# Start here
* Read this issue though understand it and it context. 
* Validate with the user how it should work and what metric is needed
* Fix the code as described
* Fix `/home/bjarkek/Documents/thesis/thesis-progress/results/arrival_rates` where all the scripts has values but not the correct ones. So values need to

## Issue description for the next agent

The current implementation has a metric-definition problem in the load-sweep results.

The JSONL field `arrival_rate` represents the expected number of **customer order lines released per simulation timestep**. It is therefore a customer-demand rate.

However, the current `throughput` and `keep_up_ratio` appear to use:

```python
num_completed_tasks / horizon
```

where `num_completed_tasks` includes both:

- customer pickup tasks;
- inventory put-away tasks.

This creates an invalid comparison:

```text
all completed tasks per timestep
--------------------------------
customer order lines arriving per timestep
```

For example:

```json
{
  "arrival_rate": 0.3,
  "num_completed_tasks": 773,
  "num_completed_putaways": 338,
  "horizon": 2000,
  "throughput": 0.3865,
  "keep_up_ratio": 1.2883
}
```

The current calculation is:

```text
773 / 2000 = 0.3865 total tasks per timestep
0.3865 / 0.3 = 1.2883
```

The ratio is above 1 because put-away tasks are included in the numerator. It must not be interpreted as the system completing 128.8% of customer demand.

For this row, the estimated number of completed customer pickup tasks is:

```text
num_completed_picks =
num_completed_tasks - num_completed_putaways
                    = 773 - 338
                    = 435
```

The customer pickup throughput is therefore:

```text
pickup_throughput = 435 / 2000 = 0.2175
```

Compared with the customer arrival rate:

```text
pickup_keep_up_ratio = 0.2175 / 0.3 = 0.725
```

This shows the customer-facing system is not processing pickup work at the same rate as customer demand, despite the current total-task ratio being greater than 1.

## Required code change

The implementation should keep the two workload types separate.

Add or calculate the following fields:

```python
num_completed_picks = (
    num_completed_tasks - num_completed_putaways
)

task_throughput = num_completed_tasks / horizon

pickup_throughput = num_completed_picks / horizon

pickup_keep_up_ratio = (
    pickup_throughput / arrival_rate
    if arrival_rate > 0
    else None
)
```

Recommended JSONL output:

```json
{
  "arrival_rate": 0.3,
  "num_completed_tasks": 773,
  "num_completed_putaways": 338,
  "num_completed_picks": 435,
  "task_throughput": 0.3865,
  "pickup_throughput": 0.2175,
  "pickup_keep_up_ratio": 0.725
}
```

The existing `throughput` field should either be renamed to `task_throughput` or its meaning should be made explicit. Avoid silently changing its meaning because existing result files and summary tables may depend on it.

## Required keep-up logic

There are two possible interpretations, and the implementation must choose one explicitly.

### Customer-facing keep-up

If the main research question concerns customer service, the keep-up test should use pickup tasks only:

```text
completed pickup work
compared with
released customer pickup work
```

The keep-up criterion should use pickup-specific quantities:

```python
pickup_throughput >= f_up * pickup_release_rate
```

If the current implementation includes final unfinished work in the keep-up calculation, create a pickup-specific equivalent:

```python
pickup_throughput >= f_up * (
    completed_picks + unfinished_pick_tasks
) / horizon
```

The exact formula must use the same definition of release rate everywhere. Do not compare pickup throughput with a rate containing put-away releases.

### Total warehouse workload

It is also valid to measure whether the fleet processes all warehouse work, including replenishment:

```text
completed pickup tasks + completed put-away tasks
compared with
released pickup tasks + released put-away tasks
```

If this metric is retained, it must be given a separate name, such as:

```python
warehouse_keep_up_ratio
```

It must not be called simply `keep_up_ratio` if the thesis interprets that field as customer demand performance.

## Recommended metric names

Use explicit names:

```text
arrival_rate
    Expected customer order-line arrivals per timestep.

num_completed_picks
    Number of completed customer pickup tasks.

num_completed_putaways
    Number of completed inventory put-away tasks.

pickup_throughput
    Completed pickup tasks per timestep.

putaway_throughput
    Completed put-away tasks per timestep.

total_task_throughput
    Completed pickup and put-away tasks per timestep.

pickup_keep_up_ratio
    Pickup throughput divided by customer order-line arrival rate.

warehouse_keep_up_ratio
    Total task throughput divided by the corresponding total workload release rate.
```

If the code uses `num_completed_tasks` as the total count, retain it for compatibility but document it clearly:

```text
num_completed_tasks = num_completed_picks + num_completed_putaways
```

## Summary and load-sweep changes

The summary currently uses `throughput` to determine capacity. This must be changed depending on the chosen definition.

For customer-facing capacity, use:

```python
pickup_throughput
```

and determine capacity from the highest arrival rate where the pickup-based keep-up criterion succeeds.

Do not determine customer capacity from:

```python
num_completed_tasks / horizon
```

because that includes put-aways and can make the capacity look artificially high.

The summary should report both values if useful:

```text
pickup throughput
total task throughput
pickup keep-up ratio
customer keep-up status
```

The main capacity table should use the pickup-based result.

## Tests that must be added

Add tests for the following cases:

1. If 100 total tasks are completed and 20 are put-aways, then:
   ```text
   completed picks = 80
   ```
2. If the horizon is 1,000:
   ```text
   pickup throughput = 80 / 1000
   ```
3. If `arrival_rate = 0.1`, then:
   ```text
   pickup_keep_up_ratio = pickup_throughput / 0.1
   ```
4. Put-away tasks must not increase `pickup_keep_up_ratio`.
5. A run with many completed put-aways but insufficient completed picks must not be classified as keeping up with customer demand.
6. A zero arrival rate must not cause division by zero.
7. Existing JSONL rows without the new fields should either be migrated or handled explicitly by the summary script.

## Important data limitation

The formula:

```python
num_completed_picks = num_completed_tasks - num_completed_putaways
```

is valid only if `num_completed_tasks` includes exactly:

```text
completed pickup tasks + completed put-away tasks
```

The next agent should verify this in the simulator and metrics implementation. If `num_completed_tasks` already excludes put-aways, or if it counts another task category, the calculation must be adjusted accordingly.

The preferred implementation is to count pickup completions directly in the simulator rather than infer them indirectly:

```python
num_completed_picks
num_completed_putaways
num_completed_tasks
```

Then assert:

```python
num_completed_tasks == (
    num_completed_picks + num_completed_putaways
)
```

when those are the only task types.

## Expected correction for the example

For the supplied row, the corrected interpretation is:

```text
arrival_rate:              0.3
completed total tasks:     773
completed put-aways:       338
completed picks:           435
total task throughput:     0.3865
pickup throughput:         0.2175
current ratio:              1.2883
corrected pickup ratio:    0.725
```

The current `keeps_up: true` value should be re-evaluated after the pickup-based keep-up logic is implemented. It may change to `false`, depending on the exact release and backlog formula.

## Acceptance criteria

The issue is resolved when:

- `arrival_rate` is documented as customer order-line arrivals per timestep.
- Pickup and put-away completions are reported separately.
- Customer pickup throughput is calculated independently.
- Customer keep-up uses pickup work, not total task work.
- Total warehouse workload remains available as a separate metric.
- The summary and capacity sweep use the intended metric.
- Existing JSONL rows are either migrated or clearly marked as using the old definition.
- Tests verify that put-away completions cannot artificially improve customer keep-up.
- The example row produces a pickup throughput of approximately `0.2175` and a pickup ratio of approximately `0.725`, assuming the task counts have the stated meaning.