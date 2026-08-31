import networkx as nx  # For graph visualization
import matplotlib.pyplot as plt  # For plotting
import torch  # For tensor operations

# Auxiliary Friendship Score Visualization
def visualize_friendship_scores_with_existing(predictions: torch.Tensor, A: torch.Tensor) -> None:
    """
    Creates side-by-side visualization of predicted friendship scores and existing friendships
    Args:
        predictions: Matrix of predicted friendship scores
        A: Actual adjacency matrix of existing friendships
    """

    # Create two subplots side by side
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Left subplot: Predicted friendship scores
    im1 = ax1.imshow(predictions.detach().numpy(), cmap='GnBu_r')
    ax1.set_title('Predicted Friendship Scores')
    plt.colorbar(im1, ax=ax1, label=" Friendship Score")

    # Right subplot: Existing friendships
    im2 = ax2.imshow(A.detach().numpy(), cmap='Blues')
    ax2.set_title('Existing Friendships')
    plt.colorbar(im2, ax=ax2, label="Connection Status")

    # Add labels and annotations to both plots
    for ax in [ax1, ax2]:
        ax.set_xlabel('User Id')
        ax.set_ylabel('User Id')

        # Add numerical values in each cell 
        for i in range(len(predictions)):
            for j in range(len(predictions)):
                text = f'{predictions[i, j]:.2f}' if ax == ax1 else str(int(A[i, j]))
                ax.text(j, i, text, ha='center', va='center')

    plt.tight_layout()
    plt.pause(0.001)