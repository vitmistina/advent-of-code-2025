# Research: Day 7 Part 1 - Tachyon Beam Split Counter

**Feature**: [spec.md](../spec.md)
**Created**: 2025-12-09

## Beam Simulation Algorithm

### Decision: Queue-based BFS with state tracking

**Rationale**:

- BFS ensures all beams are processed level-by-level (row-by-row in this case)
- Queue allows easy management of multiple active beams
- State tracking (visited set) prevents infinite loops and duplicate processing

**Implementation approach**:

1. Parse grid and find starting position 'S'
2. Initialize queue with starting beam at (row=0, col=S_position, direction=DOWN)
3. Use a set to track visited states: `(row, col, direction)` to prevent reprocessing
4. While queue not empty:
   - Dequeue beam
   - If state already visited, skip (beam merge)
   - Mark state as visited
   - Move beam in its direction
   - If out of bounds, discard beam
   - If empty space '.', continue moving
   - If splitter '^', increment split count, emit two new beams (LEFT and RIGHT)
5. Return total split count

**Alternatives considered**:

- Recursive simulation: More complex to manage multiple beams, harder to debug
- Grid marking: Would require multiple passes and complicate merge detection

## Beam Merging Strategy

### Decision: Use (row, col, direction) tuple as state key

**Rationale**:

- Two beams at the same position moving in the same direction are functionally identical
- Using a visited set with (row, col, direction) tuples automatically handles merging
- When a duplicate state is encountered, skip processing (beam already handled)
- This prevents double-counting splits from merged beams

**Critical insight**:
The puzzle description shows that when two splitters create beams that occupy the same space, they count as separate splits (2) but create only 3 beams total (middle is shared). The visited set approach naturally handles this:

- Splitter 1: creates left beam (unique), middle beam (new)
- Splitter 2: creates middle beam (duplicate, skipped), right beam (unique)
- Split count = 2, active beams = 3 (left, middle, right)

**Example from puzzle**:

```
......^.^......
```

Two splitters, each counts as 1 split = 2 total splits
But they create only 3 distinct beams (left, middle, right) because middle is shared.

## Direction Representation

### Decision: Use cardinal directions with delta tuples

**Rationale**:

- Simple and clear representation
- Easy to calculate next position: `next_pos = (row + dr, col + dc)`

**Implementation**:

```python
DOWN = (1, 0)   # Tachyon beams always start moving down
LEFT = (0, -1)  # Emitted from splitter
RIGHT = (0, 1)  # Emitted from splitter
```

Note: We only need three directions for this puzzle (DOWN, LEFT, RIGHT). No UP direction needed.

## Split Counting

### Decision: Increment counter each time a splitter is encountered

**Rationale**:

- Each splitter encounter represents one split event
- Count increments when beam hits '^', regardless of whether emitted beams merge later
- Merged beams don't affect the split count of their origin

**Clarification**:

- If 2 splitters are hit, split count = 2 (even if resulting beams merge)
- Merging affects beam propagation, not split counting
- Each splitter can only be counted once per unique beam encounter

## Edge Cases

### No splitters in grid

- Expected behavior: split count = 0
- Beam travels downward until it exits the grid
- No special handling needed

### Overlapping beams

- Expected behavior: Merge beams with same (row, col, direction)
- Implementation: Visited set automatically handles this
- Merged beams can trigger further splits downstream

### All splitters in one row

- Expected behavior: Multiple splits in same row, beams continue downward
- Implementation: Queue processes all beams at current level before moving to next

## Best Practices from Prior AoC Solutions

### Grid parsing

- Read file as lines, strip whitespace
- Convert to list of strings for easy indexing: `grid[row][col]`
- Find starting position 'S' during parsing

### Testing strategy

- Unit tests for individual splitter encounters
- Integration test with provided example (test_input.txt → 21 splits)
- Edge case tests for boundary conditions

### Performance considerations

- For typical AoC inputs (grid size ~100x100), performance is not a concern
- Visited set prevents exponential blowup from beam multiplication
- Queue-based approach is O(rows × cols × directions) worst case

## Summary

The solution uses a **queue-based BFS** with a **visited state set** to:

1. Simulate multiple beams moving through the grid
2. Automatically merge duplicate beams (same position + direction)
3. Count each splitter encounter as one split
4. Handle overlapping beams without double-counting splits

This approach is simple, correct, and efficient for the problem constraints.
