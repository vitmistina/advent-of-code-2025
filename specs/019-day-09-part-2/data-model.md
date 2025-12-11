# Data Model: Day 9 Part 2 - Optimized Ray Tracing

**Feature**: Day 9 Part 2 - Largest Red-Green Rectangle  
**Date**: December 11, 2025  
**Source**: Extracted from feature spec and research decisions

---

## Entity: RedTile

Represents a single red tile vertex in the closed polygon loop.

### Fields

| Field       | Type              | Description                              | Validation                    |
| ----------- | ----------------- | ---------------------------------------- | ----------------------------- |
| `position`  | `tuple[int, int]` | (x, y) coordinate of the tile            | Non-negative integers         |
| `incoming`  | `tuple[int, int]` | Unit direction vector from previous tile | One of: (0,±1), (±1,0)        |
| `outgoing`  | `tuple[int, int]` | Unit direction vector to next tile       | One of: (0,±1), (±1,0)        |
| `turn_type` | `str`             | Classification as "convex" or "concave"  | Must be "convex" or "concave" |
| `index`     | `int`             | Position in ordered vertex list          | 0 ≤ index < n                 |

### Relationships

- **Sequential**: Each RedTile connects to next RedTile via `outgoing` direction
- **Circular**: Last RedTile wraps to first RedTile (closed loop)
- **Polygon**: Collection of all RedTiles forms simple closed polygon

### State Transitions

1. **Parsing** → RedTile created with position
2. **Direction Computation** → incoming/outgoing vectors added
3. **Classification** → turn_type determined based on winding

### Invariants

- Consecutive tiles must be axis-aligned (same x OR same y)
- `incoming` and `outgoing` must differ (no straight angles in polygon)
- All tiles in list form a simple, non-self-intersecting loop

---

## Entity: GreenEdgeTile

Represents a green tile on the straight path between consecutive red tiles.

### Fields

| Field         | Type              | Description                                         | Validation                         |
| ------------- | ----------------- | --------------------------------------------------- | ---------------------------------- |
| `position`    | `tuple[int, int]` | (x, y) coordinate of the tile                       | Non-negative integers              |
| `orientation` | `str`             | "horizontal" or "vertical"                          | Must be "horizontal" or "vertical" |
| `coordinate`  | `int`             | Fixed coordinate (y for horizontal, x for vertical) | Non-negative integer               |

### Relationships

- **Segment**: Part of edge between two consecutive RedTiles
- **Indexed**: Stored in EdgeIndex by coordinate for fast lookup

### Invariants

- Lies on line segment between two consecutive RedTiles
- Not a RedTile itself (intermediate position only)

---

## Entity: EdgeIndex

Precomputed data structure for efficient ray casting.

### Fields

| Field              | Type                       | Description                                        |
| ------------------ | -------------------------- | -------------------------------------------------- |
| `horizontal_edges` | `dict[int, list[int]]`     | Maps y-coordinate → list of x positions with edges |
| `vertical_edges`   | `dict[int, list[int]]`     | Maps x-coordinate → list of y positions with edges |
| `corners`          | `dict[str, list[RedTile]]` | Maps coordinate key → list of corner tiles         |

### Methods

| Method             | Parameters | Returns         | Description                                      |
| ------------------ | ---------- | --------------- | ------------------------------------------------ |
| `get_edges_at_x`   | `x: int`   | `list[int]`     | Returns all y positions of vertical edges at x   |
| `get_edges_at_y`   | `y: int`   | `list[int]`     | Returns all x positions of horizontal edges at y |
| `get_corners_at_x` | `x: int`   | `list[RedTile]` | Returns corners with perpendicular edges at x    |
| `get_corners_at_y` | `y: int`   | `list[RedTile]` | Returns corners with perpendicular edges at y    |

### Relationships

- **Contains**: All GreenEdgeTiles organized by coordinate
- **References**: All RedTiles with perpendicular edges for ray filtering

---

## Entity: Ray

