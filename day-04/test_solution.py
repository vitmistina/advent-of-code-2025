"""Tests for Day 4 Part 1: Accessible Paper Rolls Counter."""

from .solution import (
    count_adjacent_rolls,
    is_accessible,
    is_valid_position,
    parse_grid,
    solve_part1,
    solve_part2,
)


def test_is_accessible_threshold():
    """Test is_accessible for < 4 logic."""
    assert is_accessible(0) is True
    assert is_accessible(3) is True
    assert is_accessible(4) is False
    assert is_accessible(8) is False


def test_is_accessible_boundary_cases():
    """Test is_accessible for boundary cases."""
    for n in [0, 1, 2, 3]:
        assert is_accessible(n) is True
    for n in [4, 5, 6, 7, 8]:
        assert is_accessible(n) is False


def test_single_roll_accessible():
    """Test single '@' should be accessible."""
    grid = ["@"]
    assert is_accessible(count_adjacent_rolls(grid, 0, 0)) is True


def test_all_accessible_grid():
    """Test grid where all rolls are accessible."""
    grid = ["@.@", "...", "@.@"]
    accessible = [
        is_accessible(count_adjacent_rolls(grid, r, c))
        for r, row in enumerate(grid)
        for c, val in enumerate(row)
        if val == "@"
    ]
    assert all(accessible)


def test_example_grid_part1():
    """Test with provided example expecting 13 accessible rolls (Part 1)."""
    input_data = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""
    result = solve_part1(input_data)
    assert result == 13, f"Expected 13 accessible rolls, got {result}"


def test_example_grid_part2():
    """Test with provided example expecting 43 total removed rolls (Part 2)."""
    input_data = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""
    result = solve_part2(input_data)
    assert result == 43, f"Expected 43 removed rolls, got {result}"


def test_parse_grid_basic():
    """Test parse_grid with basic input."""
    input_data = "@.@\n...\n@.@"
    grid = parse_grid(input_data)
    assert grid == ["@.@", "...", "@.@"], f"Grid parsing failed: {grid}"


def test_parse_grid_empty():
    """Test parse_grid with empty input."""
    grid = parse_grid("")
    assert grid == [], f"Expected empty grid, got {grid}"


def test_identify_paper_rolls():
    """Test identification of '@' positions in grid."""
    input_data = "@.@\n...\n@.@"
    grid = parse_grid(input_data)
    positions = [(r, c) for r, row in enumerate(grid) for c, val in enumerate(row) if val == "@"]
    assert positions == [(0, 0), (0, 2), (2, 0), (2, 2)], (
        f"Paper roll positions incorrect: {positions}"
    )


def test_count_adjacent_zero():
    """Test count_adjacent_rolls for roll with no neighbors."""
    grid = ["@.@", "...", "@.@"]
    assert count_adjacent_rolls(grid, 0, 0) == 0
    assert count_adjacent_rolls(grid, 0, 2) == 0
    assert count_adjacent_rolls(grid, 2, 0) == 0
    assert count_adjacent_rolls(grid, 2, 2) == 0


def test_count_adjacent_edge():
    """Test count_adjacent_rolls for roll at grid edge with one neighbor."""
    grid = ["@@.", "...", "..."]
    assert count_adjacent_rolls(grid, 0, 0) == 1
    assert count_adjacent_rolls(grid, 0, 1) == 1


def test_count_adjacent_corner():
    """Test count_adjacent_rolls for roll at grid corner with one neighbor."""
    grid = ["@..", "@..", "..."]
    assert count_adjacent_rolls(grid, 0, 0) == 1
    assert count_adjacent_rolls(grid, 1, 0) == 1


def test_count_adjacent_full():
    """Test count_adjacent_rolls for roll with 8 neighbors."""
    grid = ["@@@", "@@@", "@@@"]
    assert count_adjacent_rolls(grid, 1, 1) == 8


def test_is_valid_position_bounds():
    """Test is_valid_position for boundary checking."""
    grid = ["@.@", "...", "@.@"]
    assert is_valid_position(grid, 0, 0)
    assert is_valid_position(grid, 2, 2)
    assert not is_valid_position(grid, -1, 0)
    assert not is_valid_position(grid, 0, -1)
    assert not is_valid_position(grid, 3, 0)
    assert not is_valid_position(grid, 0, 3)


def test_empty_grid():
    """Test with empty grid."""
    result = solve_part1("")
    assert result == 0, f"Expected 0 for empty grid, got {result}"


def test_single_roll():
    """Test single roll with no neighbors (accessible)."""
    result = solve_part1("@")
    assert result == 1, f"Expected 1 accessible roll, got {result}"


def test_all_accessible():
    """Test grid where all rolls are accessible (< 4 neighbors each)."""
    input_data = """@.@
...
@.@"""
    result = solve_part1(input_data)
    assert result == 4, f"Expected 4 accessible rolls, got {result}"
