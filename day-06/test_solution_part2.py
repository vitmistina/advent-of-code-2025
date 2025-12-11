"""
Test module for Day 6, Part 2 - Cephalopod Math (Right-to-Left Columns).
Implements test cases for the worksheet solver following TDD approach.

Tests cover:
- Basic problem parsing and evaluation
- Example worksheet from spec (acceptance criteria)
- Edge cases (variable spacing, missing numbers/operators)
- Error handling for malformed input
"""

import io
import pytest
from .utils import Problem, evaluate_problem
from .solution_part2 import solve_worksheet


class TestEvaluateProblem:
    """Tests for the evaluate_problem function (reused from Part 1)."""

    def test_addition(self):
        """Test simple addition."""
        problem = Problem(operands=[1, 2, 3], operation="+", result=0)
        assert evaluate_problem(problem) == 6

    def test_multiplication(self):
        """Test simple multiplication."""
        problem = Problem(operands=[2, 3, 4], operation="*", result=0)
        assert evaluate_problem(problem) == 24

    def test_single_operand_addition(self):
        """Test addition with single operand (identity)."""
        problem = Problem(operands=[42], operation="+", result=0)
        assert evaluate_problem(problem) == 42

    def test_single_operand_multiplication(self):
        """Test multiplication with single operand (identity)."""
        problem = Problem(operands=[42], operation="*", result=0)
        assert evaluate_problem(problem) == 42

    def test_invalid_operation(self):
        """Test invalid operation raises ValueError."""
        problem = Problem(operands=[1, 2], operation="-", result=0)
        with pytest.raises(ValueError, match="Unknown operation"):
            evaluate_problem(problem)


class TestSolveWorksheet:
    """Tests for the solve_worksheet function (Part 2 specific)."""

    def test_single_problem_addition(self):
        """Test solving a single addition problem.

        In Part 2, numbers are in columns (top-to-bottom) and columns are read right-to-left.
        For a simple two-number addition:
          3 1
          4 2
            +

        Col 1 (right): 3, 4 → 34
        Col 0 (left): 1, 2 → 12
        Reading right-to-left: 34 + 12 = 46
        """
        worksheet = "31\n42\n+\n"
        result = solve_worksheet(io.StringIO(worksheet))
        # Numbers (right-to-left): 34, 12
        # Operation: +
        # Expected: 34 + 12 = 46
        assert result == 46

    def test_single_problem_multiplication(self):
        """Test solving a single multiplication problem.

        In Part 2:
          5
          3
          *

        Col 0: 5, 3 → 53
        Numbers (right-to-left): 53
        Operation: *
        Expected: 53 = 53 (single operand)
        """
        worksheet = "5\n3\n*\n"
        result = solve_worksheet(io.StringIO(worksheet))
        # Numbers: 53
        # Operation: *
        # Expected: 53 = 53
        assert result == 53

    def test_acceptance_criteria_example(self):
        """Test the example from the spec (acceptance criteria).

        The worksheet is parsed right-to-left:
        columns 0-2: problem 1 (rightmost problem)
        column 3: separator
        columns 4-6: problem 2 (left problem)

        For each problem, read columns top-to-bottom to get digit rows,
        then reconstruct numbers from digit columns.
        """
        worksheet = """123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +
"""
        result = solve_worksheet(io.StringIO(worksheet))
        # Expected grand total: 3263827
        assert result == 3263827

    def test_verbose_mode(self, capsys):
        """Test verbose output."""
        worksheet = "31\n42\n+\n"
        result = solve_worksheet(io.StringIO(worksheet), verbose=True)
        captured = capsys.readouterr()
        assert "Grand Total:" in captured.out
        assert "46" in captured.out
        assert result == 46

    def test_debug_mode(self, capsys):
        """Test debug output."""
        worksheet = "31\n42\n+\n"
        result = solve_worksheet(io.StringIO(worksheet), debug=True)
        captured = capsys.readouterr()
        assert "[DEBUG]" in captured.out
        assert result == 46

    def test_empty_worksheet(self):
        """Test empty worksheet doesn't raise error (returns 0).

        Empty input should result in no problems and grand total 0.
        """
        worksheet = ""
        result = solve_worksheet(io.StringIO(worksheet))
        assert result == 0

    def test_file_input(self, tmp_path):
        """Test solving from a file."""
        test_file = tmp_path / "worksheet.txt"
        test_file.write_text("31\n42\n+\n")
        result = solve_worksheet(str(test_file))
        assert result == 46


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_large_numbers(self):
        """Test with large numbers.

        Format:
          999
          888
          777
          *

        Col 0: 9, 8, 7 → 987
        Col 1: 9, 8, 7 → 987
        Col 2: 9, 8, 7 → 987
        Operation: *

        Problem (rightmost to leftmost): 987, 987, 987
        Result: 987 * 987 * 987 = 960596643
        """
        worksheet = "999\n888\n777\n*  \n"
        result = solve_worksheet(io.StringIO(worksheet))
        assert result == 987 * 987 * 987

    def test_zero_in_operands(self):
        """Test with zero in operands.

        Format:
          5
          0
          *

        Numbers: 50
        Operation: *
        Expected: 50 = 50
        """
        worksheet = "5\n0\n*\n"
        result = solve_worksheet(io.StringIO(worksheet))
        assert result == 50

    def test_trailing_whitespace(self):
        """Test worksheet with trailing whitespace."""
        worksheet = "31  \n42  \n+   \n"
        result = solve_worksheet(io.StringIO(worksheet))
        assert result == 46

    def test_leading_whitespace(self):
        """Test worksheet with leading whitespace."""
        worksheet = "  31\n  42\n  +\n"
        result = solve_worksheet(io.StringIO(worksheet))
        assert result == 46

    def test_three_problems(self):
        """Test with three separate problems.

        Format:
          1 2 3
          * + *

        Problem 1 (rightmost): 3, op *  → 3
        Problem 2 (middle): 2, op +  → 2
        Problem 3 (leftmost): 1, op *  → 1

        Grand Total: 3 + 2 + 1 = 6
        """
        worksheet = "1 2 3\n* + *\n"
        result = solve_worksheet(io.StringIO(worksheet))
        assert result == 6
