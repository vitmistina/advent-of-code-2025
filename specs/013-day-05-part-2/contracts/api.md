# API Contract: Day 5 Part 2

**Phase**: Phase 1 (Design & Contracts)  
**Status**: Completed  
**Date**: December 5, 2025

---

## Function Contract: solve_part2()

### Signature

```python
def solve_part2(data: str) -> int:
```

### Purpose

Calculate the total count of unique fresh ingredient IDs across all fresh ingredient ID ranges, ignoring the available IDs section.

### Input Contract

**Parameter**: `data: str`

**Format**:

```
START-END
START-END
...
[blank line]
ID
ID
...
```

**Requirements**:

- Must be a valid string (raises `TypeError` if not)
- Must contain ranges section (line(s) with `START-END` format)
- Must contain blank line separator
- May contain available IDs section (ignored by Part 2)
- Ranges and IDs must be parseable as integers
- Each range must have exactly one `-` separator

**Valid Examples**:

```python
# Example 1: Simple single range
data1 = "5-5\n\n"

# Example 2: Multiple ranges with available IDs (ignored)
data2 = "3-5\n10-14\n16-20\n12-18\n\n1\n5\n8\n11\n17\n32\n"

# Example 3: Adjacent ranges
data3 = "1-10\n11-20\n\n"

# Example 4: Large ranges
data4 = "1-1000000\n500000-1500000\n\n"
```

**Invalid Examples** (raise errors):

```python
# Missing blank line separator
bad1 = "3-5\n10-14\n1\n5"  # ValueError

# Non-numeric values
bad2 = "a-b\n\n"  # ValueError

# Wrong format
bad3 = "3 5\n\n"  # ValueError (should be 3-5)

# Non-string input
bad4 = 12345  # TypeError
```

### Output Contract

**Return Type**: `int`

**Value**: Total count of unique fresh ingredient IDs across all merged ranges

**Constraints**:

- Non-negative integer (≥ 0)
- Represents union of all ranges (no double-counting overlaps)
- For empty range list, returns 0

**Valid Outputs**:

```python
solve_part2("5-5\n\n")  # → 1
solve_part2("1-10\n11-20\n\n")  # → 20
solve_part2("3-5\n10-14\n16-20\n12-18\n\n1\n5\n8\n11\n17\n32\n")  # → 14
solve_part2("\n\n")  # → 0 (no ranges)
solve_part2("1-1000000\n\n")  # → 1000000
```

### Complexity Contract

**Time Complexity**: O(R log R) where R = number of ranges

- Parse: O(R)
- Merge: O(R log R) dominated by sort
- Sum: O(M) where M ≤ R

**Space Complexity**: O(R)

- Stores R parsed ranges
- Stores M ≤ R merged intervals
- No full enumeration of IDs

### Behavior Contract

#### Overlapping Ranges

- Ranges [3-5] and [10-14] and [12-18] and [16-20] → merged to [3-5] and [10-20]
- Count = 3 + 11 = 14 ✅

#### Adjacent Ranges

- Ranges [1-10] and [11-20] → merged to [1-20]
- Count = 20 ✅

#### Non-Adjacent Ranges

- Ranges [1-3] and [5-7] → NOT merged
- Count = 3 + 3 = 6 ✅

#### Single-ID Ranges

- Range [10-10] → single ID
- Count = 1 ✅

#### Empty Ranges

- No ranges provided → count 0
- Result = 0 ✅

#### Large ID Values

- Range [1000000000-1000000010] → 11 IDs
- No enumeration; counted via formula ✅

### Error Handling Contract

| Error Type   | Trigger                      | Behavior                                                      |
| ------------ | ---------------------------- | ------------------------------------------------------------- |
| `TypeError`  | Input is not a string        | Raises `TypeError("Input data must be a string.")`            |
| `ValueError` | Missing blank line separator | Raises `ValueError("Malformed input: missing blank line...")` |
| `ValueError` | Malformed range line         | Raises `ValueError("Malformed range line: '{line}'")`         |
| `ValueError` | Range has start > end        | Raises `ValueError` from FreshRange.**post_init**             |
| `ValueError` | Non-numeric range values     | Raises `ValueError("Malformed range line: '{line}'")`         |

### Acceptance Criteria

✅ **AC-001**: Function returns integer count of fresh IDs  
✅ **AC-002**: Overlapping ranges correctly merged (no double-counting)  
✅ **AC-003**: Adjacent ranges correctly merged  
✅ **AC-004**: Non-adjacent ranges NOT merged (gaps preserved)  
✅ **AC-005**: Available IDs section completely ignored  
✅ **AC-006**: Single-ID ranges handled correctly  
✅ **AC-007**: Large ID ranges handled efficiently (no enumeration)  
✅ **AC-008**: Empty range list returns 0  
✅ **AC-009**: O(R log R) time complexity achieved  
✅ **AC-010**: O(R) space complexity achieved  
✅ **AC-011**: All error cases raise appropriate exceptions with descriptive messages

### Test Cases Covering Contract

```python
# Basic functionality
test_single_range()  # AC-006
test_multiple_non_overlapping()  # AC-004
test_overlapping_ranges()  # AC-002
test_adjacent_ranges_merged()  # AC-003

# From specification examples
test_example_database_14_ids()  # AC-001, AC-002, AC-003, AC-005

# Edge cases
test_empty_ranges()  # AC-008
test_large_range()  # AC-007
test_single_id_ranges()  # AC-006
test_heavily_overlapping()  # AC-002

# Error cases
test_missing_blank_line()  # AC-011
test_malformed_range()  # AC-011
test_non_string_input()  # AC-011
test_reverse_range()  # AC-011
```

---

## Reused Functions (Part 1)

### parse_database()

```python
def parse_database(data: str) -> tuple[list[FreshRange], list[int]]:
```

**Input**: String with ranges, blank line, and IDs  
**Output**: Tuple of (ranges, available*ids)  
**Usage in Part 2**: `ranges, * = parse_database(data)`  
**Complexity**: O(R + I) where I = count of IDs (ignored)

---

### merge_ranges()

```python
def merge_ranges(ranges: List[FreshRange]) -> List[Tuple[int, int]]:
```

**Input**: List of potentially overlapping FreshRange objects  
**Output**: Sorted list of disjoint (start, end) tuples  
**Usage in Part 2**: Core merging logic, unchanged  
**Complexity**: O(R log R) time, O(R) space

---

## Integration Example

```python
from day_05.solution import solve_part2

# Typical usage
input_file = "day-05/input.txt"
with open(input_file) as f:
    puzzle_input = f.read()

result = solve_part2(puzzle_input)
print(f"Part 2 Answer: {result}")
```

---

## Non-Functional Requirements

| Requirement                   | Satisfied                    |
| ----------------------------- | ---------------------------- |
| Uses Python 3.10+             | ✅ (dataclasses, type hints) |
| Follows PEP8                  | ✅ (ruff formatted)          |
| Includes docstring            | ✅                           |
| Unit testable                 | ✅                           |
| No external dependencies      | ✅ (built-in only)           |
| Deterministic (pure function) | ✅ (no side effects)         |
| Handles large inputs          | ✅ (O(R log R) scales well)  |