Represents a directional scan from a rectangle corner.

### Fields

| Field           | Type  | Description                           | Validation                   |
| --------------- | ----- | ------------------------------------- | ---------------------------- |
| `start_pos`     | `int` | Starting coordinate (x or y)          | Non-negative integer         |
| `end_pos`       | `int` | Ending coordinate (x or y)            | Must be > start_pos          |
| `fixed_coord`   | `int` | Fixed coordinate perpendicular to ray | Non-negative integer         |
| `direction`     | `str` | "horizontal" or "vertical"            | Must match edge orientation  |
| `initial_state` | `str` | "inside" or "outside"                 | Determined by boundary check |

### Relationships

- **Cast from**: Rectangle corner (RedTile)
- **Uses**: EdgeIndex filtered by fixed_coord
- **Generates**: List of RaySegments

### State Transitions

1. **Initialization** → Start/end/fixed coordinates set
2. **Filtering** → Relevant edges retrieved from EdgeIndex
3. **State Determination** → Initial inside/outside state computed
4. **Segment Generation** → Edge crossings produce RaySegments

---

## Entity: RaySegment

Represents a continuous region along a ray where tiles are inside or outside the polygon.

### Fields

| Field   | Type  | Description                    | Validation                    |
| ------- | ----- | ------------------------------ | ----------------------------- |
| `start` | `int` | Starting coordinate of segment | Non-negative integer          |
| `end`   | `int` | Ending coordinate of segment   | Must be ≥ start               |
| `state` | `str` | "inside" or "outside"          | Must be "inside" or "outside" |

### Relationships

- **Part of**: Ray that generated this segment
- **Validated against**: Rectangle edge boundaries

### Invariants

- Consecutive segments must have opposite states (toggle on crossing)
- Zero-width "outside" segments (start == end) are filtered out
- Segments span the entire ray from start to end with no gaps

---

## Entity: Rectangle

Represents a candidate rectangle formed by two red tiles as opposite corners.

### Fields

| Field      | Type              | Description                             | Validation                           |
| ---------- | ----------------- | --------------------------------------- | ------------------------------------ |
| `corner1`  | `tuple[int, int]` | First red tile corner (min x, min y)    | Valid RedTile position               |
| `corner2`  | `tuple[int, int]` | Opposite red tile corner (max x, max y) | Valid RedTile position               |
| `width`    | `int`             | Horizontal distance                     | Must be > 0                          |
| `height`   | `int`             | Vertical distance                       | Must be > 0                          |
| `area`     | `int`             | Total area (width × height)             | Must be > 0                          |
| `is_valid` | `bool`            | Whether all edges are inside polygon    | Initially None, set after validation |

### Relationships

- **Corners**: Two RedTiles from the polygon
- **Validated by**: Four Rays (two per corner, perpendicular directions)
- **Has**: Four edges that must not overlap "outside" segments

### Validation Rules

For each of the four rectangle edges:

1. Cast rays along that edge from appropriate corners
2. Check if edge coordinates overlap any "outside" RaySegment
3. Rectangle is valid only if all four edges remain "inside"

### State Transitions

1. **Enumeration** → Rectangle created from RedTile pair
2. **Area Calculation** → width, height, area computed
3. **Ray Casting** → Four rays cast and segments generated
4. **Validation** → is_valid set based on segment overlaps
5. **Comparison** → Valid rectangles compared for maximum area

---

## Data Flow Diagram

```
Input Text
    ↓
[Parse Coordinates]
    ↓
List of RedTiles (positions only)
    ↓
[Compute Winding Direction] ← Signed Area
    ↓
List of RedTiles (+ incoming/outgoing/turn_type)
    ↓
[Precompute Green Edges]
    ↓
EdgeIndex (horizontal_edges, vertical_edges, corners)
    ↓
[Enumerate Rectangle Pairs]
    ↓
List of Rectangles (corner pairs)
    ↓
[For Each Rectangle: Cast 4 Rays]
    ↓
Rays → RaySegments (inside/outside states)
    ↓
[Validate Edges Against Segments]
    ↓
Valid Rectangles (is_valid=True)
    ↓
[Find Maximum Area]
    ↓
Result: Maximum Rectangle Area (int)
```

