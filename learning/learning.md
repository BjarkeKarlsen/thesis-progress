
## Thoughs about the code

## How do validate which run is the best?

For every iteration we calculate a episode_return_mean but is it based on just this episode or is it acctually right now based on multiple episodes. Since it goes up per time so does it take the total amount of task delivered? If it does then this is the wrong way to validate that the step in this episode was wrong since the whole iteration should complete as many task as possible.

# Task Assigner

Token Passing picks its own tasks. Because this is a controller for the arms/controller (centralised, section-based, decentralised) then they can pick theor own task.

# Action masking

Is where we mask illegale moves. But what purpose does it serve? does it improve that the agent does not try to do this move again or do we accutally need more logic to know this. It would need some kind of signal that this has been masked? Or we also have the override loss, so where does this differe and is it not the same and how can happen to take a move that need to be overrriden? The override_penalty is given in the multi_agent_env.py

# RL Module i need to understand that

# GNN_encoder is it the graph?

Look into of the Gnn encoder is just the graph anmd the we have the local_subgraph_encoding which is kinda a duplication of graphs

# Base has two heads

There is a head for policy and for the graph. Here i need to understand what is going on.

# Need general understanding of how planners is being built.
