import torch  # PyTorch for deep learning
import torch.nn as nn  # Neural network modules
import torch.nn.functional as F  # Neural network functions

def create_social_network_data(num_users : int =6)  -> tuple[torch.Tensor, torch.Tensor]:
    """
    Creates synthetic social network data with user features and friendship connections
    Args:
        num_users: Number of users in the network
    Returns:
        X: User feature matrix (age, posts_count, friends_count)
        A: Adjacency matrix representing friendships
    """

    # User features matrix: Each row represents a user with [ age, posts_count, friends_count]
    X = torch.tensor([
        [25, 100, 50],   # User 0: 25 years old, 100 posts, 50 friends
        [30, 200, 100],  # User 1
        [28, 150, 75],   # User 2
        [35, 120, 30],   # User 3
        [22, 300, 150],  # User 4
        [27, 180, 80]    # User 5
    ], dtype=torch.float32)

    # Adjacency matrix: Represents who is friends with whom (symmetric matrix)
    A = torch.tensor([
        [0, 1, 0, 0, 1, 0],  # User 0's connections
        [1, 0, 1, 0, 0, 1],  # User 1's connections
        [0, 1, 0, 1, 0, 0],  # User 2's connections
        [0, 0, 1, 0, 1, 0],  # User 3's connections
        [1, 0, 0, 1, 0, 1],  # User 4's connections
        [0, 1, 0, 0, 1, 0]   # User 5's connections
    ], dtype=torch.float32)
    
    return X, A

