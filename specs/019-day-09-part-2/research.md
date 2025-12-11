# Research: Day 9 Part 2 - Optimized Ray Tracing Implementation

**Feature**: Day 9 Part 2 - Largest Red-Green Rectangle  
**Date**: December 11, 2025  
**Purpose**: Resolve technical unknowns and establish implementation patterns

## Research Questions

This research phase resolves the following unknowns from the technical context:

1. How to detect polygon winding direction (clockwise vs counter-clockwise)?
2. How to classify turns as convex vs concave based on direction vectors?
3. How to implement efficient ray casting with edge-only validation?
4. How to optimize ray tracing by filtering edges by coordinate?

## Decision 1: Polygon Winding Detection

### Decision

Use the **Shoelace Formula** (signed area method) to detect polygon winding direction.

### Rationale

The shoelace formula is:

- **Efficient**: O(n) time complexity
- **Robust**: Works for any simple polygon
- **Numerically stable**: Integer arithmetic for axis-aligned edges
- **Standard**: Well-established in computational geometry

### Implementation Pattern

```python
def compute_signed_area(vertices: list[tuple[int, int]]) -> float:
    """Compute signed area using shoelace formula."""
    area = 0.0
    n = len(vertices)

    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]  # Wraparound
        area += x1 * y2 - x2 * y1

    return area / 2.0

def is_clockwise(vertices: list[tuple[int, int]]) -> bool:
    """Check if polygon vertices are ordered clockwise."""
    # For screen coordinates (Y-down), negative area = clockwise
    return compute_signed_area(vertices) < 0
```

### Coordinate System Note

For Advent of Code grids with Y-axis pointing downward (row increases downward):

- **Negative signed area** → Clockwise winding
- **Positive signed area** → Counter-clockwise winding

### Alternatives Considered

- **Angle sum method**: More complex, requires trigonometry
- **Turning angle method**: Requires careful angle normalization

**Rejected because**: Shoelace is simpler and more efficient for axis-aligned polygons.

---

## Decision 2: Convex/Concave Turn Classification

### Decision

Use **2D cross product** of direction vectors to classify turns, interpreted based on polygon winding.

### Rationale

- **Simple**: Single multiplication operation
- **Deterministic**: No floating-point edge cases for axis-aligned edges
- **Winding-aware**: Correctly interprets convex/concave based on traversal direction

### Implementation Pattern

```python
def compute_direction_vector(from_vertex: tuple[int, int],
                            to_vertex: tuple[int, int]) -> tuple[int, int]:
    """Compute unit direction vector between vertices."""
    dx = to_vertex[0] - from_vertex[0]
    dy = to_vertex[1] - from_vertex[1]

    # Normalize to unit vector for axis-aligned edges
    if dx != 0:
        dx = dx // abs(dx)  # +1 or -1
    if dy != 0:
        dy = dy // abs(dy)  # +1 or -1

    return (dx, dy)

def classify_turn(incoming: tuple[int, int],
                  outgoing: tuple[int, int],
                  is_clockwise: bool) -> str:
    """Classify turn as convex or concave."""
    # 2D cross product: incoming × outgoing
    cross = incoming[0] * outgoing[1] - incoming[1] * outgoing[0]

    if is_clockwise:
        # Clockwise: right turn (cross < 0) = convex
        return "convex" if cross < 0 else "concave"
    else:
        # Counterclockwise: left turn (cross > 0) = convex
        return "convex" if cross > 0 else "concave"

def classify_all_vertices(vertices: list[tuple[int, int]]) -> list[dict]:
    """Classify all vertices with wraparound handling."""
    n = len(vertices)
    is_cw = is_clockwise(vertices)

    classifications = []
    for i in range(n):
        prev = vertices[(i - 1) % n]  # Wraparound
        current = vertices[i]
        next_v = vertices[(i + 1) % n]

        incoming = compute_direction_vector(prev, current)
        outgoing = compute_direction_vector(current, next_v)
        turn_type = classify_turn(incoming, outgoing, is_cw)

        classifications.append({
            'vertex': current,
            'incoming': incoming,
            'outgoing': outgoing,
            'classification': turn_type
        })

    return classifications
```

### Key Insight

- **Convex corner** = exterior corner (turns "outward" from interior)
- **Concave corner** = interior corner (turns "inward" toward interior)
- Classification depends on winding: right turn is convex in CW, concave in CCW

### Alternatives Considered

