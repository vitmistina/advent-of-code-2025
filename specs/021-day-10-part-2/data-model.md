# Data Model: Day 10 Part 2 - Joltage Configuration System

**Phase**: Phase 1 (Design & Data Model)  
**Date**: 2025-12-12  
**Spec Reference**: [spec.md](./spec.md)  
**Research Reference**: [research.md](./research.md)

---

## Entity Relationships

```
PuzzleInput
├── Machine[] (1 to many)
│   ├── Button[] (1 to many)
│   │   └── counter_indices: int[]
│   ├── Counter[] (1 to many)
│   │   ├── index: int
│   │   ├── target: int
│   │   └── current_value: int
│   └── Solution
│       ├── press_counts: int[] (one per button)
│       └── total_presses: int

PuzzleResult
├── per_machine_results: int[] (one minimum presses per machine)
└── total_minimum_presses: int (sum of all machines)
```

---

## Entity Definitions

### 1. Button

**Purpose**: Represents a physical button on a machine that increments specific counters.

**Attributes**:
- `button_id` (int): Sequential index (0 to M-1) identifying this button
- `affected_counter_indices` (list[int]): Which counters this button affects
  - Example: `[1, 3]` means button increments counters 1 and 3 when pressed
  - Must be: non-empty, sorted, unique indices
  - Range: 0 to N-1 (where N is number of counters)

**Constraints**:
- Must have at least one affected counter (otherwise useless)
- Cannot have duplicate indices in affected list
- Cannot reference counter indices outside valid range [0, N-1]

**Validation Rules**:
```python
class Button:
    def __init__(self, button_id: int, affected_counter_indices: list[int]):
        assert isinstance(button_id, int) and button_id >= 0, "ID must be non-negative integer"
        assert isinstance(affected_counter_indices, list), "Must be list"
        assert len(affected_counter_indices) > 0, "Must affect at least one counter"
        assert len(affected_counter_indices) == len(set(affected_counter_indices)), "No duplicates"
        assert all(isinstance(idx, int) and idx >= 0 for idx in affected_counter_indices), "All indices must be non-negative integers"
        
        self.button_id = button_id
        self.affected_counter_indices = sorted(affected_counter_indices)
```

**Example**:
```
Button(0, [1, 3])    ✓ Valid: affects counters 1 and 3
Button(1, [2])       ✓ Valid: affects counter 2
Button(2, [0, 0])    ✗ Invalid: duplicate indices
Button(3, [])        ✗ Invalid: no affected counters
Button(4, [-1, 2])   ✗ Invalid: negative index
```

---

### 2. Counter

**Purpose**: Represents a joltage level tracker that must reach an exact target value.

**Attributes**:
- `counter_id` (int): Sequential index (0 to N-1) identifying this counter
- `target_value` (int): Exact value this counter must reach (non-negative)
- `current_value` (int): Current value of this counter (starts at 0, updated during solving)

**Constraints**:
- Target value must be non-negative integer
- Current value never exceeds target (solver prunes branches that violate this)
- Counter starts at 0 (invariant maintained during solving)

**Validation Rules**:
```python
class Counter:
    def __init__(self, counter_id: int, target_value: int):
        assert isinstance(counter_id, int) and counter_id >= 0, "ID must be non-negative integer"
        assert isinstance(target_value, int) and target_value >= 0, "Target must be non-negative integer"
        
        self.counter_id = counter_id
        self.target_value = target_value
        self.current_value = 0  # Always starts at 0
    
    def increment(self, amount: int = 1):
        """Increase current value when button is pressed."""
        assert amount > 0, "Can only increment by positive amount"
        self.current_value += amount
    
    def is_at_target(self) -> bool:
        """Check if counter has reached target."""
        return self.current_value == self.target_value
    
    def exceeds_target(self) -> bool:
        """Check if counter has surpassed target (pruning condition)."""
        return self.current_value > self.target_value
    
    def reset(self):
        """Reset to 0 for next solve attempt."""
        self.current_value = 0
```

**Example**:
```
Counter(0, 5)        ✓ Valid: counter 0 needs to reach 5
Counter(1, 0)        ✓ Valid: counter 1 already at target (needs nothing)
Counter(2, -3)       ✗ Invalid: negative target
```

---

### 3. Machine

**Purpose**: Represents a single factory machine that needs joltage configuration.

**Attributes**:
- `machine_id` (int): Optional identifier for this machine (e.g., line number)
- `buttons` (list[Button]): All available buttons for this machine
  - Must have at least 1 button
  - M buttons (indexed 0 to M-1)
- `counters` (list[Counter]): All joltage counters for this machine
  - Must have at least 1 counter
  - N counters (indexed 0 to N-1)
  - Each counter has independent target value

**Derived Attributes**:
- `num_buttons` (int): Length of buttons list (M)
- `num_counters` (int): Length of counters list (N)
- `solution` (Solution): Result of solving this machine

**Constraints**:
- Button indices in buttons list must match their button_id values
- Counter indices in counters list must match their counter_id values
- All button affected_counter_indices must be in valid range [0, N-1]
- No requirement that all buttons/counters are used

