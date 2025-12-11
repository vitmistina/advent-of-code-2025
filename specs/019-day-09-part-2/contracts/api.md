# API Contract: Core Function Signatures

**Feature**: Day 9 Part 2 - Optimized Ray Tracing  
**Date**: December 11, 2025  
**Purpose**: Define all public function signatures and contracts

---

## Main Entry Point

### `solve_part2(input_data: str) -> int`

**Purpose**: Main solution function for Day 9 Part 2

**Parameters**:

- `input_data` (str): Raw puzzle input with one "x,y" coordinate per line

**Returns**:

- `int`: Maximum area of valid rectangles formed by red tiles

**Raises**:

- `ValueError`: If input is malformed or empty
- `ValueError`: If consecutive tiles are not axis-aligned
- `ValueError`: If polygon is degenerate (zero area)

**Example**:

```python
input_data = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""

result = solve_part2(input_data)
assert result == 24
```

**Contract**:

- MUST parse all coordinates successfully
- MUST validate axis-alignment
- MUST detect winding direction
- MUST classify all turns
- MUST enumerate all rectangle pairs
- MUST validate rectangles via ray casting
- MUST return maximum area among valid rectangles

---

## Parsing Functions

### `parse_coordinates(input_data: str) -> list[tuple[int, int]]`

**Purpose**: Parse raw input into list of (x, y) coordinates

**Parameters**:

- `input_data` (str): Multi-line string with "x,y" format

**Returns**:

- `list[tuple[int, int]]`: Ordered list of coordinates

**Raises**:

- `ValueError`: If any line is malformed
- `ValueError`: If coordinates are negative
- `ValueError`: If input is empty

**Example**:

```python
coords = parse_coordinates("7,1\n11,1\n11,7")
assert coords == [(7, 1), (11, 1), (11, 7)]
```

**Contract**:

- MUST strip whitespace from lines
- MUST validate integer format
- MUST validate non-negative values
- MUST preserve order

---

### `validate_axis_alignment(vertices: list[tuple[int, int]]) -> None`

**Purpose**: Validate that consecutive vertices are axis-aligned

**Parameters**:

- `vertices` (list[tuple[int, int]]): Ordered vertex list

**Returns**:

- `None`

**Raises**:

- `ValueError`: If any consecutive pair is not axis-aligned (same x OR same y)

**Example**:

```python
valid = [(0, 0), (5, 0), (5, 5)]  # OK: horizontal then vertical
validate_axis_alignment(valid)  # No exception

invalid = [(0, 0), (3, 4)]  # ERROR: diagonal
validate_axis_alignment(invalid)  # Raises ValueError
```

**Contract**:

- MUST check all consecutive pairs including wraparound (last to first)
- MUST raise on first invalid pair

---

## Winding and Classification Functions

### `compute_signed_area(vertices: list[tuple[int, int]]) -> float`

**Purpose**: Compute signed area using shoelace formula

**Parameters**:

- `vertices` (list[tuple[int, int]]): Ordered vertex list

**Returns**:

- `float`: Signed area (negative for clockwise in screen coords)

**Example**:

```python
vertices = [(0, 0), (4, 0), (4, 3), (0, 3)]
area = compute_signed_area(vertices)
assert area == 12.0  # CCW in math coords
```

**Contract**:

- MUST handle wraparound correctly
- MUST use shoelace formula
- MUST return exact value (no rounding)

---

### `is_clockwise(vertices: list[tuple[int, int]]) -> bool`

**Purpose**: Determine if vertices are ordered clockwise

**Parameters**:

- `vertices` (list[tuple[int, int]]): Ordered vertex list

**Returns**:

- `bool`: True if clockwise in screen coordinates (Y-down)

**Example**:

```python
cw_vertices = [(0, 0), (0, 3), (4, 3), (4, 0)]
assert is_clockwise(cw_vertices) == True

ccw_vertices = [(0, 0), (4, 0), (4, 3), (0, 3)]
assert is_clockwise(ccw_vertices) == False
```