- **J/L/F/7 taxonomy**: Maps to specific turn combinations but adds unnecessary complexity

**Rejected because**: Convex/concave classification captures all necessary geometric information without extra abstraction layers.

---

## Decision 3: Ray Casting with Edge-Only Validation

### Decision

Use **even-odd ray casting** with state toggling and segment generation to validate rectangles by checking only their boundaries.

### Rationale

The puzzle guarantees a simple, hole-free polygon with green interior:

- **Edge checking is sufficient**: If all four rectangle edges stay inside, interior must be inside
- **Efficient**: O(edges_on_coordinate) instead of O(grid_size)
- **Correct**: Jordan curve theorem guarantees inside/outside alternation

### Implementation Pattern

```python
def generate_ray_segments(ray_start: int, ray_end: int,
                         edge_positions: list[int]) -> list[tuple[int, int, str]]:
    """
    Generate segments along a ray based on edge crossings.

    Returns:
        List of (start, end, state) tuples where state is "inside" or "outside"
    """
    if not edge_positions:
        # No crossings = entire ray is inside
        return [(ray_start, ray_end, "inside")]

    segments = []
    state = "inside"  # Start inside (from red tile)
    current_pos = ray_start

    for edge_pos in sorted(edge_positions):
        if edge_pos <= ray_start or edge_pos >= ray_end:
            continue

        # Record segment before crossing
        if current_pos < edge_pos:
            segments.append((current_pos, edge_pos, state))

        # Toggle state at crossing
        state = "outside" if state == "inside" else "inside"
        current_pos = edge_pos

    # Final segment to ray end
    if current_pos < ray_end:
        segments.append((current_pos, ray_end, state))

    # Filter zero-width outside segments
    return filter_zero_width_segments(segments)

def filter_zero_width_segments(segments: list[tuple]) -> list[tuple]:
    """Remove zero-width 'outside' segments from consecutive crossings."""
    filtered = []
    for start, end, state in segments:
        if state == "outside" and start == end:
            continue  # Skip zero-width outside segments
        filtered.append((start, end, state))
    return filtered

def validate_rectangle_edge(edge_start: int, edge_end: int,
                            segments: list[tuple[int, int, str]]) -> bool:
    """
    Check if rectangle edge overlaps any 'outside' segment.

    Returns:
        True if edge is entirely inside, False if any part is outside
    """
    for seg_start, seg_end, state in segments:
        if state == "outside":
            # Check for overlap
            if not (edge_end <= seg_start or edge_start >= seg_end):
                return False  # Edge overlaps outside segment
    return True
```

### Initial Ray State Determination

```python
def determine_initial_state(corner: tuple[int, int],
                           ray_direction: tuple[int, int],
                           perpendicular_edges: list[int]) -> str:
    """
    Determine if ray starts inside or outside based on first step.

    Check if the half-open interval starting one unit away from corner
    immediately crosses a perpendicular boundary.
    """
    # First position along ray
    first_pos = corner[0] + ray_direction[0], corner[1] + ray_direction[1]

    # Check if this position crosses a perpendicular edge
    for edge in perpendicular_edges:
        if edge == first_pos[0] or edge == first_pos[1]:
            return "outside"  # Immediately crosses boundary

    return "inside"  # Interior to polygon
```

### Edge-Only Validation Justification

Given the puzzle's simple-polygon guarantee:

1. **Jordan curve theorem**: Every scan line crosses boundary an even number of times
2. **Interior fill guarantee**: All tiles strictly inside the loop are green
3. **Concavity handling**: Pockets pierce at least one rectangle edge
4. **Result**: Validating edges is sufficient; interior propagates inward

### Alternatives Considered

- **Full grid scan**: Check every tile in rectangle interior

**Rejected because**: O(width × height) is prohibitively expensive for large rectangles; edge-only validation leverages the fill guarantee.

---

## Decision 4: Coordinate Filtering Optimization

### Decision

Precompute edges into horizontal/vertical sets indexed by coordinate (x or y).

### Rationale

- **Dramatic speedup**: O(K) instead of O(E) per ray, where K << E
- **Memory efficient**: Two dictionaries with coordinate keys
- **Simple to implement**: Standard Python dict with list values

### Implementation Pattern

