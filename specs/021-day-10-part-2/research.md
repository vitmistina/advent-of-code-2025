# Research: Day 10 Part 2 - Integer Linear Programming Approach

**Date**: 2025-12-12  
**Feature**: Joltage Configuration Optimization  
**Purpose**: Resolve technical unknowns and select optimal algorithms

---

## Problem Formulation

### Mathematical Model

**Given:**

- Matrix B (n×m): Each column represents a button, each row a counter
- Target vector t (n×1): Desired joltage levels for each counter
- Constraint: B·x = t, where x ≥ 0 and x ∈ ℤᵐ

**Objective:** Minimize ||x||₁ = sum(x) (total button presses)

**Example:**

```
Buttons: (3), (1,3), (2), (2,3), (0,2), (0,1)
Targets: {3, 5, 4, 7}

Matrix B (4 counters × 6 buttons):
     B0  B1  B2  B3  B4  B5
C0: [ 0   0   0   0   1   1 ]
C1: [ 0   1   0   0   0   1 ]
C2: [ 0   0   1   1   1   0 ]
C3: [ 1   1   0   1   0   0 ]

Target t: [3, 5, 4, 7]ᵀ
```

### Relationship to Part 1

**Part 1 (Indicator Lights):**

- System: B·x = t (mod 2) over GF(2)
- Operations: XOR (toggle)
- Solution: Gaussian elimination over binary field

**Part 2 (Joltage Counters):**

- System: B·x = t over non-negative integers
- Operations: Addition (increment)
- Solution: Integer linear programming with L1 minimization

**Key insight**: Same matrix B, different algebraic structure

---

## Technology Selection

### Decision: NumPy-Based Gaussian Elimination with Integer Enumeration

**Rationale:**

1. **No Additional Dependencies**: Leverages existing NumPy (already used in Part 1)
2. **Problem Scale**: Small systems (m ≤ 20 buttons, n ≤ 20 counters) suit direct methods
3. **Code Reuse**: Adapts Part 1's Gaussian elimination structure to integer arithmetic
4. **Performance**: Expected <0.1s per machine for k ≤ 10 free variables (enumeration: O(2^k · n · m))
5. **Optimality Guarantee**: Exhaustive search over solution space ensures global minimum

**Implementation Strategy:**

```python
def solve_integer_linear_system(B: np.ndarray, t: np.ndarray) -> Optional[np.ndarray]:
    """
    Solve B·x = t for non-negative integer x minimizing sum(x).

    Algorithm:
    1. Row-reduce augmented matrix [B | t] to identify pivot/free variables
    2. Check feasibility (no contradictions like 0 = c where c ≠ 0)
    3. Enumerate free variable assignments in feasible ranges
    4. For each assignment, back-substitute to solve for pivot variables
    5. Validate non-negativity and exact match, track minimum L1 norm
    6. Return optimal solution vector x
    """
    # Step 1: Gaussian elimination with integer arithmetic
    # Step 2: Identify free variables (columns without pivots)
    # Step 3: Enumerate free variable values (start with small bounds)
    # Step 4: Back-substitute and validate
    # Step 5: Return best solution
```

**Complexity:**

- Row reduction: O(n² · m)
- Enumeration: O(2^k) where k = m - rank(B)
- Per enumeration: O(n · m) for validation
- **Total**: O(n² · m + 2^k · n · m) ≈ O(2^k · n · m) for k < 15

### Alternatives Considered

#### Alternative 1: SciPy `linprog` with `integrality` Constraints

**Pros:**

- Built into SciPy (no extra dependencies)
- Uses HiGHS MILP solver (production-grade)
- Handles edge cases robustly

**Cons:**

- Designed for large-scale problems (overkill for m ≤ 20)
- Potential convergence issues with exact equality constraints
- Less educational (black-box solver)

**When to use:** If problem scales beyond m > 30 or enumeration becomes infeasible

#### Alternative 2: Dedicated MILP Solvers (PuLP, CVXPY)

**Pros:**

- Mature solvers (CBC, GLPK, Gurobi)
- Handle complex constraints and large problems
- Standard tooling for optimization

**Cons:**

- **Requires additional dependencies** (CBC solver ~10MB)
- Constitution Principle IX prefers minimal dependencies for AoC
- Over-engineering for current scale

**When to use:** If problem complexity increases significantly in future parts

#### Alternative 3: LP Relaxation + Rounding Heuristic

**Pros:**

- Fast (LP solvable in polynomial time)
- Provides lower bound on optimal solution

**Cons:**

- No optimality guarantee (rounding may miss true minimum)
- Requires validation and potentially local search
- AoC expects exact answers

**When to use:** As a preprocessing step to bound enumeration ranges

---

## Best Practices

### Integer Arithmetic Handling

**Challenge**: Gaussian elimination traditionally uses floating-point division, but we need exact integer solutions.

**Solution Patterns:**

1. **Fraction-Based Elimination**: Use Python's `fractions.Fraction` during row reduction to maintain exact rational arithmetic, then verify integer solutions exist.

2. **GCD-Based Elimination**: Use integer linear combinations with gcd calculations to eliminate without introducing fractions.

3. **Hybrid Approach**: Use floating-point LP relaxation to bound search space, then enumerate integers.

**Recommended**: Fractions module for exact arithmetic during elimination, then enumerate integer solutions.

