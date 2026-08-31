from torch import Tensor  # For type hinting
import torch  # For tensor operations
from friend_recommender_gnn import FriendRecommenderGNN  # Import the G

def recommend_friends(model: FriendRecommenderGNN, X: Tensor, A: Tensor):
    """
    Recommends friends for each user based on the friendship score matrix.

    Args:
        model: The trained GNN model.
        X: Node feature matrix of shape (num_nodes, input_dim).
        A: Adjacency matrix of shape (num_nodes, num_nodes).
    Returns:
        recommendations: A list of recommended friends for each user.
    """

    model.eval()  # Set the model to evaluation mode
    with torch.no_grad():  # Disable gradient computation for inference
        predictions = model(X, A)  # Get friendship score matrix

        print("Friendship Recommendations:")
        for user in range(len(A)):
            # Get existing friends for current user
            existing_friends = set(torch.where(A[user] > 0)[0].tolist())

            # Calculate scores for pentential new friends
            potential_friends = []
            for other_user in range(len(A)):
                if other_user != user and other_user not in existing_friends:
                    score = predictions[user][other_user].item()
                    potential_friends.append((other_user, score))

            # Sort potential friends by score in descending order
            potential_friends.sort(key=lambda x: x[1], reverse=True)

            # Print recommendations
            print(f"\nUser {user}:")
            print(f"Current friends: {existing_friends}")
            print("Top 2 recommendations:", end=" ")
            for friend, score in potential_friends[:2]:
                print(f"User {friend} ({score:.3f})", end=" ")