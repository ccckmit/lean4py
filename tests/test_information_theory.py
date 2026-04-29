import pytest
import math
from lean4py.information_theory import entropy, mutual_information, kl_divergence


class TestEntropy:
    def test_entropy_uniform(self):
        """Uniform distribution: H = log2(n)."""
        p = [0.25, 0.25, 0.25, 0.25]
        assert abs(entropy(p) - 2.0) < 1e-10

    def test_entropy_certain(self):
        """Certain event: H = 0."""
        p = [1.0, 0.0, 0.0]
        assert abs(entropy(p) - 0.0) < 1e-10

    def test_entropy_empty(self):
        assert entropy([]) == 0.0

    def test_entropy_not_normalized(self):
        """Should normalize automatically."""
        p = [1, 1, 1, 1]  # Sum = 4
        assert abs(entropy(p) - 2.0) < 1e-10

    def test_entropy_bernoulli(self):
        """Bernoulli(p): H = -p log p - (1-p) log(1-p)."""
        p = 0.3
        expected = -p * math.log2(p) - (1-p) * math.log2(1-p)
        assert abs(entropy([p, 1-p]) - expected) < 1e-10


class TestMutualInformation:
    def test_mi_independent(self):
        """Independent variables: I(X;Y) = 0."""
        joint = [[0.25, 0.25], [0.25, 0.25]]
        x_marginal = [0.5, 0.5]
        y_marginal = [0.5, 0.5]
        assert abs(mutual_information(joint, x_marginal, y_marginal)) < 1e-10

    def test_mi_dependent(self):
        """Perfect dependence: I(X;Y) = H(X)."""
        joint = [[0.5, 0.0], [0.0, 0.5]]
        x_marginal = [0.5, 0.5]
        y_marginal = [0.5, 0.5]
        mi = mutual_information(joint, x_marginal, y_marginal)
        assert mi > 0.6  # Should be close to 1 bit

    def test_mi_empty(self):
        assert mutual_information([], [], []) == 0.0


class TestKLDivergence:
    def test_kl_identical(self):
        """Same distribution: D_KL(P||P) = 0."""
        p = [0.5, 0.3, 0.2]
        assert abs(kl_divergence(p, p)) < 1e-10

    def test_kl_different(self):
        """Different distributions: D_KL > 0."""
        p = [0.5, 0.5]
        q = [0.7, 0.3]
        kl = kl_divergence(p, q)
        assert kl > 0

    def test_kl_mismatch_length(self):
        with pytest.raises(ValueError):
            kl_divergence([0.5, 0.5], [0.5])

    def test_kl_q_zero(self):
        """If q has zero for non-zero p, KL = inf."""
        p = [1.0, 0.0]
        q = [0.0, 1.0]
        assert kl_divergence(p, q) == float('inf')
