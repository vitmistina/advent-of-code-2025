# API Contract: Day 1 Part 1 - Secret Entrance

**Feature**: 004-day-01-part-1  
**Date**: 2025-12-01

## Overview

This document defines the function signatures, input/output contracts, and behavior specifications for all public functions in the Day 1 Part 1 solution.

---

## Core Functions

### `parse_input(input_text: str) -> list[tuple[str, int]]`

**Purpose**: Parse puzzle input into structured rotation instructions.

**Input**:
- `input_text`: str
  - Multi-line string from puzzle input file
  - Each line format: `<direction><distance>` (e.g., "L68", "R48")
  - May contain empty lines (will be ignored)

**Output**:
- `list[tuple[str, int]]`
  - List of rotation tuples (direction, distance)
  - Direction: 'L' or 'R'
  - Distance: non-negative integer
  - Empty list if no valid rotations

**Behavior**:
- Strips leading/trailing whitespace from input
- Splits on newlines
- Skips empty lines after stripping
- Validates direction is 'L' or 'R'
- Parses distance as integer
- Preserves order of rotations

**Exceptions**:
- `ValueError`: If line has invalid direction (not L or R)
  - Message: `"Invalid direction '{direction}' in line: {line}"`
- `ValueError`: If line has non-numeric distance
  - Message: `"Invalid distance in line: {line}"`

**Example**:
```python
input_text = """L68
L30
R48"""
result = parse_input(input_text)
assert result == [('L', 68), ('L', 30), ('R', 48)]
```

**Edge Cases**:
```python
# Empty input
parse_input("") == []

# Only empty lines
parse_input("\n\n\n") == []

# Mixed empty and valid lines
parse_input("L10\n\nR20") == [('L', 10), ('R', 20)]

# Invalid direction
parse_input("X10") → ValueError

# Invalid distance
parse_input("L10A") → ValueError
```

---

### `apply_rotation(position: int, direction: str, distance: int) -> int`

**Purpose**: Apply a single rotation to the dial and return the new position.

**Input**:
- `position`: int
  - Current dial position (0-99)
  - Precondition: `0 <= position < 100`
- `direction`: str
  - Either 'L' (left/decrease) or 'R' (right/increase)
- `distance`: int
  - Number of clicks to rotate
  - Typically non-negative, but function handles negative as reverse

**Output**:
- `int`
  - New dial position after rotation (0-99)
  - Postcondition: `0 <= result < 100`

**Behavior**:
- Left rotation ('L'): `new_position = (position - distance) % 100`
- Right rotation ('R'): `new_position = (position + distance) % 100`
- Wraps around correctly at boundaries (0 ↔ 99)

**Exceptions**:
- `ValueError`: If direction not in ('L', 'R')
  - Message: `"Direction must be 'L' or 'R', got: {direction}"`

**Example**:
```python
# Basic rotations
apply_rotation(50, 'L', 68) == 82
apply_rotation(82, 'L', 30) == 52
apply_rotation(52, 'R', 48) == 0

# Wraparound cases
apply_rotation(5, 'L', 10) == 95   # Wraps from 0 to 99
apply_rotation(99, 'R', 1) == 0    # Wraps from 99 to 0

# No movement
apply_rotation(50, 'L', 0) == 50
apply_rotation(50, 'R', 0) == 50

# Multiple wraps
apply_rotation(10, 'L', 250) == 60  # (10 - 250) % 100 = -240 % 100 = 60
apply_rotation(10, 'R', 250) == 60  # (10 + 250) % 100 = 260 % 100 = 60
```

**Edge Cases**:
```python
# Position at boundaries
apply_rotation(0, 'L', 1) == 99
apply_rotation(99, 'R', 1) == 0

# Large distance
apply_rotation(50, 'R', 999) == 49  # (50 + 999) % 100 = 1049 % 100 = 49

# Invalid direction
apply_rotation(50, 'X', 10) → ValueError
```

---

### `solve_part1(rotations: list[tuple[str, int]]) -> int`

**Purpose**: Count how many times dial points at 0 after any rotation in the sequence.

**Input**:
- `rotations`: list[tuple[str, int]]
  - Sequence of rotation instructions
  - Each tuple: (direction, distance)
  - May be empty list

**Output**:
- `int`
  - Count of times dial pointed at 0 after a rotation
  - Zero or positive integer
  - Does NOT count initial position (dial starts at 50)

**Behavior**:
- Initialize position to 50, zero_count to 0
- For each rotation in sequence:
  1. Apply rotation to get new position
  2. If new position == 0, increment zero_count
- Return zero_count

**Exceptions**:
- None (assumes valid input from parse_input)

