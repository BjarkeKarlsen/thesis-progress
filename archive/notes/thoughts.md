# Thoughts

The idea is we measure the task rate and if the agents can keep up with a task rate. This gives us the core expression: Note all planner or arms/controller should be able to keep up else we would not produces any findings.

## How do we compare a run and which parameter and why?

The thesis will in the end compare the warehouse under the diffferent storage types: fixed, demand, congestion. We will compare the models of one of more planners (Token Passing) as same concept as Knippenberg, and our 3 arms(controllers) centralised, section-based, decentralised. Here we will do here check first to do a comparison in the Warehouse graph we have design. Here we want to measure the performance of the adaptive storage against fixed with the different types of warehouse: fixed, demand, congestion. Here we should show the training as a graph plot where we compare the training. Then we should make a evaluation whereas we compare the throughput. We may need more numbers to help with this. There should also be produced some plot/images of the graph where it changes the location which decreases the amount of travel time. Be critical and we should also see if there is instance where it degrade the performance of the travel time. Here it will be congestion. So we have a plot of demand moved the plot where it create congestion problem, and how the congestion would fix this. Again be crical of the ideas. Which part moved, demand rule against fixed, compared the router against the values and this should also consider if a plot is easier.


| router        | wait for agent | travel | blocked | crowding |
| ------------- | -------------- | ------ | ------- | -------- |
| Centralised   |                |        |         |          |
| Section-based |                |        |         |          |
| Decentralised |                |        |         |          |
| Token Passing |                |        |         |          |

a initial idea for some of the values: short_run_2026-10-18.md

Should we either write the research question 2 into the research question 1 or we should handle the test in a way whereas it will be easier to understand. Because it is gonna be the same values.

Research question 3 the congestion against demand storage should compare the values in plot maybe in a table in sub document. (Later we will move part of the thesis to the appendix, since we have a 60 pages limit, but do not think about this before the thesis is complete). The cost of adaptive storage belongs in the method chapter. But the values gained from it belong in the method. Here we should compare the values for relocation distance per update (explain the terms), distance per relocated unit, fleet task travel per 100 steps/per update, (not sure) relocation distance/ fleet task travel, task travel save per update 100 steps, relcation distance/travel saved, extra task finished per update 100 steps. We take the idea from CRAMP and compare the evaluation in a graph that is with 8, 16, 32, 64 agents. With increasing the amount of agents will maybe help answering the gain though the congestion. This would then answer research question 4: How do the effects change wiith more agents and more orders. As i see it we should decide on a load of 0.6 or something else we do multiple compariason which would leed to a mess, the idea is we in in the appendix do a search for finding a reasonable number using the Token Passing to decide undetermine numbers. Which lets us argrue for why the number was choosen. Here we havce some initial values done: arrival_short_2026-10-18.md 

In the method and code we propably should use the same values as Knippenberg, so we dont do a study of me selecting the right cost. Here we should also propably look into the values from the SLAP/DSLAP for the allocating cost, so we again does not invent random numbers.

Research question 5: Does local communication help the decentralised arm? However we have a discussion open about this in message_design.md and that has a design plan in 

Training should be a graph of iteration for each arm in one color each and then the training task per episode. One with the service time if that is our learning function/ penality function. Then maybe save the override rate and so one for the validation.

Validation should also be a graphs. Here we have what we talked about earlier.

Concept is that as Knippenberg compare:
We take the idea from the Knippenberg with placing this graph in a lattince world and compare against other models if it is thesable to use the graph in the lattice spaces. With setting the graph cost to 1 per node.

Extra question that was temporarily removed but should be seen it they belong back as research questions: 1. Does a closed-loop coupling between storage location assignment and MAPD reduce the average travel distance per completed task compared to a decoupled baseline? 2. Does the closed-loop coupling reduce average edge congestion (e.g., average queue length or waiting time on busy edges) compared to a decoupled baseline? 3. At a fixed number of agents and tasks, which controller architecture (centralised, section-based, or fully distributed) achieves the highest throughput? 4. As the number of agents and tasks increases, which architecture shows the slowest degradation in throughput and travel distance? 5. Under purely individual reward structures, do storage–routing policies concentrate traffic on a small set of storage locations and paths (commons-like overuse)? 6. Do congestion-sensitive rewards reduce this concentration and improve performance? 7. In distributed controllers, does enabling local communication improve throughput and reduce congestion? 8. When new agents are added, does the system maintain stable performance?

# Other work that needs to be handled

1. Reduce the amount of memory we use when we design a graph and the local sub graph: memory_reduction_plan.md and the embed_once_design.md whereas we embed the graph once. 
2. Looking into the research goals: research_goals_2026-10-18.md as we stated in how we observe a run and make sure they make sense to messaure and why.
3. Figure out the Relocation cost does not make sense for moving new items that arrive, this only makes sense for items that is already on the graph in a node. So here we have to rethink if there is a cost, or we should let the SLAP controller learn when to move the items as in SLAP or DSLAP. Since as of now it is false what we do. stock_template_2026-10-17.md what was implemented. storage_mode_prompt.md
4. Look into Ray Rllib and how the we should handle the new API stack so we reduce the amount of errors or warning and have migrated to the new API stack. 

# Where to start

1. We should propably start with the critical things. So start with finding out the GAPS as 