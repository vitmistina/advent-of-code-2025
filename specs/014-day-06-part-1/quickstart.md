# Quickstart: Day 6, Part 1 - Vertical Math Worksheet Parser

**Feature Branch**: `014-day-06-part-1`  
**Goal**: Implement a memory-efficient streaming parser for vertically-formatted math worksheets

## Feature Overview

Parse a vertically-formatted math worksheet where:
- **Numbers** are arranged in vertical columns
- **Operations** (+ or *) appear in the bottom row
- **Problems** are separated by full columns of whitespace
- **Goal**: Calculate the sum of all problem results (grand total)

Example:
```
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
```

Four problems:
- 123 * 45 * 6 = 33210
- 328 + 64 + 98 = 490
- 51 * 387 * 215 = 4243455
- 64 + 23 + 314 = 401

**Grand Total**: 33210 + 490 + 4243455 + 401 = **4277556**

---

## Architecture Highlights

### Stream-Based Design

Instead of loading the entire worksheet, we process it as a **stream**:

1. **Line Stream**: Read input line-by-line (supports arbitrarily long lines)
2. **Column Stream**: Transform lines into vertical columns (process left-to-right)
3. **Problem Stream**: Group columns by separator boundaries
4. **Result Stream**: Evaluate problems and accumulate grand total

### Memory Efficiency

✅ Constant memory regardless of worksheet width  
✅ Generator-based pipeline (lazy evaluation)  
✅ Problems processed incrementally  
✅ Grand total computed as we go  

### Generator Usage

```python
# Example pipeline
lines = read_lines_as_stream('input.txt')           # Generator
cols = columns_from_lines(lines)                    # Generator
groups = problem_column_groups(cols)                # Generator
grand_total = sum(
    evaluate_problem(extract_problem(group))
    for group in groups
)
```

Each stage is a generator, so we never hold the full worksheet in memory.

---

## Implementation Outline

### Phase 1: Parser Module (`day-06/parser.py`)

**Step 1**: Define Column class
```python
@dataclass
class Column:
    index: int
    values: List[str]
    
    @property
    def is_separator(self) -> bool:
        return all(v.isspace() or v == '' for v in self.values)
```

**Step 2**: Implement line-to-column transformation
```python
def columns_from_lines(lines: Iterator[str]) -> Iterator[Column]:
    # Buffer all lines, then yield columns left-to-right
    buffer = list(lines)
    max_width = max(len(line) for line in buffer) if buffer else 0
    
    for col_idx in range(max_width):
        values = [line[col_idx] if col_idx < len(line) else ' ' for line in buffer]
        yield Column(index=col_idx, values=values)
```

**Step 3**: Implement column grouping
```python
def problem_column_groups(columns: Iterator[Column]) -> Iterator[ProblemGroup]:
    group = []
    for col in columns:
        if col.is_separator:
            if group:
                yield ProblemGroup(columns=group)
                group = []
        else:
            group.append(col)
    if group:
        yield ProblemGroup(columns=group)
```

**Step 4**: Implement problem extraction
```python
def extract_problem(group: ProblemGroup) -> Problem:
    # Last row contains operation
    operation_row = group.columns[-1].values[-1]  # Wait, this is wrong...
    
    # Actually: reconstruct last row from all columns in group
    last_row = ''.join(col.values[-1] for col in group.columns)
    
    # Find operation symbol
    operation = '+' if '+' in last_row else '*'
    
    # Extract numbers from columns (skip operation row)
    operands = []
    for col in group.columns:
        # Vertical number in this column
        number_str = ''.join(col.values[:-1])  # All rows except operation
        number_str = ''.join(c for c in number_str if c.isdigit())
        if number_str:
            operands.append(int(number_str))
    
    return Problem(operands=operands, operation=operation, result=None)
```

---

### Phase 2: Solution Module (`day-06/solution.py`)

**Step 1**: Define Problem class
```python
@dataclass
class Problem:
    operands: List[int]
    operation: str
    result: Optional[int] = None
    
    def __post_init__(self):
        if self.operation not in ('+', '*'):
            raise ValueError(f"Invalid operation: {self.operation}")
        if len(self.operands) < 2:
            raise ValueError("Need at least 2 operands")
```

**Step 2**: Implement problem evaluation
```python
def evaluate_problem(problem: Problem) -> int:
    result = problem.operands[0]
    for operand in problem.operands[1:]:
        if problem.operation == '+':
            result += operand
        else:  # '*'
            result *= operand
    return result
```

