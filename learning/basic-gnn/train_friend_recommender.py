from torch.optim import Adam
from torch.nn import functional as F
from social_graph import create_social_network_data  # For creating synthetic social network data
from social_graph_visualize import visualize_social_graph  # For visualizing the social network graph
from visualize_friendship_scores_with_existing import visualize_friendship_scores_with_existing  # For visualizing friendship scores
from friend_recommender_gnn import FriendRecommenderGNN  # The GNN model for friend recommendation
from preprocess import preprocess_adjacency  # For preprocessing the adjacency matrix


def train_friend_recommender():
    """
    Trains the GNN model for friend recommendation
    Returns:
        model: Trained GNN model
        X: User features
        A: Adjacency matrix
    """

    # Initialize dataset
    X, A = create_social_network_data(num_users=6)

    # Preprocess adjacency matrix (add self-loops and normalize)
    A_normalized = preprocess_adjacency(A)
    # Show initial network structure
    visualize_social_graph(A)

    # Model initialization
    model = FriendRecommenderGNN(input_dim=3, hidden_dim=16)
    optimizer = Adam(model.parameters(), lr=0.01)

    # Training loop

    for epoch in range(100):
        model.train()
        optimizer.zero_grad() # Reset gradients

        # Forward pass
        friendship_scores = model(X, A_normalized)

        # Calculate binary cross entropy loss
        loss = F.binary_cross_entropy(friendship_scores, A)

        # Backward pass and optimization
        loss.backward()
        optimizer.step()

        # Print progress every 20 epochs
        if epoch % 20 == 0:
            print(f"Epoch {epoch}, Loss: {loss.item():.4f}")

    return model, X, A