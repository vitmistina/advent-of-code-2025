"""
Unit tests for day-06/solution.py (User Story 1: evaluate_problem)
"""

import pytest
import solution


def test_evaluate_problem_multiplication():
    """Evaluate a multiplication problem."""
    problem = solution.Problem(operands=[2, 3, 4], operation="*", result=0)
    result = solution.evaluate_problem(problem)
    assert result == 24


def test_evaluate_problem_addition():
    """Evaluate an addition problem."""
    problem = solution.Problem(operands=[10, 20, 30], operation="+", result=0)
    result = solution.evaluate_problem(problem)
    assert result == 60


def test_evaluate_problem_single_operand():
    """Evaluate problem with single operand."""
    problem = solution.Problem(operands=[42], operation="+", result=0)
    result = solution.evaluate_problem(problem)
    assert result == 42


def test_evaluate_problem_large_multiplication():
    """Evaluate multiplication of large numbers."""
    problem = solution.Problem(operands=[123, 45, 6], operation="*", result=0)
    result = solution.evaluate_problem(problem)
    assert result == 123 * 45 * 6
