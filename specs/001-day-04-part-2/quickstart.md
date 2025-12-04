# Quickstart: Day 4 Part 2 - Printing Department

**Feature**: Iterative removal of accessible paper rolls  
**Branch**: `001-day-04-part-2`  
**Date**: 2025-12-04

---

## Overview

Implement Part 2 of Day 4: an iterative algorithm that removes accessible paper rolls (< 4 neighbors) and continues until no more rolls can be accessed. The solution uses an optimized dictionary-based approach to track roll positions and neighbor counts.

---

## Prerequisites

- Existing Day 4 Part 1 solution in `day-04/solution.py`
- Python 3.10+ environment with `pytest`
- UV package manager configured
- Branch `001-day-04-part-2` checked out

---

## Quick Start

### 1. Review Planning Documents

```powershell
# Read research decisions
cat specs/001-day-04-part-2/research.md

# Review data model
cat specs/001-day-04-part-2/data-model.md

# Check algorithm contract
cat specs/001-day-04-part-2/contracts/solve_part2.md
```

### 2. Run Existing Part 1 Tests (Baseline)

```powershell
cd day-04
uv run pytest test_solution.py -v
```

**Expected**: All Part 1 tests pass ✅

### 3. Create Part 2 Tests (RED phase)

Add to `day-04/test_solution.py`:

```python
def test_example_part2():
    """Test Part 2 with sample expecting 43 total removed."""
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
    result = solve_part2(input_data)
    assert result == 43, f"Expected 43 total removed, got {result}"

def test_all_isolated_part2():
    """Test Part 2 where all rolls removed in one iteration."""
    input_data = "@.@\n...\n@.@"
    result = solve_part2(input_data)
    assert result == 4, f"Expected 4 removed, got {result}"
```

### 4. Verify Tests Fail (RED)

```powershell
uv run pytest test_solution.py::test_example_part2 -v
```

**Expected**: `NameError: name 'solve_part2' is not defined` ❌

### 5. Implement `solve_part2()` (GREEN phase)

Add to `day-04/solution.py`:

```python
def solve_part2(input_data: str) -> int:
    """
    Solve Day 4 Part 2: Count total removable paper rolls.

    Iteratively removes accessible rolls (< 4 neighbors) until
    no more rolls can be accessed.

    Args:
        input_data: Multiline string containing grid

    Returns:
        Total count of removed paper rolls
    """
    grid = parse_grid(input_data)
    if not grid:
        return 0

    # Initialize roll tracker: {(row, col): neighbor_count}
    rolls: dict[tuple[int, int], int] = {}
    for row, row_str in enumerate(grid):
        for col, val in enumerate(row_str):
            if val == "@":
                rolls[(row, col)] = count_adjacent_rolls(grid, row, col)

    total_removed = 0

    # Iterative removal
    while True:
        # Find accessible rolls (< 4 neighbors)
        accessible = {pos for pos, count in rolls.items() if count < 4}

        # Termination check
        if not accessible:
            break

        # Remove accessible rolls
        for pos in accessible:
            del rolls[pos]
            row, col = pos

            # Update neighbor counts for surrounding positions
            for dr, dc in DIRECTIONS:
                neighbor_pos = (row + dr, col + dc)
                if neighbor_pos in rolls:
                    rolls[neighbor_pos] -= 1

        total_removed += len(accessible)

    return total_removed
```

### 6. Run Tests (GREEN)

```powershell
uv run pytest test_solution.py -v
```

**Expected**: All tests pass ✅

### 7. Update Main Block

Add Part 2 output to `day-04/solution.py`:

```python
if __name__ == "__main__":
    with open("day-04/input.txt") as f:
        input_data = f.read()

    part1_result = solve_part1(input_data)
    part2_result = solve_part2(input_data)

    print(f"Part 1: {part1_result}")
    print(f"Part 2: {part2_result}")
```

### 8. Run Against Real Input

```powershell
uv run python day-04/solution.py
```

**Expected Output**:

```
Part 1: [some number]
Part 2: [some number]
```

