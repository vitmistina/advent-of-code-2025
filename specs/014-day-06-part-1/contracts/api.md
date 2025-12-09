# API Contracts: Day 6, Part 1 - Vertical Math Worksheet Parser

**Feature Branch**: `014-day-06-part-1`  
**Purpose**: Define the public interfaces and contracts for the solution

## Module: `parser.py`

### Function: `read_lines_as_stream(source: Union[str, Path, IO]) -> Iterator[str]`

**Purpose**: Stream lines from input without loading entire file into memory.

**Signature**:

```python
def read_lines_as_stream(
    source: Union[str, Path, IO]
) -> Iterator[str]:
    """
    Yield lines from a file or file-like object.

    Args:
        source: File path (str or Path), or file-like object (IO)

    Yields:
        str: Individual lines (including newline characters)

    Raises:
        FileNotFoundError: If source is a path that doesn't exist
        IOError: If file cannot be read

    Example:
        with open('input.txt') as f:
            for line in read_lines_as_stream(f):
                process(line)
    """
```

**Contract**:

- Yields one complete line at a time
- Lines include trailing newline characters (if present in source)
- Generator, so it's lazy - file is read on-demand
- Automatically closes file if source is a path

**Test Cases**:

- Read from file path
- Read from file object
- Empty file returns no lines
- File with N lines yields exactly N items

---

### Class: `Column`

**Purpose**: Represent a vertical column from the worksheet.

**Definition**:

```python
@dataclass
class Column:
    """A vertical column from the worksheet."""

    index: int
    """Position of this column in the worksheet (0-based)."""

    values: List[str]
    """Character at this column position for each row."""

    @property
    def is_separator(self) -> bool:
        """
        Returns True if this column contains only whitespace.

        A separator column marks a boundary between problems.

        Returns:
            bool: True if all values are whitespace or empty
        """

    @property
    def content(self) -> str:
        """
        Non-whitespace content in this column.

        Useful for debugging and verification.

        Returns:
            str: All non-whitespace characters concatenated
        """
```

**Contract**:

- Immutable after creation
- All values must have same length (worksheet height)
- `is_separator` is computed property, not stored
- Can be hashed and compared

**Validation**:

- index >= 0
- len(values) >= 1

---

### Function: `columns_from_lines(lines: Iterator[str]) -> Iterator[Column]`

**Purpose**: Transform a stream of lines into a stream of columns.

**Signature**:

```python
def columns_from_lines(
    lines: Iterator[str]
) -> Iterator[Column]:
    """
    Transform line stream into column stream.

    Reads all input lines, then yields columns left-to-right.

    Args:
        lines: Iterator of strings (each representing one line)

    Yields:
        Column: Column objects representing vertical positions

    Raises:
        ValueError: If input lines have inconsistent lengths

    Example:
        lines = ['abc', 'def']
        for col in columns_from_lines(lines):
            # First yields Column(index=0, values=['a', 'd'])
            # Then yields Column(index=1, values=['b', 'e'])
            # Then yields Column(index=2, values=['c', 'f'])
            print(col)
    """
```

**Contract**:

- Consumes entire line iterator (must buffer all lines)
- Yields columns in left-to-right order
- Each column has consistent height
- Handles lines of different lengths (pads shorter lines with spaces)

**Test Cases**:

- Single line
- Multiple lines of same length
- Lines of different lengths (padding)
- Empty input (yields nothing)
- Single character columns

---

### Function: `problem_column_groups(columns: Iterator[Column]) -> Iterator[ProblemGroup]`

**Purpose**: Group columns into problems by identifying separator boundaries.

**Signature**:

```python
def problem_column_groups(
    columns: Iterator[Column]
) -> Iterator[ProblemGroup]:
    """
    Group columns into problems using separator columns as boundaries.

    Yields groups of consecutive columns that form a single problem.
    Separator columns (all whitespace) mark boundaries and are not included.

    Args:
        columns: Iterator of Column objects

    Yields:
        ProblemGroup: Groups of adjacent non-separator columns

    Example:
        # For columns [A, SEP, B, C, SEP, D]
        # Yields ProblemGroup([A])
        # Then ProblemGroup([B, C])
        # Then ProblemGroup([D])
    """
```

**Contract**:

- Yields ProblemGroup objects in order
- Separator columns are consumed but not yielded
- Each group contains at least one non-separator column
- Groups maintain column order and indices

**Test Cases**:

- Single problem (no separators)
- Multiple problems (with separators)
- Separators at start/end (ignored)
- Consecutive separators (treated as one boundary)

---

### Function: `extract_problem(group: ProblemGroup) -> Problem`

**Purpose**: Parse a problem group into operands and operation.

**Signature**:

```python
def extract_problem(group: ProblemGroup) -> Problem:
    """
    Extract operands and operation from a problem group.

    - Last row contains the operation symbol (+, *)
    - Other rows contain digits forming numbers in vertical columns
    - Numbers are read top-to-bottom in each column

    Args:
        group: ProblemGroup containing one problem's columns

    Returns:
        Problem: Parsed problem with operands and operation

    Raises:
        ValueError: If operation symbol not found
        ValueError: If no operands extracted

    Example:
        # For a problem:
        #   123
        #    45
        #     6
        #   *
        # Returns Problem(operands=[123, 45, 6], operation='*', result=None)
    """
```

