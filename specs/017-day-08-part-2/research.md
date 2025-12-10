# Research: AoC Day 8 Part 2 - Complete Circuit Formation

**Date**: December 10, 2025  
**Feature**: 017-day-08-part-2  
**Phase**: 0 (Research & Decision Making)

## Research Questions

### 1. Algorithm Choice: Dictionary-Based vs Classic Union-Find

**Decision**: Use **Classic Union-Find** with path compression and union-by-rank

**Rationale**:

**Part 2 changes the game completely**. Unlike Part 1 (connect exactly N pairs), Part 2 requires:

- Processing pairs until ALL boxes form ONE circuit
- Checking "are these in same circuit?" for potentially hundreds of thousands of pairs
- With N=1000 boxes, we have ~500k total pairs to check

**Performance comparison**:

| Operation               | Dictionary Approach (Part 1) | Classic Union-Find                   |
| ----------------------- | ---------------------------- | ------------------------------------ |
| Find circuit membership | O(C) scan of all circuits    | O(α(N)) ≈ O(1) with path compression |
| Merge two circuits      | O(\|smaller circuit\|)       | O(1) with union-by-rank              |
| Check if connected      | O(C) × 2 (find both)         | O(α(N)) × 2 ≈ O(1)                   |

**Where C = number of circuits, N = number of boxes, α(N) = inverse Ackermann (≈ 4 for practical N)**

**Concrete example (N=1000 boxes)**:

- Total pairwise distances: ~500,000 pairs
- Actual connections needed: 999 (to unite 1000 boxes)
- **Rejected pairs**: ~499,000 pairs (already in same circuit)

**Dictionary approach cost**:

```
For each of ~500k pairs:
  find_circuit(a): scan all circuits (starts at 1000, decreases)
  find_circuit(b): scan all circuits
  Average circuits to scan: ~500
  Total operations: 500k × 500 × 2 = 500 million operations
```

**Union-Find cost**:

```
For each of ~500k pairs:
  find(a): ~4 array lookups with path compression
  find(b): ~4 array lookups
  Total operations: 500k × 8 = 4 million operations
```

**Performance ratio: ~125x faster with Union-Find**

**The user's skepticism is CORRECT**: hundreds of thousands of membership checks make the dictionary approach's O(C) scan prohibitively slow. Union-Find's O(α(N)) ≈ O(1) lookup is critical for Part 2.

**Alternatives Considered**:

- **Optimize dictionary with reverse lookup**: Maintain `point_id -> circuit_name` dict. Pros: O(1) find. Cons: still O(|circuit|) merge cost; added complexity maintaining bidirectional mapping.

  - **Verdict**: This is essentially reinventing Union-Find poorly. Classic UF is cleaner and faster.

- **NetworkX connected_components**: Pros: battle-tested. Cons: external dependency violates Constitution; overkill for this problem.

- **Stick with dictionary approach from Part 1**: Pros: code reuse. Cons: **125x slower**; unacceptable for competition where runtime matters.

**Implementation Strategy**:

Use classic Union-Find with two optimizations:

1. **Path compression**: During `find()`, flatten tree by pointing all nodes directly to root
2. **Union-by-rank**: Merge smaller tree under larger tree to keep depth minimal

```python
class UnionFind:
    """Union-Find data structure with path compression and union-by-rank."""

    def __init__(self, n: int):
        """Initialize n disjoint sets (each element is its own parent)."""
        self.parent = list(range(n))  # parent[i] = i initially
        self.rank = [0] * n           # tree depth estimate
        self.num_components = n       # track circuit count

    def find(self, x: int) -> int:
        """Find root of x's set with path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Compress path
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """Unite sets containing x and y. Returns True if merged, False if already connected."""
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False  # Already in same set

        # Union-by-rank: attach smaller tree under larger
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1

        self.num_components -= 1
        return True  # Successful merge

    def is_fully_connected(self) -> bool:
        """Check if all elements are in one component."""
        return self.num_components == 1
```

---

### 2. Stopping Condition & Final Connection Detection

**Decision**: Track `num_components` and detect transition from 2→1

**Rationale**:

We need to identify the **exact pair** whose connection unifies the final two circuits.

**Algorithm**:

```python
for distance, point_a, point_b in sorted_distances:
    if uf.num_components == 2:
        # Next successful merge will be the final connection
        root_a = uf.find(point_a)
        root_b = uf.find(point_b)
        if root_a != root_b:
            # This is the final connection!
            return points[point_a][0] * points[point_b][0]  # product of X coords

    uf.union(point_a, point_b)  # Returns True if merged, False if already connected
```

