# Quickstart Guide: Day 10 Part 2 Implementation

**Feature**: Joltage Configuration Optimization  
**Date**: 2025-12-12  
**For**: Developers implementing the solution

---

## Overview

This guide walks through implementing Day 10 Part 2, which extends Part 1's binary toggle system to integer-valued counters with increment operations. The core algorithm uses Gaussian elimination with free variable enumeration to find minimal button press solutions.

---

## Prerequisites

**Existing Code** (from Part 1):

- ✅ `day-10/solution.py` — contains `parse_input()`, `parse_line()`
- ✅ `day-10/test_input.txt` — test data with 3 machines
- ✅ `day-10/input.txt` — actual puzzle input

**Dependencies** (already installed):

- NumPy for matrix operations
- Pytest for testing

**New Files to Create**:

- `day-10/solution_part2.py` — Part 2 solver implementation
- `day-10/test_solution_part2.py` — Part 2 tests (TDD: write first!)

---

## Phase 1: Write Failing Tests (RED)

### Step 1.1: Create Test File

Create `day-10/test_solution_part2.py`:

```python
"""Tests for Day 10 Part 2: Joltage Configuration."""

import pytest
import numpy as np
from pathlib import Path
from solution_part2 import (
    solve_part2,
    build_button_matrix,
    solve_integer_linear_system,
    verify_solution,
)
from solution import parse_input  # Reuse from Part 1


def test_example_1_machine():
    """Test first example machine: expected minimum presses = 10."""
    # Machine: [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
    buttons = [[3], [1, 3], [2], [2, 3], [0, 2], [0, 1]]
    targets = [3, 5, 4, 7]

    B = build_button_matrix(buttons, len(targets))
    t = np.array(targets)

    x = solve_integer_linear_system(B, t)

    assert x is not None, "System should be feasible"
    assert verify_solution(B, t, x), "Solution must satisfy B·x = t"
    assert np.all(x >= 0), "All button presses must be non-negative"
    assert np.sum(x) == 10, f"Expected 10 presses, got {np.sum(x)}"


def test_example_2_machine():
    """Test second example machine: expected minimum presses = 12."""
    buttons = [[0, 2, 3, 4], [2, 3], [0, 4], [0, 1, 2], [1, 2, 3, 4]]
    targets = [7, 5, 12, 7, 2]

    B = build_button_matrix(buttons, len(targets))
    t = np.array(targets)

    x = solve_integer_linear_system(B, t)

    assert x is not None, "System should be feasible"
    assert verify_solution(B, t, x), "Solution must satisfy B·x = t"
    assert np.sum(x) == 12, f"Expected 12 presses, got {np.sum(x)}"


def test_example_3_machine():
    """Test third example machine: expected minimum presses = 11."""
    buttons = [[0, 1, 2, 3, 4], [0, 3, 4], [0, 1, 2, 4, 5], [1, 2]]
    targets = [10, 11, 11, 5, 10, 5]

    B = build_button_matrix(buttons, len(targets))
    t = np.array(targets)

    x = solve_integer_linear_system(B, t)

    assert x is not None, "System should be feasible"
    assert verify_solution(B, t, x), "Solution must satisfy B·x = t"
    assert np.sum(x) == 11, f"Expected 11 presses, got {np.sum(x)}"


def test_all_examples_aggregate():
    """Test aggregation across all three example machines: total = 33."""
    test_input = Path(__file__).parent / "test_input.txt"
    machines = parse_input(test_input.read_text())

    total = solve_part2(machines)

    assert total == 33, f"Expected total 33 presses, got {total}"


def test_build_button_matrix_structure():
    """Verify button matrix construction is correct."""
    buttons = [[3], [1, 3], [2], [2, 3], [0, 2], [0, 1]]
    num_counters = 4

    B = build_button_matrix(buttons, num_counters)

    # Expected matrix:
    #      B0  B1  B2  B3  B4  B5
    # C0: [ 0   0   0   0   1   1 ]
    # C1: [ 0   1   0   0   0   1 ]
    # C2: [ 0   0   1   1   1   0 ]
    # C3: [ 1   1   0   1   0   0 ]

    expected = np.array([
        [0, 0, 0, 0, 1, 1],
        [0, 1, 0, 0, 0, 1],
        [0, 0, 1, 1, 1, 0],
        [1, 1, 0, 1, 0, 0]
    ])

    assert np.array_equal(B, expected), "Button matrix structure incorrect"


def test_verify_solution_accepts_valid():
    """Test that verify_solution accepts a valid solution."""
    B = np.array([[1, 2], [1, 1]])
    t = np.array([5, 3])
    x = np.array([1, 2])  # 1×1 + 2×2 = 5, 1×1 + 1×2 = 3

    assert verify_solution(B, t, x), "Valid solution rejected"


def test_verify_solution_rejects_invalid():
    """Test that verify_solution rejects invalid solutions."""
    B = np.array([[1, 2], [1, 1]])
    t = np.array([5, 3])
    x = np.array([0, 2])  # 0×1 + 2×2 = 4 ≠ 5

    assert not verify_solution(B, t, x), "Invalid solution accepted"


def test_zero_target_case():
    """Test edge case where all targets are zero (optimal: 0 presses)."""
    buttons = [[0], [1], [0, 1]]
    targets = [0, 0]

    B = build_button_matrix(buttons, len(targets))
    t = np.array(targets)

    x = solve_integer_linear_system(B, t)

    assert x is not None, "Zero target should be feasible"
    assert np.sum(x) == 0, "Zero target requires 0 presses"
```

