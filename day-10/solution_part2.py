"""Advent of Code 2025 - Day 10 Part 2: Joltage Configuration.

Solves the joltage counter optimization problem using integer linear programming.
Given a button matrix B and target joltage vector t, finds non-negative integer
solution x that minimizes ||x||_1 (total button presses) subject to B·x = t.

Approach:
- Gaussian elimination over rationals to identify pivot/free variables
- Enumerate free variable assignments within smart bounds
- Back-substitute to solve for pivot variables
- Verify constraints and track minimum L1 norm solution

Complexity: O(2^k · n · m) where k = free variables, n = counters, m = buttons
Expected performance: <0.1s per machine for k ≤ 10
"""

from fractions import Fraction
from pathlib import Path

import numpy as np
from solution import Machine, parse_input


def build_button_matrix(buttons: list[list[int]], num_counters: int) -> np.ndarray:
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
                raise IndexError(
                    f"Button affects counter {counter_idx} but only {num_counters} exist"
                )
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
    B: np.ndarray, t: np.ndarray
) -> tuple[np.ndarray | None, list[int], list[int]]:
    """
    Perform Gaussian elimination over rationals to identify pivot/free variables.

    Args:
        B: Button matrix (n_counters × n_buttons)
        t: Target vector (n_counters,)

    Returns:
        Tuple of (augmented_matrix_rref, pivot_columns, free_columns)
        Returns (None, [], []) if system is infeasible
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


def solve_integer_linear_system(
    B: np.ndarray, t: np.ndarray, verbose: bool = False
) -> np.ndarray | None:
    """
    Solve B·x = t for non-negative integer x minimizing ||x||_1.

    Args:
        B: Button matrix (n_counters × n_buttons)
        t: Target vector (n_counters,)
        verbose: If True, print detailed diagnostic information

    Returns:
        Optimal solution vector x, or None if infeasible
    """
    n, m = B.shape

    if verbose:
        print(f"\n{'=' * 60}")
        print(f"Solving system: {n} counters, {m} buttons")
        print(f"Target vector: {t}")
        print(f"Button matrix B:\n{B}")

    # Step 1: Gaussian elimination to identify structure
    aug, pivot_cols, free_cols = gaussian_elimination_integer(B, t)

    if aug is None:
        if verbose:
            print("❌ INFEASIBLE: System has contradictory constraints (0 = c where c ≠ 0)")
        return None  # Infeasible system

    k = len(free_cols)

    if verbose:
        print(f"✓ System is feasible")
        print(f"Pivot columns (basic variables): {pivot_cols}")
        print(f"Free columns (free variables): {free_cols}")
        print(f"Number of free variables: {k}")
        print(f"Rank of matrix: {len(pivot_cols)}")

    # Step 2: Use LP relaxation to get smart bounds for free variables
    from scipy.optimize import linprog

    # Solve LP relaxation: minimize sum(x) subject to B·x = t, x ≥ 0
    c = np.ones(m)  # Minimize sum of all variables
    result = linprog(c, A_eq=B, b_eq=t, bounds=(0, None), method="highs")

    if result.success:
        # Use LP solution to bound free variables with generous buffer
        lp_solution = result.x
        max_bounds = []
        for col in free_cols:
            # For each free variable, use ceiling of LP value + 50% buffer, capped at max target
            lp_upper = int(np.ceil(lp_solution[col] * 1.5))
            max_bounds.append(min(lp_upper + 10, max(t)))

        if verbose:
            print(f"LP relaxation solution: {lp_solution}")
            print(f"LP optimal cost: {result.fun}")
            print(f"Smart bounds for free variables: {max_bounds}")
    else:
        # Fallback to simple bounds if LP fails
        max_bounds = [min(sum(t), 500) for _ in free_cols]
        if verbose:
            print(f"LP relaxation failed, using fallback bounds: {max_bounds}")

    # Calculate search space size
    search_space = 1
    for bound in max_bounds:
        search_space *= bound + 1

    if verbose:
        print(f"Search space size: {search_space} combinations")

    # Step 3: Enumerate free variable combinations using smart bounds
    best_x = None
    best_cost = float("inf")
    valid_solutions = 0
    invalid_solutions = 0

    from itertools import product

    # Create enumeration ranges based on smart bounds
    enum_ranges = [range(bound + 1) for bound in max_bounds]

    for free_vals in product(*enum_ranges):
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
                invalid_solutions += 1
                break  # Invalid solution

            x[pivot_col] = round(rhs)
        else:
            # Verify solution
            if verify_solution(B, t, x):
                valid_solutions += 1
                cost = np.sum(x)
                if cost < best_cost:
                    best_cost = cost
                    best_x = x.copy()
            else:
                invalid_solutions += 1

    if verbose:
        print(f"\nSearch complete:")
        print(f"  Valid solutions found: {valid_solutions}")
        print(f"  Invalid attempts: {invalid_solutions}")
        if best_x is not None:
            print(f"  ✓ Optimal solution: {best_x}")
            print(f"  ✓ Total button presses: {best_cost}")
            print(f"  ✓ Verification: B·x = {B @ best_x}, target = {t}")
        else:
            print(f"  ❌ NO VALID SOLUTION FOUND")

    return best_x


def solve_part2(machines: list[Machine], verbose: bool = False) -> int:
    """
    Solve Part 2: find minimum button presses across all machines.

    Args:
        machines: List of parsed machine definitions
        verbose: If True, print detailed diagnostic information

    Returns:
        Total minimum button presses across all machines
    """
    total = 0
    total = 0
    infeasible_count = 0

    for idx, machine in enumerate(machines, 1):
        buttons = machine["buttons"]
        targets = machine["jolts"]

        if not targets:
            continue  # Skip machines without joltage requirements

        B = build_button_matrix(buttons, len(targets))
        t = np.array(targets)

        x = solve_integer_linear_system(B, t, verbose=False)

        if x is None:
            infeasible_count += 1
            # Print detailed diagnostics for infeasible machines
            print(f"\n{'#' * 60}")
            print(f"⚠️  Machine {idx}/{len(machines)}: INFEASIBLE")
            print(f"Buttons: {buttons}")
            print(f"Targets: {targets}")
            solve_integer_linear_system(B, t, verbose=True)
            continue

        machine_total = int(np.sum(x))
        total += machine_total

        if verbose:
            print(f"✓ Machine {idx} solved: {machine_total} button presses")

    if infeasible_count > 0:
        print(f"\n⚠️  Summary: {infeasible_count} infeasible machine(s) skipped")
    return total


def main():
    """Main entry point for Part 2."""
    import sys

    verbose = "--verbose" in sys.argv or "-v" in sys.argv

    input_path = Path(__file__).parent / "input.txt"
    machines = parse_input(input_path.read_text())

    if verbose:
        print(f"Total machines to process: {len(machines)}")

    result = solve_part2(machines, verbose=verbose)
    print(f"\n{'=' * 60}")
    print(f"Part 2 Result: {result}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
