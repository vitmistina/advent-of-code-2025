# Quick Start: Day 4 Part 1 - Accessible Paper Rolls Counter

**Feature**: Count accessible paper rolls on a grid  
**Estimated Time**: 30-45 minutes (following TDD workflow)  
**Difficulty**: Easy-Medium

## Prerequisites

- Python 3.10+ installed
- UV package manager configured
- Repository cloned and dependencies installed
- Advent of Code session token in `.env` file

## Workflow Overview

This guide follows the **Red-Green-Refactor** TDD cycle mandated by the constitution.

```
1. Setup (5 min)
2. RED: Write Tests (10 min)
3. GREEN: Implement Solution (15-20 min)
4. REFACTOR: Optimize (5-10 min)
5. Submit (5 min)
```

---

## Step 1: Setup (5 minutes)

### Download Challenge Files

```bash
# Run meta runner to download challenge description and inputs
uv run -m cli.meta_runner download --day 4
```

**Expected Output**:

- `day-04/` folder created
- `day-04/input.txt` downloaded
- `day-04/test_input.txt` generated from example
- `day-04/description.md` saved

### Verify Files

```bash
ls day-04/
# Expected: description.md, input.txt, test_input.txt
```

### Create Solution Skeleton

```bash
# Create empty solution file
touch day-04/solution.py

# Create test file
touch day-04/test_solution.py
```

---

## Step 2: RED Phase - Write Failing Tests (10 minutes)

**Objective**: Write tests FIRST based on puzzle examples, verify they FAIL

### Create Test File: `day-04/test_solution.py`

```python
"""Tests for Day 4 Part 1: Accessible Paper Rolls Counter."""

from solution import solve_part1


def test_example_grid():
    """Test with provided example expecting 13 accessible rolls."""
    input_data = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""

    result = solve_part1(input_data)
    assert result == 13, f"Expected 13 accessible rolls, got {result}"


def test_empty_grid():
    """Test with empty grid."""
    result = solve_part1("")
    assert result == 0, f"Expected 0 for empty grid, got {result}"


def test_single_roll():
    """Test single roll with no neighbors (accessible)."""
    result = solve_part1("@")
    assert result == 1, f"Expected 1 accessible roll, got {result}"


def test_all_accessible():
    """Test grid where all rolls are accessible (< 4 neighbors each)."""
    input_data = """@.@
...
@.@"""
    result = solve_part1(input_data)
    assert result == 4, f"Expected 4 accessible rolls, got {result}"
```

### Run Tests (Should FAIL)

```bash
cd day-04
uv run pytest test_solution.py -v
```

**Expected**: All tests FAIL with `ImportError` or `AttributeError` (function not implemented)

**✅ RED Phase Complete**: Tests written and verified to fail

---

## Step 3: GREEN Phase - Implement Solution (15-20 minutes)

**Objective**: Write minimum code to make tests pass

### Create Solution File: `day-04/solution.py`

```python
"""Day 4 Part 1: Count accessible paper rolls on a grid.

A paper roll is accessible if fewer than 4 rolls exist in its 8 adjacent positions.
"""

from typing import List, Tuple


# Direction offsets for 8 adjacent positions
DIRECTIONS: List[Tuple[int, int]] = [
    (-1, -1), (-1, 0), (-1, 1),  # NW, N, NE
    (0, -1),           (0, 1),    # W,     E
    (1, -1),  (1, 0),  (1, 1)     # SW, S, SE
]


def parse_grid(input_data: str) -> List[str]:
    """Parse input string into grid representation.

    Args:
        input_data: Multiline string containing grid

    Returns:
        List of strings, each representing a row
    """
    if not input_data.strip():
        return []
    return [line.strip() for line in input_data.strip().split('\n')]


def is_valid_position(grid: List[str], row: int, col: int) -> bool:
    """Check if position is within grid boundaries.

    Args:
        grid: The grid representation
        row: Row index to check
        col: Column index to check

    Returns:
        True if position is valid, False otherwise
    """
    if not grid:
        return False
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])


def count_adjacent_rolls(grid: List[str], row: int, col: int) -> int:
    """Count paper rolls in 8 adjacent positions.

    Args:
        grid: The grid representation
        row: Row index of center position
        col: Column index of center position

    Returns:
        Number of adjacent paper rolls (0-8)
    """
    count = 0
    for dr, dc in DIRECTIONS:
        new_row, new_col = row + dr, col + dc
        if is_valid_position(grid, new_row, new_col):
            if grid[new_row][new_col] == '@':
                count += 1
    return count


def is_accessible(adjacent_count: int) -> bool:
    """Determine if a paper roll is accessible.

    Args:
        adjacent_count: Number of adjacent paper rolls

    Returns:
        True if accessible (< 4 neighbors), False otherwise
    """
    return adjacent_count < 4


def solve_part1(input_data: str) -> int:
    """Solve Day 4 Part 1: Count accessible paper rolls.

    Args:
        input_data: Multiline string containing grid

    Returns:
        Count of accessible paper rolls
    """
    grid = parse_grid(input_data)

    if not grid:
        return 0

    accessible_count = 0

    # Check each position in the grid
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            # Only check positions with paper rolls
            if grid[row][col] == '@':
                adjacent = count_adjacent_rolls(grid, row, col)
                if is_accessible(adjacent):
                    accessible_count += 1

    return accessible_count


if __name__ == "__main__":
    # Read input and solve
    with open("input.txt") as f:
        input_data = f.read()

    result = solve_part1(input_data)
    print(f"Part 1: {result}")
```

