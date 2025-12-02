# Day 2: Gift Shop Invalid Product ID Detection

## Puzzle Description

The gift shop's product database contains invalid IDs formed by repeating digit sequences. An ID is invalid if it consists of a digit sequence repeated exactly twice.

**Examples**: 55 (5+5), 6464 (64+64), 123123 (123+123)

See [description.md](description.md) for full problem statement.

## Part 1: Sum of Invalid IDs

**Answer**: `9188031749`

### Approach

**Algorithm**: String-based pattern matching

- Convert number to string
- Check if length is even (odd-length numbers cannot be split evenly)
- Split in half and compare: if `first_half == second_half`, it's invalid

**Complexity**: O(n × m) where n = total numbers, m = average digits per number

### Implementation

1. **`is_invalid_id(num: int) -> bool`**: Core pattern detection using string split
2. **`parse_ranges(input_text: str) -> list[tuple[int, int]]`**: Parse comma-separated ranges
3. **`find_invalid_ids_in_range(start: int, end: int) -> list[int]`**: Scan range for invalid IDs
4. **`solve_part1(input_text: str) -> int`**: Integrate all components and sum results

### Test Results

```
8 tests, 100% pass rate in 0.04 seconds
✓ Pattern detection (55→invalid, 101→valid)
✓ Edge cases (11, 22, single digits)
✓ Range scanning (11-22 → [11, 22])
✓ Input parsing (comma-separated ranges)
✓ Full example verification (sum = 1227775554)
```

### Key Insights

- **String manipulation** cleaner than arithmetic for pattern matching
- **TDD approach** caught edge cases early (odd-length, single digits)
- **Incremental implementation** enabled independent testing per user story

## Part 2

_Not yet attempted_

## Usage

```powershell
# Run tests
uv run pytest day-02/test_solution.py -v

# Run solution
python day-02/solution.py
# Output: Part 1: 9188031749

# Lint and format
uv run ruff check day-02/
uv run ruff format day-02/
```

---

**Specification**: `specs/007-day-02-part-1/`  
**TDD Workflow**: RED-GREEN-REFACTOR cycle strictly followed
