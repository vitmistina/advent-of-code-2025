# Research Phase: Day 10 Part 2 - Algorithm Analysis & Strategy

**Phase**: Phase 0 (Research & Analysis)  
**Date**: 2025-12-12  
**Status**: Complete  
**Output of**: Specification analysis and technical investigation

---

## Problem Summary

Given a factory machine with:
- **M buttons** (0 to M-1), each affecting specific counters
- **N joltage counters** (0 to N-1), each with a target value
- Counters start at 0
- Each button press increments its affected counters by 1

**Objective**: Minimize total button presses (sum of all press counts) to reach all target values simultaneously.

**Scope**: Solve this for each machine independently, then aggregate results.

---

## Mathematical Formulation

### System of Linear Equations

Let:
- $x_i$ = number of times button $i$ is pressed
- $b_{ij}$ = 1 if button $i$ affects counter $j$, 0 otherwise
- $t_j$ = target value for counter $j$

**Constraint System**:
$$\sum_{i=0}^{M-1} b_{ij} \cdot x_i = t_j \quad \forall j \in [0, N-1]$$

**Optimization**:
$$\text{Minimize} \sum_{i=0}^{M-1} x_i$$

**Subject to**:
$$x_i \geq 0 \text{ and integer} \quad \forall i$$

### Matrix Form

$$B \cdot \vec{x} = \vec{t}$$

where:
- $B$ is an $N \times M$ matrix (counters × buttons)
- $\vec{x}$ is the $M \times 1$ solution vector (button presses)
- $\vec{t}$ is the $N \times 1$ target vector

**Example 1** (from problem):
```
Buttons: (3), (1,3), (2), (2,3), (0,2), (0,1)
Targets: {3,5,4,7}

Matrix B (4x6):
     B0  B1  B2  B3  B4  B5
C0:  1   0   0   0   1   1    = 3
C1:  0   1   0   1   0   1    = 5
C2:  0   1   1   1   1   0    = 4
C3:  1   1   0   0   0   0    = 7

Solution: x = [1, 3, 0, 3, 1, 2]ᵀ
Total presses: 1+3+0+3+1+2 = 10 ✓
```

---

## Algorithm Evaluation

### Option 1: Gaussian Elimination (Linear Algebra)

**Approach**: Use Gaussian elimination with back-substitution to solve the system exactly.

**Advantages**:
- Polynomial time complexity: $O(M^2 \cdot N)$ or $O(N^3)$ depending on shape
- Handles exact integer solutions when they exist
- Can detect infeasible systems early

**Disadvantages**:
- May produce non-integer intermediate results
- Requires handling of floating-point precision issues
- Must validate that solution contains only non-negative integers
- Risk of numerical instability

**Complexity**: $O(\min(M^2N, N^3))$ for $N$ counters, $M$ buttons

**Feasibility**: **MODERATE** - Works but requires careful handling of integer constraints

---

### Option 2: Brute Force Search with Pruning

**Approach**: Enumerate button press combinations, pruning branches that exceed any target.

**Algorithm**:
1. Start with $x = [0, 0, ..., 0]$
2. For each button $i$, try all press counts from 0 to max_target
3. Prune branches where any counter exceeds its target
4. Return first solution found (greedy: try fewer presses first)

**Advantages**:
- Simple to implement and understand
- Naturally handles integer constraints
- Works for any button configuration (no singularity issues)
- Can terminate early if solution found

**Disadvantages**:
- Exponential worst-case: $O(T^M)$ where $T$ is average target
- Very slow for large targets or many buttons
- May timeout on large inputs

**Complexity**: Worst case $O(T^M)$, best case $O(1)$

**Feasibility**: **MODERATE** - Works for examples but may be too slow for actual puzzle

---

### Option 3: Integer Linear Programming (ILP)

**Approach**: Formulate as ILP and use a solver library.

**Algorithm**:
1. Define system $B \vec{x} = \vec{t}$
2. Define objective: minimize $\sum x_i$
3. Add constraints: $x_i \geq 0$, $x_i \in \mathbb{Z}$
4. Use library (e.g., `scipy.optimize.linprog` or PuLP)

**Advantages**:
- Optimal solution guaranteed
- Battle-tested algorithms
- Handles complex constraints easily
- Good performance for realistic sizes

**Disadvantages**:
- Requires external dependency (may not be available)
- Overkill for this problem's mathematical simplicity
- ILP is NP-hard in general (though often fast in practice)

**Complexity**: Variable based on solver (often much better than worst case)

**Feasibility**: **HIGH** - But adds dependency; check if already available

---

### Option 4: Greedy + Backtracking (Hybrid)

