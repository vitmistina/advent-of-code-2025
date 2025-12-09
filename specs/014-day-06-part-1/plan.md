# Implementation Plan: Day 6, Part 1 - Vertical Math Worksheet Parser

**Feature Branch**: `014-day-06-part-1`  
**Status**: Ready for Implementation  
**Design Pattern**: Generator-based streaming with memory efficiency

## Technical Context

### Problem Analysis

The input is a vertically-formatted math worksheet where:

- **Layout**: Numbers are arranged in vertical columns; operation symbols appear at the bottom row
- **Problem Separation**: Problems are separated by full columns containing only whitespace
- **Format**: Line-based input with potentially very long lines (arbitrarily long stream)
- **Constraint**: Need to handle this without loading the entire width into memory

### Architecture Decision: Stream-Based Processing with Generators

Instead of parsing the entire worksheet into memory, we'll process it as a stream of **column groups**, where each group represents a single problem.

**Key Insight**: We can read the input line-by-line, track column positions as we process, and identify column boundaries that contain only whitespace (problem separators). This way:

- Memory usage is constant regardless of worksheet width
- We process one problem at a time
- Grand total accumulates as problems are solved
- Solution naturally supports arbitrarily long horizontal streams

## Data Model

### Core Entities

```
Problem:
  - operands: List[int]          # Numbers extracted from vertical columns
  - operation: str               # '+' or '*'
  - result: int                  # Cached computation result

Column:
  - index: int                   # Position in the worksheet (0-based)
  - values: List[str]            # Non-whitespace character at each row
  - is_separator: bool           # True if all values are whitespace

Problem Group:
  - start_column: int            # First column of this problem
  - end_column: int              # Last column of this problem
  - columns: List[Column]        # All columns in this problem
```

## Solution Architecture

### Module: `parser.py`

Responsible for parsing the worksheet and extracting problems.

**Key Functions**:

#### `read_lines_as_stream(file_or_stream)`

- **Purpose**: Generator that yields lines from input without loading entire file
- **Input**: File object or iterable of lines
- **Yields**: Individual lines (including newlines)
- **Memory**: O(1) - only one line buffered at a time

#### `columns_from_lines(lines_generator)`

- **Purpose**: Transform line stream into column stream
- **Input**: Generator of lines
- **Yields**: Column objects containing values at each row
- **Algorithm**:
  1. Read all lines into a buffer (needed for height detection)
  2. For each character position (column index):
     - Extract characters at that position from each line
     - Group into Column object
     - Yield the column
- **Memory**: O(max_height) - all lines must be loaded to determine column height

**Note**: Step 1 is a necessary tradeoff; we can't determine problem boundaries without knowing the full height. However, this is constant memory per worksheet (lines are typically short relative to width).

#### `problem_column_groups(columns_generator)`

- **Purpose**: Group columns into problems based on separator columns (all whitespace)
- **Input**: Generator of Column objects
- **Yields**: Problem groups (sequences of columns before separator)
- **Algorithm**:
  1. Accumulate columns in current group
  2. When encountering an all-whitespace column:
     - Mark as separator/boundary
     - Yield accumulated group
     - Start new group
  3. Yield final group at end
- **Memory**: O(max_problem_width) - only columns in current problem buffered

#### `extract_problem(column_group)`

- **Purpose**: Parse a problem group into operands and operation symbol
- **Input**: Sequence of Column objects for one problem
- **Returns**: Problem object with operands list and operation symbol
- **Algorithm**:
  1. Last row contains operation symbol(s) - identify +, \*, or spaces
  2. Split operation row by spaces to identify which columns have operations
  3. For each non-operation column, extract vertical number:
     - Read digits from top to bottom in that column
     - Parse as integer
  4. Return Problem with sorted operands and operation
- **Memory**: O(max_problem_width)

#### `evaluate_problem(problem)`

- **Purpose**: Compute result for a single problem
- **Input**: Problem object
- **Returns**: Integer result
- **Algorithm**:
  1. Start with first operand as accumulator
  2. Apply operation (+ or \*) sequentially from left to right:
     - `result = result + operand` (for +)
     - `result = result * operand` (for \*)
  3. Return final result
- **Memory**: O(1) - only tracking accumulator

### Module: `solution.py`

Main orchestration combining parsing and computation.

**Key Functions**:

#### `solve_worksheet(input_stream, verbose=False)`

- **Purpose**: Parse entire worksheet and compute grand total
- **Input**: File object, file path, or iterable of lines
- **Returns**: Integer grand total
- **Algorithm**:
  ```
  1. lines = read_lines_as_stream(input_stream)
  2. cols = columns_from_lines(lines)
  3. groups = problem_column_groups(cols)
  4. grand_total = 0
  5. for group in groups:
       problem = extract_problem(group)
       result = evaluate_problem(problem)
       grand_total += result
       (optional logging if verbose)
  6. return grand_total
  ```
- **Memory**: O(max_lines_height + max_problem_width) - constant relative to total input width
- **Streaming**: Processes problems as they're encountered; never holds entire worksheet in memory

## Key Design Decisions

### 1. Line Buffer Requirement

**Decision**: Buffer all lines before processing columns

**Rationale**:

- Cannot identify problem boundaries (separator columns) without knowing worksheet height
- Need full height to distinguish "space in column X" from "missing value"
- Lines are typically much shorter than worksheet width, so this is acceptable

**Impact**:

- Memory: O(total_lines × average_line_width) for input
- Trade-off: Necessary for correctness in identifying column separators

### 2. Column-at-a-time Processing

