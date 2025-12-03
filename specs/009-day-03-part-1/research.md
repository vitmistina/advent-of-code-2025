# Research: Day 3 Part 1 - Battery Bank Joltage Calculator

**Feature**: [spec.md](spec.md)  
**Date**: December 3, 2025  
**Purpose**: Research technical decisions and algorithms for maximum joltage calculation

## Research Questions

### 1. How to find the maximum two-digit number from a string of digits?

**Decision**: Greedy two-pass algorithm with O(n) complexity

**Rationale**:

- A battery bank is a string of digits where each digit represents a battery
- We need to select exactly two digits that form the largest two-digit number
- The digits must maintain their original left-to-right order (no rearranging)
- The "joltage" is calculated as: first_digit \* 10 + second_digit
- **Key insight**: The optimal solution is always:
  1. First battery: Maximum digit in `bank[:-1]` (all except last, since we need at least one digit after it)
  2. Second battery: Maximum digit in the substring AFTER the first battery's position

**Algorithm correctness proof**:

Let's verify with all examples:

1. `987654321111111`:

   - Max in `bank[:-1]` = '9' at position 0
   - Max in `bank[1:]` = '8' at position 1
   - Result: 98 ✓

2. `811111111111119`:

   - Max in `bank[:-1]` = '8' at position 0
   - Max in `bank[1:]` = '9' at position 14
   - Result: 89 ✓

3. `234234234234278`:

   - Max in `bank[:-1]` = '7' at position 13
   - Max in `bank[14:]` = '8' at position 14
   - Result: 78 ✓

4. `818181911112111`:
   - Max in `bank[:-1]` = '9' at position 6
   - Max in `bank[7:]` = '2' at position 13
   - Result: 92 ✓

**Why greedy works**:

- To maximize a two-digit number XY, we want X to be as large as possible (tens place has 10x weight)
- Among all positions with max X, we want the **earliest** occurrence (to maximize the substring available for finding max Y)
- Then we want Y to be as large as possible from the remaining digits after position of X

**Alternatives considered**:

- **Brute-force O(n²)**: Check all pairs - correct but unnecessarily slow, rejected for performance
- **Sort and take top two**: Violates "cannot rearrange" constraint - rejected
- **Take first two max digits globally**: Fails if max digit is last (no second digit available) - rejected
- **Dynamic programming**: Overkill for this problem - rejected

**Implementation approach**:

```python
def max_joltage(bank: str) -> int:
    """Find maximum joltage from a battery bank using greedy algorithm."""
    if len(bank) < 2:
        return 0

    # Find the maximum digit in all positions except the last
    # (we need at least one digit after the first battery)
    max_first_digit = max(bank[:-1])
    first_pos = bank.index(max_first_digit)

    # Find the maximum digit after the first battery
    max_second_digit = max(bank[first_pos + 1:])

    # Calculate joltage
    joltage = int(max_first_digit) * 10 + int(max_second_digit)
    return joltage
```

**Test cases**:

- `max_joltage("987654321111111")` → 98 (first='9' at 0, second='8' at 1)
- `max_joltage("811111111111119")` → 89 (first='8' at 0, second='9' at 14)
- `max_joltage("234234234234278")` → 78 (first='7' at 13, second='8' at 14)
- `max_joltage("818181911112111")` → 92 (first='9' at 6, second='2' at 13)
- `max_joltage("45")` → 45 (first='4' at 0, second='5' at 1)
- `max_joltage("987")` → 98 (first='9' at 0, second='8' at 1)
- `max_joltage("5555555")` → 55 (first='5' at 0, second='5' at 1)
- `max_joltage("123456789")` → 89 (first='8' at 7, second='9' at 8)

**Performance benefits**:

- **Greedy algorithm**: O(n) - linear scan to find max in each substring
  - `max(bank[:-1])` = O(n)
  - `bank.index(max_first_digit)` = O(n)
  - `max(bank[first_pos + 1:])` = O(n)
  - Total: O(n)
- **Brute-force alternative**: O(n²) - check all pairs
- **Improvement**: For n=100: Greedy=~300 ops vs Brute-force=5000 ops (16x faster)
- **For typical banks** (n≈15): Greedy=~45 ops vs Brute-force=105 ops (2.3x faster)

### 2. How to parse input and handle multiple battery banks?

**Decision**: Split by newlines, process each line independently

**Rationale**:

- Input format is one battery bank per line
- Each line contains only digit characters ('1' through '9')
- Process each bank independently and sum the maximum joltages
- Python's `splitlines()` handles various newline formats

**Alternatives considered**:

- **Manual line parsing**: More complex, no benefit over splitlines()
- **Streaming/generator**: Overkill for small input sizes

**Implementation approach**:

```python
def parse_input(input_text: str) -> list[str]:
    """Parse input into list of battery bank strings."""
    return [line.strip() for line in input_text.strip().splitlines() if line.strip()]
```

**Test cases**:

- Multi-line input correctly splits into separate banks
- Empty lines are filtered out
- Leading/trailing whitespace is handled

