"""Tests for Day 9 Part 2: Optimized ray tracing."""

import sys
from pathlib import Path

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from solution_part2 import classify_all_vertices, parse_coordinates, validate_axis_alignment

# ============================================================================
# Phase 2: User Story 1 - Part A: Parsing & Validation
# ============================================================================


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
    vertices = [(0, 0), (4, 0), (4, 3), (0, 3)]  # Rectangle - all edges axis-aligned
    validate_axis_alignment(vertices)  # Should not raise


def test_validate_axis_alignment_invalid():
    """Test diagonal vertices fail validation."""
    vertices = [(0, 0), (3, 4)]  # Diagonal
    with pytest.raises(ValueError, match="not axis-aligned"):
        validate_axis_alignment(vertices)


# ============================================================================
# Phase 2: User Story 1 - Part B: Winding Detection
# ============================================================================


def test_compute_signed_area_clockwise():
    """Test signed area for clockwise polygon."""
    # Square traced clockwise in screen coordinates
    vertices = [(0, 0), (0, 3), (4, 3), (4, 0)]
    from solution_part2 import compute_signed_area

    area = compute_signed_area(vertices)
    assert area < 0  # Negative for clockwise in screen coords


def test_compute_signed_area_ccw():
    """Test signed area for counter-clockwise polygon."""
    vertices = [(0, 0), (4, 0), (4, 3), (0, 3)]
    from solution_part2 import compute_signed_area

    area = compute_signed_area(vertices)
    assert area > 0  # Positive for CCW in screen coords


def test_is_clockwise_example():
    """Test winding detection with Day 9 Part 2 example."""
    vertices = [(7, 1), (11, 1), (11, 7), (9, 7), (9, 5), (2, 5), (2, 3), (7, 3)]
    from solution_part2 import is_clockwise

    # The example polygon is counter-clockwise (CCW)
    assert not is_clockwise(vertices)


# ============================================================================
# Phase 2: User Story 1 - Part C: Turn Classification
# ============================================================================


def test_compute_direction_vector():
    """Test direction vector computation."""
    from solution_part2 import compute_direction_vector

    assert compute_direction_vector((7, 3), (7, 1)) == (0, -1)  # Up
    assert compute_direction_vector((7, 1), (11, 1)) == (1, 0)  # Right
    assert compute_direction_vector((11, 1), (11, 7)) == (0, 1)  # Down
    assert compute_direction_vector((11, 7), (9, 7)) == (-1, 0)  # Left


def test_classify_turn_convex():
    """Test convex turn classification."""
    from solution_part2 import classify_turn

    # CCW polygon: Right -> Down is convex (right turn in CCW)
    incoming = (1, 0)
    outgoing = (0, 1)
    assert classify_turn(incoming, outgoing, is_clockwise=False) == "convex"


def test_classify_turn_concave():
    """Test concave turn classification."""
    from solution_part2 import classify_turn

    # CCW polygon: Down -> Right is concave (left turn away from interior in CCW)
    incoming = (0, 1)
    outgoing = (1, 0)
    assert classify_turn(incoming, outgoing, is_clockwise=False) == "concave"


def test_classify_all_vertices_example():
    """Test full vertex classification with example."""
    from solution_part2 import classify_all_vertices

    vertices = [(7, 1), (11, 1), (11, 7), (9, 7), (9, 5), (2, 5), (2, 3), (7, 3)]
    classifications = classify_all_vertices(vertices)

    assert len(classifications) == 8
    # Verify structure of first classification
    assert "vertex" in classifications[0]
    assert "classification" in classifications[0]
    assert classifications[0]["vertex"] == (7, 1)
    expected = ["convex", "convex", "convex", "convex", "concave", "convex", "convex", "concave"]
    actual = [c["classification"] for c in classifications]
    assert actual == expected


# ============================================================================
# Phase 3: User Story 2 - Edge Index
# ============================================================================


def test_edge_index_vertical_edges():
    """Test vertical edge indexing."""
    from solution_part2 import EdgeIndex

    vertices = [(0, 0), (10, 0), (10, 10), (0, 10)]
    index = EdgeIndex(vertices)

    edges_at_y1 = index.get_edges_at_y(1)
    assert len(edges_at_y1) == 2  # The two vertical line of the square
    assert 0 in edges_at_y1
    assert 10 in edges_at_y1


def test_edge_index_horizontal_edges():
    """Test horizontal edge indexing."""
    from solution_part2 import EdgeIndex

    vertices = [(0, 0), (10, 0), (10, 10), (0, 10)]
    index = EdgeIndex(vertices)

    edges_at_x1 = index.get_edges_at_x(1)
    assert len(edges_at_x1) == 2  # The two horizontal line of the square
    assert 0 in edges_at_x1
    assert 10 in edges_at_x1


def test_edge_index_corners_are_handled_separately():
    """Test horizontal edge indexing."""
    from solution_part2 import EdgeIndex

    vertices = [(0, 0), (10, 0), (10, 10), (0, 10)]
    index = EdgeIndex(vertices)

    edges_at_x0 = index.get_edges_at_x(0)
    assert (
        len(edges_at_x0) == 0
    )  # Although corners exist, they are not edges and have special logic


