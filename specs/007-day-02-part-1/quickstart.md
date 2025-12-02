# Quickstart Guide: Day 2 Part 1 - Invalid Product ID Detection

**Feature**: Day 2 Part 1 Solution  
**Branch**: `007-day-02-part-1`  
**Date**: December 2, 2025

## Prerequisites

- Python 3.10+
- UV package manager installed
- Git repository cloned
- AOC session token configured in `.env`

## Quick Start (5 minutes)

### 1. Download Challenge Data

The challenge description and input have already been downloaded to `day-02/`.

Verify files exist:

```bash
ls day-02/
# Expected: description.md, input.txt
```

### 2. Follow TDD Workflow

**Phase 1: RED (Write Failing Tests First)**

```bash
# Create test file first
touch day-02/test_solution.py
```

Edit `day-02/test_solution.py` and write tests for:

- `test_is_invalid_id()` - Pattern validation
- `test_parse_ranges()` - Input parsing
- `test_solve_part1_example()` - Full example

Run tests to verify they FAIL:

```bash
uv run pytest day-02/test_solution.py -v
# Expected: ImportError or test failures
```

**Phase 2: GREEN (Implement Minimal Solution)**

Create `day-02/solution.py` and implement:

- `is_invalid_id(num: int) -> bool`
- `parse_ranges(input_text: str) -> list[tuple[int, int]]`
- `find_invalid_ids_in_range(start: int, end: int) -> list[int]`
- `solve_part1(input_text: str) -> int`
- `main()` - entry point

Run tests until GREEN:

```bash
uv run pytest day-02/test_solution.py -v
# Expected: All tests pass
```

**Phase 3: REFACTOR (Clean Up)**

- Add docstrings
- Add type hints
- Optimize if needed
- Keep tests GREEN

### 3. Run Solution

```bash
uv run day-02/solution.py
# Expected output:
# Part 1: [your answer]
```

### 4. Submit Answer

1. Copy the answer from terminal output
2. Visit https://adventofcode.com/2025/day/2
3. Manually paste answer into submission form
4. Submit!

### 5. Update Progress

```bash
# Update README.md progress tracker
# Commit changes
git add day-02/ specs/007-day-02-part-1/
git commit -m "feat: solve day 02 part 1"
git push
```

## Detailed Implementation Guide

### Test Examples

Use these examples from the problem description:

```python
# test_solution.py
def test_is_invalid_id():
    """Test invalid ID pattern detection."""
    # Invalid patterns (repeated sequence)
    assert is_invalid_id(11) == True      # "1" + "1"
    assert is_invalid_id(22) == True      # "2" + "2"
    assert is_invalid_id(99) == True      # "9" + "9"
    assert is_invalid_id(1010) == True    # "10" + "10"
    assert is_invalid_id(6464) == True    # "64" + "64"
    assert is_invalid_id(123123) == True  # "123" + "123"

    # Valid patterns (not repeated)
    assert is_invalid_id(101) == False    # Odd length
    assert is_invalid_id(1234) == False   # "12" != "34"


def test_find_invalid_ids_in_range():
    """Test finding invalid IDs in ranges."""
    assert find_invalid_ids_in_range(11, 22) == [11, 22]
    assert find_invalid_ids_in_range(95, 115) == [99]
    assert find_invalid_ids_in_range(998, 1012) == [1010]
    assert find_invalid_ids_in_range(1698522, 1698528) == []


def test_solve_part1_example():
    """Test with full example from problem."""
    example = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"
    assert solve_part1(example) == 1227775554
```

### Implementation Template

