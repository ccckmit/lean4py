# lean4py AGENTS.md

## Install
```bash
pip install -e ".[dev]"
```
Requires Python >=3.10. Dev dependencies (pytest, build, twine) defined in `pyproject.toml`.

## Test
```bash
pytest tests/                  # All tests
pytest tests/test_<module>.py -v  # Single module (e.g., test_prover.py)
```

## Key Commands
- Run examples: `python examples/<name>.py` (01_logic, 02_sets, 03_algebra, 04_number_theory, 04_prover, 05_linear_algebra, 06_real_analysis, 07_probability, 08_graph_theory)

## Structure
- `lean4py/` - Package: logic, sets, algebra, nat, tactics, prover, number_theory, linear_algebra, real_analysis, probability, graph_theory
- `tests/` - pytest tests (one-to-one with modules)
- `examples/` - Numbered usage examples

## Critical Implementation Notes
### tableau_prove (prover.py)
1. `¬(A → B)` expands to `[A, ¬B]` on one branch (α-rule), not two
2. Negated literals (e.g., `¬p`) do not expand: `else: pass` in `_expand_branch`
3. `_is_complementary` uses `==` (not `is`) for Prop equality

### Prop Objects
- `Prop('p') == Prop('p')` is True (name-based equality)
- `Prop('p') is Prop('p')` is False (distinct objects)
- Always use `==` for equality checks in prover logic

## Modules
- `lean4py.logic` - Prop, implies, and_, or_, not_, iff, Theorem, prove
- `lean4py.sets` - Set_from, union, intersection, subset, complement, difference, etc.
- `lean4py.algebra` - Magma, Semigroup, Monoid, Group, AbelianGroup, Ring, Field
- `lean4py.nat` - Nat, zero, succ, pred, nat_add, nat_mul, etc.
- `lean4py.tactics` - intros, cases, split, by, sorry, calc, TacticProof, etc.
- `lean4py.prover` - tableau_prove, truth_table_prove, is_valid, is_satisfiable, find_counterexample
- `lean4py.number_theory` - Integer, gcd, lcm, is_prime, phi, mod_exp, bezout_identity, etc.
- `lean4py.linear_algebra` - Vector, Matrix, dot_product, det, rank, eigenvalues, etc.
- `lean4py.real_analysis` - Real, limit, derivative, integral, series_sum, Function, etc.
- `lean4py.probability` - ProbabilitySpace, ExpectedValue, NormalDistribution, bayes_theorem, etc.
- `lean4py.graph_theory` - Graph, bfs, dfs, shortest_path, dijkstra, minimum_spanning_tree, etc.