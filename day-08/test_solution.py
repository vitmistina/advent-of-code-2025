"""Tests for Day 8 Part 1: Circuit Analysis."""

from pathlib import Path

import pytest
from .solution import (
    compute_all_distances,
    euclidean_distance,
    find_circuit,
    get_three_largest_sizes,
    parse_input,
    process_connections,
    solve_part1,
)


@pytest.fixture
def example_input():
    """Load the example input from test_input.txt."""
    test_file = Path(__file__).parent / "test_input.txt"
    return test_file.read_text()


@pytest.fixture
def sample_points():
    """Small known dataset for unit tests."""
    return [
        (0, 0, 0),  # ID 0
        (3, 4, 0),  # ID 1
        (0, 0, 5),  # ID 2
    ]


# ============================================================================
# USER STORY 1: Parse Junction Box Coordinates
# ============================================================================


def test_parse_input(example_input):
    """Test parsing of junction box coordinates."""
    points = parse_input(example_input)

    # Example has 20 junction boxes
    assert len(points) == 20

    # First point from example: 162,817,812
    assert points[0] == (162, 817, 812)

    # Second point from example: 57,618,57
    assert points[1] == (57, 618, 57)

    # All points should be 3-tuples of integers
    for point in points:
        assert len(point) == 3
        assert all(isinstance(coord, int) for coord in point)


def test_parse_input_validates_format():
    """Test parsing validates input format."""
    valid_input = "1,2,3\n4,5,6\n"
    points = parse_input(valid_input)
    assert len(points) == 2
    assert points[0] == (1, 2, 3)
    assert points[1] == (4, 5, 6)


# ============================================================================
# USER STORY 2: Calculate Euclidean Distances
# ============================================================================


def test_euclidean_distance(sample_points):
    """Test Euclidean distance calculation between two 3D points."""
    # Distance from (0,0,0) to (3,4,0) should be 5.0
    # sqrt(3^2 + 4^2 + 0^2) = sqrt(9 + 16 + 0) = sqrt(25) = 5.0
    dist = euclidean_distance(sample_points[0], sample_points[1])
    assert abs(dist - 5.0) < 0.001

    # Distance from (0,0,0) to (0,0,5) should be 5.0
    dist = euclidean_distance(sample_points[0], sample_points[2])
    assert abs(dist - 5.0) < 0.001

    # Distance from (3,4,0) to (0,0,5) should be sqrt(50) ≈ 7.071
    dist = euclidean_distance(sample_points[1], sample_points[2])
    assert abs(dist - 7.0710678118654755) < 0.001


def test_compute_all_distances(sample_points):
    """Test computing all pairwise distances."""
    distances = compute_all_distances(sample_points)

    # With 3 points, we should have 3 pairs: (0,1), (0,2), (1,2)
    assert len(distances) == 3

    # All distances should be tuples of (distance, id_a, id_b)
    for dist, id_a, id_b in distances:
        assert isinstance(dist, float)
        assert isinstance(id_a, int)
        assert isinstance(id_b, int)
        assert id_a < id_b  # IDs should be ordered

    # Verify sorted by distance (ascending)
    for i in range(len(distances) - 1):
        assert distances[i][0] <= distances[i + 1][0]


def test_distances_sorted():
    """Test that distances are sorted in ascending order."""
    points = [
        (0, 0, 0),  # ID 0
        (1, 0, 0),  # ID 1 - distance 1 from ID 0
        (10, 0, 0),  # ID 2 - distance 10 from ID 0, 9 from ID 1
    ]
    distances = compute_all_distances(points)

    # Shortest distance should be first: (0,1) with distance 1.0
    assert distances[0][0] == 1.0
    assert distances[0][1] == 0
    assert distances[0][2] == 1

    # Next should be (1,2) with distance 9.0
    assert distances[1][0] == 9.0
    assert distances[1][1] == 1
    assert distances[1][2] == 2

    # Longest should be (0,2) with distance 10.0
    assert distances[2][0] == 10.0
    assert distances[2][1] == 0
    assert distances[2][2] == 2


