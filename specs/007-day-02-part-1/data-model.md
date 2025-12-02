# Data Model: Day 2 Part 1 - Invalid Product ID Detection

**Feature**: [spec.md](spec.md)  
**Date**: December 2, 2025

## Overview

This feature processes product ID ranges to identify invalid IDs (numbers formed by repeating a digit sequence twice). The data model is intentionally simple, using primitive types and standard collections.

## Entities

### Product ID Range

Represents a continuous, inclusive range of product IDs to be validated.

**Attributes**:

- `start`: Integer - first product ID in range (inclusive)
- `end`: Integer - last product ID in range (inclusive)

**Representation**: `tuple[int, int]` in Python (immutable pair)

**Validation Rules**:

- Both `start` and `end` must be non-negative integers
- `start` should be ≤ `end` (reversed ranges are invalid)
- No leading zeros in string representation

**Examples**:

```python
(11, 22)           # Range from 11 to 22
(95, 115)          # Range from 95 to 115
(1188511880, 1188511890)  # Large number range
```

### Invalid Product ID

A product ID that matches the invalid pattern: a digit sequence repeated exactly twice.

**Attributes**:

- `value`: Integer - the invalid product ID

**Representation**: `int` in Python

**Validation Rules**:

- Must have even number of digits when converted to string
- First half of digits must equal second half
- No leading zeros (enforced by integer type)

**Pattern Examples**:

```python
55        # "5" + "5" → invalid
6464      # "64" + "64" → invalid
123123    # "123" + "123" → invalid
1010      # "10" + "10" → invalid
222222    # "222" + "222" → invalid

# Valid (not invalid):
101       # Odd length, cannot split evenly
121       # Odd length
1234      # "12" ≠ "34"
```

**State**: Immutable - IDs don't change state

### Range Input

The complete input containing multiple product ID ranges.

**Attributes**:

- `ranges`: Collection of Product ID Ranges

**Representation**: `list[tuple[int, int]]` in Python

**Format**: Comma-separated range strings, each with format "start-end"

**Example**:

```python
# Input text:
"11-22,95-115,998-1012"

# Parsed representation:
[(11, 22), (95, 115), (998, 1012)]
```

**Validation Rules**:

- Non-empty string
- Comma-separated values
- Each range has exactly one dash separator
- All numeric parts are valid integers

## Data Flow

```
Input File (input.txt)
    ↓
[parse_ranges()]
    ↓
List of Range Tuples: [(start, end), ...]
    ↓
[find_invalid_ids_in_range()] for each range
    ↓
List of Invalid IDs: [11, 22, 99, 1010, ...]
    ↓
[sum()]
    ↓
Total Sum: Integer result
```

## Processing States

### Input Processing

1. **Raw Input**: String from file

   - Example: `"11-22,95-115,998-1012"`

2. **Parsed Ranges**: Structured list
   - Example: `[(11, 22), (95, 115), (998, 1012)]`

### Range Processing (per range)

1. **Range Tuple**: `(start, end)`
2. **Iteration**: For each ID in `range(start, end + 1)`
3. **Validation**: Check if ID matches invalid pattern
4. **Collection**: Accumulate invalid IDs

### Aggregation

1. **All Invalid IDs**: Flat list from all ranges

   - Example: `[11, 22, 99, 1010]`

2. **Final Sum**: Single integer
   - Example: `1142`

## Relationships

```
Range Input (1)
    ├── contains many (n)
    │   Product ID Range
    │       ├── evaluated for many (m)
    │       │   Product ID candidates
    │       │       └── classified as (0 or 1)
    │       │           Invalid Product ID
    │       └── yields many (0..m)
    │           Invalid Product IDs
    └── produces (1)
        Sum Result
```

## Data Constraints

### Performance Constraints

- **Range Size**: Individual ranges are small (< 1000 IDs typically)
- **Total Ranges**: Dozens of ranges per input
- **ID Size**: Support integers up to billions (Python handles arbitrary precision)

### Memory Constraints

- **Storage**: O(R) where R = number of ranges (minimal)
- **Processing**: O(1) space for validation (string comparison)
- **Results**: O(I) where I = total invalid IDs found (small)

### Time Complexity

- **Parsing**: O(R) where R = number of ranges
- **Validation**: O(N × K) where N = total IDs checked, K = avg digit count
- **Summation**: O(I) where I = invalid IDs found

## Implementation Notes

### Type Hints

```python
from typing import List, Tuple

def parse_ranges(input_text: str) -> List[Tuple[int, int]]:
    """Parse input into list of (start, end) tuples."""
    ...

def is_invalid_id(num: int) -> bool:
    """Check if number matches invalid pattern."""
    ...

def find_invalid_ids_in_range(start: int, end: int) -> List[int]:
    """Find all invalid IDs in inclusive range."""
    ...

def solve_part1(input_text: str) -> int:
    """Calculate sum of all invalid IDs from all ranges."""
    ...
```

### Immutability

All data structures are treated as immutable:

- Ranges are tuples (immutable)
- Invalid IDs are integers (immutable)
- New lists created rather than modified in-place

### Error Cases

**Invalid Input Formats**:

- Empty input → return 0 (no invalid IDs)
- Malformed range (no dash) → ValueError
- Non-numeric values → ValueError
- Reversed range (start > end) → ValueError or empty result

**No Error Cases** (handled naturally):

- Large numbers → Python supports arbitrary precision
- Single-ID range → `range(n, n+1)` yields one value
- No invalid IDs in range → empty list, sum = 0

## Examples

### Complete Example

**Input**:

```
11-22,95-115,998-1012
```

**Parsed**:

```python
ranges = [(11, 22), (95, 115), (998, 1012)]
```

**Processing**:

```python
# Range (11, 22):
#   11: "1" + "1" ✓ invalid
#   12: "1" ≠ "2" ✗ valid
#   ...
#   22: "2" + "2" ✓ invalid
# Result: [11, 22]

# Range (95, 115):
#   99: "9" + "9" ✓ invalid
#   Others: ✗ valid
# Result: [99]

# Range (998, 1012):
#   1010: "10" + "10" ✓ invalid
#   Others: ✗ valid
# Result: [1010]
```

**Aggregation**:

```python
all_invalid = [11, 22, 99, 1010]
total = sum(all_invalid) = 1142
```

## Schema (Conceptual)

While this is not a database application, here's the conceptual schema:

```
RangeInput
├── id: string (from filename)
├── raw_text: string
└── ranges: list[Range]

Range
├── start: int
└── end: int

InvalidID
└── value: int

Result
├── invalid_ids: list[int]
└── total_sum: int
```

## Validation Rules Summary

| Entity     | Rule                     | Enforcement            |
| ---------- | ------------------------ | ---------------------- |
| Range      | start ≤ end              | Parse-time check       |
| Range      | Both integers            | Type conversion        |
| Invalid ID | Even digit count         | String length check    |
| Invalid ID | First half = second half | String comparison      |
| Invalid ID | No leading zeros         | Integer type (natural) |
| Input      | Comma-separated          | Parse-time split       |
| Input      | Dash-separated pairs     | Parse-time split       |
