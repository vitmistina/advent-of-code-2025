# API Contract: Solver Functions

**Feature**: Day 10 Part 2 - Joltage Configuration  
**Date**: 2025-12-12  
**Type**: Python Function Signatures

---

## Core Solver API

### `solve_part2(data: List[Machine]) -> int`

**Description**: Main entry point for solving Part 2 puzzle. Processes all machines and returns total minimum button presses.

**Input**:

```python
data: List[Machine]  # Parsed machine definitions from input file
```

**Output**:

```python
int  # Total minimum button presses across all machines
```

**Behavior**:

- Iterates through each machine in data
- Constructs button matrix B and target vector t for each
- Solves integer linear programming problem B·x = t
- Aggregates total presses across all machines
- Returns total sum

**Example**:

```python
machines = parse_input(input_text)
result = solve_part2(machines)  # Returns 33 for test input
```

**Error Handling**:

- If a machine is infeasible, logs warning and skips (contributes 0 to total)
- Raises `ValueError` if input data is malformed

---

### `solve_integer_linear_system(B: np.ndarray, t: np.ndarray) -> Optional[np.ndarray]`

**Description**: Solves B·x = t for non-negative integer x minimizing ||x||₁.

**Input**:

```python
B: np.ndarray  # Button matrix, shape (n_counters, n_buttons), dtype=int
t: np.ndarray  # Target vector, shape (n_counters,), dtype=int
```

**Output**:

```python
Optional[np.ndarray]  # Solution vector x of shape (n_buttons,) with dtype=int,
                      # or None if system is infeasible
```

**Constraints**:

- B·x = t must hold exactly
- x[i] ≥ 0 for all i (non-negative)
- x[i] ∈ ℤ for all i (integer)
- Minimizes sum(x) among all feasible solutions

**Algorithm**:

1. Row-reduce augmented matrix [B | t] to identify pivot/free variables
2. Check feasibility (no contradictions)
3. Enumerate free variable assignments within smart bounds
4. For each assignment, back-substitute to solve for pivot variables
5. Validate non-negativity and exact match
6. Return solution with minimum L1 norm

**Example**:

```python
B = np.array([[0, 0, 0, 0, 1, 1],
              [0, 1, 0, 0, 0, 1],
              [0, 0, 1, 1, 1, 0],
              [1, 1, 0, 1, 0, 0]], dtype=int)
t = np.array([3, 5, 4, 7], dtype=int)

x = solve_integer_linear_system(B, t)
# x might be [1, 2, 0, 1, 1, 1] with sum = 6
```

**Performance**:

- Expected: O(2^k · n · m) where k = free variables
- Typical: <0.1s for k ≤ 10
- Falls back to SciPy if k > 15 (optional)

**Error Handling**:

- Returns `None` if system is infeasible (no solution exists)
- Raises `ValueError` if B and t have incompatible shapes

---

### `build_button_matrix(buttons: List[List[int]], num_counters: int) -> np.ndarray`

**Description**: Constructs the button matrix B from button definitions.

**Input**:

```python
buttons: List[List[int]]  # Each sublist contains counter indices affected by that button
num_counters: int         # Total number of counters in the machine
```

**Output**:

```python
np.ndarray  # Matrix B of shape (num_counters, num_buttons) with dtype=int
            # B[i,j] = 1 if button j affects counter i, else 0
```

**Example**:

```python
buttons = [[3], [1, 3], [2], [2, 3], [0, 2], [0, 1]]
num_counters = 4

B = build_button_matrix(buttons, num_counters)
# B.shape = (4, 6)
# B = [[0, 0, 0, 0, 1, 1],
#      [0, 1, 0, 0, 0, 1],
#      [0, 0, 1, 1, 1, 0],
#      [1, 1, 0, 1, 0, 0]]
```

**Validation**:

- All counter indices must be in range [0, num_counters)
- Raises `IndexError` if indices out of bounds

---

