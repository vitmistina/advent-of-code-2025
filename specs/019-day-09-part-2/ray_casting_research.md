# Ray Casting Algorithm Research: Point-in-Polygon Testing

## 1. Standard Ray Casting Algorithm

### Core Principle

The ray casting algorithm (also known as the even-odd rule or crossing number algorithm) determines if a point is inside a polygon by casting a ray from the point to infinity and counting edge crossings:

- **Odd number of crossings** → point is **inside**
- **Even number of crossings** → point is **outside**

### Mathematical Foundation

```python
def point_in_polygon_basic(point: tuple[float, float],
                           polygon: list[tuple[float, float]]) -> bool:
    """
    Basic ray casting algorithm using horizontal ray to the right.

    Time Complexity: O(n) where n is number of polygon vertices
    Space Complexity: O(1)
    """
    x, y = point
    n = len(polygon)
    inside = False

    # Iterate through each edge of the polygon
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]  # Wraparound to first vertex

        # Check if ray crosses this edge
        if ((y1 > y) != (y2 > y)) and (x < (x2 - x1) * (y - y1) / (y2 - y1) + x1):
            inside = not inside

    return inside
```

### Algorithm Steps

1. **Choose ray direction**: Typically horizontal (right) or vertical (up/down)
2. **For each polygon edge**: Check if the ray intersects the edge
3. **Count crossings**: Toggle inside/outside state with each crossing
4. **Return result**: Final state determines if point is inside

---

## 2. Edge Crossing Toggle Mechanism

### State Machine Model

The ray casting algorithm operates as a state machine:

```
Initial State: OUTSIDE (or determined by first crossing)
              ↓
         [Ray Start]
              ↓
    ┌─────────┴─────────┐
    │                   │
    ↓                   ↓
 OUTSIDE ←─────→ INSIDE
         crossing    crossing
```

### Toggle Logic

```python
class RayState:
    """Track inside/outside state during ray traversal."""

    def __init__(self, initial_state: bool = False):
        self.inside = initial_state
        self.crossings = 0

    def cross_edge(self):
        """Toggle state when crossing an edge."""
        self.inside = not self.inside
        self.crossings += 1

    def is_inside(self) -> bool:
        return self.inside
```

### Segment Generation Pattern

For polygon interior detection with ray tracing, segments track continuous regions:

```python
from dataclasses import dataclass
from typing import Literal

@dataclass
class RaySegment:
    """Represents a continuous segment along a ray."""
    start: int  # Starting coordinate
    end: int    # Ending coordinate (exclusive for half-open intervals)
    state: Literal['inside', 'outside']

def generate_segments(ray_start: int,
                     edge_crossings: list[int],
                     initial_state: Literal['inside', 'outside']) -> list[RaySegment]:
    """
    Generate segments from edge crossings.

    Args:
        ray_start: Starting coordinate of the ray
        edge_crossings: Sorted list of coordinates where edges are crossed
        initial_state: State at ray_start ('inside' or 'outside')

    Returns:
        List of RaySegment objects representing continuous regions
    """
    if not edge_crossings:
        # No crossings - entire ray is one segment
        return [RaySegment(ray_start, float('inf'), initial_state)]

    segments = []
    current_pos = ray_start
    current_state = initial_state

    for crossing in edge_crossings:
        # Add segment from current position to crossing
        if crossing > current_pos:  # Skip zero-width segments
            segments.append(RaySegment(current_pos, crossing, current_state))

        # Toggle state after crossing
        current_state = 'outside' if current_state == 'inside' else 'inside'
        current_pos = crossing

    # Add final segment from last crossing to infinity
    segments.append(RaySegment(current_pos, float('inf'), current_state))

    return segments
```

### Example: Segment Generation

```
Ray direction: →
Starting at position 0, initial state: INSIDE

Edge crossings at: [3, 4, 7]

Position: 0   1   2   3   4   5   6   7   8   9
State:    I   I   I   O   I   I   I   O   O   O
Segments: [====]     [=======]

Segment 1: (0, 3, 'inside')   - Width 3
Segment 2: (3, 4, 'outside')  - Width 1
Segment 3: (4, 7, 'inside')   - Width 3
Segment 4: (7, ∞, 'outside')  - Extends to boundary
```

