"""
Advent of Code 2025 - Day 09 Part 1: Largest Red Tile Rectangle.

This module implements a solution to find the largest rectangle in a grid using
two red tiles as opposite corners. The solution consists of three main phases:

1. Input Parsing (US1): Parse red tile coordinates from "x,y" formatted input
2. Area Calculation (US2): Calculate rectangle area from two opposite corners
3. Largest Rectangle (US3): Find the maximum area among all distinct tile pairs

Example:
    Input coordinates: (2,5), (11,1), (7,3)
    Possible rectangles: (2,5)-(11,1)=36, (2,5)-(7,3)=6, (11,1)-(7,3)=8
    Output: 36 (maximum area)
"""

from itertools import combinations
from pathlib import Path


def validate_input(lines: list[str]) -> None:
    """
    Validate that input is non-empty and each line is properly formatted.

    Checks that input contains at least one line and that each line conforms
    to the "x,y" format with non-negative integer coordinates.

    Args:
        lines: List of input lines to validate

    Raises:
        ValueError: If input is empty, contains empty lines, malformed entries,
                   non-integer coordinates, or negative coordinate values
    """
    if not lines:
        raise ValueError("Input cannot be empty")

    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            raise ValueError(f"Line {i} is empty")

        parts = line.split(",")
        if len(parts) != 2:
            raise ValueError(f"Line {i} has invalid format: expected 'x,y', got '{line}'")

        try:
            x, y = int(parts[0].strip()), int(parts[1].strip())
            if x < 0 or y < 0:
                raise ValueError(f"Line {i} has negative coordinates: ({x}, {y})")
        except ValueError as e:
            if "invalid literal" in str(e):
                raise ValueError(f"Line {i} contains non-integer coordinates: '{line}'") from e
            raise


def parse_coordinates(lines: list[str]) -> list[tuple[int, int]]:
    """
    Parse red tile coordinates from input lines in "x,y" format.

    Validates input and converts each line into a tuple of (x, y) coordinates.
    Whitespace around coordinates is automatically stripped. This is the
    recommended entry point for coordinate parsing from raw input.

    Args:
        lines: List of input lines in "x,y" format, one coordinate per line

    Returns:
        List of (x, y) tuples representing red tile positions

    Raises:
        ValueError: If input validation fails (see validate_input for details)
    """
    validate_input(lines)

    coordinates = []
    for line in lines:
        line = line.strip()
        if line:
            x, y = map(int, line.split(","))
            coordinates.append((x, y))

    return coordinates


def calculate_rectangle_area(corner1: tuple[int, int], corner2: tuple[int, int]) -> int:
    """
    Calculate the area of a rectangle given two opposite corner coordinates.

    Uses the formula: area = (|x1 - x2| + 1) * (|y1 - y2| + 1)
    The formula includes both boundary tiles (inclusive on both ends).
    The function is order-invariant (corner1 and corner2 can be in any order).

    Args:
        corner1: First corner as (x, y) tuple
        corner2: Second corner as (x, y) tuple

    Returns:
        Area of the rectangle (integer)

    Example:
        >>> calculate_rectangle_area((2, 5), (11, 1))
        50  # (|2-11| + 1) * (|5-1| + 1) = 10 * 5 = 50
    """
    x1, y1 = corner1
    x2, y2 = corner2
    return (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)


def find_largest_rectangle(coordinates: list[tuple[int, int]]) -> int:
    """
    Find the largest rectangle that can be formed from distinct pairs of red tiles.

    Uses itertools.combinations to generate all distinct pairs and evaluates
    the rectangle area for each pair. Returns the maximum area found.
    This is the main logic for Part 1 of the puzzle.

    Args:
        coordinates: List of (x, y) tuples representing red tile positions

    Returns:
        Maximum rectangle area among all possible distinct pairs

    Raises:
        ValueError: If fewer than 2 tiles provided (cannot form a rectangle)

    Example:
        >>> find_largest_rectangle([(2, 5), (11, 1), (7, 3)])
        36  # Pair (2,5)-(11,1) has max area of 36
    """
    if len(coordinates) < 2:
        raise ValueError("Need at least 2 red tiles to form a rectangle")

    max_area = 0

    for pair in combinations(coordinates, 2):
        area = calculate_rectangle_area(pair[0], pair[1])
        max_area = max(max_area, area)

    return max_area


def solve_part1(coordinates: list[tuple[int, int]]) -> int:
    """
    Solve Part 1: Find the largest rectangle area from red tile coordinates.

    This is the main entry point for Part 1. It accepts parsed coordinates
    and delegates to find_largest_rectangle for the actual computation.

    Args:
        coordinates: List of (x, y) tuples representing red tile positions

    Returns:
        Maximum rectangle area (integer)

    Raises:
        ValueError: If insufficient tiles provided for forming a rectangle
    """
    return find_largest_rectangle(coordinates)


def solve_part2(data) -> int:
    """Solve Part 2 of the puzzle."""
    # TODO: Implement Part 2 solution
    return 0


def main():
    """
    Main entry point for the solution script.

    Reads puzzle input from input.txt, parses coordinates, and solves
    both Part 1 and Part 2 (Part 2 stub for future implementation).

    Expected input format:
        input.txt: One coordinate per line in "x,y" format
        Example:
            2,5
            11,1
            7,3
    """
    input_file = Path(__file__).parent / "input.txt"
    input_text = input_file.read_text()

    lines = input_text.strip().split("\n")
    coordinates = parse_coordinates(lines)

    part1_answer = solve_part1(coordinates)
    print(f"Part 1: {part1_answer}")

    part2_answer = solve_part2(coordinates)
    print(f"Part 2: {part2_answer}")


if __name__ == "__main__":
    main()
