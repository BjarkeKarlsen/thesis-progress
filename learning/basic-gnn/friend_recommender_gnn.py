import torch
import torch.nn as nn
from simple_gnn import SimpleGNNLayer

class FriendRecommenderGNN(nn.Module):
    """
    Complete GNN model for friend recommendation.

    This version:
    - Uses two GNN layers to compute node embeddings.
    - Computes a friendship score for every ordered pair (i, j).
    - Returns a symmetric score matrix with values in (0, 1) via sigmoid,
      matching the behavior of the loop-based version.
    """
    def __init__(self, input_dim, hidden_dim) -> None:
        super(FriendRecommenderGNN, self).__init__()
        # Two GNN layers for message passing / representation learning
        self.gnn1 = SimpleGNNLayer(input_dim, hidden_dim)
        self.gnn2 = SimpleGNNLayer(hidden_dim, hidden_dim)

        # Linear layer that maps concatenated pair embeddings to a single score
        # Input: 2 * hidden_dim (embedding of node i + embedding of node j)
        # Output: 1 logit per pair
        self.predictor = nn.Linear(hidden_dim * 2, 1)
   
    def forward(self, X, A)-> torch.Tensor:
        """
        Forward pass for the GNN model.

        Args:
            X: Node feature matrix of shape (num_nodes, input_dim).
            A: Adjacency matrix of shape (num_nodes, num_nodes).

        Returns:
            Friendship score matrix of shape (num_nodes, num_nodes),
            symmetric, with values in (0, 1) after sigmoid.
        """

        # Pass input through GNN layers
        H1 = self.gnn1(X, A)  # First GNN layer embeddings
        H2 = self.gnn2(H1, A)  # Second GNN layer embeddings

        # Generate friendship predictions
        friendship_scores = self.predict_friendship(H2)
        return friendship_scores

    def predict_friendship(self, H: torch.Tensor) -> torch.Tensor:
        """
        Computes friendship scores between all pairs of users.

        This implements the same logic as the nested-loop version:
        - For each pair (i, j), concatenate H[i] and H[j].
        - Apply the linear predictor and a sigmoid to get a score in (0, 1).
        - Ensure the score matrix is symmetric: score(i, j) == score(j, i).

        Args:
            H: Node embeddings from GNN layers,
               shape (num_nodes, hidden_dim).

        Returns:
            Friendship score matrix of shape (num_nodes, num_nodes),
            symmetric, with values in (0, 1).
        """
        num_nodes = H.size(0)

        # Expand embeddings to form all pairs (i, j)
        # H_expanded_1[i, j, :] = H[i, :]  (repeat along dim=1)
        # H_expanded_2[i, j, :] = H[j, :]  (repeat along dim=0)
        H_expanded_1 = H.unsqueeze(1).expand(-1, num_nodes, -1)  # (num_nodes, num_nodes, hidden_dim)
        H_expanded_2 = H.unsqueeze(0).expand(num_nodes, -1, -1)  # (num_nodes, num_nodes, hidden_dim)

        # Concatenate embeddings for each pair: [H[i], H[j]]
        pairwise_embeddings = torch.cat(
            [H_expanded_1, H_expanded_2],
            dim=-1
        )  # (num_nodes, num_nodes, hidden_dim * 2)

        # Apply linear predictor to get logits for all pairs
        logits = self.predictor(pairwise_embeddings).squeeze(-1)  # (num_nodes, num_nodes)

        # Apply sigmoid to match version 2's use of torch.sigmoid
        scores = torch.sigmoid(logits)  # (num_nodes, num_nodes), values in (0, 1)

        # Enforce symmetry explicitly to match the loop version:
        # scores[i, j] = scores[j, i]
        scores = (scores + scores.t()) / 2.0

        return scores