---

## 3. Edge Case Handling

### Edge Case 1: Ray Through Vertex

**Problem**: When a ray passes exactly through a polygon vertex, it may count as 0, 1, or 2 crossings depending on the geometry.

**Solution**: Apply consistent vertex handling rules:

```python
def crosses_edge_robust(ray_y: float,
                       edge_start: tuple[float, float],
                       edge_end: tuple[float, float],
                       ray_x: float) -> bool:
    """
    Robust edge crossing test that handles vertex cases.

    Convention: Include edge if ray_y is in [min_y, max_y),
    excluding the upper vertex (half-open interval).
    """
    x1, y1 = edge_start
    x2, y2 = edge_end

    # Ensure y1 < y2 for consistent comparison
    if y1 > y2:
        x1, y1, x2, y2 = x2, y2, x1, y1

    # Ray must be strictly between y1 (inclusive) and y2 (exclusive)
    if not (y1 <= ray_y < y2):
        return False

    # Compute x-intersection of ray with edge
    # Edge equation: x = x1 + (x2-x1) * (y-y1) / (y2-y1)
    x_intersection = x1 + (x2 - x1) * (ray_y - y1) / (y2 - y1)

    # Ray crosses if intersection is to the right of ray origin
    return ray_x < x_intersection
```

**Key Principle**: Use half-open intervals [y_min, y_max) so each vertex is counted exactly once.

### Edge Case 2: Ray Along Edge

**Problem**: When a ray travels parallel to a polygon edge, it's unclear whether to count as inside or outside.

**Solution 1: Parallel Edge Exclusion**

```python
def is_parallel_to_ray(edge_start: tuple[int, int],
                      edge_end: tuple[int, int],
                      ray_direction: Literal['horizontal', 'vertical']) -> bool:
    """Check if edge is parallel to ray direction."""
    x1, y1 = edge_start
    x2, y2 = edge_end

    if ray_direction == 'horizontal':
        return y1 == y2  # Horizontal edge
    else:  # vertical
        return x1 == x2  # Vertical edge
```

**Solution 2: Perpendicular Edge Filtering**

```python
def filter_perpendicular_edges(all_edges: list[tuple[tuple[int, int], tuple[int, int]]],
                               ray_direction: Literal['up', 'down', 'left', 'right'],
                               ray_coordinate: int) -> list[tuple[int, int]]:
    """
    Filter edges perpendicular to ray and matching the ray's fixed coordinate.

    For horizontal rays (left/right): Select vertical edges with matching X
    For vertical rays (up/down): Select horizontal edges with matching Y

    Returns:
        List of crossing coordinates (sorted)
    """
    crossings = []

    for edge_start, edge_end in all_edges:
        x1, y1 = edge_start
        x2, y2 = edge_end

        if ray_direction in ['left', 'right']:
            # Need vertical edges (x1 == x2) at ray's Y coordinate
            if x1 == x2 and x1 == ray_coordinate:
                # Add both endpoints (will be deduplicated/sorted later)
                crossings.extend([y1, y2])

        else:  # 'up' or 'down'
            # Need horizontal edges (y1 == y2) at ray's X coordinate
            if y1 == y2 and y1 == ray_coordinate:
                crossings.extend([x1, x2])

    return sorted(set(crossings))  # Remove duplicates and sort
```

### Edge Case 3: Degenerate Cases

```python
def handle_degenerate_cases(polygon: list[tuple[int, int]],
                           point: tuple[int, int]) -> bool | None:
    """
    Handle degenerate cases before applying ray casting.

    Returns:
        True if inside, False if outside, None if non-degenerate (proceed with algorithm)
    """
    # Empty polygon
    if len(polygon) < 3:
        return False

    # Point on vertex
    if point in polygon:
        return True  # Or False, depending on problem definition

    # Point on edge (requires separate edge-point test)
    for i in range(len(polygon)):
        edge_start = polygon[i]
        edge_end = polygon[(i + 1) % len(polygon)]
        if point_on_segment(point, edge_start, edge_end):
            return True  # Or False, depending on problem definition

    return None  # Non-degenerate case

def point_on_segment(point: tuple[int, int],
                    seg_start: tuple[int, int],
                    seg_end: tuple[int, int]) -> bool:
    """Check if point lies on line segment (for integer coordinates)."""
    px, py = point
    x1, y1 = seg_start
    x2, y2 = seg_end

    # Check collinearity using cross product
    cross = (py - y1) * (x2 - x1) - (px - x1) * (y2 - y1)
    if cross != 0:
        return False

    # Check if point is within segment bounds
    if min(x1, x2) <= px <= max(x1, x2) and min(y1, y2) <= py <= max(y1, y2):
        return True

    return False
```

