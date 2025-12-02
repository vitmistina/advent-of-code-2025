# API Contract: Day 2 Part 2 - Invalid Product ID Detection

**Feature**: Day 2 Part 2 - Invalid Product ID Detection (Extended Pattern)  
**Phase**: Phase 1 - Design & Contracts  
**Date**: December 2, 2025  
**Module**: `day-02/solution.py`

## Overview

This contract defines the public API for Day 2 Part 2 solution. It extends the Part 1 API with new functions for detecting invalid IDs using the "at least twice" repetition rule.

---

## Public Functions

### `solve_part2(input_data: str) -> int`

Main entry point for solving Part 2 of Day 2.

**Purpose**: Process comma-separated ID ranges and return the sum of all invalid product IDs using Part 2 rules (pattern repeated at least twice).

**Parameters**:

- `input_data: str` - Comma-separated ID ranges (e.g., "11-22,95-115,998-1012")

**Returns**:

- `int` - Sum of all invalid product IDs found across all ranges

**Behavior**:

1. Parse input into list of ranges
2. For each range, identify all invalid IDs using Part 2 rules
3. Sum all invalid IDs across all ranges
4. Return the total sum

**Example**:

```python
input_data = "11-22,95-115"
result = solve_part2(input_data)
# Returns: 243 (11 + 22 + 99 + 111)
```

**Edge Cases**:

- Empty input: Returns 0
- Ranges with no invalid IDs: Contribute 0 to sum
- Single range: Processes normally

**Errors**:

- Raises `ValueError` if input format is invalid
- Raises `ValueError` if range start > end

**Testing**:

```python
def test_solve_part2_example():
    example = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"
    assert solve_part2(example) == 4174379265
```

---

### `is_invalid_id_part2(num: int) -> bool`

Check if a product ID is invalid according to Part 2 rules.

**Purpose**: Determine if a number consists entirely of a digit sequence repeated at least twice.

**Parameters**:

- `num: int` - Product ID to validate

**Returns**:

- `bool` - True if invalid (has repeated pattern ≥2 times), False if valid

**Behavior**:

1. Convert number to string
2. Iterate through all divisors of string length (from 1 to len//2)
3. For each divisor, extract pattern and check if repeating it forms the string
4. Return True on first match (early termination)
5. Return False if no pattern found

**Algorithm**:

```python
def is_invalid_id_part2(num: int) -> bool:
    """Check if number has a repeated pattern (at least twice)."""
    s = str(num)
    n = len(s)

    for pattern_len in range(1, n // 2 + 1):
        if n % pattern_len == 0:
            pattern = s[:pattern_len]
            repetitions = n // pattern_len
            if pattern * repetitions == s and repetitions >= 2:
                return True

    return False
```

**Examples**:

```python
# Part 2 specific (not invalid in Part 1)
assert is_invalid_id_part2(111) == True      # "1" × 3
assert is_invalid_id_part2(565656) == True   # "56" × 3
assert is_invalid_id_part2(824824824) == True # "824" × 3

# Part 1 and Part 2 overlap
assert is_invalid_id_part2(11) == True       # "1" × 2
assert is_invalid_id_part2(1010) == True     # "10" × 2

# Valid in both parts
assert is_invalid_id_part2(101) == False
assert is_invalid_id_part2(12345) == False
```

**Edge Cases**:

- Single digit (1-9): Always returns False
- Ambiguous patterns (e.g., "222222"): Returns True (any valid pattern match)
- Large numbers: Performance acceptable (O(n²) where n = digit count)

**Testing**:

```python
def test_is_invalid_id_part2():
    # Single digits valid
    assert is_invalid_id_part2(5) == False

    # Two times repetition
    assert is_invalid_id_part2(11) == True
    assert is_invalid_id_part2(1010) == True

    # Three+ times repetition (NEW in Part 2)
    assert is_invalid_id_part2(111) == True
    assert is_invalid_id_part2(565656) == True
    assert is_invalid_id_part2(824824824) == True
    assert is_invalid_id_part2(2121212121) == True

    # Valid IDs
    assert is_invalid_id_part2(101) == False
    assert is_invalid_id_part2(1698523) == False
```

---

### `check_range_part2(start: int, end: int) -> list[int]`

Find all invalid IDs within a specific range using Part 2 rules.

**Purpose**: Helper function to identify invalid IDs in a single range.

**Parameters**:

- `start: int` - First ID in range (inclusive)
- `end: int` - Last ID in range (inclusive)

**Returns**:

- `list[int]` - List of all invalid product IDs in the range

**Behavior**:

1. Iterate through all integers from start to end (inclusive)
2. For each integer, check if invalid using `is_invalid_id_part2()`
3. Collect all invalid IDs in a list
4. Return the list

**Example**:

```python
invalid = check_range_part2(11, 22)
# Returns: [11, 22]

invalid = check_range_part2(95, 115)
# Returns: [99, 111]
```

**Edge Cases**:

- Range with no invalid IDs: Returns empty list
- Single number range (start == end): Returns list with 0 or 1 element

**Testing**:

```python
def test_check_range_part2():
    assert check_range_part2(11, 22) == [11, 22]
    assert check_range_part2(95, 115) == [99, 111]
    assert check_range_part2(998, 1012) == [999, 1010]
    assert check_range_part2(1698522, 1698528) == []
```

---

## Reused from Part 1

These functions remain unchanged and are reused by Part 2:

### `parse_input(input_data: str) -> list[tuple[int, int]]`

Parse comma-separated ranges into list of (start, end) tuples.

**Signature**: `parse_input(input_data: str) -> list[tuple[int, int]]`

**Example**:

```python
ranges = parse_input("11-22,95-115")
# Returns: [(11, 22), (95, 115)]
```

**Note**: No changes needed for Part 2. Same input format.

---

## Backward Compatibility

Part 1 functions remain in `solution.py` and continue to work:

```python
# Part 1 API (UNCHANGED)
def solve_part1(input_data: str) -> int: ...
def is_invalid_id(num: int) -> bool: ...  # Part 1 rules (exactly twice)
def check_range(start: int, end: int) -> list[int]: ...
```

**Contract**: Part 1 tests must continue to pass after Part 2 implementation.

---

## Command-Line Interface

The solution script supports both parts via command-line argument:

```bash
# Run Part 1
uv run day-02/solution.py --part 1

# Run Part 2
uv run day-02/solution.py --part 2

# Default (Part 1)
uv run day-02/solution.py
```

**Implementation**:

```python
if __name__ == "__main__":
    import sys

    part = int(sys.argv[1]) if len(sys.argv) > 1 else 1

    with open("day-02/input.txt") as f:
        input_data = f.read().strip()

    if part == 1:
        result = solve_part1(input_data)
    else:
        result = solve_part2(input_data)

    print(f"Part {part}: {result}")
```

---

## Testing Contract

### Test Organization

```python
# test_solution.py structure

# ===== PART 1 TESTS (Existing - must remain green) =====
def test_parse_input(): ...
def test_is_invalid_id_part1(): ...
def test_check_range_part1(): ...
def test_solve_part1_example(): ...

# ===== PART 2 TESTS (New) =====
def test_is_invalid_id_part2(): ...
def test_check_range_part2(): ...
def test_solve_part2_individual_ranges(): ...
def test_solve_part2_example(): ...
```

### Test Data

**Example Input** (from spec):

```python
EXAMPLE_INPUT = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"

EXPECTED_PART2_SUM = 4174379265
```

**Individual Range Tests**:

```python
PART2_RANGE_TESTS = [
    ("11-22", [11, 22]),
    ("95-115", [99, 111]),
    ("998-1012", [999, 1010]),
    ("1188511880-1188511890", [1188511885]),
    ("222220-222224", [222222]),
    ("1698522-1698528", []),
    ("446443-446449", [446446]),
    ("38593856-38593862", [38593859]),
    ("565653-565659", [565656]),
    ("824824821-824824827", [824824824]),
    ("2121212118-2121212124", [2121212121]),
]
```

---

## Type Hints

All functions use Python 3.10+ type hints:

```python
from typing import Optional

def solve_part2(input_data: str) -> int: ...
def is_invalid_id_part2(num: int) -> bool: ...
def check_range_part2(start: int, end: int) -> list[int]: ...
def parse_input(input_data: str) -> list[tuple[int, int]]: ...
```

---

## Performance Contract

- **Pattern Detection**: O(n²) per number where n = digit count (acceptable for AoC)
- **Range Processing**: O(m) where m = range size (must iterate all numbers)
- **Overall**: Should complete example input in <5 seconds on modern hardware
- **Memory**: O(k) where k = number of invalid IDs found (minimal)

---

## Error Handling

Functions should raise clear exceptions for invalid input:

```python
# Invalid format
parse_input("abc-def")  # ValueError: invalid literal for int()

# Invalid range
check_range_part2(100, 50)  # ValueError: start must be <= end

# Empty input
solve_part2("")  # Returns 0 (no ranges = no invalid IDs)
```
