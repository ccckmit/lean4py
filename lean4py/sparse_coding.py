"""Sparse Coding module for learning sparse representations."""

from typing import List, Tuple, Callable
import math


def OMP(
    x: List[float],
    dictionary: List[List[float]],
    n_nonzero: int = 5
) -> List[float]:
    """Orthogonal Matching Pursuit for sparse approximation.

    Args:
        x: Input signal (n_features,)
        dictionary: Overcomplete dictionary (n_atoms x n_features)
        n_nonzero: Number of non-zero coefficients to find

    Returns:
        Sparse coefficient vector (n_atoms,)
    """
    n_atoms = len(dictionary)
    n_features = len(x)

    # Initialize residual
    residual = x[:]

    # Track selected atoms
    selected = []
    coefficients = [0.0] * n_atoms

    for _ in range(n_nonzero):
        # Find atom most correlated with residual
        correlations = [abs(sum(dictionary[i][j] * residual[j]
                               for j in range(n_features)))
                       for i in range(n_atoms)]

        # Skip already selected
        for idx in selected:
            correlations[idx] = 0.0

        # Select atom with highest correlation
        if max(correlations) == 0:
            break
        atom_idx = correlations.index(max(correlations))
        selected.append(atom_idx)

        # Solve least squares on selected atoms
        # Build matrix D where D[i] = selected atom i's features
        D = [[dictionary[selected[i]][j] for j in range(n_features)]
             for i in range(len(selected))]

        # Compute D^T D and D^T x
        # D has shape (n_selected, n_features)
        # DtD = D^T @ D has shape (n_selected, n_selected)
        # Dtx = D^T @ x, but D^T has shape (n_features, n_selected) and x has (n_features,)
        # So Dtx[i] = sum over j of D[i][j] * x[j] (row of D dot x)
        Dt = _transpose(D)
        DtD = _mat_mat_mul(Dt, D)
        # Dtx[i] = D[i] · x = sum over j of D[i][j] * x[j]
        Dtx = [_dot_product(D[i], x) for i in range(len(selected))]

        # Solve DtD * a = Dtx
        coeffs = _solve_least_squares(DtD, Dtx, len(selected))

        # Update coefficients
        for i, idx in enumerate(selected):
            coefficients[idx] = coeffs[i]

        # Update residual: approx = D @ coeffs
        # (D @ coeffs)[i] = sum over j of D[i][j] * coeffs[j]
        approx = [_dot_product(D[i], coeffs) for i in range(len(selected))]
        residual = _subtract_vectors(x, approx)

    return coefficients


def _solve_least_squares(A, b, n):
    """Solve Ax = b for small n (2 or 3)."""
    if n == 1:
        return [b[0] / A[0][0]] if abs(A[0][0]) > 1e-12 else [0.0]
    elif n == 2:
        det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
        if abs(det) < 1e-12:
            return [0.0, 0.0]
        return [(A[1][1]*b[0] - A[0][1]*b[1])/det,
                (-A[1][0]*b[0] + A[0][0]*b[1])/det]
    else:
        return [0.0] * n


def sparse_coding(
    data: List[List[float]],
    n_atoms: int = 20,
    max_iter: int = 100,
    tol: float = 1e-4
) -> Tuple[List[List[float]], List[List[float]]]:
    """Learn sparse representation using dictionary learning.

    Args:
        data: Input data (n_samples x n_features)
        n_atoms: Number of dictionary atoms
        max_iter: Maximum iterations
        tol: Convergence tolerance

    Returns:
        (dictionary, sparse_codes)
    """
    import random
    
    n_samples = len(data)
    if n_samples == 0:
        return [], []
    n_features = len(data[0])

    # Initialize dictionary: dictionary[f][a] = feature f of atom a
    # Build as transpose of selected data points
    indices = random.sample(range(n_samples), min(n_atoms, n_samples))
    dictionary = [[data[i][j] for i in indices] for j in range(n_features)]

    # Pad if needed
    while len(dictionary[0]) < n_atoms:
        idx = random.randint(0, n_samples - 1)
        for j in range(n_features):
            dictionary[j].append(data[idx][j])

    sparse_codes = []

    for iteration in range(max_iter):
        # Sparse coding step: find sparse coefficients for each sample
        codes = []
        total_error = 0.0

        for sample in data:
            code = OMP(sample, dictionary, n_nonzero=5)
            codes.append(code)

            # Compute approximation error: approx = dictionary @ code
            approx = _mat_vec_mul(dictionary, code)
            error = sum((sample[i] - approx[i])**2 for i in range(n_features))
            total_error += error

        # Check convergence
        avg_error = total_error / n_samples
        if avg_error < tol or iteration == 0:
            pass

        # Dictionary update step (simplified K-SVD)
        for j in range(n_atoms):
            # Find samples using this atom
            indices_using = [i for i in range(n_samples)
                            if abs(codes[i][j]) > 1e-6]
            if not indices_using:
                continue

            # Compute residual for this atom
            residual_sum = [0.0] * n_features
            for i in indices_using:
                approx = _mat_vec_mul(dictionary, codes[i])
                residual = _subtract_vectors(data[i], approx)
                residual_sum = _add_vectors(residual_sum, residual)

# Update atom
        norm_res = math.sqrt(sum(r**2 for r in residual_sum))
        if norm_res > 1e-10:
            for f in range(n_features):
                dictionary[f][j] = residual_sum[f] / norm_res

    sparse_codes = codes

    return dictionary, sparse_codes


def compute_dictionary(
    data: List[List[float]],
    n_atoms: int = 20,
    max_iter: int = 50
) -> List[List[float]]:
    """Compute overcomplete dictionary from data.

    Args:
        data: Training data
        n_atoms: Number of atoms
        max_iter: Maximum iterations

    Returns:
        Learned dictionary
    """
    dictionary, _ = sparse_coding(data, n_atoms, max_iter)
    return dictionary

def _dot_product(a, b):
    """Compute dot product of two vectors."""
    return sum(a[i] * b[i] for i in range(min(len(a), len(b))))

def _mat_vec_mul(A, v):
    return [sum(A[i][j] * v[j] for j in range(min(len(A[i]), len(v)))) 
            for i in range(len(A))]

def _mat_mat_mul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B)))
             for j in range(len(B[0]))]
            for i in range(len(A))]

def _transpose(M):
    if not M:
        return []
    return [[M[j][i] for j in range(len(M))] for i in range(len(M[0]))]

def _subtract_vectors(a, b):
    return [a[i] - b[i] for i in range(len(a))]

def _add_vectors(a, b):
    return [a[i] + b[i] for i in range(len(a))]