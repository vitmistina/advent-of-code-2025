# Quickstart: Day 9 Part 2 Implementation Guide

**Feature**: Day 9 Part 2 - Largest Red-Green Rectangle  
**Date**: December 11, 2025  
**Purpose**: Step-by-step implementation guide following TDD principles

---

## Overview

This guide walks through implementing the optimized ray tracing solution for Day 9 Part 2 using **strict TDD** (Red-Green-Refactor). The implementation will be in `day-09/solution_part2.py` with tests in `day-09/test_solution_part2.py`.

**Key Strategy**: Build from bottom up - parsing → winding → classification → edges → rays → validation → integration.

---

## Prerequisites

✅ **Research Complete**: See `research.md` for algorithmic decisions  
✅ **Data Model Complete**: See `data-model.md` for entities  
✅ **API Contracts Complete**: See `contracts/api.md` for signatures  
✅ **Constitution Compliance**: All principles verified in `plan.md`

---

## File Structure

```
day-09/
├── solution.py              # Part 1 (already exists)
├── solution_part2.py        # Part 2 (NEW - create this)
├── test_solution.py         # Part 1 tests (already exists)
├── test_solution_part2.py   # Part 2 tests (NEW - create this)
├── input.txt                # Actual puzzle input (already exists)
├── test_input.txt           # Example input (already exists)
└── description.md           # Challenge description (already exists)
```

---

## Implementation Phases (TDD)

### Phase 1: Parsing & Validation (User Story 1 - Part A)

#### RED: Write Failing Tests First

Create `day-09/test_solution_part2.py`:

```python
"""Tests for Day 9 Part 2: Optimized ray tracing."""

import pytest
from day_09.solution_part2 import parse_coordinates, validate_axis_alignment


def test_parse_coordinates_valid():
    """Test parsing valid coordinate input."""
    input_data = "7,1\n11,1\n11,7"
    result = parse_coordinates(input_data)
    assert result == [(7, 1), (11, 1), (11, 7)]


def test_parse_coordinates_with_whitespace():
    """Test parsing handles whitespace."""
    input_data = " 7, 1 \n 11,1\n11, 7 "
    result = parse_coordinates(input_data)
    assert result == [(7, 1), (11, 1), (11, 7)]


def test_parse_coordinates_empty_input():
    """Test parsing rejects empty input."""
    with pytest.raises(ValueError, match="empty"):
        parse_coordinates("")


def test_validate_axis_alignment_valid():
    """Test axis-aligned vertices pass validation."""
    vertices = [(7, 1), (11, 1), (11, 7)]  # Horizontal then vertical
    validate_axis_alignment(vertices)  # Should not raise


def test_validate_axis_alignment_invalid():
    """Test diagonal vertices fail validation."""
    vertices = [(0, 0), (3, 4)]  # Diagonal
    with pytest.raises(ValueError, match="not axis-aligned"):
        validate_axis_alignment(vertices)
```