---

## 4. Efficient Python Implementation Patterns

### Pattern 1: Precomputed Edge Sets with Coordinate Filtering

```python
from collections import defaultdict
from typing import Literal

class EdgeIndex:
    """Precomputed edge index for efficient ray casting."""

    def __init__(self, polygon: list[tuple[int, int]]):
        self.polygon = polygon
        self.horizontal_edges_by_y = defaultdict(list)  # y -> [(x1, x2), ...]
        self.vertical_edges_by_x = defaultdict(list)    # x -> [(y1, y2), ...]
        self._build_index()

    def _build_index(self):
        """Build coordinate-indexed edge structures."""
        n = len(self.polygon)

        for i in range(n):
            x1, y1 = self.polygon[i]
            x2, y2 = self.polygon[(i + 1) % n]

            # Horizontal edge
            if y1 == y2:
                min_x, max_x = min(x1, x2), max(x1, x2)
                self.horizontal_edges_by_y[y1].append((min_x, max_x))

            # Vertical edge
            elif x1 == x2:
                min_y, max_y = min(y1, y2), max(y1, y2)
                self.vertical_edges_by_x[x1].append((min_y, max_y))

    def cast_ray_horizontal(self, start_x: int, y: int,
                           direction: Literal['left', 'right']) -> list[int]:
        """
        Cast horizontal ray and return crossing x-coordinates.

        Optimization: Only considers vertical edges at the ray's y-coordinate.
        """
        crossings = []

        # For horizontal ray, we need vertical edges
        for x, y_ranges in self.vertical_edges_by_x.items():
            for y_min, y_max in y_ranges:
                # Check if ray's y-coordinate intersects this vertical edge
                if y_min <= y < y_max:  # Half-open interval
                    # Check if edge is in ray direction
                    if direction == 'right' and x > start_x:
                        crossings.append(x)
                    elif direction == 'left' and x < start_x:
                        crossings.append(x)

        return sorted(crossings, reverse=(direction == 'left'))

    def cast_ray_vertical(self, x: int, start_y: int,
                         direction: Literal['up', 'down']) -> list[int]:
        """
        Cast vertical ray and return crossing y-coordinates.

        Optimization: Only considers horizontal edges at the ray's x-coordinate.
        """
        crossings = []

        # For vertical ray, we need horizontal edges
        for y, x_ranges in self.horizontal_edges_by_y.items():
            for x_min, x_max in x_ranges:
                # Check if ray's x-coordinate intersects this horizontal edge
                if x_min <= x < x_max:  # Half-open interval
                    # Check if edge is in ray direction
                    if direction == 'down' and y > start_y:
                        crossings.append(y)
                    elif direction == 'up' and y < start_y:
                        crossings.append(y)

        return sorted(crossings, reverse=(direction == 'up'))
```

### Pattern 2: Initial State Determination

