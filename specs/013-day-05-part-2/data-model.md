# Data Model: Day 5 Part 2

**Phase**: Phase 1 (Design & Contracts)  
**Status**: Completed  
**Date**: December 5, 2025

## Overview

Part 2 reuses the core data model from Part 1 (`FreshRange`, range merging) and adds minimal new logic for summing merged ranges to calculate total fresh IDs.

# Data Model: Day 5 Part 2 - Fresh Ingredient ID Range Coverage

## Entity: FreshRange

- **Fields:**
  - start: int (inclusive)
  - end: int (inclusive)
- **Description:** Represents a closed interval of fresh ingredient IDs.
- **Validation:** start <= end

## Entity: MergedRange

- **Fields:**
  - start: int
  - end: int
- **Description:** Disjoint, sorted intervals after merging all FreshRanges.

## Relationships

- Many FreshRange → merged into Many MergedRange (union)

## State/Transitions

- Input: List[FreshRange] parsed from input (ignore available IDs section)
- Output: List[MergedRange] (disjoint, sorted)
- Final: Total count = sum(end - start + 1 for each MergedRange)

## Validation Rules

- All ranges must be valid (start <= end)
- Input may be empty (edge case)

---

## Primary Entities

### Entity 1: FreshRange

**Purpose**: Immutable representation of a single fresh ingredient ID range  
**Reused from**: Part 1

```python
@dataclass
class FreshRange:
    start: int
    end: int

    def __post_init__(self):
        if self.start > self.end:
            raise ValueError(f"Invalid FreshRange: start ({self.start}) > end ({self.end})")
```

**Fields**:
| Field | Type | Constraints | Rationale |
|-------|------|-------------|-----------|
| `start` | `int` | `start ≤ end` | Inclusive lower bound of fresh ID range |
| `end` | `int` | `end ≥ start` | Inclusive upper bound of fresh ID range |

**Behavior**:

- **Immutable**: Frozen dataclass (no mutation after creation)
- **Validation**: Rejects reverse ranges (start > end) with ValueError
- **Inclusive**: Both `start` and `end` are valid fresh IDs
  - Range [3, 5] contains IDs: 3, 4, 5 (count = 3)
  - Formula: `count = end - start + 1`

**Examples**:

```python
r1 = FreshRange(3, 5)       # ✅ Valid: 3 IDs
r2 = FreshRange(10, 10)     # ✅ Valid: 1 ID (single ID range)
r3 = FreshRange(5, 3)       # ❌ ValueError: start > end
```

---

### Entity 2: Merged Range Union

**Purpose**: Representation of the complete set of fresh IDs via disjoint intervals  
**Storage**: `List[Tuple[int, int]]` (list of (start, end) tuples)

```python
# Result of merge_ranges([FreshRange(3, 5), FreshRange(10, 14), FreshRange(16, 20), FreshRange(12, 18)])
merged: List[Tuple[int, int]] = [(3, 5), (10, 20)]
```

**Properties**:

- **Sorted**: Tuples are sorted by start position (ascending)
- **Disjoint**: No tuple overlaps or touches
  - (3, 5) and (10, 20) have gap at IDs 6, 7, 8, 9
  - Adjacency is merged: (1, 10) and (11, 20) become (1, 20)
- **Complete union**: Union contains all IDs from any input range, no duplicates

**Calculation**:

```python
# Given merged = [(3, 5), (10, 20)]
total_ids = sum(end - start + 1 for start, end in merged)
          = (5 - 3 + 1) + (20 - 10 + 1)
          = 3 + 11
          = 14
```

---

### Entity 3: Database Input

**Purpose**: Parsed input file with fresh ranges and available ingredient IDs  
**Storage**: Tuple `(ranges: List[FreshRange], available_ids: List[int])`

```python
# From input:
# 3-5
# 10-14
# 16-20
# 12-18
#
# 1
# 5
# 8
# 11
# 17
# 32

ranges, available_ids = parse_database(data)
# ranges = [FreshRange(3, 5), FreshRange(10, 14), FreshRange(16, 20), FreshRange(12, 18)]
# available_ids = [1, 5, 8, 11, 17, 32]
```

**Part 2 Usage**:

- ✅ **Uses**: `ranges` (first element)
- ❌ **Ignores**: `available_ids` (second element)

---

## Functions & Their Contracts

### Function 1: parse_database()

**Signature**:

```python
def parse_database(data: str) -> tuple[list[FreshRange], list[int]]:
```

**Purpose**: Parse input string into ranges and available IDs  
**Reused from**: Part 1

**Input**:

- `data: str` - Input string with format:

  ```
  START-END
  START-END
  ...

  ID
  ID
  ...
  ```

**Output**:

- Tuple containing:
  - `List[FreshRange]`: Parsed fresh ranges (order as given in input)
  - `List[int]`: Parsed available ingredient IDs (order as given in input)

**Complexity**: O(R + I) where R = ranges, I = available IDs  
**Space**: O(R + I)

**Error Handling**:

- Raises `ValueError` if input is not a string
- Raises `ValueError` if blank line separator is missing
- Raises `ValueError` for malformed range lines (non-numeric, wrong format)
- Raises `ValueError` for malformed ID lines (non-numeric)

**Examples**:

```python
data = "3-5\n10-14\n\n1\n5\n"
ranges, ids = parse_database(data)
# ranges = [FreshRange(3, 5), FreshRange(10, 14)]
# ids = [1, 5]

# Part 2 usage
ranges, _ = parse_database(data)  # Ignore IDs
```

---

### Function 2: merge_ranges()

**Signature**:

```python
def merge_ranges(ranges: List[FreshRange]) -> List[Tuple[int, int]]:
```

**Purpose**: Merge overlapping/adjacent ranges into disjoint union  
**Reused from**: Part 1

**Input**:

- `ranges: List[FreshRange]` - Potentially overlapping ranges

**Output**:

- `List[Tuple[int, int]]` - Sorted, disjoint intervals representing union
  - Guaranteed sorted by start
  - Guaranteed non-overlapping
  - Adjacent ranges merged (e.g., [1-10] and [11-20] → [1-20])

**Complexity**: O(R log R) time (dominated by sort), O(R) space  
**Algorithm**:

1. Sort ranges by start position: O(R log R)
2. Single-pass merge: O(R)
   - Start with first range
   - For each subsequent range:
     - If overlaps/adjacent with current: extend current
     - Else: start new interval

**Example**:

```python
ranges = [FreshRange(3, 5), FreshRange(10, 14), FreshRange(16, 20), FreshRange(12, 18)]
merged = merge_ranges(ranges)
# merged = [(3, 5), (10, 20)]

# Walkthrough:
# Sort:   [FreshRange(3, 5), FreshRange(10, 14), FreshRange(12, 18), FreshRange(16, 20)]
# Pass 1: Add (3, 5) to merged
# Pass 2: (10, 14) doesn't touch (3, 5), add new interval
# Pass 3: (12, 18) touches (10, 14) [10 ≤ 14+1], merge: (10, max(14, 18)) = (10, 18)
# Pass 4: (16, 20) touches (10, 18) [16 ≤ 18+1], merge: (10, max(18, 20)) = (10, 20)
# Result: [(3, 5), (10, 20)]
```

---

### Function 3: solve_part2()

**Signature**:

```python
def solve_part2(data: str) -> int:
```

**Purpose**: Calculate total count of unique fresh ingredient IDs across all ranges  
**NEW in Part 2**

**Input**:

- `data: str` - Database input string (same format as Part 1)

**Output**:

- `int` - Total count of unique IDs that are fresh (in any range)

**Complexity**: O(R log R) time, O(R) space  
**Algorithm**:

1. Parse input: O(R + I)
2. Merge ranges: O(R log R)
3. Sum IDs in merged ranges: O(M) where M ≤ R

**Implementation**:

```python
def solve_part2(data: str) -> int:
    """
    Calculate total unique fresh ingredient IDs across all ranges.
    Ignores available ingredient IDs section.

    Time: O(R log R) where R = number of ranges
    Space: O(R)
    """
    ranges, _ = parse_database(data)  # Ignore available IDs
    merged = merge_ranges(ranges)
    total_fresh = sum(end - start + 1 for start, end in merged)
    return total_fresh
```

**Examples**:

```python
# Example 1: Simple range
data = "3-5\n\n"
solve_part2(data) → 3  # IDs: 3, 4, 5

# Example 2: Overlapping ranges (union)
data = "3-5\n10-14\n16-20\n12-18\n\n1\n5\n8\n11\n17\n32\n"
solve_part2(data) → 14  # IDs: 3, 4, 5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20

# Example 3: Adjacent ranges (merged into one)
data = "1-10\n11-20\n\n"
solve_part2(data) → 20  # IDs: 1, 2, ..., 20 (merged into [1-20])
```

---

## State Transitions

Part 2 has no stateful objects; all functions are pure (deterministic, no side effects).

```
Input String
    ↓
parse_database()
    ↓
(ranges, available_ids)
    ↓
merge_ranges(ranges)
    ↓
List[Tuple[int, int]] (merged)
    ↓
sum() over intervals
    ↓
int (total count) ← OUTPUT
```

---

## Validation Rules

### Range Validation

- **Constraint**: `start ≤ end` (enforced in `FreshRange.__post_init__`)
- **Constraint**: `start, end ≥ 0` (assumed from puzzle context; not enforced)

### Database Validation

- **Constraint**: Input MUST have blank line separating ranges and IDs
- **Constraint**: Ranges and IDs MUST be parseable as integers
- **Constraint**: Ranges MUST be in format `START-END` with single `-` separator

### Merge Output Validation

- **Guarantee**: Output intervals are sorted by start position
- **Guarantee**: No interval overlaps (disjoint)
- **Guarantee**: Adjacent intervals are merged (no gap of exactly 1)

---

## Summary

| Component            | Type      | Reused      | Complexity | Status |
| -------------------- | --------- | ----------- | ---------- | ------ |
| **FreshRange**       | Dataclass | From Part 1 | -          | ✅     |
| **parse_database()** | Function  | From Part 1 | O(R + I)   | ✅     |
| **merge_ranges()**   | Function  | From Part 1 | O(R log R) | ✅     |
| **solve_part2()**    | Function  | NEW         | O(R log R) | ✅     |
| **Merged union**     | Output    | NEW concept | O(M)       | ✅     |

**No new entities; focus on reuse and minimal extension.**