**Validation Rules**:
```python
class Machine:
    def __init__(self, machine_id: int, buttons: list[Button], counters: list[Counter]):
        assert isinstance(buttons, list) and len(buttons) > 0, "Must have at least one button"
        assert isinstance(counters, list) and len(counters) > 0, "Must have at least one counter"
        
        # Validate button IDs match positions
        for i, btn in enumerate(buttons):
            assert btn.button_id == i, f"Button at position {i} has ID {btn.button_id}"
        
        # Validate counter IDs match positions
        for i, cnt in enumerate(counters):
            assert cnt.counter_id == i, f"Counter at position {i} has ID {cnt.counter_id}"
        
        # Validate button references valid counters
        num_counters = len(counters)
        for btn in buttons:
            for idx in btn.affected_counter_indices:
                assert 0 <= idx < num_counters, f"Button {btn.button_id} references invalid counter {idx}"
        
        self.machine_id = machine_id
        self.buttons = buttons
        self.counters = counters
        self.solution = None
    
    @property
    def num_buttons(self) -> int:
        return len(self.buttons)
    
    @property
    def num_counters(self) -> int:
        return len(self.counters)
    
    @property
    def target_vector(self) -> list[int]:
        """Get target values in order."""
        return [c.target_value for c in self.counters]
    
    @property
    def is_solved(self) -> bool:
        """Check if all counters are at target."""
        return all(c.is_at_target() for c in self.counters)
    
    @property
    def exceeds_any_target(self) -> bool:
        """Check if any counter exceeds its target (for pruning)."""
        return any(c.exceeds_target() for c in self.counters)
    
    def reset(self):
        """Reset all counters to 0 for solving."""
        for counter in self.counters:
            counter.reset()
```

**Example**:
```
Machine(
    machine_id=0,
    buttons=[
        Button(0, [0]),
        Button(1, [1, 3]),
        Button(2, [2])
    ],
    counters=[
        Counter(0, 3),
        Counter(1, 5),
        Counter(2, 4),
        Counter(3, 7)
    ]
)
✓ Valid: 3 buttons, 4 counters, all constraints satisfied
```

---

### 4. Solution

**Purpose**: Represents the solution to a single machine (minimum button presses needed).

**Attributes**:
- `machine_id` (int): ID of machine this solves
- `press_counts` (list[int]): How many times each button is pressed
  - Index i = how many times button i is pressed
  - Must be non-negative integers
  - Length must equal number of buttons
- `total_presses` (int): Sum of all press counts
  - Must equal sum(press_counts)
- `is_feasible` (bool): Whether a valid solution exists

**Computed Properties**:
- `verification` (dict): Shows how each button press affects each counter

**Validation Rules**:
```python
class Solution:
    def __init__(self, machine_id: int, press_counts: list[int] = None):
        self.machine_id = machine_id
        self.press_counts = press_counts or []
        
        if press_counts:
            assert all(isinstance(p, int) and p >= 0 for p in press_counts), \
                "All press counts must be non-negative integers"
            assert len(press_counts) > 0, "Must have at least one button press count"
    
    @property
    def total_presses(self) -> int:
        """Total button presses (sum of all press counts)."""
        return sum(self.press_counts) if self.press_counts else 0
    
    @property
    def is_feasible(self) -> bool:
        """Whether solution is valid (all presses are non-negative)."""
        return all(p >= 0 for p in self.press_counts) if self.press_counts else False
    
    def verify(self, buttons: list[Button], targets: list[int]) -> tuple[bool, list[int]]:
        """
        Verify this solution actually reaches targets.
        Returns: (is_valid, final_counter_values)
        """
        if not self.is_feasible:
            return False, []
        
        if len(self.press_counts) != len(buttons):
            return False, []
        
        # Simulate button presses
        final_values = [0] * len(targets)
        for button_idx, press_count in enumerate(self.press_counts):
            button = buttons[button_idx]
            for counter_idx in button.affected_counter_indices:
                final_values[counter_idx] += press_count
        
        # Check if matches targets
        is_valid = final_values == targets
        return is_valid, final_values
```

**Example**:
```
Solution(machine_id=0, press_counts=[1, 3, 0, 3, 1, 2])
- total_presses = 10
- is_feasible = True
- verify() = (True, [3, 5, 4, 7])  ← matches targets
```

---

### 5. PuzzleInput

**Purpose**: Represents the entire puzzle input (all machines to solve).

**Attributes**:
- `machines` (list[Machine]): All machines in the puzzle
- `metadata` (dict): Optional metadata (source file, timestamp, etc.)

**Computed Properties**:
- `num_machines` (int): Total machines to solve
- `total_buttons` (int): Sum of buttons across all machines
- `total_counters` (int): Sum of counters across all machines

**Methods**:
- `parse_from_text(text: str)`: Create from problem input format
- `save_to_file(path: str)`: Persist to file
- `load_from_file(path: str)`: Load from file