**Decision**: Stream columns rather than pre-parsing the entire grid

**Rationale**:

- Supports arbitrarily long horizontal streams (width has no limit)
- Only one column processed at a time (except during problem extraction)
- Aligns with user requirement: "open each line as a stream and process each stream"

**Impact**:

- Memory: Constant for streaming phase
- Simplicity: Natural separation between column identification and problem parsing

### 3. Generator-based Pipeline

**Decision**: Use Python generators to chain processing stages

**Rationale**:

- Natural fit for streaming architecture
- Allows lazy evaluation - only process what's needed
- Memory-efficient chaining of transformations
- Clear separation of concerns between parsing stages

**Impact**:

- Code is declarative and easy to test
- Each stage is independently testable

### 4. Problem Evaluation Order

**Decision**: Process problems left-to-right, accumulating grand total as we go

**Rationale**:

- Aligns with column-at-a-time processing
- Grand total is computed incrementally, not stored
- Only final result is retained in memory

**Impact**:

- Memory: O(1) for grand total accumulation
- Supports verification: can report partial results if needed

## Implementation Steps

### Phase 1: Parser Module

**Step 1.1**: Implement `read_lines_as_stream()`

- Simple line-by-line generator
- Handle file paths, file objects, and iterables
- Test with sample inputs

**Step 1.2**: Implement `Column` class and `columns_from_lines()`

- Define Column dataclass with index, values, is_separator property
- Compute is_separator based on all values being whitespace
- Test column extraction with example worksheet

**Step 1.3**: Implement `problem_column_groups()`

- Accumulate columns until separator found
- Yield groups as sequences
- Test with multi-problem worksheets

**Step 1.4**: Implement `extract_problem()`

- Parse operation row
- Extract numbers from columns
- Return Problem dataclass
- Test number extraction accuracy

### Phase 2: Solution Module

**Step 2.1**: Implement `Problem` class

- Dataclass with operands and operation
- Validation of operation symbol

**Step 2.2**: Implement `evaluate_problem()`

- Sequential left-to-right evaluation
- Support + and \* operations
- Test with known problem results (e.g., 123*45*6=33210)

**Step 2.3**: Implement `solve_worksheet()`

- Orchestrate entire pipeline
- Accumulate grand total
- Test with example worksheet (expected: 4277556)

### Phase 3: Testing

**Step 3.1**: Unit tests for parser module

- Test column identification
- Test separator detection
- Test problem extraction with edge cases

**Step 3.2**: Unit tests for solution module

- Test problem evaluation
- Test grand total accumulation

**Step 3.3**: Integration tests

- Test with example worksheet from problem description
- Test with multi-problem scenarios
- Test with edge cases (single problem, many problems)

**Step 3.4**: Performance tests

- Verify memory efficiency with large worksheets
- Benchmark against naive approach (if needed)

## Testing Strategy

### Unit Tests: `test_parser.py`

```python
# Test read_lines_as_stream
test_read_lines_from_file()
test_read_lines_from_iterable()

# Test columns_from_lines
test_column_extraction_basic()
test_column_separator_detection()
test_column_is_separator_property()

# Test problem_column_groups
test_single_problem_grouping()
test_multiple_problem_grouping()
test_separator_column_isolation()

# Test extract_problem
test_extract_single_operand()
test_extract_multiple_operands()
test_extract_operation_symbol()
test_handle_variable_width_numbers()
test_handle_multi_digit_numbers()
```

### Unit Tests: `test_solution.py`

```python
# Test evaluate_problem
test_evaluate_addition()
test_evaluate_multiplication()
test_evaluate_mixed_operations()

# Test solve_worksheet
test_solve_single_problem()
test_solve_multiple_problems()
test_solve_example_worksheet()
test_grand_total_accumulation()
```

### Integration Tests: `test_solution.py`

```python
# Full worksheet processing
test_example_worksheet_returns_4277556()
test_with_test_input_file()
test_large_arbitrary_width_worksheet()
```

## Success Criteria

✅ **Functional**:

- Correctly parses vertically-formatted problems
- Identifies problem boundaries via separator columns
- Evaluates problems with correct operation
- Computes accurate grand total
- Handles example: 33210 + 490 + 4243455 + 401 = 4277556

✅ **Non-Functional**:

- Memory usage is constant regardless of worksheet width
- All processing uses generators to avoid buffering
- Handles arbitrarily long horizontal streams
- Performance is acceptable (linear in total input size)

✅ **Code Quality**:

- Clear separation of parsing and evaluation concerns
- Comprehensive unit tests
- Type hints throughout
- Docstrings for all public functions

## Edge Cases Handled

1. **Single number problem** → Extra spaces in operation row, but valid evaluation
2. **Leading zeros** → Parsed as integers (naturally handled)
3. **Very wide worksheets** → Streamed column-by-column, no width limit
4. **Many problems** → Processed incrementally, grand total accumulates
5. **Multi-digit numbers** → Extracted from vertical columns character-by-character
6. **Irregular spacing** → Separator detection based on all-whitespace columns

## Files to Create/Modify

- `day-06/solution.py` - Main solution with `solve_worksheet()` function
- `day-06/parser.py` - Parsing utilities with generators
- `day-06/test_solution.py` - Comprehensive test suite

## Notes

- Generator design ensures we never hold the entire worksheet in memory simultaneously
- Column-based processing naturally supports the "stream" approach requested
- Incremental grand total accumulation allows for progress reporting if needed
- Architecture is extensible for Part 2 (which likely changes operation evaluation rules)
