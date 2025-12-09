# Data Model: Day 7 Part 1 - Tachyon Beam Split Counter

**Feature**: [spec.md](../spec.md)
**Created**: 2025-12-09

## Entities

### Grid

**Description**: Represents the 2D manifold diagram from the input file.

**Attributes**:

- Rows: List of strings, each representing one row of the grid
- Width: Number of columns (consistent across all rows)
- Height: Number of rows

**Relationships**:

- Contains cells with characters: 'S' (start), '^' (splitter), '.' (empty)

**Validation Rules**:

- Must contain exactly one 'S' (starting position)
- All rows must have the same length
- Only valid characters: 'S', '^', '.'

---

### Beam

**Description**: Represents a tachyon beam moving through the grid.

**Attributes**:

- Position: (row, col) tuple indicating current location
- Direction: (delta_row, delta_col) tuple indicating movement direction

**State Transitions**:

- **Moving**: Beam advances one step in its direction each iteration
- **Splitting**: When beam encounters '^', it stops and creates two new beams (left and right)
- **Exiting**: When beam moves out of grid bounds, it is discarded
- **Merging**: When two beams reach the same (row, col, direction), they merge into one

**Relationships**:

- Originates from starting position 'S' or from a splitter '^'
- Interacts with grid cells (empty space, splitter)

---

### Beam State

**Description**: Unique identifier for a beam's position and direction.

**Attributes**:

- Row: Current row index (0-based)
- Column: Current column index (0-based)
- Direction: Tuple (delta_row, delta_col)

**Purpose**:

- Used as key in visited set to prevent duplicate beam processing
- Enables automatic beam merging when duplicate states are encountered

---

### Split Counter

**Description**: Tracks the total number of beam splits that have occurred.

**Attributes**:

- Count: Integer, incremented each time a beam encounters a splitter

**Validation Rules**:

- Must be non-negative
- Increments by 1 for each splitter encounter
- Not affected by beam merging (splits count even if resulting beams merge)

---

## Direction Constants

**DOWN**: (1, 0) - Beam moves down one row
**LEFT**: (0, -1) - Beam moves left one column
**RIGHT**: (0, 1) - Beam moves right one column

All beams start with direction DOWN from position 'S'.

---

## State Management

### Visited Set

**Description**: Tracks all beam states that have been processed.

**Structure**: Set of (row, col, direction) tuples

**Purpose**:

- Prevents infinite loops
- Automatically handles beam merging
- Ensures each unique beam path is processed exactly once

**Example**:

```
Visited: {(1, 7, DOWN), (3, 7, LEFT), (3, 7, RIGHT), (3, 8, DOWN), ...}
```

### Beam Queue

**Description**: Holds all active beams waiting to be processed.

**Structure**: Queue (FIFO) of (row, col, direction) tuples

**Purpose**:

- Manages multiple simultaneous beams
- Ensures breadth-first processing (level-by-level)

**Example**:

```
Queue: [(4, 6, DOWN), (4, 7, DOWN), (4, 8, DOWN)]
```

---

## Data Flow

1. **Input**: Text file (test_input.txt or input.txt) → Grid
2. **Initialization**: Find 'S' → Create initial beam with direction DOWN
3. **Simulation**:
   - Dequeue beam
   - Check if state in visited set (if yes, skip - beam merged)
   - Add state to visited set
   - Move beam
   - Process cell:
     - '.' or 'S': Continue in same direction
     - '^': Increment split counter, enqueue LEFT and RIGHT beams
     - Out of bounds: Discard beam
4. **Output**: Split counter value (integer)

---

## Example State Evolution

Given input:

```
.......S.......
...............
.......^.......
```

**Initial state**:

- Grid: 3x15
- Start position: (0, 7)
- Queue: [(0, 7, DOWN)]
- Visited: {}
- Split count: 0

**After step 1** (beam at S):

- Queue: [(1, 7, DOWN)]
- Visited: {(0, 7, DOWN)}
- Split count: 0

**After step 2** (beam at empty):

- Queue: [(2, 7, DOWN)]
- Visited: {(0, 7, DOWN), (1, 7, DOWN)}
- Split count: 0

**After step 3** (beam hits splitter):

- Queue: [(2, 6, LEFT), (2, 8, RIGHT)]
- Visited: {(0, 7, DOWN), (1, 7, DOWN), (2, 7, DOWN)}
- Split count: 1 ✓ (first split!)

**Continue** until queue is empty...

---

## Summary

The data model centers on:

- **Grid**: Static 2D structure from input
- **Beam**: Dynamic entity with position and direction
- **State tracking**: Visited set and queue manage beam simulation
- **Split counter**: Simple integer tracking split events

This model supports efficient beam merging through state deduplication and accurate split counting independent of beam merging behavior.
