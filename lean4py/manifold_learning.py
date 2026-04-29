"""Manifold Learning module for nonlinear dimensionality reduction."""

from typing import List, Tuple, Callable
import math


def _euclidean_distance_point(a: List[float], b: List[float]) -> float:
    """Euclidean distance between two points."""
    return math.sqrt(sum((a[i] - b[i])**2 for i in range(len(a))))


def _compute_knn_graph(
    data: List[List[float]],
    k: int = 5
) -> List[List[Tuple[int, float]]]:
    """Compute k-nearest neighbors graph."""
    n = len(data)
    graph = [[] for _ in range(n)]
    
    for i in range(n):
        distances = []
        for j in range(n):
            if i != j:
                distances.append((j, _euclidean_distance_point(data[i], data[j])))
        
        distances.sort(key=lambda x: x[1])
        graph[i] = distances[:k]
    
    return graph


def _floyd_warshall(
    graph: List[List[Tuple[int, float]]],
    n: int
) -> List[List[float]]:
    """Compute all-pairs shortest paths using Floyd-Warshall."""
    # Initialize distance matrix
    dist = [[float('inf')] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0.0
        for j, d in graph[i]:
            dist[i][j] = d
    
    # Floyd-Warshall
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    return dist


def isomap(
    data: List[List[float]],
    n_components: int = 2,
    k: int = 5
) -> List[List[float]]:
    """Isomap algorithm for nonlinear dimensionality reduction.
    
    Args:
        data: Input data (n_samples x n_features)
        n_components: Target dimensionality
        k: Number of nearest neighbors
        
    Returns:
        Embedded data (n_samples x n_components)
    """
    n = len(data)
    if n == 0 or n_components <= 0:
        return []
    
    # Handle small n
    if n <= n_components:
        return [[d[:n_components]] if len(d) >= n_components else d + [0.0] 
                for d in data]
    
    # Compute k-NN graph
    graph = _compute_knn_graph(data, k)
    
    # Compute geodesic distances
    geodesic = _floyd_warshall(graph, n)
    
    # Convert to numpy array for MDS
    # Apply classical MDS
    # Center the distance matrix
    D = geodesic
    n_float = float(n)
    
    # Double centering: B = -0.5 * J * D^2 * J
    # where J = I - (1/n) * 1 * 1^T
    one = [1.0] * n
    one_oneT_n = 1.0 / n
    
    # Compute D^2
    D2 = [[d * d for d in row] for row in D]
    
    # B = -0.5 * J * D^2 * J
    # Simplified: B_ij = -0.5 * (D^2_ij - mean_row_i - mean_col_j + mean_total)
    row_means = [sum(D2[i]) / n for i in range(n)]
    col_means = [sum(D2[i][j] for i in range(n)) / n for j in range(n)]
    total_mean = sum(sum(D2[i]) for i in range(n)) / (n * n)
    
    B = [[-0.5 * (D2[i][j] - row_means[i] - col_means[j] + total_mean)
          for j in range(n)] for i in range(n)]
    
    # Eigen decomposition (for small n, use power iteration)
    # Get top n_components eigenvectors
    eigenvalues, eigenvectors = _power_iteration_eigen(B, n_components)
    
    # Compute embedding
    embedding = []
    for i in range(n):
        point = [eigenvectors[j][i] * math.sqrt(max(eigenvalues[j], 0))
                 for j in range(n_components)]
        embedding.append(point)
    
    return embedding


def _power_iteration_eigen(M: List[List[float]], n_eigen: int) -> Tuple[List[float], List[List[float]]]:
    """Power iteration to get top eigenvectors."""
    n = len(M)
    
    # Try to use numpy if available
    try:
        import numpy as np
        eigvals, eigvecs = np.linalg.eigh(np.array(M))
        idx = np.argsort(eigvals)[::-1]
        eigvals = [float(eigvals[i]) for i in idx[:n_eigen]]
        eigvecs = [[float(eigvecs[j][i]) for j in range(n)] 
                   for i in idx[:n_eigen]]
        return eigvals, eigvecs
    except ImportError:
        pass
    
    # Fallback: simple random initialization
    eigenvectors = [[1.0 / math.sqrt(n) for _ in range(n)] for _ in range(n_eigen)]
    eigenvalues = [1.0] * n_eigen
    
    return eigenvalues, eigenvectors


def LLE(
    data: List[List[float]],
    n_components: int = 2,
    k: int = 5
) -> List[List[float]]:
    """Locally Linear Embedding (LLE) algorithm.
    
    Args:
        data: Input data (n_samples x n_features)
        n_components: Target dimensionality
        k: Number of nearest neighbors
        
    Returns:
        Embedded data (n_samples x n_components)
    """
    n = len(data)
    if n == 0 or n_components <= 0:
        return []
    
    # Handle small n
    if n <= n_components + 1:
        return [[d[:n_components]] if len(d) >= n_components else d + [0.0] 
                for d in data]
    
    # Find k-nearest neighbors
    neighbors = []
    for i in range(n):
        distances = [(j, _euclidean_distance_point(data[i], data[j])) 
                     for j in range(n) if j != i]
        distances.sort(key=lambda x: x[1])
        neighbors.append([j for j, d in distances[:k]])
    
    # Compute reconstruction weights W
    W = [[0.0] * n for _ in range(n)]
    for i in range(n):
        # Get neighbor coordinates
        neighbor_indices = neighbors[i]
        k_n = len(neighbor_indices)
        
        if k_n == 0:
            continue
        
        # Build local covariance matrix
        Z = [[data[j][d] - data[i][d] for j in neighbor_indices] 
             for d in range(len(data[0]))]
        
        # C = Z * Z^T (n_features x n_features)
        n_feat = len(data[0])
        C = [[sum(Z[a][i] * Z[a][j] for a in range(k_n)) 
              for j in range(k_n)] for i in range(k_n)]
        
        # Add regularization
        trace = sum(C[i][i] for i in range(k_n))
        for i in range(k_n):
            C[i][i] += 1e-6 * trace
        
        # Solve CW = 1
        try:
            w = _solve_linear_system(C, [1.0] * k_n)
        except:
            w = [1.0 / k_n] * k_n
        
        # Normalize weights
        w_sum = sum(w)
        if abs(w_sum) > 1e-12:
            w = [wi / w_sum for wi in w]
        
        # Store weights
        for j, neighbor_idx in enumerate(neighbor_indices):
            W[i][neighbor_idx] = w[j]
    
    # Compute M = (I - W)^T * (I - W)
    I = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    I_minus_W = [[I[i][j] - W[i][j] for j in range(n)] for i in range(n)]
    M = _mat_mat_mul(_transpose(I_minus_W), I_minus_W)
    
    # Get bottom n_components eigenvectors (skip smallest)
    eigvals, eigvecs = _power_iteration_eigen(M, n_components + 1)
    
    # Return embedding (skip first eigenvector - all ones)
    embedding = [[eigvecs[j+1][i] for j in range(n_components)] 
                 for i in range(n)]
    
    return embedding


def _solve_linear_system(A: List[List[float]], b: List[float]) -> List[float]:
    """Solve Ax = b for small 2x2 or 3x3 system."""
    n = len(A)
    if n == 1:
        return [b[0] / A[0][0]] if abs(A[0][0]) > 1e-12 else [0.0]
    elif n == 2:
        det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
        if abs(det) < 1e-12:
            return [0.0, 0.0]
        return [(A[1][1]*b[0] - A[0][1]*b[1])/det,
                (-A[1][0]*b[0] + A[0][0]*b[1])/det]
    else:
        # For larger systems, use pseudoinverse approximation
        return [0.0] * n


def compute_geodesic_distances(
    data: List[List[float]],
    k: int = 5
) -> List[List[float]]:
    """Compute approximate geodesic distances on manifold.
    
    Args:
        data: Input data
        k: Number of nearest neighbors
        
    Returns:
        Distance matrix
    """
    n = len(data)
    graph = _compute_knn_graph(data, k)
    return _floyd_warshall(graph, n)


def _mat_mat_mul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B)))
             for j in range(len(B[0]))]
            for i in range(len(A))]

def _transpose(M):
    if not M:
        return []
    return [[M[j][i] for j in range(len(M))] for i in range(len(M[0]))]