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

### Development

This solution follows Test-Driven Development (TDD):

- All tests written before implementation
- Comprehensive coverage for parsing, merging, and validation
- Verified against both test and real inputs
