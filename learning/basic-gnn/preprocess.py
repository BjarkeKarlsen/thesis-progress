import torch

def preprocess_adjacency(A: torch.Tensor) -> torch.Tensor:
    """
    Preprocesses the adjacency matrix for GNN input.

    This function:
    - Adds self-loops to preserve each node's own features.
    - Applies symmetric degree normalization to balance neighbor influence.

    Mathematically:
        1. Add self-loops:      Ā = A + I
        2. Compute degrees:     D̄_ii = sum_j Ā_ij
        3. Symmetric normalize: Ā_norm = D̄^(-1/2) Ā D̄^(-1/2)

    Args:
        A: Adjacency matrix of shape (num_nodes, num_nodes).

    Returns:
        A_norm: Symmetrically normalized adjacency matrix with self-loops,
                same shape and device as A.
    """
    num_nodes = A.size(0)
    device = A.device

    # 1. Add self-loops: Ā = A + I
    #    This ensures each node also aggregates its own features.
    I = torch.eye(num_nodes, device=device)
    A_hat = A + I

    # 2. Compute degree vector: d_i = sum_j Ā_ij
    #    d_hat[i] is the (augmented) degree of node i.
    d_hat = A_hat.sum(dim=1)  # Shape: (num_nodes,)

    # 3. Compute D̄^(-1/2) as a vector: d_i^(-1/2)
    #    We use the vector of inverse square-root degrees to rescale edges.
    #    Adding eps avoids division by zero if any degree is 0.
    eps = 1e-8
    d_hat_inv_sqrt = torch.pow(d_hat + eps, -0.5)  # Shape: (num_nodes,)

    # 4. Apply symmetric normalization:
    #    We want: Ā_norm[i, j] = Ā[i, j] * d_i^(-1/2) * d_j^(-1/2)
    #
    #    d_hat_inv_sqrt.view(-1, 1) is a column vector: [d_0^-0.5, d_1^-0.5, ...]^T
    #    d_hat_inv_sqrt.view(1, -1) is a row vector:    [d_0^-0.5, d_1^-0.5, ...]
    #
    #    Multiplying:
    #      A_hat * d_col * d_row
    #    scales each element A_hat[i, j] by d_i^-0.5 from the row side
    #    and by d_j^-0.5 from the column side, implementing:
    #      Ā_norm = D̄^(-1/2) Ā D̄^(-1/2)
    #    without explicitly forming the diagonal matrices.
    A_norm = A_hat * d_hat_inv_sqrt.view(-1, 1) * d_hat_inv_sqrt.view(1, -1)

    return A_norm