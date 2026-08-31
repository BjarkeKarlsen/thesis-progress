#%%
from social_graph import create_social_network_data
from social_graph_visualize import visualize_social_graph

# Create synthetic social network data
X, A = create_social_network_data(num_users=6)

# Visualize the social network graph
visualize_social_graph(A)
# %%