### Run Tests (Should PASS)

```bash
uv run pytest test_solution.py -v
```

**Expected**: All tests PASS ✅

**✅ GREEN Phase Complete**: Tests passing with working implementation

---

## Step 4: REFACTOR Phase - Optimize (5-10 minutes)

**Objective**: Clean up code while keeping tests green

### Potential Refactorings

1. **Performance**: Already O(n) - no optimization needed for typical inputs
2. **Readability**: Code is clear with good function decomposition
3. **Documentation**: All functions have docstrings ✅

### Run Tests After Refactoring

```bash
uv run pytest test_solution.py -v
```

**Expected**: Tests still PASS after any refactoring

**✅ REFACTOR Phase Complete**: Code clean and tests green

---

## Step 5: Run Against Actual Input (5 minutes)

### Execute Solution

```bash
uv run day-04/solution.py
```

**Expected Output**:

```
Part 1: [YOUR ANSWER]
```

### Verify Answer

1. Copy the output number
2. Go to [Advent of Code Day 4](https://adventofcode.com/2025/day/4)
3. Paste answer in Part 1 submission box
4. Submit manually (as required by constitution)

---

## Step 6: Commit & Document

### Commit Changes

```bash
git add day-04/
git commit -m "feat: solve day 4 part 1 - accessible paper rolls counter"
git push origin 011-day-04-part-1
```

### Update Progress Tracker

Edit `README.md` to mark Day 4 Part 1 as complete:

```markdown
## Progress

| Day | Part 1 | Part 2 | Notes                   |
| --- | ------ | ------ | ----------------------- |
| 4   | ✅     | ⬜     | Grid adjacency counting |
```

---

## Troubleshooting

### Tests Fail with Import Error

**Problem**: `ImportError: cannot import name 'solve_part1'`

**Solution**: Ensure `solution.py` exists and defines `solve_part1` function

### Wrong Answer on Example

**Problem**: Test expects 13 but got different number

**Debug Steps**:

1. Verify grid parsing: `grid = parse_grid(input_data); print(len(grid), len(grid[0]))`
2. Check boundary logic: Ensure out-of-bounds positions return False
3. Verify threshold: Must be `< 4` not `<= 4`
4. Check directions: Should have exactly 8 direction tuples

### Performance Issues

**Problem**: Solution takes too long on actual input

**Solutions**:

- Verify you're not re-parsing grid multiple times
- Ensure boundary checks happen before grid access
- Check for infinite loops in adjacency counting

---

## Testing Checklist

- [ ] Tests written BEFORE implementation
- [ ] Tests verified to FAIL initially (RED)
- [ ] Implementation makes tests PASS (GREEN)
- [ ] Code refactored while maintaining green tests (REFACTOR)
- [ ] Example test case passes (13 accessible rolls)
- [ ] Edge cases tested (empty grid, single roll)
- [ ] Actual input processed successfully
- [ ] Answer submitted manually to AoC website

---

## Next Steps

After completing Part 1:

1. **Wait for Part 2**: AoC unlocks Part 2 after Part 1 submission
2. **Run meta runner**: Download Part 2 description when available
3. **Follow TDD cycle**: RED → GREEN → REFACTOR for Part 2
4. **Reuse helpers**: Many Part 1 functions may be useful for Part 2

---

## Time Estimates by Phase

| Phase     | Estimated Time | Critical Success Factor                    |
| --------- | -------------- | ------------------------------------------ |
| Setup     | 5 min          | Meta runner configured properly            |
| RED       | 10 min         | Tests comprehensive, verified to fail      |
| GREEN     | 15-20 min      | Focus on making tests pass, not perfection |
| REFACTOR  | 5-10 min       | Keep tests green during cleanup            |
| Submit    | 5 min          | Manual submission following AoC rules      |
| **Total** | **40-50 min**  | TDD discipline maintained                  |

---

## References

- **Specification**: `specs/011-day-04-part-1/spec.md`
- **Data Model**: `specs/011-day-04-part-1/data-model.md`
- **Contracts**: `specs/011-day-04-part-1/contracts/function-interface.md`
- **Research**: `specs/011-day-04-part-1/research.md`
- **Constitution**: `.specify/memory/constitution.md`
