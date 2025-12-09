# Architecture Diagram: Day 6, Part 1

## Overall Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                     INPUT: Text File (Line Stream)               │
│  Each line can be arbitrarily long (supports streaming)         │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     │ read_lines_as_stream()
                     │ (Generator)
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│              STAGE 1: LINE STREAM                                 │
│                                                                   │
│  Yields: Individual lines from input                             │
│  Memory: O(1) - one line at a time                               │
│  Purpose: Support arbitrarily long lines                         │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     │ columns_from_lines()
                     │ (Generator)
                     │ Requires: Buffering all lines for height
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│              STAGE 2: COLUMN STREAM                               │
│                                                                   │
│  Lines:  ["123", " 45", "  6", " * "]                            │
│  Col 0:  Column(index=0, values=['1',' ',' ',' '])               │
│  Col 1:  Column(index=1, values=['2','4','6','*'])               │
│  Col 2:  Column(index=2, values=['3','5','  '])                  │
│  Col 3:  Column(index=3, values=[' ',' ',' ',' ']) ← SEPARATOR   │
│  Col 4:  Column(index=4, values=['3','6','9','+'])               │
│  ...                                                              │
│                                                                   │
│  Yields: Columns left-to-right                                   │
│  Memory: O(1) - one column at a time                             │
│  Purpose: Process width without limit                            │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     │ problem_column_groups()
                     │ (Generator)
                     │ Groups by separators (is_separator=True)
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│          STAGE 3: PROBLEM GROUP STREAM                            │
│                                                                   │
│  Group 1: [Col0, Col1, Col2]       (123 * 45 * 6)                │
│  Separator: [Col3]                 (all spaces)                  │
│  Group 2: [Col4, Col5, Col6]       (328 + 64 + 98)               │
│  Separator: [Col7]                 (all spaces)                  │
│  Group 3: [Col8, ...]              (51 * 387 * 215)              │
│  ...                                                              │
│                                                                   │
│  Yields: Problem groups                                          │
│  Memory: O(max_problem_width)                                    │
│  Purpose: Organize columns for extraction                        │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     │ extract_problem()
                     │ (Sequential processing)
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│            STAGE 4: PROBLEM STREAM                                │
│                                                                   │
│  Problem 1: Problem(                                              │
│      operands=[123, 45, 6],                                       │
│      operation='*',                                               │
│      result=None)                                                 │
│                                                                   │
│  Problem 2: Problem(                                              │
│      operands=[328, 64, 98],                                      │
│      operation='+',                                               │
│      result=None)                                                 │
│  ...                                                              │
│                                                                   │
│  Processing: For each group, extract operands & operation        │
│  Memory: O(max_problem_width)                                    │
│  Purpose: Structured representation of problem                   │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     │ evaluate_problem()
                     │ (Sequential evaluation)
                     │ Accumulate to grand_total
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│          STAGE 5: RESULT ACCUMULATION                             │
│                                                                   │
│  Problem 1: 123 * 45 * 6         → 33210      ┐                  │
│  Problem 2: 328 + 64 + 98        → 490        │                  │
│  Problem 3: 51 * 387 * 215       → 4243455    ├─ Sum             │
│  Problem 4: 64 + 23 + 314        → 401        │                  │
│                                                ▼                  │
│  GRAND TOTAL = 4277556                                            │
│                                                                   │
│  Memory: O(1) - only tracking accumulator                        │
│  Purpose: Produce final answer                                   │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                  OUTPUT: Grand Total (int)                        │
│                        4277556                                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Module Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                       solution.py                                 │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  solve_worksheet(source) ─┐                                      │
│      ▼                     │                                      │
│  1. Lines ←───────────────┼──────────── read_lines_as_stream()   │
│      │                    │                                       │
│  2. Columns ←─────────────┼──────────── columns_from_lines()     │
│      │                    │                                       │
│  3. Groups ←──────────────┼──────────── problem_column_groups()  │
│      │                    │                                       │
│  4. For each group:       │                                       │
│      │                    │                                       │
│  4a. Problem ←────────────┼──────────── extract_problem()        │
│      │                    │                                       │
│  4b. Result ←─────────────┼──────────── evaluate_problem()       │
│      │                    │                                       │
│  5. Accumulate → grand_total                                     │
│                           │                                       │
│  Return grand_total ──────┘                                      │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Imported from parser.py                      │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘


┌──────────────────────────────────────────────────────────────────┐
│                       parser.py                                   │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  read_lines_as_stream(source)                                    │
│    Returns: Iterator[str]                                        │
│    Generator yielding one line per iteration                     │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ class Column:                                           │    │
│  │   index: int                                            │    │
│  │   values: List[str]                                     │    │
│  │   @property is_separator() -> bool                      │    │
│  │   @property content() -> str                            │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                   │
│  columns_from_lines(lines)                                       │
│    Input: Iterator[str]                                          │
│    Returns: Iterator[Column]                                     │
│    Generator yielding columns left-to-right                      │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ class ProblemGroup:                                     │    │
│  │   start_column: int                                     │    │
│  │   end_column: int                                       │    │
│  │   columns: List[Column]                                 │    │
│  │   @property width() -> int                              │    │
│  │   @property height() -> int                             │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                   │
│  problem_column_groups(columns)                                  │
│    Input: Iterator[Column]                                       │
│    Returns: Iterator[ProblemGroup]                               │
│    Groups columns by separator boundaries                        │
│                                                                   │
│  extract_problem(group: ProblemGroup)                            │
│    Returns: Problem                                              │
│    Parses operands and operation from columns                    │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘

                                     ┌─────────────────────┐
                                     │ ┌───────────────┐   │
                                     │ │ class Problem │   │
                                     │ │  operands: [] │   │
                                     │ │  operation: ''│   │
                                     │ │  result: int  │   │
                                     │ └───────────────┘   │
                                     │                     │
                                     │ evaluate_problem()  │
                                     │   → int             │
                                     └─────────────────────┘
                                         (from solution.py)
