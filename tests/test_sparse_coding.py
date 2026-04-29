"""Tests for Sparse Coding module."""

import sys
sys.path.insert(0, '/Users/Shared/ccc/project/lean4py')

from lean4py.sparse_coding import OMP, sparse_coding, compute_dictionary


class TestOMP:
    """Tests for Orthogonal Matching Pursuit."""
    
    def test_omp_no_nonzero(self):
        """Test OMP with zero non-zero coefficient limit."""
        x = [1.0, 2.0, 3.0]
        dictionary = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
        
        coeffs = OMP(x, dictionary, n_nonzero=0)
        
        assert len(coeffs) == 3
        assert all(c == 0 for c in coeffs)


class TestSparseCoding:
    """Tests for sparse coding / dictionary learning."""
    
    def test_sparse_coding_empty_data(self):
        """Test sparse coding with empty data."""
        dictionary, codes = sparse_coding([], n_atoms=3)
        
        assert dictionary == []
        assert codes == []