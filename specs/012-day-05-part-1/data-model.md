# Data Model — Day 5 Part 1

## Entities

### FreshRange

- **Purpose**: Represents one inclusive interval of fresh ingredient IDs provided in the database header.
- **Fields**:
  - `start` (int, ≥ 0)
  - `end` (int, ≥ start)
- **Derived Data**: `length = end - start + 1` used only for diagnostics.
- **Validation**:
  - Reject inputs where `start > end`; treat as malformed line.
  - Normalize single-value ranges (e.g., `5-5`) into `[5, 5]` intervals.

### RangeUnion

- **Purpose**: Canonical list of merged, non-overlapping `FreshRange` intervals sorted by `start`.
- **Fields**:
  - `intervals` (list[tuple[int, int]]) sorted ascending and pairwise disjoint.
- **Behaviors**:
  - Built once per puzzle input by sorting and merging the raw ranges (`O(R log R)`).
  - Supports `contains(id: int)` either via binary search or sweep pointer.

### IngredientID

- **Purpose**: Records each available ingredient ID from the second block of the database.
- **Fields**:
  - `value` (int, ≥ 0)
  - `status` (enum: `fresh` | `spoiled`) computed lazily by membership check against `RangeUnion`.
- **Validation**: Accepts zeros unless puzzle statement later forbids; negative values trigger explicit rejection per edge-case exploration.

### FreshCountSummary

- **Purpose**: Aggregates final counts for reporting and testing.
- **Fields**:
  - `total_available` (int)
  - `fresh_count` (int)
  - `spoiled_count` (int)
  - `fresh_ids` (list[int], optional debug output for visualization/tests)

## Relationships & Flow

1. Parse each header line into a `FreshRange`.
2. `RangeUnion` consumes all `FreshRange` objects, merges overlaps, and produces sorted intervals.
3. Each `IngredientID` is streamed through the merged intervals to set its `status`.
4. `FreshCountSummary` tallies outcomes for reporting to CLI and tests.

## State Transitions

- `FreshRange` → `RangeUnion` during merge.
- `IngredientID (unknown)` → `IngredientID (fresh/spoiled)` after membership evaluation.
- `FreshCountSummary` accumulates as soon as each ingredient is labeled; no rollback states required.
