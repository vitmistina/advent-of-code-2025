"""
Unit tests for day-06/parser.py (User Story 2: Multiple problems integration)
"""

import pytest
import parser


def test_parse_two_problems_end_to_end():
    """Parse worksheet with two problems separated by whitespace."""
    lines = ["12 34\n", "56 78\n", "*  + \n"]

    # Pipeline: lines -> columns -> problem groups -> extract problems
    cols = list(parser.columns_from_lines(iter(lines)))
    groups = list(parser.problem_column_groups(iter(cols)))

    assert len(groups) == 2

    # First problem (cols 0-1)
    # Row 0: "12", Row 1: "56" -> operands 12, 56
    p1 = parser.extract_problem(groups[0])
    assert p1.operands == [12, 56]  # Row 0: 12; Row 1: 56
    assert p1.operation == "*"
    assert p1.result == 12 * 56

    # Second problem (cols 3-4)
    # Row 0: "34", Row 1: "78" -> operands 34, 78
    p2 = parser.extract_problem(groups[1])
    assert p2.operands == [34, 78]  # Row 0: 34; Row 1: 78
    assert p2.operation == "+"
    assert p2.result == 34 + 78


def test_parse_three_problems_with_multi_digit_operands():
    """Parse worksheet with three problems and multi-digit operands."""
    lines = ["123 456  789\n", "    789  456\n", "*    +   * \n"]

    cols = list(parser.columns_from_lines(iter(lines)))
    groups = list(parser.problem_column_groups(iter(cols)))

    assert len(groups) == 3

    # First problem (cols 0-2): Row 0: "123"; Row 1: "" (empty) -> ["123"]
    p1 = parser.extract_problem(groups[0])
    assert p1.operands == [123]
    assert p1.operation == "*"
    assert p1.result == 123

    # Second problem (cols 4-7): Row 0: "456"; Row 1: "789" -> ["456", "789"]
    p2 = parser.extract_problem(groups[1])
    assert p2.operands == [456, 789]
    assert p2.operation == "+"
    assert p2.result == 456 + 789

    # Third problem (cols 9-11): Row 0: "789"; Row 1: "456" -> ["789", "456"]
    p3 = parser.extract_problem(groups[2])
    assert p3.operands == [789, 456]
    assert p3.operation == "*"
    assert p3.result == 789 * 456


def test_parse_variable_length_problems():
    """Problems with different heights should still work."""
    lines1 = ["12\n", "34\n", "+ \n"]
    cols1 = list(parser.columns_from_lines(iter(lines1)))
    groups1 = list(parser.problem_column_groups(iter(cols1)))
    p1 = parser.extract_problem(groups1[0])
    assert p1.operands == [12, 34]  # Row 0: 12; Row 1: 34

    # Longer problem
    lines2 = ["5\n", "6\n", "7\n", "8\n", "*\n"]
    cols2 = list(parser.columns_from_lines(iter(lines2)))
    groups2 = list(parser.problem_column_groups(iter(cols2)))
    p2 = parser.extract_problem(groups2[0])
    assert p2.operands == [5, 6, 7, 8]  # Each row is an operand


def test_parse_variable_width_problems():
    """Problems with different widths in same worksheet."""
    # First problem: 2 columns, then separator, second problem: 3 columns
    lines = ["12 345\n", "67 890\n", "+  + \n"]

    cols = list(parser.columns_from_lines(iter(lines)))
    groups = list(parser.problem_column_groups(iter(cols)))

    assert len(groups) == 2

    # First problem: Row 0: "12"; Row 1: "67"
    p1 = parser.extract_problem(groups[0])
    assert p1.operands == [12, 67]
    assert len(groups[0].columns) == 2

    # Second problem: Row 0: "345"; Row 1: "890"
    p2 = parser.extract_problem(groups[1])
    assert p2.operands == [345, 890]
    assert len(groups[1].columns) == 3


def test_parse_with_trailing_spaces():
    """Worksheet with trailing spaces and separators."""
    lines = ["12   34  \n", "56   78  \n", "*    +   \n"]

    cols = list(parser.columns_from_lines(iter(lines)))
    groups = list(parser.problem_column_groups(iter(cols)))

    # Should find two problems despite trailing spaces
    assert len(groups) == 2


def test_empty_worksheet():
    """Empty worksheet returns no problems."""
    lines = []
    cols = list(parser.columns_from_lines(iter(lines)))
    groups = list(parser.problem_column_groups(iter(cols)))

    assert len(groups) == 0


def test_worksheet_only_separators():
    """Worksheet with only separator columns."""
    lines = ["   \n", "   \n", "   \n"]
    cols = list(parser.columns_from_lines(iter(lines)))
    groups = list(parser.problem_column_groups(iter(cols)))

    assert len(groups) == 0
