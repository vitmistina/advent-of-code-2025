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

## Part 2: Extended Pattern Detection (At Least Twice)

**Answer**: `11323661261`

### Approach

**Algorithm**: Divisor-based pattern matching

- Part 2 extends Part 1 by detecting patterns repeated **at least twice** (vs exactly twice)
- Examples: 111 (1×3), 565656 (56×3), 824824824 (824×3), 2121212121 (21×5)
- Part 2 is a **superset** of Part 1 (includes all Part 1 invalids plus more)

**Algorithm Details**:

1. Convert number to string
2. Iterate through all divisors of string length (1 to len//2)
3. For each divisor, extract pattern and check if repeating it ≥2 times forms the string
4. Return true on first match (early termination)

**Complexity**: O(n²) per number where n = digit count (acceptable for AoC constraints)

### Implementation

1. **`is_invalid_id_part2(num: int) -> bool`**: Core pattern detection with divisor iteration
2. **`check_range_part2(start: int, end: int) -> list[int]`**: Scan range using Part 2 rules
3. **`solve_part2(input_text: str) -> int`**: Reuses `parse_ranges()` from Part 1, aggregates results

### Test Results

```
23 tests total (8 Part 1 + 15 Part 2), 100% pass rate in 0.07 seconds
✓ Part 1 backward compatibility maintained
✓ Pattern detection (11, 111, 565656, 824824824 all invalid)
✓ All 11 example ranges verified individually
✓ Full example sum = 4174379265
✓ Multi-range aggregation
✓ Edge cases (empty input, ranges with no invalids)
```

### Key Insights

- **Separate functions** preserved Part 1 backward compatibility
- **Divisor-based approach** handles arbitrary repetition counts elegantly
- **Early termination** optimizes performance (return on first pattern match)
- **TDD workflow** caught edge cases: "222222" can be 2×6, 22×3, or 222×2 (any match makes it invalid)

## Usage

```powershell
# Run tests
uv run pytest day-02/test_solution.py -v

# Run Part 1
uv run python day-02/solution.py --part 1
# Output: Part 1: 9188031749

# Run Part 2
uv run python day-02/solution.py --part 2
# Output: Part 2: 11323661261

# Lint and format
uv run ruff check day-02/
uv run ruff format day-02/
```

---

**Specification**:
- Part 1: `specs/007-day-02-part-1/`
- Part 2: `specs/008-day-02-part-2/`

**TDD Workflow**: RED-GREEN-REFACTOR cycle strictly followed
