# Quickstart: Day 3 Part 1 - Battery Bank Joltage Calculator

**Feature**: [spec.md](../spec.md)  
**Date**: December 3, 2025  
**Purpose**: Step-by-step implementation guide using Test-Driven Development

## Prerequisites

- ✅ Python 3.10+ installed
- ✅ UV package manager configured
- ✅ Feature branch `009-day-03-part-1` checked out
- ✅ Day 3 folder structure created (`day-03/`)
- ✅ Input files downloaded (`input.txt`, `test_input.txt`)

## Implementation Workflow

This guide follows the **RED-GREEN-REFACTOR** cycle mandated by the Constitution.

---

## Phase 1: RED - Write Failing Tests

### Step 1.1: Create test file

```bash
# Create test file
touch day-03/test_solution.py
```

### Step 1.2: Write test for max_joltage (core logic)

**File**: `day-03/test_solution.py`

```python
"""Tests for Day 3 Part 1: Battery Bank Joltage Calculator."""

from solution import max_joltage, parse_input, solve_part1


def test_max_joltage():
    """Test maximum joltage calculation for each example."""
    assert max_joltage("987654321111111") == 98
    assert max_joltage("811111111111119") == 89
    assert max_joltage("234234234234278") == 78
    assert max_joltage("818181911112111") == 92


def test_max_joltage_edge_cases():
    """Test edge cases for maximum joltage calculation."""
    assert max_joltage("45") == 45          # Minimum: 2 digits
    assert max_joltage("5555555") == 55     # All same digits
    assert max_joltage("987") == 98         # Descending order
    assert max_joltage("123456789") == 89   # Ascending order
```

### Step 1.3: Write test for parse_input

```python
def test_parse_input():
    """Test input parsing."""
    input_text = """987654321111111
811111111111119
234234234234278"""

    banks = parse_input(input_text)
    assert len(banks) == 3
    assert banks[0] == "987654321111111"
    assert banks[1] == "811111111111119"
    assert banks[2] == "234234234234278"


def test_parse_input_empty():
    """Test parsing empty input."""
    assert parse_input("") == []
    assert parse_input("   \n  \n  ") == []
```

### Step 1.4: Write test for solve_part1 (integration)

```python
def test_solve_part1():
    """Test full example from problem."""
    input_text = """987654321111111
811111111111119
234234234234278
818181911112111"""

    result = solve_part1(input_text)
    assert result == 357  # 98 + 89 + 78 + 92
```

### Step 1.5: Verify tests FAIL

```bash
# Run tests - they should fail because solution.py doesn't exist yet
uv run pytest day-03/test_solution.py -v
```

**Expected output**: Import errors or test failures (RED phase ✅)

---

## Phase 2: GREEN - Implement Minimum Code

### Step 2.1: Create solution file

**File**: `day-03/solution.py`

```python
"""Day 3 Part 1: Battery Bank Joltage Calculator.

Solution for Advent of Code 2025 Day 3.
Calculates maximum joltage from battery banks.
"""


def parse_input(input_text: str) -> list[str]:
    """
    Parse input text into list of battery bank strings.

    Args:
        input_text: Multi-line string where each line is a battery bank

    Returns:
        List of battery bank strings (one per line, whitespace stripped)
    """
    return [line.strip() for line in input_text.strip().splitlines() if line.strip()]


def max_joltage(bank: str) -> int:
    """
    Find maximum joltage from a battery bank using greedy algorithm.

    The maximum joltage is the largest two-digit number that can be formed
    by selecting exactly two batteries (digits) from the bank while
    maintaining their left-to-right order.

    Greedy approach:
    1. First battery: max digit in bank[:-1] (need at least one after it)
    2. Second battery: max digit after first battery's position

    Args:
        bank: String of digit characters representing batteries

    Returns:
        Maximum joltage value (0-99)
    """
    if len(bank) < 2:
        return 0

    # Find the maximum digit in all positions except the last
    # (we need at least one digit after the first battery)
    max_first_digit = max(bank[:-1])
    first_pos = bank.index(max_first_digit)

    # Find the maximum digit after the first battery
    max_second_digit = max(bank[first_pos + 1:])

    # Calculate joltage
    joltage = int(max_first_digit) * 10 + int(max_second_digit)
    return joltage


def solve_part1(input_text: str) -> int:
    """
    Solve Day 3 Part 1: Calculate total output joltage.

    Processes each battery bank to find its maximum joltage, then
    sums all maximum joltages to get the total output.

    Args:
        input_text: Multi-line string of battery banks

    Returns:
        Total output joltage (sum of all maximum joltages)
    """
    banks = parse_input(input_text)
    total = sum(max_joltage(bank) for bank in banks)
    return total


def main() -> None:
    """Entry point for running solution with input.txt."""
    from pathlib import Path

    input_file = Path(__file__).parent / "input.txt"
    input_text = input_file.read_text()

    result = solve_part1(input_text)
    print(f"Part 1: {result}")


if __name__ == "__main__":
    main()
```