```python
class EdgeIndex:
    """Precomputed edge index for efficient ray casting."""

    def __init__(self, vertices: list[tuple[int, int]]):
        self.horizontal_edges = {}  # y -> list of x positions
        self.vertical_edges = {}    # x -> list of y positions
        self._build_index(vertices)

    def _build_index(self, vertices: list[tuple[int, int]]):
        """Build coordinate-indexed edge sets."""
        n = len(vertices)

        for i in range(n):
            v1 = vertices[i]
            v2 = vertices[(i + 1) % n]

            if v1[1] == v2[1]:  # Horizontal edge
                y = v1[1]
                x_min, x_max = min(v1[0], v2[0]), max(v1[0], v2[0])
                if y not in self.horizontal_edges:
                    self.horizontal_edges[y] = []
                self.horizontal_edges[y].extend(range(x_min + 1, x_max + 1))

            elif v1[0] == v2[0]:  # Vertical edge
                x = v1[0]
                y_min, y_max = min(v1[1], v2[1]), max(v1[1], v2[1])
                if x not in self.vertical_edges:
                    self.vertical_edges[x] = []
                self.vertical_edges[x].extend(range(y_min + 1, y_max + 1))

    def get_horizontal_edges_at_y(self, y: int) -> list[int]:
        """Get all horizontal edge x-positions at given y."""
        return self.horizontal_edges.get(y, [])

    def get_vertical_edges_at_x(self, x: int) -> list[int]:
        """Get all vertical edge y-positions at given x."""
        return self.vertical_edges.get(x, [])
```

### Performance Analysis

For a grid with 1000 edges:

- **Naive approach**: O(1000) edge checks per ray × 4 rays = 4000 checks
- **Coordinate filtering**: O(10) edges per coordinate × 4 rays = 40 checks
- **Speedup**: ~100× for typical Advent of Code inputs

### Corner Inclusion Strategy

Include corners in filtered sets based on their perpendicular edges:

- **Convex corners**: Always included (represent real boundaries)
- **Concave corners**: Included only when approached from blocking side

### Alternatives Considered

- **Spatial grid**: 2D grid with occupancy map
- **Quad-tree**: Hierarchical spatial structure

**Rejected because**: Simple coordinate dictionaries provide sufficient performance for Advent of Code scale (~10³ edges) without complexity overhead.

---

## Technology Stack Summary

### Core Technologies

- **Python 3.10+**: Standard library only (itertools, pathlib)
- **pytest**: Testing framework (already in pyproject.toml)
- **Data structures**: Sets for edges, lists for vertices, dicts for indexing

### Performance Characteristics

- **Parsing**: O(n) where n = number of red tiles
- **Edge precomputation**: O(n) to build index
- **Rectangle enumeration**: O(n²) pairs of red tiles
- **Per-rectangle validation**: O(K) where K = edges per coordinate (typically << n)
- **Total complexity**: O(n² × K) which is tractable for n < 1000

### Memory Usage

- **Edge sets**: O(E) where E = total green edge tiles
- **Indexed lookups**: O(E) additional for dictionaries
- **Total**: O(E) which is acceptable for problem constraints

---

## Best Practices Applied

### From Constitution

- **Clean Python**: Use type hints, PEP8 style, descriptive names
- **Function-based**: Separate functions for parsing, classification, ray casting, validation
- **TDD-ready**: Each component is independently testable
- **Docstrings**: All functions documented with examples

### From Research

- **Geometric robustness**: Integer arithmetic for axis-aligned edges
- **Edge case handling**: Wraparound, zero-width segments, degenerate cases
- **Performance-conscious**: Coordinate filtering, precomputation
- **Clear abstractions**: EdgeIndex class, segment tuples, classification dicts

---

## Implementation Checklist

- [x] Winding detection algorithm (shoelace formula)
- [x] Turn classification logic (cross product)
- [x] Ray casting with state toggling
- [x] Segment generation and filtering
- [x] Edge-only rectangle validation
- [x] Coordinate filtering optimization
- [x] Initial ray state determination
- [x] Zero-width segment handling
- [ ] Integration into solution_part2.py (Phase 1)
- [ ] Comprehensive test coverage (Phase 1)

---

## References

- Shoelace Formula: Standard computational geometry algorithm for polygon area
- Jordan Curve Theorem: Mathematical basis for ray casting
- 2D Cross Product: Vector operation for turn direction
- Even-Odd Rule: Point-in-polygon test using ray intersections

---

**Status**: ✅ Research Complete  
**Next Phase**: Phase 1 - Generate data model, contracts, and quickstart