```python
# solution.py
"""Advent of Code 2025 - Day 02 Part 1 Solution."""

from pathlib import Path


def is_invalid_id(num: int) -> bool:
    """
    Check if number is formed by repeating a digit sequence twice.

    Args:
        num: Integer product ID to validate

    Returns:
        True if ID is invalid (matches pattern), False otherwise

    Examples:
        >>> is_invalid_id(55)
        True
        >>> is_invalid_id(101)
        False
    """
    s = str(num)
    if len(s) % 2 != 0:
        return False
    mid = len(s) // 2
    return s[:mid] == s[mid:]


def parse_ranges(input_text: str) -> list[tuple[int, int]]:
    """
    Parse comma-separated ranges into list of (start, end) tuples.

    Args:
        input_text: String containing comma-separated ranges

    Returns:
        List of (start, end) tuples
    """
    if not input_text.strip():
        return []

    ranges = []
    for range_str in input_text.strip().split(','):
        start_str, end_str = range_str.strip().split('-')
        ranges.append((int(start_str), int(end_str)))
    return ranges


def find_invalid_ids_in_range(start: int, end: int) -> list[int]:
    """
    Find all invalid IDs in inclusive range [start, end].

    Args:
        start: First ID in range
        end: Last ID in range

    Returns:
        List of invalid product IDs
    """
    return [num for num in range(start, end + 1) if is_invalid_id(num)]


def solve_part1(input_text: str) -> int:
    """
    Solve Part 1: Calculate sum of all invalid IDs.

    Args:
        input_text: Comma-separated range input

    Returns:
        Sum of all invalid product IDs
    """
    ranges = parse_ranges(input_text)
    invalid_ids = []

    for start, end in ranges:
        invalid_ids.extend(find_invalid_ids_in_range(start, end))

    return sum(invalid_ids)


def main():
    """Main entry point."""
    input_file = Path(__file__).parent / "input.txt"
    input_text = input_file.read_text().strip()

    part1_answer = solve_part1(input_text)
    print(f"Part 1: {part1_answer}")


if __name__ == "__main__":
    main()
```

## Testing Checklist

- [ ] RED: All tests written and failing
- [ ] GREEN: All tests passing
- [ ] REFACTOR: Code cleaned, tests still green
- [ ] Example test passes (sum = 1227775554)
- [ ] Individual range tests pass
- [ ] Edge cases handled (empty input, single ID ranges)
- [ ] Code has docstrings and type hints
- [ ] Follows PEP8 style (run `ruff check day-02/`)

## Common Issues

### Test Not Failing Initially

**Problem**: Tests pass immediately without implementation  
**Solution**: Verify import - should get `ImportError` or `AttributeError`

### Wrong Sum for Example

**Problem**: Getting different sum than 1227775554  
**Solution**:

- Verify all 8 invalid IDs found: 11, 22, 99, 1010, 1188511885, 222222, 446446, 38593859
- Check pattern matching logic (must be even length)
- Check range is inclusive (use `range(start, end + 1)`)

### Performance Issues

**Problem**: Solution takes too long  
**Solution**:

- Avoid generating all IDs in memory (use generator or iterate)
- Pattern check should be O(K) where K = digit count
- Don't pre-generate all possible invalid IDs

## File Structure Reference

```
day-02/
├── solution.py          # Main implementation
├── test_solution.py     # Test suite
├── input.txt            # Actual puzzle input
├── test_input.txt       # Example input (optional)
├── description.md       # Problem description
└── README.md            # Notes (optional)

specs/007-day-02-part-1/
├── spec.md              # Feature specification
├── plan.md              # Implementation plan
├── research.md          # Technical research
├── data-model.md        # Data model
├── quickstart.md        # This file
└── contracts/
    └── api-contract.md  # Function contracts
```

## Next Steps

After completing Part 1:

1. Wait for Part 2 to unlock
2. Read Part 2 description
3. Create new spec: `specs/008-day-02-part-2/`
4. Follow same TDD workflow
5. Extend existing `solution.py` with `solve_part2()`

## Documentation

- **Spec**: [spec.md](spec.md) - Full feature specification
- **Research**: [research.md](research.md) - Algorithm decisions
- **Data Model**: [data-model.md](data-model.md) - Entity definitions
- **API Contract**: [contracts/api-contract.md](contracts/api-contract.md) - Function signatures
- **Plan**: [plan.md](plan.md) - Implementation plan

## Help

**Stuck on algorithm?** Review [research.md](research.md) for pattern detection approach

**Need function signatures?** Check [contracts/api-contract.md](contracts/api-contract.md)

**Confused about entities?** See [data-model.md](data-model.md)

**Testing questions?** TDD is NON-NEGOTIABLE per Constitution Principle IV