### 9. Submit Answer (Manual)

1. Copy Part 2 result from output
2. Visit https://adventofcode.com/2025/day/4
3. Paste answer in Part 2 submission form
4. Submit manually

---

## TDD Workflow Summary

| Phase        | Action               | Command                                              | Expected Result     |
| ------------ | -------------------- | ---------------------------------------------------- | ------------------- |
| **RED**      | Write failing test   | `uv run pytest test_solution.py::test_example_part2` | ❌ `NameError`      |
| **GREEN**    | Implement solution   | Add `solve_part2()`                                  | ✅ All tests pass   |
| **REFACTOR** | Optimize (if needed) | Run tests after changes                              | ✅ Tests still pass |

---

## Verification Checklist

- [ ] Part 1 tests still pass (regression check)
- [ ] `test_example_part2` returns 43 for sample input
- [ ] `test_all_isolated_part2` returns 4 for isolated rolls
- [ ] Edge cases tested (empty grid, no accessible rolls)
- [ ] Real input produces valid answer
- [ ] Code follows PEP8 (run `ruff check day-04/`)
- [ ] All functions have docstrings
- [ ] Performance acceptable (< 1 second for real input)

---

## Key Files

| File                                    | Purpose                             |
| --------------------------------------- | ----------------------------------- |
| `day-04/solution.py`                    | Implementation (Part 1 + Part 2)    |
| `day-04/test_solution.py`               | Tests (Part 1 + Part 2)             |
| `day-04/input.txt`                      | Real puzzle input                   |
| `day-04/test_input.txt`                 | Sample input for testing            |
| `specs/001-day-04-part-2/plan.md`       | This implementation plan            |
| `specs/001-day-04-part-2/research.md`   | Algorithm research and decisions    |
| `specs/001-day-04-part-2/data-model.md` | Data structures and transformations |

---

## Troubleshooting

### Tests fail with wrong count

**Problem**: `test_example_part2` fails with incorrect total

**Solution**:

1. Verify neighbor count updates are correct (decrement by 1 for each removed neighbor)
2. Ensure all 8 directions are checked when updating neighbors
3. Confirm termination condition (accessible set empty, not rolls dict empty)

### Infinite loop

**Problem**: Algorithm never terminates

**Solution**:

1. Add iteration counter and debug print:
   ```python
   iteration = 0
   while True:
       iteration += 1
       if iteration > 100:  # Safety check
           raise RuntimeError(f"Too many iterations")
   ```
2. Verify accessible set is actually being removed from rolls dict
3. Check that neighbor counts are being decremented correctly

### Performance issues

**Problem**: Solution takes > 1 second

**Solution**:

1. Ensure you're using dictionary, not rescanning grid each iteration
2. Verify you're not recreating accessible set unnecessarily
3. Profile with:
   ```python
   import time
   start = time.time()
   result = solve_part2(input_data)
   print(f"Time: {time.time() - start:.3f}s")
   ```

---

## Next Steps

After completing Part 2:

1. **Commit changes**:

   ```powershell
   git add day-04/solution.py day-04/test_solution.py
   git commit -m "feat: solve day 04 part 2"
   ```

2. **Update progress tracker** in `README.md`:

   ```markdown
   | Day | Part 1 | Part 2 | Notes                       |
   | --- | ------ | ------ | --------------------------- |
   | 4   | ✅     | ✅     | Optimized iterative removal |
   ```

3. **Clean up** (optional):

   ```powershell
   ruff format day-04/solution.py
   ruff check day-04/solution.py --fix
   ```

4. **Document learnings** in `day-04/README.md` (optional):
   - Algorithm approach (dictionary-based tracking)
   - Performance optimization (avoid full grid scans)
   - Edge cases discovered

---

## References

- **Problem Description**: `day-04/description.md`
- **Feature Spec**: `specs/001-day-04-part-2/spec.md`
- **Algorithm Research**: `specs/001-day-04-part-2/research.md`
- **AoC Day 4**: https://adventofcode.com/2025/day/4