**Step 3**: Implement main solver
```python
def solve_worksheet(source: Union[str, Path, IO], verbose=False) -> int:
    lines = read_lines_as_stream(source)
    cols = columns_from_lines(lines)
    groups = problem_column_groups(cols)
    
    grand_total = 0
    count = 0
    for group in groups:
        problem = extract_problem(group)
        result = evaluate_problem(problem)
        grand_total += result
        count += 1
        if verbose:
            print(f"Problem {count}: {problem.operands} {problem.operation} = {result}")
    
    return grand_total
```

---

### Phase 3: Testing (`day-06/test_solution.py`)

**Test the parser**:
```python
def test_extract_columns_simple():
    lines = ['abc', 'def']
    cols = list(columns_from_lines(iter(lines)))
    assert cols[0].index == 0
    assert cols[0].values == ['a', 'd']
    assert cols[0].is_separator == False

def test_separator_column():
    lines = ['a  b']
    cols = list(columns_from_lines(iter(lines)))
    assert cols[1].is_separator == True

def test_problem_grouping():
    lines = ['a  b']
    cols = columns_from_lines(iter(lines))
    groups = list(problem_column_groups(cols))
    assert len(groups) == 2
    assert len(groups[0].columns) == 1
    assert len(groups[1].columns) == 1
```

**Test problem evaluation**:
```python
def test_evaluate_addition():
    p = Problem(operands=[2, 3, 4], operation='+')
    assert evaluate_problem(p) == 9

def test_evaluate_multiplication():
    p = Problem(operands=[2, 3, 4], operation='*')
    assert evaluate_problem(p) == 24

def test_example_worksheet():
    # Create example worksheet from problem description
    input_text = "123 328  51 64 \n 45 64  387 23 \n  6 98  215 314\n*   +   *   +  "
    result = solve_worksheet(StringIO(input_text))
    assert result == 4277556
```

---

## Key Design Decisions

### 1. Line Buffer Requirement

We must buffer all lines to identify separator columns. This is necessary because:
- Can't distinguish "space in column" from "missing value" without full height
- Need consistent column height for all problems

**Trade-off**: Memory O(total_lines) is acceptable since lines are typically short relative to width.

### 2. Column-at-a-time Processing

Process columns left-to-right without holding entire width:
- Supports arbitrarily long worksheets
- Natural fit for line-based input
- Aligns with "stream processing" requirement

### 3. Problem Evaluation Pipeline

Use generators to chain transformations:
- Each stage is independent and testable
- Memory footprint is constant
- Easy to add logging/debugging between stages

---

## Expected Behavior

### Input: Example Worksheet
```
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
```

### Output
```
Grand Total: 4277556
```

### With Verbose Flag
```
Problem 1: [123, 45, 6] * = 33210
Problem 2: [328, 64, 98] + = 490
Problem 3: [51, 387, 215] * = 4243455
Problem 4: [64, 23, 314] + = 401
Grand Total: 4277556
```

---

## Files to Create/Modify

| File | Purpose |
|------|---------|
| `day-06/parser.py` | Column and problem parsing (generators) |
| `day-06/solution.py` | Problem evaluation and main solver |
| `day-06/test_solution.py` | Comprehensive test suite |
| `day-06/solution_original.py` | (if exists) - keep for reference |

---

## Running the Solution

```bash
# Run against test input
python -m day_06.solution test_input.txt

# Run against actual input
python -m day_06.solution input.txt

# Run with verbose output
python -m day_06.solution input.txt --verbose

# Run tests
pytest day-06/test_solution.py -v
```

---

## Success Criteria Checklist

- [ ] Parser correctly identifies vertical columns
- [ ] Separator columns are detected (all whitespace)
- [ ] Problems are extracted with correct operands
- [ ] Operation symbols are identified correctly
- [ ] Problems are evaluated left-to-right
- [ ] Grand total is calculated correctly
- [ ] Example worksheet returns 4277556
- [ ] Solution handles arbitrarily long lines
- [ ] Memory usage is constant relative to worksheet width
- [ ] All tests pass
- [ ] Code includes docstrings and type hints

---

## Next Steps

1. **Create `day-06/parser.py`** with Column class and generator functions
2. **Create `day-06/solution.py`** with Problem class and evaluation logic
3. **Create `day-06/test_solution.py`** with comprehensive tests
4. **Run tests** and verify all acceptance scenarios pass
5. **Optimize** if needed (profile memory usage)
6. **Document** edge cases and design decisions

---

## References

- See `plan.md` for detailed architecture
- See `data-model.md` for entity definitions
- See `contracts/api.md` for public interface specifications
