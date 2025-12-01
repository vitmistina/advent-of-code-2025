"""Advent of Code 2025 - Day 01 Solution."""

from pathlib import Path


def parse_input(input_text: str) -> list[tuple[str, int]]:
    """
    Parse the puzzle input into list of (direction, distance) tuples.

    Args:
        input_text: Multi-line string containing rotation instructions.
                   Each line format: <direction><distance> (e.g., "L68", "R48")

    Returns:
        List of (direction, distance) tuples where:
        - direction: 'L' or 'R'
        - distance: integer number of clicks

    Example:
        >>> parse_input("L68\\nR48")
        [('L', 68), ('R', 48)]
    """
    if not input_text.strip():
        return []

    rotations = []
    for line in input_text.strip().split("\n"):
        if not line.strip():
            continue
        direction = line[0]
        distance = int(line[1:])
        rotations.append((direction, distance))
    return rotations


def apply_rotation(position: int, direction: str, distance: int) -> int:
    """
    Apply a single rotation to the dial and return new position.

    The dial is circular with positions 0-99. Left rotation decreases position,
    right rotation increases position, with wraparound at boundaries.

    Args:
        position: Current dial position (0-99)
        direction: 'L' for left (decrease) or 'R' for right (increase)
        distance: Number of clicks to rotate

    Returns:
        New dial position after rotation (0-99)

    Examples:
        >>> apply_rotation(50, 'L', 68)
        82
        >>> apply_rotation(99, 'R', 1)
        0
        >>> apply_rotation(5, 'L', 10)
        95
    """
    if direction == "L":
        return (position - distance) % 100
    else:  # direction == "R"
        return (position + distance) % 100


def solve_part1(rotations: list[tuple[str, int]]) -> int:
    """
    Solve Part 1: Count how many times dial points at 0 after rotations.

    The dial starts at position 50. For each rotation in sequence:
    1. Apply the rotation to get new position
    2. If new position is 0, increment the count

    Args:
        rotations: List of (direction, distance) tuples

    Returns:
        Number of times the dial pointed at 0 after any rotation

    Example:
        >>> rotations = [('L', 68), ('L', 30), ('R', 48)]
        >>> solve_part1(rotations)
        1
    """
    position = 50  # Dial starts at 50
    zero_count = 0

    for direction, distance in rotations:
        position = apply_rotation(position, direction, distance)
        if position == 0:
            zero_count += 1

    return zero_count


def solve_part2(data) -> int:
    """Solve Part 2 of the puzzle."""
    # TODO: Implement Part 2 solution
    return 0


def main():
    """Main entry point."""
    input_file = Path(__file__).parent / "input.txt"
    input_text = input_file.read_text()

    data = parse_input(input_text)

    part1_answer = solve_part1(data)
    print(f"Part 1: {part1_answer}")

    part2_answer = solve_part2(data)
    print(f"Part 2: {part2_answer}")


if __name__ == "__main__":
    main()
