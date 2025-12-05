# Quickstart: Day 5 Part 2 - Fresh Ingredient ID Range Coverage

## How to Run

1. Ensure you are in the project root and have Python 3.10+ installed.
2. Run the solution for part 2:

```sh
uv run day-05/solution.py --part 2
```

- By default, this uses `input.txt` in `day-05/`.
- To use the test input:

```sh
uv run day-05/solution.py --part 2 --test
```

## How to Test

```sh
uv run -m pytest day-05/test_solution.py
```

## API Contract (Optional)

- See `specs/013-day-05-part-2/contracts/fresh-range-count.openapi.yaml` for a sample API contract.

## Notes

- The available IDs section in the input is ignored for Part 2.
- The merging logic is reused from Part 1 for efficiency.

**Phase**: Phase 1 (Design & Contracts)  
**Status**: Completed  
**Date**: December 5, 2025

## Quick Overview

**Goal**: Calculate the total number of unique ingredient IDs that are fresh (within any fresh range).

**Key Difference from Part 1**:

- Part 1: Check if specific available IDs are fresh (binary lookup)
- Part 2: Count ALL fresh IDs across all ranges (union calculation)

**Complexity**: O(R log R) time, O(R) space where R = number of ranges

---

## Usage

### Basic Usage

```python
from day_05.solution import solve_part2

data = open("day-05/test_input.txt").read()
result = solve_part2(data)
print(f"Total fresh IDs: {result}")
```

### Input Format

```
3-5
10-14
16-20
12-18

1
5
8
11
17
32
```

- **Lines 1-4**: Fresh ingredient ID ranges (inclusive, format: START-END)
- **Blank line**: Separator
- **Lines 5+**: Available ingredient IDs (ignored by Part 2)

### Expected Output

```python
solve_part2(test_data)  # → 14
```

**Why 14?**

- Fresh ranges: [3-5], [10-14], [16-20], [12-18]
- After merge: [3-5], [10-20] (overlapping ranges [10-14], [16-20], [12-18] merge)
- Count: (5-3+1) + (20-10+1) = 3 + 11 = 14

---

## Testing

### Running Tests

```bash
# Run all Day 5 tests (Parts 1 & 2)
uv run pytest day-05/test_solution.py -v

# Run only Part 2 tests
uv run pytest day-05/test_solution.py -k "part2" -v

# Run with coverage
uv run pytest day-05/test_solution.py --cov=day_05
```

### Test Scenarios (TDD Red-Green-Refactor)

All tests are designed to pass once `solve_part2()` is implemented:

**Basic Cases**:

```python
def test_single_range():
    data = "5-5\n\n"
    assert solve_part2(data) == 1

def test_multiple_non_overlapping():
    data = "1-3\n5-7\n\n"
    assert solve_part2(data) == 6  # 1,2,3,5,6,7 (gap at 4)

def test_overlapping_ranges():
    data = "3-5\n1-4\n\n"
    assert solve_part2(data) == 5  # Union: 1,2,3,4,5
```

**Example from Specification**:

```python
def test_example_database():
    data = "3-5\n10-14\n16-20\n12-18\n\n1\n5\n8\n11\n17\n32\n"
    assert solve_part2(data) == 14
```

**Adjacent Ranges** (must be merged):

```python
def test_adjacent_ranges_merged():
    data = "1-10\n11-20\n\n"
    assert solve_part2(data) == 20  # Merged into [1-20]
```

---

## Implementation Checklist

- [ ] **Step 1**: Read `spec.md` and acceptance criteria
- [ ] **Step 2**: Write test cases (RED - tests fail)
- [ ] **Step 3**: Implement `solve_part2(data: str) -> int`
  - Parse database: `ranges, _ = parse_database(data)`
  - Merge ranges: `merged = merge_ranges(ranges)`
  - Count IDs: `sum(end - start + 1 for start, end in merged)`
- [ ] **Step 4**: Run tests (GREEN - tests pass)
- [ ] **Step 5**: Refactor and optimize (REFACTOR - keep tests green)
- [ ] **Step 6**: Run full test suite: `uv run pytest day-05/`
- [ ] **Step 7**: Test with real input: `uv run day-05/solution.py --part 2`

---

## Key Design Decisions

### 1. Reuse Part 1 Functions