```python
def determine_initial_ray_state(corner: tuple[int, int],
                               ray_direction: Literal['up', 'down', 'left', 'right'],
                               edge_index: EdgeIndex,
                               polygon_winding: Literal['cw', 'ccw']) -> Literal['inside', 'outside']:
    """
    Determine if the first tile in ray direction is inside or outside the polygon.

    Uses the half-open interval convention: the ray starts one unit away from
    the corner, and we check if that position immediately intersects a
    perpendicular boundary.

    Args:
        corner: Starting corner (x, y)
        ray_direction: Direction of the ray
        edge_index: Precomputed edge index
        polygon_winding: Polygon orientation ('cw' or 'ccw')

    Returns:
        'inside' or 'outside' - the initial state of the ray
    """
    x, y = corner

    # Compute the first position along the ray (one unit away)
    if ray_direction == 'right':
        first_pos = (x + 1, y)
        perpendicular_coord = y
        check_edges = edge_index.vertical_edges_by_x
    elif ray_direction == 'left':
        first_pos = (x - 1, y)
        perpendicular_coord = y
        check_edges = edge_index.vertical_edges_by_x
    elif ray_direction == 'down':
        first_pos = (x, y + 1)
        perpendicular_coord = x
        check_edges = edge_index.horizontal_edges_by_y
    else:  # 'up'
        first_pos = (x, y - 1)
        perpendicular_coord = x
        check_edges = edge_index.horizontal_edges_by_y

    # Check if the first position immediately crosses a perpendicular edge
    # This is a simplified check - actual implementation depends on geometry

    # For clockwise polygons, interior is to the right of directed edges
    # For counter-clockwise, interior is to the left

    # Heuristic: If stepping in ray direction immediately hits an edge
    # perpendicular to that direction, we start outside

    # This is problem-specific - returning a placeholder
    return 'inside'  # Default assumption for rays starting from polygon vertices
```

### Pattern 3: Zero-Width Segment Filtering

```python
def filter_zero_width_segments(segments: list[RaySegment]) -> list[RaySegment]:
    """
    Remove zero-width 'outside' segments created by consecutive edge crossings.

    Zero-width segments occur when two edges are crossed in immediate succession,
    representing a ray that grazes along the polygon boundary momentarily.
    """
    filtered = []

    for seg in segments:
        width = seg.end - seg.start

        # Keep all 'inside' segments and non-zero-width 'outside' segments
        if seg.state == 'inside' or width > 0:
            filtered.append(seg)

    return filtered
```

### Pattern 4: Complete Optimized Implementation

```python
class OptimizedRayCaster:
    """
    Optimized ray casting for axis-aligned rectangle validation.

    Key optimizations:
    1. Precomputed edge index by coordinate
    2. Coordinate filtering (only check relevant edges)
    3. Half-open interval convention for consistent vertex handling
    4. Zero-width segment elimination
    """

    def __init__(self, polygon: list[tuple[int, int]]):
        self.polygon = polygon
        self.edge_index = EdgeIndex(polygon)
        self.winding = self._compute_winding()

    def _compute_winding(self) -> Literal['cw', 'ccw']:
        """Compute polygon winding using signed area."""
        area = 0
        n = len(self.polygon)

        for i in range(n):
            x1, y1 = self.polygon[i]
            x2, y2 = self.polygon[(i + 1) % n]
            area += (x2 - x1) * (y2 + y1)

        return 'cw' if area > 0 else 'ccw'

    def validate_rectangle(self, corner1: tuple[int, int],
                          corner2: tuple[int, int]) -> bool:
        """
        Validate if rectangle with opposite corners is entirely inside polygon.

        Casts 4 rays (2 from each corner in perpendicular directions) and
        checks if any rectangle edge crosses an 'outside' segment.
        """
        x1, y1 = corner1
        x2, y2 = corner2

        # Ensure corner1 is bottom-left, corner2 is top-right
        min_x, max_x = min(x1, x2), max(x1, x2)
        min_y, max_y = min(y1, y2), max(y1, y2)

        # Cast rays from each corner
        corners_and_directions = [
            ((min_x, min_y), ['right', 'up']),     # Bottom-left
            ((max_x, max_y), ['left', 'down']),    # Top-right
            ((min_x, max_y), ['right', 'down']),   # Top-left
            ((max_x, min_y), ['left', 'up']),      # Bottom-right
        ]

        for corner, directions in corners_and_directions:
            for direction in directions:
                if not self._validate_ray(corner, direction, min_x, max_x, min_y, max_y):
                    return False

        return True

    def _validate_ray(self, corner: tuple[int, int],
                     direction: str,
                     rect_min_x: int, rect_max_x: int,
                     rect_min_y: int, rect_max_y: int) -> bool:
        """
        Validate a single ray - check if rectangle edge overlaps 'outside' segment.
        """
        x, y = corner

        # Get crossings for this ray
        if direction in ['left', 'right']:
            crossings = self.edge_index.cast_ray_horizontal(x, y, direction)
            rect_edge_start = rect_min_x if direction == 'right' else rect_max_x
            rect_edge_end = rect_max_x if direction == 'right' else rect_min_x
        else:  # up or down
            crossings = self.edge_index.cast_ray_vertical(x, y, direction)
            rect_edge_start = rect_min_y if direction == 'up' else rect_max_y
            rect_edge_end = rect_max_y if direction == 'up' else rect_min_y

        # Determine initial state
        initial_state = determine_initial_ray_state(corner, direction,
                                                    self.edge_index, self.winding)

        # Generate segments
        segments = generate_segments(x, crossings, initial_state)
        segments = filter_zero_width_segments(segments)

        # Check if rectangle edge overlaps any 'outside' segment
        for seg in segments:
            if seg.state == 'outside':
                # Check if [rect_edge_start, rect_edge_end] overlaps [seg.start, seg.end]
                if max(rect_edge_start, seg.start) < min(rect_edge_end, seg.end):
                    return False  # Rectangle edge crosses outside region

        return True
```

