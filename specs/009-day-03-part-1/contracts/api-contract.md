# API Contract: Day 3 Part 1 - Battery Bank Joltage Calculator

**Feature**: [spec.md](../spec.md)  
**Date**: December 3, 2025  
**Purpose**: Define function signatures and contracts for battery bank joltage calculation

## Public API

### parse_input

**Signature**:

```python
def parse_input(input_text: str) -> list[str]:
    """
    Parse input text into list of battery bank strings.

    Args:
        input_text: Multi-line string where each line is a battery bank

    Returns:
        List of battery bank strings (one per line, whitespace stripped)

    Examples:
        >>> parse_input("987\\n811")
        ['987', '811']

        >>> parse_input("  45  \\n  \\n123  ")
        ['45', '123']
    """
```

**Contract**:

- **Input**: Any string (including empty string)
- **Output**: List of non-empty strings (bank representations)
- **Behavior**:
  - Splits input by newlines
  - Strips whitespace from each line
  - Filters out empty lines
  - Preserves order of banks
- **Edge cases**:
  - Empty input → returns empty list `[]`
  - Single line → returns list with one element
  - Blank lines → filtered out

---

### max_joltage

**Signature**:

```python
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

    Examples:
        >>> max_joltage("987654321111111")
        98

        >>> max_joltage("811111111111119")
        89

        >>> max_joltage("45")
        45

        >>> max_joltage("5555")
        55
    """
```

**Contract**:

- **Input**: String of digit characters ('1' through '9')
- **Output**: Integer representing maximum joltage
- **Algorithm**:
  - Find max digit in `bank[:-1]` (all except last, need at least one after)
  - Find position of that max digit (earliest occurrence via `index()`)
  - Find max digit in substring after that position
  - Calculate joltage = first_digit \* 10 + second_digit
- **Complexity**: O(n) where n = len(bank) - three linear scans
- **Constraints**:
  - Bank must have at least 2 digits (returns 0 otherwise)
  - Digits must be in range '1'-'9' (problem guarantees this)
- **Edge cases**:
  - Two-digit bank → first at position 0, second at position 1
  - All same digits → returns repeated value (e.g., 55)
  - Single digit → returns 0 (len check)

---

### solve_part1

**Signature**:

```python
def solve_part1(input_text: str) -> int:
    """
    Solve Day 3 Part 1: Calculate total output joltage.

    Processes each battery bank to find its maximum joltage, then
    sums all maximum joltages to get the total output.

    Args:
        input_text: Multi-line string of battery banks

    Returns:
        Total output joltage (sum of all maximum joltages)

    Examples:
        >>> input_text = '''987654321111111
        ... 811111111111119
        ... 234234234234278
        ... 818181911112111'''
        >>> solve_part1(input_text)
        357
    """
```

**Contract**:

- **Input**: Multi-line string representing all battery banks
- **Output**: Integer representing total output joltage
- **Behavior**:
  - Parse input into list of banks
  - Calculate max joltage for each bank
  - Sum all max joltages
  - Return total
- **Complexity**: O(B × n) where B = number of banks, n = avg bank length
- **Edge cases**:
  - Empty input → returns 0
  - Single bank → returns that bank's max joltage
  - No valid banks → returns 0

---

## Internal Helper Functions

### main

**Signature**:

```python
def main() -> None:
    """
    Entry point for running solution with input.txt.

    Reads input from day-03/input.txt, solves Part 1, and prints result.
    """
```

**Contract**:

- **Input**: None (reads from file)
- **Output**: None (prints to stdout)
- **Behavior**:
  - Read content from `day-03/input.txt`
  - Call `solve_part1(content)`
  - Print result in format: "Part 1: {result}"
- **Error handling**:
  - FileNotFoundError if input.txt doesn't exist
  - ValueError if input format is invalid

---

## Example Usage

### Command Line

```bash
# Run solution with actual input
uv run day-03/solution.py

# Run tests
uv run pytest day-03/test_solution.py -v
```

### Programmatic

```python
from day_03.solution import solve_part1

# Example from problem
input_text = """987654321111111
811111111111119
234234234234278
818181911112111"""

result = solve_part1(input_text)
assert result == 357
```

---

## Test Contract

All test functions must follow pytest conventions and use the RED-GREEN-REFACTOR cycle.

### test_max_joltage

```python
def test_max_joltage() -> None:
    """Test maximum joltage calculation for each example."""
    assert max_joltage("987654321111111") == 98
    assert max_joltage("811111111111119") == 89
    assert max_joltage("234234234234278") == 78
    assert max_joltage("818181911112111") == 92
```

### test_max_joltage_edge_cases

```python
def test_max_joltage_edge_cases() -> None:
    """Test edge cases for maximum joltage calculation."""
    assert max_joltage("45") == 45          # Minimum: 2 digits
    assert max_joltage("5555555") == 55     # All same
    assert max_joltage("987") == 98         # Descending
    assert max_joltage("123456789") == 89   # Ascending
```

### test_parse_input

```python
def test_parse_input() -> None:
    """Test input parsing."""
    input_text = """987654321111111
    811111111111119
    234234234234278"""

    banks = parse_input(input_text)
    assert len(banks) == 3
    assert banks[0] == "987654321111111"
    assert banks[1] == "811111111111119"
    assert banks[2] == "234234234234278"
```

### test_solve_part1

```python
def test_solve_part1() -> None:
    """Test full example from problem."""
    input_text = """987654321111111
811111111111119
234234234234278
818181911112111"""

    result = solve_part1(input_text)
    assert result == 357  # 98 + 89 + 78 + 92
```

---

## Error Handling

### Input Validation

- **Empty input**: Return 0 (no banks to process)
- **Malformed banks**: Rely on problem guarantee of valid input
- **File not found**: Raise FileNotFoundError with clear message

### Type Safety

All functions use type hints for:

- Parameter types
- Return types
- Documentation clarity

### Assertions

No runtime assertions needed - problem guarantees valid input format.

---

## Performance Contract

| Function      | Time Complexity | Space Complexity | Expected Runtime        |
| ------------- | --------------- | ---------------- | ----------------------- |
| `parse_input` | O(L)            | O(L)             | < 1ms for L=10KB        |
| `max_joltage` | O(n)            | O(1)             | < 0.1ms for n=100       |
| `solve_part1` | O(B × n)        | O(B)             | < 10ms for B=1000, n=20 |

Where:

- L = total input length
- n = digits per bank
- B = number of banks

---

## Compatibility

- **Python Version**: 3.10+
- **Dependencies**: None (stdlib only)
- **Testing Framework**: pytest
- **Execution**: Via `uv run`
