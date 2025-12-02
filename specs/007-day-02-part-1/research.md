# Research: Day 2 Part 1 - Invalid Product ID Detection

**Feature**: [spec.md](spec.md)  
**Date**: December 2, 2025  
**Purpose**: Research technical decisions and algorithms for invalid ID detection

## Research Questions

### 1. How to efficiently detect if a number is formed by repeating a digit sequence twice?

**Decision**: String-based pattern matching with mathematical validation

**Rationale**:

- A number is invalid if it can be split into two identical halves
- Algorithm: Convert number to string, check if first half == second half
- Works for all sizes: "55" → "5"+"5", "123123" → "123"+"123"
- Edge case: Must have even length (odd length cannot be split evenly)
- No leading zeros constraint is naturally handled (integer conversion)

**Alternatives considered**:

- **Pure mathematical approach**: Divide number repeatedly - rejected due to complexity for large numbers
- **Regex pattern matching**: Possible but less clear than direct string comparison
- **Generate and check**: Generate all possible repeated patterns - rejected as inefficient

**Implementation approach**:

```python
def is_invalid_id(num: int) -> bool:
    """Check if number is formed by repeating a sequence twice."""
    s = str(num)
    # Must have even length to split evenly
    if len(s) % 2 != 0:
        return False
    # Split in half and compare
    mid = len(s) // 2
    return s[:mid] == s[mid:]
```

**Test cases**:

- `is_invalid_id(55)` → True (5 + 5)
- `is_invalid_id(6464)` → True (64 + 64)
- `is_invalid_id(123123)` → True (123 + 123)
- `is_invalid_id(101)` → False (odd length)
- `is_invalid_id(121)` → False (odd length)
- `is_invalid_id(1212)` → True (12 + 12)

### 2. How to handle large ranges efficiently?

**Decision**: Iterate through ranges with early optimization for small ranges

**Rationale**:

- For ranges like "11-22", direct iteration is simple and fast
- For large ranges like "1188511880-1188511890", only 11 numbers to check
- Even for billions: range("222220-222224") = 5 numbers
- Python's range() is memory-efficient (generator, not list)
- O(1) check per number, O(n) total where n = range size

**Alternatives considered**:

- **Mathematical generation of invalid IDs**: Generate all possible repeated patterns and check if in range - more complex, not needed for given constraints
- **Pre-compute all invalid IDs**: Memory intensive, not needed
- **Binary search**: Overkill for linear pattern detection

**Implementation approach**:

```python
def find_invalid_ids_in_range(start: int, end: int) -> list[int]:
    """Find all invalid IDs in inclusive range [start, end]."""
    invalid_ids = []
    for num in range(start, end + 1):
        if is_invalid_id(num):
            invalid_ids.append(num)
    return invalid_ids
```

**Performance analysis**:

- Example input has ranges totaling ~100 numbers max
- Even 1 million numbers @ O(1) each = milliseconds
- Well within 10 second constraint

### 3. How to parse comma-separated ranges?

**Decision**: Simple string split and pattern extraction

**Rationale**:

- Format is well-defined: "start1-end1,start2-end2,..."
- Python's `split(',')` handles comma separation
- Split on '-' to extract start and end
- Convert to integers for range processing

**Alternatives considered**:

- **Regex parsing**: Overkill for simple format
- **CSV module**: Not needed for simple comma separation

**Implementation approach**:

```python
def parse_ranges(input_text: str) -> list[tuple[int, int]]:
    """Parse comma-separated ranges into list of (start, end) tuples."""
    ranges = []
    for range_str in input_text.strip().split(','):
        if not range_str.strip():
            continue
        start_str, end_str = range_str.strip().split('-')
        start, end = int(start_str), int(end_str)
        ranges.append((start, end))
    return ranges
```

**Test cases**:

- `"11-22,95-115"` → `[(11, 22), (95, 115)]`
- Single range `"998-1012"` → `[(998, 1012)]`
- With whitespace `"11-22, 95-115"` → `[(11, 22), (95, 115)]`

### 4. Edge cases to handle

**Decision**: Defensive validation with clear error messages

**Rationale**: AoC inputs are well-formed, but tests should validate edge cases

**Edge cases identified**:

1. **Single ID range** (e.g., "55-55"): Valid, check if 55 is invalid
2. **Large numbers**: Python handles arbitrary precision integers
3. **Empty input**: Return empty list or 0 sum
4. **Reversed range** (e.g., "100-50"): Error or treat as empty
5. **Malformed format**: Should raise clear error in tests

**Handling approach**:

- Single ID: Natural handling via `range(55, 56)` = [55]
- Large numbers: No special handling needed (Python int)
- Empty input: Early return with empty result
- Reversed range: Document as invalid, may skip or error
- Malformed: Let split() raise natural errors for now

### 5. Testing strategy

**Decision**: TDD with RED-GREEN-REFACTOR cycle

**Rationale**: Following Constitution Principle IV (NON-NEGOTIABLE)

**Test organization**:

1. **RED Phase**: Write failing tests for:
   - `test_is_invalid_id()` - core validation logic
   - `test_parse_ranges()` - input parsing
   - `test_find_invalid_ids_in_range()` - range scanning
   - `test_solve_part1()` - integration with example
2. **GREEN Phase**: Implement minimal code to pass

3. **REFACTOR Phase**: Optimize and clean

**Example test structure**:

```python
def test_is_invalid_id():
    assert is_invalid_id(55) == True
    assert is_invalid_id(6464) == True
    assert is_invalid_id(123123) == True
    assert is_invalid_id(101) == False
    assert is_invalid_id(99) == True
    assert is_invalid_id(1010) == True

def test_solve_part1_example():
    # Full example from problem
    input_text = "11-22,95-115,998-1012,..."
    result = solve_part1(input_text)
    assert result == 1227775554
```

## Technology Stack Decisions

### Language Features

- **Python 3.10+**: Use type hints, match statements if helpful
- **Stdlib only**: No external dependencies beyond pytest
- **Pathlib**: For file operations (reading input)

### Performance Considerations

- **String operations**: O(k) where k = digit count (negligible)
- **Range iteration**: O(n) where n = range size (manageable)
- **Total complexity**: O(R × N × K) where R=ranges, N=avg range size, K=avg digits
- **Expected**: < 100ms for actual input based on constraints

### Code Structure

```
solution.py:
- parse_ranges(input_text: str) -> list[tuple[int, int]]
- is_invalid_id(num: int) -> bool
- find_invalid_ids_in_range(start: int, end: int) -> list[int]
- solve_part1(input_text: str) -> int
- main() - entry point

test_solution.py:
- test_is_invalid_id()
- test_parse_ranges()
- test_find_invalid_ids_in_range()
- test_solve_part1_example()
```

## Risk Assessment

### Low Risk

- ✅ Algorithm complexity: O(1) per number check
- ✅ Input parsing: Well-defined format
- ✅ Test coverage: Clear examples provided

### Medium Risk

- ⚠️ Large range performance: Mitigated by generator-based iteration
- ⚠️ Edge cases: Mitigated by comprehensive test suite

### No Risk

- Python integer precision (unlimited)
- Memory usage (small ranges)

## Open Questions

**None** - All technical decisions resolved through research phase.
