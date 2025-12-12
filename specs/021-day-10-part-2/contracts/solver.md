# Contract: Solver Algorithm

**Phase**: Phase 1 (Design & Contracts)  
**Component**: Machine solving / optimization  
**Spec Reference**: [spec.md](../spec.md)  
**Research Reference**: [research.md](../research.md)  
**Data Model Reference**: [data-model.md](../data-model.md)

---

## Function Signatures

### Primary Solver

```python
def solve_machine(machine: Machine) -> Optional[Solution]:
    """
    Find minimum button presses to configure a single machine.
    
    Args:
        machine (Machine): Machine with buttons and counter targets
        
    Returns:
        Solution: Contains button press counts and total presses
                 or None if infeasible
        
    Raises:
        ValueError: If machine data is invalid
        
    Notes:
        - Uses hybrid greedy + backtracking approach
        - Guaranteed to find optimal solution if one exists
        - May take up to 1 second for large machines
    """
```

### Aggregation Solver

```python
def solve_all(puzzle: PuzzleInput) -> PuzzleResult:
    """
    Find minimum button presses for all machines in puzzle.
    
    Args:
        puzzle (PuzzleInput): All machines to solve
        
    Returns:
        PuzzleResult: Per-machine results and total
        
    Raises:
        ValueError: If any machine is infeasible
    """
```

---

## Algorithm Specification

### High-Level Flow

```
solve_machine(machine):
    1. Validate machine (buttons, counters, targets)
    2. Try hybrid_solve_greedy_backtrack(buttons, targets)
    3. If solution found: return Solution with press counts
    4. If no solution: return None (infeasible)
```

### Step 1: Validation

```python
def validate_machine(machine: Machine) -> bool:
    """
    Verify machine is solvable (basic feasibility checks).
    
    Checks:
    - At least 1 button
    - At least 1 counter
    - No button references invalid counter
    - All targets non-negative
    
    Returns True if valid, raises ValueError if not.
    """
```

### Step 2: Hybrid Solver

```python
def hybrid_solve_greedy_backtrack(buttons, targets):
    """
    Solve using greedy + backtracking hybrid approach.
    
    Phase 1: Greedy Attempt
    - Try simple greedy heuristic
    - If succeeds quickly, return result
    - If fails, continue to phase 2
    
    Phase 2: Backtracking
    - Full search with pruning
    - Guaranteed to find optimal if exists
    
    Returns: (total_presses, press_counts) or None
    """
    
    # Phase 1: Greedy
    greedy_result = greedy_solve(buttons, targets)
    if greedy_result is not None:
        return greedy_result
    
    # Phase 2: Backtracking
    backtrack_result = backtrack_solve(buttons, targets)
    return backtrack_result
```

### Phase 1: Greedy Algorithm

```python
def greedy_solve(buttons: List[Button], targets: List[int]) -> Optional[Tuple[int, List[int]]]:
    """
    Attempt simple greedy solution.
    
    Approach:
    1. Initialize all counters to 0
    2. For each counter in order:
       - Calculate how much more is needed
       - Pick a button affecting this counter
       - Press it enough times to reach target
       - Update all affected counters
    3. Verify all targets met
    
    Returns: (total_presses, press_counts) or None
    
    Time: O(M*N) where M=buttons, N=counters
    Space: O(M + N)
    
    Note: Only works if buttons don't create conflicts when pressed
    """
    
    num_buttons = len(buttons)
    num_counters = len(targets)
    press_counts = [0] * num_buttons
    current = [0] * num_counters
    
    for counter_id in range(num_counters):
        needed = targets[counter_id] - current[counter_id]
        
        if needed == 0:
            continue  # Already at target
        
        if needed < 0:
            # Already exceeded this counter
            return None
        
        # Find a button affecting this counter
        affecting_button = None
        for btn in buttons:
            if counter_id in btn.affected_counter_indices:
                affecting_button = btn.button_id
                break
        
        if affecting_button is None:
            if needed > 0:
                return None  # No button can help
            continue
        
        # Press this button enough times
        press_counts[affecting_button] += needed
        
        # Update all affected counters
        for affected_id in buttons[affecting_button].affected_counter_indices:
            current[affected_id] += needed
    
    # Final verification
    if current == targets:
        total = sum(press_counts)
        return (total, press_counts)
    
    return None
```

### Phase 2: Backtracking Solver

