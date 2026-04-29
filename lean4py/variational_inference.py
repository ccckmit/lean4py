"""Variational Inference module for approximate Bayesian inference."""

from typing import List, Tuple, Callable, Optional
import math


class MeanFieldVI:
    """Mean Field Variational Inference.
    
    Assumes q(z) = prod q_i(z_i) where each q_i is a simple distribution.
    """
    
    def __init__(self, n_params: int, param_types: Optional[List[str]] = None):
        """Initialize VI with parameter dimensions.
        
        Args:
            n_params: Number of latent variables
            param_types: Types of distributions ('normal', 'bernoulli', etc.)
        """
        self.n_params = n_params
        if param_types is None:
            param_types = ['normal'] * n_params
        self.param_types = param_types
        
        # Initialize variational parameters
        # For normal: mean and log variance
        self.variational_params = []
        for _ in range(n_params):
            self.variational_params.append({'mean': 0.0, 'log_var': 0.0})
    
    def set_params(self, params: List[dict]):
        """Set variational parameters."""
        self.variational_params = params
    
    def sample(self, n_samples: int = 1) -> List[List[float]]:
        """Sample from variational distribution."""
        import random
        samples = []
        for _ in range(n_samples):
            sample = []
            for p in self.variational_params:
                if p.get('log_var', 0) > 10:
                    std = math.exp(5)
                else:
                    std = math.sqrt(math.exp(p.get('log_var', 0)))
                z = random.gauss(p['mean'], std)
                sample.append(z)
            samples.append(sample)
        return samples
    
    def get_means(self) -> List[float]:
        """Get means of variational distributions."""
        return [p['mean'] for p in self.variational_params]


def ELBO(
    log_likelihood: Callable[[List[float]], float],
    log_prior: Callable[[List[float]], float],
    q: MeanFieldVI,
    n_samples: int = 100
) -> float:
    """Compute Evidence Lower Bound (ELBO).
    
    ELBO = E_q[log p(x|z)] - KL(q||p)
    
    Args:
        log_likelihood: Log likelihood function log p(x|z)
        log_prior: Log prior function log p(z)
        q: Variational distribution
        n_samples: Number of Monte Carlo samples
        
    Returns:
        ELBO value
    """
    samples = q.sample(n_samples)
    
    # E_q[log p(x|z)]
    exp_likelihood = sum(log_likelihood(s) for s in samples) / len(samples)
    
    # E_q[log p(z)] - E_q[log q(z)]
    exp_prior = sum(log_prior(s) for s in samples) / len(samples)
    
    # KL term (approximation for mean-field Gaussian)
    kl = 0.0
    for p in q.variational_params:
        kl += -0.5 * (1 + p.get('log_var', 0) - p['mean']**2 - math.exp(p.get('log_var', 0)))
    
    return exp_likelihood - kl


def mean_field_update(
    log_likelihood: Callable[[List[float]], float],
    log_prior: Callable[[List[float]], float],
    q: MeanFieldVI,
    idx: int,
    n_samples: int = 50
) -> dict:
    """Update one variational parameter using coordinate ascent.
    
    Args:
        log_likelihood: Log likelihood function
        log_prior: Log prior function
        q: Variational distribution
        idx: Index of parameter to update
        n_samples: Number of samples
        
    Returns:
        Updated variational parameters for idx
    """
    # Sample from current q
    current_means = q.get_means()
    
    # Simple update: set mean to the mode of the conditional
    # This is a simplified version - real VI would use more sophisticated updates
    samples = q.sample(n_samples)
    
    # Compute gradient approximation
    grad_sum = 0.0
    for s in samples:
        # Approximate gradient using likelihood
        eps = 0.01
        s_plus = s[:]
        s_plus[idx] += eps
        s_minus = s[:]
        s_minus[idx] -= eps
        
        # Simple finite difference
        grad = (log_likelihood(s_plus) - log_likelihood(s_minus)) / (2 * eps)
        grad_sum += grad
    
    avg_grad = grad_sum / n_samples
    
    # Update mean
    new_mean = q.variational_params[idx]['mean'] + 0.01 * avg_grad
    
    return {'mean': new_mean, 'log_var': q.variational_params[idx].get('log_var', 0)}


def coordinate_ascent_vi(
    log_likelihood: Callable[[List[float]], float],
    log_prior: Callable[[List[float]], float],
    n_params: int,
    n_iter: int = 100,
    tol: float = 1e-4
) -> MeanFieldVI:
    """Run coordinate ascent VI to maximize ELBO.
    
    Args:
        log_likelihood: Log likelihood function
        log_prior: Log prior function
        n_params: Number of latent variables
        n_iter: Maximum iterations
        tol: Convergence tolerance
        
    Returns:
        Optimized variational distribution
    """
    q = MeanFieldVI(n_params)
    
    prev_elbo = float('-inf')
    
    for iteration in range(n_iter):
        # Update each parameter
        for idx in range(n_params):
            new_params = mean_field_update(log_likelihood, log_prior, q, idx)
            q.variational_params[idx] = new_params
        
        # Check convergence
        current_elbo = ELBO(log_likelihood, log_prior, q)
        
        if abs(current_elbo - prev_elbo) < tol:
            break
        
        prev_elbo = current_elbo
    
    return q


def variational_linear_regression(
    X: List[List[float]],
    y: List[float],
    n_samples: int = 100
) -> Tuple[List[float], List[float]]:
    """Bayesian linear regression using variational inference.
    
    Args:
        X: Input features
        y: Target values
        n_samples: Number of posterior samples
        
    Returns:
        (posterior_means, posterior_stds)
    """
    n = len(X)
    if n == 0:
        return [], []
    
    m = len(X[0])
    
    # Log likelihood: log p(y|X,w) = -0.5 * sum((y - Xw)^2)
    def log_likelihood(w):
        pred = [sum(w[j] * X[i][j] for j in range(m)) for i in range(n)]
        return -0.5 * sum((y[i] - pred[i])**2 for i in range(n))
    
    # Log prior: standard normal prior on weights
    def log_prior(w):
        return -0.5 * sum(wi**2 for wi in w)
    
    # Run VI
    q = coordinate_ascent_vi(log_likelihood, log_prior, m)
    
    # Get posterior statistics
    samples = q.sample(n_samples)
    
    posterior_means = q.get_means()
    posterior_stds = [0.1] * m  # Simplified - use sample std
    
    return posterior_means, posterior_stds