## Parsing API (Reused from Part 1)

### `parse_input(input_text: str) -> List[Machine]`

**Description**: Parses the complete puzzle input into a list of machine definitions.

**Input**:

```python
input_text: str  # Multi-line string with one machine per line
```

**Output**:

```python
List[Machine]  # List of parsed machine dictionaries
```

**Example**:

```python
input_text = """
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
"""

machines = parse_input(input_text)
# Returns list of 2 Machine dicts
```

**Error Handling**:

- Skips empty lines
- Raises `ValueError` if line format is invalid

---

### `parse_line(line: str) -> Machine`

**Description**: Parses a single machine definition line.

**Input**:

```python
line: str  # Format: "[lights] (buttons) (buttons) ... {targets}"
```

**Output**:

```python
Machine  # Dict with keys: 'lights', 'buttons', 'jolts'
```

**Example**:

```python
line = "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"

machine = parse_line(line)
# {
#   'lights': [0, 1, 1, 0],
#   'buttons': [[3], [1, 3], [2], [2, 3], [0, 2], [0, 1]],
#   'jolts': [3, 5, 4, 7]
# }
```

**Error Handling**:

- Raises `ValueError` if brackets, parentheses, or braces are missing
- Raises `ValueError` if content cannot be parsed as integers

---

## Validation API

### `verify_solution(B: np.ndarray, t: np.ndarray, x: np.ndarray) -> bool`

**Description**: Verifies that a solution satisfies all constraints.

**Input**:

```python
B: np.ndarray  # Button matrix (n_counters, n_buttons)
t: np.ndarray  # Target vector (n_counters,)
x: np.ndarray  # Candidate solution (n_buttons,)
```

**Output**:

```python
bool  # True if x satisfies B·x = t and x ≥ 0, False otherwise
```

**Validation Checks**:

1. `np.array_equal(B @ x, t)` — exact equality
2. `np.all(x >= 0)` — non-negativity
3. `np.all(x == x.astype(int))` — integer values (no fractional presses)

**Example**:

```python
x = np.array([1, 2, 0, 1, 1, 1])
is_valid = verify_solution(B, t, x)  # Returns True if constraints satisfied
```

---

### `is_system_feasible(B: np.ndarray, t: np.ndarray) -> bool`

**Description**: Checks if the linear system has any solutions (not necessarily non-negative integer).

**Input**:

```python
B: np.ndarray  # Button matrix
t: np.ndarray  # Target vector
```

**Output**:

```python
bool  # True if system has solutions, False if contradictory
```

**Algorithm**:

- Row-reduce augmented matrix [B | t]
- Check for contradictory rows (0 = c where c ≠ 0)
- Return False if contradiction found, True otherwise

**Example**:

```python
# Infeasible system
B = np.array([[1, 2], [2, 4]])
t = np.array([1, 3])  # Second row implies 1=1.5, contradiction

is_system_feasible(B, t)  # Returns False
```

---

## Utility API

### `compute_enumeration_bounds(B: np.ndarray, t: np.ndarray, free_cols: List[int]) -> List[Tuple[int, int]]`

**Description**: Computes smart bounds for free variable enumeration using LP relaxation.

**Input**:

```python
B: np.ndarray       # Button matrix
t: np.ndarray       # Target vector
free_cols: List[int] # Indices of free variables
```

**Output**:

```python
List[Tuple[int, int]]  # List of (lower, upper) bounds for each free variable
```

**Example**:

```python
bounds = compute_enumeration_bounds(B, t, [0, 2, 5])
# [(0, 5), (0, 3), (0, 7)]  # Three free variables with individual bounds
```

**Strategy**:

1. Solve LP relaxation (continuous variables)
2. Use ceiling of LP solution as upper bound
3. Add small buffer (e.g., +2) for safety
4. Cap at sum(t) as absolute upper bound

---

### `gaussian_elimination_integer(B: np.ndarray, t: np.ndarray) -> Tuple[np.ndarray, List[int], List[int]]`

