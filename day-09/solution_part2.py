"""
Advent of Code 2025 - Day 09 Part 2: Optimized Ray Tracing.

Implements efficient rectangle validation using precomputed edge sets
and ray casting with coordinate filtering.

This solution finds the largest rectangle formed by red and green tiles
using an optimized ray tracing approach:
1. Parse red tile coordinates and classify turns (convex/concave)
2. Precompute green edge tiles into horizontal/vertical sets
3. Use ray casting with edge filtering to validate rectangles
4. Find maximum area among valid rectangles

Key optimization: Filter edges by coordinate (x or y) to avoid scanning
every grid position, enabling O(edges) instead of O(grid_size²).
"""

Coordinate = tuple[int, int]


# ============================================================================
# Phase 2: User Story 1 - Part A: Parsing & Validation
# ============================================================================


def parse_coordinates(input_data: str) -> list[Coordinate]:
    """
    Parse raw input into list of (x, y) coordinates.

    Args:
        input_data: Multi-line string with "x,y" format

    Returns:
        List of (x, y) tuples in order

    Raises:
        ValueError: If input is empty or malformed

    Example:
        >>> parse_coordinates("7,1\\n11,1\\n11,7")
        [(7, 1), (11, 1), (11, 7)]
    """
    if not input_data.strip():
        raise ValueError("Input cannot be empty")

    coordinates = []
    for i, line in enumerate(input_data.strip().split("\n"), 1):
        line = line.strip()
        if not line:
            raise ValueError(f"Line {i} is empty")

        parts = line.split(",")
        if len(parts) != 2:
            raise ValueError(f"Invalid format at line {i}: expected 'x,y', got '{line}'")

        try:
            x = int(parts[0].strip())
            y = int(parts[1].strip())
        except ValueError as e:
            raise ValueError(f"Non-integer coordinates at line {i}: '{line}'") from e

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

    Example:
        >>> validate_axis_alignment([(0, 0), (5, 0), (5, 5)])  # OK
        >>> validate_axis_alignment([(0, 0), (3, 4)])  # Raises ValueError
    """
    n = len(vertices)
    for i in range(n):
        v1 = vertices[i]
        v2 = vertices[(i + 1) % n]  # Wraparound

        same_x = v1[0] == v2[0]
        same_y = v1[1] == v2[1]

        if not (same_x or same_y):
            raise ValueError(f"Vertices {v1} and {v2} are not axis-aligned")


# ============================================================================
# Phase 2: User Story 1 - Part B: Winding Detection
# ============================================================================


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

    Example:
        >>> compute_signed_area([(0, 0), (4, 0), (4, 3), (0, 3)])
        12.0  # Positive for CCW
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

    Example:
        >>> is_clockwise([(0, 0), (0, 3), (4, 3), (4, 0)])
        True  # Clockwise in screen coords
    """
    return compute_signed_area(vertices) < 0


# ============================================================================
# Phase 2: User Story 1 - Part C: Turn Classification
# ============================================================================


def compute_direction_vector(from_vertex: Coordinate, to_vertex: Coordinate) -> Coordinate:
    """
    Compute unit direction vector between vertices.

    Args:
        from_vertex: Starting vertex
        to_vertex: Ending vertex

    Returns:
        Unit direction vector, one of: (0, ±1), (±1, 0)

    Example:
        >>> compute_direction_vector((7, 3), (7, 1))
        (0, -1)  # Up
        >>> compute_direction_vector((7, 1), (11, 1))
        (1, 0)  # Right
    """
    dx = to_vertex[0] - from_vertex[0]
    dy = to_vertex[1] - from_vertex[1]

    if dx != 0:
        dx = dx // abs(dx)
    if dy != 0:
        dy = dy // abs(dy)

    return (dx, dy)


def classify_turn(incoming: Coordinate, outgoing: Coordinate, is_clockwise: bool) -> str:
    """
    Classify turn as convex or concave based on winding.

    Args:
        incoming: Incoming direction vector
        outgoing: Outgoing direction vector
        is_clockwise: Whether polygon is clockwise

    Returns:
        "convex" or "concave"

    Example:
        >>> classify_turn((1, 0), (0, 1), is_clockwise=False)
        'convex'  # Right turn in CCW polygon
    """
    cross = incoming[0] * outgoing[1] - incoming[1] * outgoing[0]

    if is_clockwise:
        return "convex" if cross < 0 else "concave"
    else:
        return "convex" if cross > 0 else "concave"