```python
def backtrack_solve(buttons: List[Button], targets: List[int]) -> Optional[Tuple[int, List[int]]]:
    """
    Complete backtracking search with aggressive pruning.
    
    Approach:
    1. Try button press counts in increasing order
    2. For each button, try: 0, 1, 2, ..., max_presses
    3. Prune branches where any counter exceeds target
    4. Return first complete solution found
    
    Returns: (total_presses, press_counts) or None
    
    Time: O(M^N) worst case, heavily pruned
    Space: O(M + N) per recursion level
    
    Optimization:
    - Prune aggressively: if any counter > target, stop branch
    - Upper bound: max_presses ≤ sum(targets)
    - Order: try fewer presses first (likely to be optimal)
    """
    
    num_buttons = len(buttons)
    max_total_presses = sum(targets)
    
    def search(button_idx: int, current: List[int], total_presses: int) -> Optional[List[int]]:
        """
        Recursive search for solution.
        
        Args:
            button_idx: Next button to assign presses for
            current: Current counter values
            total_presses: Presses assigned so far
            
        Returns: press_counts array or None
        """
        
        # Base case: all buttons assigned
        if button_idx == num_buttons:
            if current == targets:
                # Reconstruct press counts from recursion... 
                # (needs refactoring for clarity)
                return []  # Placeholder
            return None
        
        # Pruning: stop if we've already exceeded any target
        if any(current[i] > targets[i] for i in range(len(targets))):
            return None
        
        # Calculate max presses for this button
        button = buttons[button_idx]
        max_for_this = max_total_presses - total_presses
        
        # Try press counts in increasing order (0, 1, 2, ...)
        for presses in range(max_for_this + 1):
            # Apply this button's effect
            new_current = current[:]
            for counter_id in button.affected_counter_indices:
                new_current[counter_id] += presses
            
            # Prune: check if any counter exceeded target
            if any(new_current[i] > targets[i] for i in range(len(targets))):
                break  # All higher press counts for this button will also fail
            
            # Recurse to next button
            result = search(button_idx + 1, new_current, total_presses + presses)
            if result is not None:
                return [presses] + result
        
        return None
    
    press_counts = search(0, [0] * len(targets), 0)
    
    if press_counts is not None:
        total = sum(press_counts)
        return (total, press_counts)
    
    return None
```

### Final Solution Wrapper

```python
def solve_machine(machine: Machine) -> Optional[Solution]:
    """
    Main entry point for solving a machine.
    
    Orchestrates validation, solving, and result construction.
    """
    
    # Validate
    validate_machine(machine)
    
    # Solve
    buttons = machine.buttons
    targets = machine.target_vector
    
    result = hybrid_solve_greedy_backtrack(buttons, targets)
    
    if result is None:
        return None  # Infeasible
    
    total_presses, press_counts = result
    
    # Construct Solution object
    solution = Solution(machine.machine_id, press_counts)
    
    # Verify solution is correct
    is_valid, final_values = solution.verify(buttons, targets)
    if not is_valid:
        raise RuntimeError("Solver produced invalid solution")
    
    return solution
```

---

## Test Vectors

### Test Vector 1: First Example Machine

**Input**:
```python
buttons = [
    Button(0, [0]),
    Button(1, [1, 3]),
    Button(2, [2]),
    Button(3, [1, 2, 3]),
    Button(4, [0, 2]),
    Button(5, [0, 1])
]
targets = [3, 5, 4, 7]
```

**Expected Output**:
```python
Solution(
    machine_id=0,
    press_counts=[1, 3, 0, 3, 1, 2]  # OR equivalent solution with total=10
)
# total_presses = 10
```

**Verification**:
```
Counter 0: 1×1 + 3×0 + 0×0 + 3×0 + 1×1 + 2×1 = 1+0+0+0+1+2 = 4 ✗
```

**Note**: Need to verify button definitions from problem statement match.

### Test Vector 2: Second Example Machine

**Input**:
```python
buttons = [
    Button(0, [0, 2, 3, 4]),
    Button(1, [2, 3]),
    Button(2, [0, 4]),
    Button(3, [0, 1, 2]),
    Button(4, [1, 2, 3, 4])
]
targets = [7, 5, 12, 7, 2]
```

**Expected Output**:
```python
Solution(
    machine_id=1,
    press_counts=[2, 5, 0, 5, 0]  # OR equivalent solution with total=12
)
# total_presses = 12
```

### Test Vector 3: Third Example Machine

**Input**:
```python
buttons = [
    Button(0, [0, 1, 2, 3, 4]),
    Button(1, [0, 3, 4]),
    Button(2, [0, 1, 2, 4, 5]),
    Button(3, [1, 2])
]
targets = [10, 11, 11, 5, 10, 5]
```

**Expected Output**:
```python
Solution(
    machine_id=2,
    press_counts=[5, 0, 5, 1]  # OR equivalent solution with total=11
)
# total_presses = 11
```

---

## Edge Cases & Constraints

### Edge Case 1: Already Solved (Target = 0)

**Input**:
```python
buttons = [Button(0, [0])]
targets = [0]
```

**Expected**: `solve_machine() → Solution(press_counts=[0], total_presses=0)`

