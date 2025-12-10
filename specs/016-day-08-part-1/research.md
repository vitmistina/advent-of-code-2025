# Research: AoC Day 8 Part 1 - Circuit Analysis Algorithm

**Date**: December 10, 2025  
**Feature**: 016-day-08-part-1  
**Phase**: 0 (Research & Decision Making)

## Research Questions

### 1. Union-Find vs Dictionary-Based Grouping

**Decision**: Use dictionary-based grouping with named sets (as suggested by user)

**Rationale**:

- **User's approach is simpler for this problem**: The user suggested assigning IDs to points, maintaining sets in a dictionary, and merging sets based on distance order. This is conceptually clearer than classic Union-Find for someone reading the code.
- **Classic Union-Find advantages not critical here**: Union-Find with path compression and union-by-rank is optimal for repeated "are these connected?" queries. However, we only need final circuit sizes, not repeated connectivity checks.
- **Dictionary approach is more Pythonic**: Using a dict with string keys ("circuit_1", "circuit_2") and set values is idiomatic Python and easier to debug/visualize.
- **Performance is acceptable**: With ~1000 junction boxes, we compute ~500k distances once, sort them, and process 1000 connections. The difference between O(α(n)) Union-Find operations and O(1) set operations on small sets is negligible.

**Alternatives Considered**:

- **Classic Union-Find with parent array**: More traditional competitive programming approach. Pros: theoretically optimal for connectivity queries; well-documented. Cons: Less readable; overkill for one-time circuit size calculation; requires separate circuit size computation at the end.
- **NetworkX graph library**: Could use nx.connected_components() after adding edges. Pros: battle-tested, handles connectivity automatically. Cons: external dependency violates Constitution (standard library only); heavier weight than needed.

**Implementation Details**:

```python
# Pseudo-code for dictionary-based grouping
circuits = {}  # key: circuit_name, value: set of point IDs
next_circuit_id = 0

for distance, point_a, point_b in sorted_distances[:num_connections]:
    circuit_a = find_circuit(point_a, circuits)
    circuit_b = find_circuit(point_b, circuits)

    if circuit_a is None and circuit_b is None:
        # Both unassigned: create new circuit
        circuits[f"circuit_{next_circuit_id}"] = {point_a, point_b}
        next_circuit_id += 1
    elif circuit_a is not None and circuit_b is None:
        # Point B joins circuit A
        circuits[circuit_a].add(point_b)
    elif circuit_a is None and circuit_b is not None:
        # Point A joins circuit B
        circuits[circuit_b].add(point_a)
    elif circuit_a != circuit_b:
        # Merge two circuits
        circuits[circuit_a].update(circuits[circuit_b])
        del circuits[circuit_b]
    # else: both in same circuit, skip
```

---

### 2. Distance Calculation Precision

**Decision**: Use standard floating-point arithmetic with Python's `math.sqrt`

**Rationale**:

- **Euclidean distance formula**: `sqrt((x2-x1)^2 + (y2-y1)^2 + (z2-z1)^2)`
- **Float64 precision is sufficient**: Coordinates are integers (based on example); distance precision to ~15 decimal places is more than enough for sorting.
- **No need for integer-only distance**: Some competitive programming solutions avoid sqrt by comparing squared distances. Not necessary here since we need to sort all distances anyway.
- **Tie-breaking**: If two pairs have identical distances (unlikely with 3D coordinates but possible), sort by point IDs to ensure deterministic ordering.

**Alternatives Considered**:

- **Squared distances only**: Avoid sqrt entirely, compare squared values. Pros: faster, no floating-point. Cons: less intuitive; spec mentions "Euclidean distance" explicitly; marginal performance gain not worth reduced clarity.
- **Decimal type for precision**: Pros: exact arithmetic. Cons: overkill for integer coordinates; much slower; standard library only requirement favors built-in float.

**Implementation Details**:

```python
import math

def euclidean_distance(point_a, point_b):
    """Calculate Euclidean distance between two 3D points."""
    dx = point_b[0] - point_a[0]
    dy = point_b[1] - point_a[1]
    dz = point_b[2] - point_a[2]
    return math.sqrt(dx*dx + dy*dy + dz*dz)
```

---

### 3. Pairwise Distance Storage Strategy