**Why track num_components instead of checking after each union**:

- `num_components` decrements atomically during `union()`
- Checking `== 1` after each connection is cleaner than re-scanning the structure
- Allows early exit the moment we detect the final connection

**Edge case**: What if input is already fully connected?

- `num_components` starts at N, never reaches 1 through connections
- Solution: check `uf.is_fully_connected()` before starting
- Return special message if already unified (though spec implies this won't happen)

---

### 3. Distance Calculation & Sorting Strategy

**Decision**: Reuse Part 1 approach with minor modification

**Rationale**:

Part 1's `compute_all_distances()` is already optimal:

- Pre-compute all O(N²) distances once
- Sort by distance: O(N² log N)
- For N=1000: ~500k pairs, ~10M comparisons in sort → milliseconds

**No changes needed** - the sorting strategy handles Part 2's requirement to process in distance order.

**Implementation**: Direct reuse from Part 1

```python
def compute_all_distances(points: list[JunctionBox]) -> list[DistancePair]:
    """Compute all pairwise distances and return sorted list."""
    distances = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            dist = euclidean_distance(points[i], points[j])
            distances.append((dist, i, j))
    distances.sort()  # Sort by distance (first tuple element)
    return distances
```

---

### 4. Input Parsing & Coordinate Handling

**Decision**: Reuse Part 1 parsing verbatim

**Rationale**:

Part 1's `parse_input()` already handles:

- Line-by-line parsing of "X,Y,Z" format
- Auto-increment IDs (list index = junction box ID)
- Whitespace handling

**No changes needed** - Part 2 uses identical input format.

---

### 5. Answer Calculation

**Decision**: Return product of X coordinates of the final connecting pair

**Rationale**:

Spec requirement: "product of the X coordinates of the two junction boxes involved in the final connection"

**Implementation**:

```python
def solve_part2(input_data: str) -> int:
    """Solve Part 2: Find connection that completes circuit unification.

    Returns:
        Product of X coordinates of final connecting pair
    """
    points = parse_input(input_data)
    distances = compute_all_distances(points)
    uf = UnionFind(len(points))

    for distance, point_a, point_b in distances:
        # Check if this connection will complete unification
        if uf.num_components == 2 and uf.find(point_a) != uf.find(point_b):
            # This is the final connection!
            x_a = points[point_a][0]
            x_b = points[point_b][0]
            return x_a * x_b

        uf.union(point_a, point_b)

    # Should never reach here if input guarantees full connectivity
    raise ValueError("No connection unified all circuits")
```

**Example validation**:

- Final connection: boxes at (216,146,977) and (117,168,530)
- Product: 216 × 117 = 25272 ✓

---

## Summary of Decisions

| Aspect        | Decision                                                 | Key Benefit                             |
| ------------- | -------------------------------------------------------- | --------------------------------------- |
| **Algorithm** | Classic Union-Find with path compression & union-by-rank | 125x faster for ~500k membership checks |
| **Stopping**  | Track `num_components`, detect 2→1 transition            | Early exit at final connection          |
| **Distance**  | Reuse Part 1 pre-computation & sorting                   | No changes needed, already optimal      |
| **Parsing**   | Reuse Part 1 parser                                      | Identical input format                  |
| **Answer**    | Product of X coords at final merge                       | Direct spec requirement                 |

## Complexity Analysis

| Operation             | Count      | Per-Op Cost    | Total           |
| --------------------- | ---------- | -------------- | --------------- |
| Parse input           | N lines    | O(1)           | O(N)            |
| Compute distances     | N(N-1)/2   | O(1)           | O(N²)           |
| Sort distances        | 1          | O(N² log N)    | O(N² log N)     |
| Union-Find operations | ~N² checks | O(α(N)) ≈ O(1) | O(N²)           |
| **Overall**           |            |                | **O(N² log N)** |

For N=1000: ~10 million operations, well under 1 second.

**Dictionary approach would be**: O(N² × N) = O(N³) ≈ 1 billion operations → unacceptable.

## Open Questions

**None** - All technical decisions resolved.

## Acknowledgment

User's skepticism about dictionary approach scaling to "hundreds of thousands of merges" was **absolutely correct**. The find_circuit() scan becomes the bottleneck in Part 2. Classic Union-Find is the right choice here.

## Next Steps

Proceed to **Phase 1**:

1. Generate `data-model.md` (Union-Find structure, junction boxes)
2. Generate `quickstart.md` (developer workflow, testing strategy)
3. Update agent context
