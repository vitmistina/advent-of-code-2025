# Function Contract: Day 4 Part 1 Solution

**Feature**: Accessible Paper Rolls Counter  
**Version**: 1.0  
**Date**: 2025-12-04

## Overview

This contract defines the public interface for the Day 4 Part 1 solution. All functions follow type-hinted Python signatures and include comprehensive docstrings.

---

## Primary Interface

### `solve_part1(input_data: str) -> int`

**Description**: Main entry point for solving Day 4 Part 1 puzzle

**Purpose**: Count the number of accessible paper rolls in a warehouse grid

**Parameters**:

- `input_data` (str): Multiline string containing the grid representation
  - Each line represents a row
  - '@' character represents a paper roll
  - '.' character represents empty space
  - Lines may have leading/trailing whitespace (will be stripped)

**Returns**:

- `int`: Total count of accessible paper rolls
  - A paper roll is accessible if it has fewer than 4 adjacent paper rolls
  - Adjacent means any of the 8 surrounding positions (N, NE, E, SE, S, SW, W, NW)

**Raises**:

- No exceptions expected for valid input
- Invalid input behavior: undefined (not part of puzzle requirements)

**Examples**:

```python
# Example 1: Small grid
input_data = """..@@.
@@@.@"""
result = solve_part1(input_data)
# Returns: count of accessible rolls

# Example 2: Provided test case
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
# Returns: 13
```

**Performance**:

- Time Complexity: O(rows × cols) where rows and cols are grid dimensions
- Space Complexity: O(rows × cols) for grid storage
- Expected execution time: < 1 second for typical puzzle inputs

**Dependencies**: Calls internal helper functions defined below

---

## Supporting Functions

### `parse_grid(input_data: str) -> List[str]`

**Description**: Convert input string into grid representation

**Parameters**:

- `input_data` (str): Multiline string with grid data

**Returns**:

- `List[str]`: List of strings, each representing a grid row with whitespace stripped

**Examples**:

```python
input_data = "..@\n.@@\n"
grid = parse_grid(input_data)
# Returns: ["..@", ".@@"]
```

**Contract**:

- Empty input returns empty list
- Each line is stripped of leading/trailing whitespace
- Empty lines are preserved as empty strings

---

### `is_valid_position(grid: List[str], row: int, col: int) -> bool`

**Description**: Check if a position is within grid boundaries

**Parameters**:

- `grid` (List[str]): The grid representation
- `row` (int): Zero-based row index
- `col` (int): Zero-based column index

**Returns**:

- `bool`: True if position is within bounds, False otherwise

**Examples**:

```python
grid = ["..@", ".@@"]
is_valid_position(grid, 0, 0)  # Returns: True
is_valid_position(grid, 1, 2)  # Returns: True
is_valid_position(grid, 2, 0)  # Returns: False (row out of bounds)
is_valid_position(grid, 0, 3)  # Returns: False (col out of bounds)
is_valid_position(grid, -1, 0) # Returns: False (negative row)
```

**Contract**:

- Returns True iff: `0 <= row < len(grid) AND 0 <= col < len(grid[0])`
- Empty grid: Returns False for any position
- Assumes rectangular grid (all rows same length)

---

### `count_adjacent_rolls(grid: List[str], row: int, col: int) -> int`

**Description**: Count paper rolls in the 8 adjacent positions

**Parameters**:

- `grid` (List[str]): The grid representation
- `row` (int): Zero-based row index of center position
- `col` (int): Zero-based column index of center position

**Returns**:

- `int`: Number of adjacent positions containing '@' (range: 0-8)

**Examples**:

```python
grid = [
    "...",
    ".@.",
    "..."
]
count_adjacent_rolls(grid, 1, 1)  # Returns: 0 (no adjacent rolls)

grid = [
    "@@@",
    "@@@",
    "@@@"
]
count_adjacent_rolls(grid, 1, 1)  # Returns: 8 (all positions have rolls)

grid = [
    "..@",
    "@@@"
]
count_adjacent_rolls(grid, 0, 2)  # Returns: 2 (positions (1,1) and (1,2))
```

**Contract**:

- Checks all 8 directions: `[(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]`
- Out-of-bounds positions are not counted (treated as empty)
- Only positions containing '@' are counted
- Does not check the center position itself

