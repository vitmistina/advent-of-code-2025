# Quickstart: Day 2 Part 2 - Invalid Product ID Detection (Extended Pattern)

**Feature**: Day 2 Part 2 - Invalid Product ID Detection (Extended Pattern)  
**Branch**: `008-day-02-part-2`  
**Date**: December 2, 2025

## Prerequisites

- ✅ Part 1 solution complete and tested (`day-02/solution.py` exists)
- ✅ All Part 1 tests passing (`day-02/test_solution.py`)
- ✅ Input file downloaded (`day-02/input.txt`)
- ✅ Development environment set up (Python 3.10+, pytest, uv)

## Quick Start (5 minutes)

### 1. Verify Part 1 Tests Pass

**CRITICAL**: Before touching any code, ensure Part 1 works:

```bash
# Run Part 1 tests
uv run pytest day-02/test_solution.py::test_solve_part1_example -v

# Run Part 1 solution
uv run python day-02/solution.py --part 1
```

**Expected**: All tests green, Part 1 sum: 1227775554

---

### 2. Understand Part 2 Rule Change

**Part 1 Rule**: Invalid if pattern repeated **exactly 2 times**

- Examples: 55 (5×2), 1010 (10×2), 123123 (123×2)

**Part 2 Rule**: Invalid if pattern repeated **at least 2 times**

- Includes all Part 1 invalids PLUS:
  - 111 (1×3), 999 (9×3), 565656 (56×3), 824824824 (824×3), 2121212121 (21×5)

**Key Insight**: Part 2 is a superset of Part 1!

---

### 3. TDD Workflow Overview

Follow strict RED → GREEN → REFACTOR cycle:

1. **RED Phase**: Write failing tests for Part 2
2. **GREEN Phase**: Implement minimum code to pass tests
3. **REFACTOR Phase**: Clean up while keeping tests green
4. **VERIFY Phase**: Ensure Part 1 tests still pass

---

## Detailed TDD Workflow

### RED Phase: Write Failing Tests

**Step 1**: Add Part 2 test cases to `day-02/test_solution.py`

```python
# Add to test_solution.py

def test_is_invalid_id_part2():
    """Test Part 2 pattern detection (at least twice)."""
    # Part 1 overlap (exactly twice - still invalid in Part 2)
    assert is_invalid_id_part2(11) == True
    assert is_invalid_id_part2(22) == True
    assert is_invalid_id_part2(1010) == True

    # NEW in Part 2 (three or more times)
    assert is_invalid_id_part2(111) == True    # 1×3
    assert is_invalid_id_part2(999) == True    # 9×3
    assert is_invalid_id_part2(565656) == True  # 56×3
    assert is_invalid_id_part2(824824824) == True  # 824×3
    assert is_invalid_id_part2(2121212121) == True  # 21×5

    # Still valid
    assert is_invalid_id_part2(101) == False
    assert is_invalid_id_part2(12345) == False

def test_check_range_part2():
    """Test range checking with Part 2 rules."""
    assert check_range_part2(11, 22) == [11, 22]
    assert check_range_part2(95, 115) == [99, 111]  # 111 NEW in Part 2
    assert check_range_part2(998, 1012) == [999, 1010]  # 999 NEW in Part 2
    assert check_range_part2(1698522, 1698528) == []

def test_solve_part2_example():
    """Test Part 2 with complete example input."""
    example = (
        "11-22,95-115,998-1012,1188511880-1188511890,"
        "222220-222224,1698522-1698528,446443-446449,"
        "38593856-38593862,565653-565659,824824821-824824827,"
        "2121212118-2121212124"
    )
    assert solve_part2(example) == 4174379265
```

**Step 2**: Run tests - they should FAIL

```bash
uv run pytest day-02/test_solution.py::test_is_invalid_id_part2 -v
```

**Expected Output**: `NameError: name 'is_invalid_id_part2' is not defined`

**✅ RED Phase Complete**: Tests written and failing as expected

---

### GREEN Phase: Implement Solution

**Step 1**: Add `is_invalid_id_part2()` function to `day-02/solution.py`

```python
def is_invalid_id_part2(num: int) -> bool:
    """
    Check if a number is invalid using Part 2 rules.

    A number is invalid if it consists of a digit sequence repeated
    at least twice (e.g., 111 = "1"×3, 565656 = "56"×3).

    Args:
        num: Product ID to check

    Returns:
        True if invalid (repeated pattern ≥2), False otherwise
    """
    s = str(num)
    n = len(s)

    # Check all possible pattern lengths (1 to n/2)
    for pattern_len in range(1, n // 2 + 1):
        if n % pattern_len == 0:  # Length divisible by pattern
            pattern = s[:pattern_len]
            repetitions = n // pattern_len

            # Check if repeating pattern forms the string
            if pattern * repetitions == s and repetitions >= 2:
                return True  # Found repeated pattern

    return False  # No repeated pattern found
```

**Step 2**: Add helper function `check_range_part2()`

```python
def check_range_part2(start: int, end: int) -> list[int]:
    """
    Find all invalid IDs in a range using Part 2 rules.

    Args:
        start: First ID in range (inclusive)
        end: Last ID in range (inclusive)

    Returns:
        List of invalid product IDs in the range
    """
    invalid = []
    for num in range(start, end + 1):
        if is_invalid_id_part2(num):
            invalid.append(num)
    return invalid
```

