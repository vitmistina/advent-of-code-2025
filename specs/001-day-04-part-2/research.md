# Research: Day 4 Part 2 - Iterative Removal Algorithm

**Date**: 2025-12-04  
**Feature**: Day 4 Part 2 - Printing Department  
**Context**: Research for optimized iterative removal of accessible paper rolls

## Decision 1: Algorithm Approach

**Decision**: Neighbor-count-bucketed sets with O(1) accessibility lookup

**Rationale**:

- The user specifically requested efficient handling of iterations with memoization/dynamic programming
- Bucketing rolls by neighbor count (0-8) eliminates the O(R) filtering bottleneck present in dictionary-based approaches
- Accessible rolls are simply the union of buckets 0-3 (O(1) lookup instead of O(R) filter)
- When a roll is removed, neighbors move between buckets (O(1) set remove + add operations)
- Complexity: O(K) per iteration where K = rolls removed (only touch removed rolls + their 8K neighbors)
- Previous dictionary approach required O(R) filtering every iteration
- Naive approach: O(R² × I) where I = number of iterations (full grid scan each time)

**Alternatives considered**:

1. **Dictionary-based tracking**: Map position -> neighbor_count, filter for count < 4
   - Rejected: O(R) filtering step every iteration to find accessible rolls
   - Still viable but strictly slower than bucketed approach
2. **Naive grid scanning**: Recreate grid after each removal pass, scan all cells
   - Rejected: O(R² × I) complexity, excessive string/list manipulation overhead
3. **Set-based tracking**: Track only accessible rolls in a set, rebuild set after removals
   - Rejected: Requires full re-scan of all remaining rolls after each iteration
4. **Priority queue**: Use heap to track rolls by neighbor count
   - Rejected: Heap operations are O(log R), and every removal requires updating 8 neighbors' positions in heap (complex)

**Implementation details**:

```python
# Data structure: buckets indexed by neighbor count
by_count: dict[int, set[tuple[int, int]]] = {i: set() for i in range(9)}

# Initial population
for each @ in grid:
    count = count_adjacent_rolls(grid, row, col)
    by_count[count].add((row, col))

# Iterative removal
while by_count[0] or by_count[1] or by_count[2] or by_count[3]:
    # O(1) accessibility check: union of buckets 0-3
    accessible = by_count[0] | by_count[1] | by_count[2] | by_count[3]

    for pos in accessible:
        # Find and remove from current bucket
        for count in range(4):
            if pos in by_count[count]:
                by_count[count].remove(pos)
                break

        # Update neighbors: move each from bucket N to bucket N-1
        for dr, dc in DIRECTIONS:
            neighbor = (pos[0] + dr, pos[1] + dc)
            for old_count in range(1, 9):  # Can't be in bucket 0
                if neighbor in by_count[old_count]:
                    by_count[old_count].remove(neighbor)
                    by_count[old_count - 1].add(neighbor)
                    break

    total_removed += len(accessible)
```

---

## Decision 2: Neighbor Count Update Strategy

**Decision**: Move neighbors between buckets when a roll is removed (set operations)

**Rationale**:

- When a roll at (r, c) is removed, exactly 8 positions might be affected: all 8 adjacent cells
- For each affected neighbor that still exists, move it from bucket N to bucket N-1
- This is O(1) per neighbor: `bucket[N].remove(pos)` + `bucket[N-1].add(pos)`
- Total work per iteration: O(K) where K is rolls removed in that iteration
- Neighbors can only be in buckets 1-8 (if they were in bucket 0, they'd already be removed)
- Maintains correctness: neighbor counts always reflect current grid state

**Alternatives considered**:

1. **Decrement counter in dictionary**: Track position -> count, decrement when neighbor removed
   - Rejected: Still requires O(R) filtering to find accessible rolls each iteration
2. **Full recount after removals**: For each remaining roll, recount all 8 neighbors
   - Rejected: O(R) work per iteration even if only a few rolls removed
3. **Lazy evaluation**: Mark counts as dirty, recount only when needed
   - Rejected: Adds complexity without performance benefit; we need counts for all rolls each iteration

---

## Decision 3: Data Structure for Grid Representation

**Decision**: Convert grid to bucketed sets at initialization, indexed by neighbor count (0-8)

**Rationale**:

- Dictionary of sets provides O(1) accessibility check: just check if buckets 0-3 are non-empty
- Bucket structure maps directly to problem domain: neighbor count determines accessibility
- Removal is O(1) with `bucket[N].remove(pos)`
- Moving between buckets is O(1): remove from one set, add to another
- Existence check is O(1) with `pos in bucket[N]`
- Memory overhead minimal: 9 sets vs full grid representation
- Natural partitioning: accessible rolls (0-3) vs inaccessible rolls (4-8)

**Alternatives considered**:

1. **Single dictionary (position -> count)**: All rolls in one dict, filter for accessible
   - Rejected: Requires O(R) filtering every iteration; no structural advantage
2. **List of lists (mutable grid)**: Convert grid to `list[list[str]]`, modify in place
   - Rejected: Still requires scanning to find all `@` positions; no performance gain
3. **Two sets**: One for all rolls, one for accessible rolls
   - Rejected: Still need neighbor count tracking; would require additional dictionary anyway

---

## Decision 4: Termination Condition

**Decision**: Terminate when all buckets 0-3 are empty (no accessible rolls remain)

**Rationale**:

- Directly implements problem statement: "keep repeating until no new rolls become accessible"
- Natural loop exit: `while by_count[0] or by_count[1] or by_count[2] or by_count[3]`
- Equivalent to: `while by_count[0] | by_count[1] | by_count[2] | by_count[3]`
- Guaranteed termination: each iteration strictly reduces total roll count (accessible sets non-empty before loop continues)
- No risk of infinite loop: worst case all rolls removed, best case stable configuration reached
- Clear semantics: accessible buckets empty = no more removals possible

**Alternatives considered**:

1. **Check accessible set size**: Compute union and check if empty
   - Rejected: Same result but requires set union operation; condition is less direct
2. **Fixed iteration count**: Iterate exactly N times
   - Rejected: Unknown how many iterations needed; risk of under/over-iteration
3. **Check for grid changes**: Compare grid state before/after iteration
   - Rejected: More complex than checking bucket emptiness; same information

---

## Decision 5: Integration with Part 1 Code

**Decision**: Reuse `parse_grid()`, `count_adjacent_rolls()`, and `DIRECTIONS` from Part 1

**Rationale**:

- DRY principle: existing functions already tested and working
- `count_adjacent_rolls()` used only during initialization of neighbor counts
- `DIRECTIONS` constant used for finding neighbor positions during updates
- Maintains consistency with Part 1 solution structure

**Alternatives considered**:

1. **Duplicate functions in Part 2**: Copy parsing/counting logic
   - Rejected: Violates DRY, increases maintenance burden
2. **Refactor into shared module**: Extract common code to separate file
   - Rejected: Over-engineering for AoC; single file per day is standard pattern

---

## Decision 6: Return Value Format

**Decision**: `solve_part2()` returns total removed count (integer)

**Rationale**:

- Problem asks: "How many total rolls of paper could the Elves remove?"
- Part 1 returns count of initially accessible rolls (13 for sample)
- Part 2 returns total removed after all iterations (43 for sample)
- Consistent with existing AoC solution pattern: single integer return

**Alternatives considered**:

1. **Return tuple**: (initial_accessible, total_removed)
   - Rejected: Part 2 only asks for total removed; initial count is Part 1's concern
2. **Return iteration details**: List of counts per iteration
   - Rejected: Problem doesn't ask for this; over-complicates

---

## Best Practices

### Python-specific

- Use `dict[int, set[tuple[int, int]]]` type hints for clarity
- Initialize all buckets 0-8: `{i: set() for i in range(9)}`
- Use set union for accessible check: `by_count[0] | by_count[1] | by_count[2] | by_count[3]`
- Employ tuple unpacking for neighbor iteration: `for dr, dc in DIRECTIONS`
- Leverage set operations: `remove()` and `add()` are O(1)

### Performance

- Minimize grid string operations (convert once to bucketed sets)
- Avoid unnecessary iterations: only check buckets 1-8 when finding neighbors (they can't be in bucket 0)
- O(1) accessibility lookup eliminates O(R) filtering bottleneck
- Early termination when accessible buckets (0-3) are all empty
- Cache neighbor calculations (8-direction offset is constant)

### Testing

- Verify sample case: 13 initial accessible, 43 total removed
- Test edge cases: single roll, all isolated rolls, all clustered rolls
- Validate bucket transitions maintain invariant (neighbor count always accurate)
- Confirm termination (no infinite loops)
- Check bucket integrity: no roll appears in multiple buckets

---

## Summary

The optimized approach uses bucketed sets indexed by neighbor count (0-8), eliminating the O(R) filtering bottleneck present in dictionary-based approaches. Accessible rolls are the union of buckets 0-3 (O(1) lookup), and removing a roll moves its neighbors between buckets via O(1) set operations. This achieves O(K) complexity per iteration (where K is average removals per iteration) compared to naive O(R² × I) full grid scanning or O(R × K) dictionary filtering. The solution reuses Part 1 infrastructure, maintains code clarity, and follows TDD principles.
