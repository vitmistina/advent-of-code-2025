# Data Model: Day 10 Part 2 - Joltage Configuration

**Feature**: Joltage Configuration Optimization  
**Date**: 2025-12-12  
**Status**: Design Phase

---

## Overview

This data model defines the entities and relationships for solving the joltage counter optimization problem. The model extends Part 1's indicator light system to handle integer-valued counters with increment operations instead of binary toggles.

---

## Core Entities

### 1. Machine

Represents a factory machine with buttons that increment joltage counters.

**Attributes:**

| Attribute  | Type                 | Description                                       | Validation                                     |
| ---------- | -------------------- | ------------------------------------------------- | ---------------------------------------------- |
| `lights`   | `List[int]`          | Binary indicator states (0/1) - ignored in Part 2 | Optional, legacy from Part 1                   |
| `buttons`  | `List[Button]`       | Collection of available buttons                   | Non-empty list                                 |
| `counters` | `List[Counter]`      | Collection of joltage counters                    | Non-empty list, length matches targets         |
| `targets`  | `List[int]`          | Target joltage values for each counter            | Non-negative integers, length matches counters |
| `solution` | `Optional[Solution]` | Optimal button press solution                     | Computed, may be None if infeasible            |

**Relationships:**

- Has many `Button` (1:N)
- Has many `Counter` (1:N)
- Has one `Solution` (1:1, optional)

**State Transitions:**

```
UNINITIALIZED → PARSED → SOLVED → VALIDATED
```

**Business Rules:**

- Number of counters must equal length of targets vector
- Button indices must reference valid counters (0 ≤ idx < num_counters)
- Targets must be non-negative integers

**Example:**

```python
Machine(
    buttons=[
        Button(id=0, affected_counters=[3]),
        Button(id=1, affected_counters=[1, 3]),
        Button(id=2, affected_counters=[2]),
        Button(id=3, affected_counters=[2, 3]),
        Button(id=4, affected_counters=[0, 2]),
        Button(id=5, affected_counters=[0, 1]),
    ],
    targets=[3, 5, 4, 7],
    counters=[Counter(0, 0), Counter(1, 0), Counter(2, 0), Counter(3, 0)]
)
```

---

### 2. Button

Represents a physical button that increments specific joltage counters when pressed.

**Attributes:**

| Attribute           | Type        | Description                                 | Validation             |
| ------------------- | ----------- | ------------------------------------------- | ---------------------- |
| `id`                | `int`       | Unique button identifier within machine     | Non-negative           |
| `affected_counters` | `List[int]` | Indices of counters this button increments  | Valid counter indices  |
| `press_count`       | `int`       | Number of times pressed in optimal solution | Non-negative, computed |

**Relationships:**

- Belongs to one `Machine` (N:1)
- Affects many `Counter` (M:N through affected_counters)

**Operations:**

```python
def press(self, counters: List[Counter], times: int = 1) -> None:
    """Increment affected counters by specified number of presses."""
    for counter_idx in self.affected_counters:
        counters[counter_idx].increment(times)
```

**Business Rules:**

- A button may affect zero or more counters (empty list is valid)
- Pressing a button increments each affected counter by exactly +1
- Press count in solution must be non-negative integer

**Example:**

```python
Button(id=1, affected_counters=[1, 3], press_count=2)
# Pressing this button twice increments counter[1] by 2 and counter[3] by 2
```

---

### 3. Counter

Represents a joltage level tracker that can be incremented by button presses.

**Attributes:**

| Attribute       | Type  | Description                 | Validation                        |
| --------------- | ----- | --------------------------- | --------------------------------- |
| `index`         | `int` | Counter position in machine | Non-negative                      |
| `current_value` | `int` | Current joltage level       | Non-negative integer, starts at 0 |
| `target_value`  | `int` | Desired joltage level       | Non-negative integer              |

**Relationships:**

- Belongs to one `Machine` (N:1)
- Affected by many `Button` (M:N)

**Operations:**

```python
def increment(self, amount: int = 1) -> None:
    """Increase counter value by specified amount."""
    self.current_value += amount

def is_at_target(self) -> bool:
    """Check if counter has reached target value."""
    return self.current_value == self.target_value

def reset(self) -> None:
    """Reset counter to initial state (0)."""
    self.current_value = 0
```

