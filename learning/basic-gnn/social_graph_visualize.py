import networkx as nx  # For graph visualization
import matplotlib.pyplot as plt  # For plotting
import torch  # For tensor operations

def visualize_social_graph(A: torch.Tensor) -> None:
    """
    Visualizes the social network graph using networkx
    Args:
        A: Adjacency matrix representing friendships
    """
    # Convert adjacency matrix to networkx graph
    G = nx.from_numpy_array(A.numpy())
    
    # Create and customize the visualization
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111)
    pos = nx.spring_layout(G)  # Position nodes using spring layout
    nx.draw(G, pos, 
            ax=ax,
            with_labels=True,  # Show node labels
            node_color='lightblue',
            node_size=500,
            font_size=16,
            font_weight='bold')
    
    plt.title("Social Network Graph")
    plt.tight_layout()
    plt.pause(0.001)