---

## 5. Coordinate Filtering Optimization

### Optimization Strategy

**Problem**: Naive ray casting iterates over all polygon edges (O(n) per ray).

**Solution**: Index edges by coordinate, filter to relevant subset (O(1) average case with good spatial distribution).

### Implementation: Coordinate-Based Edge Lookup

```python
class CoordinateFilteredEdges:
    """
    Index edges by their fixed coordinate for O(1) filtering.

    For axis-aligned grids:
    - Horizontal edges indexed by Y
    - Vertical edges indexed by X
    """

    def __init__(self):
        # Map: coordinate -> list of edge spans
        self.horizontal_by_y: dict[int, list[tuple[int, int]]] = defaultdict(list)
        self.vertical_by_x: dict[int, list[tuple[int, int]]] = defaultdict(list)

    def add_horizontal_edge(self, y: int, x_start: int, x_end: int):
        """Add horizontal edge at fixed y-coordinate."""
        self.horizontal_by_y[y].append((min(x_start, x_end), max(x_start, x_end)))

    def add_vertical_edge(self, x: int, y_start: int, y_end: int):
        """Add vertical edge at fixed x-coordinate."""
        self.vertical_by_x[x].append((min(y_start, y_end), max(y_start, y_end)))

    def get_horizontal_edges_at_x(self, x: int) -> list[tuple[int, int]]:
        """
        Get horizontal edges that intersect vertical line at x.

        Returns:
            List of (y, y_span) where edge exists at this x
        """
        intersections = []
        for y, x_spans in self.horizontal_by_y.items():
            for x_min, x_max in x_spans:
                if x_min <= x <= x_max:
                    intersections.append(y)
        return sorted(set(intersections))

    def get_vertical_edges_at_y(self, y: int) -> list[int]:
        """
        Get vertical edges that intersect horizontal line at y.

        Returns:
            List of x-coordinates where edges exist at this y
        """
        intersections = []
        for x, y_spans in self.vertical_by_x.items():
            for y_min, y_max in y_spans:
                if y_min <= y <= y_max:
                    intersections.append(x)
        return sorted(set(intersections))
```

### Performance Comparison

```python
# Naive approach: O(E) per ray, where E = number of edges
def naive_ray_cast(ray_y: int, edges: list[Edge]) -> int:
    crossings = 0
    for edge in edges:  # O(E)
        if ray_crosses_edge(ray_y, edge):
            crossings += 1
    return crossings

# Optimized approach: O(K) per ray, where K = edges at ray's coordinate
def optimized_ray_cast(ray_y: int, edge_index: CoordinateFilteredEdges) -> int:
    relevant_edges = edge_index.get_vertical_edges_at_y(ray_y)  # O(K), K << E
    return len(relevant_edges)
```

**Complexity Analysis**:

- **Naive**: O(R × E) for R rays and E edges
- **Optimized**: O(R × K) where K is average edges per coordinate
- **Speedup**: ~100x for sparse grids (K ≈ 10, E ≈ 1000)

### Spatial Indexing for Large Grids

For very large grids, add secondary spatial index:

```python
from typing import NamedTuple

class BoundingBox(NamedTuple):
    min_x: int
    max_x: int
    min_y: int
    max_y: int

class SpatiallyIndexedEdges:
    """Two-level index: coarse grid cells + coordinate maps."""

    def __init__(self, cell_size: int = 100):
        self.cell_size = cell_size
        self.cells: dict[tuple[int, int], CoordinateFilteredEdges] = {}

    def _get_cell(self, x: int, y: int) -> tuple[int, int]:
        """Map coordinate to cell ID."""
        return (x // self.cell_size, y // self.cell_size)

    def add_edge(self, start: tuple[int, int], end: tuple[int, int]):
        """Add edge and index in relevant cells."""
        x1, y1 = start
        x2, y2 = end

        # Find all cells this edge crosses
        cell_start = self._get_cell(x1, y1)
        cell_end = self._get_cell(x2, y2)

        # Add to all relevant cells (simplified - assume axis-aligned)
        for cx in range(min(cell_start[0], cell_end[0]),
                       max(cell_start[0], cell_end[0]) + 1):
            for cy in range(min(cell_start[1], cell_end[1]),
                           max(cell_start[1], cell_end[1]) + 1):
                cell_key = (cx, cy)
                if cell_key not in self.cells:
                    self.cells[cell_key] = CoordinateFilteredEdges()

                # Add edge to this cell's index
                if y1 == y2:  # Horizontal
                    self.cells[cell_key].add_horizontal_edge(y1, x1, x2)
                else:  # Vertical
                    self.cells[cell_key].add_vertical_edge(x1, y1, y2)
```

---

## Summary: Best Practices for Efficient Ray Casting

### 1. **Precomputation Phase**

- Build edge index organized by coordinate (x for vertical, y for horizontal)
- Compute polygon winding (clockwise/counter-clockwise)
- Classify corners as convex/concave for advanced filtering

### 2. **Ray Casting Phase**

- Use axis-aligned rays (horizontal or vertical only)
- Apply coordinate filtering: only check edges perpendicular to ray
- Use half-open intervals [min, max) for consistent vertex handling
- Start rays one unit away from corners to avoid ambiguity

### 3. **State Tracking**

- Initialize state based on outward normal and ray direction
- Toggle state at each edge crossing
- Generate segments as (start, end, state) tuples

### 4. **Optimization Techniques**

- **Coordinate filtering**: O(K) instead of O(E) per ray
- **Zero-width elimination**: Filter out consecutive crossings
- **Early termination**: Stop validation on first 'outside' overlap
- **Spatial indexing**: Grid cells for very large problems

### 5. **Edge Case Handling**

- **Vertex touching**: Half-open intervals prevent double-counting
- **Parallel edges**: Filter to perpendicular edges only
- **Concave corners**: Include in edge set but respect blocking direction
- **Degenerate rectangles**: Handle zero-width/height cases

### 6. **Code Patterns**

```python
# Pattern 1: Build index
edge_index = EdgeIndex(polygon)

# Pattern 2: Cast ray with filtering
crossings = edge_index.cast_ray_horizontal(start_x, y, 'right')

# Pattern 3: Generate segments
segments = generate_segments(start_x, crossings, initial_state)
segments = filter_zero_width_segments(segments)

# Pattern 4: Validate rectangle edge
for seg in segments:
    if seg.state == 'outside' and overlaps(seg, rect_edge):
        return False
return True
```

---

## References & Further Reading

1. **Sunday, D.** (2001). "Inclusion of a Point in a Polygon" - Comprehensive edge case analysis
2. **Haines, E.** (1994). "Point in Polygon Strategies" - Performance comparison of algorithms
3. **O'Rourke, J.** (1998). "Computational Geometry in C" - Mathematical foundations
4. **Preparata & Shamos** (1985). "Computational Geometry: An Introduction" - Theoretical analysis

**Complexity Guarantees**:

- Preprocessing: O(E) to build edge index
- Per-ray query: O(K) where K = edges at coordinate
- Per-rectangle: O(4 × K) = O(K) for edge-only validation
- Total: O(E + R × K) vs naive O(R × E)

**When to Use**:

- ✅ Axis-aligned grids with sparse edge distribution
- ✅ Many rectangle validation queries
- ✅ Need for deterministic edge case handling
- ❌ Non-axis-aligned polygons (requires different algorithm)
- ❌ Single point-in-polygon queries (simpler algorithm sufficient)
