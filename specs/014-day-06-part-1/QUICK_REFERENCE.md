# Quick Reference Card: Day 6, Part 1

## Problem At A Glance

```
INPUT:  Vertical math worksheet    OUTPUT: Grand total (int)
        (arbitrarily wide)                 
        
Example:
┌────────────────────────────┐
│ 123 328  51 64             │
│  45 64  387 23             │
│   6 98  215 314            │
│ *   +   *   +              │
└────────────────────────────┘

Problems:
  123 * 45 * 6    = 33,210
  328 + 64 + 98   = 490
  51 * 387 * 215  = 4,243,455
  64 + 23 + 314   = 401

ANSWER: 4,277,556
```

---

## Architecture Pipeline

```
read_lines_as_stream()
       ↓ (Generator)
columns_from_lines()
       ↓ (Generator)
problem_column_groups()
       ↓ (Generator)
extract_problem()
       ↓ (Sequential)
evaluate_problem()
       ↓ (Sequential)
grand_total (int)
```

**Key**: Each stage is a generator for memory efficiency

---

## Module Layout

### `parser.py`

```python
class Column:
    index: int
    values: List[str]
    @property is_separator: bool

class ProblemGroup:
    start_column: int
    end_column: int
    columns: List[Column]

def read_lines_as_stream(source) → Iterator[str]
def columns_from_lines(lines) → Iterator[Column]
def problem_column_groups(cols) → Iterator[ProblemGroup]
def extract_problem(group) → Problem
```

### `solution.py`

```python
class Problem:
    operands: List[int]
    operation: str        # '+' or '*'
    result: Optional[int]

def evaluate_problem(problem) → int
def solve_worksheet(source, verbose=False) → int
```

---

## Memory Profile

```
Phase          Memory        Note
─────────────────────────────────────────
Input buffering     O(lines)    Must buffer all lines
Column streaming    O(1)        Process one per iteration
Problem extraction  O(width)    Hold current problem
Evaluation          O(1)        Just arithmetic
Accumulation        O(1)        Sum accumulator
─────────────────────────────────────────
TOTAL               O(lines)    Constant w.r.t. width ✅
```

---

## Testing Checklist

- [ ] Parser: Column extraction
- [ ] Parser: Separator detection
- [ ] Parser: Problem grouping
- [ ] Parser: Number extraction
- [ ] Solution: Addition evaluation
- [ ] Solution: Multiplication evaluation
- [ ] Solution: Single problem
- [ ] Solution: Multiple problems
- [ ] Solution: Example = 4,277,556
- [ ] Integration: File input
- [ ] Integration: Large worksheet
- [ ] Edge cases: Wide lines
- [ ] Edge cases: Many problems

---

## Implementation Sequence

### Step 1: Column Class
```python
@dataclass
class Column:
    index: int
    values: List[str]
    
    @property
    def is_separator(self) -> bool:
        return all(v.isspace() or v == '' for v in self.values)
```

### Step 2: Line Streaming
```python
def read_lines_as_stream(source):
    with open(source) if isinstance(source, str) else source as f:
        for line in f:
            yield line
```

### Step 3: Column Transformation
```python
def columns_from_lines(lines):
    buffer = list(lines)
    max_width = max((len(line) for line in buffer), default=0)
    for col_idx in range(max_width):
        values = [line[col_idx] if col_idx < len(line) else ' ' 
                  for line in buffer]
        yield Column(index=col_idx, values=values)
```

### Step 4: Problem Grouping
```python
def problem_column_groups(columns):
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

### Step 5: Problem Extraction
```python
def extract_problem(group):
    # Last row = operation row
    operation_row = ''.join(col.values[-1] for col in group.columns)
    operation = '+' if '+' in operation_row else '*'
    
    # Extract numbers from columns
    operands = []
    for col in group.columns:
        num_str = ''.join(c for c in ''.join(col.values[:-1]) 
                         if c.isdigit())
        if num_str:
            operands.append(int(num_str))
    
    return Problem(operands=operands, operation=operation)
