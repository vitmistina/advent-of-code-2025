"""
Utility module for Day 6 - Cephalopod Math Worksheet Solver.
Provides shared components between Part 1 and Part 2 solutions.

This module contains:
- Problem dataclass: Used by both Part 1 and Part 2
- evaluate_problem: Evaluation logic shared by both parts
- Type aliases: Common type definitions

Both Part 1 (vertical columns, left-to-right) and Part 2 (vertical columns, right-to-left)
use the same data model and evaluation logic. Only the parsing/grouping logic differs.
"""

from dataclasses import dataclass
from typing import List

# Type aliases
Operands = List[int]
Operation = str


@dataclass
class Problem:
    """
    A parsed math problem with operands, operation, and result.
    
    Used by both Part 1 and Part 2 solutions. The data model is generic
    and works for both left-to-right and right-to-left column reading.
    
    Attributes:
        operands: List of integer operands
        operation: Operation symbol ('+' or '*')
        result: Pre-computed result of applying the operation to operands
    """

    operands: List[int]
    operation: str  # '+' or '*'
    result: int


def evaluate_problem(problem: Problem) -> int:
    """
    Evaluate a math problem by applying the operation to all operands.

    This function is shared between Part 1 and Part 2 since the evaluation
    logic is identical. Only the parsing differs between the two parts.

    Args:
        problem: Problem with operands and operation

    Returns:
        int: The result of applying the operation to all operands

    Raises:
        ValueError: If operation is not '+' or '*'
    """
    if problem.operation == "+":
        return sum(problem.operands)
    elif problem.operation == "*":
        result = 1
        for operand in problem.operands:
            result *= operand
        return result
    else:
        raise ValueError(f"Unknown operation: {problem.operation}")
