# Quickstart: Day 1 Part 1 - Secret Entrance

**Feature**: 004-day-01-part-1  
**Date**: 2025-12-01

## Overview

This quickstart guide helps developers get up to speed on implementing the Day 1 Part 1 solution using Test-Driven Development.

---

## Prerequisites

**Required**:
- Python 3.10 or higher
- UV package manager (already installed)
- Git (for commits)

**Installed**:
- pytest (in dev dependencies)
- ruff (for linting/formatting)

**Environment Setup**:
```bash
# Verify Python version
python --version  # Should be 3.10+

# Virtual environment is managed by UV
# No manual activation needed when using `uv run`
```

---

## Project Structure

```
day-01/
├── solution.py          # Main solution (implement here)
├── test_solution.py     # Tests (write here first - TDD!)
├── input.txt            # Actual puzzle input
├── test_input.txt       # Sample input from puzzle
└── description.md       # Puzzle description (reference)
```

---

## Quick Start (5 minutes)

### 1. Read the Puzzle Description

```bash
# Open and read the puzzle description
code day-01/description.md
```

**Key Points**:
- Dial has positions 0-99 (circular)
- Starts at position 50
- Rotations format: `L<distance>` or `R<distance>`
- Count how many times dial lands on 0

### 2. Review the Spec

```bash
# Open the feature specification
code specs/004-day-01-part-1/spec.md
```

**Key Requirements** (FR-001 to FR-007):
- Parse rotation instructions (L/R + distance)
- Apply rotations with circular wraparound
- Count zeros after each rotation
- Handle invalid input gracefully

### 3. Review Contracts & Data Model

```bash
# Study the API contracts
code specs/004-day-01-part-1/contracts/api-contract.md

# Study the data model
code specs/004-day-01-part-1/data-model.md
```

**Core Functions to Implement**:
```python
parse_input(input_text: str) -> list[tuple[str, int]]
apply_rotation(position: int, direction: str, distance: int) -> int
solve_part1(rotations: list[tuple[str, int]]) -> int
```

---

## TDD Workflow (RED-GREEN-REFACTOR)

### Phase 1: RED - Write Failing Tests

**Start here**: `day-01/test_solution.py`

```bash
# Open test file
code day-01/test_solution.py
```

**Write tests FIRST**:

```python
def test_parse_input_sample(test_input):
    """Test parsing the sample input."""
    data = parse_input(test_input)
    assert len(data) == 10
    assert data[0] == ('L', 68)
    assert data[2] == ('R', 48)

def test_apply_rotation_left():
    """Test left rotation."""
    assert apply_rotation(50, 'L', 68) == 82
    assert apply_rotation(82, 'L', 30) == 52

def test_apply_rotation_right():
    """Test right rotation."""
    assert apply_rotation(52, 'R', 48) == 0

def test_apply_rotation_wraparound():
    """Test wraparound at boundaries."""
    assert apply_rotation(5, 'L', 10) == 95  # Left from 0
    assert apply_rotation(99, 'R', 1) == 0   # Right from 99

def test_solve_part1_sample(parsed_test_data):
    """Test Part 1 with sample input - should return 3."""
    result = solve_part1(parsed_test_data)
    assert result == 3
```

**Run tests (should FAIL)**:
```bash
uv run pytest day-01/test_solution.py -v
```

**Expected**: Tests fail because functions are not implemented yet. This is CORRECT for TDD!

---

### Phase 2: GREEN - Implement to Pass Tests

**Now implement**: `day-01/solution.py`

```bash
# Open solution file
code day-01/solution.py
```

**Implement functions**:

```python
def parse_input(input_text: str) -> list[tuple[str, int]]:
    """Parse rotation instructions from puzzle input."""
    rotations = []
    for line in input_text.strip().split('\n'):
        if not line.strip():
            continue
        direction = line[0]
        if direction not in ('L', 'R'):
            raise ValueError(f"Invalid direction '{direction}' in line: {line}")
        try:
            distance = int(line[1:])
        except ValueError:
            raise ValueError(f"Invalid distance in line: {line}")
        rotations.append((direction, distance))
    return rotations


def apply_rotation(position: int, direction: str, distance: int) -> int:
    """Apply a single rotation to the dial."""
    if direction not in ('L', 'R'):
        raise ValueError(f"Direction must be 'L' or 'R', got: {direction}")
    
    if direction == 'L':
        return (position - distance) % 100
    else:  # direction == 'R'
        return (position + distance) % 100


def solve_part1(rotations: list[tuple[str, int]]) -> int:
    """Count how many times dial points at 0 after rotations."""
    position = 50  # Dial starts at 50
    zero_count = 0
    
    for direction, distance in rotations:
        position = apply_rotation(position, direction, distance)
        if position == 0:
            zero_count += 1
    
    return zero_count
```