**Step 3**: Add main `solve_part2()` function

```python
def solve_part2(input_data: str) -> int:
    """
    Solve Day 2 Part 2: Sum all invalid product IDs.

    Args:
        input_data: Comma-separated ID ranges (e.g., "11-22,95-115")

    Returns:
        Sum of all invalid product IDs across all ranges
    """
    ranges = parse_input(input_data)  # Reuse Part 1 parser
    total = 0

    for start, end in ranges:
        invalid_ids = check_range_part2(start, end)
        total += sum(invalid_ids)

    return total
```

**Step 4**: Run tests - they should PASS

```bash
uv run pytest day-02/test_solution.py::test_is_invalid_id_part2 -v
uv run pytest day-02/test_solution.py::test_check_range_part2 -v
uv run pytest day-02/test_solution.py::test_solve_part2_example -v
```

**Expected**: All Part 2 tests green ✅

**✅ GREEN Phase Complete**: Tests passing with minimum implementation

---

### REFACTOR Phase: Optimize & Clean

**Step 1**: Review code for improvements

Potential optimizations:

- Early termination is already implemented (first match returns)
- No unnecessary allocations
- Clear variable names and comments

**Step 2**: Add docstrings (already done above)

**Step 3**: Run all tests (Part 1 + Part 2)

```bash
uv run pytest day-02/test_solution.py -v
```

**Expected**: All tests green (both Part 1 and Part 2) ✅

**✅ REFACTOR Phase Complete**: Code clean, all tests passing

---

### VERIFY Phase: Backward Compatibility

**Critical**: Ensure Part 1 still works!

```bash
# Run Part 1 specific tests
uv run pytest day-02/test_solution.py::test_solve_part1_example -v

# Run Part 1 solution
uv run python day-02/solution.py --part 1
```

**Expected**:

- Part 1 tests: ✅ PASS
- Part 1 sum: 1227775554 (unchanged)

**✅ VERIFY Phase Complete**: Part 1 unaffected by Part 2 changes

---

## Running the Solution

### Test with Example Input

```bash
# Create test file with example
echo "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124" > day-02/test_input_part2.txt

# Run Part 2 on test input
uv run python -c "
from day_02.solution import solve_part2
with open('day-02/test_input_part2.txt') as f:
    print(solve_part2(f.read().strip()))
"
```

**Expected Output**: `4174379265`

### Run with Actual Puzzle Input

```bash
# Update solution.py CLI to support part argument
uv run python day-02/solution.py --part 2
```

**Expected**: Your puzzle answer (different from example)

### Submit Answer

1. Copy the output number
2. Go to https://adventofcode.com/2024/day/2
3. Submit manually (no automated submission per AoC Constitution)

---

## Verification Checklist

Before submitting:

- [ ] All Part 1 tests still pass
- [ ] All Part 2 tests pass
- [ ] Example input produces 4174379265
- [ ] Code follows PEP8 (run `ruff check day-02/`)
- [ ] Functions have docstrings
- [ ] Type hints added to all functions
- [ ] No hardcoded values (except test data)
- [ ] Performance acceptable (<5 seconds for actual input)

---

## Common Issues & Solutions

### Issue: Part 1 tests failing after Part 2 implementation

**Solution**: You modified Part 1 functions. Revert changes to:

- `solve_part1()`
- `is_invalid_id()` (Part 1 version)
- `check_range()` (Part 1 version)

Keep Part 2 functions separate!

### Issue: Part 2 tests passing but example gives wrong sum

**Solution**: Check individual ranges:

```python
# Debug each range
ranges = parse_input(EXAMPLE_INPUT)
for start, end in ranges:
    invalid = check_range_part2(start, end)
    print(f"{start}-{end}: {invalid} -> {sum(invalid)}")
```

Compare output with spec expectations.

### Issue: Performance too slow (>10 seconds)

**Solution**:

- Verify early termination in `is_invalid_id_part2()` (return on first match)
- Profile with `python -m cProfile day-02/solution.py --part 2`
- Ensure not recalculating patterns unnecessarily

---

## Next Steps After Completion

1. **Update README**: Document Part 2 completion
2. **Commit**: `git commit -m "feat: solve day 2 part 2 - extended pattern detection"`
3. **Push**: `git push origin 008-day-02-part-2`
4. **Mark Progress**: Update main README.md progress tracker
5. **Reflect**: Note any learnings or interesting patterns in `day-02/README.md`

---

## Resources

- **Specification**: `specs/008-day-02-part-2/spec.md`
- **API Contract**: `specs/008-day-02-part-2/contracts/api-contract.md`
- **Research**: `specs/008-day-02-part-2/research.md`
- **Data Model**: `specs/008-day-02-part-2/data-model.md`
- **AoC Problem**: https://adventofcode.com/2024/day/2

---

## Time Estimate

- **RED Phase**: 10 minutes (write tests)
- **GREEN Phase**: 20 minutes (implement solution)
- **REFACTOR Phase**: 10 minutes (clean up)
- **VERIFY Phase**: 5 minutes (check Part 1)
- **Total**: ~45 minutes

Good luck! 🎄