def classify_all_vertices(vertices: list[Coordinate]) -> list[dict]:
    """
    Classify all vertices with wraparound handling.

    Args:
        vertices: Ordered vertex list

    Returns:
        List of dicts with vertex info and classification

    Example:
        >>> classify_all_vertices([(0, 0), (4, 0), (4, 3), (0, 3)])
        [{'vertex': (0, 0), 'index': 0, 'classification': 'convex', ...}, ...]
    """
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

        classifications.append(
            {
                "vertex": current,
                "index": i,
                "incoming": incoming,
                "outgoing": outgoing,
                "classification": turn_type,
            }
        )

    return classifications


# ============================================================================
# Phase 3: User Story 2 - Edge Index
# ============================================================================


class EdgeIndex:
    """Precomputed edge index for efficient ray casting."""

    def __init__(self, vertices: list[Coordinate]):
        """
        Initialize edge index with vertex list.

        Args:
            vertices: Ordered vertex list
        """
        # Map from y -> list of x-coordinates of vertical edges at that y
        self.vertical_edges_at_y: dict[int, set[int]] = {}
        # Map from x -> list of y-coordinates of horizontal edges at that x
        self.horizontal_edges_at_x: dict[int, set[int]] = {}
        self._build_index(vertices)

    def _build_index(self, vertices: list[Coordinate]):
        """
        Build coordinate-indexed edge sets.

        Args:
            vertices: Ordered vertex list
        """
        n = len(vertices)

        for i in range(n):
            v1 = vertices[i]
            v2 = vertices[(i + 1) % n]

            if v1[1] == v2[1]:  # Horizontal edge
                y = v1[1]
                x_min, x_max = min(v1[0], v2[0]), max(v1[0], v2[0])
                # Store all x-coordinates along this horizontal edge (excluding corners)
                for x in range(x_min + 1, x_max):
                    if x not in self.horizontal_edges_at_x:
                        self.horizontal_edges_at_x[x] = set()
                    self.horizontal_edges_at_x[x].add(y)

            elif v1[0] == v2[0]:  # Vertical edge
                x = v1[0]
                y_min, y_max = min(v1[1], v2[1]), max(v1[1], v2[1])
                # Store all y-coordinates along this vertical edge (excluding corners)
                for y in range(y_min + 1, y_max):
                    if y not in self.vertical_edges_at_y:
                        self.vertical_edges_at_y[y] = set()
                    self.vertical_edges_at_y[y].add(x)

    def get_edges_at_x(self, x: int) -> list[int]:
        """
        Get horizontal edge y-positions at given x.

        Args:
            x: X-coordinate

        Returns:
            Sorted list of y-positions where horizontal edges exist
        """
        return sorted(self.horizontal_edges_at_x.get(x, []))

    def get_edges_at_y(self, y: int) -> list[int]:
        """
        Get vertical edge x-positions at given y.

        Args:
            y: Y-coordinate

        Returns:
            Sorted list of x-positions where vertical edges exist
        """
        return sorted(self.vertical_edges_at_y.get(y, []))


# ============================================================================
# Phase 4A: Classification Filter
# ============================================================================


def filter_convex_classifications_at(
    classifications: list[dict], axis: str, coordinate: int
) -> list[int]:
    """
    Filter convex vertices at a specific coordinate on an axis.

    For vertices on a given axis line, returns the coordinates
    perpendicular to that axis for only the convex vertices.

    Args:
        classifications: List of vertex classification dicts
        axis: "x" or "y" - the axis to filter by
        coordinate: The coordinate value on that axis

    Returns:
        Sorted list of perpendicular coordinates for convex vertices

    Example:
        >>> vertices = [(7, 1), (11, 1), (11, 7), (9, 7), (9, 5), (2, 5), (2, 3), (7, 3)]
        >>> classifications = classify_all_vertices(vertices)
        >>> filter_convex_classifications_at(classifications, "y", 1)
        [7, 11]  # Convex vertices on line y=1
    """
    result = []

    for vc in classifications:
        vertex = vc.get("vertex")
        classification = vc.get("classification")

        if vertex is None or classification is None:
            continue

        # Check if vertex is on the specified axis line
        if axis == "y" and vertex[1] == coordinate and classification == "convex":
            result.append(vertex[0])  # Return x-coordinate
        if axis == "x" and vertex[0] == coordinate and classification == "convex":
            result.append(vertex[1])  # Return y-coordinate
    return sorted(result)


# ============================================================================
# Phase 4: User Story 3 - Ray Segment Generation
# ============================================================================


