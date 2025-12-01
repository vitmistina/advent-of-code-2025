# API Contract: Day 1 Part 2 Solution Functions

**Feature**: Count all zero crossings during dial rotations  
**Date**: December 1, 2025  
**Module**: `day-01/solution.py`

## Overview

This contract defines the function signatures, behavior, and testing expectations for Day 1 Part 2. Functions must maintain backward compatibility with Part 1.

---

## Function: `count_zero_crossings_during_rotation`

**NEW in Part 2**: Core algorithm for detecting zero crossings during a rotation.

### Signature

```python
def count_zero_crossings_during_rotation(
    start_position: int,
    direction: str,
    distance: int
) -> int
```

### Parameters

| Parameter        | Type  | Constraints                 | Description                           |
| ---------------- | ----- | --------------------------- | ------------------------------------- |
| `start_position` | `int` | `0 <= start_position <= 99` | Current dial position before rotation |
| `direction`      | `str` | `'L'` or `'R'`              | Rotation direction (Left/Right)       |
| `distance`       | `int` | `>= 0`                      | Number of clicks to rotate            |

### Returns

- **Type**: `int`
- **Value**: Number of times position 0 is crossed **during** the rotation (not including start or end positions)
- **Range**: `>= 0`

### Behavior

**Right rotation** (`direction == 'R'`):

```
Crosses 0 when transitioning from 99 → 0
Formula: (start_position + distance) // 100
```

**Left rotation** (`direction == 'L'`):

```
Crosses 0 when transitioning from 0 → 99 (going backward)
Formula: max(0, (distance - start_position + 99) // 100)
```

**Edge cases**:

- `distance == 0`: Returns `0` (no movement)
- `start_position == 0`: Right rotation counts first crossing at +100, left rotation counts at +1
- Large distances: Handles multi-wrap correctly (e.g., 1000 clicks → ~10 crossings)

### Examples

```python
# Multi-wrap right
count_zero_crossings_during_rotation(50, 'R', 1000) == 10

# Boundary wrap right
count_zero_crossings_during_rotation(99, 'R', 1) == 1

# Cross once left
count_zero_crossings_during_rotation(50, 'L', 60) == 1

# Don't reach zero left
count_zero_crossings_during_rotation(50, 'L', 30) == 0

# Zero distance
count_zero_crossings_during_rotation(50, 'R', 0) == 0

# From zero, right
count_zero_crossings_during_rotation(0, 'R', 100) == 1

# From zero, left (immediately crosses)
count_zero_crossings_during_rotation(0, 'L', 1) == 1
```

### Exceptions

- **ValueError**: If `direction` is not `'L'` or `'R'`

### Complexity

- **Time**: O(1)
- **Space**: O(1)

### Testing Requirements

- Parameterized tests with `@pytest.mark.parametrize` covering:
  - Zero distance
  - Right rotation: no cross, single cross, multi-wrap
  - Left rotation: no cross, single cross, multi-wrap
  - Boundary positions (0, 99)
  - Large distances (>1000)

---

## Function: `solve_part2`

**NEW in Part 2**: Main solution function for Part 2.

### Signature

```python
def solve_part2(rotations: list[tuple[str, int]]) -> int
```

### Parameters

| Parameter   | Type                    | Description                                               |
| ----------- | ----------------------- | --------------------------------------------------------- |
| `rotations` | `list[tuple[str, int]]` | Sequence of `(direction, distance)` rotation instructions |

### Returns

- **Type**: `int`
- **Value**: Total count of all zero crossings (during rotations + end positions)
- **Range**: `>= 0`

### Behavior

1. Initialize dial position to `50`
2. Initialize zero count to `0`
3. For each rotation instruction:
   - Count crossings during rotation using `count_zero_crossings_during_rotation()`
   - Add to total count
   - Apply rotation to update position
   - If final position is `0`, increment total count
4. Return total count

**Invariant**: Result >= `solve_part1(rotations)` (Part 2 includes all Part 1 crossings)

### Examples

```python
# Sample input from puzzle description
sample_rotations = [
    ('L', 68), ('L', 30), ('R', 48), ('L', 5),
    ('R', 60), ('L', 55), ('L', 1), ('L', 99),
    ('R', 14), ('L', 82)
]

solve_part2(sample_rotations) == 6
# Breakdown:
# - L68 from 50: 1 during, ends at 82
# - L30 from 82: 0 during, ends at 52
# - R48 from 52: 0 during, ends at 0 → +1 end
# - L5 from 0: 0 during, ends at 95
# - R60 from 95: 1 during, ends at 55
# - L55 from 55: 0 during, ends at 0 → +1 end
# - L1 from 0: 0 during, ends at 99
# - L99 from 99: 0 during, ends at 0 → +1 end
# - R14 from 0: 0 during, ends at 14
# - L82 from 14: 1 during, ends at 32
# Total: 3 during + 3 end = 6 ✓

# Empty input
solve_part2([]) == 0

# Single rotation ending at 0
solve_part2([('R', 50)]) == 1  # 50 + 50 = 100 % 100 = 0
```

