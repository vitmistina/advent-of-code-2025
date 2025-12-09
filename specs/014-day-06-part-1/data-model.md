# Data Model: Day 6, Part 1 - Vertical Math Worksheet Parser

**Feature Branch**: `014-day-06-part-1`  
**Purpose**: Define the data structures and relationships for worksheet parsing

## Entity Definitions

### Column

Represents a single vertical column in the worksheet.

```python
@dataclass
class Column:
    """A vertical column from the worksheet containing values from each row."""
    index: int
    values: List[str]  # Character at this column position for each row

    @property
    def is_separator(self) -> bool:
        """True if this column contains only whitespace (problem boundary)."""
        return all(v.isspace() or v == '' for v in self.values)

    @property
    def content(self) -> str:
        """Non-whitespace content in this column (e.g., digits or operation symbol)."""
        return ''.join(v for v in self.values if not v.isspace())
```

**Relationships**:

- Multiple columns form a **Problem Group**
- Separator columns mark problem boundaries

**Constraints**:

- `index` >= 0
- `values` must have consistent length (equal to worksheet height)
- `is_separator` is computed, not stored

---

### Problem Group

Represents a logically grouped set of columns that comprise one problem.

```python
@dataclass
class ProblemGroup:
    """A collection of adjacent columns representing one math problem."""
    start_column: int      # Index of first column in this group
    end_column: int        # Index of last column in this group
    columns: List[Column]  # The columns in this group

    @property
    def width(self) -> int:
        """Number of columns in this group."""
        return len(self.columns)

    @property
    def height(self) -> int:
        """Number of rows (determined by column values)."""
        return len(self.columns[0].values) if self.columns else 0
```

**Relationships**:

- Contains multiple **Column** objects
- Represents one **Problem**

**Constraints**:

- Columns must be contiguous (no separators within group)
- At least one column required
- All columns must have same height

---

### Problem

Represents the parsed, evaluated math problem.

```python
@dataclass
class Problem:
    """A parsed and evaluated math problem."""
    operands: List[int]    # Numbers to be operated on
    operation: str         # '+' or '*'
    result: int            # Computed result

    def __post_init__(self):
        """Validate problem structure."""
        if self.operation not in ('+', '*'):
            raise ValueError(f"Invalid operation: {self.operation}")
        if not self.operands:
            raise ValueError("Problem must have at least one operand")
        if len(self.operands) < 2:
            raise ValueError("Problem must have at least 2 operands")
```

**Relationships**:

- Represents one row in the final solution
- Multiple problems sum to the **Worksheet** result

**Constraints**:

- `operation` must be '+' or '\*'
- `operands` must have at least 2 elements
- `result` must be computed via sequential operation application

**Validation Rules**:

- All operands must be non-negative integers
- Operation application must be left-to-right:
  - For '+': result = operand₀ + operand₁ + ... + operandₙ
  - For '\*': result = operand₀ × operand₁ × ... × operandₙ

---

### Worksheet

Represents the entire input and its solution.

```python
@dataclass
class Worksheet:
    """The complete input worksheet with all problems and grand total."""
    problems: List[Problem]
    grand_total: int

    @property
    def problem_count(self) -> int:
        """Number of problems in this worksheet."""
        return len(self.problems)

    def verify(self) -> bool:
        """Verify grand total matches sum of problem results."""
        expected = sum(p.result for p in self.problems)
        return self.grand_total == expected
```

**Relationships**:

- Contains multiple **Problem** objects
- Computed from the input stream

**Constraints**:

- `grand_total` must equal sum of all `problem.result` values
- All problems must be present in the list

---

## State Transitions

### Problem Parsing Pipeline

```
Input Stream (lines)
    ↓
columns_from_lines()
    ↓
Column Stream
    ↓
problem_column_groups()
    ↓
ProblemGroup Stream
    ↓
extract_problem()
    ↓
Problem Stream
    ↓
evaluate_problem()
    ↓
Problem (with result)
    ↓
Accumulate to grand_total
    ↓
Final: Worksheet
```

**Key State Points**:

1. **Input Lines**: Raw text lines

   - Lines include newline characters
   - Can be arbitrarily long
   - Stream form: one line at a time