def generate_ray_segments(
    ray_start: int,
    ray_end: int,
    edge_positions: list[int],
    initial_state: str = "inside",
    convex_corners: list[int] = None,
) -> list[tuple[int, int, str]]:
    """
    Generate segments along ray based on edge crossings.

    Args:
        ray_start: Starting coordinate
        ray_end: Ending coordinate
        edge_positions: List of edge crossing positions
        initial_state: Starting state ("inside" or "outside")
        convex_corners: Optional list of filtered convex corner coordinates

    Returns:
        List of (start, end, state) tuples

    Example:
        >>> generate_ray_segments(0, 10, [3, 7], "inside")
        [(0, 3, 'inside'), (3, 7, 'outside'), (7, 10, 'inside')]
    """
    # Determine if ray is reversed (going backwards)
    is_reversed = ray_start > ray_end
    ray_min = min(ray_start, ray_end)
    ray_max = max(ray_start, ray_end)

    # Merge edge positions with convex corner positions
    all_positions = list(edge_positions) if edge_positions else []

    if convex_corners:
        all_positions.extend(convex_corners)

    if not all_positions:
        return [(ray_start, ray_end, initial_state)]

    segments = []
    state = initial_state
    current_pos = ray_start

    for edge_pos in sorted(all_positions):
        if edge_pos <= ray_min or edge_pos >= ray_max:
            continue

        if not is_reversed:
            # Forward ray: current_pos < edge_pos
            if current_pos < edge_pos:
                segments.append((current_pos, edge_pos, state))
                state = "outside" if state == "inside" else "inside"
                current_pos = edge_pos
        else:
            # Reversed ray: current_pos > edge_pos
            if current_pos > edge_pos:
                segments.append((current_pos, edge_pos, state))
                state = "outside" if state == "inside" else "inside"
                current_pos = edge_pos

    if not is_reversed:
        if current_pos < ray_end:
            segments.append((current_pos, ray_end, state))
    else:
        if current_pos > ray_end:
            segments.append((current_pos, ray_end, state))

    return filter_zero_width_segments(segments)


def filter_zero_width_segments(segments: list[tuple]) -> list[tuple]:
    """
    Remove zero-width 'outside' segments.

    Args:
        segments: List of (start, end, state) tuples

    Returns:
        Filtered list with zero-width outside segments removed

    Example:
        >>> filter_zero_width_segments([(0, 2, 'inside'), (2, 2, 'outside'), (2, 5, 'inside')])
        [(0, 2, 'inside'), (2, 5, 'inside')]
    """
    return [
        (start, end, state)
        for start, end, state in segments
        if not (state == "outside" and start == end)
    ]


def determine_initial_ray_state(vertex_classification: dict, direction: tuple[int, int]) -> str:
    """
    Determine initial state of ray based on vertex and ray direction.

    For a ray starting at a vertex:
    - At a convex vertex, the ray stays in its current state
    - At a concave vertex, the ray changes state (inside <-> outside)

    Args:
        vertex_classification: Dict with classification data or bool for simplified mode
        direction: Ray direction (dx, dy). Required if vertex_classification is dict

    Returns:
        "inside" or "outside"

    Example:
         vc = {'classification': 'convex', 'outgoing': (1, 0)}
         determine_initial_ray_state(vc, (1, 0))
        'inside'
    """

    # Non-simplified version: use vertex classification and direction
    if direction is None:
        raise ValueError("direction required when vertex_classification is a dict")

    classification = vertex_classification.get("classification")
    outgoing = vertex_classification.get("outgoing")
    incoming = vertex_classification.get("incoming")
    opposite_incoming = (-incoming[0], -incoming[1])

    if classification is None or outgoing is None:
        raise ValueError("vertex_classification must contain 'classification' and 'outgoing'")

    # At a convex vertex, ray continues straight (no state change)
    # At a concave vertex, ray changes state (inside becomes outside, outside becomes inside)
    if classification == "convex":
        if direction in (opposite_incoming, outgoing):
            # Ray aligns with polygon boundary at convex vertex - starts inside
            return "inside"
        else:
            # Ray goes away from polygon at convex vertex - starts outside
            return "outside"
    else:  # concave
        # At concave vertex, ray always continues to the inner green tiles - starts inside
        return "inside"


# ============================================================================
# Phase 5: User Story 4 - Rectangle Validation
# ============================================================================