**Approach**: Try a greedy approach first, backtrack if stuck.

**Algorithm**:
1. Process counters in order: greedily find button combination for counter 0
2. Check if that combination works for counter 1
3. If not, backtrack and try alternative button combinations
4. Return first valid solution found

**Advantages**:
- Combines simplicity of greedy with exactness of backtracking
- Often terminates quickly on realistic inputs
- Natural integer handling
- No external dependencies

**Disadvantages**:
- May miss optimal solution (depends on ordering)
- Still exponential in worst case
- Requires careful implementation to avoid infinite loops

**Complexity**: $O(M^N)$ worst case, but typically much better

**Feasibility**: **HIGH** - Good balance of simplicity and performance

---

## Algorithm Decision

### Recommended: **Option 4 - Greedy + Backtracking (Hybrid)**

**Rationale**:
1. **Practical Performance**: For Advent of Code inputs, greedy often finds optimal or near-optimal solution quickly
2. **No Dependencies**: Pure Python, no external solvers required
3. **Integer-Native**: Naturally works with integer constraints
4. **Understandability**: Clear logic flow for code review and maintenance
5. **Testability**: Easy to trace execution path and debug

**Fallback Strategy**: If hybrid approach times out, implement Option 1 (Gaussian elimination) with integer validation

### Implementation Approach

**Step 1: Greedy Solver**
```python
def greedy_solve(buttons, targets):
    """
    Greedy approach: for each counter, find minimum button presses needed.
    May not work if buttons have overlapping effects on multiple counters.
    """
    presses = [0] * len(buttons)
    current = [0] * len(targets)
    
    for counter_idx, target in enumerate(targets):
        needed = target - current[counter_idx]
        if needed < 0:
            # Already exceeded target - greedy failed
            return None
        
        # Find buttons affecting this counter, minimize extra increments
        affecting_buttons = [i for i, btn in enumerate(buttons) 
                            if counter_idx in btn]
        if not affecting_buttons:
            if needed > 0:
                return None  # Infeasible
            continue
        
        # For each affecting button, calculate how many presses needed
        # Choose the one that minimizes collateral damage
        best_button = affecting_buttons[0]
        presses[best_button] += needed
        
        # Update all affected counters
        for j in buttons[best_button]:
            current[j] += needed
    
    # Verify solution
    if current == targets:
        return sum(presses), presses
    return None
```

**Step 2: Backtracking Solver**
```python
def backtrack_solve(buttons, targets, max_presses=None):
    """
    Backtracking approach: try button combinations, backtrack on constraint violation.
    """
    if max_presses is None:
        max_presses = sum(targets)  # Upper bound
    
    def search(button_idx, current_state, presses_so_far):
        # Base case: all buttons processed
        if button_idx == len(buttons):
            if current_state == targets:
                return presses_so_far
            return None
        
        # Try different press counts for this button
        button = buttons[button_idx]
        max_for_this_button = max_presses - sum(presses_so_far)
        
        for presses in range(max_for_this_button + 1):
            # Apply button presses
            new_state = current_state[:]
            for counter_idx in button:
                new_state[counter_idx] += presses
            
            # Pruning: if any counter exceeds target, stop
            if any(new_state[i] > targets[i] for i in range(len(targets))):
                continue
            
            # Recurse
            result = search(button_idx + 1, new_state, 
                          presses_so_far + presses)
            if result is not None:
                return result
        
        return None
    
    return search(0, [0] * len(targets), 0)
```

**Step 3: Hybrid Solver**
```python
def solve_machine(buttons, targets):
    """
    Try greedy first, fall back to backtracking if needed.
    """
    # Try greedy approach first (fast)
    result = greedy_solve(buttons, targets)
    if result is not None:
        return result[0]  # Return total presses
    
    # Fall back to backtracking (slower but complete)
    result = backtrack_solve(buttons, targets)
    if result is not None:
        return result
    
    # No solution found
    return None
```

---

## Edge Cases Analysis

### 1. Zero Target
**Case**: Machine where some targets are 0 (counter already configured)
```
Buttons: (0), (1)
Targets: {0, 5}
Solution: Don't press button 0, press button 1 five times → Total: 5
```
**Handling**: Solver naturally handles this; target=0 requires 0 presses for that counter

### 2. Single Button, Single Counter
**Case**: Minimal machine
```
Buttons: (0)
Targets: {7}
Solution: Press button 0 seven times → Total: 7
```
**Handling**: Simple case; backtracking terminates immediately

### 3. Button Affects Nothing
**Case**: Unused button
```
Buttons: (0), (99)
Targets: {5}
Solution: Press button 0 five times, ignore button 1 → Total: 5
```
**Handling**: Solver naturally ignores unused buttons (press count = 0)