**State Transitions:**

```
current_value: 0 → [incrementing] → target_value
```

**Business Rules:**

- All counters start at current_value = 0
- Target must be reached exactly (no overshooting in optimal solution)
- Values cannot be negative

**Example:**

```python
Counter(index=2, current_value=0, target_value=4)
# After 4 increments: current_value = 4, is_at_target() = True
```

---

### 4. Solution

Represents the optimal button press strategy for a machine.

**Attributes:**

| Attribute             | Type                           | Description                                | Validation                                  |
| --------------------- | ------------------------------ | ------------------------------------------ | ------------------------------------------- |
| `button_presses`      | `np.ndarray`                   | Vector of press counts per button          | Non-negative integers, length = num_buttons |
| `total_presses`       | `int`                          | Sum of all button presses (L1 norm)        | Non-negative                                |
| `is_feasible`         | `bool`                         | Whether solution satisfies all constraints | Computed                                    |
| `verification_result` | `Optional[VerificationResult]` | Proof that solution is correct             | Optional, for debugging                     |

**Relationships:**

- Belongs to one `Machine` (1:1)

**Operations:**

```python
def compute_total_presses(self) -> int:
    """Calculate total button presses (L1 norm)."""
    return int(np.sum(self.button_presses))

def verify(self, B: np.ndarray, t: np.ndarray) -> bool:
    """Verify solution satisfies B·x = t and x ≥ 0."""
    return np.array_equal(B @ self.button_presses, t) and np.all(self.button_presses >= 0)

def apply_to_machine(self, machine: Machine) -> None:
    """Apply button presses to machine and update counter values."""
    for button_id, press_count in enumerate(self.button_presses):
        for _ in range(press_count):
            machine.buttons[button_id].press(machine.counters)
```

**Business Rules:**

- Solution must satisfy B·x = t exactly (no approximation)
- All press counts must be non-negative integers
- Total presses should be minimal among all feasible solutions

**Example:**

```python
Solution(
    button_presses=np.array([1, 2, 0, 1, 1, 1]),  # 6 buttons
    total_presses=6,  # 1+2+0+1+1+1
    is_feasible=True
)
```

---

### 5. PuzzleInput

Represents the complete collection of machines from the input file.

**Attributes:**

| Attribute               | Type            | Description                                    | Validation             |
| ----------------------- | --------------- | ---------------------------------------------- | ---------------------- |
| `machines`              | `List[Machine]` | All machines to be configured                  | Non-empty list         |
| `total_minimum_presses` | `int`           | Aggregated minimum presses across all machines | Non-negative, computed |

**Relationships:**

- Has many `Machine` (1:N)

**Operations:**

```python
def solve_all_machines(self) -> int:
    """Solve each machine and return total minimum presses."""
    total = 0
    for machine in self.machines:
        solution = solve_machine(machine)
        if solution is not None:
            machine.solution = solution
            total += solution.total_presses
    self.total_minimum_presses = total
    return total

def get_unsolved_machines(self) -> List[Machine]:
    """Return machines without solutions (infeasible or not yet solved)."""
    return [m for m in self.machines if m.solution is None]
```

**Business Rules:**

