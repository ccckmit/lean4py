"""Kalman Filter module for linear Gaussian state space models."""

from typing import List, Tuple, Optional
import math


class KalmanFilter:
    """Kalman Filter for linear dynamical systems.
    
    State transition: x_{t+1} = F * x_t + w, w ~ N(0, Q)
    Observation: z_t = H * x_t + v, v ~ N(0, R)
    """
    
    def __init__(
        self,
        state_dim: int,
        obs_dim: int,
        F: Optional[List[List[float]]] = None,
        H: Optional[List[List[float]]] = None,
        Q: Optional[List[List[float]]] = None,
        R: Optional[List[List[float]]] = None,
        x0: Optional[List[float]] = None,
        P0: Optional[List[List[float]]] = None
    ):
        self.state_dim = state_dim
        self.obs_dim = obs_dim
        
        # Default matrices
        if F is None:
            F = [[1.0 if i == j else 0.0 for j in range(state_dim)] 
                 for i in range(state_dim)]
        if H is None:
            H = [[1.0 if i == j else 0.0 for j in range(state_dim)] 
                 for i in range(obs_dim)]
        if Q is None:
            Q = [[0.1 if i == j else 0.0 for j in range(state_dim)] 
                 for i in range(state_dim)]
        if R is None:
            R = [[0.1 if i == j else 0.0 for j in range(obs_dim)] 
                 for i in range(obs_dim)]
        if x0 is None:
            x0 = [0.0] * state_dim
        if P0 is None:
            P0 = [[1.0 if i == j else 0.0 for j in range(state_dim)] 
                  for i in range(state_dim)]
        
        self.F = F
        self.H = H
        self.Q = Q
        self.R = R
        self.x = x0
        self.P = P0
    
    def predict(self) -> List[float]:
        """Prediction step: x_{t|t-1} = F * x_{t-1|t-1}
        
        Returns:
            Predicted state
        """
        # x = F * x
        self.x = self._mat_vec_mul(self.F, self.x)
        
        # P = F * P * F^T + Q
        FP = self._mat_mat_mul(self.F, self.P)
        self.P = self._add_matrices(FP, self._transpose(self.F), self.Q)
        
        return self.x
    
    def update(self, z: List[float]) -> List[float]:
        """Update step: incorporate observation z_t.
        
        Args:
            z: Observation vector
            
        Returns:
            Updated state estimate
        """
        # Innovation: y = z - H * x
        Hx = self._mat_vec_mul(self.H, self.x)
        y = [z[i] - Hx[i] for i in range(self.obs_dim)]
        
        # Innovation covariance: S = H * P * H^T + R
        HP = self._mat_mat_mul(self.H, self.P)
        S = self._add_matrices(HP, self._transpose(self.H), self.R)
        
        # Kalman gain: K = P * H^T * S^{-1}
        K = self._kalman_gain(S)
        
        # Update state: x = x + K * y
        self.x = self._add_vectors(self.x, self._mat_vec_mul(K, y))
        
        # Update covariance: P = (I - K * H) * P
        IKH = self._subtract_matrices(
            [[1.0 if i == j else 0.0 for j in range(self.state_dim)] for i in range(self.state_dim)],
            self._mat_mat_mul(K, self.H)
        )
        self.P = self._mat_mat_mul(IKH, self.P)
        
        return self.x
    
    def _kalman_gain(self, S: List[List[float]]) -> List[List[float]]:
        """Compute Kalman gain K = P * H^T * S^{-1}."""
        # For simplicity, use pseudoinverse approach
        HT = self._transpose(self.H)
        PH = self._mat_mat_mul(self.P, HT)
        
        # Simple 2x2 or 1x1 inverse
        S_inv = self._matrix_inverse_2x2(S) if len(S) <= 2 else self._pseudo_inverse(S)
        
        return self._mat_mat_mul(PH, S_inv)
    
    def _matrix_inverse_2x2(self, M: List[List[float]]) -> List[List[float]]:
        """Inverse of 1x1 or 2x2 matrix."""
        n = len(M)
        if n == 1:
            if abs(M[0][0]) < 1e-12:
                return [[1.0]]
            return [[1.0 / M[0][0]]]
        
        # 2x2 inverse
        a, b = M[0][0], M[0][1]
        c, d = M[1][0], M[1][1]
        det = a * d - b * c
        
        if abs(det) < 1e-12:
            return [[1.0, 0.0], [0.0, 1.0]]
        
        return [[d/det, -b/det], [-c/det, a/det]]
    
    def _pseudo_inverse(self, M: List[List[float]]) -> List[List[float]]:
        """Simple pseudoinverse for larger matrices."""
        n = len(M)
        # Approximation: divide by diagonal elements
        result = [[0.0] * n for _ in range(n)]
        for i in range(n):
            if abs(M[i][i]) > 1e-12:
                result[i][i] = 1.0 / M[i][i]
        return result
    
    def _mat_vec_mul(self, A: List[List[float]], v: List[float]) -> List[float]:
        """Matrix-vector multiplication."""
        return [sum(A[i][j] * v[j] for j in range(len(v))) 
                for i in range(len(A))]
    
    def _mat_mat_mul(self, A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
        """Matrix-matrix multiplication."""
        return [[sum(A[i][k] * B[k][j] for k in range(len(B)))
                 for j in range(len(B[0]))]
                for i in range(len(A))]
    
    def _transpose(self, M: List[List[float]]) -> List[List[float]]:
        """Matrix transpose."""
        return [[M[j][i] for j in range(len(M))] for i in range(len(M[0]))]
    
    def _add_matrices(self, A: List[List[float]], B: List[List[float]], 
                      C: List[List[float]]) -> List[List[float]]:
        """A * B^T + C (specific for Kalman filter)"""
        BT = self._transpose(B)
        AB = self._mat_mat_mul(A, BT)
        return [[AB[i][j] + C[i][j] for j in range(len(C[0]))] 
                for i in range(len(C))]
    
    def _add_vectors(self, a: List[float], b: List[float]) -> List[float]:
        """Vector addition."""
        return [a[i] + b[i] for i in range(len(a))]
    
    def _subtract_matrices(self, A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
        """Matrix subtraction."""
        return [[A[i][j] - B[i][j] for j in range(len(A[0]))] 
                for i in range(len(A))]


def kalman_smooth(
    xs: List[List[float]],
    Ps: List[List[List[float]]],
    F: List[List[float]]
) -> Tuple[List[List[float]], List[List[List[float]]]]:
    """Rauch-Tung-Striebel smoother for Kalman filter.
    
    Args:
        xs: Filtered state means
        Ps: Filtered state covariances
        F: State transition matrix
        
    Returns:
        (smoothed_xs, smoothed_Ps)
    """
    T = len(xs)
    if T == 0:
        return [], []
    
    smoothed_xs = [None] * T
    smoothed_Ps = [None] * T
    
    smoothed_xs[T-1] = xs[T-1]
    smoothed_Ps[T-1] = Ps[T-1]
    
    for t in range(T-2, -1, -1):
        # Predicted covariance
        FP = _mat_mat_mul(F, Ps[t])
        FPFt = _mat_mat_mul(FP, _transpose(F))
        
        # Add process noise (simplified)
        for i in range(len(FPFt)):
            FPFt[i][i] += 0.1
        
        # Smoother gain
        PFPFt = _mat_mat_mul(Ps[t], _transpose(F))
        
        det = _det(FPFt)
        if abs(det) < 1e-12:
            continue
            
        FPFt_inv = _inverse_2x2(FPFt)
        G = _mat_mat_mul(PFPFt, FPFt_inv)
        
        # Smooth state
        x_pred = _mat_vec_mul(F, xs[t])
        smoothed_xs[t] = _add_vectors(
            xs[t],
            _mat_vec_mul(G, _subtract_vectors(smoothed_xs[t+1], x_pred))
        )
        
        # Smooth covariance
        I = [[1.0 if i == j else 0.0 for j in range(len(xs[t]))] 
             for i in range(len(xs[t]))]
        GF = _mat_mat_mul(G, F)
        smoothed_Ps[t] = _add_matrices(
            Ps[t],
            _mat_mat_mul(_subtract_matrices(I, GF), Ps[t])
        )
    
    return smoothed_xs, smoothed_Ps


def _mat_vec_mul(A, v):
    return [sum(A[i][j] * v[j] for j in range(len(v))) for i in range(len(A))]

def _mat_mat_mul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B)))
             for j in range(len(B[0]))]
            for i in range(len(A))]

def _transpose(M):
    return [[M[j][i] for j in range(len(M))] for i in range(len(M[0]))]

def _add_vectors(a, b):
    return [a[i] + b[i] for i in range(len(a))]

def _subtract_vectors(a, b):
    return [a[i] - b[i] for i in range(len(a))]

def _add_matrices(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] 
            for i in range(len(A))]

def _subtract_matrices(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] 
            for i in range(len(A))]

def _det(M):
    n = len(M)
    if n == 1:
        return M[0][0]
    if n == 2:
        return M[0][0] * M[1][1] - M[0][1] * M[1][0]
    return 0.0

def _inverse_2x2(M):
    det = _det(M)
    if abs(det) < 1e-12:
        return [[1.0, 0.0], [0.0, 1.0]]
    return [[M[1][1]/det, -M[0][1]/det], [-M[1][0]/det, M[0][0]/det]]