**Example**:
```python
# Puzzle example (should return 3)
rotations = [
    ('L', 68), ('L', 30), ('R', 48),  # → 0 (count=1)
    ('L', 5), ('R', 60), ('L', 55),   # → 0 (count=2)
    ('L', 1), ('L', 99),              # → 0 (count=3)
    ('R', 14), ('L', 82)
]
assert solve_part1(rotations) == 3

# No zeros
rotations = [('L', 10), ('R', 5)]
assert solve_part1(rotations) == 0

# Empty input
assert solve_part1([]) == 0

# Single rotation to zero
assert solve_part1([('R', 50)]) == 1  # 50 + 50 = 100 % 100 = 0
```

**Edge Cases**:
```python
# All rotations land on zero
rotations = [('R', 50), ('R', 100), ('L', 100)]
# 50→0 (count=1), 0→0 (count=2), 0→0 (count=3)
assert solve_part1(rotations) == 3

# Rotation stays at current position
rotations = [('L', 0), ('R', 0)]
assert solve_part1(rotations) == 0

# Large number of rotations
rotations = [('R', 1)] * 10000  # Many rotations
result = solve_part1(rotations)  # Should complete in <2s
```

---

## Helper Functions (Optional)

These functions are not required but may improve code organization:

### `parse_rotation_line(line: str) -> tuple[str, int]`

**Purpose**: Parse a single rotation line.

**Input**: `line: str` - Single line like "L68"

**Output**: `tuple[str, int]` - (direction, distance)

**Exceptions**: `ValueError` on invalid format

**Note**: This is internal to parse_input() and may not be exposed publicly.

---

## Main Entry Point

### `main() -> None`

**Purpose**: Main execution entry point for the solution script.

**Behavior**:
1. Read input from `day-01/input.txt`
2. Parse input into rotations
3. Solve Part 1
4. Print result: `"Part 1: {answer}"`
5. (Part 2 will be added after Part 1 completion)

**Example Output**:
```
Part 1: 123
Part 2: 0
```

**Exceptions**: May raise if input file not found or invalid.

---

## Contract Summary Table

| Function | Input Types | Output Type | Can Raise | Complexity |
|----------|-------------|-------------|-----------|------------|
| `parse_input` | str | list[tuple[str, int]] | ValueError | O(n) |
| `apply_rotation` | int, str, int | int | ValueError | O(1) |
| `solve_part1` | list[tuple[str, int]] | int | - | O(n) |
| `main` | - | None | IOError | O(n) |

---

## Validation Against Requirements

| Requirement | Contract Support |
|------------|-----------------|
| FR-001: Accept rotation sequence | ✅ `parse_input` returns list of rotations |
| FR-002: Start at 50, apply in order | ✅ `solve_part1` initializes at 50, iterates sequentially |
| FR-003: Count zeros | ✅ `solve_part1` returns count |
| FR-004: Handle invalid input | ✅ `parse_input` raises ValueError with clear messages |
| FR-005: Process large files | ✅ O(n) complexity, efficient implementation |
| FR-006: Circular wraparound | ✅ `apply_rotation` uses modulo 100 |
| FR-007: Ignore empty lines | ✅ `parse_input` skips empty after strip |

---

## Testing Contract

Each function contract above implies test cases:

### `parse_input` Tests
- ✅ Valid multi-line input
- ✅ Empty input
- ✅ Empty lines mixed with valid
- ✅ Invalid direction raises ValueError
- ✅ Invalid distance raises ValueError

### `apply_rotation` Tests
- ✅ Left rotation (no wrap)
- ✅ Right rotation (no wrap)
- ✅ Left wraparound (0→99)
- ✅ Right wraparound (99→0)
- ✅ Zero distance (no movement)
- ✅ Large distance (multiple wraps)
- ✅ Invalid direction raises ValueError

### `solve_part1` Tests
- ✅ Puzzle example (returns 3)
- ✅ Empty rotations (returns 0)
- ✅ No zeros in sequence (returns 0)
- ✅ All rotations to zero
- ✅ Large rotation count (performance)

---

## Type Hints Summary

```python
from typing import Tuple, List

Rotation = Tuple[str, int]
ParsedInput = List[Rotation]
Position = int

def parse_input(input_text: str) -> ParsedInput: ...
def apply_rotation(position: Position, direction: str, distance: int) -> Position: ...
def solve_part1(rotations: ParsedInput) -> int: ...
def main() -> None: ...
```

---

## Notes

- All contracts assume Python 3.10+ (tuple[...] syntax)
- Docstrings should mirror these contracts
- Type hints are mandatory per Constitution Principle I
- Error messages should be descriptive per Constitution Principle IX

**All contracts defined and ready for TDD implementation.**
