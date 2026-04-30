# lean4py AGENTS.md

## Install
```bash
pip install -e ".[dev]"
```
Requires Python >=3.10. Dev dependencies (pytest, build, twine) in `pyproject.toml`.

## Test
```bash
pytest tests/                          # All tests
pytest tests/test_<module>.py -v       # Single module
```

## Key Commands
- Run examples: `python examples/<name>.py` (01_logic through 08_graph_theory)
- Check version: `python -c "import lean4py; print(lean4py.__version__)"`

## Structure
- `lean4py/` - Core modules: logic, sets, algebra, nat, tactics, prover, number_theory, linear_algebra, real_analysis, probability, graph_theory, statistics, optimization, symbolic, pde, time_series, ml_basics, neural_network, bayesian, signal_processing, information_theory, reinforcement_learning, gaussian_process, hmm, kalman_filter, sparse_coding, manifold_learning, gnn, variational_inference, information_retrieval, homological_algebra, sheaf, lie_algebra, representation_theory, stacks, lie_groups, operator_algebras, free_probability, adjunction_representation, derived_categories, free_operator_algebras, kahler_geometry, spectral_sequence, topos, lie_algebra_classification, hopf_algebra, model_category, algebraic_geometry, numerical_methods, graph_algorithms, differential_geometry, two_category, automata_theory
- `tests/` - pytest tests (one-to-one with modules)
- `examples/` - Numbered usage examples
- `_doc/` - Version planning documents (v0.1 - v1.20)

## Critical Implementation Notes

### tableau_prove (prover.py)
1. `¬(A → B)` expands to `[A, ¬B]` on one branch (α-rule), not two
2. Negated literals (e.g., `¬p`) do not expand: `else: pass` in `_expand_branch`
3. `_is_complementary` uses `==` (not `is`) for Prop equality

### Prop Objects
- `Prop('p') == Prop('p')` is True (name-based equality)
- `Prop('p') is Prop('p')` is False (distinct objects)
- Always use `==` for equality checks in prover logic

### Module Organization
- `algebra.py` - Magma through Field (basic); extended to Module, Ideal, Lattice
- `linear_algebra.py` - Vector, Matrix, eigenvalues; also exports `compute_mean_vector`, `compute_covariance_matrix`, `pca`
- `real_analysis.py` - Sequence/Function limit, derivative, integral, ODE solvers

## Version History
- v1.13: Homological algebra, Sheaf theory, Lie algebras, Extended representation theory
- v1.14: (planned - spectral sequences, topos, Dynkin diagrams, Hopf algebras)
- v1.15: Stacks, Lie groups, Operator algebras
- v1.16: Cech cohomology, Compact Lie groups, Adjoint orbits, Free probability
- v1.17: Derived categories, Free operator algebras, Kähler geometry
- v1.18: Spectral sequences, Topos theory, Lie algebra classification, Hopf algebras
- v1.19: Model categories, Algebraic geometry, Numerical methods, Graph algorithms
- v1.20: Differential geometry, 2-categories, Automata theory, Formal languages