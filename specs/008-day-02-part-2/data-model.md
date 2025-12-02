# Data Model: Day 2 Part 2 - Invalid Product ID Detection (Extended Pattern)

**Feature**: Day 2 Part 2 - Invalid Product ID Detection (Extended Pattern)  
**Phase**: Phase 1 - Design & Contracts  
**Date**: December 2, 2025

## Overview

This data model extends the Day 2 Part 1 model to support detection of invalid product IDs using the "at least twice" repetition rule. The core entities remain the same, with updated validation logic for pattern matching.

## Entities

### IDRange

Represents a continuous span of product IDs to be checked.

**Attributes**:

- `start: int` - First product ID in the range (inclusive)
- `end: int` - Last product ID in the range (inclusive)

**Validation Rules**:

- `start >= 0` (no negative IDs)
- `end >= start` (valid range)
- Range format in input: `"start-end"` (e.g., "11-22")

**Relationships**:

- Contains zero or more ProductIDs
- Parsed from comma-separated input string

**Example**:

```
Input: "11-22"
IDRange(start=11, end=22)
Contains: [11, 12, 13, ..., 22]
```

---

### ProductID

Represents a single product ID value within a range.

**Attributes**:

- `value: int` - The actual product ID number
- `is_valid: bool` - Whether the ID passes validation (computed)

**Validation Rules** (Part 2):

- Invalid if: The string representation consists of a digit sequence repeated at least twice
- Valid if: No repeated pattern exists

**State Transitions**:

```
[Created] → [Validated] → [Classified as Valid/Invalid] → [Included in Sum or Skipped]
```

**Examples**:

| Value   | String    | Pattern | Repetitions | Valid? | Part 1 Valid?            |
| ------- | --------- | ------- | ----------- | ------ | ------------------------ |
| 11      | "11"      | "1"     | 2           | No     | No                       |
| 111     | "111"     | "1"     | 3           | No     | Yes (Part 1: only if ×2) |
| 565656  | "565656"  | "56"    | 3           | No     | Yes                      |
| 446446  | "446446"  | "446"   | 2           | No     | No                       |
| 101     | "101"     | -       | -           | Yes    | Yes                      |
| 1698523 | "1698523" | -       | -           | Yes    | Yes                      |

---

### PatternMatch

Represents a detected repeated pattern in a product ID. (NEW in Part 2)

**Attributes**:

- `pattern: str` - The digit sequence that repeats
- `repetitions: int` - Number of times the pattern repeats
- `is_valid_match: bool` - True if repetitions >= 2

**Validation Rules**:

- Pattern length must be >= 1
- Pattern length must divide total string length evenly
- Repetitions must be >= 2 to make ID invalid

**Examples**:

```
"111" → PatternMatch(pattern="1", repetitions=3, is_valid_match=True)
"565656" → PatternMatch(pattern="56", repetitions=3, is_valid_match=True)
"222222" → Multiple matches possible:
  - PatternMatch(pattern="2", repetitions=6, is_valid_match=True)
  - PatternMatch(pattern="22", repetitions=3, is_valid_match=True)
  - PatternMatch(pattern="222", repetitions=2, is_valid_match=True)
  (Any one match is sufficient to mark ID as invalid)
```

---

### ValidationResult

Represents the outcome of checking an ID range. (Extends Part 1)

**Attributes**:

- `invalid_ids: list[int]` - All invalid IDs found in the range
- `total_invalid_sum: int` - Sum of all invalid IDs
- `range_start: int` - Starting ID of the range
- `range_end: int` - Ending ID of the range

**Computed Fields**:

- `count_invalid: int` - Length of invalid_ids list
- `count_total: int` - (range_end - range_start + 1)

**Example**:

```
Range: 11-22
ValidationResult(
    invalid_ids=[11, 22],
    total_invalid_sum=33,
    range_start=11,
    range_end=22,
    count_invalid=2,
    count_total=12
)
```

---

## Relationships