```

### Step 6: Problem Evaluation
```python
def evaluate_problem(problem):
    result = problem.operands[0]
    for operand in problem.operands[1:]:
        if problem.operation == '+':
            result += operand
        else:
            result *= operand
    return result
```

### Step 7: Main Solver
```python
def solve_worksheet(source, verbose=False):
    lines = read_lines_as_stream(source)
    cols = columns_from_lines(lines)
    groups = problem_column_groups(cols)
    
    grand_total = 0
    for group in groups:
        problem = extract_problem(group)
        result = evaluate_problem(problem)
        grand_total += result
        if verbose:
            print(f"{problem.operands} {problem.operation} = {result}")
    
    return grand_total
```

---

## Test Examples

```python
# Test 1: Single column
assert list(columns_from_lines(['a', 'b'])) == [Column(0, ['a', 'b'])]

# Test 2: Separator detection
col = Column(0, [' ', ' '])
assert col.is_separator == True

# Test 3: Grouping
groups = list(problem_column_groups([col1, sep, col2]))
assert len(groups) == 2

# Test 4: Addition
p = Problem([2, 3, 4], '+')
assert evaluate_problem(p) == 9

# Test 5: Multiplication
p = Problem([2, 3, 4], '*')
assert evaluate_problem(p) == 24

# Test 6: Example
result = solve_worksheet('test_input.txt')
assert result == 4277556
```

---

## Key Design Rationales

| Decision | Reason |
|----------|--------|
| Stream-based | Support arbitrarily long lines |
| Generators | Memory efficiency, lazy evaluation |
| Line buffering | Need full height for separator detection |
| Column separation | Natural processing left-to-right |
| Incremental grand total | Constant memory, supports progress |

---

## Error Handling

```python
# Inputs that should work
✓ File path (str)
✓ Path object
✓ File object (opened)
✓ Iterator of lines
✓ Arbitrarily wide worksheets
✓ Arbitrarily many problems

# Errors to handle
✗ Missing file → FileNotFoundError
✗ Malformed problem → ValueError
✗ Missing operation → ValueError
✗ < 2 operands → ValueError
✗ Invalid operation → ValueError
```

---

## Success Validation

```python
# Final test
result = solve_worksheet('input.txt')
print(f"Grand Total: {result}")

# Expected: 4277556 or whatever the correct answer is
# Memory: O(lines) - constant relative to width
# Speed: Linear in total input size
```

---

## Performance Considerations

```
Current approach:
  Time:   O(n) where n = total characters
  Memory: O(lines × avg_line_length) + O(max_problem_width)
  
Memory efficiency:
  ✅ Constant relative to WORKSHEET WIDTH
  ✅ Supports arbitrarily long lines
  ❌ Must buffer lines (necessary trade-off)
  
Optimization opportunities (if needed):
  • Stream lines in chunks if memory is constraint
  • Use memory-mapped I/O for huge files
  • Lazy-load operation evaluation
```

---

## References

| Doc | Purpose |
|-----|---------|
| spec.md | Full specification |
| plan.md | Implementation details |
| data-model.md | Entity definitions |
| contracts/api.md | Function signatures |
| ARCHITECTURE.md | Visual diagrams |
| quickstart.md | Implementation guide |

---

## Quick Commands

```bash
# Run solution
python -m day_06.solution input.txt

# Run tests
pytest day-06/test_solution.py -v

# Run with verbose output
python -m day_06.solution input.txt --verbose

# Check specific test
pytest day-06/test_solution.py::test_example_worksheet -v
```

---

## Status Indicators

- ✅ Specification: Complete
- ✅ Planning: Complete
- ✅ Architecture: Designed
- ✅ Contracts: Defined
- ⏳ Implementation: Ready to Start
- ⏳ Testing: Test cases planned
- ⏳ Documentation: Implementation to come

---

*This card summarizes the complete plan for Day 6, Part 1. Refer to full documents for details.*
