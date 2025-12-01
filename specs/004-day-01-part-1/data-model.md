# Data Model: Day 1 Part 1 - Secret Entrance

**Feature**: 004-day-01-part-1  
**Date**: 2025-12-01

## Overview

This document defines the core data entities and their relationships for the Day 1 Part 1 solution. The model is deliberately simple to reflect the straightforward nature of the puzzle.

## Entities

### 1. Rotation

Represents a single rotation instruction from the puzzle input.

**Fields**:
- `direction`: str - Either 'L' (left) or 'R' (right)
- `distance`: int - Number of clicks to rotate (≥ 0)

**Validation Rules**:
- `direction` must be exactly 'L' or 'R' (case-sensitive)
- `distance` must be a non-negative integer
- `distance` is not bounded (puzzle doesn't specify max)

**Representation**:
```python
Rotation = tuple[str, int]
# Example: ('L', 68) or ('R', 48)
```

**Why tuple instead of class**:
- Immutable - rotations don't change
- Simple - only two fields
- Lightweight - thousands of rotations in memory
- Pythonic - clean unpacking in loops

---

### 2. DialState

Represents the current state of the dial during rotation sequence processing.

**Fields**:
- `position`: int - Current dial position (0-99 inclusive)
- `zero_count`: int - Number of times dial has pointed at 0 (≥ 0)

**Invariants**:
- `position` is always in range [0, 99]
- `zero_count` increments by 1 each time `position == 0` after a rotation
- Initial state: `position = 50`, `zero_count = 0`

**State Transitions**:
```
Initial: position=50, zero_count=0
After rotation: position=new_position, zero_count=previous + (1 if new_position==0 else 0)
```

**Representation**:
```python
# Option 1: Implicit (no explicit class)
position: int  # Current position
zero_count: int  # Running count

# Option 2: dataclass (if complexity increases)
from dataclasses import dataclass

@dataclass
class DialState:
    position: int
    zero_count: int = 0
```

**Decision**: Use **Option 1** (implicit) for Part 1
- Simpler for single-part puzzle
- Two variables are clear enough
- Can refactor to dataclass in Part 2 if needed

---

### 3. ParsedInput

Collection of rotation instructions parsed from puzzle input.

**Fields**:
- `rotations`: list[Rotation] - Ordered sequence of rotations to apply

**Validation Rules**:
- List may be empty (valid input with no rotations)
- Order matters (rotations applied sequentially)
- No duplicate detection needed (duplicates are allowed)

**Representation**:
```python
ParsedInput = list[tuple[str, int]]
# Example: [('L', 68), ('L', 30), ('R', 48), ...]
```

---

## Data Flow

```
Input File (input.txt)
    ↓
parse_input() → ParsedInput (list[Rotation])
    ↓
solve_part1() → iterates over rotations
    ↓
For each Rotation:
    apply_rotation() → new position (int)
    Check if position == 0
    Increment zero_count if true
    ↓
Final Result: zero_count (int)
```

---

## Type Definitions

```python
"""Type aliases for Day 1 Part 1 solution."""

from typing import Tuple, List

# Core types
Rotation = Tuple[str, int]  # (direction, distance)
Position = int  # 0-99 inclusive
ParsedInput = List[Rotation]

# Function signatures use these types
def parse_input(input_text: str) -> ParsedInput: ...
def apply_rotation(position: Position, direction: str, distance: int) -> Position: ...
def solve_part1(rotations: ParsedInput) -> int: ...
```

---

## Validation Rules

### Input Validation

| Rule | Check | Error Message |
|------|-------|--------------|
| Direction must be L or R | `direction in ('L', 'R')` | `"Invalid direction '{direction}' in line: {line}"` |
| Distance must be numeric | `int(line[1:])` | `"Invalid distance in line: {line}"` |
| Line format | Length ≥ 2 chars | `"Invalid rotation format: {line}"` |

### State Validation

| Rule | Check | When |
|------|-------|------|
| Position in range | `0 <= position < 100` | After each rotation (implicit via modulo) |
| Zero count non-negative | `zero_count >= 0` | Always (monotonically increasing) |

---

## Examples

### Valid Input Examples

```python
# Single rotation
[('L', 68)]

# Multiple rotations (from puzzle example)
[('L', 68), ('L', 30), ('R', 48), ('L', 5), ('R', 60), 
 ('L', 55), ('L', 1), ('L', 99), ('R', 14), ('L', 82)]

# Empty input
[]

# Rotation to same position (L0 or R0)
[('L', 0)]

# Large distance (wraps multiple times)
[('R', 999)]  # 999 % 100 = 99 clicks right from 50 → 49
```

### Invalid Input Examples

```python
# Invalid direction
"X68"  → ValueError: Invalid direction 'X'

# No distance
"L"  → ValueError: Invalid distance in line: L

# Non-numeric distance
"L2A"  → ValueError: Invalid distance in line: L2A

# Empty line (handled gracefully - skipped)
""  → Skipped during parsing
```

---

## Relationships

```
ParsedInput (1) ──contains──> (0..n) Rotation
                                    │
                                    │ applied to
                                    ↓
                              DialState
                                    │
                                    │ produces
                                    ↓
                              Final Count (int)
```

**Cardinality**:
- One ParsedInput contains zero or more Rotations
- Each Rotation is applied to one DialState sequentially
- Final count is a single integer result

---

## Implementation Notes

### Memory Considerations
- **ParsedInput**: O(n) where n = number of rotations
- **DialState**: O(1) - only two integers
- **Total**: O(n) dominated by input storage

### Performance Characteristics
- **Parsing**: O(n) - linear scan of input lines
- **Rotation**: O(1) - constant time modulo arithmetic
- **Total**: O(n) - optimal for sequential processing

### Thread Safety
- Not applicable - single-threaded execution
- Rotations are sequential by nature

---

## Future Considerations (Part 2)

Part 2 requirements are not yet known, but potential data model extensions:

- **History tracking**: Store position after each rotation
- **Multi-dial support**: Track multiple dials simultaneously  
- **Undo operations**: Need to store rotation history
- **Complex state**: Might need DialState dataclass

**Current design supports easy extension**:
- Type aliases make refactoring straightforward
- Function signatures are stable
- Can add DialState class without changing existing code

---

## Validation Against Requirements

| Requirement | Data Model Support |
|------------|-------------------|
| FR-001: Accept rotation sequence | ✅ ParsedInput = list[Rotation] |
| FR-002: Start at 50, apply in order | ✅ Initial position=50, sequential processing |
| FR-003: Count zeros | ✅ zero_count field in DialState |
| FR-004: Handle invalid input | ✅ Validation rules defined |
| FR-006: Circular 0-99 | ✅ Position type constrained, modulo arithmetic |
| FR-007: Ignore empty lines | ✅ Parsing logic skips empty lines |

---

## Summary

**Key Design Decisions**:
1. ✅ Use tuples for Rotation (lightweight, immutable)
2. ✅ Implicit DialState (two variables vs. class)
3. ✅ Type aliases for documentation and clarity
4. ✅ Validation raises ValueError with clear messages

**All entities defined and validated against functional requirements.**