### Step 1.2: Run Tests to Verify Failures

```bash
uv run pytest day-10/test_solution_part2.py -v
```

**Expected**: All tests FAIL with import errors or NotImplementedError. This confirms tests are written correctly (RED phase).

---

## Phase 2: Implement Core Functions (GREEN)

### Step 2.1: Create `solution_part2.py` Skeleton

Create `day-10/solution_part2.py`:

```python
"""Advent of Code 2025 - Day 10 Part 2: Joltage Configuration."""

from pathlib import Path
from typing import List, Optional, Tuple
import numpy as np
from fractions import Fraction
from solution import parse_input, Machine  # Reuse from Part 1


def build_button_matrix(buttons: List[List[int]], num_counters: int) -> np.ndarray:
    """
    Construct button matrix B where B[i,j] = 1 if button j affects counter i.

    Args:
        buttons: List of button definitions (each is list of counter indices)
        num_counters: Total number of counters

    Returns:
        Matrix B of shape (num_counters, num_buttons)
    """
    num_buttons = len(buttons)
    B = np.zeros((num_counters, num_buttons), dtype=int)

    for j, button in enumerate(buttons):
        for counter_idx in button:
            if counter_idx >= num_counters:
                raise IndexError(f"Button affects counter {counter_idx} but only {num_counters} exist")
            B[counter_idx, j] = 1

    return B


def verify_solution(B: np.ndarray, t: np.ndarray, x: np.ndarray) -> bool:
    """
    Verify that solution x satisfies B·x = t and x ≥ 0.

    Args:
        B: Button matrix
        t: Target vector
        x: Candidate solution

    Returns:
        True if x is a valid solution, False otherwise
    """
    if x is None:
        return False

    # Check exact equality B·x = t
    if not np.array_equal(B @ x, t):
        return False

    # Check non-negativity
    if not np.all(x >= 0):
        return False

    # Check integer values
    if not np.allclose(x, x.astype(int)):
        return False

    return True


def gaussian_elimination_integer(
    B: np.ndarray,
    t: np.ndarray
) -> Tuple[np.ndarray, List[int], List[int]]:
    """
    Perform Gaussian elimination over rationals to identify pivot/free variables.

    Args:
        B: Button matrix (n_counters × n_buttons)
        t: Target vector (n_counters,)

    Returns:
        Tuple of (augmented_matrix_rref, pivot_columns, free_columns)
    """
    n, m = B.shape

    # Build augmented matrix [B | t] using Fractions for exact arithmetic
    aug = [[Fraction(B[i, j]) for j in range(m)] + [Fraction(t[i])] for i in range(n)]

    pivot_cols = []
    current_row = 0

    for col in range(m):
        # Find pivot in current column
        pivot_row = None
        for r in range(current_row, n):
            if aug[r][col] != 0:
                pivot_row = r
                break

        if pivot_row is None:
            continue  # No pivot in this column -> free variable

        # Swap rows if needed
        if pivot_row != current_row:
            aug[current_row], aug[pivot_row] = aug[pivot_row], aug[current_row]

        # Scale pivot row to make pivot = 1
        pivot_val = aug[current_row][col]
        aug[current_row] = [val / pivot_val for val in aug[current_row]]

        # Eliminate below pivot
        for r in range(current_row + 1, n):
            if aug[r][col] != 0:
                factor = aug[r][col]
                aug[r] = [aug[r][j] - factor * aug[current_row][j] for j in range(m + 1)]

        pivot_cols.append(col)
        current_row += 1

    # Check feasibility
    for r in range(n):
        if all(aug[r][j] == 0 for j in range(m)) and aug[r][m] != 0:
            return None, [], []  # Infeasible: 0 = c where c ≠ 0

    # Identify free variables
    free_cols = [c for c in range(m) if c not in pivot_cols]

    # Convert back to numpy (keeping Fraction precision for now)
    return np.array(aug, dtype=object), pivot_cols, free_cols


def solve_integer_linear_system(B: np.ndarray, t: np.ndarray) -> Optional[np.ndarray]:
    """
    Solve B·x = t for non-negative integer x minimizing ||x||_1.

    Args:
        B: Button matrix (n_counters × n_buttons)
        t: Target vector (n_counters,)

    Returns:
        Optimal solution vector x, or None if infeasible
    """
    n, m = B.shape

    # Step 1: Gaussian elimination to identify structure
    aug, pivot_cols, free_cols = gaussian_elimination_integer(B, t)

    if aug is None:
        return None  # Infeasible system

    k = len(free_cols)

    # Step 2: Determine enumeration bounds for free variables
    # Simple strategy: try values from 0 to sum(t) for each free variable
    # TODO: Optimize with LP relaxation bounds
    max_val = min(sum(t), 20)  # Cap at reasonable max

    # Step 3: Enumerate free variable combinations
    best_x = None
    best_cost = float('inf')

    from itertools import product

    for free_vals in product(range(max_val + 1), repeat=k):
        x = np.zeros(m, dtype=int)

        # Assign free variables
        for i, col in enumerate(free_cols):
            x[col] = free_vals[i]

        # Back-substitute for pivot variables
        # Start from last pivot and work backwards
        for i in reversed(range(len(pivot_cols))):
            pivot_col = pivot_cols[i]

            # Find row containing this pivot
            row = i

            # Solve for x[pivot_col]: x[pivot_col] = aug[row, m] - sum(aug[row, j] * x[j] for j != pivot_col)
            rhs = float(aug[row, m])
            for j in range(m):
                if j != pivot_col:
                    rhs -= float(aug[row, j]) * x[j]

            # Check if result is non-negative integer
            if rhs < 0 or not np.isclose(rhs, round(rhs)):
                break  # Invalid solution

            x[pivot_col] = round(rhs)
        else:
            # Verify solution
            if verify_solution(B, t, x):
                cost = np.sum(x)
                if cost < best_cost:
                    best_cost = cost
                    best_x = x.copy()

    return best_x


def solve_part2(machines: List[Machine]) -> int:
    """
    Solve Part 2: find minimum button presses across all machines.

    Args:
        machines: List of parsed machine definitions

    Returns:
        Total minimum button presses across all machines
    """
    total = 0

    for machine in machines:
        buttons = machine['buttons']
        targets = machine['jolts']

        if not targets:
            continue  # Skip machines without joltage requirements

        B = build_button_matrix(buttons, len(targets))
        t = np.array(targets)

        x = solve_integer_linear_system(B, t)

        if x is None:
            print(f"Warning: Machine is infeasible, skipping")
            continue

        total += int(np.sum(x))

    return total


def main():
    """Main entry point for Part 2."""
    input_path = Path(__file__).parent / "input.txt"
    machines = parse_input(input_path.read_text())

    result = solve_part2(machines)
    print(f"Part 2 Result: {result}")


if __name__ == "__main__":
    main()
```

