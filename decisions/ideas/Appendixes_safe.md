# Appendix

We are going to have a appendix for every number that does not come from another article to create a test for how the number is generated. So we have a test for:


## The graph 
* Here we generate multiple instance of the graph of a fleet size of [8, 16, 32, 64]. We should multiple of these instance and explain how the proof works in simple terms. We cite the Knippenberg as inspiration and.

* Then dependent on the size we should figure out the amount of reasonble number based on the size of the graph. It should not just be 3 but it should be dependent on if we use [8, 16, 32, 64]. We probably should have a liniar scaling with the amount of vertexes scaling with the amount of agents. So, this would remove the parameter of num_zones? Or it should be kept for being albe to use it test the differnt section sizes. 

## The Storage 
* *vertex_capacity* How do we know how much each storage node should be able to hold? How can we test this in a way that does not require us to test the overall sytem or to make a lot of assumption since we have the β paramter to decide how much space each item takes up. Here we can also fithnd a model done on the internet and use their numbers for how much storage and the amount of β is the congestion weight of the storage rule. How much room one unit takes is the unit size per SKU. This also need to look at if someone already did this and our needs citation. *unit_capacities*: [0.5, 1.0, 2.0]
* We assume the deliver nodes and receiving nodes can hold ulimited amount? Or do we assume they also have a storage capacity? How would in contribute to the system and what problems would each of them have? We also need to add the reasoning for why we choose what we did. 
* *arrival_rate*: The arraival rate of storage should be decided using the Token Passing model for the load sweep where we use this number as the baseline. It have to be able to keep up but not as the agnet would be waiting for the task to arrive. Frit we run the load_sweep for each of the amount of agents [8, 16, 32, 64], where we adjust the receiving rate in a reasonable way when we increase the amount of agents.
* *arrival* so the arrival it the total arrival, but we also have a arrival rate which seems contradition to have both values. 
    * *margin* does what? there is a certain margin we can accept? 
    * *receiving* is the node that get the stock?
    * *putaway* is the thing that muse the stock? 
    * *cold_stock_top_k* Would this not go against a learned policy where it has to figure out where the items goes?

* *n_deliver* How do we know how much should arriave with the n_deliver parameter?
* *initial_units* Why do we have a initial units of 8? does this not seems low for 64 agents? and why is it this number? 
* *demand* Demand is a Zipf with a given skew but does our number make sense and do we have argument why it is as we have chosen the values of: 
```demand:
  skew: 1.0
  rotation_period: 200
  rotation_shift: 5
```

* `Idea to test` it with: You can test capacity without running the whole system. A shelf has to hold its starting stock plus one period's arrivals at the expected demand. That follows from the arrival equation and the starting stock formula in app:instances. So capacity can be set as the largest required load times a margin, and Appendix G's capacity check confirms it on each fleet. That is one calculation with no extra assumptions, and it explains why m=8 needed 300 rather than 200. Shelf sizes from industry sources would only be decoration unless they come with a real citation. I'd use the calculation, and cite a source only if you find one that fits our unit sizes.

* `Add this`: Delivery and receiving capacity. I'd assume both are unlimited. A delivery vertex is where orders leave and a receiving vertex is where stock enters. Neither holds stock in the model, and Ma et al. put no capacity on pickup or delivery locations. What limits these vertices is that only one robot can stand there, and the vertex rule already enforces that. A dock capacity would add a queue at receiving that no research question asks about. Give it one sentence of reasoning and list it in the scope appendix.

* `Test`: this for load sweep: Arrival rate from the load sweep. This makes sense, and load_sweep.py already reads off the rate at 0.6 of Token Passing's capacity. That is the "keeps up, but agents don't wait for tasks" point. One warning on scaling: don't scale the rate linearly with m. The warehouse grows as 16m, so trips get longer roughly as √m and throughput per agent falls. Run the sweep for each fleet size and take 0.6 of that fleet's capacity. The earlier commit "scale arrival rates linearly by fleet size" should be replaced by this.

# A episode length 
* Why is it 2000? We set this because it would let our demand and congestion evovle over time for our assingment route. We have to have a reason for this number, where we can do some testing.
* To look into this issue we probably need to decide on the learned_storage_policy before we can continue. Since we have a clear need to figure out if this is a learned policy and how long they do their updates to figure out the number. Note since we as of right now only change every 100 steps does that make sense for a learned policy? Maybe it is our only way of making sure that we can measure when improvement come from the updated storage policy or from the controller policy
* *storage_rule* is the delta 100 that decide when we update a storage rule. There is no reason for this number
* *congestion_weight* why does it have a congestion weight of 1.0? 




`Test`: Episode length 2000. This one doesn't have to wait for the learned-storage decision, because the horizon can be derived from timescales:
- Warm-up. It must pass the point where the backlog settles. Measure this with Token Passing on each fleet size.
- Drift. It must then cover several demand drifts. The ranking moves every 200 steps, so 2000 steps gives 10 moves.
- Storage periods. It must also cover several storage periods Δ.

    A test would show throughput and backlog over time and set the horizon to the warm-up plus k drift periods. Your last point is right: a fixed storage period is what lets you tell whether an improvement came from storage or from the controller, because the two act on different timescales. That is a reason to keep the rules and leave a learned storage policy as future work, as how_the_system_works.md already recommends. Also note that the configs refresh storage every 100 steps but Δ is still TBD in the thesis. That mismatch needs a decision.

# Agents
* The cost is directly taken from the Knippenberg to not study the configuration for agents. Why did we select the observation depth to 5? the Knippenberg also studied this so why this and should we test with differnt depeth? 

# Congestion reward and sensitivy 
* How did we arraive with this function and is it good? Does it do the same principal as the CRAMP to penalilise?
* The reward is vary small contribution alsmost not anything at 0.1, so from our initail test does not seem like the reward works at all. We need a reason for having this number else we need to do test to find out why we choose this number

# Model
* How did we arraive at this model and why is this the model? why this amount of 
    * *num_rounds* what does this do?
    * *hidden_width* why the depth?
    * *head_hidden_width* why thi?

# PPO 
We do we have the numbers we do? and the training bugdet we do? in the thesi does we not say the score attribute was dependent on the task instead of the episode_return_mean?s



# Experiment
The configuation form here should cited where each of the comes from.
```code   
  reward 
  discount: 0.99            # gamma
  # n_deliver is raised well above 1.0. A 5000-iteration run on this instance showed rising
  # training return with zero evaluation completions, consistent with the per-step shaping
  # term outweighing a small completion bonus.
  deliver_reward: 10.0
  override_penalty: 0.5
  move_cost: 0.1            # c_move, after van Knippenberg et al. (2021)
  congestion_reward_weight: 0.1
  congestion_sensitive: false
  seed: 0
```