- `parse_database()` - Already handles input parsing
- `merge_ranges()` - Already implements O(R log R) union logic
- `FreshRange` - Already validates ranges

### 2. Ignore Available IDs

```python
ranges, _ = parse_database(data)  # Discard available_ids
```

- Part 2 specification explicitly states available IDs are irrelevant
- Simplifies parsing and avoids wasted iterations

### 3. Count via Arithmetic (Not Enumeration)

```python
# ✅ CORRECT: O(M) counting
total = sum(end - start + 1 for start, end in merged)

# ❌ WRONG: O(N) enumeration (memory explosion for large ranges)
total = len(set(id for start, end in merged for id in range(start, end+1)))
```

### 4. Merge Adjacent Ranges

```python
# Input: [1-10, 11-20]
# After merge: [(1, 20)]
# Count: 20 (not 21, no double-counting at boundary)
```

---

## Complexity Analysis

| Operation | Time           | Space    | Notes                        |
| --------- | -------------- | -------- | ---------------------------- |
| Parse     | O(R)           | O(R)     | R = number of ranges         |
| Merge     | O(R log R)     | O(R)     | Sort + single-pass merge     |
| Count     | O(M)           | O(1)     | M = merged intervals (M ≤ R) |
| **Total** | **O(R log R)** | **O(R)** | Dominated by sort            |

**Why Not Slower Alternatives?**

- ❌ O(N) enumeration: N = total IDs could be billions
- ❌ O(R × MAX_ID): For 1000 ranges of [1, 1M], this is 1B ops
- ✅ O(R log R): For 1000 ranges, ~10K ops

---

## Example Walkthrough

### Input

```
3-5
10-14
16-20
12-18

1
5
8
11
17
32
```

### Step 1: Parse

```python
ranges = [FreshRange(3, 5), FreshRange(10, 14), FreshRange(16, 20), FreshRange(12, 18)]
available_ids = [1, 5, 8, 11, 17, 32]  # Ignored by Part 2
```

### Step 2: Sort (by start)

```python
ranges_sorted = [FreshRange(3, 5), FreshRange(10, 14), FreshRange(12, 18), FreshRange(16, 20)]
```

### Step 3: Merge

```
Process (3, 5):        merged = [(3, 5)]
Process (10, 14):      10 > 5+1 (gap), add new: merged = [(3, 5), (10, 14)]
Process (12, 18):      12 ≤ 14+1 (adjacent/overlap), merge: merged = [(3, 5), (10, 18)]
Process (16, 20):      16 ≤ 18+1 (adjacent), merge: merged = [(3, 5), (10, 20)]
```

### Step 4: Count

```python
interval_1 = (3, 5):    count = 5 - 3 + 1 = 3
interval_2 = (10, 20):  count = 20 - 10 + 1 = 11
total = 3 + 11 = 14
```

### Output

```python
14
```

---

## Running Against Real Input

```bash
# Part 2 only
uv run day-05/solution.py --part 2

# Output: Part 2: <result>
```

---

## Debugging Tips

### If Tests Fail

1. **Check parse_database()**:

   ```python
   data = "..."
   ranges, ids = parse_database(data)
   print(f"Parsed ranges: {ranges}")
   print(f"Parsed IDs: {ids}")
   ```

2. **Check merge_ranges()**:

   ```python
   merged = merge_ranges(ranges)
   print(f"Merged: {merged}")
   for start, end in merged:
       print(f"  [{start}, {end}] contains {end - start + 1} IDs")
   ```

3. **Check sum**:
   ```python
   total = sum(end - start + 1 for start, end in merged)
   print(f"Total: {total}")
   ```

### Common Issues

- **Wrong Count**: Verify merge output is correct (overlaps/adjacencies handled)
- **Off by One**: Remember ranges are inclusive: count = end - start + 1 (not end - start)
- **Parsing Error**: Ensure blank line separator exists between ranges and IDs
- **Empty Ranges**: Empty range list should return 0

---

## Next Steps

- ✅ **Design Complete**: Data model, contracts, and quickstart documented
- ⏭️ **TDD Tasks**: Run `/speckit.tasks` to generate RED-GREEN-REFACTOR task list
- ⏭️ **Implementation**: Start with RED (write failing tests)
- ⏭️ **Validation**: Ensure all tests pass (GREEN)
- ⏭️ **Optimization**: REFACTOR while keeping tests green