### Exceptions

- **ValueError**: If any rotation has invalid direction (bubbles up from helper functions)

### Complexity

- **Time**: O(n) where n = length of rotations list
- **Space**: O(1) auxiliary space (input list not counted)

### Testing Requirements

- Test with sample input (expected: 6)
- Test empty input (expected: 0)
- Test single rotation ending at 0
- Test multiple rotations with no zeros (expected: 0)
- Test large input (performance validation)
- Test result >= Part 1 result (invariant validation)

---

## Function: `solve_part1` (UNCHANGED)

**From Part 1**: Counts only end-position zeros for backward compatibility.

### Signature

```python
def solve_part1(rotations: list[tuple[str, int]]) -> int
```

### Contract

- **Behavior**: Count how many times dial points at 0 **after** rotations (not during)
- **Must remain unchanged**: Implementation should not be modified for Part 2
- **Validation**: `solve_part1(sample_input) == 3` must still pass

---

## Function: `apply_rotation` (UNCHANGED)

**From Part 1**: Applies a single rotation to dial position.

### Signature

```python
def apply_rotation(position: int, direction: str, distance: int) -> int
```

### Contract

- **Behavior**: Calculate new position using modulo arithmetic
- **Must remain unchanged**: Implementation should not be modified for Part 2
- **Used by both**: Part 1 and Part 2 solutions

---

## Function: `parse_input` (UNCHANGED)

**From Part 1**: Parses puzzle input into rotation instructions.

### Signature

```python
def parse_input(input_text: str) -> list[tuple[str, int]]
```

### Contract

- **Behavior**: Parse multi-line string into `(direction, distance)` tuples
- **Must remain unchanged**: Implementation should not be modified for Part 2
- **Used by both**: Part 1 and Part 2 solutions

---

## Integration Contract

### File Structure

```
day-01/solution.py
├── parse_input()                              # Unchanged from Part 1
├── apply_rotation()                           # Unchanged from Part 1
├── count_zero_crossings_during_rotation()    # NEW in Part 2
├── solve_part1()                              # Unchanged from Part 1
├── solve_part2()                              # NEW in Part 2
└── main()                                     # Modified to call solve_part2
```

### Test Structure

```
day-01/test_solution.py
├── test_parse_input()                                    # Existing
├── test_apply_rotation()                                 # Existing
├── test_count_zero_crossings_during_rotation()          # NEW
│   └── Parameterized with edge cases
├── test_solve_part1()                                    # Existing
├── test_solve_part2()                                    # NEW
│   └── Sample input validation
└── test_part2_includes_part1()                          # NEW
    └── Validate Part2 >= Part1 invariant
```

### Backward Compatibility

**Requirements**:

1. All Part 1 tests must continue to pass
2. `solve_part1()` implementation must not change
3. `apply_rotation()` and `parse_input()` must not change
4. New functions must not break existing functionality

**Validation**:

```bash
# Run all tests including Part 1
uv run pytest day-01/test_solution.py -v

# All tests should pass (existing + new)
```

---

## Error Handling Contract

### Input Validation

**At parsing layer** (`parse_input`):

- Malformed lines (no direction/distance) → skip or raise ValueError
- Empty input → return empty list `[]`

**At function layer**:

- Invalid direction → raise `ValueError` with message
- Negative distance → not validated (parser guarantees `\d+` → non-negative)
- Out-of-range position → not validated (modulo ensures valid range)

### Exception Guarantees

- **Strong exception safety**: Functions do not modify state on error
- **No silent failures**: Invalid inputs raise exceptions, not return sentinel values
- **Clear messages**: `ValueError` includes descriptive message (e.g., "Direction must be 'L' or 'R', got: 'X'")

---

## Performance Contract

### Guarantees

| Function                               | Time Complexity | Space Complexity | Max Runtime             |
| -------------------------------------- | --------------- | ---------------- | ----------------------- |
| `count_zero_crossings_during_rotation` | O(1)            | O(1)             | <1μs                    |
| `apply_rotation`                       | O(1)            | O(1)             | <1μs                    |
| `solve_part2`                          | O(n)            | O(1)             | <2s for n=10k rotations |
| `parse_input`                          | O(n)            | O(n)             | <100ms for n=10k lines  |

### Scalability

- Must handle distance up to 10,000 without timeout
- Must handle 10,000 rotations without timeout
- Total runtime for (10k rotations × 10k avg distance) < 2 seconds

---

## Summary

**New functions**:

- `count_zero_crossings_during_rotation()`: O(1) zero crossing detection
- `solve_part2()`: O(n) aggregation with during + end crossings

**Unchanged functions**:

- `parse_input()`, `apply_rotation()`, `solve_part1()`

**Testing**:

- Parameterized tests for edge cases
- Sample input validation (expected: 6)
- Backward compatibility validation

**Performance**:

- O(1) per rotation calculation
- O(n) total for sequence processing
- <2s for large inputs (10k × 10k)