**Contract**:

- Identifies operation from last row
- Extracts all numbers from problem columns
- Returns Problem with result=None (to be evaluated later)
- Raises ValueError if operation or operands missing

**Validation**:

- Operation must be '+' or '\*'
- Must have at least 2 operands
- All operands must be non-negative integers

**Test Cases**:

- Addition problem
- Multiplication problem
- Multi-digit numbers
- Variable width numbers
- Numbers with leading zeros

---

## Module: `solution.py`

### Class: `Problem`

**Purpose**: Represent a parsed and evaluated math problem.

**Definition**:

```python
@dataclass
class Problem:
    """A parsed math problem with operation and result."""

    operands: List[int]
    """Numbers to be operated on, in left-to-right order."""

    operation: str
    """Operation symbol: '+' or '*'."""

    result: Optional[int] = None
    """Computed result; None before evaluation."""

    def __post_init__(self):
        """Validate problem structure."""
        # Raises ValueError if invalid

    def evaluate(self) -> int:
        """
        Compute and cache the result.

        Returns:
            int: Result of applying operation to operands left-to-right
        """
```

**Contract**:

- Immutable after creation
- Can be evaluated to compute result
- Validation happens in **post_init**

**Validation Rules**:

- operation must be '+' or '\*'
- operands must have at least 2 elements
- all operands must be >= 0

---

### Function: `evaluate_problem(problem: Problem) -> int`

**Purpose**: Compute the result of a problem by applying operation sequentially.

**Signature**:

```python
def evaluate_problem(problem: Problem) -> int:
    """
    Evaluate a problem by applying its operation to operands sequentially.

    Operation is applied left-to-right:
    - For '+': result = op[0] + op[1] + op[2] + ...
    - For '*': result = op[0] * op[1] * op[2] * ...

    Args:
        problem: Problem object with operands and operation

    Returns:
        int: Result of evaluation

    Raises:
        ValueError: If operation is invalid

    Example:
        p = Problem(operands=[2, 3, 4], operation='*')
        assert evaluate_problem(p) == 24  # 2 * 3 * 4
    """
```

**Contract**:

- Returns integer result
- Applies operation strictly left-to-right (not mathematical precedence)
- Does not modify input problem

**Test Cases**:

- Addition: [2, 3, 4] + → 9
- Multiplication: [2, 3, 4] \* → 24
- Single addition: [5, 5] + → 10
- Single multiplication: [5, 5] \* → 25
- Large numbers

---

### Function: `solve_worksheet(source: Union[str, Path, IO], verbose: bool = False) -> int`

**Purpose**: Parse and solve entire worksheet, returning grand total.

**Signature**:

```python
def solve_worksheet(
    source: Union[str, Path, IO],
    verbose: bool = False
) -> int:
    """
    Parse and solve a complete worksheet, returning the grand total.

    Pipeline:
    1. Read lines from source
    2. Transform into columns
    3. Group columns by separator boundaries
    4. Extract and evaluate each problem
    5. Accumulate results into grand total

    Args:
        source: File path (str/Path) or file-like object
        verbose: If True, print progress information

    Returns:
        int: Grand total (sum of all problem results)

    Raises:
        FileNotFoundError: If source file not found
        ValueError: If worksheet format is invalid

    Example:
        total = solve_worksheet('input.txt')
        print(f"Grand total: {total}")
    """
```

**Contract**:

- Processes entire worksheet and returns single integer
- Uses streaming/generators for memory efficiency
- Supports both file paths and file objects
- Optional verbose output for debugging

**Memory Efficiency**:

- Never holds entire worksheet in memory
- Only buffers one column group at a time
- Grand total is accumulated, not stored

**Test Cases**:

- Single problem worksheet
- Multi-problem worksheet
- Example worksheet (returns 4277556)
- Large worksheet (many problems)
- Worksheet from file path
- Worksheet from file object

---

## Type Aliases

```python
from typing import Union, Path, IO, Iterator, List, Optional

ColumnIndex = int
ColumnValues = List[str]
Operand = int
Operation = str  # '+' or '*'
ProblemResult = int

LineStream = Iterator[str]
ColumnStream = Iterator[Column]
ProblemGroupStream = Iterator[ProblemGroup]
ProblemStream = Iterator[Problem]

InputSource = Union[str, Path, IO]
```

---

## Error Handling

### Expected Errors

```python
FileNotFoundError
  - Raised when source file path doesn't exist

ValueError
  - Invalid worksheet format (malformed problem)
  - Missing operation symbol
  - Insufficient operands (< 2)
  - Invalid operation symbol (not '+' or '*')

IOError
  - File cannot be read

AssertionError (internal only)
  - Contract violations (should never reach user)
```

### Error Messages

- `"File not found: {path}"`
- `"Invalid operation symbol in problem: {symbol}"`
- `"Problem must have at least 2 operands, got {count}"`
- `"Inconsistent line lengths in worksheet"`

---

## Integration Example

```python
from pathlib import Path
from solution import solve_worksheet

# Parse and solve
result = solve_worksheet('input.txt', verbose=True)
print(f"Grand Total: {result}")

# Or with file object
with open('input.txt') as f:
    result = solve_worksheet(f)

# Or with Path object
result = solve_worksheet(Path('input.txt'))
```