**Directions Checked**:

```
NW  N  NE
 W  X  E     (X = center position)
SW  S  SE
```

---

### `is_accessible(adjacent_count: int) -> bool`

**Description**: Determine if a paper roll is accessible based on neighbor count

**Parameters**:

- `adjacent_count` (int): Number of adjacent paper rolls (0-8)

**Returns**:

- `bool`: True if accessible (< 4 neighbors), False otherwise

**Examples**:

```python
is_accessible(0)  # Returns: True
is_accessible(3)  # Returns: True
is_accessible(4)  # Returns: False
is_accessible(8)  # Returns: False
```

**Contract**:

- Returns True iff `adjacent_count < 4`
- Threshold is strictly less than 4 (not less than or equal to)
- Valid input range: 0-8 (from count_adjacent_rolls)

---

## Constants

```python
DIRECTIONS: List[Tuple[int, int]] = [
    (-1, -1), (-1, 0), (-1, 1),  # Northwest, North, Northeast
    (0, -1),           (0, 1),    # West,            East
    (1, -1),  (1, 0),  (1, 1)     # Southwest, South, Southeast
]
```

**Description**: Direction offsets for checking adjacent positions

**Usage**: Add to (row, col) to get adjacent position coordinates

---

## Type Definitions

```python
from typing import List, Tuple

Grid = List[str]
Position = Tuple[int, int]
Direction = Tuple[int, int]
```

---

## Integration Contract

### Command Line Execution

**Expected Usage**:

```bash
uv run day-04/solution.py
```

**Behavior**:

- Reads from `day-04/input.txt`
- Calls `solve_part1(input_data)`
- Prints result to stdout
- Format: "Part 1: {result}"

### Testing Interface

**Test File**: `day-04/test_solution.py`

**Test Function**:

```python
def test_example_grid():
    """Test with provided example expecting 13 accessible rolls."""
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

**Test Execution**:

```bash
uv run pytest day-04/test_solution.py
```

---

## Validation Rules

1. **Input Format**:

   - Must be valid multiline string
   - Each line represents a grid row
   - Only '@' and '.' characters allowed (plus whitespace)

2. **Grid Properties**:

   - Must be rectangular (all rows same length)
   - May be empty (0 rows, 0 columns)
   - No maximum size constraint (performance requirements apply)

3. **Accessibility Criteria**:

   - Threshold: fewer than 4 adjacent rolls (< 4, not <= 4)
   - All 8 directions must be checked
   - Out-of-bounds positions treated as empty

4. **Output**:
   - Non-negative integer
   - Maximum value: total number of '@' characters in grid

---

## Error Handling

**Philosophy**: Advent of Code inputs are well-formed; extensive validation is not required

**Expected Behavior**:

- Valid input: Return correct count
- Empty grid: Return 0
- No paper rolls: Return 0

**Undefined Behavior** (not tested):

- Invalid characters in grid
- Non-rectangular grid
- Negative dimensions

---

## Backward Compatibility

**Version**: 1.0 (initial implementation)

**Future Changes**:

- Part 2 may add `solve_part2(input_data: str) -> int` function
- Core helper functions should remain stable
- Interface changes will increment version number

---

## Examples & Test Cases

### Minimal Test Cases

```python
# Test 1: Empty grid
assert solve_part1("") == 0

# Test 2: Single roll (no neighbors)
assert solve_part1("@") == 1

# Test 3: Single roll with 3 neighbors (accessible)
input_data = """@@
@@"""
# Position (0,0): neighbors (0,1), (1,0), (1,1) = 3 → accessible
# All 4 rolls have 3 neighbors each → all accessible
assert solve_part1(input_data) == 4

# Test 4: Single roll with 4 neighbors (not accessible)
input_data = """@@@
@@@"""
# Center position (0,1): has 5 neighbors → not accessible
# Edge/corner positions: vary between 3-5 neighbors
# Expected: only corners with 3 neighbors are accessible

# Test 5: Provided example
assert solve_part1(EXAMPLE_GRID) == 13
```

---

## References

- Feature Specification: `specs/011-day-04-part-1/spec.md`
- Data Model: `specs/011-day-04-part-1/data-model.md`
- Research Notes: `specs/011-day-04-part-1/research.md`
