# Research: Day 4 Part 1 - Accessible Paper Rolls Counter

**Feature**: Count accessible paper rolls on a grid  
**Date**: 2025-12-04  
**Status**: Complete

## Research Tasks

### 1. Grid Representation in Python

**Decision**: Use list of strings for grid representation

**Rationale**:

- Input is naturally string-based (lines from file)
- Direct character access via `grid[row][col]`
- Minimal memory overhead
- Common pattern in Advent of Code solutions
- Immutable strings prevent accidental modification

**Alternatives Considered**:

- 2D list of characters: Extra overhead from splitting strings into lists
- NumPy array: Overkill for this problem size, adds external dependency
- Dict with (row, col) keys: More memory, slower access for dense grids

**Implementation Notes**:

```python
# Read grid from file
grid = [line.strip() for line in input_data.strip().split('\n')]
# Access: grid[row][col]
```

---

### 2. Adjacency Direction Iteration

**Decision**: Use direction offset tuples for 8-directional traversal

**Rationale**:

- Clear, explicit representation of all 8 directions
- Easy to iterate through all neighbors with single loop
- Self-documenting code with named directions
- Standard pattern in grid-based algorithms

**Alternatives Considered**:

- Nested loops with offsets (-1, 0, 1): Less clear, requires filtering out (0, 0)
- Individual if statements for each direction: Repetitive, harder to maintain
- Complex mathematical formulas: Less readable

**Implementation Notes**:

```python
DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),  # NW, N, NE
    (0, -1),           (0, 1),    # W,     E
    (1, -1),  (1, 0),  (1, 1)     # SW, S, SE
]

for dr, dc in DIRECTIONS:
    new_row, new_col = row + dr, col + dc
    # Check bounds and content
```

---

### 3. Boundary Checking Strategy

**Decision**: Check bounds before accessing grid

**Rationale**:

- Prevents IndexError exceptions
- Clear intent in code
- Efficient - single condition check
- Pythonic approach for 2D grid access

**Alternatives Considered**:

- Try/except for IndexError: Exception handling is slower than conditional checks
- Pad grid with border: Extra memory, complicates input processing
- Separate edge/corner logic: Code duplication, harder to maintain

**Implementation Notes**:

```python
def is_valid_position(grid, row, col):
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])

def count_adjacent_rolls(grid, row, col):
    count = 0
    for dr, dc in DIRECTIONS:
        new_row, new_col = row + dr, col + dc
        if is_valid_position(grid, new_row, new_col):
            if grid[new_row][new_col] == '@':
                count += 1
    return count
```

---

### 4. Test-Driven Development Approach

**Decision**: Use pytest with example grid test cases

**Rationale**:

- Constitution requires TDD (Principle IV - NON-NEGOTIABLE)
- Feature spec provides detailed test scenario with expected output (13 accessible rolls)
- pytest is project standard
- Example includes visual representation for validation

**Test Structure**:

1. **RED Phase**: Test with example grid expecting 13 accessible rolls
2. **GREEN Phase**: Implement functions to pass test
3. **REFACTOR Phase**: Optimize if needed while maintaining green tests

**Implementation Notes**:

```python
# test_solution.py
def test_example_grid():
    input_data = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""

    result = solve_part1(input_data)
    assert result == 13
```

---

### 5. Performance Considerations

**Decision**: Simple iteration without optimization initially

**Rationale**:

- Typical AoC grid sizes are manageable (< 1000x1000)
- Premature optimization violates TDD principles
- Green phase focuses on correctness
- Refactor phase can optimize if needed
- Constitution specifies <1 second for typical sizes - easily achievable

**Alternatives Considered**:

- Pre-compute all roll positions: Minor benefit for simple counting
- Use sets for O(1) lookup: Unnecessary for small grids
- Parallel processing: Overkill for problem size

**Complexity Analysis**:

- Grid parsing: O(rows \* cols)
- For each roll, check 8 neighbors: O(rolls \* 8) = O(rolls)
- Total: O(rows \* cols) which is acceptable for typical puzzle inputs

---

## Summary

All technical decisions are clear and aligned with:

- Constitution principles (TDD, clean code, Python 3.10+)
- Feature requirements (grid processing, adjacency counting, accessibility determination)
- Project standards (pytest, PEP8, function-based solutions)

No blockers identified. Ready to proceed to Phase 1 (Design).
