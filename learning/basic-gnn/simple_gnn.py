import torch
import torch.nn as nn

class SimpleGNNLayer(nn.Module):
    """
    Basic Graph Neural Network layer implementing message passing
    """
    def __init__(self, in_features, out_features):
        super(SimpleGNNLayer, self).__init__()
        # Linear transformation for feature updating
        self.linear = nn.Linear(in_features, out_features)

    def forward(self, X, A):
        """
        Forward pass for the GNN layer
        Args:
            X: Node feature matrix (num_nodes x in_features)
            A: Adjacency matrix (num_nodes x num_nodes)
        """
        # Message passing: agregate neighbor features
        X = torch.mm(A, X)  # Matrix multiplication of adjacency matrix and features

        # Transform aggregated features through linear layer and ReLU activation
        X = self.linear(X)  # Apply linear transformation
        X = torch.relu(X)   # Apply non-linearity
        return X