# lean4py AGENTS.md

## Install
```bash
pip install -e ".[dev]"           # Dev install with pytest, build, twine
pip install -e ".[probability]"    # + numpy, scipy for probability tests
```
Requires Python >=3.10.

## Test
```bash
pytest tests/                          # All tests
pytest tests/test_prover.py -v         # Single module
pytest tests/test_probability.py -v    # Needs [probability] deps
```
Config in `pyproject.toml`: testpaths = `["tests"]`, python_files = `["test_*.py"]`.

Some modules have multiple test files with version suffixes (`_v11`, `_v12`, etc.) and `_extended` variants.

## Structure
- `lean4py/` - 63 modules (logic → automata_theory, noncommutative_geometry, ergodic_theory, etc.)
- `tests/` - 82 test files (not strictly one-to-one; some modules have versioned/extended tests)
- `examples/` - 10 examples (01_logic through 08_graph_theory, plus v1.3_demo.py, 04_prover.py)
- `_doc/` - Version planning (v0.1 - v1.21)

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
- `real_analysis.py` - Sequence/Function limit, derivative, integral, ODE solvers (`euler_method`, `runge_kutta_4`)

## Notes
- No linting/formatting config (no .flake8, setup.cfg, or CI workflows)
- `__init__.py` is massive (1037 lines) - exports from all 63 modules
- Current version: 1.23.0

## Roadmap (mathlib4 alignment)

| Version | Modules | mathlib4 alignment |
|---------|----------|-------------------|
| v1.22 (next) | `noncommutative_geometry`, `ergodic_theory`, `higher_category_theory`, `k_theory` | Spectral triples, Ergodic theorems, ∞-categories, K-groups |
| v1.23 (planned) | `topology`, `measure_theory`, `functional_analysis`, `combinatorics` | Topological spaces, Lebesgue integral, Banach/Hilbert spaces, Pigeonhole/Catalan |

### Priority gaps vs mathlib4
- **Topology**: General topology, metric spaces, uniform spaces (mathlib4 `Mathlib.Topology`)
- **Measure Theory**: σ-algebras, Lebesgue measure, integration (mathlib4 `Mathlib.MeasureTheory`)
- **Functional Analysis**: Normed/Banach/Hilbert spaces, operators (mathlib4 `Mathlib.Analysis`)
- **Combinatorics**: Enumerative, set families, extremal (mathlib4 `Mathlib.Combinatorics`)

See `_doc/v1.22.md` and `_doc/v1.23.md` for detailed plans.