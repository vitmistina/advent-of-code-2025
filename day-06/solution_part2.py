"""
Solution module for Day 6, Part 2 - Cephalopod Math (Right-to-Left Columns).
Implements problem evaluation and worksheet solving logic for right-to-left columns.

This module provides:
- solve_worksheet: Main entry point to solve an entire worksheet (Part 2 specific)

The solve_worksheet function reuses the data model (Problem) and evaluation logic
(evaluate_problem) from utils.py, with only the parsing/grouping logic specific to Part 2.

The solve_worksheet function provides a complete streaming pipeline that
processes worksheets of arbitrary size without loading them entirely into memory.

Key differences from Part 1:
- Numbers are reconstructed by reading columns right-to-left
- Columns are grouped right-to-left
- Each number is extracted top-to-bottom from a column (most significant digit at top)

Example:
    >>> import solution_part2
    >>> # From file
    >>> total = solution_part2.solve_worksheet("worksheet.txt", verbose=True)
    >>> print(f"Grand Total: {total}")

    >>> # From string
    >>> import io
    >>> worksheet = '''123 328  51 64
    ...  45 64  387 23
    ...   6 98  215 314
    ... *   +   *   +
    ... '''
    >>> total = solution_part2.solve_worksheet(io.StringIO(worksheet))
    >>> # Grand Total: 3263827
    >>> assert total == 3263827
"""

from typing import Union, Any
from pathlib import Path

# Import shared components
from .utils import Problem, evaluate_problem


def solve_worksheet(
    source: Union[str, Path, Any], verbose: bool = False, debug: bool = False
) -> int:
    """
    Solve a complete worksheet (Part 2 - right-to-left columns) and return the grand total.

    This function implements the full streaming pipeline for Part 2:
    read_lines_as_stream → columns_from_lines → problem_column_groups_part2 →
    extract_problem_part2 → evaluate_problem → sum results

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
        problem_column_groups_part2,
        extract_problem_part2,
    )

    # Initialize grand total
    grand_total = 0
    problem_count = 0

    try:
        # Stream the lines from the source
        lines = read_lines_as_stream(source)

        # Transform lines to columns
        cols = columns_from_lines(lines)

        # Group columns into problems (Part 2 version: right-to-left)
        groups = problem_column_groups_part2(cols)

        # Process each problem
        for group in groups:
            problem = extract_problem_part2(group)
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
    print(f"\n✨ Grand Total (Part 2): {total}")


if __name__ == "__main__":
    main()
