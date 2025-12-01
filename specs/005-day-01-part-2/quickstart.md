# Quickstart: Day 1 Part 2 Implementation

**Feature**: Count all zero crossings during dial rotations  
**Branch**: `005-day-01-part-2`  
**Date**: December 1, 2025

## Overview

This quickstart guide provides step-by-step instructions for implementing, testing, and running the Day 1 Part 2 solution using TDD workflow.

## Prerequisites

- Python 3.10+ installed
- UV package manager configured
- Repository cloned and on branch `005-day-01-part-2`
- Part 1 solution complete (`day-01/solution.py` with `solve_part1()`)

## Project Structure

```
day-01/
├── solution.py          # Extend with Part 2 functions
├── test_solution.py     # Add Part 2 tests
├── input.txt            # Actual puzzle input (already exists)
└── test_input.txt       # Sample input (already exists)

specs/005-day-01-part-2/
├── spec.md              # Feature specification
├── plan.md              # This implementation plan
├── research.md          # Algorithm research
├── data-model.md        # Data entities
└── contracts/
    └── api-contract.md  # Function contracts
```

## TDD Workflow (RED-GREEN-REFACTOR)

### Phase 1: RED - Write Failing Tests

**Step 1.1**: Add test for `count_zero_crossings_during_rotation()`

```bash
# Open test file
code day-01/test_solution.py
```

Add parameterized test:

```python
import pytest
from solution import count_zero_crossings_during_rotation

@pytest.mark.parametrize("start,direction,distance,expected", [
    # Zero distance
    (50, "R", 0, 0),
    (50, "L", 0, 0),
    # Right rotation
    (50, "R", 1000, 10),  # Multi-wrap
    (99, "R", 1, 1),       # Boundary
    (0, "R", 100, 1),      # Exact wrap
    (50, "R", 40, 0),      # No cross
    # Left rotation
    (50, "L", 60, 1),      # Cross once
    (50, "L", 30, 0),      # Don't reach
    (0, "L", 1, 1),        # From zero
    (50, "L", 250, 3),     # Multi-wrap
])
def test_count_zero_crossings_during_rotation(start, direction, distance, expected):
    assert count_zero_crossings_during_rotation(start, direction, distance) == expected
```

**Step 1.2**: Add test for `solve_part2()`

```python
def test_solve_part2_sample_input():
    """Test Part 2 with sample input (expected: 6 total)."""
    test_input = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""
    rotations = parse_input(test_input)
    result = solve_part2(rotations)
    assert result == 6
```

**Step 1.3**: Verify tests FAIL

```bash
uv run pytest day-01/test_solution.py::test_count_zero_crossings_during_rotation -v
uv run pytest day-01/test_solution.py::test_solve_part2_sample_input -v
```