**Contract**:

- MUST use signed area method
- MUST interpret negative area as clockwise (Y-down screen coords)

---

### `compute_direction_vector(from_vertex: tuple[int, int], to_vertex: tuple[int, int]) -> tuple[int, int]`

**Purpose**: Compute unit direction vector between vertices

**Parameters**:

- `from_vertex` (tuple[int, int]): Starting vertex
- `to_vertex` (tuple[int, int]): Ending vertex

**Returns**:

- `tuple[int, int]`: Unit direction vector, one of: (0, ±1), (±1, 0)

**Example**:

```python
vec = compute_direction_vector((7, 3), (7, 1))
assert vec == (0, -1)  # Moving up (y decreases)

vec = compute_direction_vector((7, 1), (11, 1))
assert vec == (1, 0)  # Moving right (x increases)
```

**Contract**:

- MUST normalize to unit vector
- MUST handle only axis-aligned edges

---

### `classify_turn(incoming: tuple[int, int], outgoing: tuple[int, int], is_clockwise: bool) -> str`

**Purpose**: Classify turn as convex or concave

**Parameters**:

- `incoming` (tuple[int, int]): Direction entering vertex
- `outgoing` (tuple[int, int]): Direction leaving vertex
- `is_clockwise` (bool): Polygon winding direction

**Returns**:

- `str`: "convex" or "concave"

**Example**:

```python
# Clockwise polygon: Up -> Right is convex (right turn)
turn = classify_turn((0, -1), (1, 0), is_clockwise=True)
assert turn == "convex"

# Clockwise polygon: Left -> Up is concave (left turn)
turn = classify_turn((-1, 0), (0, -1), is_clockwise=True)
assert turn == "concave"
```

**Contract**:

- MUST use 2D cross product
- MUST interpret based on winding direction
- MUST return only "convex" or "concave"

---

### `classify_all_vertices(vertices: list[tuple[int, int]]) -> list[dict]`

**Purpose**: Classify all vertices with full metadata

**Parameters**:

- `vertices` (list[tuple[int, int]]): Ordered vertex list

**Returns**:

- `list[dict]`: List of classification dicts with keys:
  - `vertex`: tuple[int, int]
  - `incoming`: tuple[int, int]
  - `outgoing`: tuple[int, int]
  - `classification`: str ("convex" or "concave")
  - `index`: int

**Example**:

```python
vertices = [(7,1), (11,1), (11,7)]
classifications = classify_all_vertices(vertices)
assert len(classifications) == 3
assert classifications[0]['vertex'] == (7, 1)
assert classifications[0]['classification'] == "convex"
```

**Contract**:

- MUST handle wraparound for first and last vertices
- MUST include all metadata fields
- MUST preserve vertex order

---

## Edge Precomputation Functions

### `class EdgeIndex`

#### `__init__(self, vertices: list[tuple[int, int]])`

**Purpose**: Initialize edge index from polygon vertices

**Parameters**:

- `vertices` (list[tuple[int, int]]): Ordered vertex list

**Contract**:

- MUST precompute all green edge tiles
- MUST organize into horizontal/vertical sets
- MUST handle wraparound edge

---

#### `get_edges_at_x(self, x: int) -> list[int]`

**Purpose**: Get all vertical edge y-positions at given x

**Parameters**:

- `x` (int): X-coordinate to filter by

**Returns**:

- `list[int]`: Y-positions of vertical edges at x

**Example**:

```python
index = EdgeIndex(vertices)
edges = index.get_edges_at_x(11)
assert 2 in edges  # Vertical edge at (11, 2)
```

**Contract**:

- MUST return empty list if no edges at x
- MUST return sorted positions

---

#### `get_edges_at_y(self, y: int) -> list[int]`

**Purpose**: Get all horizontal edge x-positions at given y

**Parameters**:

- `y` (int): Y-coordinate to filter by

**Returns**:

- `list[int]`: X-positions of horizontal edges at y

