# API Contract: Day 2 Part 1 - Invalid Product ID Detection

**Feature**: [spec.md](../spec.md)  
**Date**: December 2, 2025  
**Type**: Internal Function API (Python module)

## Overview

This document defines the function signatures, behaviors, and contracts for the Day 2 Part 1 solution. Since this is an Advent of Code challenge, the "API" is the set of public functions in `solution.py` that can be imported and tested.

## Module: `day_02.solution`

### Function: `parse_ranges`

Parse comma-separated range input into structured data.

**Signature**:

```python
def parse_ranges(input_text: str) -> list[tuple[int, int]]:
    """
    Parse comma-separated ranges into list of (start, end) tuples.

    Args:
        input_text: String containing comma-separated ranges.
                   Format: "start1-end1,start2-end2,..."
                   Example: "11-22,95-115,998-1012"

    Returns:
        List of (start, end) tuples where start and end are integers.
        Example: [(11, 22), (95, 115), (998, 1012)]

    Raises:
        ValueError: If input format is invalid (missing dash, non-numeric values)
    """
```

**Behavior**:

- Strips whitespace from input and individual range strings
- Splits on comma to separate ranges
- Splits each range on dash to get start and end
- Converts both parts to integers
- Returns list of tuples

**Examples**:

```python
>>> parse_ranges("11-22,95-115")
[(11, 22), (95, 115)]

>>> parse_ranges("998-1012")
[(998, 1012)]

>>> parse_ranges("11-22, 95-115")  # Handles spaces
[(11, 22), (95, 115)]
```

**Error Cases**:

```python
>>> parse_ranges("invalid")
ValueError: not enough values to unpack (expected 2, got 1)

>>> parse_ranges("11-abc")
ValueError: invalid literal for int() with base 10: 'abc'

>>> parse_ranges("")
[]  # Returns empty list for empty input
```

---

### Function: `is_invalid_id`

Determine if a product ID matches the invalid pattern.

**Signature**:

```python
def is_invalid_id(num: int) -> bool:
    """
    Check if number is formed by repeating a digit sequence twice.

    A number is invalid if it consists of a digit sequence repeated exactly
    twice. Examples: 55 (5+5), 6464 (64+64), 123123 (123+123).

    Args:
        num: Integer product ID to validate

    Returns:
        True if ID is invalid (matches pattern), False otherwise
    """
```

**Behavior**:

- Converts number to string to analyze digit pattern
- Checks if string has even length (required for even split)
- Splits string in half at midpoint
- Returns True if first half equals second half
- No leading zeros (integer type prevents this)

**Examples**:

```python
>>> is_invalid_id(55)
True  # "5" + "5"

>>> is_invalid_id(6464)
True  # "64" + "64"

>>> is_invalid_id(123123)
True  # "123" + "123"

>>> is_invalid_id(1010)
True  # "10" + "10"

>>> is_invalid_id(101)
False  # Odd length, cannot split evenly

>>> is_invalid_id(1234)
False  # "12" != "34"

>>> is_invalid_id(99)
True  # "9" + "9"
```

**Edge Cases**:

```python
>>> is_invalid_id(0)
False  # Single digit "0", odd length

>>> is_invalid_id(11)
True  # "1" + "1"

>>> is_invalid_id(1188511885)
True  # "118851" + "1885" → wait, let me recalculate
# Actually "11885" + "11885" = True
```

---

### Function: `find_invalid_ids_in_range`

Find all invalid product IDs within a given range.

**Signature**:

```python
def find_invalid_ids_in_range(start: int, end: int) -> list[int]:
    """
    Find all invalid IDs in inclusive range [start, end].

    Args:
        start: First ID in range (inclusive)
        end: Last ID in range (inclusive)

    Returns:
        List of invalid product IDs found in range, in ascending order
    """
```

**Behavior**:

- Iterates through range [start, end] inclusive
- Checks each number using `is_invalid_id()`
- Collects all invalid IDs in a list
- Returns list (naturally sorted by iteration order)

**Examples**:

```python
>>> find_invalid_ids_in_range(11, 22)
[11, 22]

>>> find_invalid_ids_in_range(95, 115)
[99]

>>> find_invalid_ids_in_range(998, 1012)
[1010]

>>> find_invalid_ids_in_range(1698522, 1698528)
[]  # No invalid IDs in this range

>>> find_invalid_ids_in_range(55, 55)
[55]  # Single-element range
```

**Edge Cases**:

```python
>>> find_invalid_ids_in_range(100, 50)
[]  # Reversed range yields no iterations

>>> find_invalid_ids_in_range(10, 20)
[11]  # Only 11 is invalid in this range
```

---

### Function: `solve_part1`

Main solution function for Part 1.

**Signature**:

```python
def solve_part1(input_text: str) -> int:
    """
    Solve Part 1: Calculate sum of all invalid IDs from all ranges.

    Args:
        input_text: Comma-separated range input string
                   Example: "11-22,95-115,998-1012"

    Returns:
        Sum of all invalid product IDs found across all ranges
    """
```

**Behavior**:

1. Parse input text into list of ranges using `parse_ranges()`
2. For each range, find invalid IDs using `find_invalid_ids_in_range()`
3. Collect all invalid IDs into a single list
4. Return sum of all invalid IDs

**Examples**:

```python
>>> solve_part1("11-22,95-115,998-1012")
1142  # sum([11, 22, 99, 1010])

>>> solve_part1("11-22")
33  # sum([11, 22])

>>> solve_part1("222220-222224")
222222  # Only one invalid ID in range

>>> solve_part1("")
0  # Empty input, no ranges, sum = 0
```

**Full Example**:

```python
>>> example_input = """11-22,95-115,998-1012,1188511880-1188511890,
... 222220-222224,1698522-1698528,446443-446449,38593856-38593862,
... 565653-565659,824824821-824824827,2121212118-2121212124"""
>>> solve_part1(example_input)
1227775554
```

---

### Function: `main`

Entry point for command-line execution.

**Signature**:

```python
def main() -> None:
    """
    Main entry point for solution execution.

    Reads input from 'input.txt' in same directory as solution.
    Prints Part 1 result to stdout.
    """
```

**Behavior**:

- Reads from `day-02/input.txt` using pathlib
- Calls `solve_part1()` with input text
- Prints result with label "Part 1: {result}"

**Example Output**:

```
Part 1: 1227775554
```

---

## Testing Contract

### Test File: `test_solution.py`

**Required Test Functions**:

1. `test_is_invalid_id()` - Validate pattern detection
2. `test_is_invalid_id_edge_cases()` - Edge cases for validation
3. `test_parse_ranges()` - Input parsing
4. `test_find_invalid_ids_in_range()` - Range scanning
5. `test_solve_part1_example()` - Full example integration test
6. `test_solve_part1_individual_ranges()` - Individual range tests

**Test Data**:

- Use examples from problem description
- Verify all 8 invalid IDs: 11, 22, 99, 1010, 1188511885, 222222, 446446, 38593859
- Verify total sum: 1227775554

---

## Type Definitions

```python
from typing import List, Tuple

# Type aliases for clarity
Range = Tuple[int, int]  # (start, end)
RangeList = List[Range]
InvalidIDList = List[int]
```

---

## Error Handling

### Expected Errors

| Function                    | Error Type          | Condition                     | Handling            |
| --------------------------- | ------------------- | ----------------------------- | ------------------- |
| `parse_ranges`              | `ValueError`        | Malformed range string        | Let error propagate |
| `parse_ranges`              | `ValueError`        | Non-numeric value             | Let error propagate |
| `is_invalid_id`             | None                | Always succeeds for int input | N/A                 |
| `find_invalid_ids_in_range` | None                | Handles all int inputs        | N/A                 |
| `solve_part1`               | `ValueError`        | Invalid input format          | Let error propagate |
| `main`                      | `FileNotFoundError` | Missing input.txt             | Let error propagate |

### Design Philosophy

- Fail fast: Let errors propagate rather than silent failure
- Clear error messages from built-in exceptions
- No custom exception types needed for this simple solution

---

## Performance Contract

### Complexity Guarantees

| Function                    | Time Complexity | Space Complexity |
| --------------------------- | --------------- | ---------------- |
| `parse_ranges`              | O(R)            | O(R)             |
| `is_invalid_id`             | O(K)            | O(K)             |
| `find_invalid_ids_in_range` | O(N × K)        | O(I)             |
| `solve_part1`               | O(R × N × K)    | O(R + I)         |

Where:

- R = number of ranges
- N = average range size
- K = average digit count
- I = total invalid IDs found

### Performance Targets

- Process example input (11 ranges) in < 100ms
- Process actual puzzle input in < 10 seconds
- Memory usage stays below 100MB

---

## Integration Points

### File System

**Input**:

- Location: `day-02/input.txt`
- Format: Single line with comma-separated ranges
- Encoding: UTF-8

**Test Input**:

- Location: `day-02/test_input.txt`
- Format: Same as input.txt
- Content: Example from problem description

### Command Line

**Execution**:

```bash
uv run day-02/solution.py
```

**Output Format**:

```
Part 1: {integer_result}
```

### Testing

**Execution**:

```bash
uv run pytest day-02/test_solution.py -v
```

**Expected Output**:

- All tests pass
- Coverage of core functions
- Validation against problem examples

---

## Version

**API Version**: 1.0  
**Stability**: Stable  
**Changes**: Initial release for Day 2 Part 1