**Decision**: Pre-compute all distances, store as list of tuples, sort once

**Rationale**:

- **Space complexity**: With N junction boxes, we have N\*(N-1)/2 pairs. For N=1000, that's ~500k pairs. Each tuple (distance, id_a, id_b) is ~32 bytes → ~16 MB total. Acceptable.
- **Time complexity**: O(N²) to compute all distances, O(N² log N) to sort. For N=1000, this is ~500k operations, well under 1 second.
- **Simplifies connection logic**: Once sorted, we iterate through the list and pick the first N pairs that don't violate "already connected" constraint.
- **Alternative (heap-based streaming)**: Could use a min-heap to avoid storing all distances at once. Pros: O(N² log K) space where K is connections made. Cons: more complex; space saving not needed for N=1000.

**Alternatives Considered**:

- **Compute distances on-demand**: Only calculate when needed. Pros: lower memory. Cons: requires priority queue or repeated scans; much slower for N=1000.
- **Distance matrix (N×N array)**: Pros: fast lookup by index. Cons: wastes space (symmetric matrix, diagonal is zero); harder to sort all pairs.

**Implementation Details**:

```python
def compute_all_distances(points):
    """Compute all pairwise distances and return sorted list."""
    distances = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            dist = euclidean_distance(points[i], points[j])
            distances.append((dist, i, j))
    distances.sort()  # Sort by distance (first element of tuple)
    return distances
```

---

### 4. Example vs Full Input Parameterization

**Decision**: Pass `num_connections` as parameter to `solve_part1(input_data, num_connections=1000)`

**Rationale**:

- **Example uses 10 connections**: Test input should verify behavior with 10 connections → circuits [5, 4, 2, 2, 1, 1, 1, 1, 1, 1, 1].
- **Full input uses 1000 connections**: Actual puzzle requires 1000.
- **Parameterization enables testing**: By making num_connections configurable, we can test the example (10) and run the full solution (1000) with the same code.
- **Default to 1000**: The main puzzle answer uses 1000, so that should be the default.

**Alternatives Considered**:

- **Hardcode 1000**: Simpler but breaks example testing.
- **Auto-detect from input size**: Fragile; input size doesn't determine connection count (spec says "up to 1000 connections").

**Implementation Details**:

```python
def solve_part1(input_data: str, num_connections: int = 1000) -> int:
    """Solve Day 8 Part 1: Circuit Analysis.

    Args:
        input_data: Newline-separated list of X,Y,Z coordinates
        num_connections: Number of closest pairs to connect (default 1000)

    Returns:
        Product of three largest circuit sizes
    """
    # Implementation here
    pass
```

---

### 5. Parsing Strategy

**Decision**: Simple line-by-line parsing with `str.split(',')`

**Rationale**:

- **Input format is simple**: Each line is "X,Y,Z" with integer coordinates.
- **Standard library only**: No need for CSV module or regex.
- **Robust error handling**: Strip whitespace, validate three values per line.

**Implementation Details**:

```python
def parse_input(input_data: str):
    """Parse input into list of (x, y, z) tuples with auto-increment IDs.

    Returns:
        List of (x, y, z) tuples indexed by position (ID = index)
    """
    points = []
    for line in input_data.strip().split('\n'):
        x, y, z = map(int, line.split(','))
        points.append((x, y, z))
    return points
```

---

## Summary of Decisions

| Aspect               | Decision                             | Key Benefit                       |
| -------------------- | ------------------------------------ | --------------------------------- |
| **Data Structure**   | Dictionary with named sets           | Pythonic, readable, easy to debug |
| **Distance Calc**    | `math.sqrt` with float64             | Simple, accurate, built-in        |
| **Storage**          | Pre-compute all distances, sort once | Fast for N=1000, simple iteration |
| **Parameterization** | `num_connections` parameter          | Enables example testing           |
| **Parsing**          | Line-by-line split on comma          | Simple, robust, no dependencies   |

## Open Questions

**None** - All technical decisions resolved.

## Next Steps

Proceed to **Phase 1**:

1. Generate `data-model.md` (entity definitions)
2. Generate `contracts/` (if needed - likely N/A for this feature)
3. Generate `quickstart.md` (developer workflow)
4. Update agent context