---

## Storage Considerations

### Memory Efficiency

| Structure   | Size  | Notes                                  |
| ----------- | ----- | -------------------------------------- |
| RedTiles    | O(n)  | n = number of red tiles (~10-1000)     |
| EdgeIndex   | O(E)  | E = number of green edges (~100-10000) |
| Rectangles  | O(n²) | Enumerated but not all stored          |
| RaySegments | O(K)  | K = edges per coordinate (~1-100)      |

**Peak memory**: O(E) for EdgeIndex, all other structures are transient

### Performance Optimization

- **EdgeIndex precomputation**: One-time O(n) cost, amortized over O(n²) rectangles
- **Coordinate filtering**: Reduces per-ray cost from O(E) to O(K)
- **Early rejection**: Invalid rectangles discarded immediately
- **Segment caching**: Not needed (segments computed per rectangle)

---

## Example Data Instance (From Test Case)

### Input

```
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
```

### Parsed RedTiles

```python
[
    RedTile(position=(7,1), incoming=(0,-1), outgoing=(1,0), turn_type="convex", index=0),
    RedTile(position=(11,1), incoming=(1,0), outgoing=(0,1), turn_type="convex", index=1),
    RedTile(position=(11,7), incoming=(0,1), outgoing=(-1,0), turn_type="convex", index=2),
    RedTile(position=(9,7), incoming=(-1,0), outgoing=(0,-1), turn_type="convex", index=3),
    RedTile(position=(9,5), incoming=(0,-1), outgoing=(-1,0), turn_type="concave", index=4),
    RedTile(position=(2,5), incoming=(-1,0), outgoing=(0,-1), turn_type="convex", index=5),
    RedTile(position=(2,3), incoming=(0,-1), outgoing=(1,0), turn_type="convex", index=6),
    RedTile(position=(7,3), incoming=(1,0), outgoing=(0,-1), turn_type="concave", index=7),
]
```

### EdgeIndex (Partial)

```python
horizontal_edges = {
    1: [8, 9, 10],      # y=1: edges from (7,1) to (11,1)
    3: [3, 4, 5, 6],    # y=3: edges from (2,3) to (7,3)
    5: [3, 4, 5, 6, 7, 8],  # y=5: edges from (2,5) to (9,5)
    7: [10],            # y=7: edge from (9,7) to (11,7)
}

vertical_edges = {
    2: [4],             # x=2: edge from (2,3) to (2,5)
    7: [2],             # x=7: edge from (7,1) to (7,3)
    9: [6],             # x=9: edge from (9,5) to (9,7)
    11: [2, 3, 4, 5, 6],  # x=11: edges from (11,1) to (11,7)
}
```

### Valid Rectangle Example

```python
Rectangle(
    corner1=(2,3),
    corner2=(9,5),
    width=7,
    height=2,
    area=14,  # NOT 24 - this is example structure only
    is_valid=True  # All edges inside polygon
)
```

---

## Validation Rules Summary

### RedTile Validation

- Position coordinates must be non-negative integers
- Consecutive tiles must be axis-aligned (same x OR same y)
- Loop must close (last tile connects to first)
- No self-intersections (guaranteed by puzzle)

### Rectangle Validation

- Both corners must be existing RedTiles
- Width and height must be positive
- All four edges must not overlap "outside" RaySegments
- Area calculation: `(max_x - min_x + 1) × (max_y - min_y + 1)` (inclusive)

### Ray Segment Validation

- Segments must cover entire ray with no gaps
- Consecutive segments must have opposite states
- Zero-width "outside" segments are filtered
- Initial state determined by perpendicular boundary check

---

**Status**: ✅ Data Model Complete  
**Next**: Generate API contracts for function signatures