Expected output: `ImportError` or `AttributeError` (functions don't exist yet) ✓

---

### Phase 2: GREEN - Implement Minimum Code

**Step 2.1**: Implement `count_zero_crossings_during_rotation()`

```bash
# Open solution file
code day-01/solution.py
```

Add function:

```python
def count_zero_crossings_during_rotation(
    start_position: int,
    direction: str,
    distance: int
) -> int:
    """
    Count how many times position 0 is crossed during rotation.

    This counts intermediate crossings DURING the rotation, not including
    the start or end positions.

    Time complexity: O(1)
    Space complexity: O(1)

    Args:
        start_position: Current dial position (0-99)
        direction: 'L' for left (decrease) or 'R' for right (increase)
        distance: Number of clicks to rotate

    Returns:
        Number of times position 0 is crossed during rotation

    Examples:
        >>> count_zero_crossings_during_rotation(50, 'R', 1000)
        10
        >>> count_zero_crossings_during_rotation(99, 'R', 1)
        1
        >>> count_zero_crossings_during_rotation(50, 'L', 60)
        1
    """
    if distance == 0:
        return 0

    if direction not in ('L', 'R'):
        raise ValueError(f"Direction must be 'L' or 'R', got: {direction}")

    start_position = start_position % 100

    if direction == 'R':
        # Right rotation: count how many times we pass through multiples of 100
        return (start_position + distance) // 100
    else:  # 'L'
        # Left rotation: count how many times we cross 0 going backward
        if distance <= start_position:
            return 0
        return 1 + (distance - start_position - 1) // 100
```

**Step 2.2**: Implement `solve_part2()`

```python
def solve_part2(rotations: list[tuple[str, int]]) -> int:
    """
    Solve Part 2: Count all clicks where dial points at 0.

    Counts both:
    1. Zero crossings DURING rotations (intermediate positions)
    2. Zero end-positions AFTER rotations (final positions)

    Time complexity: O(n) where n = number of rotations
    Space complexity: O(1)

    Args:
        rotations: List of (direction, distance) tuples

    Returns:
        Total number of times the dial pointed at 0 (during + after rotations)

    Example:
        >>> rotations = [('L', 68), ('R', 48), ('L', 55)]
        >>> solve_part2(rotations)
        # Returns count of all zero crossings
    """
    position = 50  # Dial starts at 50
    total_zero_count = 0

    for direction, distance in rotations:
        # Count zeros crossed DURING rotation
        during_count = count_zero_crossings_during_rotation(
            position, direction, distance
        )
        total_zero_count += during_count

        # Apply rotation to get new position
        position = apply_rotation(position, direction, distance)

        # Count if ended at 0
        if position == 0:
            total_zero_count += 1

    return total_zero_count
```

**Step 2.3**: Update `main()` to call Part 2

```python
def main():
    """Main entry point."""
    input_file = Path(__file__).parent / "input.txt"
    input_text = input_file.read_text()

    data = parse_input(input_text)

    part1_answer = solve_part1(data)
    print(f"Part 1: {part1_answer}")

    part2_answer = solve_part2(data)
    print(f"Part 2: {part2_answer}")
```

**Step 2.4**: Run tests (should PASS)

```bash
uv run pytest day-01/test_solution.py -v
```

Expected output: All tests pass ✓

---

### Phase 3: REFACTOR - Clean Up Code

**Step 3.1**: Verify code quality

```bash
# Run Ruff linter
uv run ruff check day-01/solution.py

# Run Ruff formatter
uv run ruff format day-01/solution.py
```

**Step 3.2**: Add additional edge case tests (optional)

```python
def test_part2_empty_input():
    """Empty input should return 0."""
    assert solve_part2([]) == 0

def test_part2_includes_part1():
    """Part 2 count should be >= Part 1 count."""
    test_input = """L68
L30
R48"""
    rotations = parse_input(test_input)
    part1 = solve_part1(rotations)
    part2 = solve_part2(rotations)
    assert part2 >= part1
```

**Step 3.3**: Re-run all tests

```bash
uv run pytest day-01/test_solution.py -v
```

---

## Running the Solution

### Run with Test Input (Sample)

```bash
# Create simple test script
cat > day-01/test_run.py << 'EOF'
from pathlib import Path
from solution import parse_input, solve_part2

test_input = Path(__file__).parent / "test_input.txt"
rotations = parse_input(test_input.read_text())
result = solve_part2(rotations)
print(f"Test input result: {result} (expected: 6)")
EOF

# Run test
uv run python day-01/test_run.py
```

Expected output: `Test input result: 6 (expected: 6)` ✓

### Run with Actual Input

```bash
uv run python day-01/solution.py
```

Expected output:

```
Part 1: <answer>
Part 2: <answer>
```

**Note**: Part 2 answer should be >= Part 1 answer.

### Submit Answer (Manual)

1. Copy Part 2 answer from output
2. Go to https://adventofcode.com/2025/day/1
3. Paste answer into Part 2 submission form
4. Click "Submit"

---

## Testing Commands

### Run All Tests

```bash
uv run pytest day-01/test_solution.py -v
```

### Run Specific Test

```bash
uv run pytest day-01/test_solution.py::test_count_zero_crossings_during_rotation -v
```

### Run with Coverage

```bash
uv run pytest day-01/test_solution.py --cov=day-01/solution --cov-report=term-missing
```

### Run Performance Test (Optional)

```python
# Add to test_solution.py
def test_solve_part2_performance():
    """Verify Part 2 handles large inputs efficiently."""
    import time

    # Generate large input (10k rotations with large distances)
    large_input = [('R', 5000), ('L', 3000)] * 5000

    start = time.perf_counter()
    result = solve_part2(large_input)
    elapsed = time.perf_counter() - start

    assert elapsed < 2.0, f"Too slow: {elapsed:.3f}s (expected <2s)"
    assert result >= 0  # Sanity check
```

---

## Debugging

### Enable Verbose Output

```python
# Add to solve_part2() for debugging
def solve_part2(rotations: list[tuple[str, int]]) -> int:
    position = 50
    total_zero_count = 0

    for i, (direction, distance) in enumerate(rotations):
        during_count = count_zero_crossings_during_rotation(position, direction, distance)
        total_zero_count += during_count

        position = apply_rotation(position, direction, distance)

        end_count = 1 if position == 0 else 0
        total_zero_count += end_count

        # Debug output
        print(f"Rotation {i+1}: {direction}{distance} → pos={position}, "
              f"during={during_count}, end={end_count}, total={total_zero_count}")

    return total_zero_count
```

### Interactive Testing

```bash
uv run python
```

```python
>>> from day_01.solution import *
>>> count_zero_crossings_during_rotation(50, 'R', 1000)
10
>>> count_zero_crossings_during_rotation(99, 'R', 1)
1
```

---

## Common Issues

### Issue: Tests fail with `ImportError`

**Solution**: Ensure function is defined in `solution.py`

### Issue: Wrong zero crossing count

**Solution**: Verify formula:

- Right: `(start + distance) // 100`
- Left: `0 if distance <= start else 1 + (distance - start - 1) // 100`

### Issue: Part 2 < Part 1

**Solution**: Bug in logic - Part 2 should include all Part 1 crossings. Check that end-position zeros are counted.

---

## Next Steps

After implementation:

1. ✅ Run all tests: `uv run pytest day-01/test_solution.py -v`
2. ✅ Run solution: `uv run python day-01/solution.py`
3. ✅ Verify Part 2 >= Part 1
4. ✅ Submit answer manually at adventofcode.com
5. ✅ Update `README.md` with completion status
6. ✅ Commit: `git commit -am "feat: solve day 1 part 2"`
7. ✅ Merge to main: `git checkout main && git merge 005-day-01-part-2`

---

## References

- **Spec**: [spec.md](../spec.md)
- **Plan**: [plan.md](../plan.md)
- **Research**: [research.md](../research.md)
- **Data Model**: [data-model.md](../data-model.md)
- **API Contract**: [contracts/api-contract.md](../contracts/api-contract.md)
- **Constitution**: [.specify/memory/constitution.md](../../.specify/memory/constitution.md)

---

## Summary

**TDD Cycle**:

1. RED: Write tests → verify they fail
2. GREEN: Implement functions → tests pass
3. REFACTOR: Clean code → tests still pass

**Key Functions**:

- `count_zero_crossings_during_rotation()`: O(1) crossing detection
- `solve_part2()`: O(n) aggregation with during + end counts

**Performance**: <2s for 10k rotations × 10k distance

**Validation**: Part 2 >= Part 1, sample input returns 6
