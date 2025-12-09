"""
Parser module for Day 6, Part 1 - Vertical Math Worksheet Parser.
Implements streaming and column extraction logic per spec.

This module provides a memory-efficient streaming pipeline for parsing
vertically-formatted math worksheets where:
- Numbers are arranged in vertical columns
- Operations (+ or *) appear in the bottom row
- Problems are separated by full columns of whitespace

The pipeline processes worksheets without loading them entirely into memory:
1. read_lines_as_stream: Read input line-by-line
2. columns_from_lines: Convert lines to vertical columns
3. problem_column_groups: Group columns by separator boundaries
4. extract_problem: Parse each group into a Problem

Example:
    >>> import parser
    >>> lines = parser.read_lines_as_stream("worksheet.txt")
    >>> cols = parser.columns_from_lines(lines)
    >>> groups = parser.problem_column_groups(cols)
    >>> for group in groups:
    ...     problem = parser.extract_problem(group)
    ...     print(f"Problem: {problem.operands} {problem.operation}")
"""

from dataclasses import dataclass
from typing import List, Iterator, Union, IO, Optional, Any
from pathlib import Path

# Type aliases
Line = str
Lines = Iterator[Line]


@dataclass
class Column:
    """A vertical column from the worksheet containing values from each row."""

    index: int
    values: List[str]  # Character at this column position for each row

    @property
    def is_separator(self) -> bool:
        """True if this column contains only whitespace (problem boundary)."""
        return all(v.isspace() or v == "" for v in self.values)

    @property
    def content(self) -> str:
        """Non-whitespace content in this column (e.g., digits or operation symbol)."""
        return "".join(v for v in self.values if not v.isspace())


@dataclass
class ProblemGroup:
    """A collection of adjacent columns representing one math problem."""

    start_column: int  # Index of first column in this group
    end_column: int  # Index of last column in this group
    columns: List[Column]  # The columns in this group

    @property
    def width(self) -> int:
        """Number of columns in this group."""
        return len(self.columns)

    @property
    def height(self) -> int:
        """Number of rows (determined by column values)."""
        return len(self.columns[0].values) if self.columns else 0


# Type aliases
Columns = Iterator[Column]
ProblemGroups = Iterator[ProblemGroup]


def read_lines_as_stream(source: Union[str, Path, IO]) -> Iterator[str]:
    """
    Yield lines from a file or file-like object without loading entire file into memory.

    Args:
        source: File path (str or Path), or file-like object (IO)

    Yields:
        str: Individual lines (including newline characters)

    Raises:
        FileNotFoundError: If source is a path that doesn't exist
        IOError: If file cannot be read
    """
    if isinstance(source, (str, Path)):
        with open(source, "r") as f:
            for line in f:
                yield line
    else:
        for line in source:
            yield line


def columns_from_lines(lines: Iterator[str]) -> Iterator[Column]:
    """
    Transform line stream into column stream.

    Converts a stream of lines (as strings) into a stream of Column objects,
    where each column contains the characters at that position from all lines.

    Args:
        lines: Iterator of line strings (including newlines)

    Yields:
        Column: Column objects with index, values, and properties

    Raises:
        ValueError: If lines have inconsistent lengths
    """
    # Read all lines into memory to determine height
    all_lines = list(lines)

    if not all_lines:
        return

    # Strip newlines to get actual content
    stripped_lines = [line.rstrip("\n\r") for line in all_lines]

    # Determine width (max line length)
    width = max(len(line) for line in stripped_lines) if stripped_lines else 0

    # Pad all lines to same length
    padded_lines = [line.ljust(width) for line in stripped_lines]

    # Generate columns
    for col_idx in range(width):
        values = [line[col_idx] for line in padded_lines]
        yield Column(index=col_idx, values=values)


def extract_problem(problem_group: ProblemGroup) -> "Problem":
    """
    Extract a single problem from a group of columns.

    Each ROW (except the last) contains one operand, read horizontally across all
    columns in this group. Numbers are right-aligned within the column span.

    Args:
        problem_group: A ProblemGroup containing columns of a single problem

    Returns:
        Problem: The parsed problem with operands, operation, and result

    Raises:
        ValueError: If problem format is invalid (no operation found, etc.)
    """
    from utils import Problem

    if not problem_group.columns:
        raise ValueError("Problem group has no columns")

    height = problem_group.height
    if height < 2:
        raise ValueError("Problem must have at least 2 rows (operands and operation)")

    # Get operation from last row
    last_row = [col.values[-1] for col in problem_group.columns]
    operation_char = None
    for char in last_row:
        if char in ["+", "*"]:
            operation_char = char
            break

    if operation_char is None:
        raise ValueError("No operation found in last row")

    # Read each row (except last) horizontally to get operands
    operands = []

    for row_idx in range(height - 1):  # Exclude last row (operation row)
        # Get the characters from all columns in this row
        row_chars = [col.values[row_idx] for col in problem_group.columns]

        # Join into a string and strip whitespace to get the number
        row_str = "".join(row_chars).strip()

        # Extract digits only
        digit_str = "".join(c for c in row_str if c.isdigit())

        if digit_str:
            operands.append(int(digit_str))

    if not operands:
        raise ValueError("No operands found in problem")

    # Evaluate the problem
    if operation_char == "+":
        result = sum(operands)
    else:  # "*"
        result = 1
        for op in operands:
            result *= op

    return Problem(operands=operands, operation=operation_char, result=result)


