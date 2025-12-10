"""Tests for Advent of Code 2025 - Day 09."""

import sys
from pathlib import Path

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from solution import (
    calculate_rectangle_area,
    find_largest_rectangle,
    parse_coordinates,
    solve_part1,
    solve_part2,
    validate_input,
)


@pytest.fixture
def test_input():
    """Load test input."""
    test_file = Path(__file__).parent / "test_input.txt"
    content = test_file.read_text().strip()
    if not content:
        return ""
    return content


@pytest.fixture
def test_input_lines(test_input):
    """Split test input into lines."""
    return test_input.strip().split("\n")


@pytest.fixture
def parsed_coordinates(test_input_lines):
    """Parse test input coordinates."""
    if not test_input_lines or test_input_lines[0] == "":
        return []
    return parse_coordinates(test_input_lines)


class TestValidateInput:
    """Tests for validate_input function."""

    def test_validate_input_valid(self):
        """Test validation of valid input."""
        lines = ["2,5", "11,1"]
        validate_input(lines)  # Should not raise

    def test_validate_input_empty(self):
        """Test validation fails on empty input."""
        with pytest.raises(ValueError, match="Input cannot be empty"):
            validate_input([])

    def test_validate_input_empty_line(self):
        """Test validation fails on empty line."""
        with pytest.raises(ValueError, match="Line .* is empty"):
            validate_input(["2,5", "", "11,1"])

    def test_validate_input_malformed(self):
        """Test validation fails on malformed line."""
        with pytest.raises(ValueError, match="invalid format"):
            validate_input(["2,5,3"])

    def test_validate_input_non_integer(self):
        """Test validation fails on non-integer coordinates."""
        with pytest.raises(ValueError, match="non-integer"):
            validate_input(["2.5,5"])

    def test_validate_input_negative(self):
        """Test validation fails on negative coordinates."""
        with pytest.raises(ValueError, match="negative"):
            validate_input(["-2,5"])


class TestParseCoordinates:
    """Tests for parse_coordinates function."""

    def test_parse_coordinates_valid(self):
        """Test parsing valid coordinates."""
        lines = ["2,5", "11,1", "7,3"]
        result = parse_coordinates(lines)
        assert result == [(2, 5), (11, 1), (7, 3)]

    def test_parse_coordinates_with_whitespace(self):
        """Test parsing coordinates with whitespace."""
        lines = [" 2 , 5 ", "11, 1"]
        result = parse_coordinates(lines)
        assert result == [(2, 5), (11, 1)]

    def test_parse_coordinates_empty_input(self):
        """Test parsing fails on empty input."""
        with pytest.raises(ValueError, match="Input cannot be empty"):
            parse_coordinates([])


class TestCalculateRectangleArea:
    """Tests for calculate_rectangle_area function."""

    def test_calculate_area_basic(self):
        """Test area calculation for basic rectangle."""
        area = calculate_rectangle_area((2, 5), (11, 1))
        assert area == 50  # (|2-11| + 1) * (|5-1| + 1) = 10 * 5 = 50

    def test_calculate_area_zero_width(self):
        """Test area calculation with zero width."""
        area = calculate_rectangle_area((2, 5), (2, 10))
        assert area == 6  # (|2-2| + 1) * (|5-10| + 1) = 1 * 6 = 6

    def test_calculate_area_zero_height(self):
        """Test area calculation with zero height."""
        area = calculate_rectangle_area((2, 5), (10, 5))
        assert area == 9  # (|2-10| + 1) * (|5-5| + 1) = 9 * 1 = 9

    def test_calculate_area_same_point(self):
        """Test area calculation with same point."""
        area = calculate_rectangle_area((2, 5), (2, 5))
        assert area == 1  # (0 + 1) * (0 + 1) = 1

    def test_calculate_area_order_invariant(self):
        """Test that order of corners doesn't matter."""
        area1 = calculate_rectangle_area((2, 5), (11, 1))
        area2 = calculate_rectangle_area((11, 1), (2, 5))
        assert area1 == area2


class TestFindLargestRectangle:
    """Tests for find_largest_rectangle function."""

    def test_find_largest_basic(self):
        """Test finding largest rectangle from basic input."""
        coordinates = [(2, 5), (11, 1), (7, 3)]
        result = find_largest_rectangle(coordinates)
        # Check all pairs: (2,5)-(11,1)=50, (2,5)-(7,3)=18, (11,1)-(7,3)=20
        assert result == 50

    def test_find_largest_two_tiles(self):
        """Test with exactly two tiles."""
        coordinates = [(0, 0), (5, 5)]
        result = find_largest_rectangle(coordinates)
        assert result == 36  # (5-0+1) * (5-0+1) = 6 * 6 = 36

    def test_find_largest_insufficient_tiles(self):
        """Test fails with fewer than 2 tiles."""
        with pytest.raises(ValueError, match="at least 2"):
            find_largest_rectangle([(0, 0)])

    def test_find_largest_collinear(self):
        """Test with collinear tiles (minimum area)."""
        coordinates = [(0, 0), (5, 0), (10, 0)]
        result = find_largest_rectangle(coordinates)
        # All pairs are on same row: (0,0)-(5,0)=6, (0,0)-(10,0)=11, (5,0)-(10,0)=6
        assert result == 11  # (|0-10| + 1) * (|0-0| + 1) = 11 * 1 = 11


class TestSolvePart1:
    """Tests for solve_part1 function."""

    def test_solve_part1_basic(self):
        """Test Part 1 with basic coordinates."""
        coordinates = [(2, 5), (11, 1), (7, 3)]
        result = solve_part1(coordinates)
        assert result == 50

    def test_solve_part1_insufficient_tiles(self):
        """Test Part 1 fails with insufficient tiles."""
        with pytest.raises(ValueError):
            solve_part1([(0, 0)])


def test_solve_part1_with_test_input(parsed_coordinates):
    """Test Part 1 with example input - expects area of 50."""
    result = solve_part1(parsed_coordinates)
    expected = 50
    assert result == expected, f"Expected {expected}, got {result}"


def test_part2(parsed_coordinates):
    """Test Part 2 with example input."""
    result = solve_part2(parsed_coordinates)
    # TODO: Replace with expected answer from puzzle
    expected = 0
    assert result == expected, f"Expected {expected}, got {result}"