def validate_rectangle_edge(
    edge_start: int, edge_end: int, segments: list[tuple[int, int, str]]
) -> bool:
    """
    Check if rectangle edge overlaps any 'outside' segment.

    Args:
        edge_start: Start coordinate of edge
        edge_end: End coordinate of edge
        segments: List of (start, end, state) tuples

    Returns:
        True if edge is valid (no outside overlap), False otherwise

    Example:
        >>> validate_rectangle_edge(2, 8, [(0, 10, 'inside')])
        True
        >>> validate_rectangle_edge(6, 7, [(0, 5, 'inside'), (5, 8, 'outside')])
        False
    """
    # Normalize edge coordinates (handle reversed order)
    norm_edge_start = min(edge_start, edge_end)
    norm_edge_end = max(edge_start, edge_end)

    for seg_start, seg_end, state in segments:
        if state == "outside":
            # Normalize segment coordinates (handle reversed order)
            norm_seg_start = min(seg_start, seg_end)
            norm_seg_end = max(seg_start, seg_end)

            # Check for overlap
            if not (norm_edge_end < norm_seg_start or norm_edge_start > norm_seg_end):
                # Overlap detected
                return False
    return True


def calculate_rectangle_area(corner1: Coordinate, corner2: Coordinate) -> int:
    """
    Calculate rectangle area including corners.

    Args:
        corner1: First corner coordinate
        corner2: Second corner coordinate

    Returns:
        Rectangle area (inclusive of corners)

    Example:
        >>> calculate_rectangle_area((2, 3), (9, 5))
        24  # (9-2+1) * (5-3+1) = 8 * 3
    """
    width = abs(corner2[0] - corner1[0]) + 1
    height = abs(corner2[1] - corner1[1]) + 1
    return width * height


# ============================================================================
# Phase 6: User Story 5 - Integration & solve_part2
# ============================================================================