```

---

## Memory Usage Profile

```
                    Memory Usage Over Time
                    ─────────────────────

  ▲
  │    Input buffering phase
  │    (buffering all lines)
  │    
M │    ┌────────────┐
e │    │            │
m │    │   PEAK     │ (height = #lines × avg_line_length)
o │    │            │
r │    │            │
y │    │            │
  │    └────┬───────┘
  │         │
  │    Processing phase
  │    (columns & groups streamed)
  │    ┌─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┐
  │    │  ~constant memory      │  (width × problem_height)
  │    │  for active columns    │
  │    └─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┘
  │         │
  │    Result accumulation
  │    ┌──────────────────────┐
  │    │ minimal memory (1)   │
  │    └──────────────────────┘
  │
  └─────────────────────────────────────────────────► Time
    Input   Processing   Completion
```

---

## Data Flow Example

```
Input (4 lines):
┌──────────────────────┐
│ 123 328  51 64      │
│  45 64  387 23      │
│   6 98  215 314     │
│ *   +   *   +       │
└──────────────────────┘

Step 1: Lines Stream
┌─────────────┬─────────────┬─────────────┬──────────────┐
│ "123 328..." │ " 45 64 ..." │ "  6 98 ..." │ "*   +   ..." │
└─────────────┴─────────────┴─────────────┴──────────────┘

Step 2: Columns Stream
Cols:  0   1   2   3   4   5   6   7   8   9  10  11  12  13  14
      ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
      │ 1 │ 2 │ 3 │   │ 3 │ 2 │ 8 │   │ 5 │ 1 │   │ 6 │ 4 │   │   │
      │   │ 4 │ 5 │   │   │ 6 │ 4 │   │ 3 │   │   │ 2 │ 3 │   │   │
      │   │   │ 6 │   │   │ 9 │ 8 │   │ 2 │ 2 │   │ 3 │ 1 │   │   │
      │ * │   │   │   │ + │   │   │   │ * │   │   │   │   │ + │   │
      └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
      │<─ Gr1  ─>│Sep│<─ Gr2  ─>│Sep│<─ Gr3  ─>│Sep│<─ Gr4  ─>│Sep│

Step 3: Problem Groups
┌──────────────────────┬──────────────────────┬──────────────────────┬──────────────────────┐
│ [Col0, Col1, Col2]   │ [Col4, Col5, Col6]   │ [Col8, Col9, Col10]  │ [Col12, Col13, Col14]│
└──────────────────────┴──────────────────────┴──────────────────────┴──────────────────────┘

Step 4: Extract Problems
┌──────────────────────┬──────────────────────┬──────────────────────┬──────────────────────┐
│ Problem(             │ Problem(             │ Problem(             │ Problem(             │
│   operands=[         │   operands=[         │   operands=[         │   operands=[         │
│     123, 45, 6       │     328, 64, 98      │     51, 387, 215     │     64, 23, 314      │
│   ],                 │   ],                 │   ],                 │   ],                 │
│   operation='*'      │   operation='+'      │   operation='*'      │   operation='+'      │
│ )                    │ )                    │ )                    │ )                    │
└──────────────────────┴──────────────────────┴──────────────────────┴──────────────────────┘
      ↓ evaluate          ↓ evaluate            ↓ evaluate           ↓ evaluate
    33210   +              490          +        4243455      +         401
    └────────────────────────────────────────────────────────────────────┘
                              ↓ sum
                            4277556  ← GRAND TOTAL
```

---

## Processing Pipeline Code

```python
# Conceptual view of solve_worksheet()

def solve_worksheet(source):
    """Process entire worksheet as a pipeline of generators."""
    
    lines = read_lines_as_stream(source)
    #  Generator: yields Line objects
    
    columns = columns_from_lines(lines)
    #  Generator: yields Column objects
    
    groups = problem_column_groups(columns)
    #  Generator: yields ProblemGroup objects
    
    grand_total = 0
    for group in groups:
        problem = extract_problem(group)
        #  Parses this group into a Problem object
        
        result = evaluate_problem(problem)
        #  Computes result left-to-right
        
        grand_total += result
        #  Accumulate
    
    return grand_total
```

**Memory analysis**:
1. `lines` - Generator (O(1) per line)
2. `columns` - Generator (O(1) per column)
3. `groups` - Generator (O(width) for current problem group)
4. `extract_problem()` - O(width) for current problem
5. `evaluate_problem()` - O(1) - just arithmetic
6. `grand_total` - O(1) - just accumulator

**Total memory**: O(lines_buffered) + O(max_problem_width) = constant relative to worksheet **width**
