# Quickstart Guide: Day 7 Part 1 - Tachyon Beam Split Counter

**Feature**: [spec.md](../spec.md)
**Created**: 2025-12-09

## Overview

This guide helps you implement and test the Day 7 Part 1 solution for counting tachyon beam splits in a manifold diagram.

## Prerequisites

- Python 3.x installed
- Input files in `day-07/` directory:
  - `test_input.txt` (provided example, expects 21 splits)
  - `input.txt` (your AoC puzzle input)

## Project Structure

```
day-07/
├── solution.py          # Main solution logic
├── test_solution.py     # Unit and integration tests
├── test_input.txt       # Example input (21 splits expected)
├── input.txt           # Your puzzle input
└── README.md           # Documentation
```

## Implementation Steps

### Step 1: Create solution.py

Create the main solution file with three key functions:

1. **parse_grid(filename)**: Read input file and find 'S'
2. **simulate_beams(grid, start_pos)**: Run beam simulation, count splits
3. **count_splits(filename)**: Main entry point

### Step 2: Implement Core Algorithm

Use a queue-based BFS approach:

```python
from collections import deque

DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

def simulate_beams(grid, start_pos):
    queue = deque([(start_pos[0], start_pos[1], DOWN)])
    visited = set()
    split_count = 0

    while queue:
        row, col, direction = queue.popleft()

        # Skip if already processed (beam merging)
        if (row, col, direction) in visited:
            continue
        visited.add((row, col, direction))

        # Move beam
        dr, dc = direction
        new_row, new_col = row + dr, col + dc

        # Check bounds
        if not (0 <= new_row < len(grid) and 0 <= new_col < len(grid[0])):
            continue

        cell = grid[new_row][new_col]

        if cell == '.' or cell == 'S':
            # Continue in same direction
            queue.append((new_row, new_col, direction))
        elif cell == '^':
            # Split! Count it and emit two beams
            split_count += 1
            queue.append((new_row, new_col, LEFT))
            queue.append((new_row, new_col, RIGHT))

    return split_count
```

### Step 3: Create Tests

Create `test_solution.py`:

```python
from solution import count_splits, simulate_beams

def test_example_input():
    """Integration test with provided example"""
    result = count_splits("day-07/test_input.txt")
    assert result == 21, f"Expected 21, got {result}"

def test_no_splitters():
    """Edge case: no splitters"""
    grid = ["...S...", ".......", "......."]
    result = simulate_beams(grid, (0, 3))
    assert result == 0, f"Expected 0, got {result}"

def test_single_split():
    """Unit test: one splitter"""
    grid = ["...S...", "...^..."]
    result = simulate_beams(grid, (0, 3))
    assert result == 1, f"Expected 1, got {result}"

if __name__ == "__main__":
    test_example_input()
    test_no_splitters()
    test_single_split()
    print("All tests passed!")
```

### Step 4: Run Tests

```bash
# Run integration test
python day-07/test_solution.py

# Expected output: "All tests passed!"
```

### Step 5: Solve Main Puzzle

```bash
# Run on main input
python -c "from day-07.solution import count_splits; print(count_splits('day-07/input.txt'))"

# Or add a main block to solution.py:
if __name__ == "__main__":
    result = count_splits("day-07/input.txt")
    print(f"Answer: {result}")
```

## Key Implementation Notes

### Beam Merging

- Use `(row, col, direction)` tuple as state key
- Add to visited set before processing
- Skip if already visited (automatic merging)

### Split Counting

- Increment counter when beam encounters '^'
- Each splitter = 1 split, regardless of beam merging
- Two splitters creating overlapping beams = 2 splits (not 3)

### Direction Handling

- Beams always start moving DOWN from 'S'
- Splitters emit LEFT and RIGHT beams (not up or down)
- Use delta tuples for easy position calculation

## Testing Checklist

- [ ] Integration test passes (test_input.txt → 21)
- [ ] No splitters returns 0
- [ ] Single splitter returns 1
- [ ] Merged beams don't double-count splits
- [ ] Solution works on main input.txt

## Troubleshooting

### Wrong split count on test input

- Check that you're incrementing split_count only when hitting '^'
- Verify beam merging logic (visited set)
- Ensure beams are emitted LEFT and RIGHT from splitter position (not from next position)

### Infinite loop or very slow

- Ensure you're checking visited set before processing
- Verify bounds checking is correct
- Check that beams exit when out of bounds

### Off-by-one errors

- Remember: beams move THEN check cell (or check cell THEN emit)
- Be consistent with whether splitter position is included in visited set

## Success Criteria

✓ test_input.txt returns 21
✓ Main input.txt returns correct answer for AoC submission
✓ All unit tests pass
✓ Code is clean and readable

## Next Steps

After completing Day 7 Part 1:

1. Submit answer to Advent of Code
2. Proceed to Day 7 Part 2 (if available)
3. Document any interesting insights or optimizations
