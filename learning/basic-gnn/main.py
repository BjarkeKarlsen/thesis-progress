from train_friend_recommender import train_friend_recommender
from visualize_friendship_scores_with_existing import visualize_friendship_scores_with_existing
from recommend_friends import recommend_friends
import torch
from matplotlib import pyplot as plot

def main():
    """
    Main execution function that ties everything together
    """
    # Train the GNN model for friend recommendation
    model, X, A = train_friend_recommender()

    # Generate predictions
    model.eval()
    with torch.no_grad():
        friendship_scores = model(X, A)

    # Visualize results
    print("\nFriendship Score Matrix vs Existing Friendships:")
    visualize_friendship_scores_with_existing(friendship_scores, A)

    # Show personalized recommendations
    recommend_friends(model, X, A)

    plot.show()  # Keep the plots open until closed by the user


if __name__ == "__main__":
    main()