### Step 2.2: Run Tests Again

```bash
uv run pytest day-10/test_solution_part2.py -v
```

**Expected**: Tests should now PASS (GREEN phase). If any fail, debug and fix implementation.

---

## Phase 3: Optimize and Refactor

### Step 3.1: Add LP Relaxation Bounds (Optional Optimization)

If enumeration is slow (k > 10), add bounds optimization:

```python
from scipy.optimize import linprog

def compute_lp_relaxation_bounds(B: np.ndarray, t: np.ndarray, free_cols: List[int]) -> List[int]:
    """
    Compute upper bounds for free variables using LP relaxation.

    Args:
        B: Button matrix
        t: Target vector
        free_cols: Indices of free variables

    Returns:
        List of upper bounds for each free variable
    """
    m = B.shape[1]
    c = np.ones(m)  # Minimize sum(x)

    res = linprog(c, A_eq=B, b_eq=t, bounds=(0, None), method='highs')

    if not res.success:
        # LP infeasible, use default bounds
        return [sum(t)] * len(free_cols)

    bounds = []
    for col in free_cols:
        # Use ceiling + buffer
        upper = int(np.ceil(res.x[col])) + 2
        bounds.append(min(upper, sum(t)))

    return bounds
```

Then modify enumeration to use these bounds instead of fixed `max_val`.