- All machines are independent (solving one doesn't affect others)
- Total minimum presses is the sum of individual machine solutions
- Invalid machines (infeasible) should be logged but not fail entire puzzle

**Example:**

```python
PuzzleInput(
    machines=[machine1, machine2, machine3],
    total_minimum_presses=33  # 10 + 12 + 11
)
```

---

## Supporting Types

### LinearSystem

Represents the mathematical structure of the optimization problem.

**Attributes:**

| Attribute    | Type         | Description                                    |
| ------------ | ------------ | ---------------------------------------------- |
| `B`          | `np.ndarray` | Button matrix (n×m: counters × buttons)        |
| `t`          | `np.ndarray` | Target vector (n×1)                            |
| `rank`       | `int`        | Rank of matrix B                               |
| `pivot_cols` | `List[int]`  | Column indices with pivots (basic variables)   |
| `free_cols`  | `List[int]`  | Column indices without pivots (free variables) |

**Operations:**

```python
def row_reduce(self) -> np.ndarray:
    """Perform Gaussian elimination to row echelon form."""
    # Returns augmented matrix [B | t] in RREF

def is_feasible(self) -> bool:
    """Check if system has any solutions."""
    # Returns False if contradiction exists (0 = c where c ≠ 0)

def count_free_variables(self) -> int:
    """Return number of free variables (degrees of freedom)."""
    return len(self.free_cols)
```

---

### VerificationResult

Proof that a solution is correct.

**Attributes:**

| Attribute                 | Type            | Description                                  |
| ------------------------- | --------------- | -------------------------------------------- |
| `satisfies_equality`      | `bool`          | B·x = t holds                                |
| `satisfies_nonnegativity` | `bool`          | x ≥ 0 holds                                  |
| `counter_values`          | `List[int]`     | Final counter values after applying solution |
| `error_message`           | `Optional[str]` | Description of violation if any              |

---

## Validation Rules

### Input Validation

**Machine Parsing:**

- ✅ Line must contain bracket-delimited lights: `[.##.]`
- ✅ Line must contain parenthesis-delimited buttons: `(0,1,2)`
- ✅ Line must contain curly-brace-delimited targets: `{3,5,4,7}`
- ❌ Reject if any section is malformed or missing

**Button Validation:**

- ✅ Counter indices must be non-negative integers
- ✅ Counter indices must be within range [0, num_counters)
- ❌ Reject if indices out of bounds

**Target Validation:**

- ✅ All target values must be non-negative integers
- ✅ Number of targets must equal number of counters
- ❌ Reject if count mismatch or negative values

### Solution Validation

**Feasibility Check:**

- ✅ Verify B·x = t exactly (no floating-point tolerance)
- ✅ Verify x[i] ≥ 0 for all i
- ✅ Verify x[i] ∈ ℤ (integer values)

**Optimality Check (for testing):**

- ✅ Compare with known example results (10, 12, 11)
- ⚠️ Cannot verify optimality in general without exhaustive search

---

## Matrix Construction

### Building the Button Matrix B

Given buttons and counters:

```python
def build_button_matrix(buttons: List[Button], num_counters: int) -> np.ndarray:
    """
    Construct matrix B where B[i,j] = 1 if button j affects counter i, else 0.

    Args:
        buttons: List of Button objects with affected_counters
        num_counters: Total number of counters in machine

    Returns:
        B matrix of shape (num_counters, num_buttons)
    """
    num_buttons = len(buttons)
    B = np.zeros((num_counters, num_buttons), dtype=int)

    for j, button in enumerate(buttons):
        for counter_idx in button.affected_counters:
            B[counter_idx, j] = 1

    return B
```

**Example:**

Buttons: `(3)`, `(1,3)`, `(2)`, `(2,3)`, `(0,2)`, `(0,1)`  
Counters: 4 (indices 0, 1, 2, 3)

```
Matrix B:
     B0  B1  B2  B3  B4  B5
C0: [ 0   0   0   0   1   1 ]
C1: [ 0   1   0   0   0   1 ]
C2: [ 0   0   1   1   1   0 ]
C3: [ 1   1   0   1   0   0 ]
```

---

## Edge Cases

### Zero Targets

**Scenario**: Counter already at target (target = 0)  
**Handling**: x = [0, 0, ..., 0] is optimal (0 presses)

### Infeasible System

**Scenario**: No non-negative integer solution exists  
**Handling**: Return None, log warning

### Redundant Buttons

**Scenario**: Multiple buttons with identical affected_counters  
**Handling**: Algorithm handles naturally (both are equivalent in solution)

### Overdetermined System

**Scenario**: More constraints than variables (n > m)  
**Handling**: May be infeasible; row reduction detects contradictions

### Underdetermined System

**Scenario**: More variables than constraints (m > n)  
**Handling**: Free variables exist; enumerate to find minimum L1 solution

---

## Summary

**Key Entities**: Machine, Button, Counter, Solution, PuzzleInput  
**Core Operation**: Construct B matrix, solve B·x = t for minimal ||x||₁  
**Validation**: Input parsing, constraint satisfaction, solution verification  
**Edge Cases**: Zero targets, infeasibility, redundancy handled explicitly

**Next Step**: Define API contracts for solver functions and data transformations.