def problem_column_groups(columns: Iterator[Column]) -> Iterator[ProblemGroup]:
    """
    Group columns into problems based on separator columns.

    A separator column is one containing only whitespace. Consecutive non-separator
    columns form a single problem group.

    Args:
        columns: Iterator of Column objects from the worksheet

    Yields:
        ProblemGroup: Groups of contiguous non-separator columns
    """
    all_columns = list(columns)

    if not all_columns:
        return

    start_idx = None

    for idx, col in enumerate(all_columns):
        if col.is_separator:
            # End of a problem group
            if start_idx is not None:
                yield ProblemGroup(
                    start_column=start_idx, end_column=idx - 1, columns=all_columns[start_idx:idx]
                )
                start_idx = None
        else:
            # Start of a problem group
            if start_idx is None:
                start_idx = idx

    # Don't forget the last group if it ends at the last column
    if start_idx is not None:
        yield ProblemGroup(
            start_column=start_idx, end_column=len(all_columns) - 1, columns=all_columns[start_idx:]
        )


def problem_column_groups_part2(columns: Iterator[Column]) -> Iterator[ProblemGroup]:
    """
    Group columns into problems based on separator columns (Part 2 version: right-to-left).

    For Part 2, we identify problems by finding separator columns (columns of only whitespace),
    then group adjacent non-separator columns. We yield groups from right-to-left.

    Args:
        columns: Iterator of Column objects from the worksheet

    Yields:
        ProblemGroup: Groups of contiguous non-separator columns (yielded right-to-left)
    """
    all_columns = list(columns)

    if not all_columns:
        return

    # Find all groups (left-to-right)
    groups = []
    start_idx = None

    for idx, col in enumerate(all_columns):
        if col.is_separator:
            # End of a problem group
            if start_idx is not None:
                group_cols = all_columns[start_idx:idx]
                groups.append(
                    ProblemGroup(
                        start_column=start_idx,
                        end_column=idx - 1,
                        columns=group_cols,
                    )
                )
                start_idx = None
        else:
            # Start of a problem group
            if start_idx is None:
                start_idx = idx

    # Don't forget the last group if it ends at the last column
    if start_idx is not None:
        group_cols = all_columns[start_idx:]
        groups.append(
            ProblemGroup(
                start_column=start_idx,
                end_column=len(all_columns) - 1,
                columns=group_cols,
            )
        )

    # Yield groups in right-to-left order
    for group in reversed(groups):
        # Also reverse the columns within each group for right-to-left reading
        reversed_cols = list(reversed(group.columns))
        yield ProblemGroup(
            start_column=group.start_column,
            end_column=group.end_column,
            columns=reversed_cols,
        )


def extract_problem_part2(problem_group: ProblemGroup) -> "Problem":
    """
    Extract a single problem from a group of columns (Part 2 version: right-to-left).

    For Part 2:
    - Each COLUMN (except the last row) contains one operand, read top-to-bottom
    - The operator is the symbol at the BOTTOM of each column
    - Numbers are reconstructed by joining digits in a column (top = most significant)

    Args:
        problem_group: A ProblemGroup containing columns of a single problem

    Returns:
        Problem: The parsed problem with operands, operation, and result

    Raises:
        ValueError: If problem format is invalid
    """
    from utils import Problem

    if not problem_group.columns:
        raise ValueError("Problem group has no columns")

    height = problem_group.height
    if height < 2:
        raise ValueError("Problem must have at least 2 rows (operands and operation)")

    # Get operation from last row (bottom of problem)
    last_row = [col.values[-1] for col in problem_group.columns]
    operation_char = None
    for char in last_row:
        if char in ["+", "*"]:
            operation_char = char
            break

    if operation_char is None:
        raise ValueError("No operation found in last row")

    # Extract operands: each column (except last row) gives one number
    # Read column top-to-bottom (most significant digit at top)
    operands = []

    for col in problem_group.columns:
        # Read digits from top to bottom of this column (excluding the operator row)
        digits = []
        for row_idx in range(height - 1):  # Exclude last row (operation row)
            char = col.values[row_idx]
            if char.isdigit():
                digits.append(char)

        # Reconstruct the number from digits
        if digits:
            number_str = "".join(digits)
            operands.append(int(number_str))

    if not operands:
        raise ValueError("No operands found in problem")

    # Evaluate the problem
    if operation_char == "+":
        result = sum(operands)
    else:  # "*"
        result = 1
        for op in operands:
            result *= op

    return Problem(operands=operands, operation=operation_char, result=result)
