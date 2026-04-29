"""Gaussian Process regression module."""

from typing import List, Tuple, Callable, Optional
import math


def rbf_kernel(x1: List[float], x2: List[float], length_scale: float = 1.0) -> float:
    """Radial Basis Function (RBF) kernel.
    
    k(x1, x2) = exp(-||x1 - x2||^2 / (2 * length_scale^2))
    
    Args:
        x1, x2: Input vectors
        length_scale: Kernel length scale parameter
        
    Returns:
        Kernel value
    """
    if len(x1) != len(x2):
        return 0.0
    
    squared_dist = sum((x1[i] - x2[i]) ** 2 for i in range(len(x1)))
    return math.exp(-squared_dist / (2 * length_scale ** 2))


class GaussianProcessRegressor:
    """Gaussian Process Regressor."""
    
    def __init__(self, kernel: Optional[Callable] = None, noise: float = 1e-8):
        self.kernel = kernel if kernel else \
            (lambda x1, x2: rbf_kernel(x1, x2, length_scale=1.0))
        self.noise = noise
        self.X_train = None
        self.y_train = None
        self.K_inv = None
    
    def fit(self, X: List[List[float]], y: List[float]):
        """Fit the GP to training data.
        
        Args:
            X: Training inputs (n_samples x n_features)
            y: Training targets (n_samples,)
        """
        self.X_train = X
        self.y_train = y
        n = len(X)
        
        # Compute kernel matrix K
        K = [[self.kernel(X[i], X[j]) for j in range(n)] for i in range(n)]
        
        # Add noise to diagonal
        for i in range(n):
            K[i][i] += self.noise
        
        # Invert K (simple inversion for small datasets)
        self.K_inv = self._invert_matrix(K)
        self.y_train = y
    
    def predict(self, X_test: List[List[float]]) -> Tuple[List[float], List[float]]:
        """Predict mean and variance for test points.
        
        Args:
            X_test: Test inputs
            
        Returns:
            (mean_predictions, variance_predictions)
        """
        if self.X_train is None:
            return [], []
        
        n_train = len(self.X_train)
        n_test = len(X_test)
        
        # Compute k* (kernel between test and training)
        k_star = [[self.kernel(X_test[i], self.X_train[j]) 
                   for j in range(n_train)] for i in range(n_test)]
        
        # Mean: k*^T @ K_inv @ y
        means = []
        for i in range(n_test):
            mean = sum(k_star[i][j] * sum(self.K_inv[j][k] * self.y_train[k] 
                                        for k in range(n_train))
                      for j in range(n_train))
            means.append(mean)
        
        # Variance: k(x,x) - k*^T @ K_inv @ k*
        variances = []
        for i in range(n_test):
            # k(x, x)
            k_xx = self.kernel(X_test[i], X_test[i])
            
            # k*^T @ K_inv @ k*
            temp = [sum(self.K_inv[j][k] * k_star[i][k] for k in range(n_train))
                    for j in range(n_train)]
            k_Kinv_k = sum(k_star[i][j] * temp[j] for j in range(n_train))
            
            variances.append(max(k_xx - k_Kinv_k, 1e-10))
        
        return means, variances
    
    def _invert_matrix(self, A: List[List[float]]) -> List[List[float]]:
        """Simple matrix inversion using Gaussian elimination."""
        n = len(A)
        
        # Create augmented matrix [A | I]
        aug = [A[i][:] + [1.0 if j == i else 0.0 for j in range(n)] 
                for i in range(n)]
        
        # Gaussian elimination
        for col in range(n):
            # Find pivot
            pivot_row = col
            for row in range(col + 1, n):
                if abs(aug[row][col]) > abs(aug[pivot_row][col]):
                    pivot_row = row
            
            # Swap rows
            aug[col], aug[pivot_row] = aug[pivot_row], aug[col]
            
            # Normalize pivot row
            pivot = aug[col][col]
            if abs(pivot) < 1e-12:
                # Singular matrix, return identity
                return [[1.0 if i == j else 0.0 for j in range(n)] 
                        for i in range(n)]
            
            for j in range(2 * n):
                aug[col][j] /= pivot
            
            # Eliminate column
            for row in range(n):
                if row != col:
                    factor = aug[row][col]
                    for j in range(2 * n):
                        aug[row][j] -= factor * aug[col][j]
        
        # Extract inverse from right half
        return [aug[i][n:] for i in range(n)]


def predict_gp(
    X_train: List[List[float]],
    y_train: List[float],
    X_test: List[List[float]],
    kernel: Optional[Callable] = None,
    noise: float = 1e-8
) -> Tuple[List[float], List[float]]:
    """Convenience function for GP regression.
    
    Args:
        X_train: Training inputs
        y_train: Training targets
        X_test: Test inputs
        kernel: Kernel function (default: RBF)
        noise: Noise term
        
    Returns:
        (mean_predictions, std_predictions)
    """
    gp = GaussianProcessRegressor(kernel=kernel, noise=noise)
    gp.fit(X_train, y_train)
    means, variances = gp.predict(X_test)
    stds = [math.sqrt(v) for v in variances]
    return means, stds