### Step 2.2: Run tests - they should PASS

```bash
# Run tests again - should pass now
uv run pytest day-03/test_solution.py -v
```

**Expected output**: All tests passing (GREEN phase ✅)

---

## Phase 3: REFACTOR - Optimize and Clean

### Step 3.1: Review code quality

Check if code is:

- ✅ Readable and clear
- ✅ Well-documented with docstrings
- ✅ Type-hinted
- ✅ Following PEP8 (via Ruff)
- ✅ Efficient enough (O(n²) acceptable)

### Step 3.2: Run linter

```bash
# Format and lint
uv run ruff format day-03/
uv run ruff check day-03/
```

### Step 3.3: Verify tests still pass

```bash
# Ensure refactoring didn't break anything
uv run pytest day-03/test_solution.py -v
```

**Expected**: All tests still passing (REFACTOR phase ✅)

---

## Phase 4: Execute and Submit

### Step 4.1: Test with example input

```bash
# Verify solution works with test input
cat day-03/test_input.txt
uv run day-03/solution.py
```

**Expected output**: `Part 1: 357` (matching the example)

### Step 4.2: Run with actual input

```bash
# Run with actual puzzle input
uv run day-03/solution.py
```

### Step 4.3: Submit answer manually

1. Copy the output from the solution
2. Go to [Advent of Code 2025 Day 3](https://adventofcode.com/2025/day/3)
3. Paste answer in Part 1 submission box
4. Click Submit

---

## Verification Checklist

Before submitting, verify:

- [ ] All tests pass: `uv run pytest day-03/test_solution.py -v`
- [ ] Code passes linting: `uv run ruff check day-03/`
- [ ] Test input produces expected result (357)
- [ ] Actual input produces a valid result
- [ ] All functions have docstrings
- [ ] Type hints are present

---

## File Structure After Completion

```
day-03/
├── solution.py          ✅ Main solution (3 functions + main)
├── test_solution.py     ✅ Pytest tests (5 test functions)
├── input.txt            ✅ Actual puzzle input
├── test_input.txt       ✅ Example input
├── description.md       ✅ Challenge description
└── README.md            ⏳ Optional notes

specs/009-day-03-part-1/
├── spec.md              ✅ Feature specification
├── plan.md              ✅ Implementation plan
├── research.md          ✅ Algorithm decisions
├── data-model.md        ✅ Entity definitions
├── quickstart.md        ✅ This guide
└── contracts/
    └── api-contract.md  ✅ Function signatures
```

---

## Troubleshooting

### Tests fail with import errors

**Problem**: Cannot import from `solution`

**Solution**: Ensure you're in the `day-03/` directory or use proper module path:

```bash
cd day-03
uv run pytest test_solution.py -v
```

### Tests pass but wrong answer for actual input

**Problem**: Logic error not caught by tests

**Solution**: Add more test cases to `test_solution.py` to cover edge cases

### Performance too slow

**Problem**: Solution takes > 1 second

**Solution**: Profile the code and optimize the inner loop (unlikely for n < 100)

---

## Next Steps

After completing Part 1:

1. Commit your work:

   ```bash
   git add day-03/
   git commit -m "feat: solve day 03 part 1"
   git push origin 009-day-03-part-1
   ```

2. Update progress in main README.md

3. Wait for Part 2 to be released

4. Run `/speckit.specify` for Part 2 when ready

---

## Time Estimates

| Phase             | Estimated Time  |
| ----------------- | --------------- |
| RED (write tests) | 10 minutes      |
| GREEN (implement) | 15 minutes      |
| REFACTOR (clean)  | 5 minutes       |
| Execute & verify  | 5 minutes       |
| **Total**         | **~35 minutes** |

---

## Success Criteria

✅ All acceptance scenarios from spec pass  
✅ Test coverage for edge cases  
✅ Code follows Constitution principles  
✅ Correct answer submitted to Advent of Code  
✅ TDD cycle (RED-GREEN-REFACTOR) followed strictly