**Run tests (should PASS)**:
```bash
uv run pytest day-01/test_solution.py -v
```

**Expected**: All tests pass! ✅

---

### Phase 3: REFACTOR - Clean Up

**Check**:
- ✅ Code is readable
- ✅ No duplication
- ✅ Type hints present
- ✅ Docstrings clear
- ✅ PEP 8 compliant

**Run linter**:
```bash
uv run ruff check day-01/solution.py
uv run ruff format day-01/solution.py
```

**Re-run tests** (must still pass):
```bash
uv run pytest day-01/test_solution.py -v
```

---

## Running the Solution

### Test with Sample Input

```bash
# Verify test_input.txt has the sample from puzzle
cat day-01/test_input.txt

# Run solution against test input
uv run day-01/solution.py
```

**Expected Output**:
```
Part 1: 3
Part 2: 0
```

### Test with Actual Input

```bash
# Run against actual puzzle input
uv run day-01/solution.py
```

**Expected**: Actual answer (to be submitted manually)

---

## Common Issues & Solutions

### Issue: Tests fail with "Module not found"

**Solution**: Use pytest from the day folder or use module syntax
```bash
# From repo root
uv run pytest day-01/test_solution.py

# Or from day-01 folder
cd day-01
uv run pytest test_solution.py
```

### Issue: Modulo gives unexpected results

**Check**: Python's modulo handles negatives correctly
```python
# Python modulo always returns non-negative for positive divisor
(-5) % 100 == 95  # ✅ Correct
```

### Issue: Wrong zero count

**Debug**: Print positions after each rotation
```python
for direction, distance in rotations:
    position = apply_rotation(position, direction, distance)
    print(f"{direction}{distance} → {position}")
    if position == 0:
        zero_count += 1
```

---

## Performance Tips

**Not needed for Part 1**, but good to know:

```python
# Current implementation is already optimal: O(n)
# No optimization needed unless Part 2 requires it

# For profiling (if needed):
import time
start = time.time()
result = solve_part1(rotations)
print(f"Time: {time.time() - start:.3f}s")
```

---

## Next Steps After Part 1

1. ✅ Verify solution works with test input (returns 3)
2. ✅ Run against actual input
3. ✅ Submit answer to Advent of Code website (MANUALLY)
4. ✅ Update README.md progress tracker
5. ✅ Commit: `git commit -m "feat: solve day 01 part 1"`
6. ⏳ Wait for Part 2 to unlock
7. ⏳ Repeat TDD process for Part 2

---

## Testing Checklist

Before submitting, verify:

- [ ] All tests pass: `uv run pytest day-01/test_solution.py -v`
- [ ] Linter passes: `uv run ruff check day-01/`
- [ ] Test input returns 3
- [ ] Actual input returns a number
- [ ] Code has type hints
- [ ] Code has docstrings
- [ ] Edge cases tested (empty input, wraparound, invalid input)

---

## Key Resources

**Local Files**:
- `specs/004-day-01-part-1/spec.md` - Feature specification
- `specs/004-day-01-part-1/contracts/api-contract.md` - Function contracts
- `specs/004-day-01-part-1/data-model.md` - Data structures
- `specs/004-day-01-part-1/research.md` - Implementation decisions
- `day-01/description.md` - Puzzle description

**Constitution**:
- `.specify/memory/constitution.md` - Project rules and principles

**Commands**:
```bash
# Run tests
uv run pytest day-01/test_solution.py -v

# Run solution
uv run day-01/solution.py

# Lint code
uv run ruff check day-01/

# Format code
uv run ruff format day-01/

# Run all tests in project
uv run pytest
```

---

## Tips for Success

1. **Read the puzzle carefully** - Edge cases are in the description
2. **Write tests first** - TDD ensures you understand the problem
3. **Start simple** - Solve for test input, then optimize
4. **Use the REPL** - Quick experiments: `python -i day-01/solution.py`
5. **Trust the modulo** - Python's `%` handles circular arithmetic correctly
6. **Verify manually** - Walk through the sample by hand once

---

**Time Estimate**: 30-60 minutes for Part 1 with TDD approach

**Ready to start?** Open `day-01/test_solution.py` and write your first failing test! 🚀
