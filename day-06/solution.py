"""
Solution module for Day 6, Part 1 - Vertical Math Worksheet Parser.
Implements problem evaluation and worksheet solving logic per spec.

This module provides:
- solve_worksheet: Main entry point to solve an entire worksheet

The solve_worksheet function provides a complete streaming pipeline that
processes worksheets of arbitrary size without loading them entirely into memory.

The Problem dataclass and evaluate_problem logic are shared with Part 2 in utils.py.

Example:
    >>> import solution
    >>> # From file
    >>> total = solution.solve_worksheet("worksheet.txt", verbose=True)
    >>> print(f"Grand Total: {total}")

    >>> # From string
    >>> import io
    >>> worksheet = "12 34\\n56 78\\n*  + \\n"
    >>> total = solution.solve_worksheet(io.StringIO(worksheet))
    >>> # Problem 1: 15 * 26 = 390
    >>> # Problem 2: 37 + 48 = 85
    >>> # Total: 475
    >>> assert total == 475
"""

from typing import Union, Any
from pathlib import Path

# Import shared components
from .utils import Problem, evaluate_problem


def solve_worksheet(
    source: Union[str, Path, Any], verbose: bool = False, debug: bool = False
) -> int:
    """
    Solve a complete worksheet and return the grand total of all problem results.

    This function implements the full streaming pipeline:
    read_lines_as_stream → columns_from_lines → problem_column_groups →
    extract_problem → evaluate_problem → sum results

    Args:
        source: File path (str or Path) or file-like object (IO)
        verbose: Print problem details and results
        debug: Print detailed debug information

    Returns:
        int: Grand total (sum of all problem results)

    Raises:
        FileNotFoundError: If source is a path that doesn't exist
        IOError: If file cannot be read
        ValueError: If problem parsing fails
    """
    # Import here to avoid circular imports
    from parser import (
        read_lines_as_stream,
        columns_from_lines,
        problem_column_groups,
        extract_problem,
    )

    # Initialize grand total
    grand_total = 0
    problem_count = 0

    try:
        # Stream the lines from the source
        lines = read_lines_as_stream(source)

        # Transform lines to columns
        cols = columns_from_lines(lines)

        # Group columns into problems
        groups = problem_column_groups(cols)

        # Process each problem
        for group in groups:
            problem = extract_problem(group)
            result = evaluate_problem(problem)
            grand_total += result
            problem_count += 1

            if debug:
                print(
                    f"[DEBUG] Problem {problem_count}: operands={problem.operands}, "
                    f"operation={problem.operation}, result={result}"
                )
            elif verbose:
                print(
                    f"Problem {problem_count}: {' '.join(str(op) for op in problem.operands)} "
                    f"{problem.operation} = {result}"
                )

        if verbose and problem_count > 0:
            print(f"Grand Total: {grand_total}")

        return grand_total

    except Exception as e:
        if debug:
            print(f"[DEBUG] Error processing worksheet: {e}")
        raise


def main():
    """Main entry point for running the solution."""
    import os
    from pathlib import Path

    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    input_file = script_dir / "input.txt"

    total = solve_worksheet(str(input_file), verbose=True)
    print(f"\n✨ Grand Total: {total}")


if __name__ == "__main__":
    main()