# ============================================================================
# Phase 4A: Classification Filter
# ============================================================================


def test_classification_filter():
    from solution_part2 import filter_convex_classifications_at

    vertices = [(7, 1), (11, 1), (11, 7), (9, 7), (9, 5), (2, 5), (2, 3), (7, 3)]
    classifications = classify_all_vertices(vertices)

    filtered = filter_convex_classifications_at(classifications, "y", 1)
    assert filtered == [7, 11]

    filtered = filter_convex_classifications_at(classifications, "y", 5)
    assert filtered == [2]

    filtered = filter_convex_classifications_at(classifications, "x", 7)
    assert filtered == [1]


# ============================================================================
# Phase 4: User Story 3 - Ray Segment Generation
# ============================================================================


def test_generate_ray_segments_no_crossings():
    """Test ray with no edge crossings."""
    from solution_part2 import generate_ray_segments

    segments = generate_ray_segments(0, 10, [], "inside")
    assert segments == [(0, 10, "inside")]


def test_generate_ray_segments_with_crossings():
    """Test ray with edge crossings."""
    from solution_part2 import generate_ray_segments

    segments = generate_ray_segments(0, 10, [3, 7], "inside")
    assert segments == [(0, 3, "inside"), (3, 7, "outside"), (7, 10, "inside")]


def test_filter_zero_width_segments():
    """Test filtering zero-width outside segments."""
    from solution_part2 import filter_zero_width_segments

    segments = [(0, 2, "inside"), (2, 2, "outside"), (2, 5, "inside")]
    filtered = filter_zero_width_segments(segments)
    assert filtered == [(0, 2, "inside"), (2, 5, "inside")]


def test_from_11_7_leftwards():
    """Test ray segment generation from (7, y) leftwards."""
    from solution_part2 import generate_ray_segments, filter_convex_classifications_at

    vertices = [(7, 1), (11, 1), (11, 7), (9, 7), (9, 5), (2, 5), (2, 3), (7, 3)]
    classifications = classify_all_vertices(vertices)

    y = 7
    ray3_edges = []  # we know this, it's correct
    ray3_state = "inside"  # we know this, it's correct
    filtered = filter_convex_classifications_at(classifications, "y", y)
    ray3_segments = generate_ray_segments(11, 7, ray3_edges, ray3_state, filtered)
    expected_segments = [(11, 9, "inside"), (9, 7, "outside")]
    assert ray3_segments == expected_segments


# ============================================================================
# Phase 4: User Story 3 - Initial Ray State
# ============================================================================


def test_determine_initial_ray_state_inside():
    """Test initial ray state determination - inside case."""
    from solution_part2 import determine_initial_ray_state

    vertex_index = 0  # Starting at first vertex (7,1)

    vertices = [(7, 1), (11, 1), (11, 7), (9, 7), (9, 5), (2, 5), (2, 3), (7, 3)]
    classifications = classify_all_vertices(vertices)
    vertex_classification = classifications[vertex_index]

    direction = (1, 0)  # Ray going right

    # Starting from inside the polygon
    state = determine_initial_ray_state(vertex_classification, direction)
    assert state == "inside"


def test_determine_initial_ray_state_outside():
    """Test initial ray state determination - outside case."""
    from solution_part2 import determine_initial_ray_state

    vertex_index = 0  # Starting at first vertex (7,1)

    vertices = [(7, 1), (11, 1), (11, 7), (9, 7), (9, 5), (2, 5), (2, 3), (7, 3)]
    classifications = classify_all_vertices(vertices)
    vertex_classification = classifications[vertex_index]

    direction = (0, -1)  # Ray going up

    # Starting from outside the polygon
    state = determine_initial_ray_state(vertex_classification, direction)
    assert state == "outside"


# ============================================================================
# Phase 5: User Story 4 - Rectangle Validation
# ============================================================================


def test_validate_rectangle_edge_inside():
    """Test edge entirely inside."""
    from solution_part2 import validate_rectangle_edge

    segments = [(0, 10, "inside")]
    assert validate_rectangle_edge(2, 8, segments)


def test_validate_rectangle_edge_outside():
    """Test edge overlaps outside segment."""
    from solution_part2 import validate_rectangle_edge

    segments = [(0, 5, "inside"), (5, 8, "outside"), (8, 10, "inside")]
    assert not validate_rectangle_edge(6, 7, segments)


def test_validate_rectangle_edge_production_outside_example():
    """Test edge overlaps outside segment."""
    from solution_part2 import validate_rectangle_edge

    segments = [(11, 7, "inside"), (7, 2, "outside")]
    assert not validate_rectangle_edge(2, 11, segments)


def test_calculate_rectangle_area():
    """Test area calculation."""
    from solution_part2 import calculate_rectangle_area

    area = calculate_rectangle_area((2, 3), (9, 5))
    assert area == (9 - 2 + 1) * (5 - 3 + 1)  # 8 * 3 = 24


# ============================================================================
# Phase 6: User Story 5 - Integration & solve_part2
# ============================================================================


def test_solve_part2_example():
    """Test complete solution with example input."""
    from solution_part2 import solve_part2

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
