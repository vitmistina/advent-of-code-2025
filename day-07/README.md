# Day 7 Part 1: Tachyon Beam Split Counter

## Problem Description

A tachyon beam enters a manifold diagram at the location marked `S`, always moving downward. The beam passes freely through empty space (`.`). When a beam encounters a splitter (`^`), the beam stops and two new beams are emitted:

- One continuing downward from the column to the left of the splitter
- One continuing downward from the column to the right of the splitter

The task is to count the total number of times a beam is split by splitter characters.

## Solution Approach

The solution uses a **queue-based BFS algorithm** with state tracking:

1. **Beam Representation**: Each beam is represented as a tuple `(row, col, direction)`.
2. **Direction Constants**:
   - `DOWN = (1, 0)`: Beams always start moving downward and continue downward after splitting
3. **Visited State Set**: Track `(row, col, direction)` tuples to prevent reprocessing identical states.
   - When a duplicate state is encountered, the beams have merged and we skip processing
   - This prevents double-counting splits and handles overlapping beams correctly
4. **Split Counting**: Each time a splitter (`^`) is encountered, the split count is incremented by 1.
5. **Algorithm**:
   - Initialize queue with starting beam at `S` moving `DOWN`
   - While queue is not empty:
     - Dequeue beam
     - Skip if state was already visited (beam merging)
     - Mark state as visited
     - Move beam one step in its direction
     - Check the new cell:
       - `.` or `S`: Continue in same direction
       - `^`: Increment split count, emit left and right beams
       - Out of bounds: Discard beam

## Implementation Files

- `solution.py`: Main solution with `parse_grid()`, `simulate_beams()`, and `count_splits()` functions
- `test_solution.py`: Unit and integration tests using unittest
  - Integration test with `test_input.txt` (expects 21 splits)
  - Edge case tests (no splitters, single splitters, merged beams)
  - Beam merging verification

## Running the Solution

### From the root directory:

```bash
python -m day-07.solution
```

### From day-07 directory:

```bash
python solution.py        # Requires relative path adjustments
python test_solution.py   # Run tests
```

## Results

- **Test Input**: 21 splits ✓
- **Main Input**: 1546 splits

## Key Insights

1. **Beam Merging**: When two beams have the same `(row, col, direction)`, they are functionally identical and merge into one. Using a visited set automatically handles this.

2. **Split Counting vs. Beam Count**: Two splitters that each emit a left and right beam might create only 3 distinct beams if the middle beams overlap. However, each splitter still counts as 1 split.

3. **Downward Direction**: After a splitter, beams continue moving `DOWN` from their new column positions, not horizontally.

4. **Performance**: The visited state set prevents exponential growth. Time complexity is O(rows × cols × directions) = O(rows × cols) since we only have one direction (DOWN).
