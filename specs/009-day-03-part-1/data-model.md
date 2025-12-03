# Data Model: Day 3 Part 1 - Battery Bank Joltage Calculator

**Feature**: [spec.md](spec.md)  
**Date**: December 3, 2025  
**Purpose**: Define entities and their relationships for battery bank joltage calculation

## Entity Definitions

### Battery Bank

**Description**: A sequence of batteries represented as a string of digit characters, where each character represents an individual battery with that joltage rating.

**Attributes**:

- **digits** (str): The sequence of digit characters ('1' through '9') representing batteries
- **length** (int): Number of batteries in the bank (derived from len(digits))

**Validation Rules**:

- Must contain at least 2 digits (need exactly 2 batteries to form a pair)
- All characters must be valid digits ('1' through '9')
- No whitespace or other characters allowed

**Examples**:

- `"987654321111111"` - 15 batteries
- `"45"` - 2 batteries (minimum valid size)
- `"5555555"` - 7 batteries (all same rating)

### Battery

**Description**: An individual power unit with a joltage rating from 1 to 9, represented by a single digit character in a battery bank string.

**Attributes**:

- **rating** (int): Joltage rating (1-9)
- **position** (int): Zero-based index in the battery bank string

**Constraints**:

- Rating must be in range [1, 9]
- Position must be valid index in bank string
- Cannot be rearranged from original position

**Examples**:

- In bank `"987"`: Battery at position 0 has rating 9
- In bank `"987"`: Battery at position 1 has rating 8
- In bank `"987"`: Battery at position 2 has rating 7

### Battery Pair

**Description**: Two batteries selected from a bank that produce a specific joltage value based on their positions.

**Attributes**:

- **first_position** (int): Index of first battery (i)
- **second_position** (int): Index of second battery (j)
- **joltage** (int): The two-digit number formed by the batteries

**Constraints**:

- first_position < second_position (maintains left-to-right order)
- Both positions must be valid indices in the bank
- joltage = rating_at_first \* 10 + rating_at_second

**Calculation Formula**:

```
joltage = int(bank[first_position]) * 10 + int(bank[second_position])
```

**Examples**:

- Bank `"987"`, positions (0, 1) → joltage = 9 × 10 + 8 = 98
- Bank `"987"`, positions (0, 2) → joltage = 9 × 10 + 7 = 97
- Bank `"987"`, positions (1, 2) → joltage = 8 × 10 + 7 = 87

### Maximum Joltage

**Description**: The highest joltage value that can be produced from a single battery bank by selecting the optimal pair of batteries.

**Attributes**:

- **value** (int): The maximum joltage (0-99 range)
- **bank** (str): The source battery bank

**Calculation**:

- Evaluate all possible battery pairs in the bank
- Select the pair with the highest joltage value
- Return that maximum value

**Examples**:

- Bank `"987654321111111"` → max joltage = 98
- Bank `"811111111111119"` → max joltage = 89
- Bank `"45"` → max joltage = 45

### Total Output Joltage

**Description**: The sum of maximum joltage values from all battery banks.

**Attributes**:

- **value** (int): Sum of all maximum joltages
- **banks** (list[str]): All battery banks in the input

**Calculation**:

- For each battery bank, calculate its maximum joltage
- Sum all maximum joltages
- Return the total

**Example**:

```
Banks:
  "987654321111111" → 98
  "811111111111119" → 89
  "234234234234278" → 78
  "818181911112111" → 92

Total Output Joltage = 98 + 89 + 78 + 92 = 357
```

## Entity Relationships

```
Input (str)
  │
  ├─ contains multiple ──→ Battery Bank (str)
  │                          │
  │                          ├─ contains ──→ Battery (char)
  │                          │                  │
  │                          │                  └─ has rating (int 1-9)
  │                          │
  │                          ├─ generates all ──→ Battery Pair
  │                          │                      │
  │                          │                      └─ produces joltage (int 0-99)
  │                          │
  │                          └─ has one ──→ Maximum Joltage (int)
  │
  └─ produces ──→ Total Output Joltage (int)
```

## Data Flow

```
Input Text
    ↓
  parse_input()
    ↓
  List[Battery Bank (str)]
    ↓
  for each bank
    ↓
  max_joltage(bank)
    ↓
  try all pairs → Battery Pair
    ↓
  calculate joltage for each pair
    ↓
  select maximum → Maximum Joltage (int)
    ↓
  sum all maximums
    ↓
  Total Output Joltage (int)
```

## Implementation Notes

### Primitive Types Used

All entities are represented using Python primitive types:

- **Battery Bank**: `str` (sequence of digit characters)
- **Battery**: Single character from string (accessed via index)
- **Battery Pair**: Implicit in loop variables `(i, j)`
- **Joltage**: `int` (calculated value)
- **Maximum Joltage**: `int` (tracked variable)
- **Total Output Joltage**: `int` (sum result)

### No Complex Data Structures Needed

The solution uses only:

- Strings (for battery banks)
- Integers (for positions and joltage values)
- Lists (for holding bank strings)

No classes, named tuples, or dataclasses are necessary - the problem is simple enough to solve with primitives and pure functions.

### Type Hints

```python
def parse_input(input_text: str) -> list[str]:
    """Parse input into list of battery bank strings."""
    ...

def max_joltage(bank: str) -> int:
    """Find maximum joltage from a battery bank."""
    ...

def solve_part1(input_text: str) -> int:
    """Solve Day 3 Part 1: Calculate total output joltage."""
    ...
```

## Validation Rules Summary

| Entity       | Rule            | Validation Method                           |
| ------------ | --------------- | ------------------------------------------- |
| Battery Bank | Length ≥ 2      | `len(bank) >= 2`                            |
| Battery Bank | Only digits     | All chars in '123456789'                    |
| Battery      | Rating in 1-9   | Implicit (guaranteed by input)              |
| Battery Pair | i < j           | Loop constraint `for j in range(i+1, n)`    |
| Joltage      | Range 0-99      | Implicit (single digit × 10 + single digit) |
| Total        | Sum of integers | Natural Python sum() behavior               |

## Edge Case Handling

| Case            | Data State  | Expected Behavior           |
| --------------- | ----------- | --------------------------- |
| Empty input     | `""`        | Returns 0 (no banks)        |
| Single bank     | One line    | Process that bank only      |
| Two-digit bank  | `"45"`      | One pair: (0,1) → 45        |
| All same digits | `"5555"`    | All pairs = 55, max = 55    |
| Very long bank  | 100+ digits | O(n²) still acceptable      |
| Single digit    | `"5"`       | Invalid (no pairs possible) |