# ============================================================================
# USER STORY 3: Connect Closest Pairs Using Union-Find
# ============================================================================


def test_find_circuit():
    """Test finding which circuit contains a point."""
    circuits = {
        "circuit_0": {0, 1, 2},
        "circuit_1": {3, 4},
        "circuit_2": {5},
    }

    assert find_circuit(0, circuits) == "circuit_0"
    assert find_circuit(1, circuits) == "circuit_0"
    assert find_circuit(3, circuits) == "circuit_1"
    assert find_circuit(5, circuits) == "circuit_2"
    assert find_circuit(99, circuits) is None  # Not in any circuit


def test_process_connections_creates_circuits():
    """Test that process_connections creates circuits from distance pairs."""
    # Simple case: 4 points, connect them in pairs
    points = [
        (0, 0, 0),  # ID 0
        (1, 0, 0),  # ID 1
        (10, 0, 0),  # ID 2
        (11, 0, 0),  # ID 3
    ]
    distances = compute_all_distances(points)

    # Make 2 connections (shortest distances)
    circuits = process_connections(distances, num_points=4, num_connections=2)

    # Should create 2 circuits: {0,1} and {2,3}
    circuit_sizes = sorted([len(members) for members in circuits.values()])
    assert circuit_sizes == [2, 2]


def test_process_connections_skips_same_circuit():
    """Test that connections within same circuit are skipped."""
    # 3 points in a line: 0--1--2
    points = [
        (0, 0, 0),  # ID 0
        (1, 0, 0),  # ID 1
        (2, 0, 0),  # ID 2
    ]
    distances = compute_all_distances(points)
    # Distances: (0,1)=1, (1,2)=1, (0,2)=2

    # Make 3 connections (all of them)
    circuits = process_connections(distances, num_points=3, num_connections=3)

    # Should create 1 circuit containing all 3 points
    assert len(circuits) == 1
    circuit_members = list(circuits.values())[0]
    assert len(circuit_members) == 3
    assert circuit_members == {0, 1, 2}


def test_process_connections_example_10(example_input):
    """Test with example input using 10 connections."""
    points = parse_input(example_input)
    distances = compute_all_distances(points)

    # Process 10 connections as specified in example
    circuits = process_connections(distances, num_points=len(points), num_connections=10)

    # Get circuit sizes and sort descending
    sizes = sorted([len(members) for members in circuits.values()], reverse=True)

    # Example should produce circuits of sizes [5, 4, 2, 2, 1, 1, 1, 1, 1, 1, 1]
    # (total 20 points = sum of all circuit sizes)
    assert sum(sizes) == 20
    assert sizes[0] >= 4  # Largest should be at least 4
    assert sizes[1] >= 2  # Second largest should be at least 2


# ============================================================================
# USER STORY 4: Calculate Circuit Sizes and Identify Largest Three
# ============================================================================


def test_get_three_largest_sizes():
    """Test getting the three largest circuit sizes."""
    circuits = {
        "circuit_0": {0, 1, 2, 3, 4},  # size 5
        "circuit_1": {5, 6, 7, 8},  # size 4
        "circuit_2": {9, 10},  # size 2
        "circuit_3": {11, 12},  # size 2
        "circuit_4": {13},  # size 1
    }

    largest = get_three_largest_sizes(circuits)

    assert len(largest) == 3
    assert largest == [5, 4, 2]


def test_solve_part1_example(example_input):
    """Test solve_part1 with example input (10 connections)."""
    # Example should produce answer of 40 (5 × 4 × 2)
    result = solve_part1(example_input, num_connections=10)

    # The product of three largest circuit sizes should be 40
    # Based on circuit sizes [5, 4, 2, 2, 1, 1, 1, 1, 1, 1, 1]
    assert result == 40


def test_solve_part1_full_input():
    """Test solve_part1 with full input (1000 connections)."""
    from pathlib import Path

    input_file = Path(__file__).parent / "input.txt"
    input_text = input_file.read_text()

    # Should produce a valid integer result
    result = solve_part1(input_text, num_connections=1000)

    assert isinstance(result, int)
    assert result > 0
