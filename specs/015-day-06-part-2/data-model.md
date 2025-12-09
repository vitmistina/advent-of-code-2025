# Data Model: Day 6 Part 2 - Cephalopod Math (Right-to-Left Columns)

## Entities

### Worksheet

- Represents the entire input, consisting of columns of numbers and operators.
- Attributes:
  - `columns`: List of columns (each column is a list of characters)
  - `problems`: List of `Problem` objects

### Problem

- Represents a single math problem extracted from adjacent columns.
- Attributes:
  - `operands`: List of `Number` objects
  - `operation`: Operator symbol ('+' or '\*')
  - `result`: Computed integer result

### Number

- Represents a number reconstructed from a column (top-to-bottom digits).
- Attributes:
  - `digits`: List of digit characters (top to bottom)
  - `value`: Integer value (digits joined)

### Operator

- Represents the operation to apply to operands in a problem.
- Attributes:
  - `symbol`: '+' or '\*'

## Relationships

- `Worksheet` contains multiple `Problem` objects
- Each `Problem` contains multiple `Number` objects and one `Operator`

## Validation Rules

- Each problem must have at least one operand and a valid operator
- Digits must be numeric characters
- Operator must be at the bottom of each problem column
- Problems are separated by columns of only spaces
- Numbers are reconstructed by reading column top-to-bottom
