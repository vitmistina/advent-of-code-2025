# Research & Design Decisions: Day 5 Part 2

**Phase**: Phase 0 (Outline & Research)  
**Status**: Completed  
**Date**: December 5, 2025

## Overview

This document consolidates all design decisions, architectural choices, and complexity analysis for Day 5 Part 2. All NEEDS CLARIFICATION items from the Technical Context have been resolved.

## Decision 1: Algorithm Choice - Range Merging (Union Strategy)

### Decision

**Use optimized range merging from Part 1 to compute the mathematical union of all fresh ID ranges.**

### Rationale

Part 2 requires calculating the **total count of unique fresh ingredient IDs** across all ranges without duplication. The spec explicitly states:

The range merging approach (union of intervals) is ideal because:

1. **Optimal complexity**: O(R log R) where R = number of ranges
2. **Memory efficient**: O(R) space; never stores individual IDs
3. **Scalable**: Works with any ID magnitude (tested up to 10^9)
4. **Already built**: Part 1 already implements `merge_ranges()`

### Alternatives Considered & Rejected

| Alternative                      | Complexity                                               | Why Rejected                                                   |
| -------------------------------- | -------------------------------------------------------- | -------------------------------------------------------------- |
| **Enumerate all IDs into a set** | O(N) time, O(N) space (N = total IDs)                    | N could be billions; memory infeasible                         |
| **Hash table lookup**            | O(N) time, O(N) space                                    | Same issue as enumeration; overkill for Part 2                 |
| **Naive iteration**              | O(R × MAX_ID) time                                       | For 1000 ranges of [1, 1M], this is 1B ops vs. merge's 10K ops |
| **Binary search per ID**         | O(I × log M) time (I = available IDs, M = merged ranges) | Unnecessary; Part 2 has no available IDs to check              |
| **Set math library**             | O(N)                                                     | Better to build with tuples; no external deps needed           |

### Verdict

✅ **CHOSEN**: Range merging (union of intervals) via `merge_ranges()` reuse

# Research: Day 5 Part 2 - Fresh Ingredient ID Range Coverage

## Decision: Reuse Range Merging Logic from Part 1

- Use the same merge_ranges() function as in Part 1 to union all inclusive ranges efficiently (O(R log R)).
- Only the ranges section (before the blank line) is parsed; available IDs are ignored.
- To get the total count, sum (end - start + 1) for each merged range.

## Rationale

- The merging logic is already robust, handles overlaps/adjacency, and is efficient for up to 1000 ranges.
- Parsing only the first section is simple and avoids unnecessary work.
- Summing merged range lengths is O(R) and avoids set allocation for large ranges.

## Alternatives Considered

- Allocating a set of all IDs (memory-inefficient for large ranges)
- Brute-force iteration (too slow for large input)
- Using interval trees (overkill for this problem size)

## Conclusion

- The chosen approach is optimal for AoC constraints and reuses tested code from Part 1.

## Decision 2: Reuse Part 1 Infrastructure

### Decision

**Leverage existing `merge_ranges()` and `FreshRange` from Part 1; add new `solve_part2()` function only.**

### Rationale

Part 1 already implements:

- `FreshRange(start, end)` dataclass with validation
- `merge_ranges(ranges: List[FreshRange]) -> List[Tuple[int, int]]` with O(R log R) complexity
- `parse_database()` for input parsing

Part 2 only needs to:

1. Parse ranges (reuse `parse_database()`)
2. Merge ranges (reuse `merge_ranges()`)
3. Sum IDs in merged intervals (new, trivial O(M) pass)
4. **Ignore available IDs section** (simplification from Part 1)

This avoids code duplication and maintains the DRY principle.

### Implementation Plan

```python
def solve_part2(data: str) -> int:
    """
    Calculate total unique fresh IDs across all ranges (union).
    Ignores available IDs section.

    Time: O(R log R) where R = number of ranges
    Space: O(R)
    """
    ranges, _ = parse_database(data)  # Ignore available IDs
    merged = merge_ranges(ranges)
    total_fresh = sum(end - start + 1 for start, end in merged)
    return total_fresh
```

### Verdict

✅ **CHOSEN**: Reuse Part 1 infrastructure; no reimplementation

---

## Decision 3: Handling Overlapping & Adjacent Ranges

### Decision

**Treat adjacent ranges (e.g., [1-10, 11-20]) as contiguous and merge into single interval [1-20].**

### Rationale

Per the specification:

- **FR-007**: "System MUST handle adjacent and contiguous ranges correctly by merging them into the union"
- Acceptance scenario 3 in spec: ranges [3-7] (overlapping) AND [5-10] (adjacent/overlapping) should merge cleanly

The existing `merge_ranges()` already implements the "adjacency threshold":

```python
if r.start <= last_end + 1:  # Adjacent or overlapping
    merged[-1] = (last_start, max(last_end, r.end))
```

This means:

- [1-10] and [11-20] → merged as [1-20] ✅
- [10-14] and [12-18] → merged as [10-18] ✅
- [3-5] and [10-14] → NOT merged (gap exists) ✅