**Run tests**: `uv run pytest day-09/test_solution_part2.py`  
**Expected**: All tests FAIL (functions don't exist yet) ✅ RED

#### GREEN: Implement Minimal Code

Create `day-09/solution_part2.py`:

```python
"""
Advent of Code 2025 - Day 09 Part 2: Optimized Ray Tracing.

Implements efficient rectangle validation using precomputed edge sets
and ray casting with coordinate filtering.
"""

from typing import Tuple

Coordinate = Tuple[int, int]


def parse_coordinates(input_data: str) -> list[Coordinate]:
    """
    Parse raw input into list of (x, y) coordinates.

    Args:
        input_data: Multi-line string with "x,y" format

    Returns:
        List of (x, y) tuples in order

    Raises:
        ValueError: If input is empty or malformed
    """
    if not input_data.strip():
        raise ValueError("Input cannot be empty")

    coordinates = []
    for i, line in enumerate(input_data.strip().split('\n'), 1):
        line = line.strip()
        if not line:
            raise ValueError(f"Line {i} is empty")

        parts = line.split(',')
        if len(parts) != 2:
            raise ValueError(f"Invalid format at line {i}: expected 'x,y', got '{line}'")

        try:
            x = int(parts[0].strip())
            y = int(parts[1].strip())
        except ValueError:
            raise ValueError(f"Non-integer coordinates at line {i}: '{line}'")

        if x < 0 or y < 0:
            raise ValueError(f"Negative coordinates at line {i}: ({x}, {y})")

        coordinates.append((x, y))

    return coordinates


def validate_axis_alignment(vertices: list[Coordinate]) -> None:
    """
    Validate that consecutive vertices are axis-aligned.

    Args:
        vertices: Ordered vertex list

    Raises:
        ValueError: If any consecutive pair is not axis-aligned
    """
    n = len(vertices)
    for i in range(n):
        v1 = vertices[i]
        v2 = vertices[(i + 1) % n]  # Wraparound

        same_x = v1[0] == v2[0]
        same_y = v1[1] == v2[1]

        if not (same_x or same_y):
            raise ValueError(f"Vertices {v1} and {v2} are not axis-aligned")
```

**Run tests**: `uv run pytest day-09/test_solution_part2.py`  
**Expected**: All tests PASS ✅ GREEN

#### REFACTOR: Clean up

- Add docstring examples
- Extract validation helpers if needed
- Run tests again to ensure still GREEN

---

### Phase 2: Winding Detection (User Story 1 - Part B)

#### RED: Write Failing Tests

Add to `test_solution_part2.py`:

```python
from day_09.solution_part2 import compute_signed_area, is_clockwise


def test_compute_signed_area_clockwise():
    """Test signed area for clockwise polygon."""
    # Square traced clockwise in screen coordinates
    vertices = [(0, 0), (0, 3), (4, 3), (4, 0)]
    area = compute_signed_area(vertices)
    assert area < 0  # Negative for clockwise in screen coords


def test_compute_signed_area_ccw():
    """Test signed area for counter-clockwise polygon."""
    vertices = [(0, 0), (4, 0), (4, 3), (0, 3)]
    area = compute_signed_area(vertices)
    assert area > 0  # Positive for CCW in screen coords


def test_is_clockwise_example():
    """Test winding detection with Day 9 Part 2 example."""
    vertices = [
        (7, 1), (11, 1), (11, 7), (9, 7),
        (9, 5), (2, 5), (2, 3), (7, 3)
    ]
    assert is_clockwise(vertices) == True
```

**Run**: `uv run pytest day-09/test_solution_part2.py -k winding`  
**Expected**: FAIL ✅ RED

#### GREEN: Implement

Add to `solution_part2.py`:

```python
def compute_signed_area(vertices: list[Coordinate]) -> float:
    """
    Compute signed area using shoelace formula.

    For screen coordinates (Y-down):
    - Negative area = clockwise
    - Positive area = counter-clockwise

    Args:
        vertices: Ordered vertex list

    Returns:
        Signed area (negative for clockwise)
    """
    area = 0.0
    n = len(vertices)

    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]  # Wraparound
        area += x1 * y2 - x2 * y1

    return area / 2.0


def is_clockwise(vertices: list[Coordinate]) -> bool:
    """
    Check if vertices are ordered clockwise in screen coordinates.

    Args:
        vertices: Ordered vertex list

    Returns:
        True if clockwise (negative signed area)
    """
    return compute_signed_area(vertices) < 0
```

**Run**: `uv run pytest day-09/test_solution_part2.py -k winding`  
**Expected**: PASS ✅ GREEN

---

### Phase 3: Turn Classification (User Story 1 - Part C)

#### RED: Write Failing Tests

```python
from day_09.solution_part2 import compute_direction_vector, classify_turn, classify_all_vertices


def test_compute_direction_vector():
    """Test direction vector computation."""
    assert compute_direction_vector((7, 3), (7, 1)) == (0, -1)  # Up
    assert compute_direction_vector((7, 1), (11, 1)) == (1, 0)  # Right


def test_classify_turn_convex():
    """Test convex turn classification."""
    # Clockwise polygon: Up -> Right is convex (right turn)
    incoming = (0, -1)
    outgoing = (1, 0)
    assert classify_turn(incoming, outgoing, is_clockwise=True) == "convex"


def test_classify_turn_concave():
    """Test concave turn classification."""
    # Clockwise polygon: Left -> Up is concave (left turn)
    incoming = (-1, 0)
    outgoing = (0, -1)
    assert classify_turn(incoming, outgoing, is_clockwise=True) == "concave"


def test_classify_all_vertices_example():
    """Test full vertex classification with example."""
    vertices = [(7, 1), (11, 1), (11, 7), (9, 7), (9, 5), (2, 5), (2, 3), (7, 3)]
    classifications = classify_all_vertices(vertices)

    assert len(classifications) == 8
    assert classifications[0]['classification'] == "convex"  # (7,1)
    assert classifications[4]['classification'] == "concave"  # (9,5)
    assert classifications[7]['classification'] == "concave"  # (7,3)
```

**Run**: `uv run pytest day-09/test_solution_part2.py -k classify`  
**Expected**: FAIL ✅ RED

#### GREEN: Implement

```python
def compute_direction_vector(from_vertex: Coordinate, to_vertex: Coordinate) -> Coordinate:
    """Compute unit direction vector between vertices."""
    dx = to_vertex[0] - from_vertex[0]
    dy = to_vertex[1] - from_vertex[1]

    if dx != 0:
        dx = dx // abs(dx)
    if dy != 0:
        dy = dy // abs(dy)

    return (dx, dy)


def classify_turn(incoming: Coordinate, outgoing: Coordinate, is_clockwise: bool) -> str:
    """Classify turn as convex or concave based on winding."""
    cross = incoming[0] * outgoing[1] - incoming[1] * outgoing[0]

    if is_clockwise:
        return "convex" if cross < 0 else "concave"
    else:
        return "convex" if cross > 0 else "concave"


def classify_all_vertices(vertices: list[Coordinate]) -> list[dict]:
    """Classify all vertices with wraparound handling."""
    n = len(vertices)
    is_cw = is_clockwise(vertices)

    classifications = []
    for i in range(n):
        prev = vertices[(i - 1) % n]
        current = vertices[i]
        next_v = vertices[(i + 1) % n]

        incoming = compute_direction_vector(prev, current)
        outgoing = compute_direction_vector(current, next_v)
        turn_type = classify_turn(incoming, outgoing, is_cw)

        classifications.append({
            'vertex': current,
            'index': i,
            'incoming': incoming,
            'outgoing': outgoing,
            'classification': turn_type
        })

    return classifications
```

**Run**: `uv run pytest day-09/test_solution_part2.py -k classify`  
**Expected**: PASS ✅ GREEN

---

### Phase 4: Edge Index (User Story 2)

#### RED: Write Failing Tests

```python
from day_09.solution_part2 import EdgeIndex


def test_edge_index_horizontal_edges():
    """Test horizontal edge indexing."""
    vertices = [(7, 1), (11, 1), (11, 7)]
    index = EdgeIndex(vertices)

    edges_at_y1 = index.get_edges_at_y(1)
    assert 8 in edges_at_y1
    assert 9 in edges_at_y1
    assert 10 in edges_at_y1


def test_edge_index_vertical_edges():
    """Test vertical edge indexing."""
    vertices = [(11, 1), (11, 7), (9, 7)]
    index = EdgeIndex(vertices)

    edges_at_x11 = index.get_edges_at_x(11)
    assert 2 in edges_at_x11
    assert 6 in edges_at_x11
```

**Run**: `uv run pytest day-09/test_solution_part2.py -k edge_index`  
**Expected**: FAIL ✅ RED

#### GREEN: Implement

```python
class EdgeIndex:
    """Precomputed edge index for efficient ray casting."""

    def __init__(self, vertices: list[Coordinate]):
        self.horizontal_edges: dict[int, list[int]] = {}
        self.vertical_edges: dict[int, list[int]] = {}
        self._build_index(vertices)

    def _build_index(self, vertices: list[Coordinate]):
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

    def get_edges_at_x(self, x: int) -> list[int]:
        """Get vertical edge y-positions at given x."""
        return sorted(self.vertical_edges.get(x, []))

    def get_edges_at_y(self, y: int) -> list[int]:
        """Get horizontal edge x-positions at given y."""
        return sorted(self.horizontal_edges.get(y, []))
```

**Run**: `uv run pytest day-09/test_solution_part2.py -k edge_index`  
**Expected**: PASS ✅ GREEN

---

### Phase 5: Ray Casting (User Story 3)

#### RED: Write Failing Tests

```python
from day_09.solution_part2 import generate_ray_segments, filter_zero_width_segments


def test_generate_ray_segments_no_crossings():
    """Test ray with no edge crossings."""
    segments = generate_ray_segments(0, 10, [], "inside")
    assert segments == [(0, 10, "inside")]


def test_generate_ray_segments_with_crossings():
    """Test ray with edge crossings."""
    segments = generate_ray_segments(0, 10, [3, 7], "inside")
    assert segments == [(0, 3, "inside"), (3, 7, "outside"), (7, 10, "inside")]


def test_filter_zero_width_segments():
    """Test filtering zero-width outside segments."""
    segments = [(0, 2, "inside"), (2, 2, "outside"), (2, 5, "inside")]
    filtered = filter_zero_width_segments(segments)
    assert filtered == [(0, 2, "inside"), (2, 5, "inside")]
```

**Run**: `uv run pytest day-09/test_solution_part2.py -k ray`  
**Expected**: FAIL ✅ RED

#### GREEN: Implement

```python
def generate_ray_segments(
    ray_start: int,
    ray_end: int,
    edge_positions: list[int],
    initial_state: str = "inside"
) -> list[tuple[int, int, str]]:
    """Generate segments along ray based on edge crossings."""
    if not edge_positions:
        return [(ray_start, ray_end, initial_state)]

    segments = []
    state = initial_state
    current_pos = ray_start

    for edge_pos in sorted(edge_positions):
        if edge_pos <= ray_start or edge_pos >= ray_end:
            continue

        if current_pos < edge_pos:
            segments.append((current_pos, edge_pos, state))

        state = "outside" if state == "inside" else "inside"
        current_pos = edge_pos

    if current_pos < ray_end:
        segments.append((current_pos, ray_end, state))

    return filter_zero_width_segments(segments)


def filter_zero_width_segments(segments: list[tuple]) -> list[tuple]:
    """Remove zero-width 'outside' segments."""
    return [
        (start, end, state)
        for start, end, state in segments
        if not (state == "outside" and start == end)
    ]
```

**Run**: `uv run pytest day-09/test_solution_part2.py -k ray`  
**Expected**: PASS ✅ GREEN

---

### Phase 6: Rectangle Validation (User Story 4)

#### RED: Write Failing Tests

```python
from day_09.solution_part2 import validate_rectangle_edge, calculate_rectangle_area


def test_validate_rectangle_edge_inside():
    """Test edge entirely inside."""
    segments = [(0, 10, "inside")]
    assert validate_rectangle_edge(2, 8, segments) == True


def test_validate_rectangle_edge_outside():
    """Test edge overlaps outside segment."""
    segments = [(0, 5, "inside"), (5, 8, "outside"), (8, 10, "inside")]
    assert validate_rectangle_edge(6, 7, segments) == False


def test_calculate_rectangle_area():
    """Test area calculation."""
    area = calculate_rectangle_area((2, 3), (9, 5))
    assert area == (9 - 2 + 1) * (5 - 3 + 1)  # 8 * 3 = 24
```

**Run**: `uv run pytest day-09/test_solution_part2.py -k rectangle`  
**Expected**: FAIL ✅ RED

#### GREEN: Implement

```python
def validate_rectangle_edge(
    edge_start: int,
    edge_end: int,
    segments: list[tuple[int, int, str]]
) -> bool:
    """Check if rectangle edge overlaps any 'outside' segment."""
    for seg_start, seg_end, state in segments:
        if state == "outside":
            # Check for overlap
            if not (edge_end <= seg_start or edge_start >= seg_end):
                return False
    return True


def calculate_rectangle_area(corner1: Coordinate, corner2: Coordinate) -> int:
    """Calculate rectangle area including corners."""
    width = abs(corner2[0] - corner1[0]) + 1
    height = abs(corner2[1] - corner1[1]) + 1
    return width * height
```

**Run**: `uv run pytest day-09/test_solution_part2.py -k rectangle`  
**Expected**: PASS ✅ GREEN

---

### Phase 7: Integration (User Story 5)

#### RED: Write Failing Integration Test

```python
from day_09.solution_part2 import solve_part2


def test_solve_part2_example():
    """Test complete solution with example input."""
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

**Run**: `uv run pytest day-09/test_solution_part2.py -k solve`  
**Expected**: FAIL ✅ RED

#### GREEN: Implement Main Function

```python
def solve_part2(input_data: str) -> int:
    """
    Solve Day 9 Part 2: Find largest rectangle using optimized ray tracing.

    Args:
        input_data: Raw puzzle input with "x,y" coordinates

    Returns:
        Maximum area of valid rectangles
    """
    # Parse and validate
    vertices = parse_coordinates(input_data)
    validate_axis_alignment(vertices)

    # Classify vertices
    classifications = classify_all_vertices(vertices)

    # Build edge index
    edge_index = EdgeIndex(vertices)

    # Find maximum rectangle
    max_area = 0

    # Enumerate all rectangle pairs
    from itertools import combinations
    for corner1, corner2 in combinations(vertices, 2):
        # Ensure corner1 is top-left, corner2 is bottom-right
        min_x, max_x = min(corner1[0], corner2[0]), max(corner1[0], corner2[0])
        min_y, max_y = min(corner1[1], corner2[1]), max(corner1[1], corner2[1])

        if min_x == max_x or min_y == max_y:
            continue  # Skip degenerate rectangles

        # Validate rectangle (simplified for now - full ray casting needed)
        # TODO: Implement full 4-ray validation
        area = calculate_rectangle_area((min_x, min_y), (max_x, max_y))
        max_area = max(max_area, area)

    return max_area
```

**Run**: `uv run pytest day-09/test_solution_part2.py -k solve`  
**Expected**: FAIL (needs full ray casting logic) ✅ RED

#### GREEN: Complete Ray Casting Implementation

Add full validation logic with 4 rays per rectangle. See `research.md` for complete algorithm.

**Run**: `uv run pytest day-09/test_solution_part2.py`  
**Expected**: All tests PASS ✅ GREEN

---

## Running the Solution

### On Example Input

```bash
uv run day-09/solution_part2.py < day-09/test_input.txt
```

**Expected output**: `24`

### On Actual Input

```bash
uv run day-09/solution_part2.py < day-09/input.txt
```

**Expected output**: [Actual answer - submit to AoC]

---

## Validation Checklist

- [ ] All tests pass: `uv run pytest day-09/test_solution_part2.py -v`
- [ ] Example input produces correct answer (24)
- [ ] Actual input runs in < 10 seconds
- [ ] Code follows PEP8: `uv run ruff check day-09/solution_part2.py`
- [ ] All functions have docstrings
- [ ] Type hints present on all functions
- [ ] README.md updated with progress

---

## Troubleshooting

### Common Issues

**Issue**: Tests fail with import errors  
**Fix**: Ensure `__init__.py` exists in `day-09/` folder

**Issue**: Ray segments have gaps  
**Fix**: Check wraparound logic in segment generation

**Issue**: Wrong area for example  
**Fix**: Verify area calculation includes corners (width+1, height+1)

**Issue**: Performance too slow  
**Fix**: Ensure EdgeIndex is using coordinate filtering, not iterating all edges

---

## Next Steps

After implementation:

1. Run full test suite: `uv run pytest day-09/`
2. Run solution on actual input
3. Submit answer to Advent of Code
4. Update main README.md with completion status
5. Commit with message: `feat: solve day 09 part 2 - optimized ray tracing`

---

**Status**: ✅ Quickstart Complete  
**Ready for**: TDD implementation following this guide