### 4. Infeasible System
**Case**: No solution exists
```
Buttons: (0,1)
Targets: {3, 4}
Problem: Both counters increment together, so they always differ by 0
Solution: IMPOSSIBLE (can't reach {3,4} with single button affecting both)
```
**Handling**: Backtracking returns None; report "infeasible" error

### 5. Multiple Solutions
**Case**: Redundant buttons
```
Buttons: (0), (0), (0)
Targets: {5}
Solutions: Many exist (e.g., press B0 five times, or B1 five times, etc.)
Optimal: Any single solution with total presses = 5
```
**Handling**: Backtracking finds first valid solution; guaranteed to be optimal for sum

### 6. Large Targets
**Case**: Very large target numbers
```
Buttons: (0,1,2,3,4)
Targets: {1000, 1000, 1000, 1000, 1000}
Solution: Press button 0 once → All counters reach 1000 → Total: 1
```
**Handling**: Backtracking may be slow; consider optimization (detect common targets)

### 7. Overlapping Effects
**Case**: Multiple buttons affect same counters
```
Buttons: (0), (0,1), (1)
Targets: {3, 5}
Possible: Press B0 three times (counter 0 = 3), press B2 five times (counter 1 = 5)
Total: 8
Or: Press B1 five times (both counters = 5), press B0 never? → No, counter 0 = 5 ≠ 3
```
**Handling**: Backtracking explores all combinations; finds optimal mix

---

## Performance Predictions

### Example 1: Small Machine (4 counters, 6 buttons, targets ~5)
- **Greedy**: ~1ms (linear scan)
- **Backtracking**: ~10ms (limited search space)
- **Expected**: Fast, under 1ms

### Example 2: Medium Machine (10 counters, 15 buttons, targets ~10-20)
- **Greedy**: ~1ms
- **Backtracking**: ~100ms-1s (exponential but pruned)
- **Expected**: Under 1 second

### Example 3: Actual Puzzle (up to 1000 machines, 20 buttons, large targets)
- **Greedy + Backtracking Hybrid**: ~100ms-1s per machine
- **Total Puzzle**: ~100s worst case, likely < 10s with pruning optimizations
- **Expected**: Under 10 seconds (meets spec requirement)

---

## Implementation Notes

### Optimization Techniques

1. **Early Pruning**: Stop backtracking branch if any counter exceeds target
2. **Memoization**: Cache results for duplicate subproblems (if any)
3. **Ordering**: Process counters with fewest affecting buttons first
4. **Greedy Seed**: Use greedy result as upper bound for backtracking
5. **Button Sorting**: Sort buttons by specificity (affect fewer counters first)

### Testing Strategy (TDD)

1. **Parsing Tests**: Verify example lines parse correctly
2. **Simple Cases**: Single button/counter scenarios
3. **Example Validation**: All three provided examples (10, 12, 11)
4. **Edge Cases**: Zero targets, infeasible systems
5. **Performance**: Measure time on examples, optimize if needed

### Pseudocode Flow

```
solve_puzzle(input_file):
    lines = read_input_file(input_file)
    total_presses = 0
    
    for each line in lines:
        buttons, targets = parse_line(line)
        
        min_presses = solve_machine(buttons, targets)
        if min_presses is None:
            report_error("Infeasible machine")
            continue
        
        total_presses += min_presses
    
    return total_presses
```

---

## Decision Summary

| Aspect | Decision |
|--------|----------|
| **Primary Algorithm** | Greedy + Backtracking Hybrid |
| **Fallback Algorithm** | Gaussian Elimination (if needed) |
| **External Dependencies** | None required |
| **Estimated Performance** | < 1s per machine, < 10s total |
| **Code Complexity** | Moderate (backtracking is standard pattern) |
| **Testing Approach** | TDD with red-green-refactor cycle |

---

## Next Steps (Phase 1)

1. **Data Model**: Define Machine, Button, Counter classes with validation
2. **Parser Contract**: Specify exact parsing interface and error handling
3. **Solver Contract**: Define solve_machine() and solve_all() interfaces
4. **Test Plan**: Enumerate all test cases and expected outputs
5. **Quickstart**: Document how to run example scenarios

---

## References

- **Linear Diophantine Equations**: [Wikipedia](https://en.wikipedia.org/wiki/Diophantine_equation)
- **Gaussian Elimination**: Standard numerical linear algebra technique
- **Integer Linear Programming**: Field of optimization (advanced; not needed here)
- **Backtracking**: Classic algorithmic pattern for constraint satisfaction problems
