# Phase 0 Research — Day 7 Part 2

## Research Tasks Executed

- Clarified manifold splitter semantics and how many branches a single `^` produces (2: left and right unless blocked).
- Evaluated counting strategies (DFS with memoization, iterative DP, brute-force path enumeration) for grids with stacked splitters.
- Identified validation requirements for malformed diagrams (missing `S`, illegal glyphs, disconnected grids).
- Captured performance expectations and stress-case dimensions from AoC constraints (hundreds of rows/columns max).

## Decision 1: Model the manifold as a sparse grid with semantic cell types

- **Decision**: Parse the ASCII diagram into a dictionary keyed by `(row, col)` that tracks cell type (`start`, `splitter`, `empty`, `blocked`).
- **Rationale**: Sparse dict keeps lookups O(1) and avoids repeatedly slicing strings. It also aligns with memoization because we can key caches by coordinates without carrying string context.
- **Alternatives considered**: (a) Keep raw string list and inspect neighbors on the fly — simpler but scatters parsing logic across traversal; (b) Convert into an explicit graph upfront — unnecessary overhead because the splitter branching is deterministic and only requires local neighbor checks.

## Decision 2: Use memoized DFS/DP to count downstream timelines per coordinate

- **Decision**: Perform a depth-first traversal starting at `S`, with memoization on `(row, col)` returning the total timelines reachable from that cell.
- **Rationale**: Prevents exponential recomputation when stacked splitters create overlapping substructures. With memoization, complexity is O(number_of_cells) because each cell's count is computed once. Matches user's hint toward DP/memoization and keeps recursion depth manageable (grid height ≤ few hundred).
- **Alternatives considered**: (a) Pure BFS/tree expansion recording every path — explodes combinatorially with many splitters; (b) Bottom-up DP scanning rows from bottom to top — harder to express when splitters redirect diagonally and when diagrams contain irregular gaps.

## Decision 3: Enforce strict input validation before traversal

- **Decision**: Validate unique `S`, allowed characters (`S`, `^`, `.`, whitespace), and ensure at least one row contains `S`. Raise descriptive exceptions consumed by CLI/tests.
- **Rationale**: Keeps solver behavior deterministic and satisfies FR-004/edge-case requirements. Early validation simplifies traversal logic (assumes sanitized grid).
- **Alternatives considered**: (a) Fail silently or return zero timelines — obscures user mistakes; (b) Attempt auto-correction — out of scope and risks misinterpreting puzzles.

## Decision 4: Handling overlapping or adjacent splitters

- **Decision**: Treat each splitter as producing two child coordinates: diagonally left-down and right-down (or whichever rule puzzle defines) and allow children to coincide; memoization naturally collapses overlaps to a single computed count.
- **Rationale**: Maintains correctness when branches reconverge under overlapping columns. DP cache ensures we do not double-count shared downstream nodes.
- **Alternatives considered**: (a) Prevent overlapping child coordinates — contradicts specification that overlapping timelines remain unique; (b) Track full path signatures — unnecessary because convergence should still count unique path prefixes, which DP already distinguishes by originating cell.

## Decision 5: Performance guardrails and recursion safety

- **Decision**: Keep recursion depth under control via iterative stack fallback if grid height exceeds Python's default recursion limit; also cap memoization dictionary growth by pruning unreachable whitespace.
- **Rationale**: AoC grids can approach several hundred rows; default recursion limit (~1000) is safe but documenting fallback prevents surprises. Memory remains linear in number of meaningful cells.
- **Alternatives considered**: (a) Unlimited recursion — risks hitting recursion depth in pathological cases; (b) Converting everything to iterative DP upfront — adds complexity with little benefit unless recursion actually fails.