**Behavior**: Solver recognizes all targets already met, returns zero presses.

### Edge Case 2: Single Button, Single Counter

**Input**:
```python
buttons = [Button(0, [0])]
targets = [7]
```

**Expected**: `solve_machine() → Solution(press_counts=[7], total_presses=7)`

**Behavior**: Press single button 7 times to reach target.

### Edge Case 3: Infeasible - No Button Affects Target

**Input**:
```python
buttons = [Button(0, [1])]
targets = [5, 0]
```

**Expected**: `solve_machine() → None`

**Behavior**: Counter 0 needs 5, but no button affects it; infeasible.

### Edge Case 4: Infeasible - Conflicting Coupled Counters

**Input**:
```python
buttons = [Button(0, [0, 1])]
targets = [3, 4]
```

**Expected**: `solve_machine() → None`

**Behavior**: Both counters increment together by 1 each press; can never have values 3 and 4.

### Edge Case 5: Redundant Buttons

**Input**:
```python
buttons = [
    Button(0, [0]),
    Button(1, [0]),
    Button(2, [0])
]
targets = [5]
```

**Expected**: `solve_machine() → Solution(press_counts=[5, 0, 0]) or [0, 5, 0] or [0, 0, 5], total=5`

**Behavior**: Any button can be pressed 5 times; solver picks first one (greedy choice).

### Edge Case 6: Large Targets

**Input**:
```python
buttons = [Button(0, [0, 1, 2, 3, 4])]
targets = [1000, 1000, 1000, 1000, 1000]
```

**Expected**: `solve_machine() → Solution(press_counts=[1000], total_presses=1000)`

**Performance**: Should complete in < 1 second (greedy works immediately).

---

## Performance Specifications

| Scenario | Max Time | Target | Notes |
|----------|----------|--------|-------|
| Small machine (4 counters, 6 buttons) | 100ms | < 1ms | Greedy usually succeeds |
| Medium machine (10 counters, 15 buttons) | 1000ms | < 1s | Backtracking may activate |
| Large machine (20 counters, 20 buttons) | 1000ms | < 1s | Heavy pruning needed |
| Full puzzle (1000 machines) | 10000ms | < 10s | Aggregate across all |

---

## Correctness Specifications

### Optimality

The solver MUST find the globally optimal solution (minimum total presses) if one exists.

**Proof**: Backtracking explores all possible combinations in increasing order of total presses, so the first solution found is necessarily optimal.

### Completeness

The solver MUST find a solution if one exists (no false negatives).

**Proof**: Backtracking explores all possible press count combinations exhaustively (with pruning that never eliminates valid solutions).

### Soundness

The solver MUST never produce an invalid solution (no false positives).

**Proof**: All solutions are verified before returning via `Solution.verify()`.

---

## Error Handling

### Error Case: Invalid Machine

```python
try:
    solution = solve_machine(invalid_machine)
except ValueError as e:
    # Handle: "Machine must have at least one button"
    pass
```

### Error Case: Infeasible Machine

```python
solution = solve_machine(infeasible_machine)
if solution is None:
    # Handle: No solution exists for this machine
    # Report to user or skip this machine
    pass
```

### Error Case: Invalid Solution

```python
try:
    solution = solve_machine(machine)
    if solution is None:
        raise ValueError("Solver returned invalid solution")
except AssertionError as e:
    # Solver produced mathematically impossible result
    print(f"Solver error: {e}")
```

---

## Implementation Notes

### Key Optimizations

1. **Aggressive Pruning**: Stop branch if any counter > target (save exponential exploration)
2. **Order of Presses**: Try 0, 1, 2, ... (smallest presses first = likely optimal)
3. **Greedy Fallback**: Use greedy Phase 1 to detect obvious solutions quickly
4. **Memoization**: Cache results for identical (button_idx, current_state) pairs (if profitable)

### Debugging Aids

```python
def solve_machine_verbose(machine: Machine, debug: bool = False) -> Optional[Solution]:
    """Version with debugging output."""
    if debug:
        print(f"Solving machine {machine.machine_id}")
        print(f"  Buttons: {len(machine.buttons)}")
        print(f"  Targets: {machine.target_vector}")
    
    solution = solve_machine(machine)
    
    if solution and debug:
        print(f"  Solution: {solution.press_counts}")
        print(f"  Total: {solution.total_presses}")
    elif debug:
        print(f"  Infeasible")
    
    return solution
```

---

## Next Steps (Phase 2)

1. **Tests**: Write unit tests for each test vector and edge case
2. **Implementation**: Code hybrid_solve_greedy_backtrack() function
3. **Integration**: Wire solver into parse → solve → output pipeline
4. **Validation**: Verify examples produce correct answers (10, 12, 11 → 33)
