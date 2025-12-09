# API Contracts: Day 7 Part 1 - Tachyon Beam Split Counter

**Feature**: [spec.md](../spec.md)
**Created**: 2025-12-09

## Module: solution.py

### Function: parse_grid

**Purpose**: Parse input file into grid structure

**Input**:

- `filename: str` - Path to input file (e.g., "test_input.txt", "input.txt")

**Output**:

- `grid: list[str]` - List of strings, each representing one row
- `start_pos: tuple[int, int]` - (row, col) position of 'S'

**Behavior**:

- Read file and strip whitespace from each line
- Locate position of 'S' character
- Return grid and starting position

**Example**:

```python
grid, start_pos = parse_grid("test_input.txt")
# grid = [".......S.......", "...............", ".......^.......", ...]
# start_pos = (0, 7)
```

---

### Function: simulate_beams

**Purpose**: Simulate beam movement and splitting, count total splits

**Input**:

- `grid: list[str]` - The manifold diagram
- `start_pos: tuple[int, int]` - Starting position (row, col)

**Output**:

- `split_count: int` - Total number of beam splits

**Behavior**:

- Initialize queue with starting beam at `start_pos` with direction DOWN
- Initialize visited set (empty) and split counter (0)
- While queue is not empty:
  - Dequeue beam (row, col, direction)
  - If (row, col, direction) in visited, continue (merged beam)
  - Add (row, col, direction) to visited
  - Calculate next position: (row + dr, col + dc)
  - If next position out of bounds, continue
  - Get cell at next position:
    - If '.' or 'S': enqueue beam with same direction at next position
    - If '^': increment split_count, enqueue LEFT beam and RIGHT beam
- Return split_count

**Example**:

```python
split_count = simulate_beams(grid, (0, 7))
# Returns: 21 (for test_input.txt)
```

---

### Function: count_splits

**Purpose**: Main entry point - parse and simulate in one call

**Input**:

- `filename: str` - Path to input file

**Output**:

- `split_count: int` - Total number of beam splits

**Behavior**:

- Call `parse_grid(filename)` to get grid and start position
- Call `simulate_beams(grid, start_pos)` to get split count
- Return split count

**Example**:

```python
result = count_splits("test_input.txt")
print(result)  # Output: 21
```

---

## Module: test_solution.py

### Test: test_example_input

**Purpose**: Integration test using provided example

**Input**: test_input.txt

**Expected Output**: 21

**Assertion**:

```python
assert count_splits("day-07/test_input.txt") == 21
```

---

### Test: test_no_splitters

**Purpose**: Edge case test with no splitters

**Input**: Grid with only 'S' and '.' characters

**Expected Output**: 0

**Assertion**:

```python
grid_no_splitters = ["...S...", ".......", "......."]
# Create temp file or mock
assert simulate_beams(grid_no_splitters, (0, 3)) == 0
```

---

### Test: test_single_split

**Purpose**: Unit test for single splitter

**Input**: Grid with one splitter below 'S'

**Expected Output**: 1

**Assertion**:

```python
grid_single = ["...S...", "...^..."]
assert simulate_beams(grid_single, (0, 3)) == 1
```

---

### Test: test_merged_beams

**Purpose**: Test that merged beams don't double-count splits

**Input**: Grid where two splitters create overlapping beams

**Expected Output**: 2 (two splits, even though middle beam is shared)

**Assertion**:

```python
grid_merged = [
    "...S...",
    ".......",
    "..^.^..",
]
assert simulate_beams(grid_merged, (0, 3)) == 2
```

---

## Data Structures

### Beam Queue Item

**Type**: `tuple[int, int, tuple[int, int]]`

**Structure**: `(row, col, (delta_row, delta_col))`

**Example**: `(2, 7, (1, 0))` represents beam at row 2, col 7, moving DOWN

---

### Visited State

**Type**: `set[tuple[int, int, tuple[int, int]]]`

**Structure**: Set of `(row, col, (delta_row, delta_col))` tuples

**Example**: `{(0, 7, (1, 0)), (1, 7, (1, 0)), (2, 7, (1, 0))}`

---

## Constants

```python
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
```

---

## Input/Output Format

### Input File Format

- Plain text file
- Each line represents one row of the grid
- Characters: 'S' (start), '^' (splitter), '.' (empty)
- Exactly one 'S' per file
- All lines same length

### Output Format

- Single integer
- Represents total number of beam splits
- Printed to stdout or returned from function

---

## Error Handling

**Not required** for this implementation (per user clarification):

- Missing 'S' character
- Invalid characters
- Malformed input

**Assumptions**:

- Input is well-formed
- Exactly one 'S' exists
- Only valid characters present