### Example Walkthrough

```
Input ranges: [3-5, 10-14, 16-20, 12-18]
After sort:   [3-5, 10-14, 12-18, 16-20]
After merge:  [(3, 5), (10, 20)]

IDs in (3, 5):   3, 4, 5                    → 3 IDs
IDs in (10, 20): 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20  → 11 IDs
Total: 14 fresh IDs ✅
```

### Verdict

✅ **CHOSEN**: Reuse existing adjacency logic; no changes needed

---

## Decision 4: Complexity Target

### Decision

**Maintain O(R log R) time and O(R) space complexity as mandatory constraints.**

### Rationale

AoC puzzles vary widely:

- Small inputs: 5-20 ranges
- Typical inputs: 50-200 ranges
- Worst case: 1000+ ranges

Performance targets:

- **Small**: <1ms (trivial)
- **Typical**: <10ms (acceptable)
- **Worst**: <100ms (critical for timely submission)

Our O(R log R) approach:

- 20 ranges: 20 log 20 ≈ 86 ops → <1ms ✅
- 200 ranges: 200 log 200 ≈ 1,576 ops → <1ms ✅
- 1000 ranges: 1000 log 1000 ≈ 9,965 ops → <1ms ✅

Naive O(MAX_ID) alternatives would fail for large ID ranges.

### Verdict

✅ **CHOSEN**: O(R log R) target as per plan

---

## Decision 5: Memory Model

### Decision

**Store only range boundaries (start, end tuples); never enumerate individual IDs into memory.**

### Rationale

IDs can be arbitrarily large (e.g., range [1, 1,000,000,000]):

- **Cannot** store all 1B IDs in memory
- **Can** represent as single (1, 1000000000) tuple
- **Count** via arithmetic: 1000000000 - 1 + 1 = 1000000000 IDs

Memory usage:

- Input: R ranges → 3R integers (start, end + FreshRange overhead) ≈ O(R)
- After merge: M ranges ≤ R → 2M integers ≈ O(M) ≤ O(R)
- Total: O(R) space, independent of ID magnitude ✅

### Verdict

✅ **CHOSEN**: Tuple-based representation; no ID enumeration

---

## Decision 6: Testing Strategy

### Decision

**Extend Part 1's `test_solution.py` with new tests for `solve_part2()`; follow TDD (Red-Green-Refactor).**

### Rationale

From Constitution Principle IV (Test-Driven Development):

- RED: Write tests first (from spec acceptance scenarios)
- GREEN: Implement minimum code to pass tests
- REFACTOR: Clean up while keeping tests green

Part 2 test scenarios (from spec):

1. Single range [5-5] → count = 1
2. Multiple non-overlapping ranges [1-3, 5-7] → count = 6 (gap at 4)
3. Overlapping ranges [3-5, 1-4] → count = 5 (1-5 merged)
4. Adjacent ranges [1-10, 11-20] → count = 20 (merged into 1-20)
5. Heavily overlapping [3-7, 5-10, 1-6] → count = 10 (1-10 merged)
6. Example database [3-5, 10-14, 16-20, 12-18] → count = 14

### Verdict

✅ **CHOSEN**: Extend existing test suite with Part 2 tests

---

## Decision 7: Input Parsing Behavior

### Decision

**Reuse `parse_database()` but explicitly ignore available IDs returned (parse only ranges).**

### Rationale

Part 1: Uses `parse_database()` to get both ranges AND available IDs  
Part 2: Uses `parse_database()` to get ranges, discards available IDs

Input format (unchanged):

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

Part 2 ignores the IDs section after the blank line:

```python
ranges, _ = parse_database(data)  # Discard available IDs
```

### Rationale for Ignore

- Spec explicitly states Part 2 doesn't use available IDs
- Avoids wasted parsing overhead (O(I) where I = count of IDs)
- Keeps Part 2 focused on range union problem
- Simplifies acceptance criteria (no available ID filtering)

### Verdict

✅ **CHOSEN**: Parse ranges; ignore available IDs

---

## Summary of All Decisions

| #   | Decision                         | Complexity | Status    |
| --- | -------------------------------- | ---------- | --------- |
| 1   | Algorithm: Range merging (union) | O(R log R) | ✅ Chosen |
| 2   | Reuse Part 1 infrastructure      | -          | ✅ Chosen |
| 3   | Merge adjacent ranges            | O(R)       | ✅ Chosen |
| 4   | Maintain O(R log R) target       | -          | ✅ Chosen |
| 5   | Memory: tuple-based (no enum)    | O(R)       | ✅ Chosen |
| 6   | Testing: TDD with pytest         | -          | ✅ Chosen |
| 7   | Parsing: ranges only, ignore IDs | O(R)       | ✅ Chosen |

---

## Next Steps

✅ **Phase 0 (Research)**: Completed - all decisions documented  
⏭️ **Phase 1 (Design)**: Generate data-model.md, contracts, quickstart.md  
⏭️ **Phase 2 (Tasks)**: Run `/speckit.tasks` for TDD task breakdown
