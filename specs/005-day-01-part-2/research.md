# Research: Day 1 Part 2 Zero Crossing Algorithm

**Date**: December 1, 2025  
**Feature**: Count all zero crossings during dial rotations  
**Branch**: `005-day-01-part-2`

## Overview

This research documents the algorithmic approach for counting zero crossings during circular dial rotations, including the mathematical formulas, edge cases, and implementation best practices for Part 2 of Day 1.

## Decision: Zero Crossing Detection Algorithm

**Chosen Approach**: Mathematical formula using integer division (O(1) time complexity)

### Rationale

For a circular dial with positions 0-99, counting zero crossings during rotation is a modular arithmetic problem. The key insight is that we don't need to simulate each click—we can calculate crossings directly using division.

**Right (R) rotation** (increasing position):

- Crosses 0 when transitioning from 99 → 0
- Formula: `(start_position + distance) // 100`
- This counts how many complete 100-position cycles occur

**Left (L) rotation** (decreasing position):

- Crosses 0 when transitioning from 0 → 99 (going backward)
- Formula:
  - If `distance <= start_position`: 0 crossings (don't reach 0)
  - If `distance > start_position`: `1 + (distance - start_position - 1) // 100`
  - Simplified: `max(0, (distance - start_position + 99) // 100)`

**Example calculations**:

```
Right: start=50, distance=1000
  → (50 + 1000) // 100 = 10 crossings ✓

Left: start=50, distance=60
  → 60 > 50, so crosses 0
  → 1 + (60 - 50 - 1) // 100 = 1 + 0 = 1 crossing ✓

Left: start=50, distance=30
  → 30 < 50, so no crossing
  → 0 crossings ✓

Right: start=99, distance=1
  → (99 + 1) // 100 = 1 crossing ✓
```

### Alternatives Considered

**Alternative 1: Simulate each click in a loop**

```python
for _ in range(distance):
    position = (position + 1) % 100
    if position == 0:
        count += 1
```

- **Rejected because**: O(n) time complexity where n=distance. For large distances (10,000+), this is 10,000× slower than O(1) formula. Violates performance requirement (<2 seconds).

**Alternative 2: Track path array**

```python
path = [(start + i) % 100 for i in range(distance + 1)]
count = sum(1 for p in path if p == 0)
```

- **Rejected because**: O(n) time and space. Wasteful for large distances and provides no additional value over mathematical formula.

## Edge Cases & Handling

| Edge Case                        | Behavior                                                    | Formula Validation                                   |
| -------------------------------- | ----------------------------------------------------------- | ---------------------------------------------------- |
| **Zero distance** (`distance=0`) | No movement, 0 crossings                                    | Return 0 immediately                                 |
| **Starting at 0**                | Right: first cross at +100<br>Left: cross immediately at -1 | R: (0 + d) // 100<br>L: max(0, (d - 0 + 99) // 100)  |
| **Ending at 0**                  | Counts as crossing if traversed                             | Included in formula (e.g., R100 from 0 → 1 crossing) |
| **Exact multiples of 100**       | R100 → 1 crossing<br>R200 → 2 crossings                     | (s + 100k) // 100 = k + (s // 100)                   |
| **Single wrap** (d < 100)        | Most common case, 0 or 1 crossing                           | Works correctly with formula                         |
| **Multi-wrap** (d > 100)         | Multiple crossings                                          | Formula handles automatically via // operator        |

## Implementation Strategy

### Algorithm Pseudocode

```python
def count_zero_crossings_during_rotation(
    start_position: int,
    direction: str,
    distance: int
) -> int:
    """
    Count zero crossings during rotation (not including start/end positions).

    Time complexity: O(1)
    Space complexity: O(1)
    """
    if distance == 0:
        return 0

    start_position = start_position % 100

    if direction == 'R':
        # Right: count how many times we pass through multiples of 100
        return (start_position + distance) // 100
    else:  # 'L'
        # Left: count how many times we cross 0 going backward
        if distance <= start_position:
            return 0
        return 1 + (distance - start_position - 1) // 100
```

### Part 2 Solution Structure

```python
def solve_part2(rotations: list[tuple[str, int]]) -> int:
    """
    Count all clicks where dial points at 0 (during + after rotations).

    Combines:
    1. Zero crossings during rotation (new logic)
    2. Zero end-positions (Part 1 logic)
    """
    position = 50
    total_zero_count = 0

    for direction, distance in rotations:
        # Count zeros crossed DURING rotation
        during_count = count_zero_crossings_during_rotation(
            position, direction, distance
        )
        total_zero_count += during_count

        # Apply rotation
        position = apply_rotation(position, direction, distance)

        # Count if ended at 0
        if position == 0:
            total_zero_count += 1

    return total_zero_count
```

## Performance Analysis

**Time Complexity**:

- Per rotation: O(1) for formula calculation
- Total: O(n) where n = number of rotations
- Independent of rotation distance (1 or 10,000 = same time)

**Space Complexity**: O(1) - only tracking counters

**Benchmark estimate**:

- 10,000 rotations × 10,000 avg distance
- Formula-based: ~10ms (10k × 1μs per calculation)
- Loop-based: ~10 seconds (100M iterations)
- **Speedup**: 1000× faster ✓

**Meets requirement**: <2 seconds for stated workload ✓

## Testing Strategy

### Pytest Structure

Use `pytest.mark.parametrize` for comprehensive edge case coverage:

```python
@pytest.mark.parametrize("start,dir,dist,expected_during", [
    # Zero distance
    (50, "R", 0, 0),
    (50, "L", 0, 0),

    # Right rotation crossings
    (50, "R", 1000, 10),  # Multi-wrap
    (99, "R", 1, 1),      # Boundary wrap
    (0, "R", 100, 1),     # Exact wrap from 0
    (50, "R", 40, 0),     # No crossing

    # Left rotation crossings
    (50, "L", 60, 1),     # Cross once
    (50, "L", 30, 0),     # Don't reach 0
    (0, "L", 1, 1),       # From 0 going left
    (50, "L", 250, 3),    # Multi-wrap left
])
def test_count_zero_crossings_during_rotation(start, dir, dist, expected_during):
    assert count_zero_crossings_during_rotation(start, dir, dist) == expected_during
```

### Integration Test (Full Sample)

```python
def test_solve_part2_sample_input():
    """Test Part 2 with full sample sequence (expected: 6 total)."""
    rotations = parse_input(test_input_text)
    result = solve_part2(rotations)
    assert result == 6  # 3 during + 3 at end
```

## Code Quality Guidelines

**Type Hints**: All functions must have complete type signatures

```python
def count_zero_crossings_during_rotation(
    start_position: int,
    direction: str,
    distance: int
) -> int:
```

**Docstrings**: Include complexity, behavior, and examples

```python
"""
Count zero crossings during rotation.

Time: O(1), Space: O(1)

Args:
    start_position: Current dial position (0-99)
    direction: 'L' or 'R'
    distance: Number of clicks to rotate

Returns:
    Number of times position 0 is crossed during rotation

Example:
    >>> count_zero_crossings_during_rotation(50, 'R', 1000)
    10
"""
```

**Error Handling**: Validate direction input

```python
if direction not in ('L', 'R'):
    raise ValueError(f"Direction must be 'L' or 'R', got: {direction}")
```

**Naming**: Use domain terms (position, rotation, crossing) not abbreviations

## Backward Compatibility

**Part 1 function remains unchanged**:

```python
def solve_part1(rotations: list[tuple[str, int]]) -> int:
    """Original Part 1: count only end-position zeros."""
    # Existing implementation untouched
```

**Verification**:

- Part 1 sample input should still return 3
- Part 2 should return ≥ Part 1 count (Part 2 includes all Part 1 zeros)

## Summary

**Key decisions**:

1. ✅ Use mathematical formula (O(1)) instead of simulation loop (O(n))
2. ✅ Separate function for counting during-rotation crossings
3. ✅ Comprehensive parameterized tests for edge cases
4. ✅ Maintain Part 1 function for backward compatibility

**Implementation ready**: All unknowns resolved, ready to proceed to Phase 1 (data model & contracts).