**Example**:

```python
index = EdgeIndex(vertices)
edges = index.get_edges_at_y(1)
assert 8 in edges  # Horizontal edge at (8, 1)
```

**Contract**:

- MUST return empty list if no edges at y
- MUST return sorted positions

---

## Ray Casting Functions

### `determine_initial_ray_state(start_pos: tuple[int, int], direction: tuple[int, int], edge_index: EdgeIndex) -> str`

**Purpose**: Determine if ray starts inside or outside polygon

**Parameters**:

- `start_pos` (tuple[int, int]): Ray starting position (adjacent to corner)
- `direction` (tuple[int, int]): Ray direction vector
- `edge_index` (EdgeIndex): Precomputed edge index

**Returns**:

- `str`: "inside" or "outside"

**Example**:

```python
# Ray going left from (9, 7) starts outside
state = determine_initial_ray_state((8, 7), (-1, 0), edge_index)
assert state == "outside"
```

**Contract**:

- MUST check if half-open interval immediately crosses perpendicular edge
- MUST return only "inside" or "outside"

---

### `generate_ray_segments(ray_start: int, ray_end: int, edge_positions: list[int], initial_state: str) -> list[tuple[int, int, str]]`

**Purpose**: Generate inside/outside segments along ray

**Parameters**:

- `ray_start` (int): Starting coordinate
- `ray_end` (int): Ending coordinate
- `edge_positions` (list[int]): Sorted edge crossing positions
- `initial_state` (str): "inside" or "outside"

**Returns**:

- `list[tuple[int, int, str]]`: List of (start, end, state) tuples

**Example**:

```python
segments = generate_ray_segments(0, 10, [3, 7], "inside")
assert segments == [(0, 3, "inside"), (3, 7, "outside"), (7, 10, "inside")]
```

**Contract**:

- MUST toggle state at each crossing
- MUST filter zero-width "outside" segments
- MUST cover entire ray with no gaps

---

### `validate_rectangle_edge(edge_start: int, edge_end: int, segments: list[tuple[int, int, str]]) -> bool`

**Purpose**: Check if rectangle edge overlaps any "outside" segment

**Parameters**:

- `edge_start` (int): Edge starting coordinate
- `edge_end` (int): Edge ending coordinate
- `segments` (list[tuple[int, int, str]]): Ray segments along edge

**Returns**:

- `bool`: True if edge entirely inside, False if any part outside

**Example**:

```python
segments = [(0, 5, "inside"), (5, 8, "outside"), (8, 10, "inside")]
assert validate_rectangle_edge(0, 4, segments) == True  # Entirely in first segment
assert validate_rectangle_edge(6, 7, segments) == False  # Overlaps outside segment
```

**Contract**:

- MUST check all segments for overlap
- MUST return False if ANY overlap with "outside" segment
- MUST handle edge cases (edge boundaries exactly on segment boundaries)

---

## Rectangle Validation Functions

### `enumerate_rectangles(vertices: list[tuple[int, int]]) -> list[tuple[tuple[int, int], tuple[int, int]]]`

**Purpose**: Generate all possible rectangle pairs from vertices

**Parameters**:

- `vertices` (list[tuple[int, int]]): List of red tile positions

**Returns**:

- `list[tuple[tuple[int, int], tuple[int, int]]]`: List of (corner1, corner2) pairs

**Example**:

```python
vertices = [(2, 3), (7, 1), (9, 5)]
rectangles = enumerate_rectangles(vertices)
assert len(rectangles) == 3  # All pairs: 3C2 = 3
```

**Contract**:

- MUST generate all unique pairs (no duplicates)
- MUST return corners in consistent order (min_x_min_y, max_x_max_y)

---

### `validate_rectangle(corner1: tuple[int, int], corner2: tuple[int, int], edge_index: EdgeIndex, classifications: list[dict]) -> bool`

**Purpose**: Validate rectangle using ray casting on all four edges

**Parameters**:

- `corner1` (tuple[int, int]): First corner (min x, min y)
- `corner2` (tuple[int, int]): Opposite corner (max x, max y)
- `edge_index` (EdgeIndex): Precomputed edge index
- `classifications` (list[dict]): Vertex classifications for corner metadata

**Returns**:

- `bool`: True if all four edges are inside polygon, False otherwise

**Example**:

```python
is_valid = validate_rectangle((2, 3), (9, 5), edge_index, classifications)
assert is_valid == True  # Rectangle with area 24 from test case
```

**Contract**:

- MUST cast rays for all four rectangle edges
- MUST use edge-only validation (no interior scanning)
- MUST return True only if ALL edges are inside

---

### `calculate_rectangle_area(corner1: tuple[int, int], corner2: tuple[int, int]) -> int`

**Purpose**: Calculate rectangle area from opposite corners

**Parameters**:

- `corner1` (tuple[int, int]): First corner
- `corner2` (tuple[int, int]): Opposite corner

**Returns**:

- `int`: Area including corners (width × height)

**Example**:

```python
area = calculate_rectangle_area((2, 3), (9, 5))
assert area == (9 - 2 + 1) * (5 - 3 + 1)  # 8 * 3 = 24
```

**Contract**:

- MUST include corners in calculation (inclusive bounds)
- MUST return positive integer

---

### `find_maximum_rectangle(vertices: list[tuple[int, int]]) -> int`

**Purpose**: Find maximum area among all valid rectangles

**Parameters**:

- `vertices` (list[tuple[int, int]]): List of red tile positions

**Returns**:

- `int`: Maximum area of valid rectangles

**Raises**:

- `ValueError`: If no valid rectangles exist

**Example**:

```python
vertices = [(7,1), (11,1), (11,7), (9,7), (9,5), (2,5), (2,3), (7,3)]
max_area = find_maximum_rectangle(vertices)
assert max_area == 24
```

**Contract**:

- MUST validate all rectangle pairs
- MUST calculate areas only for valid rectangles
- MUST return maximum area

---

## Utility Functions

### `filter_zero_width_segments(segments: list[tuple[int, int, str]]) -> list[tuple[int, int, str]]`

**Purpose**: Remove zero-width "outside" segments from consecutive crossings

**Parameters**:

- `segments` (list[tuple[int, int, str]]): Raw segment list

**Returns**:

- `list[tuple[int, int, str]]`: Filtered segment list

**Example**:

```python
segments = [(0, 2, "inside"), (2, 2, "outside"), (2, 5, "inside")]
filtered = filter_zero_width_segments(segments)
assert filtered == [(0, 2, "inside"), (2, 5, "inside")]
```

**Contract**:

- MUST remove only "outside" segments where start == end
- MUST preserve all "inside" segments
- MUST preserve segment order

---

## Error Handling

### Expected Exceptions

| Function                  | Exception    | Condition                                          |
| ------------------------- | ------------ | -------------------------------------------------- |
| `parse_coordinates`       | `ValueError` | Malformed input, negative coordinates, empty input |
| `validate_axis_alignment` | `ValueError` | Non-axis-aligned consecutive vertices              |
| `solve_part2`             | `ValueError` | Any parsing or validation error                    |
| `find_maximum_rectangle`  | `ValueError` | No valid rectangles found                          |

### Error Messages

- **Parsing**: `"Invalid coordinate format: expected 'x,y', got '{line}'"`
- **Axis alignment**: `"Vertices {v1} and {v2} are not axis-aligned"`
- **Empty input**: `"Input cannot be empty"`
- **No valid rectangles**: `"No valid rectangles found in polygon"`

---

## Testing Requirements

Each function MUST have:

- ✅ Happy path test with example input
- ✅ Edge case tests (empty, minimal, maximal inputs)
- ✅ Error condition tests (invalid inputs)
- ✅ Integration test with full solve_part2 function

---

**Status**: ✅ API Contracts Complete  
**Next**: Generate quickstart.md for implementation guide
