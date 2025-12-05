# Phase 0 Research — Day 5 Part 1

## Decision 1: Represent fresh ranges as merged, sorted intervals (not enumerated sets)

- **Rationale**: Sorting ranges and merging overlaps models the union-of-intervals set view directly (set theory union). It caps preprocessing at `O(R log R)` and keeps memory at `O(R)` regardless of the span of IDs. Membership checks for each ingredient can then run via binary search or two-pointer traversal, giving `O(log R)` per lookup and keeping total runtime near `O(R log R + I log R)`.
- **Alternatives considered**:
  - **Enumerate every ID into a Python `set`**: simple to implement but devolves to `O(T)` preprocessing where `T` is total span of all ranges; impossible if large ranges appear (e.g., millions of IDs).
  - **Store raw ranges without merge**: still `O(R)` memory, but overlapping ranges would force multiple comparisons per ID and complicate correctness proofs.

## Decision 2: Use two-pointer sweep between merged ranges and sorted ingredient IDs for counting

- **Rationale**: Sorting the available IDs alongside the merged ranges allows a single pass that advances pointers monotonically. Each ingredient is compared with at most one interval, yielding `O(R log R + I log I + R + I)` overall. This is optimal for the expected scale and trivially parallelizable if needed.
- **Alternatives considered**:
  - **Binary search each ID against merged ranges**: also `O(I log R)` and easy to implement, but two-pointer sweep removes the logarithmic factor on the main loop once both arrays are sorted.
  - **Interval tree or segment tree**: overkill for static, read-once data; adds complexity without runtime benefits at the described scale.

## Decision 3: Stream parsing of the database input without extra allocations

- **Rationale**: Splitting the file on the first blank line and iterating line-by-line avoids building large intermediate strings. Using `Path("day-05/input.txt").read_text().split("\n\n", 1)` is sufficient for AoC-scale files while keeping parsing `O(N)` in input size. Validation ensures empty sections are handled gracefully.
- **Alternatives considered**:
  - **Regex-based parsing**: unnecessary overhead and harder to maintain.
  - **Multiple file passes**: complicates flow and offers no benefit because the file is tiny.
