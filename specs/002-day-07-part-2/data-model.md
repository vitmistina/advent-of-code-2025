# Data Model — Day 7 Part 2 (Quantum Tachyon Manifold Timelines)

## Overview

Day 7 Part 2 extends the Part 1 solver to count the number of distinct timelines produced when a tachyon traverses a manifold diagram containing splitters. The solver is pure Python and operates on ASCII diagrams. The data model focuses on:

- Parsing and validating diagram inputs
- Representing meaningful cells (start, splitters, empty space)
- Capturing traversal state for memoized DP counting
- Surfacing deterministic results and validation errors for the CLI/tests

## Entities

### `ManifoldDiagram`

| Field           | Type              | Description                                                |
| --------------- | ----------------- | ---------------------------------------------------------- |
| `rows`          | `list[str]`       | Raw input lines stripped of trailing whitespace            |
| `height`        | `int`             | Number of meaningful rows                                  |
| `width`         | `int`             | Max row length after padding                               |
| `start`         | `Coordinate`      | `(row, col)` where `S` is located                          |
| `splitters`     | `set[Coordinate]` | Positions containing `^`                                   |
| `walkable`      | `set[Coordinate]` | Cells that can carry the particle (start, splitters, dots) |
| `allowed_chars` | `set[str]`        | `{"S", "^", ".", " "}` for validation                      |

**Relationships**: Owns many `Cell` records (implicit via `walkable` set). Provides accessors to fetch neighbors and bounds for traversal.

**Validation Rules**:

- Exactly one `S` present (FR-004, Edge Cases)
- All characters in `allowed_chars`
- Diagram must contain at least one row with non-whitespace content
- Each splitter must have at least one row below it (otherwise contributes zero timelines)

### `Cell`

| Field   | Type                                    | Description               |
| ------- | --------------------------------------- | ------------------------- |
| `coord` | `Coordinate`                            | `(row, col)` zero-indexed |
| `kind`  | `Literal["start", "splitter", "empty"]` | Semantic role             |

**Relationships**: Derived from `ManifoldDiagram`; looked up via `(row, col)`.

### `Coordinate`

| Component | Type  | Notes                |
| --------- | ----- | -------------------- |
| `row`     | `int` | 0 at top of diagram  |
| `col`     | `int` | 0 at left of diagram |

Used as dictionary/set keys for memoization and adjacency checks.

### `TimelineComputation`

| Field           | Type                    | Description                                          |
| --------------- | ----------------------- | ---------------------------------------------------- |
| `diagram`       | `ManifoldDiagram`       | Reference to parsed diagram                          |
| `memo`          | `dict[Coordinate, int]` | Cache of downstream timeline counts per cell         |
| `stack`         | `list[Coordinate]`      | Optional iterative traversal stack for deep diagrams |
| `max_depth_hit` | `bool`                  | Flag to detect recursion depth risk                  |

**Responsibilities**:

- Provide `count_timelines()` entry point used by CLI/tests
- Expose instrumentation for debugging/visualization (counts per cell)

### `TimelineResult`

| Field            | Type                    | Description                            |
| ---------------- | ----------------------- | -------------------------------------- |
| `timeline_count` | `int`                   | Total distinct timelines from `S`      |
| `path_counts`    | `dict[Coordinate, int]` | Optional map for visualization/testing |
| `duration_ms`    | `float`                 | Execution time for SC-001 verification |

### `ValidationError`

| Field      | Type                                                                           | Description             |
| ---------- | ------------------------------------------------------------------------------ | ----------------------- | ------------------------ |
| `code`     | `Literal["missing_start", "duplicate_start", "invalid_char", "empty_diagram"]` | Error classification    |
| `message`  | `str`                                                                          | User-facing description |
| `location` | `Coordinate                                                                    | None`                   | Where the issue occurred |

## Relationships Overview

- `TimelineComputation` **has one** `ManifoldDiagram`
- `ManifoldDiagram` **contains many** logical `Cell`s referenced via coordinates
- `TimelineResult` **belongs to** `TimelineComputation`
- `ValidationError` can be attached to CLI outputs or raised as exceptions consumed by tests

## State Transitions / Traversal Logic

1. **Parsing**: Raw diagram -> `ManifoldDiagram`
2. **Validation**: Enforce rules above; raise `ValidationError` on failure
3. **Traversal**:
   - Start at `start` coordinate
   - When encountering a splitter, spawn two branches: diagonal left/down and diagonal right/down (clamped to diagram bounds)
   - Memoize the count returned by each child coordinate; terminal cells with no outbound moves return `1`
4. **Aggregation**: `TimelineResult.timeline_count` = memoized value at `start`
5. **Reporting**: CLI/test harness prints the integer and optionally debugging info

## Derived/Computed Data

- `children(coord)` helper calculates reachable neighbors respecting edges and whitespace
- `is_terminal(coord)` returns `True` if no children -> contributes `1`
- `normalized_rows` may pad lines to `width` for consistent indexing

## Open Questions

None — Phase 0 research resolved prior unknowns. Further clarifications would come from additional puzzle examples if spec expands.