```
Input String
    │
    └── parses into → List[IDRange]
            │
            └── contains → List[ProductID]
                    │
                    └── validated by → PatternMatch (if invalid)
                            │
                            └── aggregates into → ValidationResult
```

## Data Flow

1. **Input Parsing**:

   - Input: `"11-22,95-115,998-1012"`
   - Output: `[IDRange(11,22), IDRange(95,115), IDRange(998,1012)]`

2. **Range Iteration**:

   - For each IDRange, generate all ProductID values
   - IDRange(11,22) → [ProductID(11), ProductID(12), ..., ProductID(22)]

3. **Pattern Detection**:

   - For each ProductID, convert value to string
   - Check all divisors of string length
   - If any divisor creates a repeated pattern ≥2 times → PatternMatch found
   - Mark ProductID as invalid if PatternMatch exists

4. **Aggregation**:

   - Collect all invalid ProductIDs across all IDRanges
   - Sum their values → final result

5. **Output**:
   - Return total sum of all invalid ProductIDs

## Example Data Flow

**Input**: `"11-22,95-115"`

**Step 1 - Parse**:

```
[IDRange(11, 22), IDRange(95, 115)]
```

**Step 2 - Generate ProductIDs**:

```
Range 1: [ProductID(11), ProductID(12), ..., ProductID(22)]
Range 2: [ProductID(95), ProductID(96), ..., ProductID(115)]
```

**Step 3 - Validate**:

```
ProductID(11) → "11" → PatternMatch("1", 2) → Invalid
ProductID(12) → "12" → No pattern → Valid
...
ProductID(22) → "22" → PatternMatch("2", 2) → Invalid
ProductID(99) → "99" → PatternMatch("9", 2) → Invalid
ProductID(111) → "111" → PatternMatch("1", 3) → Invalid (NEW in Part 2!)
```

**Step 4 - Aggregate**:

```
Invalid IDs: [11, 22, 99, 111]
Sum: 11 + 22 + 99 + 111 = 243
```

**Step 5 - Return**: `243`

## Validation Logic Changes from Part 1

| Aspect                | Part 1                                                     | Part 2                                                     |
| --------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- |
| **Rule**              | Pattern repeated exactly 2 times                           | Pattern repeated ≥2 times                                  |
| **Check**             | `len(s) % pattern_len == 0 AND len(s) // pattern_len == 2` | `len(s) % pattern_len == 0 AND len(s) // pattern_len >= 2` |
| **Example: "111"**    | Valid (1×3, not ×2)                                        | Invalid (1×3, ≥2)                                          |
| **Example: "565656"** | Valid (56×3, not ×2)                                       | Invalid (56×3, ≥2)                                         |
| **Superset**          | Subset of Part 2                                           | Includes all Part 1 invalids                               |

## Constraints & Invariants

### Constraints

- Product IDs are non-negative integers
- No leading zeros in product IDs (integer representation)
- Input ranges are inclusive on both ends
- Ranges must be non-empty (start <= end)

### Invariants

- If a ProductID is invalid in Part 1, it is also invalid in Part 2
- Part 2 sum >= Part 1 sum (Part 2 is superset)
- Single-digit numbers (1-9) are always valid
- Any number with a valid PatternMatch (repetitions ≥2) is invalid
- The first valid PatternMatch is sufficient (no need to find all)

## Test Data Examples

From specification acceptance scenarios:

| Range                 | Invalid IDs  | Notes                 |
| --------------------- | ------------ | --------------------- |
| 11-22                 | [11, 22]     | Same as Part 1        |
| 95-115                | [99, 111]    | Part 2 adds 111       |
| 998-1012              | [999, 1010]  | Part 2 adds 999       |
| 565653-565659         | [565656]     | NEW in Part 2 (56×3)  |
| 824824821-824824827   | [824824824]  | NEW in Part 2 (824×3) |
| 2121212118-2121212124 | [2121212121] | NEW in Part 2 (21×5)  |
| 1698522-1698528       | []           | No invalid IDs        |

**Complete Example Sum**: 4174379265
