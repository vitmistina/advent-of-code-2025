# Day 6, Part 1 - Vertical Math Worksheet Parser

## Overview

Solve vertically-formatted math worksheets where numbers are arranged in vertical columns, operations appear in the bottom row, and problems are separated by whitespace columns.

## Running the Solution

### With Main Input

To solve the puzzle with the main input file using `uv`:

```bash
# From project root
uv run python day-06/solution.py

# Or from the day-06 directory
cd day-06
uv run python solution.py
```

## Quick Start

### Basic Usage

```python
from solution import solve_worksheet

# Solve entire worksheet and get grand total
total = solve_worksheet("input.txt")
print(f"Grand Total: {total}")

# With verbose output
total = solve_worksheet("input.txt", verbose=True)

# With debug output
total = solve_worksheet("input.txt", debug=True)
```

### Input Format

```
123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +
```

Each column represents a digit position. Reading top-to-bottom gives operands:

- **Problem 1** (cols 0-2): 123, 45, 6 with operation `*` → 123 × 45 × 6 = 33,210
- **Problem 2** (cols 4-6): 328, 64, 98 with operation `+` → 328 + 64 + 98 = 490
- **Problem 3** (cols 8-9): 51, 387, 215 with operation `*` → 51 × 387 × 215 = 4,243,455
- **Problem 4** (cols 11-13): 64, 23, 314 with operation `+` → 64 + 23 + 314 = 401

**Grand Total**: 33,210 + 490 + 4,243,455 + 401 = **4,277,556**

## Architecture

### Modules

#### `parser.py`

Handles parsing the input into a structured format:

- **Column**: Represents a vertical column with values from each row
- **ProblemGroup**: Groups adjacent columns representing one problem
- **read_lines_as_stream**: Generator-based file reading
- **columns_from_lines**: Convert lines to vertical columns
- **problem_column_groups**: Group columns by separator boundaries
- **extract_problem**: Parse a ProblemGroup into a Problem object

#### `solution.py`

Handles evaluation and high-level solving:

- **Problem**: Dataclass representing a parsed problem
- **evaluate_problem**: Compute result of a problem
- **solve_worksheet**: Main entry point; orchestrates the full pipeline

### Memory Efficiency

All components use generators for streaming processing:

- **Lines**: Read one at a time from file
- **Columns**: Yielded as processed
- **Problems**: Parsed and evaluated incrementally
- **Memory**: Constant regardless of worksheet width (only line buffer needed)

## Usage Patterns

### Parse and Evaluate Individual Problems

```python
from parser import read_lines_as_stream, columns_from_lines, problem_column_groups, extract_problem
from solution import evaluate_problem

lines = read_lines_as_stream("worksheet.txt")
cols = columns_from_lines(lines)
groups = problem_column_groups(cols)

for group in groups:
    problem = extract_problem(group)
    result = evaluate_problem(problem)
    print(f"Problem: {problem.operands} {problem.operation} = {result}")
```

### Process from String

```python
import io
from solution import solve_worksheet

worksheet = "12 34\n56 78\n*  + \n"
total = solve_worksheet(io.StringIO(worksheet))
assert total == 390 + 85  # (15 * 26) + (37 + 48)
```

### Debug Output

```python
total = solve_worksheet("worksheet.txt", verbose=True, debug=True)
# Prints:
# [DEBUG] Problem 1: operands=[...], operation=..., result=...
# Problem 1: ... = ...
# ...
# Grand Total: ...
```

## Error Handling

The implementation handles various error conditions:

- **Empty worksheet**: Returns 0
- **No operation in problem**: Raises `ValueError`
- **Malformed columns**: Raises `ValueError` with details
- **File not found**: Raises `FileNotFoundError`

Example:

```python
try:
    total = solve_worksheet("missing.txt")
except FileNotFoundError:
    print("Worksheet file not found")
```

## Testing

Comprehensive test coverage with 38 tests across 5 test files:

```bash
# Run all tests
uv run -m pytest day-06/ -v

# Run specific test file
uv run -m pytest day-06/test_parser.py -v

# Run with coverage
uv run -m pytest day-06/ --cov=day_06 --cov-report=html
```

### Test Coverage

- **test_parser.py** (12 tests): Line reading, column extraction, problem parsing
- **test_problem_groups.py** (7 tests): Problem grouping by separators
- **test_multiple_problems.py** (7 tests): Multi-problem integration
- **test_solution.py** (4 tests): Problem evaluation
- **test_worksheet.py** (8 tests): Full worksheet solving

## Implementation Details

### Column Parsing

Each column contains:

- **index**: Position in worksheet (0-based)
- **values**: Character at this column for each row
- **is_separator**: Property indicating if all values are whitespace
- **content**: Non-whitespace content

### Problem Extraction

For each ProblemGroup:

1. Extract non-separator columns
2. Read each column top-to-bottom to get digit sequences
3. Each digit sequence forms one operand
4. Last row contains the operation symbol
5. Evaluate using the operands and operation

### Example Walkthrough

Input:

```
12 34
56 78
*  +
```

After padding to width 5:

```
"12 34"
"56 78"
"*  + "
```

Columns:

- Col 0: ['1', '5', '*'] → operand "15"
- Col 1: ['2', '6', ' '] → operand "26"
- Col 2: [' ', ' ', ' '] → separator (skip)
- Col 3: ['3', '7', '+'] → operand "37"
- Col 4: ['4', '8', ' '] → operand "48"

Problems:

- Problem 1 (cols 0-1): 15 \* 26 = 390
- Problem 2 (cols 3-4): 37 + 48 = 85
- **Total: 475**

## Files

- `parser.py`: Parsing module (223 lines)
- `solution.py`: Solution module (100 lines)
- `test_parser.py`: Parser tests (95 lines)
- `test_problem_groups.py`: Grouping tests (70 lines)
- `test_multiple_problems.py`: Integration tests (130 lines)
- `test_solution.py`: Evaluation tests (30 lines)
- `test_worksheet.py`: Worksheet tests (110 lines)
- `README.md`: This file

## Validation

✓ All 38 unit tests passing
✓ TDD approach: Red → Green → Refactor cycle
✓ Memory-efficient streaming architecture
✓ Comprehensive error handling
✓ Full docstring coverage
✓ Usage examples provided
