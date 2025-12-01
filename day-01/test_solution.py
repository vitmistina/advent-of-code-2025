"""Tests for Advent of Code 2025 - Day 01."""

from pathlib import Path

import pytest

from .solution import parse_input, solve_part1, solve_part2


@pytest.fixture
def test_input():
    """Load test input."""
    test_file = Path(__file__).parent / "test_input.txt"
    return test_file.read_text()


@pytest.fixture
def parsed_test_data(test_input):
    """Parse test input."""
    return parse_input(test_input)


def test_parse_input(test_input):
    """Test input parsing."""
    data = parse_input(test_input)
    assert data is not None
    # TODO: Add specific parsing assertions


def test_part1(parsed_test_data):
    """Test Part 1 with example input."""
    result = solve_part1(parsed_test_data)
    # TODO: Replace with expected answer from puzzle
    expected = 0
    assert result == expected, f"Expected {expected}, got {result}"


def test_part2(parsed_test_data):
    """Test Part 2 with example input."""
    result = solve_part2(parsed_test_data)
    # TODO: Replace with expected answer from puzzle
    expected = 0
    assert result == expected, f"Expected {expected}, got {result}"