### Step 3.2: Add Performance Monitoring

```python
import time

def solve_integer_linear_system(B: np.ndarray, t: np.ndarray, verbose: bool = False) -> Optional[np.ndarray]:
    start = time.time()

    # ... existing code ...

    if verbose:
        elapsed = time.time() - start
        print(f"Solved in {elapsed:.3f}s with {k} free variables ({len(list(product(range(max_val + 1), repeat=k)))} combinations)")

    return best_x
```

### Step 3.3: Run Full Test Suite

```bash
uv run pytest day-10/ -v
```

Ensure both Part 1 and Part 2 tests pass.

---

## Phase 4: Solve Actual Puzzle

### Step 4.1: Run Against Actual Input

```bash
uv run python day-10/solution_part2.py
```

**Expected Output**:

```
Part 2 Result: [ANSWER]
```

### Step 4.2: Submit Answer

1. Go to Advent of Code Day 10 page
2. Enter the result in Part 2 answer field
3. Submit manually (no auto-submission per Constitution)

### Step 4.3: Update Progress

If correct, update `README.md`:

```markdown
## Progress

| Day | Part 1 | Part 2 | Notes                                       |
| --- | ------ | ------ | ------------------------------------------- |
| 10  | ⭐     | ⭐     | Integer linear programming with enumeration |
```

---

## Troubleshooting

### Issue: Tests Timeout on Example 3

**Symptom**: `test_example_3_machine` runs for >30 seconds

**Cause**: Too many free variables (k > 12), enumeration space too large

**Solution**:

1. Add LP relaxation bounds (Step 3.1)
2. Reduce max_val cap in enumeration
3. Consider falling back to SciPy `linprog` with `integrality` constraints

### Issue: Solution Verification Fails

**Symptom**: `verify_solution(B, t, x)` returns False despite x being optimal

**Cause**: Integer overflow or floating-point precision errors

**Solution**:

- Use `dtype=int64` instead of `int32`
- Verify no intermediate calculations exceed int64 range
- Check that `np.array_equal` is used (not `np.allclose`)

### Issue: Infeasible System Warning

**Symptom**: "Machine is infeasible" printed during execution

**Cause**: System B·x = t has no non-negative integer solution (rare with valid AoC inputs)

**Solution**:

- Verify parsing is correct (buttons and targets match expected)
- Check for contradictory rows in augmented matrix
- Log the machine definition for manual inspection

---

## Next Steps

1. ✅ **Write tests first** (test_solution_part2.py)
2. ✅ **Implement core functions** (solution_part2.py)
3. ✅ **Run tests to verify GREEN**
4. ⚠️ **Optimize if needed** (LP bounds, performance monitoring)
5. ⚠️ **Solve actual puzzle**
6. ⚠️ **Submit answer manually**
7. ⚠️ **Update progress tracker**

**Estimated Time**: 2-3 hours for full implementation and testing

---

## Summary

This implementation extends Day 10 Part 1 by:

- Reusing parsing logic from Part 1
- Building button matrix B from button definitions
- Solving integer LP problem B·x = t with L1 minimization
- Using Gaussian elimination + free variable enumeration
- Validating against three known examples (10, 12, 11 → 33 total)

The TDD workflow ensures correctness through test-first development, and the modular design allows for optimization if performance becomes an issue.
