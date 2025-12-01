# Data Model: Day 1 Part 2 Solution

**Feature**: Count all zero crossings during dial rotations  
**Date**: December 1, 2025  
**Branch**: `005-day-01-part-2`

## Overview

This document defines the data entities, types, and relationships for the Day 1 Part 2 solution. The model extends Part 1 by adding zero-crossing tracking during rotations.

## Core Entities

### 1. RotationInstruction

Represents a single rotation command from the puzzle input.

**Type Definition**:

```python
RotationInstruction = tuple[str, int]
# Where:
#   [0]: direction ('L' or 'R')
#   [1]: distance (int >= 0)
```

**Fields**:

- `direction`: str - Either 'L' (left/decrease) or 'R' (right/increase)
- `distance`: int - Number of clicks to rotate (non-negative integer)

**Validation Rules**:

- `direction` must be exactly 'L' or 'R' (case-sensitive)
- `distance` must be >= 0 (zero is valid for no-op rotation)
- Parsed from input format: `<direction><distance>` (e.g., "L68", "R1000")

**Examples**:

```python
("L", 68)    # Rotate left 68 clicks
("R", 1000)  # Rotate right 1000 clicks
("L", 0)     # No rotation (edge case)
```

### 2. DialPosition

Represents the current position of the dial on the circular face.

**Type Definition**:

```python
DialPosition = int  # Range: 0-99 (inclusive)
```

**Properties**:

- Circular: wraps at boundaries (after 99 comes 0, before 0 comes 99)
- Modulo 100 arithmetic ensures position is always in valid range
- Starting position: 50 (as specified in puzzle)

**State Transitions**:

```python
# Right rotation (increase)
new_position = (current_position + distance) % 100

# Left rotation (decrease)
new_position = (current_position - distance) % 100
```

**Invariant**: `0 <= position <= 99` at all times (maintained by modulo operation)

### 3. ZeroCrossing

Represents an instance where the dial points at position 0.

**Type Definition**:

```python
# Not a separate class/struct, represented as count (int)
ZeroCrossingCount = int
```

**Categories**:

1. **During-rotation crossing**: Position 0 is traversed while rotating

   - Example: Start at 99, rotate R2 → crosses 0 at click 1
   - Detected via mathematical formula (see research.md)

2. **End-position crossing**: Final position after rotation is 0
   - Example: Start at 52, rotate R48 → ends at 0
   - Detected via simple equality check

**Relationship**:

- Part 1 counts only **end-position crossings**
- Part 2 counts **both during-rotation AND end-position crossings**
- Therefore: `Part2Count >= Part1Count` (mathematical invariant)

### 4. RotationSequence

Represents the full sequence of rotations from puzzle input.

**Type Definition**:

```python
RotationSequence = list[RotationInstruction]
```

**Properties**:

- Ordered list (sequence matters for cumulative rotation)
- Minimum length: 0 (empty input → 0 crossings)
- Maximum length: Unbounded (puzzle-dependent, typically ~10-1000 rotations)

**Processing**:

```python
position = 50  # Initial state
for instruction in sequence:
    # Process each rotation in order
    direction, distance = instruction
    # ... apply rotation and count crossings
```

## Derived Data

### ZeroCrossingDuringRotation

Calculated value: number of times position 0 is crossed while executing a single rotation.

**Calculation**:

```python
def count_zero_crossings_during_rotation(
    start: DialPosition,
    direction: str,
    distance: int
) -> int:
    """
    Returns number of during-rotation crossings for this instruction.
    Does NOT include start or end positions.
    """
    if distance == 0:
        return 0

    if direction == 'R':
        return (start + distance) // 100
    else:  # 'L'
        return max(0, (distance - start + 99) // 100)
```

**Example**:

```
Start: 50, Direction: R, Distance: 1000
→ (50 + 1000) // 100 = 10 crossings during rotation
```

### TotalZeroCrossingCount

Aggregate value: sum of all zero crossings (during + end) across entire sequence.

**Calculation**:

```python
total = 0
position = 50

for direction, distance in sequence:
    # Count during-rotation crossings
    total += count_zero_crossings_during_rotation(position, direction, distance)

    # Apply rotation
    position = (position + distance if direction == 'R'
                else position - distance) % 100

    # Count end-position crossing
    if position == 0:
        total += 1

return total
```

## Data Flow

```
Input File (input.txt)
    ↓
parse_input()
    ↓
RotationSequence: list[RotationInstruction]
    ↓
solve_part2()
    ├─→ DialPosition (state: updated each iteration)
    ├─→ count_zero_crossings_during_rotation() → int
    └─→ ZeroCrossingCount (accumulator)
    ↓
Total Zero Crossing Count (output: int)
```

## Relationships

```
┌─────────────────────┐
│  RotationSequence   │
│  (list)             │
└──────────┬──────────┘
           │ contains *
           ↓
┌─────────────────────┐
│ RotationInstruction │
│ (direction, dist)   │
└──────────┬──────────┘
           │ modifies
           ↓
┌─────────────────────┐
│   DialPosition      │
│   (0-99)            │
└──────────┬──────────┘
           │ generates
           ↓
┌─────────────────────┐
│  ZeroCrossing       │
│  (count)            │
└─────────────────────┘
```

## State Transitions

```
State Machine: Dial Rotation Processing

Initial State: position = 50, zero_count = 0

For each rotation (direction, distance):
  ┌─────────────────────────────┐
  │ Count During Crossings      │
  │ zero_count += formula(...)  │
  └─────────┬───────────────────┘
            ↓
  ┌─────────────────────────────┐
  │ Apply Rotation              │
  │ position = (pos ± dist) % 100│
  └─────────┬───────────────────┘
            ↓
  ┌─────────────────────────────┐
  │ Check End Position          │
  │ if position == 0:           │
  │   zero_count += 1           │
  └─────────────────────────────┘

Final State: zero_count = total crossings
```

## Validation Rules

### Input Validation

- Each line must match pattern: `[LR]\d+`
- Empty lines are ignored during parsing
- Invalid format raises parse error

### Runtime Validation

- Direction must be 'L' or 'R' (ValueError if not)
- Distance must be non-negative (guaranteed by parsing `\d+`)
- Position always valid due to modulo operation (no validation needed)

### Output Validation

- Part 2 result >= Part 1 result (mathematical invariant)
- Result >= 0 (zero is valid for sequences with no zero crossings)

## Type Signatures (Python)

```python
from pathlib import Path

# Core types
RotationInstruction = tuple[str, int]
DialPosition = int
RotationSequence = list[RotationInstruction]

# Functions
def parse_input(input_text: str) -> RotationSequence: ...

def apply_rotation(position: DialPosition, direction: str, distance: int) -> DialPosition: ...

def count_zero_crossings_during_rotation(
    start_position: DialPosition,
    direction: str,
    distance: int
) -> int: ...

def solve_part1(rotations: RotationSequence) -> int: ...

def solve_part2(rotations: RotationSequence) -> int: ...
```

## Complexity Analysis

| Entity              | Size          | Storage                       |
| ------------------- | ------------- | ----------------------------- |
| RotationInstruction | ~10 bytes     | O(1)                          |
| DialPosition        | 8 bytes (int) | O(1)                          |
| RotationSequence    | ~10n bytes    | O(n) where n = rotation count |
| ZeroCrossingCount   | 8 bytes (int) | O(1)                          |

**Total Space Complexity**: O(n) dominated by input storage

**Processing Complexity**: O(n) time to process sequence (each rotation is O(1))

## Summary

The data model for Part 2 is minimal and extends Part 1 with:

1. **New calculation**: `count_zero_crossings_during_rotation()` for during-rotation detection
2. **Accumulated count**: Sum of during-crossings + end-position crossings
3. **Backward compatibility**: Part 1 function remains unchanged

All entities use primitive types (int, str, tuple, list) for simplicity and performance. No custom classes needed for this algorithmic solution.