2. **Columns**: Extracted from lines

   - Logical representation of vertical structure
   - Separator columns identified
   - Stream form: one column at a time

3. **Problem Groups**: Bounded columns

   - Grouped by separator boundaries
   - Not yet parsed into operands/operations
   - Sequence form: collected per problem

4. **Problems**: Parsed and evaluated
   - Operands extracted from columns
   - Operation identified from row
   - Result computed via evaluation
   - Stream form: one problem at a time (aggregated to grand_total)

---

## Data Flow

### Parsing Phase

```
For each line in input:
  Store line in buffer

For each column position (0 to max_width):
  Create Column object:
    index = position
    values = [line[position] for line in buffer]
    is_separator = all values are whitespace

  Yield column
```

**Memory**: O(total_lines × average_line_length)

---

### Grouping Phase

```
accumulated_group = []

For each column in column_stream:
  if column.is_separator:
    if accumulated_group:
      yield ProblemGroup(columns=accumulated_group)
    accumulated_group = []
  else:
    accumulated_group.append(column)

if accumulated_group:
  yield ProblemGroup(columns=accumulated_group)
```

**Memory**: O(max_problem_width)

---

### Extraction Phase

```
For each problem_group in group_stream:

  last_row = problem_group.columns[*].values[-1]
  operation_row_str = ''.join(last_row)

  # Identify which columns have operation symbols
  operation = None
  for position in range(len(operation_row_str)):
    if operation_row_str[position] in '(+, *)':
      operation = operation_row_str[position]

  # Extract numbers from non-operation columns
  operands = []
  for column in problem_group.columns:
    # Skip all-space columns (which would be between operands)
    if not column.is_separator:
      # Extract vertical number
      number_str = ''
      for row_idx in range(len(column.values) - 1):  # Skip last (operation) row
        char = column.values[row_idx]
        if char.isdigit():
          number_str += char
      if number_str:
        operands.append(int(number_str))

  yield Problem(operands=operands, operation=operation, result=None)
```

**Memory**: O(max_problem_width)

---

### Evaluation Phase

```
grand_total = 0

For each problem in problem_stream:

  result = problem.operands[0]
  for operand in problem.operands[1:]:
    if problem.operation == '+':
      result += operand
    else:  # '*'
      result *= operand

  problem.result = result
  grand_total += result

return grand_total
```

**Memory**: O(1)

---

## Validation Rules

### Column Validation

- All columns in a problem group must have same height
- Separator column must have all values as whitespace

### Problem Validation

- Must have at least 2 operands
- Operation must be '+' or '\*'
- All operands must be non-negative integers

### Worksheet Validation

- Grand total must equal sum of problem results
- All problems must have been successfully extracted

---

## Type Definitions

```python
from dataclasses import dataclass
from typing import List, Optional

# Column-level types
ColumnIndex = int
ColumnValues = List[str]

# Problem-level types
Operand = int
Operation = str  # '+' or '*'
ProblemResult = int

# Stream types
LineStream = Iterator[str]
ColumnStream = Iterator[Column]
ProblemGroupStream = Iterator[ProblemGroup]
ProblemStream = Iterator[Problem]
```

---

## Example Walkthrough

### Input Worksheet

```
123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +
```

### Parsed Columns (selected)

- Column 0: ['1', ' ', ' ', '*'] → not separator, content='1\*'
- Column 1: ['2', '4', ' ', ' '] → not separator, content='24'
- Column 2: ['3', '5', '6', ' '] → not separator, content='356'
- Column 3: [' ', ' ', ' ', ' '] → **SEPARATOR**
- Column 4: ['3', ' ', ' ', ' '] → not separator, content='3'
- ... etc

### Problem Groups

- Group 1: Columns 0-2
- Group 2: Columns 4-6
- Group 3: Columns 8-10
- Group 4: Columns 12-14

### Extracted Problems

1. Problem(operands=[123, 45, 6], operation='\*', result=33210)
2. Problem(operands=[328, 64, 98], operation='+', result=490)
3. Problem(operands=[51, 387, 215], operation='\*', result=4243455)
4. Problem(operands=[64, 23, 314], operation='+', result=401)

### Worksheet

```
Worksheet(
  problems=[Problem(...), Problem(...), Problem(...), Problem(...)],
  grand_total=4277556
)
```