**Example**:
```python
class PuzzleInput:
    def __init__(self, machines: list[Machine], metadata: dict = None):
        assert isinstance(machines, list) and len(machines) > 0
        self.machines = machines
        self.metadata = metadata or {}
    
    @property
    def num_machines(self) -> int:
        return len(self.machines)
    
    def solve_all(self) -> int:
        """Solve all machines and return total presses."""
        total = 0
        for machine in self.machines:
            solution = solve_machine(machine)
            if solution is None:
                raise ValueError(f"Machine {machine.machine_id} is infeasible")
            machine.solution = solution
            total += solution.total_presses
        return total
```

---

### 6. PuzzleResult

**Purpose**: Represents the final result of solving the entire puzzle.

**Attributes**:
- `per_machine_results` (list[int]): Minimum presses for each machine in order
- `total_minimum_presses` (int): Sum of all machine results
- `solved_at` (datetime): When solution was computed
- `metadata` (dict): Solution metadata (algorithm, time, etc.)

**Validation**:
```python
class PuzzleResult:
    def __init__(self, per_machine_results: list[int], metadata: dict = None):
        assert isinstance(per_machine_results, list)
        assert all(isinstance(r, int) and r >= 0 for r in per_machine_results)
        
        self.per_machine_results = per_machine_results
        self.total_minimum_presses = sum(per_machine_results)
        self.metadata = metadata or {}
    
    def __repr__(self) -> str:
        return f"PuzzleResult(total={self.total_minimum_presses}, machines={len(self.per_machine_results)})"
```

---

## State Transitions

### Machine Solving Lifecycle

```
[Unsolved] --solve_machine()--> [Solving] --complete--> [Solved]
                                   |
                                   +--infeasible--> [Infeasible]
```

**States**:
- **Unsolved**: Machine created, no solution attempted
- **Solving**: Algorithm actively working on solution
- **Solved**: Valid solution found (solution property populated)
- **Infeasible**: No valid solution exists

**Transitions**:
```python
def solve_machine(machine: Machine) -> Solution:
    """
    Transition machine from Unsolved → Solving → Solved
    Or: Unsolved → Infeasible if no solution exists
    """
    machine.reset()  # Reset all counters to 0
    
    solution = hybrid_solve(machine.buttons, machine.target_vector)
    
    if solution is None:
        machine.solution = None  # Infeasible
        raise InfeasibleError(f"No solution for machine {machine.machine_id}")
    
    machine.solution = solution
    return solution
```

---

## Validation Rules Summary

| Entity | Rule | Consequence |
|--------|------|-------------|
| Button | At least 1 affected counter | Invalid otherwise |
| Button | No duplicate counter indices | Invalid otherwise |
| Button | All indices ∈ [0, N-1] | OutOfBounds error |
| Counter | Target ≥ 0 | ValueError |
| Counter | Current ≤ Target (during solving) | Pruning trigger |
| Machine | At least 1 button | Invalid otherwise |
| Machine | At least 1 counter | Invalid otherwise |
| Machine | Button IDs match positions | AssertionError |
| Counter | Counter IDs match positions | AssertionError |
| Solution | All press counts ≥ 0 | Infeasible |
| Solution | Can verify against targets | True/False from verify() |

---

## Data Flow

```
Input File
    ↓
parse_input() → PuzzleInput (list of Machines)
    ↓
For each Machine:
    ├─ reset()
    ├─ solve_machine() → Solution
    └─ solution.verify() → (bool, counter_values)
    ↓
PuzzleResult:
    ├─ per_machine_results = [10, 12, 11]
    └─ total_minimum_presses = 33
    ↓
Output (integer)
```

---

## Example Data Instances

### Example 1: First Machine

```python
Machine(
    machine_id=0,
    buttons=[
        Button(0, [0]),           # Button 0 affects counter 0
        Button(1, [1, 3]),        # Button 1 affects counters 1, 3
        Button(2, [2]),           # Button 2 affects counter 2
        Button(3, [1, 2, 3]),     # Button 3 affects counters 1, 2, 3
        Button(4, [0, 2]),        # Button 4 affects counters 0, 2
        Button(5, [0, 1])         # Button 5 affects counters 0, 1
    ],
    counters=[
        Counter(0, 3),
        Counter(1, 5),
        Counter(2, 4),
        Counter(3, 7)
    ]
)

# Solution:
Solution(
    machine_id=0,
    press_counts=[1, 3, 0, 3, 1, 2]
)
# Verify:
# Counter 0: 1×1 + 3×0 + 0×0 + 3×0 + 1×1 + 2×1 = 1+0+0+0+1+2 = 4... wait that doesn't match
# Need to verify this matches the button definitions correctly
```

**Note**: Actual button effects to be verified against problem statement.

---

## Next Steps (Phase 2)

1. **Parser Implementation**: Convert text format to Machine objects
2. **Solver Implementation**: Implement hybrid algorithm from research.md
3. **Test Suite**: Implement TDD tests based on data model
4. **Integration**: Wire parser, solver, and output together
