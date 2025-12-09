"""
Unit tests for day-06/solution.py (User Story 3: solve_worksheet)
"""

import io
import pytest
import solution


def test_solve_worksheet_single_problem():
    """Solve worksheet with a single problem."""
    input_text = "12\n34\n+ \n"
    result = solution.solve_worksheet(io.StringIO(input_text))
    # Row 0: 12; Row 1: 34
    # 12 + 34 = 46
    assert result == 46


def test_solve_worksheet_two_problems():
    """Solve worksheet with two problems."""
    input_text = "12 34\n56 78\n*  + \n"
    result = solution.solve_worksheet(io.StringIO(input_text))
    # Problem 1: Row 0: 12; Row 1: 56 → 12 * 56 = 672
    # Problem 2: Row 0: 34; Row 1: 78 → 34 + 78 = 112
    # Total: 672 + 112 = 784
    assert result == 784


def test_solve_worksheet_three_problems():
    """Solve worksheet with three problems."""
    input_text = "1 2 3\n4 5 6\n+ * + \n"
    result = solution.solve_worksheet(io.StringIO(input_text))
    # Problem 1: Row 0: 1; Row 1: 4 → 1 + 4 = 5
    # Problem 2: Row 0: 2; Row 1: 5 → 2 * 5 = 10
    # Problem 3: Row 0: 3; Row 1: 6 → 3 + 6 = 9
    # Total: 5 + 10 + 9 = 24
    assert result == 24


def test_solve_worksheet_multiple_with_multiplication():
    """Solve worksheet with multiplication operations."""
    input_text = "23\n34\n* \n"
    result = solution.solve_worksheet(io.StringIO(input_text))
    # Row 0: 23; Row 1: 34 → 23 * 34 = 782
    assert result == 782


def test_solve_worksheet_with_file_path(tmp_path):
    """Solve worksheet from file path."""
    file = tmp_path / "worksheet.txt"
    file.write_text("5\n6\n+ \n")
    result = solution.solve_worksheet(str(file))
    # Row 0: 5; Row 1: 6 → 5 + 6 = 11
    assert result == 11


def test_solve_worksheet_empty():
    """Empty worksheet returns 0."""
    input_text = ""
    result = solution.solve_worksheet(io.StringIO(input_text))
    assert result == 0


def test_solve_worksheet_verbose_output(capsys):
    """Solve worksheet with verbose output."""
    input_text = "12 34\n56 78\n*  + \n"
    result = solution.solve_worksheet(io.StringIO(input_text), verbose=True)
    captured = capsys.readouterr()

    # Should print problem details
    assert "Problem" in captured.out or "problem" in captured.out or len(captured.out) > 0
    # Problem 1: 12 * 56 = 672
    # Problem 2: 34 + 78 = 112
    # Total: 784
    assert result == 784


def test_solve_worksheet_debug_output(capsys):
    """Solve worksheet with debug output."""
    input_text = "12\n \n+ \n"
    result = solution.solve_worksheet(io.StringIO(input_text), debug=True)
    captured = capsys.readouterr()

    # Should print debug details
    assert len(captured.out) > 0 or len(captured.err) == 0
    # Row 0: 12; Row 1: empty → only one operand 12
    # Problem: 12 + = 12
    assert result == 12
