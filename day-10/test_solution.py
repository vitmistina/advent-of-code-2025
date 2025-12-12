"""Tests for Advent of Code 2025 - Day 10."""

from pathlib import Path

import pytest

from .solution import (
    parse_input,
    parse_line,
    solve_part1,
    solve_part2,
    apply_button,
    apply_sequence,
)


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
    machines = parse_input(test_input)
    assert len(machines) == 3
    # First machine expectations from description samples
    m0 = machines[0]
    assert m0["lights"] == [0, 1, 1, 0]
    assert any(btn == [3] for btn in m0["buttons"])  # contains (3)
    assert any(btn == [1, 3] for btn in m0["buttons"])  # contains (1,3)
    assert m0["jolts"] == [3, 5, 4, 7]


def test_part1(parsed_test_data):
    """Test Part 1 with example input."""
    result = solve_part1(parsed_test_data)
    # Expected total: 2 + 3 + 2 = 7 (from description)
    expected = 7
    assert result == expected, f"Expected {expected}, got {result}"


def test_toggle_sequence_behavior():
    """US2: toggling even times cancels; sequence reaches expected."""
    # Initial state: 4 lights all off
    state = [0, 0, 0, 0]
    # Button (0,3)
    b = [0, 3]
    # Press twice → cancels
    s2 = apply_sequence(state, [b], [2])
    assert s2 == state
    # Press once → toggles indices
    s1 = apply_sequence(state, [b], [1])
    assert s1 == [1, 0, 0, 1]


def test_part2(parsed_test_data):
    """Test Part 2 with example input."""
    result = solve_part2(parsed_test_data)
    # TODO: Replace with expected answer from puzzle
    expected = 0
    assert result == expected, f"Expected {expected}, got {result}"
