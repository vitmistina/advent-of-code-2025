# Data Model: Day 4 Part 2 - Printing Department

**Date**: 2025-12-04  
**Feature**: Day 4 Part 2 - Iterative Removal Algorithm

## Overview

The Part 2 solution extends Part 1's grid representation with an optimized tracking structure for efficient iterative removal of accessible paper rolls.

---

## Entities

### RollPosition (Implicit)

A coordinate pair representing a paper roll's location in the grid.

**Type**: `tuple[int, int]`

**Fields**:

- `row: int` — Zero-indexed row position (0 = top)
- `col: int` — Zero-indexed column position (0 = left)

**Validation Rules**:

- Both row and col must be non-negative integers
- Position must be within grid boundaries (validated during parsing)
- Position must contain `@` character in original grid

**State Transitions**:

```
PRESENT → REMOVED (when roll becomes accessible and is removed)
```

**Example**:

```python
pos = (0, 2)  # Row 0, Column 2
```

---

### RollTracker (Primary Data Structure)

A dictionary mapping roll positions to their current neighbor counts, enabling O(1) access, removal, and update operations.

**Type**: `dict[tuple[int, int], int]`

**Structure**:

- **Key**: `RollPosition` — (row, col) tuple
- **Value**: `int` — Count of adjacent paper rolls (0-8)

**Invariants**:

1. All keys correspond to positions that currently contain paper rolls
2. All values are in range [0, 8]
3. A roll with count < 4 is "accessible" and eligible for removal
4. Neighbor counts accurately reflect current state (updated after each removal)

**Operations**:

- **Initialize**: Populate from grid with all `@` positions and their neighbor counts
- **Filter**: Extract accessible rolls (`count < 4`)
- **Remove**: Delete roll from dictionary
- **Update**: Decrement neighbor counts when adjacent roll is removed

**Example**:

```python
rolls = {
    (0, 2): 1,  # Roll at (0,2) has 1 neighbor
    (0, 3): 2,  # Roll at (0,3) has 2 neighbors
    (1, 0): 0,  # Roll at (1,0) has 0 neighbors (isolated)
    (1, 3): 4,  # Roll at (1,3) has 4 neighbors (not accessible)
}

accessible = {pos for pos, count in rolls.items() if count < 4}
# Result: {(0,2), (0,3), (1,0)}
```

---

### AccessibleSet (Derived)

A set of positions representing rolls that can currently be removed (< 4 neighbors).

**Type**: `set[tuple[int, int]]`

**Derivation**:

```python
accessible = {pos for pos, count in rolls.items() if count < 4}
```

**Properties**:

- Recomputed at the start of each iteration
- Empty set triggers termination condition
- All positions in set are removed in the same iteration

**Lifecycle**:

```
1. Derive accessible set from RollTracker
2. If empty → TERMINATE
3. Remove all rolls in set from RollTracker
4. Update neighbor counts for affected positions
5. Repeat from step 1
```

---

## Relationships

```
Grid (input string)
    ↓ parse_grid()
List[str] (rows)
    ↓ initialization loop
RollTracker (dict)
    ↓ iteration
AccessibleSet (set)
    ↓ removal
RollTracker (updated)
```

**Flow**:

1. **Parse**: Grid string → list of row strings
2. **Initialize**: For each `@` in grid → create RollTracker entry with neighbor count
3. **Iterate**: While accessible rolls exist:
   - Derive AccessibleSet from RollTracker
   - Remove accessible rolls from RollTracker
   - Update neighbor counts for affected positions
4. **Return**: Total count of removed rolls

---

## Data Transformations

### Initialization

```python
grid = parse_grid(input_data)  # List[str]
rolls: dict[tuple[int, int], int] = {}

for row, row_str in enumerate(grid):
    for col, val in enumerate(row_str):
        if val == "@":
            neighbor_count = count_adjacent_rolls(grid, row, col)
            rolls[(row, col)] = neighbor_count
```

### Accessibility Check

```python
accessible = {pos for pos, count in rolls.items() if count < 4}
```

### Removal and Update

```python
for pos in accessible:
    del rolls[pos]
    row, col = pos

    # Update 8 surrounding positions
    for dr, dc in DIRECTIONS:
        neighbor_pos = (row + dr, col + dc)
        if neighbor_pos in rolls:
            rolls[neighbor_pos] -= 1

total_removed += len(accessible)
```

---

## Validation Rules

### At Initialization

- Grid must be rectangular (validated by `parse_grid()`)
- All neighbor counts must be in range [0, 8]
- Roll positions must correspond to `@` characters

### During Iteration

- Neighbor count must never go negative (ensured by only decrementing when neighbor exists)
- Accessible set must be empty to terminate (prevents infinite loop)
- Each iteration must remove at least one roll when accessible set is non-empty (guaranteed by problem constraints)

### At Termination

- All remaining rolls must have count ≥ 4
- Total removed count must equal initial roll count minus remaining roll count

---

## Example Walkthrough

### Initial State

```
Grid:
@.@
...
@.@

RollTracker:
{
    (0, 0): 0,  # No neighbors
    (0, 2): 0,  # No neighbors
    (2, 0): 0,  # No neighbors
    (2, 2): 0,  # No neighbors
}

AccessibleSet: {(0,0), (0,2), (2,0), (2,2)}
```

### After Iteration 1

```
RollTracker: {}  # All removed
AccessibleSet: {}  # Empty → terminate

Total removed: 4
```

### Complex Example (from problem)

```
Initial: 13 accessible rolls
Iteration 1: Remove 13 → 12 newly accessible
Iteration 2: Remove 12 → 7 newly accessible
Iteration 3: Remove 7 → 5 newly accessible
Iteration 4: Remove 5 → 2 newly accessible
Iteration 5: Remove 2 → 1 newly accessible
Iteration 6: Remove 1 → 1 newly accessible
Iteration 7: Remove 1 → 1 newly accessible
Iteration 8: Remove 1 → 0 accessible
Total: 43 removed
```

---

## Memory Complexity

- **Grid**: O(R × C) where R = rows, C = columns
- **RollTracker**: O(N) where N = number of rolls (subset of R × C)
- **AccessibleSet**: O(K) where K = accessible rolls in current iteration (K ≤ N)
- **Total**: O(R × C) dominated by grid storage

**Optimization**: After initialization, grid is not modified, only RollTracker shrinks over iterations.