### 3. How to calculate total output joltage?

**Decision**: Sum the maximum joltage from each battery bank

**Rationale**:

- Each bank independently produces its maximum joltage
- Total output is the sum across all banks
- Simple accumulation pattern

**Implementation approach**:

```python
def solve_part1(input_text: str) -> int:
    """Solve Day 3 Part 1: Calculate total output joltage."""
    banks = parse_input(input_text)
    total = sum(max_joltage(bank) for bank in banks)
    return total
```

**Test case (from problem)**:

```
Input:
987654321111111
811111111111119
234234234234278
818181911112111

Output: 98 + 89 + 78 + 92 = 357
```

### 4. Edge cases to handle

**Decision**: Defensive validation with clear behavior

**Rationale**: AoC inputs are well-formed, but tests should validate edge cases

**Edge cases identified**:

1. **Two-digit bank** (e.g., "45"): Only one choice, first='4', second='5' → 45
2. **All same digits** (e.g., "5555555"): First='5' at 0, second='5' at 1 → 55
3. **Empty input**: Return 0 (no banks = no joltage)
4. **Single digit bank**: Invalid per problem constraints (need exactly 2 batteries)
5. **Non-digit characters**: Should be caught by validation or cause natural error

**Handling approach**:

- Two-digit bank: Naturally handled (first at 0, second at 1)
- All same digits: Naturally handled (max of all '5's is '5')
- Empty input: Early return with 0 from sum()
- Single digit: Implementation returns 0 (len(bank) < 2 check)
- Non-digits: Problem guarantees valid input, but max() will handle correctly

### 5. Testing strategy

**Decision**: TDD with RED-GREEN-REFACTOR cycle

**Rationale**: Following Constitution Principle IV (NON-NEGOTIABLE)

**Test organization**:

1. **RED Phase**: Write failing tests for:
   - `test_max_joltage()` - core maximum calculation logic
   - `test_max_joltage_edge_cases()` - boundary conditions
   - `test_parse_input()` - input parsing
   - `test_solve_part1()` - integration with full example
2. **GREEN Phase**: Implement minimal code to pass
3. **REFACTOR Phase**: Clean up if needed

**Example test structure**:

```python
def test_max_joltage():
    """Test maximum joltage calculation for each example."""
    assert max_joltage("987654321111111") == 98
    assert max_joltage("811111111111119") == 89
    assert max_joltage("234234234234278") == 78
    assert max_joltage("818181911112111") == 92

def test_max_joltage_edge_cases():
    """Test edge cases."""
    assert max_joltage("45") == 45
    assert max_joltage("5555555") == 55
    assert max_joltage("987") == 98
    assert max_joltage("123456789") == 89

def test_solve_part1():
    """Test full example from problem."""
    input_text = """987654321111111
811111111111119
234234234234278
818181911112111"""
    assert solve_part1(input_text) == 357
```

## Technology Stack Decisions

### Language Features

- **Python 3.10+**: Use type hints for clarity
- **Stdlib only**: No external dependencies beyond pytest
- **Built-in functions**: `max()` and `str.index()` for greedy algorithm

### Performance Considerations

- **Greedy algorithm**: O(n) per bank where n = number of digits
- **Three linear scans**: Finding max, finding index, finding second max
- **Typical bank size**: 15-20 digits → ~45-60 operations per bank
- **Worst case**: 100 digits → ~300 operations per bank
- **Expected total time**: < 10ms for actual input
- **Much faster than brute-force**: Linear vs quadratic complexity

### Code Structure

```
solution.py:
- parse_input(input_text: str) -> list[str]
- max_joltage(bank: str) -> int
- solve_part1(input_text: str) -> int
- main() - entry point for running with input.txt

test_solution.py:
- test_max_joltage()
- test_max_joltage_edge_cases()
- test_parse_input()
- test_solve_part1()
```

## Risk Assessment

### Low Risk

- ✅ Algorithm correctness: Greedy approach proven with all examples
- ✅ Input parsing: Simple line-based format
- ✅ Test coverage: All examples from problem included
- ✅ Performance: O(n) is excellent

### Medium Risk

- ⚠️ Edge case with single digit bank: Mitigated by len check

### No Risk

- Integer overflow (single-digit \* 10 + single-digit ≤ 99)
- Memory usage (small strings)
- Input validation (problem guarantees valid format)
- Performance (O(n) is optimal for this problem)

## Open Questions

**None** - All technical decisions resolved through research phase. Greedy algorithm is both correct and optimal.

## Performance Validation

**Complexity Analysis**:

- parse_input: O(L) where L = total input length
- max_joltage: O(n) where n = digits in one bank
- solve_part1: O(B × n) where B = number of banks, n = avg digits per bank

**Expected Performance**:

- 1000 banks × 20 digits each × 60 operations = 1.2M operations
- Modern CPU: ~1-10 ns per operation
- Total time: < 10ms

**Conclusion**: Greedy algorithm is optimal - O(n) is the best we can achieve since we must examine all digits at least once.
