# Data Model: AoC Day 8 Part 2 - Complete Circuit Formation

**Feature**: 017-day-08-part-2  
**Date**: December 10, 2025  
**Phase**: 1 (Design)

## Core Entities

### 1. JunctionBox

**Description**: A point in 3D space representing a junction box location

**Type Alias**:

```python
JunctionBox = tuple[int, int, int]  # (x, y, z) coordinates
```

**Fields**:

- `x: int` — X coordinate in 3D space
- `y: int` — Y coordinate in 3D space
- `z: int` — Z coordinate in 3D space

**Validation Rules**:

- All coordinates must be integers
- No explicit range constraints (coordinates can be negative or very large)

**State Transitions**: N/A (immutable coordinate tuple)

**Relationships**:

- Indexed by position in input file (index = junction box ID)
- Participates in pairwise distance calculations with all other junction boxes
- Member of exactly one circuit (tracked by UnionFind)

---

### 2. UnionFind

**Description**: Data structure tracking circuit membership and enabling efficient connectivity queries

**Class Definition**:

```python
class UnionFind:
    """Union-Find with path compression and union-by-rank for circuit tracking."""

    parent: list[int]        # parent[i] = parent of element i (root if parent[i] == i)
    rank: list[int]          # rank[i] = approximate tree depth for union-by-rank
    num_components: int      # count of disjoint circuits
```

**Fields**:

- `parent: list[int]` — Parent pointers for each junction box (index = box ID, value = parent ID)
  - Root nodes: `parent[i] == i`
  - Non-root nodes: `parent[i]` points to parent in tree
- `rank: list[int]` — Tree depth estimate for union-by-rank optimization
  - Used to attach smaller trees under larger trees
  - Only meaningful for root nodes
- `num_components: int` — Current count of disjoint circuits
  - Starts at N (all boxes separate)
  - Decrements by 1 on each successful union
  - Goal: reach 1 (all boxes united)

**Validation Rules**:

- `parent` and `rank` must have length N (number of junction boxes)
- `num_components` must be in range [1, N]
- All `parent[i]` values must be valid indices in range [0, N-1]

**State Transitions**:

```
Initial state: N disjoint sets
  parent = [0, 1, 2, ..., N-1]  # Each box is its own parent
  rank = [0, 0, 0, ..., 0]       # All trees depth 0
  num_components = N

After union(a, b) where a and b in different sets:
  parent[root_smaller] = root_larger  # Smaller tree attached to larger
  num_components -= 1                 # One fewer circuit

After union(a, b) where a and b in same set:
  No changes (already connected)

Terminal state: 1 unified circuit
  num_components = 1
  All boxes share common root
```

**Operations**:

1. **`find(x: int) -> int`**

   - Returns root of set containing x
   - Side effect: path compression (flattens tree)
   - Complexity: O(α(N)) ≈ O(1) with path compression

2. **`union(x: int, y: int) -> bool`**

   - Merges sets containing x and y
   - Returns True if merged, False if already in same set
   - Side effect: decrements `num_components` on successful merge
   - Complexity: O(α(N)) ≈ O(1)

3. **`is_fully_connected() -> bool`**
   - Returns True if all boxes in one circuit
   - Implementation: `return self.num_components == 1`
   - Complexity: O(1)

**Relationships**:

- Tracks circuit membership for all junction boxes
- Index correspondence: `UnionFind.parent[i]` corresponds to junction box at `points[i]`

---

### 3. DistancePair

**Description**: Pre-computed distance between two junction boxes with their IDs

**Type Alias**:

```python
DistancePair = tuple[float, int, int]  # (distance, id_a, id_b)
```

**Fields**:

- `distance: float` — Euclidean distance between the two boxes
- `id_a: int` — Index of first junction box (always < id_b)
- `id_b: int` — Index of second junction box (always > id_a)

**Validation Rules**:

- `distance >= 0.0` (distance cannot be negative)
- `id_a < id_b` (canonical ordering prevents duplicates)
- Both IDs must be valid indices in junction box list

**State Transitions**: N/A (immutable tuple, computed once and sorted)

**Relationships**:

- Created for all N(N-1)/2 pairs of junction boxes
- Sorted by distance (ascending) for processing order
- Used to drive connection algorithm

---

### 4. Connection (Implicit)

**Description**: A connection between two junction boxes (represented by union operation)

**Representation**: Not explicitly stored; tracked implicitly through UnionFind state

**Properties**:

- Connects two junction boxes that were in different circuits
- Processed in order of increasing distance
- Causes circuit merge (two circuits become one)

**The Final Connection**:

- Special connection that transitions `num_components` from 2 to 1
- This connection's junction box pair determines the answer
- Answer: `points[id_a].x * points[id_b].x`

---

## Data Flow

```
Input File (text)
  ↓
parse_input()
  ↓
List[JunctionBox]  (points[0], points[1], ..., points[N-1])
  ↓
compute_all_distances()
  ↓
List[DistancePair]  (sorted by distance)
  ↓
UnionFind initialization (N disjoint sets)
  ↓
Process distances in order:
  For each (distance, id_a, id_b):
    - Check if num_components == 2
    - Check if id_a and id_b in different sets (find(a) != find(b))
    - If both true → this is the FINAL CONNECTION
      → Return points[id_a].x * points[id_b].x
    - Otherwise: union(id_a, id_b)
  ↓
Answer (int): Product of X coordinates
```

---

## Algorithm Invariants

**Invariant 1**: At any point during processing, every junction box belongs to exactly one circuit (represented by a root in UnionFind).

**Invariant 2**: `num_components` equals the number of disjoint circuits after all unions processed so far.

**Invariant 3**: Distance pairs are processed in strictly ascending order (enforced by pre-sorting).

**Invariant 4**: Once `num_components` reaches 1, no further processing is needed (early exit condition).

**Invariant 5**: The final connection occurs when `num_components == 2` and we attempt to union boxes from different sets.

---

## Example State Progression

**Example Input**: 20 junction boxes

**Initial State**:

```
num_components = 20
parent = [0, 1, 2, ..., 19]  # All separate
```

**After processing first connection** (shortest distance pair):

```
num_components = 19
parent[smaller_id] now points to larger_id root
```

**After many connections**:

```
num_components = 2
Two remaining circuits, each with multiple boxes
```

**Final connection** (e.g., boxes 5 and 12):

```
num_components transitions 2 → 1
find(5) ≠ find(12) → union(5, 12)
Answer: points[5].x * points[12].x
```

**For example**:

- Box 5: (216, 146, 977)
- Box 12: (117, 168, 530)
- Answer: 216 × 117 = 25272 ✓

---

## Type Summary

```python
# Type aliases (imported from Part 1 where applicable)
JunctionBox = tuple[int, int, int]
DistancePair = tuple[float, int, int]

# New class for Part 2
class UnionFind:
    parent: list[int]
    rank: list[int]
    num_components: int

    def __init__(self, n: int) -> None: ...
    def find(self, x: int) -> int: ...
    def union(self, x: int, y: int) -> bool: ...
    def is_fully_connected(self) -> bool: ...

# Main function signature
def solve_part2(input_data: str) -> int: ...
```

---

## Memory Complexity

For N junction boxes:

- **Junction boxes**: O(N) storage
- **Distance pairs**: O(N²) storage (~500k pairs for N=1000)
- **UnionFind**:
  - `parent`: O(N)
  - `rank`: O(N)
  - Total UnionFind: O(N)

**Total**: O(N²) dominated by distance pair storage

For N=1000:

- Points: ~32 bytes × 1000 = 32 KB
- Distances: ~32 bytes × 500k = 16 MB
- UnionFind: ~16 bytes × 1000 = 16 KB

**Total: ~16 MB** — well within acceptable limits
