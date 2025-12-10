"""Tests for Advent of Code 2025 - Day 01."""

from pathlib import Path

import pytest

from .solution import apply_rotation, parse_input, solve_part1, solve_part2


@pytest.fixture
def test_input():
    """Load test input."""
    test_file = Path(__file__).parent / "test_input.txt"
    return test_file.read_text()


@pytest.fixture
def parsed_test_data(test_input):
    """Parse test input."""
    return parse_input(test_input)


# ============================================================================
# User Story 1: Count Zero Positions - RED Phase Tests
# ============================================================================


def test_parse_input_sample(test_input):
    """Test parsing the 10-line sample input (T006)."""
    data = parse_input(test_input)
    assert data is not None
    assert len(data) == 10, f"Expected 10 rotations, got {len(data)}"
    assert data[0] == ("L", 68), f"Expected ('L', 68), got {data[0]}"
    assert data[2] == ("R", 48), f"Expected ('R', 48), got {data[2]}"
    assert data[9] == ("L", 82), f"Expected ('L', 82), got {data[9]}"


def test_parse_input_empty():
    """Test parsing empty input (T007)."""
    data = parse_input("")
    assert data == [], f"Expected empty list, got {data}"


def test_apply_rotation_left():
    """Test left rotation (T008)."""
    # 50 -> L68 -> 82
    assert apply_rotation(50, "L", 68) == 82
    # 82 -> L30 -> 52
    assert apply_rotation(82, "L", 30) == 52
    # Wraparound: 5 -> L10 -> 95
    assert apply_rotation(5, "L", 10) == 95


def test_apply_rotation_right():
    """Test right rotation (T009)."""
    # 52 -> R48 -> 0
    assert apply_rotation(52, "R", 48) == 0
    # 95 -> R60 -> 55
    assert apply_rotation(95, "R", 60) == 55
    # Wraparound: 99 -> R1 -> 0
    assert apply_rotation(99, "R", 1) == 0


def test_apply_rotation_zero_distance():
    """Test no movement with zero distance (T010)."""
    assert apply_rotation(50, "L", 0) == 50
    assert apply_rotation(50, "R", 0) == 50


def test_solve_part1_sample(parsed_test_data):
    """Test Part 1 with sample input - should return 3 (T011)."""
    result = solve_part1(parsed_test_data)
    expected = 3
    assert result == expected, f"Expected {expected}, got {result}"


def test_solve_part1_empty():
    """Test Part 1 with empty rotation list (T012)."""
    result = solve_part1([])
    expected = 0
    assert result == expected, f"Expected {expected}, got {result}"


def test_solve_part1_no_zeros():
    """Test Part 1 with rotations that never land on 0 (T013)."""
    rotations = [("L", 10), ("R", 5)]
    result = solve_part1(rotations)
    expected = 0
    assert result == expected, f"Expected {expected}, got {result}"


# ============================================================================
# User Story 1: Count All Zero Crossings - Part 2 RED Phase Tests
# ============================================================================


@pytest.mark.parametrize(
    "start,direction,distance,expected",
    [
        # Zero distance edge case
        (50, "R", 0, 0),
        (50, "L", 0, 0),
        # Right rotation - no crossing
        (50, "R", 40, 0),
        # Right rotation - single crossing at end
        (99, "R", 1, 1),  # 99->0: hits 0 once (at click 1)
        # Right rotation - exact wrap from 0
        (0, "R", 100, 1),  # 0->1->...->0 (at click 100): hits 0 once
        # Right rotation - multi-wrap
        (50, "R", 1000, 10),  # Crosses 0 ten times
        # Left rotation - don't reach 0
        (50, "L", 30, 0),
        # Left rotation - cross once
        (50, "L", 60, 1),  # Crosses 0 once at click 50
        # Left rotation - from 0 (no crossing until full lap)
        (0, "L", 1, 0),  # 0->99: doesn't hit 0
        # Left rotation - multi-wrap ending at 0
        (50, "L", 250, 3),  # Hits 0 at clicks 50, 150, 250
    ],
)
def test_count_zero_crossings_during_rotation(start, direction, distance, expected):
    """Test counting zero crossings during rotation (T004 - RED Phase)."""
    from .solution import count_zero_crossings_during_rotation

    result = count_zero_crossings_during_rotation(start, direction, distance)
    assert result == expected, (
        f"Position {start}, {direction}{distance}: expected {expected}, got {result}"
    )


def test_solve_part2_sample_input(parsed_test_data):
    """Test Part 2 with sample input - should return 6 total (T005 - RED Phase)."""
    result = solve_part2(parsed_test_data)
    expected = 6  # 3 during + 3 at end
    assert result == expected, f"Expected {expected}, got {result}"


# ============================================================================
# User Story 3: Backward Compatibility - Part 1 Validation
# ============================================================================


def test_part1_unchanged(parsed_test_data):
    """Test Part 1 solution unchanged - should return 3 (T022)."""
    result = solve_part1(parsed_test_data)
    expected = 3
    assert result == expected, f"Part 1 broken! Expected {expected}, got {result}"


def test_part2_includes_part1(parsed_test_data):
    """Test Part 2 >= Part 1 invariant (T023)."""
    part1_result = solve_part1(parsed_test_data)
    part2_result = solve_part2(parsed_test_data)
    assert part2_result >= part1_result, (
        f"Part 2 ({part2_result}) should be >= Part 1 ({part1_result})"
    )


def test_part2_includes_part1_custom_inputs():
    """Test Part 2 >= Part 1 with custom inputs (T023)."""
    test_cases = [
        [("R", 50)],  # Single rotation ending at 0
        [("L", 68), ("R", 48)],  # Multiple rotations
        [("R", 1000)],  # Large distance
    ]

    for rotations in test_cases:
        part1 = solve_part1(rotations)
        part2 = solve_part2(rotations)
        assert part2 >= part1, (
            f"Rotations {rotations}: Part 2 ({part2}) should be >= Part 1 ({part1})"
        )