def solve_part2(input_data: str) -> int:
    """
    Solve Day 9 Part 2: Find largest rectangle using optimized ray tracing.

    Args:
        input_data: Raw puzzle input with "x,y" coordinates

    Returns:
        Maximum area of valid rectangles

    Example:
        >>> input_data = "7,1\\n11,1\\n11,7\\n9,7\\n9,5\\n2,5\\n2,3\\n7,3"
        >>> solve_part2(input_data)
        24
    """
    print("[Phase 1] Parsing grid and validating input...")
    # Parse and validate
    vertices = parse_coordinates(input_data)
    print(f"  ✓ Parsed {len(vertices)} vertices")
    validate_axis_alignment(vertices)
    print(f"  ✓ All {len(vertices)} vertices are axis-aligned")

    print("\n[Phase 2] Building edge index and classifying vertices...")
    # Build edge index
    edge_index = EdgeIndex(vertices)
    print(
        f"  ✓ Edge index built (horizontal_edges_at_x: {len(edge_index.horizontal_edges_at_x)}, vertical_edges_at_y: {len(edge_index.vertical_edges_at_y)})"
    )
    classifications = classify_all_vertices(vertices)
    convex_count = sum(1 for vc in classifications if vc["classification"] == "convex")
    concave_count = len(classifications) - convex_count
    print(f"  ✓ Classified vertices: {convex_count} convex, {concave_count} concave")

    print("\n[Phase 3] Enumerating and validating rectangles...")
    max_area = 0

    # Enumerate all possible rectangles
    from itertools import combinations

    rect_list = list(combinations(vertices, 2))

    # Pre-calculate areas and sort by descending area for early exit optimization
    rect_with_areas = []
    for corner1, corner2 in rect_list:
        x1, y1 = corner1
        x2, y2 = corner2
        min_x_rect = min(x1, x2)
        max_x_rect = max(x1, x2)
        min_y_rect = min(y1, y2)
        max_y_rect = max(y1, y2)

        # Skip degenerate rectangles
        if min_x_rect == max_x_rect or min_y_rect == max_y_rect:
            continue

        area = calculate_rectangle_area((min_x_rect, min_y_rect), (max_x_rect, max_y_rect))
        rect_with_areas.append((area, corner1, corner2))

    # Sort by area descending
    rect_with_areas.sort(key=lambda x: x[0], reverse=True)

    total_rectangles = len(rect_list)
    valid_rectangles = 0
    degenerate_rectangles = total_rectangles - len(rect_with_areas)
    rectangles_checked = 0

    for rect_idx, (area, corner1, corner2) in enumerate(rect_with_areas, 1):
        rectangles_checked += 1
        # Ensure corner1 is top-left, corner2 is bottom-right
        x1, y1 = corner1
        x2, y2 = corner2

        # Create normalized corners
        min_x_rect = min(x1, x2)
        max_x_rect = max(x1, x2)
        min_y_rect = min(y1, y2)
        max_y_rect = max(y1, y2)

        # Validation: Check if all points in the rectangle are inside or on the polygon
        # Use ray casting to determine if points are inside
        valid = True

        # Cast two half interval rays from each corner
        # (determine initial state from vertex classification)

        # Find the classifications for the corners
        corner1_class = None
        corner2_class = None
        for vc in classifications:
            if vc["vertex"] == corner1:
                corner1_class = vc
            if vc["vertex"] == corner2:
                corner2_class = vc

        if corner1_class is None or corner2_class is None:
            # Skip if corners are not vertices of the polygon
            valid = False
        else:
            # Determine ray directions based on which corner is which
            dx_sign = 1 if x2 > x1 else -1
            dy_sign = 1 if y2 > y1 else -1

            # Cast rays from corner1 towards corner2
            # Ray along x-axis (horizontal) at y1
            ray1_edges = edge_index.get_edges_at_y(y1)
            ray1_state = determine_initial_ray_state(corner1_class, (dx_sign, 0))
            ray1_convex = filter_convex_classifications_at(classifications, "y", y1)
            ray1_segments = generate_ray_segments(x1, x2, ray1_edges, ray1_state, ray1_convex)

            # Ray along y-axis (vertical) at x1
            ray2_edges = edge_index.get_edges_at_x(x1)
            ray2_state = determine_initial_ray_state(corner1_class, (0, dy_sign))
            ray2_convex = filter_convex_classifications_at(classifications, "x", x1)
            ray2_segments = generate_ray_segments(y1, y2, ray2_edges, ray2_state, ray2_convex)

            # Cast rays from corner2 towards corner1
            # Ray along x-axis (horizontal) at y2
            ray3_edges = edge_index.get_edges_at_y(y2)
            ray3_state = determine_initial_ray_state(corner2_class, (-dx_sign, 0))
            ray3_convex = filter_convex_classifications_at(classifications, "y", y2)
            ray3_segments = generate_ray_segments(x2, x1, ray3_edges, ray3_state, ray3_convex)

            # Ray along y-axis (vertical) at x2
            ray4_edges = edge_index.get_edges_at_x(x2)
            ray4_state = determine_initial_ray_state(corner2_class, (0, -dy_sign))
            ray4_convex = filter_convex_classifications_at(classifications, "x", x2)
            ray4_segments = generate_ray_segments(y2, y1, ray4_edges, ray4_state, ray4_convex)

            # Find overlap of rectangle edges with ray segments
            # (ITERATE OVER RAY SEGMENTS, DO NOT ITERATE OVER EDGE TILES)

            if area == 50:
                pass  # Debug breakpoint

            # Top edge: from (min_x_rect, min_y_rect) to (max_x_rect, min_y_rect)
            if valid and not validate_rectangle_edge(min_x_rect, max_x_rect, ray1_segments):
                valid = False

            # Left edge: from (min_x_rect, min_y_rect) to (min_x_rect, max_y_rect)
            if valid and not validate_rectangle_edge(min_y_rect, max_y_rect, ray2_segments):
                valid = False

            # Right edge: from (max_x_rect, min_y_rect) to (max_x_rect, max_y_rect)
            if valid and not validate_rectangle_edge(min_y_rect, max_y_rect, ray4_segments):
                valid = False

            # Bottom edge: from (min_x_rect, max_y_rect) to (max_x_rect, max_y_rect)
            if valid and not validate_rectangle_edge(min_x_rect, max_x_rect, ray3_segments):
                valid = False

        # If all edges are valid, calculate area
        if valid:
            valid_rectangles += 1
            print(
                f"  → Rectangle {rect_idx}/{len(rect_with_areas)}: VALID! area={area} at corners {corner1} and {corner2}"
            )
            max_area = area
            break  # Early exit on first valid rectangle (largest by area)

    print(f"\n[Phase 4] Results:")
    print(f"  • Total rectangle pairs checked: {total_rectangles}")
    print(f"  • Degenerate rectangles: {degenerate_rectangles}")
    print(f"  • Rectangles validated: {rectangles_checked}")
    print(f"  • Valid rectangles found: {valid_rectangles}")
    print(f"  • Maximum area found: {max_area}")
    return max_area


# ============================================================================
# CLI Entry Point
# ============================================================================


if __name__ == "__main__":
    import sys

    # Read from stdin or file
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            input_data = f.read()
    else:
        input_data = sys.stdin.read()

    result = solve_part2(input_data)
    print(result)