```python
from fractions import Fraction
import numpy as np

def gaussian_elimination_rational(B, t):
    """Row-reduce over rationals to avoid floating-point errors."""
    n, m = B.shape
    aug = np.array([[Fraction(B[i, j]) for j in range(m)] + [Fraction(t[i])]
                    for i in range(n)])
    # Perform row reduction...
    return aug
```

### Free Variable Enumeration Strategy

**Challenge**: For k free variables, naively trying all combinations in {0, ..., max(t)} yields max(t)^k possibilities (infeasible for k > 5).

**Smart Bounds:**

1. **LP Relaxation Upper Bound**: Solve continuous relaxation, use ceiling(x_lp[i]) as upper bound for x[i]
2. **Component-wise Bound**: For button i affecting counters C, upper bound is max(t[c] for c in C)
3. **Progressive Search**: Start with small bounds (0-10), expand if no solution found

```python
def get_enumeration_bounds(B, t, x_lp):
    """Determine smart bounds for free variable enumeration."""
    m = B.shape[1]
    bounds = []
    for i in range(m):
        # Use LP relaxation ceiling + small buffer
        upper = int(np.ceil(x_lp[i])) + 2
        # But cap at reasonable max (sum of targets is absolute upper bound)
        upper = min(upper, sum(t))
        bounds.append((0, upper))
    return bounds
```

### Edge Case Handling

**Infeasible Systems:**

- Detection: After row reduction, check for contradictory rows (0 = c where c ≠ 0)
- Response: Return None or raise InfeasibleError

**Zero Targets:**

- All counters already at target → x = [0, 0, ..., 0] (minimum is 0 presses)

**Underdetermined Systems (k > 0 free variables):**

- Standard case → enumerate free variable space

**Overdetermined Systems (more equations than variables):**

- May be infeasible or have unique solution → row reduction reveals this

---

## Performance Optimization

### Expected Complexity Analysis

**Typical AoC Input Characteristics:**

- Number of machines: 3-100
- Buttons per machine: 4-10
- Counters per machine: 4-10
- Rank deficiency: k = 2-5 (few free variables)

**Performance Estimates:**

| Free Variables (k) | Enumeration Space | Time per Machine |
| ------------------ | ----------------- | ---------------- |
| k ≤ 5              | ≤ 10^5            | <0.01s           |
| k = 8              | ≈ 10^8            | ~1s              |
| k = 10             | ≈ 10^10           | ~100s (too slow) |

**Mitigation for k > 8:**

- Use LP relaxation to narrow search space
- Implement branch-and-bound pruning
- Fall back to SciPy `linprog` with `integrality`

### Caching and Memoization

**Opportunity**: If multiple machines share identical button structures (same B matrix), memoize solutions.

**Implementation**:

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def solve_cached(B_tuple, t_tuple):
    """Cache solutions for identical machine structures."""
    B = np.array(B_tuple)
    t = np.array(t_tuple)
    return solve_integer_linear_system(B, t)
```

---

## Integration with Part 1

### Code Reuse Opportunities

**Shared Components:**

- `parse_input()` and `parse_line()` — already extract jolts
- Matrix construction logic — build B from button definitions
- Test infrastructure — extend existing test framework

**Separate Components:**

- Solver algorithm (GF(2) vs integer LP)
- Solution validation (mod 2 vs exact integer)

**Recommended Structure:**

```
day-10/
├── solution.py          # Part 1 (existing)
├── solution_part2.py    # Part 2 (new)
├── parser.py            # Shared parsing logic (extract if needed)
├── test_solution.py     # Part 1 tests
└── test_solution_part2.py  # Part 2 tests
```

### Data Flow

```
Input File → parse_input() → List[Machine]
              ↓
Machine → build_button_matrix() → (B, t)
              ↓
(B, t) → solve_integer_linear_system() → x (button presses)
              ↓
x → sum(x) → minimum presses for machine
              ↓
Aggregate → total minimum presses across all machines
```

---

## Risk Assessment

### High-Confidence Areas

✅ Parsing: Reuses proven Part 1 parser  
✅ Matrix construction: Direct translation from button definitions  
✅ Small-scale testing: Three examples with known answers

### Medium-Risk Areas

⚠️ **Free variable enumeration bounds**: May need tuning for edge cases  
⚠️ **Integer arithmetic precision**: Use `int64` or `Fraction` to avoid overflow  
⚠️ **Performance for k > 10**: May require optimization or fallback solver

### Mitigation Strategies

1. **Implement LP relaxation bounds** before full enumeration
2. **Add performance monitoring** to detect slow cases early
3. **Prepare SciPy fallback** for machines with k > 10
4. **Extensive testing** with synthetic high-k cases

---

## Summary

**Chosen Approach**: NumPy-based Gaussian elimination with bounded free variable enumeration

**Key Decisions**:

1. No additional dependencies (use NumPy only)
2. Exact integer arithmetic via `fractions` module during elimination
3. Smart enumeration bounds from LP relaxation
4. Fallback to SciPy for edge cases (optional)

**Expected Outcomes**:

- Correct results on all three examples (10, 12, 11 → total 33)
- Performance: <1s per machine for typical inputs
- Maintainable code reusing Part 1 structure

**Next Steps**: Proceed to Phase 1 (Data Model & Contracts)