**Description**: Performs Gaussian elimination over integers/rationals to identify pivot and free variables.

**Input**:

```python
B: np.ndarray  # Button matrix
t: np.ndarray  # Target vector
```

**Output**:

```python
Tuple[np.ndarray, List[int], List[int]]
  # (reduced_augmented_matrix, pivot_columns, free_columns)
```

**Example**:

```python
aug, pivots, free_vars = gaussian_elimination_integer(B, t)
# pivots = [0, 2, 3]  # Columns with pivots
# free_vars = [1, 4, 5]  # Columns without pivots (degrees of freedom)
```

**Notes**:

- Uses `fractions.Fraction` for exact rational arithmetic during elimination
- Returns augmented matrix in row echelon form
- Pivot columns identify basic variables, free columns identify free variables

---

## Type Definitions

### Machine (TypedDict)

```python
from typing import TypedDict, List

class Machine(TypedDict):
    lights: List[int]       # Binary indicator states (legacy from Part 1)
    buttons: List[List[int]] # Button definitions (counter indices)
    jolts: List[int]        # Target joltage values (Part 2)
```

---

## Error Types

### `InfeasibleSystemError(Exception)`

Raised when a machine's linear system has no non-negative integer solution.

**Attributes**:

- `message: str` — Error description
- `B: np.ndarray` — Button matrix causing infeasibility
- `t: np.ndarray` — Target vector

**Example**:

```python
raise InfeasibleSystemError(
    f"System B·x = t has no non-negative integer solution: {t}"
)
```

---

## Performance Requirements

### Time Complexity Targets

| Operation                     | Expected Complexity         | Target Time     |
| ----------------------------- | --------------------------- | --------------- |
| `parse_input`                 | O(n_machines · n_buttons)   | <0.01s          |
| `build_button_matrix`         | O(n_counters · n_buttons)   | <0.001s         |
| `solve_integer_linear_system` | O(2^k · n · m)              | <1s per machine |
| `solve_part2`                 | O(n_machines · 2^k · n · m) | <10s total      |

### Space Complexity

- Button matrix B: O(n_counters · n_buttons) ≈ 400 bytes for 20×20
- Enumeration state: O(2^k) where k ≤ 15 → ~32KB worst case
- Total memory: O(n_machines · n_counters · n_buttons) ≈ <1MB for typical inputs

---

## Testing Contracts

### Test Input Expectations

**Example 1**:

```python
B = [[0,0,0,0,1,1], [0,1,0,0,0,1], [0,0,1,1,1,0], [1,1,0,1,0,0]]
t = [3, 5, 4, 7]
expected_min_presses = 10
```

**Example 2**:

```python
B = [[1,0,1,1,0], [0,0,0,1,1], [1,1,0,1,1], [1,1,0,0,1], [0,0,1,0,1]]
t = [7, 5, 12, 7, 2]
expected_min_presses = 12
```

**Example 3**:

```python
B = [[1,1,1,0], [1,0,1,1], [1,0,1,1], [1,1,0,1], [1,0,1,0], [0,1,1,0]]
t = [10, 11, 11, 5, 10, 5]
expected_min_presses = 11
```

### Acceptance Criteria

- ✅ All three examples return correct minimum presses (10, 12, 11)
- ✅ Total across examples equals 33
- ✅ Solutions verify with `verify_solution(B, t, x) == True`
- ✅ Performance: Each example solves in <1 second

---

## Summary

**Core Functions**: `solve_part2`, `solve_integer_linear_system`, `build_button_matrix`  
**Parsing Functions**: Reused from Part 1 (`parse_input`, `parse_line`)  
**Validation Functions**: `verify_solution`, `is_system_feasible`  
**Utility Functions**: `compute_enumeration_bounds`, `gaussian_elimination_integer`

**Next Step**: Generate quickstart guide with implementation examples.
