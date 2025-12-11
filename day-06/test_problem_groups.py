"""
Unit tests for day-06/parser.py (User Story 2: problem_column_groups)
"""

import pytest
from . import parser


def test_problem_column_groups_single_problem():
    """Single problem with no separators."""
    lines = ["123\n", "456\n", "+  \n"]
    cols = list(parser.columns_from_lines(iter(lines)))
    groups = list(parser.problem_column_groups(iter(cols)))

    assert len(groups) == 1
    assert groups[0].start_column == 0
    assert groups[0].end_column == 2
    assert len(groups[0].columns) == 3


def test_problem_column_groups_two_problems():
    """Two problems separated by a whitespace column."""
    lines = ["12 34\n", "56 78\n", "+  + \n"]
    cols = list(parser.columns_from_lines(iter(lines)))
    groups = list(parser.problem_column_groups(iter(cols)))

    assert len(groups) == 2
    # First problem
    assert groups[0].start_column == 0
    assert groups[0].end_column == 1
    assert len(groups[0].columns) == 2
    # Second problem
    assert groups[1].start_column == 3
    assert groups[1].end_column == 4
    assert len(groups[1].columns) == 2


def test_problem_column_groups_multiple_separators():
    """Multiple problems with multiple separator columns."""
    lines = ["1  2  3\n", "4  5  6\n", "+  +  +\n"]
    cols = list(parser.columns_from_lines(iter(lines)))
    groups = list(parser.problem_column_groups(iter(cols)))

    assert len(groups) == 3
    assert groups[0].start_column == 0
    assert groups[0].end_column == 0
    assert groups[1].start_column == 3
    assert groups[1].end_column == 3
    assert groups[2].start_column == 6
    assert groups[2].end_column == 6


def test_problem_column_groups_trailing_separator():
    """Problem followed by separator columns."""
    lines = ["12  \n", "34  \n", "+   \n"]
    cols = list(parser.columns_from_lines(iter(lines)))
    groups = list(parser.problem_column_groups(iter(cols)))

    assert len(groups) == 1
    assert groups[0].start_column == 0
    assert groups[0].end_column == 1


def test_problem_column_groups_leading_separator():
    """Separator columns followed by problem."""
    lines = ["  12\n", "  34\n", "  + \n"]
    cols = list(parser.columns_from_lines(iter(lines)))
    groups = list(parser.problem_column_groups(iter(cols)))

    assert len(groups) == 1
    assert groups[0].start_column == 2
    assert groups[0].end_column == 3


def test_problem_column_groups_empty():
    """Empty column stream."""
    cols = iter([])
    groups = list(parser.problem_column_groups(cols))

    assert len(groups) == 0


def test_problem_column_groups_all_separators():
    """All columns are separators (no problems)."""
    lines = ["  \n", "  \n", "  \n"]
    cols = list(parser.columns_from_lines(iter(lines)))
    groups = list(parser.problem_column_groups(iter(cols)))

    assert len(groups) == 0
