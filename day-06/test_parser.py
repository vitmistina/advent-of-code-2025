"""
Unit tests for day-06/parser.py (User Story 1: read_lines_as_stream, columns_from_lines)
"""

import io
import pytest
from . import parser


def test_read_lines_as_stream_file(tmp_path):
    # Create a temp file
    file = tmp_path / "input.txt"
    file.write_text("a\nb\nc\n")
    lines = list(parser.read_lines_as_stream(str(file)))
    assert lines == ["a\n", "b\n", "c\n"]


def test_read_lines_as_stream_filelike():
    f = io.StringIO("x\ny\nz\n")
    lines = list(parser.read_lines_as_stream(f))
    assert lines == ["x\n", "y\n", "z\n"]


def test_read_lines_as_stream_empty(tmp_path):
    file = tmp_path / "empty.txt"
    file.write_text("")
    lines = list(parser.read_lines_as_stream(str(file)))
    assert lines == []


def test_columns_from_lines_simple():
    lines = ["12\n", "34\n", "+*\n"]
    cols = list(parser.columns_from_lines(iter(lines)))
    assert len(cols) == 2
    assert cols[0].values == ["1", "3", "+"]
    assert cols[1].values == ["2", "4", "*"]
    assert not cols[0].is_separator
    assert not cols[1].is_separator


def test_columns_from_lines_separator():
    lines = ["1 2\n", "3 4\n", "+ *\n"]
    cols = list(parser.columns_from_lines(iter(lines)))
    assert len(cols) == 3
    assert cols[1].is_separator
    assert cols[1].values == [" ", " ", " "]


def test_extract_problem_single_simple():
    """Extract a single simple problem with multiplication."""
    # Row 0: "123"; Row 1: "456" → operands: 123, 456
    lines = ["123\n", "456\n", "*  \n"]
    cols = list(parser.columns_from_lines(iter(lines)))
    problem_group = parser.ProblemGroup(start_column=0, end_column=2, columns=cols)
    problem = parser.extract_problem(problem_group)
    assert problem.operands == [123, 456]
    assert problem.operation == "*"
    assert problem.result == 123 * 456


def test_extract_problem_single_addition():
    """Extract a single problem with addition."""
    # Rows: "1", "2", "3" → operands: 1, 2, 3
    lines = ["1\n", "2\n", "3\n", "+\n"]
    cols = list(parser.columns_from_lines(iter(lines)))
    problem_group = parser.ProblemGroup(start_column=0, end_column=0, columns=cols)
    problem = parser.extract_problem(problem_group)
    assert problem.operands == [1, 2, 3]
    assert problem.operation == "+"
    assert problem.result == 1 + 2 + 3


def test_extract_problem_multidigit():
    """Extract problem with multi-digit operands.

    Layout:
    10 20
    30 40
    +  +

    Rows: "10", "30" for problem 1 → operands: 10, 30
    Rows: "20", "40" for problem 2 → operands: 20, 40
    """
    lines = ["10 20\n", "30 40\n", "+  + \n"]
    cols = list(parser.columns_from_lines(iter(lines)))
    # First problem: cols 0-1
    problem_group1 = parser.ProblemGroup(start_column=0, end_column=1, columns=cols[:2])
    problem1 = parser.extract_problem(problem_group1)
    assert problem1.operands == [10, 30]  # Row 0: 10; Row 1: 30
    assert problem1.operation == "+"


def test_extract_problem_empty_group():
    """Error: Empty problem group."""
    problem_group = parser.ProblemGroup(start_column=0, end_column=-1, columns=[])
    with pytest.raises(ValueError, match="has no columns"):
        parser.extract_problem(problem_group)


def test_extract_problem_no_operation():
    """Error: No operation found in last row."""
    lines = ["1\n", "2\n", " \n"]  # Last row has no operation
    cols = list(parser.columns_from_lines(iter(lines)))
    problem_group = parser.ProblemGroup(start_column=0, end_column=0, columns=cols)
    with pytest.raises(ValueError, match="No operation found"):
        parser.extract_problem(problem_group)


def test_extract_problem_single_row():
    """Error: Problem must have at least 2 rows."""
    lines = ["+\n"]
    cols = list(parser.columns_from_lines(iter(lines)))
    problem_group = parser.ProblemGroup(start_column=0, end_column=0, columns=cols)
    with pytest.raises(ValueError, match="at least 2 rows"):
        parser.extract_problem(problem_group)


def test_extract_problem_no_operands():
    """Error: No operands found (only spaces and operation)."""
    lines = ["  \n", "  \n", "+ \n"]
    cols = list(parser.columns_from_lines(iter(lines)))
    problem_group = parser.ProblemGroup(start_column=0, end_column=1, columns=cols)
    with pytest.raises(ValueError, match="No operands found"):
        parser.extract_problem(problem_group)
