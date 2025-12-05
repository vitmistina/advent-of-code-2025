# Day 5: Fresh Ingredient ID Validation

## Part 1: Count Fresh Ingredients

### Problem Summary

Given a database of fresh ingredient ID ranges and a list of available ingredient IDs, determine how many of the available ingredients are fresh.

The database format consists of:

1. Fresh ID ranges (e.g., `3-5`, `10-14`) on separate lines
2. A blank line separator
3. Available ingredient IDs, one per line

### Approach

The solution uses an efficient interval merging and binary search approach:

1. **Parse**: Extract fresh ranges and ingredient IDs from the database format
2. **Merge**: Combine overlapping/adjacent ranges into disjoint intervals - O(R log R)
3. **Validate**: Use binary search to check each ingredient ID against merged ranges - O(I log R)

**Time Complexity**: O(R log R + I log R) where R = number of ranges, I = number of ingredient IDs

### Key Components

- `FreshRange`: Dataclass representing an inclusive range [start, end]
- `merge_ranges()`: Merges overlapping ranges into sorted, disjoint intervals
- `parse_database()`: Parses database format into ranges and IDs
- `is_fresh()`: Binary search to check if an ID falls within any merged range
- `solve_part1()`: Integrates all components to count fresh ingredients

### Usage

```bash
# Run with test input
uv run day-05/solution.py --test --part 1

# Run with real input
uv run day-05/solution.py --part 1

# Run tests
uv run pytest day-05/test_solution.py -v
```

### Example

**Input:**

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

**Merged Ranges:** `[(3, 5), (10, 20)]`  
**Fresh IDs:** `5, 11, 17`  
**Result:** `3`

## Part 2: Count All Fresh Ingredients

### Problem Summary

Determine the **total count of all unique ingredient IDs that are fresh** across all fresh ranges, completely ignoring the available IDs section.

### Approach

The solution reuses the efficient interval merging from Part 1:

1. **Parse**: Extract only fresh ranges (ignore available IDs section) - O(R)
2. **Merge**: Combine overlapping/adjacent ranges into disjoint intervals - O(R log R)
3. **Sum**: Add up all IDs within each merged range - O(R)

**Time Complexity**: O(R log R) where R = number of ranges (no binary search needed)

### Key Components

- `parse_ranges_part2()`: Extracts only ranges section, ignores available IDs
- `solve_part2()`: Merges ranges and sums all IDs within merged intervals

### Usage

```bash
# Run with test input
uv run day-05/solution.py --test --part 2

# Run with real input
uv run day-05/solution.py --part 2

# Run tests
uv run pytest day-05/test_solution.py -v -k "part2"
```

### Example

**Input:**

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

**Merged Ranges:** `[(3, 5), (10, 20)]`  
**All Fresh IDs:** `3, 4, 5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20`  
**Result:** `14`

### Key Difference from Part 1

- **Part 1**: Checks if specific IDs from the available list are fresh
- **Part 2**: Counts ALL fresh IDs across entire ranges, ignores the available list

### Development

- Comprehensive tests covering 7 acceptance scenarios + 4 edge cases
- All tests pass with TDD workflow
- PEP8 compliant code via ruff linting
